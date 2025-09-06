"""
Custom middleware for Azure DevOps Governance Factory
"""

from fastapi import Request, Response
from fastapi.responses import JSONResponse
import time
import structlog
from typing import Callable
import json
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.config import get_settings
from src.core.cache import cache_manager

settings = get_settings()
logger = structlog.get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client identifier
        client_ip = request.client.host
        user_id = getattr(request.state, 'user_id', None)
        client_key = f"rate_limit:{user_id or client_ip}"
        
        # Check rate limit
        current_requests = await cache_manager.get(client_key) or 0
        
        if current_requests >= settings.RATE_LIMIT_REQUESTS_PER_MINUTE:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"}
            )
        
        # Increment counter
        await cache_manager.set(client_key, current_requests + 1, 60)
        
        response = await call_next(request)
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Security headers middleware"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response


class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """Audit logging middleware for API requests"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Extract request information
        request_info = {
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent"),
        }
        
        # Execute request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log request
        logger.info(
            "api_request",
            **request_info,
            status_code=response.status_code,
            duration=duration,
            user_id=getattr(request.state, 'user_id', None)
        )
        
        return response


class GovernanceMiddleware(BaseHTTPMiddleware):
    """Governance validation middleware"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip governance for health checks and docs
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        # TODO: Add governance policy validation here
        # This would integrate with the governance engine to validate
        # requests against applicable policies
        
        response = await call_next(request)
        return response
