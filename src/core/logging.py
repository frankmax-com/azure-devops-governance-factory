"""
Structured logging configuration for Azure DevOps Governance Factory
"""

import structlog
import logging
import sys
from typing import Any, Dict
from src.core.config import get_settings

settings = get_settings()


def setup_logging():
    """Configure structured logging"""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if settings.LOG_FORMAT == "json" 
            else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )


class AuditLogger:
    """Audit logger for governance and compliance events"""
    
    def __init__(self):
        self.logger = structlog.get_logger("audit")
    
    async def log_governance_event(
        self,
        event_type: str,
        user_id: str,
        resource_type: str,
        resource_id: str,
        action: str,
        result: str,
        metadata: Dict[str, Any] = None
    ):
        """Log governance event for audit trail"""
        self.logger.info(
            "governance_event",
            event_type=event_type,
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            result=result,
            metadata=metadata or {}
        )
    
    async def log_compliance_check(
        self,
        framework: str,
        check_type: str,
        resource_id: str,
        compliance_status: bool,
        violations: list = None,
        metadata: Dict[str, Any] = None
    ):
        """Log compliance check result"""
        self.logger.info(
            "compliance_check",
            framework=framework,
            check_type=check_type,
            resource_id=resource_id,
            compliance_status=compliance_status,
            violations=violations or [],
            metadata=metadata or {}
        )
    
    async def log_policy_enforcement(
        self,
        policy_id: str,
        resource_type: str,
        resource_id: str,
        enforcement_action: str,
        result: str,
        user_id: str = None,
        metadata: Dict[str, Any] = None
    ):
        """Log policy enforcement action"""
        self.logger.info(
            "policy_enforcement",
            policy_id=policy_id,
            resource_type=resource_type,
            resource_id=resource_id,
            enforcement_action=enforcement_action,
            result=result,
            user_id=user_id,
            metadata=metadata or {}
        )
    
    async def log_security_event(
        self,
        event_type: str,
        severity: str,
        source: str,
        description: str,
        user_id: str = None,
        ip_address: str = None,
        metadata: Dict[str, Any] = None
    ):
        """Log security event"""
        self.logger.warning(
            "security_event",
            event_type=event_type,
            severity=severity,
            source=source,
            description=description,
            user_id=user_id,
            ip_address=ip_address,
            metadata=metadata or {}
        )
