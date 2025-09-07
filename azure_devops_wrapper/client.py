"""
Azure DevOps Wrapper - Main Client Class

This is the primary entry point for the Azure DevOps Python wrapper that provides
simplified access to the entire Azure DevOps REST API ecosystem.
"""

from typing import Optional, Dict, Any
from .core.http_client import HTTPClient
from .core.auth_manager import AuthManager
from .core.rate_limiter import RateLimiter
from .core.pagination import PaginationHelper

# Service imports
from .services import (
    CoreService, GitService, WorkItemsService
    # Temporarily disabled services with missing models:
    # BuildService, PipelinesService, ReleaseService, TestService, PackagingService,
    # SecurityService, GraphService, ExtensionsService,
    # NotificationService, ServiceHooksService  # AuditService - TODO: Create if needed
)

# Facade imports (temporarily disabled)
# from .facades import (
#     ProjectFacade, PipelineFacade, SecurityFacade,
#     IntegrationFacade, GovernanceFacade
# )

# Model imports
from .models.common import (
    AuthConfig, RateLimitConfig, ClientConfig
)


class AzureDevOpsClient:
    """
    Main Azure DevOps API client providing comprehensive access to all Azure DevOps services.
    
    This client provides both low-level service access and high-level business facade abstractions.
    It supports multiple authentication methods, automatic rate limiting, retry logic, and
    comprehensive error handling.
    
    Example:
        ```python
        # Initialize client with Personal Access Token
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
    
    def __init__(
        self,
        organization: str,
        auth_config: AuthConfig,
        base_url: Optional[str] = None,
        rate_limit_config: Optional[RateLimitConfig] = None,
        client_config: Optional[ClientConfig] = None
    ):
        """
        Initialize the Azure DevOps client.
        
        Args:
            organization: Azure DevOps organization name
            auth_config: Authentication configuration
            base_url: Custom base URL (defaults to https://dev.azure.com/{organization})
            rate_limit_config: Rate limiting configuration
            client_config: HTTP client configuration
        """
        self.organization = organization
        self.base_url = base_url or f"https://dev.azure.com/{organization}"
        
        # Initialize core components
        self._auth_manager = AuthManager(auth_config)
        self._rate_limiter = RateLimiter(rate_limit_config or RateLimitConfig())
        
        # Get auth header from auth manager
        auth_header = {}  # Will be set by auth manager when needed
        
        self._http_client = HTTPClient(
            base_url=self.base_url,
            auth_header=auth_header,
            timeout=getattr(client_config, 'timeout', 30) if client_config else 30,
            rate_limiter=self._rate_limiter
        )
        self._pagination_helper = PaginationHelper(self._http_client)
        
        # Initialize services
        self._initialize_services()
        
        # Initialize facades
        self._initialize_facades()
    
    def _initialize_services(self):
        """Initialize all Azure DevOps service clients."""
        # Core infrastructure services
        self._core_service = CoreService(
            self._http_client
        )
        
        # self._graph_service = GraphService(
        #     self._http_client,
        #     self._pagination_helper
        # )
        
        # self._security_service = SecurityService(
        #     self._http_client,
        #     self._pagination_helper
        # )
        
        # self._audit_service = AuditService(
        #     self._http_client,
        #     self._pagination_helper
        # )
        
        # Development services
        self._git_service = GitService(
            self._http_client
        )
        
        self._work_items_service = WorkItemsService(
            self._http_client
        )
        
        # CI/CD services (temporarily disabled)
        # self._build_service = BuildService(
        #     self._http_client,
        #     self._pagination_helper
        # )
        
        # self._pipelines_service = PipelinesService(
        #     self._http_client,
        #     self._pagination_helper
        # )
        
        # self._release_service = ReleaseService(
        #     self._http_client,
        #     self._pagination_helper
        # )
        
        # self._test_service = TestService(
        #     self._http_client,
        #     self._pagination_helper
        # )
        
        # Package and extension services (temporarily disabled)
        # self._packaging_service = PackagingService(
        #     self._http_client,
        #     self._pagination_helper
        # )
        
        # self._extensions_service = ExtensionsService(
        #     self._http_client,
        #     self._pagination_helper
        # )
        
        # Integration services (temporarily disabled)
        # self._notification_service = NotificationService(
        #     self._http_client,
        #     self._pagination_helper
        # )
        
        # self._service_hooks_service = ServiceHooksService(
        #     self._http_client,
        #     self._pagination_helper
        # )
    
    def _initialize_facades(self):
        """Initialize high-level business facade abstractions."""
        # Temporarily disabled facades:
        # self._project_facade = ProjectFacade(
        #     core_service=self._core_service,
        #     git_service=self._git_service,
        #     work_items_service=self._work_items_service,
        #     build_service=self._build_service,
        #     pipelines_service=self._pipelines_service,
        #     security_service=self._security_service,
        #     graph_service=self._graph_service
        # )
        
        # self._pipeline_facade = PipelineFacade(
        #     build_service=self._build_service,
        #     pipelines_service=self._pipelines_service,
        #     release_service=self._release_service,
        #     test_service=self._test_service,
        #     git_service=self._git_service,
        #     packaging_service=self._packaging_service,
        #     notification_service=self._notification_service,
        #     service_hooks_service=self._service_hooks_service
        # )
        
        # self._security_facade = SecurityFacade(
        #     security_service=self._security_service,
        #     graph_service=self._graph_service,
        #     core_service=self._core_service,
        #     git_service=self._git_service,
        #     notification_service=self._notification_service,
        #     extensions_service=self._extensions_service
        # )
        
        # self._integration_facade = IntegrationFacade(
        #     service_hooks_service=self._service_hooks_service,
        #     notification_service=self._notification_service,
        #     extensions_service=self._extensions_service,
        #     core_service=self._core_service,
        #     git_service=self._git_service,
        #     build_service=self._build_service,
        #     pipelines_service=self._pipelines_service
        # )
        
        # self._governance_facade = GovernanceFacade(
        #     core_service=self._core_service,
        #     graph_service=self._graph_service,
        #     security_service=self._security_service,
        #     git_service=self._git_service,
        #     work_items_service=self._work_items_service,
        #     build_service=self._build_service,
        #     pipelines_service=self._pipelines_service,
        #     release_service=self._release_service,
        #     notification_service=self._notification_service,
        #     extensions_service=self._extensions_service,
        #     audit_service=self._audit_service
        # )
        pass  # Temporarily no facades
    
    @property
    def services(self) -> "ServiceContainer":
        """Access to all low-level Azure DevOps service clients."""
        return ServiceContainer(
            core=self._core_service,
            git=self._git_service,
            work_items=self._work_items_service,
            # Temporarily disabled services:
            # build=self._build_service,
            # pipelines=self._pipelines_service,
            # release=self._release_service,
            # test=self._test_service,
            # packaging=self._packaging_service,
            # security=self._security_service,
            # graph=self._graph_service,
            # extensions=self._extensions_service,
            # notification=self._notification_service,
            # service_hooks=self._service_hooks_service
            # audit=self._audit_service  # TODO: Create AuditService if needed
        )
    
    @property
    def facades(self) -> "FacadeContainer":
        """Access to all high-level business facade abstractions."""
        return FacadeContainer(
            # Temporarily disabled facades:
            # project=self._project_facade,
            # pipeline=self._pipeline_facade,
            # security=self._security_facade,
            # integration=self._integration_facade,
            # governance=self._governance_facade
        )
    
    async def get_client_info(self) -> Dict[str, Any]:
        """
        Get information about the client configuration and status.
        
        Returns:
            Dictionary containing client information
        """
        try:
            # Test authentication
            auth_test = await self._auth_manager.get_auth_headers()
            auth_status = "valid" if auth_test else "invalid"
        except Exception:
            auth_status = "error"
        
        return {
            "organization": self.organization,
            "base_url": self.base_url,
            "auth_status": auth_status,
            "auth_type": self._auth_manager.auth_config.auth_type,
            "rate_limit_config": {
                "requests_per_second": self._rate_limiter.config.requests_per_second,
                "burst_capacity": self._rate_limiter.config.burst_capacity
            },
            "client_version": "1.0.0",
            "api_version": "7.1-preview"
        }
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection to Azure DevOps and verify authentication.
        
        Returns:
            Dictionary containing connection test results
        """
        results = {
            "connection_status": "unknown",
            "auth_status": "unknown",
            "organization_access": False,
            "rate_limit_status": "unknown",
            "response_time": 0,
            "errors": []
        }
        
        try:
            import time
            start_time = time.time()
            
            # Test basic connection and authentication
            projects = await self._core_service.list_projects(top=1)
            
            end_time = time.time()
            results["response_time"] = round((end_time - start_time) * 1000, 2)  # milliseconds
            
            results["connection_status"] = "success"
            results["auth_status"] = "valid"
            results["organization_access"] = True
            results["rate_limit_status"] = f"Available tokens: {self._rate_limiter.tokens}"
            
        except Exception as e:
            results["connection_status"] = "failed"
            results["errors"].append(str(e))
            
            if "unauthorized" in str(e).lower() or "403" in str(e):
                results["auth_status"] = "invalid"
            elif "rate limit" in str(e).lower() or "429" in str(e):
                results["rate_limit_status"] = "exceeded"
            
        return results
    
    async def close(self):
        """Close the HTTP client and clean up resources."""
        await self._http_client.close()


class ServiceContainer:
    """Container providing access to all Azure DevOps service clients."""
    
    def __init__(
        self,
        core: CoreService,
        git: GitService,
        work_items: WorkItemsService,
        # Temporarily disabled services:
        # build: BuildService,
        # pipelines: PipelinesService,
        # release: ReleaseService,
        # test: TestService,
        # packaging: PackagingService,
        # security: SecurityService,
        # graph: GraphService,
        # extensions: ExtensionsService,
        # notification: NotificationService,
        # service_hooks: ServiceHooksService
        # audit: AuditService  # TODO: Create if needed
    ):
        self.core = core
        self.git = git
        self.work_items = work_items
        # self.build = build
        # self.pipelines = pipelines
        # self.release = release
        # self.test = test
        # self.packaging = packaging
        # self.security = security
        # self.graph = graph
        # self.extensions = extensions
        # self.notification = notification
        # self.service_hooks = service_hooks
        # self.audit = audit  # TODO: Create AuditService if needed


class FacadeContainer:
    """Container providing access to all business facade abstractions."""
    
    def __init__(
        self,
        # Temporarily disabled facades:
        # project: ProjectFacade,
        # pipeline: PipelineFacade,
        # security: SecurityFacade,
        # integration: IntegrationFacade,
        # governance: GovernanceFacade
    ):
        # self.project = project
        # self.pipeline = pipeline
        # self.security = security
        # self.integration = integration
        # self.governance = governance
        pass  # Temporarily no facades
