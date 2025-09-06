"""
Core module for Azure DevOps Wrapper
"""

from .auth import AuthManager, AuthConfig, AuthType
from .client import HTTPClient
from .exceptions import *
from .pagination import PaginationHelper, create_paginator
from .rate_limiter import RateLimiter, RateLimitConfig, GlobalRateLimiter

__all__ = [
    "AuthManager",
    "AuthConfig", 
    "AuthType",
    "HTTPClient",
    "PaginationHelper",
    "create_paginator",
    "RateLimiter",
    "RateLimitConfig",
    "GlobalRateLimiter",
    "AzureDevOpsError",
    "AuthenticationError",
    "AuthorizationError", 
    "ResourceNotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    "TimeoutError",
    "ConfigurationError",
    "PaginationError"
]
