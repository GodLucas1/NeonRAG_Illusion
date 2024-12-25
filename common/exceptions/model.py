from typing import Optional, Dict, Any
from http import HTTPStatus
from .base import MultiModelRAGException

class ModelError(MultiModelRAGException):
    """Base exception class for model-related errors"""
    def __init__(
        self,
        message: str,
        model_name: str,
        status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
        error_code: str = "MODEL_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        details["model_name"] = model_name
        super().__init__(message, status_code, error_code, details)

class ModelNotFoundError(ModelError):
    """Exception for when a requested model is not found"""
    def __init__(self, model_name: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Model '{model_name}' not found",
            model_name=model_name,
            status_code=HTTPStatus.NOT_FOUND,
            error_code="MODEL_NOT_FOUND",
            details=details
        )

class ModelLoadError(ModelError):
    """Exception for errors during model loading"""
    def __init__(self, model_name: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Failed to load model '{model_name}'",
            model_name=model_name,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            error_code="MODEL_LOAD_ERROR",
            details=details
        )

class ModelInferenceError(ModelError):
    """Exception for errors during model inference"""
    def __init__(self, model_name: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Error during inference with model '{model_name}'",
            model_name=model_name,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            error_code="MODEL_INFERENCE_ERROR",
            details=details
        )

class ModelTokenLimitError(ModelError):
    """Exception for token limit exceeded errors"""
    def __init__(self, model_name: str, token_count: int, 
                 token_limit: int, details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details.update({
            "token_count": token_count,
            "token_limit": token_limit
        })
        super().__init__(
            message=f"Token limit exceeded for model '{model_name}'",
            model_name=model_name,
            status_code=HTTPStatus.BAD_REQUEST,
            error_code="TOKEN_LIMIT_EXCEEDED",
            details=details
        )

class ModelAPIError(ModelError):
    """Exception for model API related errors"""
    def __init__(self, model_name: str, api_error: str,
                 details: Optional[Dict[str, Any]] = None):
        details = details or {}
        details["api_error"] = api_error
        super().__init__(
            message=f"API error for model '{model_name}': {api_error}",
            model_name=model_name,
            status_code=HTTPStatus.BAD_GATEWAY,
            error_code="MODEL_API_ERROR",
            details=details
        )
