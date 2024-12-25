from typing import Optional, Dict, Any
from http import HTTPStatus
from .base import MultiModelRAGException

class RAGError(MultiModelRAGException):
    """Base exception class for RAG-related errors"""
    def __init__(
        self,
        message: str,
        status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
        error_code: str = "RAG_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, status_code, error_code, details)

class DocumentIngestionError(RAGError):
    """Exception for document ingestion errors"""
    def __init__(self, file_path: str, error_details: str,
                 details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details.update({
            "file_path": file_path,
            "error_details": error_details
        })
        super().__init__(
            message=f"Failed to ingest document: {file_path}",
            status_code=HTTPStatus.BAD_REQUEST,
            error_code="DOCUMENT_INGESTION_ERROR",
            details=details
        )

class VectorStoreError(RAGError):
    """Exception for vector store related errors"""
    def __init__(self, operation: str, error_details: str,
                 details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details.update({
            "operation": operation,
            "error_details": error_details
        })
        super().__init__(
            message=f"Vector store error during {operation}",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            error_code="VECTOR_STORE_ERROR",
            details=details
        )

class EmbeddingError(RAGError):
    """Exception for embedding generation errors"""
    def __init__(self, text_length: int, error_details: str,
                 details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details.update({
            "text_length": text_length,
            "error_details": error_details
        })
        super().__init__(
            message="Failed to generate embeddings",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            error_code="EMBEDDING_ERROR",
            details=details
        )

class DocumentNotFoundError(RAGError):
    """Exception for when a requested document is not found"""
    def __init__(self, document_id: str, details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details["document_id"] = document_id
        super().__init__(
            message=f"Document not found: {document_id}",
            status_code=HTTPStatus.NOT_FOUND,
            error_code="DOCUMENT_NOT_FOUND",
            details=details
        )

class ChunkingError(RAGError):
    """Exception for text chunking errors"""
    def __init__(self, text_length: int, chunk_size: int,
                 details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details.update({
            "text_length": text_length,
            "chunk_size": chunk_size
        })
        super().__init__(
            message="Error during text chunking",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            error_code="CHUNKING_ERROR",
            details=details
        )

class RetrievalError(RAGError):
    """Exception for document retrieval errors"""
    def __init__(self, query: str, error_details: str,
                 details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details.update({
            "query": query,
            "error_details": error_details
        })
        super().__init__(
            message="Failed to retrieve relevant documents",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            error_code="RETRIEVAL_ERROR",
            details=details
        )
