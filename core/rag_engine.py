# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : rag_engine.py
# Time       : 2024/12/25 16:58
# Author     : Feiren Cheng
# Description: 
"""
import os
from typing import List, Dict

from langchain.prompts import ChatPromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader, WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from common.exceptions.model import ModelTokenLimitError, ModelInferenceError
from common.exceptions.rag import DocumentIngestionError, ChunkingError, VectorStoreError
from common.logging.loggers import MultiModelRAGLogger
from ..models.base import ModelAdapter, EmbeddingAdapter
from ..utils.conversation import ConversationManager


class MultiModelRAGSystem:
    def __init__(
            self,
            model_adapter: ModelAdapter,
            embedding_adapter: EmbeddingAdapter,
            persist_directory: str = "./rag_db",
            chunk_size: int = 2000,  # 增加默认chunk大小
            chunk_overlap: int = 400,  # 相应增加overlap
            log_dir: str = "logs"
    ):
        # Initialize logger
        self.logger = MultiModelRAGLogger(log_dir=log_dir)

        self.model_adapter = model_adapter
        self.llm = model_adapter.llm

        # Initialize embeddings
        self.embedding_adapter = embedding_adapter
        self.embeddings = embedding_adapter.embeddings

        # Initialize vector store
        self.persist_directory = persist_directory

        # Try to load existing vector store
        if os.path.exists(persist_directory):
            self.vector_store = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings
            )
            print(f"Loaded existing vector store from {persist_directory}")
        else:
            self.vector_store = None
            print(f"No existing vector store found at {persist_directory}")

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True,
        )

        self.conversation_manager = ConversationManager()

        # Initialize conversation history
        self.conversation_history: List[Dict] = []

        # Enhanced RAG prompts
        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant. Use the following context to answer the question.
                              If the context contains multiple relevant pieces of information, make sure to synthesize them all.
                              If you cannot find sufficient information in the context, please say so."""),
            ("system", "Relevant context:\n{context}"),
            ("system", "Conversation history:\n{history}"),
            ("human", "{question}")
        ])

    def _get_enhanced_retriever(self, search_type: str = "similarity", k: int = 5):
        """Get an enhanced retriever with post-processing"""
        base_retriever = self.vector_store.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k}
        )

        # 创建LLM压缩器来提取最相关的内容
        compressor = LLMChainExtractor.from_llm(self.llm)

        # 创建上下文压缩检索器
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )

        return compression_retriever

    def _format_history(self) -> str:
        """Format conversation history for prompt"""
        formatted = []
        for msg in self.conversation_history[-5:]:
            formatted.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(formatted)

    async def ingest_documents(self, file_paths: List[str], force_reprocess: bool = False):
        """
        Ingest documents into the vector store

        Args:
            file_paths: List of paths to documents
            force_reprocess: If True, reprocess documents even if vector store exists
        """
        # If vector store exists and force_reprocess is False, skip ingestion
        if self.vector_store is not None and not force_reprocess:
            self.logger.log_process(process_name="document_ingestion",
                                    status="skipped",
                                    file_paths=file_paths,
                                    force_reprocess=force_reprocess)
            return

        for file_path in file_paths:
            try:
                self.logger.log_process(
                    process_name="document_ingestion",
                    status="started",
                    file_path=file_path
                )
                if file_path.endswith('.txt'):
                    loader = TextLoader(file_path)
                elif file_path.endswith('.pdf'):
                    loader = PyPDFLoader(file_path)
                elif file_path.startswith('http'):
                    loader = WebBaseLoader(file_path)
                else:
                    raise DocumentIngestionError(file_path=file_path, error_details="Unsupported file format")
                documents = loader.load()
                try:
                    splits = self.text_splitter.split_documents(documents)
                except Exception as e:
                    raise ChunkingError(
                        text_length=len(str(documents)),
                        chunk_size=self.text_splitter.chunk_size,
                        details={"error": str(e)}
                    )

                # Create new vector store or add to existing one
                try:
                    if self.vector_store is None:
                        self.vector_store = Chroma.from_documents(
                            documents=splits,
                            embedding=self.embeddings,
                            persist_directory=self.persist_directory
                        )
                        print(f"Created new vector store at {self.persist_directory}")
                    else:
                        self.vector_store.add_documents(splits)
                        print("Added new documents to existing vector store")
                except Exception as e:
                    raise VectorStoreError(
                        operation="document_storage",
                        error_details=str(e)
                    )

                self.logger.log_process(
                    process_name="document_ingestion",
                    status="completed",
                    file_path=file_path,
                    document_count=len(splits)
                )
            except Exception as e:
                self.logger.log_process(
                    process_name="document_ingestion",
                    status="failed",
                    file_path=file_path,
                    error=str(e)
                )
                raise

    def get_document_count(self) -> int:
        """Get the number of documents in the vector store"""
        if self.vector_store is None:
            return 0
        return self.vector_store._collection.count()

    def clear_vector_store(self):
        """Clear all documents from the vector store"""
        if self.vector_store is not None:
            self.vector_store._collection.delete(where={})
            self.vector_store.persist()
            print("Vector store cleared successfully")

    async def generate_response(
            self,
            question: str,
            stream: bool = False,
            use_history: bool = True,
            k: int = 5  # 增加可配置的检索文档数量
    ) -> str:
        """Generate a response using RAG"""
        try:
            if self.vector_store is None:
                raise VectorStoreError(
                    operation="retrieval",
                    error_details="No documents ingested yet"
                )

            self.logger.log_process(
                process_name="response_generation",
                status="started",
                question=question
            )

            self.conversation_manager.add_message("human", question)

            try:
                retriever = self.vector_store.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": k}
                )
                qa_chain = (
                        {
                            "context": retriever,
                            "question": RunnablePassthrough(),
                            "history": (lambda x: self._format_history()) if use_history else (
                                lambda x: "No history used")
                        }
                        | self.qa_prompt
                        | self.llm
                        | StrOutputParser()
                )
                if stream:
                    response = ""
                    async for chunk in qa_chain.astream(question):
                        response += chunk
                        yield chunk

                    self.conversation_manager.add_message("assistant", response)
                else:
                    response = await qa_chain.ainvoke(question)
                    self.conversation_manager.add_message("assistant", response)
                    yield response

            except Exception as e:
                if "token limit exceeded" in str(e).lower():
                    raise ModelTokenLimitError(
                        model_name=self.model_adapter.config.model_name,
                        token_count=0,  # You might want to calculate this
                        token_limit=0,  # You might want to get this from model config
                        details={"error": str(e)}
                    )
                else:
                    raise ModelInferenceError(
                        model_name=self.model_adapter.config.model_name,
                        details={"error": str(e)}
                    )
        except Exception as e:
            self.logger.log_process(
                process_name="response_generation",
                status="failed",
                question=question,
                error=str(e)
            )
            raise
