# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : enums.py
# Time       : 2024/12/24 10:58
# Author     : Feiren Cheng
# Description: 
"""
from enum import Enum, auto


class DocumentStatus(Enum):
    """Document processing status"""
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()
    ARCHIVED = auto()


class ProcessingPriority(Enum):
    """Processing priority levels"""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    URGENT = auto()


class FileType(Enum):
    """Supported file types"""
    TXT = "text/plain"
    PDF = "application/pdf"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    MD = "text/markdown"
    HTML = "text/html"


class ResponseFormat(Enum):
    """Response format types"""
    TEXT = "text"
    JSON = "json"
    MARKDOWN = "markdown"
    HTML = "html"


class ModelRole(Enum):
    """Model roles in the system"""
    PRIMARY = "primary"
    FALLBACK = "fallback"
    SPECIALIZED = "specialized"
    EXPERIMENTAL = "experimental"


class UserRole(Enum):
    """User roles in the system"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
    API = "api"


class SubscriptionTier(Enum):
    """Subscription tiers"""
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
