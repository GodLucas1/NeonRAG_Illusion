from typing import Optional, Dict, Any
from http import HTTPStatus
from .base import MultiModelRAGException


class ConversationError(MultiModelRAGException):
    """Base exception class for conversation-related errors"""

    def __init__(
            self,
            message: str,
            status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
            error_code: str = "CONVERSATION_ERROR",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, status_code, error_code, details)


class SessionNotFoundError(ConversationError):
    """Exception for when a requested session is not found"""

    def __init__(self, session_id: str, details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details["session_id"] = session_id
        super().__init__(
            message=f"Session not found: {session_id}",
            status_code=HTTPStatus.NOT_FOUND,
            error_code="SESSION_NOT_FOUND",
            details=details
        )


class SessionExpiredError(ConversationError):
    """Exception for expired sessions"""

    def __init__(self, session_id: str, expiry_time: str,
                 details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details.update({
            "session_id": session_id,
            "expiry_time": expiry_time
        })
        super().__init__(
            message=f"Session expired: {session_id}",
            status_code=HTTPStatus.UNAUTHORIZED,
            error_code="SESSION_EXPIRED",
            details=details
        )


class HistoryLoadError(ConversationError):
    """Exception for conversation history loading errors"""

    def __init__(self, filename: str, error_details: str,
                 details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details.update({
            "filename": filename,
            "error_details": error_details
        })
        super().__init__(
            message=f"Failed to load conversation history: {filename}",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            error_code="HISTORY_LOAD_ERROR",
            details=details
        )


class HistorySaveError(ConversationError):
    """Exception for conversation history saving errors"""

    def __init__(self, filename: str, error_details: str,
                 details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details.update({
            "filename": filename,
            "error_details": error_details
        })
        super().__init__(
            message=f"Failed to save conversation history: {filename}",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            error_code="HISTORY_SAVE_ERROR",
            details=details
        )


class MessageValidationError(ConversationError):
    """Exception for message validation errors"""

    def __init__(self, validation_errors: Dict[str, str],
                 details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details["validation_errors"] = validation_errors
        super().__init__(
            message="Message validation failed",
            status_code=HTTPStatus.BAD_REQUEST,
            error_code="MESSAGE_VALIDATION_ERROR",
            details=details
        )
