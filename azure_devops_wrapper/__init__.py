"""
Azure DevOps Wrapper - A comprehensive Python wrapper for Azure DevOps REST API

This package provides a developer-friendly interface to all ~2,125 Azure DevOps REST API operations
across 13 service categories, with built-in authentication, rate limiting, pagination, and error handling.

Main Components:
- AzureDevOpsClient: Main client for accessing Azure DevOps services
- Service Clients: Specialized clients for each Azure DevOps service area
- Business Facades: High-level business operation interfaces  
- Models: Pydantic models for all Azure DevOps entities

Key Features:
- Complete coverage of Azure DevOps REST API (~2,125 operations)
- Multiple authentication methods (PAT, OAuth, Managed Identity, Service Principal)
- Automatic rate limiting and retry logic with exponential backoff
- Comprehensive error handling and type safety
- High-level business facades for complex workflows
- Async-first design for high performance
- Enterprise governance and compliance features

Example Usage:
    ```python
    from azure_devops_wrapper import AzureDevOpsClient, AuthConfig
    
    # Initialize client
    client = AzureDevOpsClient(
        organization="myorg",
        auth_config=AuthConfig(
            auth_type="pat",
            personal_access_token="your-pat-token"
        )
    )
    
    # Use high-level business facades
    project_result = await client.facades.project.create_complete_project(
        project_name="MyProject",
        project_config={
            "description": "New project with full setup",
            "source_control": "git",
            "work_item_process": "agile"
        }
    )
    
    # Or use low-level services directly
    projects = await client.services.core.get_projects()
    ```
"""

from .client import AzureDevOpsClient, ServiceContainer, FacadeContainer
from .models.common import AuthConfig, RateLimitConfig, ClientConfig
from .core.exceptions import (
    AzureDevOpsError,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
    NetworkError
)

__version__ = "1.0.0"
__author__ = "Azure DevOps Wrapper Team"
__license__ = "MIT"
__description__ = "A comprehensive Python wrapper for the Azure DevOps REST API"

__all__ = [
    # Main client
    "AzureDevOpsClient",
    "ServiceContainer", 
    "FacadeContainer",
    
    # Configuration models
    "AuthConfig",
    "RateLimitConfig", 
    "ClientConfig",
    
    # Exceptions
    "AzureDevOpsError",
    "AuthenticationError",
    "AuthorizationError",
    "ResourceNotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    "NetworkError"
]
