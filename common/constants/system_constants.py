# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : system_constants.py
# Time       : 2024/12/24 10:55
# Author     : Feiren Cheng
# Description: 
"""
import os
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


class Environment(Enum):
    """Environment enum"""
    DEV = "development"
    TEST = "testing"
    PROD = "production"


class LogLevel(Enum):
    """Log level enum"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class PathConstants:
    """Constants related to file paths"""
    # Base directories
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    LOGS_DIR: Path = BASE_DIR / "logs"
    CACHE_DIR: Path = BASE_DIR / "cache"

    # Vector store
    VECTOR_DB_DIR: Path = DATA_DIR / "vector_store"

    # Document directories
    UPLOAD_DIR: Path = DATA_DIR / "uploads"
    PROCESSED_DIR: Path = DATA_DIR / "processed"
    FAILED_DIR: Path = DATA_DIR / "failed"

    # Cache directories
    EMBEDDING_CACHE: Path = CACHE_DIR / "embeddings"
    MODEL_CACHE: Path = CACHE_DIR / "models"


@dataclass(frozen=True)
class SecurityConstants:
    """Constants related to security"""
    TOKEN_EXPIRY = 3600  # seconds
    MAX_LOGIN_ATTEMPTS = 3
    PASSWORD_MIN_LENGTH = 8
    RATE_LIMIT_WINDOW = 60  # seconds
    MAX_SESSION_DURATION = 24 * 3600  # 24 hours
    ALLOWED_ORIGINS = ["localhost", "127.0.0.1"]

    # File security
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {".txt", ".pdf", ".md", ".doc", ".docx"}

    # API security
    API_RATE_LIMIT = 100  # requests per minute
    MAX_CONCURRENT_REQUESTS = 10


@dataclass(frozen=True)
class CacheConstants:
    """Constants related to caching"""
    DEFAULT_TTL = 3600  # 1 hour
    MAX_CACHE_SIZE = 1000  # items
    EMBEDDING_CACHE_TTL = 24 * 3600  # 24 hours
    RESPONSE_CACHE_TTL = 300  # 5 minutes

    # Cache keys
    EMBEDDING_KEY_PREFIX = "embed:"
    MODEL_KEY_PREFIX = "model:"
    RESPONSE_KEY_PREFIX = "resp:"
