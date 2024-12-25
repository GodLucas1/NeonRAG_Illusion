# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : error_constants.py
# Time       : 2024/12/24 10:57
# Author     : Feiren Cheng
# Description: 
"""
from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus


class ErrorCategory(Enum):
    """Error category enum"""
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    BUSINESS = "business"
    SYSTEM = "system"
    EXTERNAL = "external"


class ErrorSeverity(Enum):
    """Error severity enum"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class ErrorCodes:
    """Error code constants"""
    # Authentication errors
    AUTH_INVALID_TOKEN = "AUTH_001"
    AUTH_EXPIRED_TOKEN = "AUTH_002"
    AUTH_MISSING_TOKEN = "AUTH_003"

    # Validation errors
    VALIDATION_INVALID_INPUT = "VAL_001"
    VALIDATION_MISSING_FIELD = "VAL_002"
    VALIDATION_INVALID_FORMAT = "VAL_003"

    # Model errors
    MODEL_NOT_FOUND = "MODEL_001"
    MODEL_LOAD_FAILED = "MODEL_002"
    MODEL_INFERENCE_FAILED = "MODEL_003"

    # Document errors
    DOC_NOT_FOUND = "DOC_001"
    DOC_INVALID_FORMAT = "DOC_002"
    DOC_TOO_LARGE = "DOC_003"

    # System errors
    SYSTEM_DATABASE_ERROR = "SYS_001"
    SYSTEM_CACHE_ERROR = "SYS_002"
    SYSTEM_FILE_ERROR = "SYS_003"


@dataclass(frozen=True)
class ErrorMessages:
    """Error message templates"""
    # Authentication
    INVALID_TOKEN = "Invalid authentication token provided"
    EXPIRED_TOKEN = "Authentication token has expired"
    MISSING_TOKEN = "Authentication token is required"

    # Validation
    INVALID_INPUT = "Invalid input provided: {details}"
    MISSING_FIELD = "Required field missing: {field}"
    INVALID_FORMAT = "Invalid format for field: {field}"

    # Model
    MODEL_NOT_FOUND = "Model {model_name} not found"
    MODEL_LOAD_FAILED = "Failed to load model {model_name}"
    MODEL_INFERENCE_FAILED = "Model inference failed: {details}"

    # Document
    DOC_NOT_FOUND = "Document {doc_id} not found"
    DOC_INVALID_FORMAT = "Invalid document format: {format}"
    DOC_TOO_LARGE = "Document size exceeds limit of {limit} bytes"

    # System
    DATABASE_ERROR = "Database operation failed: {details}"
    CACHE_ERROR = "Cache operation failed: {details}"
    FILE_ERROR = "File operation failed: {details}"