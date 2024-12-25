import logging
import os
from typing import Dict, Any
from common.logging.formatters import (
    RequestLogFormatter, ProcessLogFormatter, AuditLogFormatter,
    ModelLogFormatter, SecurityLogFormatter
)
from common.constants.system_constants import PathConstants


class MultiModelRAGLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self._setup_log_directory()
        self._setup_loggers()

    def _setup_log_directory(self):
        """Create log directory if it doesn't exist"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Create subdirectories for different log types
        for log_type in ['requests', 'process', 'audit', 'model', 'security']:
            subdir = os.path.join(self.log_dir, log_type)
            if not os.path.exists(subdir):
                os.makedirs(subdir)

    def _setup_loggers(self):
        """Setup different loggers for each log type"""
        self.loggers = {}

        # Configure each logger type
        logger_configs = {
            'request': {'file': 'requests/requests.log', 'level': logging.INFO},
            'process': {'file': 'process/process.log', 'level': logging.DEBUG},
            'audit': {'file': 'audit/audit.log', 'level': logging.INFO},
            'model': {'file': 'model/model.log', 'level': logging.DEBUG},
            'security': {'file': 'security/security.log', 'level': logging.WARNING}
        }

        for logger_name, config in logger_configs.items():
            logger = logging.getLogger(f'rag.{logger_name}')
            logger.setLevel(config['level'])

            # Create file handler
            handler = logging.FileHandler(
                os.path.join(self.log_dir, config['file']),
                encoding='utf-8'
            )
            handler.setLevel(config['level'])

            # Add handler to logger
            logger.addHandler(handler)
            self.loggers[logger_name] = logger

    def log_request(self, method: str, path: str, duration: float,
                    status_code: int, request_id: str, **kwargs):
        """Log API request information"""
        log_entry = RequestLogFormatter.format(
            method=method,
            path=path,
            duration=duration,
            status_code=status_code,
            request_id=request_id,
            **kwargs
        )
        self.loggers['request'].info(log_entry)

    def log_process(self, process_name: str, status: str, **kwargs):
        """Log process information"""
        log_entry = ProcessLogFormatter.format(
            process_name=process_name,
            status=status,
            **kwargs
        )
        self.loggers['process'].debug(log_entry)

    def log_audit(self, action: str, resource_type: str,
                  resource_id: str, user_id: str, **kwargs):
        """Log audit information"""
        log_entry = AuditLogFormatter.format(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            **kwargs
        )
        self.loggers['audit'].info(log_entry)

    def log_model(self, model_name: str, operation: str, **kwargs):
        """Log model-related information"""
        log_entry = ModelLogFormatter.format(
            model_name=model_name,
            operation=operation,
            **kwargs
        )
        self.loggers['model'].debug(log_entry)

    def log_security(self, event_type: str, severity: str, **kwargs):
        """Log security-related information"""
        log_entry = SecurityLogFormatter.format(
            event_type=event_type,
            severity=severity,
            **kwargs
        )
        self.loggers['security'].warning(log_entry)


if __name__ == '__main__':
    log_dir = PathConstants.LOGS_DIR.__str__()
    m = MultiModelRAGLogger(log_dir)
    m.log_audit("test", "test", "test", "test", changes={"test": "test"})