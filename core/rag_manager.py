# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : rag_manager.py
# Time       : 2024/12/24 10:13
# Author     : Feiren Cheng
# Description: 
"""
from typing import Dict, Optional, List

from common.constants.model_constants import ModelProvider
from common.constants.system_constants import PathConstants
from common.mappings.model_mappings import ModelMappings
from config.model_config import ModelConfig
from .rag_engine import MultiModelRAGSystem


class MultiModelRAGManager:
    def __init__(self):
        self.rag_sessions: Dict[str, MultiModelRAGSystem] = {}
        self.model_mappings = ModelMappings()

    def create_session(
            self,
            session_id: str,
            model_type: ModelProvider,
            model_config: ModelConfig,
            embedding_config: ModelConfig,
    ) -> MultiModelRAGSystem:
        """Create a new RAG session with specified model"""
        if (model_type not in self.model_mappings.MODEL_ADAPTER_MAP
                or model_type not in self.model_mappings.EMBEDDING_ADAPTER_MAP):
            raise ValueError(f"Unsupported model type: {model_type}")

        model_adapter = self.model_mappings.get_model_adapter(model_type, model_config)
        embedding_adapter = self.model_mappings.get_embedding_adapter(model_type, embedding_config)

        self.rag_sessions[session_id] = MultiModelRAGSystem(
            model_adapter=model_adapter,
            embedding_adapter=embedding_adapter,
            persist_directory=PathConstants.VECTOR_DB_DIR.__str__(),
            chunk_size=2000,  # 增加默认chunk大小
            chunk_overlap=400,  # 相应增加overlap
            log_dir=PathConstants.LOGS_DIR.__str__()
        )
        return self.rag_sessions[session_id]

    def get_session(self, session_id: str) -> Optional[MultiModelRAGSystem]:
        """Get an existing RAG session"""
        return self.rag_sessions.get(session_id)

    def list_sessions(self) -> List[str]:
        """List all session IDs"""
        return list(self.rag_sessions.keys())
