# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : model_constants.py
# Time       : 2024/12/24 10:21
# Author     : Feiren Cheng
# Description: 
"""
from typing import Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class ModelProvider(Enum):
    """Enum for model providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    ZHIPUAI = "zhipuai"
    XAI = "xai"


@dataclass(frozen=True)
class ModelConstants:
    """Constants related to model configurations"""
    # Default model names
    DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"
    DEFAULT_CLAUDE_MODEL = "claude-3-sonnet-20240229"
    DEFAULT_ZHIPUAI_MODEL = "glm-4-flash"

    # Token limits
    MAX_TOKENS_GPT35 = 4096
    MAX_TOKENS_GPT4 = 8192
    MAX_TOKENS_CLAUDE = 200000
    MAX_TOKENS_ZHIPUAI = 8192

    # Embedding models
    DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
    EMBEDDING_DIMENSION = 1536

    # Timeout settings (in seconds)
    DEFAULT_REQUEST_TIMEOUT = 30
    LONG_RUNNING_TIMEOUT = 120

    # Rate limits
    DEFAULT_RATE_LIMIT = 10  # requests per minute
    BATCH_RATE_LIMIT = 5  # batch requests per minute

    # Cost related
    MODEL_COSTS: Tuple[Tuple[str, float]] = (
        ("gpt-3.5-turbo", 0.0015),
        ("gpt-4", 0.03),
        ("claude-3-sonnet-20240229", 0.01),
        ("glm-4-flash", 0.02)
    )


class ChunkingConstants:
    """Constants related to text chunking"""
    DEFAULT_CHUNK_SIZE = 1000
    DEFAULT_CHUNK_OVERLAP = 200
    MIN_CHUNK_SIZE = 100
    MAX_CHUNK_SIZE = 2000

    # Special chunking rules
    CODE_CHUNK_SIZE = 1500
    PDF_CHUNK_SIZE = 800
    MARKDOWN_CHUNK_SIZE = 1200


class VectorDBConstants:
    """Constants related to vector database operations"""
    DEFAULT_TOP_K = 3
    MAX_TOP_K = 10
    MIN_SIMILARITY_SCORE = 0.7
    DEFAULT_BATCH_SIZE = 100
    DEFAULT_UPDATE_BATCH_SIZE = 50
    REINDEX_THRESHOLD = 1000
