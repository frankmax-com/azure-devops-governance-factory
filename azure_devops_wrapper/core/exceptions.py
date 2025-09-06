"""
Custom exceptions for Azure DevOps Wrapper
"""

from typing import Optional, Dict, Any


class AzureDevOpsError(Exception):
    """Base exception for all Azure DevOps Wrapper errors."""
    
    def __init__(
        self, 
        message: str, 
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        self.request_id = request_id
    
    def __str__(self) -> str:
        error_parts = [self.message]
        if self.status_code:
            error_parts.append(f"Status: {self.status_code}")
        if self.request_id:
            error_parts.append(f"Request ID: {self.request_id}")
        return " | ".join(error_parts)


class AuthenticationError(AzureDevOpsError):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(message, status_code=401, **kwargs)


class AuthorizationError(AzureDevOpsError):
    """Raised when authorization fails (user doesn't have permission)."""
    
    def __init__(self, message: str = "Access denied", **kwargs):
        super().__init__(message, status_code=403, **kwargs)


class ResourceNotFoundError(AzureDevOpsError):
    """Raised when a requested resource is not found."""
    
    def __init__(self, message: str = "Resource not found", **kwargs):
        super().__init__(message, status_code=404, **kwargs)


class ValidationError(AzureDevOpsError):
    """Raised when request validation fails."""
    
    def __init__(self, message: str = "Validation failed", **kwargs):
        super().__init__(message, status_code=400, **kwargs)


class RateLimitError(AzureDevOpsError):
    """Raised when rate limit is exceeded."""
    
    def __init__(
        self, 
        message: str = "Rate limit exceeded", 
        retry_after: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, status_code=429, **kwargs)
        self.retry_after = retry_after


class ServerError(AzureDevOpsError):
    """Raised when server returns 5xx errors."""
    
    def __init__(self, message: str = "Server error", **kwargs):
        super().__init__(message, **kwargs)


class TimeoutError(AzureDevOpsError):
    """Raised when request times out."""
    
    def __init__(self, message: str = "Request timeout", **kwargs):
        super().__init__(message, **kwargs)


class ConfigurationError(AzureDevOpsError):
    """Raised when configuration is invalid."""
    
    def __init__(self, message: str = "Configuration error", **kwargs):
        super().__init__(message, **kwargs)


class PaginationError(AzureDevOpsError):
    """Raised when pagination fails."""
    
    def __init__(self, message: str = "Pagination error", **kwargs):
        super().__init__(message, **kwargs)


# Legacy alias for backward compatibility
PermissionError = AuthorizationError


def create_exception_from_response(
    status_code: int,
    message: str,
    response_data: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None
) -> AzureDevOpsError:
    """Create appropriate exception based on HTTP status code."""
    
    if status_code == 401:
        return AuthenticationError(message, response_data=response_data, request_id=request_id)
    elif status_code == 403:
        return AuthorizationError(message, response_data=response_data, request_id=request_id)
    elif status_code == 404:
        return ResourceNotFoundError(message, response_data=response_data, request_id=request_id)
    elif status_code == 400:
        return ValidationError(message, response_data=response_data, request_id=request_id)
    elif status_code == 429:
        return RateLimitError(message, response_data=response_data, request_id=request_id)
    elif 500 <= status_code < 600:
        return ServerError(message, status_code=status_code, response_data=response_data, request_id=request_id)
    else:
        return AzureDevOpsError(message, status_code=status_code, response_data=response_data, request_id=request_id)
