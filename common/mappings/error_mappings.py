from http import HTTPStatus
from typing import Dict, Type
from ..constants.error_constants import ErrorCategory, ErrorSeverity, ErrorCodes
from ..exceptions.base import MultiModelRAGException
from ..exceptions.model import ModelError, ModelNotFoundError, ModelLoadError
from ..exceptions.rag import RAGError, DocumentNotFoundError
from ..exceptions.conversation import ConversationError

class ErrorMappings:
    """Mappings related to errors in the Multi-Model RAG system"""
    
    # Map error codes to their categories
    ERROR_CATEGORY_MAP = {
        # Authentication related errors
        ErrorCodes.AUTH_INVALID_TOKEN: ErrorCategory.AUTHENTICATION,
        ErrorCodes.AUTH_EXPIRED_TOKEN: ErrorCategory.AUTHENTICATION,
        ErrorCodes.AUTH_MISSING_TOKEN: ErrorCategory.AUTHENTICATION,
        
        # Model related errors
        ErrorCodes.MODEL_NOT_FOUND: ErrorCategory.MODEL,
        ErrorCodes.MODEL_LOAD_FAILED: ErrorCategory.MODEL,
        ErrorCodes.MODEL_INFERENCE_ERROR: ErrorCategory.MODEL,
        ErrorCodes.MODEL_TIMEOUT: ErrorCategory.MODEL,
        
        # RAG related errors
        ErrorCodes.DOCUMENT_NOT_FOUND: ErrorCategory.RAG,
        ErrorCodes.DOCUMENT_PROCESSING_ERROR: ErrorCategory.RAG,
        ErrorCodes.EMBEDDING_GENERATION_ERROR: ErrorCategory.RAG,
        ErrorCodes.VECTOR_STORE_ERROR: ErrorCategory.RAG,
        
        # Conversation related errors
        ErrorCodes.CONVERSATION_NOT_FOUND: ErrorCategory.CONVERSATION,
        ErrorCodes.CONVERSATION_HISTORY_ERROR: ErrorCategory.CONVERSATION,
        ErrorCodes.MESSAGE_PROCESSING_ERROR: ErrorCategory.CONVERSATION,
        
        # System errors
        ErrorCodes.INTERNAL_SERVER_ERROR: ErrorCategory.SYSTEM,
        ErrorCodes.DATABASE_ERROR: ErrorCategory.SYSTEM,
        ErrorCodes.RATE_LIMIT_EXCEEDED: ErrorCategory.SYSTEM
    }
    
    # Map error codes to their severity levels
    ERROR_SEVERITY_MAP = {
        # Critical errors that need immediate attention
        ErrorCodes.INTERNAL_SERVER_ERROR: ErrorSeverity.CRITICAL,
        ErrorCodes.DATABASE_ERROR: ErrorSeverity.CRITICAL,
        ErrorCodes.MODEL_LOAD_FAILED: ErrorSeverity.CRITICAL,
        
        # High severity errors that affect core functionality
        ErrorCodes.MODEL_INFERENCE_ERROR: ErrorSeverity.HIGH,
        ErrorCodes.VECTOR_STORE_ERROR: ErrorSeverity.HIGH,
        ErrorCodes.DOCUMENT_PROCESSING_ERROR: ErrorSeverity.HIGH,
        
        # Medium severity errors that degrade service quality
        ErrorCodes.MODEL_TIMEOUT: ErrorSeverity.MEDIUM,
        ErrorCodes.RATE_LIMIT_EXCEEDED: ErrorSeverity.MEDIUM,
        ErrorCodes.EMBEDDING_GENERATION_ERROR: ErrorSeverity.MEDIUM,
        
        # Low severity errors that don't significantly impact service
        ErrorCodes.DOCUMENT_NOT_FOUND: ErrorSeverity.LOW,
        ErrorCodes.CONVERSATION_NOT_FOUND: ErrorSeverity.LOW,
        ErrorCodes.AUTH_EXPIRED_TOKEN: ErrorSeverity.LOW
    }
    
    # Map exception types to HTTP status codes
    EXCEPTION_STATUS_MAP: Dict[Type[MultiModelRAGException], HTTPStatus] = {
        # Authentication exceptions
        MultiModelRAGException: HTTPStatus.INTERNAL_SERVER_ERROR,  # Default fallback
        
        # Model exceptions
        ModelError: HTTPStatus.INTERNAL_SERVER_ERROR,
        ModelNotFoundError: HTTPStatus.NOT_FOUND,
        ModelLoadError: HTTPStatus.SERVICE_UNAVAILABLE,
        
        # RAG exceptions
        RAGError: HTTPStatus.INTERNAL_SERVER_ERROR,
        DocumentNotFoundError: HTTPStatus.NOT_FOUND,
        
        # Conversation exceptions
        ConversationError: HTTPStatus.BAD_REQUEST
    }
    
    @classmethod
    def get_error_category(cls, error_code: ErrorCodes) -> ErrorCategory:
        """Get the category for a given error code"""
        return cls.ERROR_CATEGORY_MAP.get(error_code, ErrorCategory.SYSTEM)
    
    @classmethod
    def get_error_severity(cls, error_code: ErrorCodes) -> ErrorSeverity:
        """Get the severity level for a given error code"""
        return cls.ERROR_SEVERITY_MAP.get(error_code, ErrorSeverity.MEDIUM)
    
    @classmethod
    def get_http_status(cls, exception: Type[MultiModelRAGException]) -> HTTPStatus:
        """Get the HTTP status code for a given exception type"""
        return cls.EXCEPTION_STATUS_MAP.get(exception, HTTPStatus.INTERNAL_SERVER_ERROR)
