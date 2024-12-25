import json
from datetime import datetime
from typing import Any, Dict


class BaseLogFormatter:
    @classmethod
    def format(cls, log_type: str, message: str, **kwargs) -> str:
        """Base format method for logs"""
        base_log = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": log_type,
            "message": message,
            **kwargs
        }
        return json.dumps(base_log)


class RequestLogFormatter(BaseLogFormatter):
    @classmethod
    def format(cls, method: str, path: str, duration: float = None, status_code: int = None,
               request_id: str = None, user_id: str = None, **kwargs) -> str:
        """Format request logs"""
        return super().format(
            log_type="REQUEST",
            message=f"{method} {path}",
            method=method,
            path=path,
            duration=duration,
            status_code=status_code,
            request_id=request_id,
            user_id=user_id,
            **kwargs
        )


class ProcessLogFormatter(BaseLogFormatter):
    @classmethod
    def format(cls, process_name: str, status: str, duration: float = None,
               details: Dict[str, Any] = None, **kwargs) -> str:
        """Format process logs"""
        return super().format(
            log_type="PROCESS",
            message=f"Process {process_name}: {status}",
            process_name=process_name,
            status=status,
            duration=duration,
            details=details,
            **kwargs
        )


class AuditLogFormatter(BaseLogFormatter):
    @classmethod
    def format(cls, action: str, resource_type: str, resource_id: str = None,
               user_id: str = None, changes: Dict[str, Any] = None, **kwargs) -> str:
        """Format audit logs"""
        return super().format(
            log_type="AUDIT",
            message=f"{action} on {resource_type} {resource_id}",
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            changes=changes,
            **kwargs
        )


class ModelLogFormatter(BaseLogFormatter):
    @classmethod
    def format(cls, model_name: str, operation: str, tokens_used: int = None,
               duration: float = None, error: str = None, **kwargs) -> str:
        """Format model-specific logs"""
        return super().format(
            log_type="MODEL",
            message=f"Model {model_name}: {operation}",
            model_name=model_name,
            operation=operation,
            tokens_used=tokens_used,
            duration=duration,
            error=error,
            **kwargs
        )


class SecurityLogFormatter(BaseLogFormatter):
    @classmethod
    def format(cls, event_type: str, severity: str, source_ip: str = None,
               user_id: str = None, details: Dict[str, Any] = None, **kwargs) -> str:
        """Format security-related logs"""
        return super().format(
            log_type="SECURITY",
            message=f"Security {event_type}: {severity}",
            event_type=event_type,
            severity=severity,
            source_ip=source_ip,
            user_id=user_id,
            details=details,
            **kwargs
        )
