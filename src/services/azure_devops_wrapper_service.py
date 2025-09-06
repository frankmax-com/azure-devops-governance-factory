"""
Azure DevOps Wrapper Integration for FastAPI Service

This module integrates the comprehensive Azure DevOps wrapper we built
with the existing FastAPI service infrastructure.
"""

from typing import Dict, List, Any, Optional
from fastapi import HTTPException
import structlog

from azure_devops_wrapper import AzureDevOpsClient, AuthConfig, RateLimitConfig
from src.core.config import get_settings

settings = get_settings()
logger = structlog.get_logger(__name__)


class AzureDevOpsWrapperService:
    """Integration service for the Azure DevOps wrapper"""
    
    def __init__(self):
        self.client: Optional[AzureDevOpsClient] = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Azure DevOps wrapper client"""
        try:
            # Configure authentication
            auth_config = AuthConfig(
                auth_type="pat",  # or "service_principal" for production
                personal_access_token=settings.AZURE_CLIENT_SECRET,
                # For service principal auth:
                # auth_type="service_principal",
                # client_id=settings.AZURE_CLIENT_ID,
                # client_secret=settings.AZURE_CLIENT_SECRET,
                # tenant_id=settings.AZURE_TENANT_ID
            )
            
            # Configure rate limiting for production use
            rate_limit_config = RateLimitConfig(
                requests_per_second=5.0,  # Conservative for Azure DevOps
                burst_capacity=20,
                max_retries=3,
                backoff_factor=2.0
            )
            
            # Initialize client
            self.client = AzureDevOpsClient(
                organization=settings.AZURE_DEVOPS_ORGANIZATION,
                auth_config=auth_config,
                rate_limit_config=rate_limit_config
            )
            
            logger.info("Azure DevOps wrapper client initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize Azure DevOps wrapper client", error=str(e))
            raise
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test connection to Azure DevOps"""
        if not self.client:
            raise HTTPException(status_code=500, detail="Azure DevOps client not initialized")
        
        try:
            return await self.client.test_connection()
        except Exception as e:
            logger.error("Azure DevOps connection test failed", error=str(e))
            raise HTTPException(status_code=500, detail=f"Connection test failed: {str(e)}")
    
    async def get_client_info(self) -> Dict[str, Any]:
        """Get client configuration information"""
        if not self.client:
            raise HTTPException(status_code=500, detail="Azure DevOps client not initialized")
        
        try:
            return await self.client.get_client_info()
        except Exception as e:
            logger.error("Failed to get client info", error=str(e))
            raise HTTPException(status_code=500, detail=f"Failed to get client info: {str(e)}")
    
    # High-Level Business Facades
    async def create_complete_project(
        self,
        project_name: str,
        project_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create complete project using the project facade"""
        if not self.client:
            raise HTTPException(status_code=500, detail="Azure DevOps client not initialized")
        
        try:
            return await self.client.facades.project.create_complete_project(
                project_name=project_name,
                project_config=project_config
            )
        except Exception as e:
            logger.error("Failed to create complete project", project_name=project_name, error=str(e))
            raise HTTPException(status_code=500, detail=f"Project creation failed: {str(e)}")
    
    async def setup_cicd_pipeline(
        self,
        project_id: str,
        pipeline_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Set up complete CI/CD pipeline using the pipeline facade"""
        if not self.client:
            raise HTTPException(status_code=500, detail="Azure DevOps client not initialized")
        
        try:
            return await self.client.facades.pipeline.create_complete_cicd_pipeline(
                project_id=project_id,
                pipeline_config=pipeline_config
            )
        except Exception as e:
            logger.error("Failed to setup CI/CD pipeline", project_id=project_id, error=str(e))
            raise HTTPException(status_code=500, detail=f"Pipeline setup failed: {str(e)}")
    
    async def implement_security_governance(
        self,
        security_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Implement security governance using the security facade"""
        if not self.client:
            raise HTTPException(status_code=500, detail="Azure DevOps client not initialized")
        
        try:
            return await self.client.facades.security.implement_zero_trust_security(
                security_config=security_config
            )
        except Exception as e:
            logger.error("Failed to implement security governance", error=str(e))
            raise HTTPException(status_code=500, detail=f"Security governance implementation failed: {str(e)}")
    
    async def setup_devops_integrations(
        self,
        project_id: str,
        integration_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Set up DevOps integrations using the integration facade"""
        if not self.client:
            raise HTTPException(status_code=500, detail="Azure DevOps client not initialized")
        
        try:
            return await self.client.facades.integration.setup_complete_devops_integration(
                project_id=project_id,
                integration_config=integration_config
            )
        except Exception as e:
            logger.error("Failed to setup DevOps integrations", project_id=project_id, error=str(e))
            raise HTTPException(status_code=500, detail=f"Integration setup failed: {str(e)}")
    
    async def implement_enterprise_governance(
        self,
        governance_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Implement enterprise governance using the governance facade"""
        if not self.client:
            raise HTTPException(status_code=500, detail="Azure DevOps client not initialized")
        
        try:
            return await self.client.facades.governance.implement_enterprise_governance(
                governance_config=governance_config
            )
        except Exception as e:
            logger.error("Failed to implement enterprise governance", error=str(e))
            raise HTTPException(status_code=500, detail=f"Enterprise governance implementation failed: {str(e)}")
    
    # Low-Level Service Access
    async def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects using the core service"""
        if not self.client:
            raise HTTPException(status_code=500, detail="Azure DevOps client not initialized")
        
        try:
            return await self.client.services.core.get_projects()
        except Exception as e:
            logger.error("Failed to get projects", error=str(e))
            raise HTTPException(status_code=500, detail=f"Failed to get projects: {str(e)}")
    
    async def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get specific project using the core service"""
        if not self.client:
            raise HTTPException(status_code=500, detail="Azure DevOps client not initialized")
        
        try:
            return await self.client.services.core.get_project(project_id)
        except Exception as e:
            logger.error("Failed to get project", project_id=project_id, error=str(e))
            raise HTTPException(status_code=500, detail=f"Failed to get project: {str(e)}")
    
    async def get_repositories(self, project_id: str) -> List[Dict[str, Any]]:
        """Get repositories using the git service"""
        if not self.client:
            raise HTTPException(status_code=500, detail="Azure DevOps client not initialized")
        
        try:
            return await self.client.services.git.get_repositories(project_id)
        except Exception as e:
            logger.error("Failed to get repositories", project_id=project_id, error=str(e))
            raise HTTPException(status_code=500, detail=f"Failed to get repositories: {str(e)}")
    
    async def get_builds(self, project_id: str = None, top: int = 50) -> List[Dict[str, Any]]:
        """Get builds using the build service"""
        if not self.client:
            raise HTTPException(status_code=500, detail="Azure DevOps client not initialized")
        
        try:
            return await self.client.services.build.get_builds(project_id=project_id, top=top)
        except Exception as e:
            logger.error("Failed to get builds", project_id=project_id, error=str(e))
            raise HTTPException(status_code=500, detail=f"Failed to get builds: {str(e)}")
    
    async def analyze_integration_health(
        self,
        project_id: Optional[str] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """Analyze integration health using the integration facade"""
        if not self.client:
            raise HTTPException(status_code=500, detail="Azure DevOps client not initialized")
        
        try:
            return await self.client.facades.integration.analyze_integration_health(
                project_id=project_id,
                days=days
            )
        except Exception as e:
            logger.error("Failed to analyze integration health", project_id=project_id, error=str(e))
            raise HTTPException(status_code=500, detail=f"Integration health analysis failed: {str(e)}")
    
    async def conduct_security_audit(self) -> Dict[str, Any]:
        """Conduct security audit using the security facade"""
        if not self.client:
            raise HTTPException(status_code=500, detail="Azure DevOps client not initialized")
        
        try:
            return await self.client.facades.security.conduct_security_audit()
        except Exception as e:
            logger.error("Failed to conduct security audit", error=str(e))
            raise HTTPException(status_code=500, detail=f"Security audit failed: {str(e)}")
    
    async def close(self):
        """Close the Azure DevOps client"""
        if self.client:
            await self.client.close()
            logger.info("Azure DevOps wrapper client closed")


# Global instance
azure_devops_wrapper_service = AzureDevOpsWrapperService()
