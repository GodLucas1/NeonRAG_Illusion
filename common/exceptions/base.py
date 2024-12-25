from typing import Optional, Dict, Any
from http import HTTPStatus

class MultiModelRAGException(Exception):
    """Base exception class for MultiModelRAG"""
    def __init__(
        self,
        message: str,
        status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary format"""
        return {
            "error": {
                "code": self.error_code,
                "message": self.message,
                "details": self.details,
                "status_code": self.status_code
            }
        }

class ValidationError(MultiModelRAGException):
    """Exception for validation errors"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=HTTPStatus.BAD_REQUEST,
            error_code="VALIDATION_ERROR",
            details=details
        )

class AuthenticationError(MultiModelRAGException):
    """Exception for authentication errors"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=HTTPStatus.UNAUTHORIZED,
            error_code="AUTHENTICATION_ERROR",
            details=details
        )

class AuthorizationError(MultiModelRAGException):
    """Exception for authorization errors"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=HTTPStatus.FORBIDDEN,
            error_code="AUTHORIZATION_ERROR",
            details=details
        )

class ResourceNotFoundError(MultiModelRAGException):
    """Exception for resource not found errors"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=HTTPStatus.NOT_FOUND,
            error_code="RESOURCE_NOT_FOUND",
            details=details
        )

class RateLimitError(MultiModelRAGException):
    """Exception for rate limit errors"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
            details=details
        )
