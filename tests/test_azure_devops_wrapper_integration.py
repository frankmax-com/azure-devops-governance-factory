"""
Comprehensive test suite for Azure DevOps Wrapper integration
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.main import app
from src.services.azure_devops_wrapper_service import AzureDevOpsWrapperService
from azure_devops_wrapper import AzureDevOpsClient, AuthConfig


class TestAzureDevOpsWrapperIntegration:
    """Test the Azure DevOps wrapper integration with FastAPI"""
    
    @pytest.fixture
    def client(self):
        """FastAPI test client"""
        return TestClient(app)
    
    @pytest.fixture
    async def async_client(self):
        """Async HTTP client for testing"""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac
    
    @pytest.fixture
    def mock_azure_devops_client(self):
        """Mock Azure DevOps client"""
        mock_client = Mock(spec=AzureDevOpsClient)
        
        # Mock services
        mock_client.services.core.get_projects = AsyncMock(return_value=[
            {"id": "project1", "name": "Test Project 1"},
            {"id": "project2", "name": "Test Project 2"}
        ])
        
        mock_client.services.core.get_project = AsyncMock(return_value={
            "id": "project1",
            "name": "Test Project 1",
            "description": "Test project description"
        })
        
        mock_client.services.git.get_repositories = AsyncMock(return_value=[
            {"id": "repo1", "name": "main", "project": {"id": "project1"}}
        ])
        
        mock_client.services.build.get_builds = AsyncMock(return_value=[
            {"id": "build1", "buildNumber": "1.0.1", "status": "completed"}
        ])
        
        # Mock facades
        mock_client.facades.project.create_complete_project = AsyncMock(return_value={
            "success": True,
            "project": {"id": "new-project", "name": "New Project"}
        })
        
        mock_client.facades.pipeline.create_complete_cicd_pipeline = AsyncMock(return_value={
            "success": True,
            "pipeline": {"id": "new-pipeline", "name": "CI/CD Pipeline"}
        })
        
        mock_client.facades.security.implement_zero_trust_security = AsyncMock(return_value={
            "success": True,
            "policies_created": 5,
            "monitoring_enabled": True
        })
        
        mock_client.facades.integration.setup_complete_devops_integration = AsyncMock(return_value={
            "success": True,
            "integrations_configured": 3
        })
        
        mock_client.facades.governance.implement_enterprise_governance = AsyncMock(return_value={
            "success": True,
            "policies_implemented": 10
        })
        
        mock_client.facades.integration.analyze_integration_health = AsyncMock(return_value={
            "overall_health": "excellent",
            "service_hooks_health": {"success_rate": 0.98},
            "notification_health": {"delivery_success_rate": 0.99}
        })
        
        mock_client.facades.security.conduct_security_audit = AsyncMock(return_value={
            "overall_score": 85,
            "critical_issues": 0,
            "recommendations": ["Enable MFA", "Review permissions"]
        })
        
        mock_client.test_connection = AsyncMock(return_value={
            "connection_status": "success",
            "auth_status": "valid",
            "response_time": 250
        })
        
        mock_client.get_client_info = AsyncMock(return_value={
            "organization": "test-org",
            "auth_type": "pat",
            "client_version": "1.0.0"
        })
        
        mock_client.close = AsyncMock()
        
        return mock_client
    
    @pytest.fixture
    def mock_wrapper_service(self, mock_azure_devops_client):
        """Mock wrapper service"""
        with patch('src.services.azure_devops_wrapper_service.azure_devops_wrapper_service') as mock_service:
            mock_service.client = mock_azure_devops_client
            mock_service.test_connection = mock_azure_devops_client.test_connection
            mock_service.get_client_info = mock_azure_devops_client.get_client_info
            mock_service.get_projects = mock_azure_devops_client.services.core.get_projects
            mock_service.get_project = mock_azure_devops_client.services.core.get_project
            mock_service.get_repositories = mock_azure_devops_client.services.git.get_repositories
            mock_service.get_builds = mock_azure_devops_client.services.build.get_builds
            mock_service.create_complete_project = mock_azure_devops_client.facades.project.create_complete_project
            mock_service.setup_cicd_pipeline = mock_azure_devops_client.facades.pipeline.create_complete_cicd_pipeline
            mock_service.implement_security_governance = mock_azure_devops_client.facades.security.implement_zero_trust_security
            mock_service.setup_devops_integrations = mock_azure_devops_client.facades.integration.setup_complete_devops_integration
            mock_service.implement_enterprise_governance = mock_azure_devops_client.facades.governance.implement_enterprise_governance
            mock_service.analyze_integration_health = mock_azure_devops_client.facades.integration.analyze_integration_health
            mock_service.conduct_security_audit = mock_azure_devops_client.facades.security.conduct_security_audit
            mock_service.close = mock_azure_devops_client.close
            yield mock_service


class TestHealthAndStatus:
    """Test health and status endpoints"""
    
    def test_health_endpoint(self, client, mock_wrapper_service):
        """Test health check endpoint"""
        response = client.get("/api/v1/azure-devops/health")
        assert response.status_code == 200
        data = response.json()
        assert data["connection_status"] == "success"
        assert data["auth_status"] == "valid"
    
    def test_client_info_endpoint(self, client, mock_wrapper_service):
        """Test client info endpoint"""
        response = client.get("/api/v1/azure-devops/info")
        assert response.status_code == 200
        data = response.json()
        assert data["organization"] == "test-org"
        assert data["auth_type"] == "pat"


class TestProjectManagement:
    """Test project management endpoints"""
    
    def test_get_projects(self, client, mock_wrapper_service):
        """Test getting all projects"""
        response = client.get("/api/v1/azure-devops/projects")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Test Project 1"
    
    def test_get_specific_project(self, client, mock_wrapper_service):
        """Test getting specific project"""
        response = client.get("/api/v1/azure-devops/projects/project1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "project1"
        assert data["name"] == "Test Project 1"
    
    def test_create_complete_project(self, client, mock_wrapper_service):
        """Test creating complete project"""
        project_data = {
            "project_name": "New Test Project",
            "description": "Test project description",
            "source_control": "git",
            "work_item_process": "agile",
            "teams": [{"name": "Dev Team", "description": "Development team"}],
            "area_paths": ["Frontend", "Backend"],
            "iteration_paths": ["Sprint 1", "Sprint 2"]
        }
        
        response = client.post("/api/v1/azure-devops/projects/complete", json=project_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Complete project creation initiated"
        assert data["project_name"] == "New Test Project"
        assert data["status"] == "in_progress"


class TestPipelineManagement:
    """Test pipeline management endpoints"""
    
    def test_create_complete_pipeline(self, client, mock_wrapper_service):
        """Test creating complete CI/CD pipeline"""
        pipeline_data = {
            "project_id": "project1",
            "pipeline_name": "Test Pipeline",
            "repository": {"name": "main", "branch": "main"},
            "build_stages": [{"name": "Build", "tasks": ["restore", "build", "test"]}],
            "deployment_stages": [{"name": "Development", "environment": "dev"}],
            "security_scanning": {"enabled": True},
            "notifications": {"email": ["test@example.com"]}
        }
        
        response = client.post("/api/v1/azure-devops/pipelines/complete", json=pipeline_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Complete CI/CD pipeline creation initiated"
        assert data["project_id"] == "project1"
        assert data["status"] == "in_progress"
    
    def test_get_builds(self, client, mock_wrapper_service):
        """Test getting builds"""
        response = client.get("/api/v1/azure-devops/builds?project_id=project1&top=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["buildNumber"] == "1.0.1"


class TestSecurityAndGovernance:
    """Test security and governance endpoints"""
    
    def test_implement_zero_trust_security(self, client, mock_wrapper_service):
        """Test implementing zero-trust security"""
        security_data = {
            "identity_verification": {"mfa_required": True},
            "least_privilege": {"enabled": True},
            "continuous_monitoring": {"enabled": True},
            "data_protection": {"encryption_required": True}
        }
        
        response = client.post("/api/v1/azure-devops/security/zero-trust", json=security_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Zero-trust security implementation initiated"
        assert data["status"] == "in_progress"
    
    def test_conduct_security_audit(self, client, mock_wrapper_service):
        """Test conducting security audit"""
        response = client.get("/api/v1/azure-devops/security/audit")
        assert response.status_code == 200
        data = response.json()
        assert data["overall_score"] == 85
        assert data["critical_issues"] == 0
        assert len(data["recommendations"]) == 2


class TestIntegrationManagement:
    """Test integration management endpoints"""
    
    def test_setup_complete_integrations(self, client, mock_wrapper_service):
        """Test setting up complete integrations"""
        integration_data = {
            "project_id": "project1",
            "chat_integrations": {"slack": {"channels": [{"name": "dev", "webhook_url": "https://hooks.slack.com/test"}]}},
            "monitoring": {"datadog": {"webhook_url": "https://api.datadoghq.com/webhook"}}
        }
        
        response = client.post("/api/v1/azure-devops/integrations/complete", json=integration_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Complete DevOps integrations setup initiated"
        assert data["project_id"] == "project1"
        assert data["status"] == "in_progress"
    
    def test_analyze_integration_health(self, client, mock_wrapper_service):
        """Test analyzing integration health"""
        response = client.get("/api/v1/azure-devops/integrations/health?project_id=project1&days=30")
        assert response.status_code == 200
        data = response.json()
        assert data["overall_health"] == "excellent"
        assert data["service_hooks_health"]["success_rate"] == 0.98


class TestEnterpriseGovernance:
    """Test enterprise governance endpoints"""
    
    def test_implement_enterprise_governance(self, client, mock_wrapper_service):
        """Test implementing enterprise governance"""
        governance_data = {
            "organizational_policies": {
                "security": [{"name": "Code Review Policy", "type": "mandatory"}]
            },
            "compliance_framework": {"standards": ["SOX", "SOC2"]},
            "risk_management": {"enabled": True}
        }
        
        response = client.post("/api/v1/azure-devops/governance/enterprise", json=governance_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Enterprise governance implementation initiated"
        assert data["status"] == "in_progress"


class TestAnalyticsAndReporting:
    """Test analytics and reporting endpoints"""
    
    def test_get_analytics_dashboard(self, client, mock_wrapper_service):
        """Test getting analytics dashboard"""
        response = client.get("/api/v1/azure-devops/analytics/dashboard?project_id=project1&time_range=30d")
        assert response.status_code == 200
        data = response.json()
        assert "integration_health" in data
        assert "security_status" in data
        assert "timestamp" in data


class TestBatchOperations:
    """Test batch operations"""
    
    def test_batch_create_projects(self, client, mock_wrapper_service):
        """Test batch project creation"""
        projects_data = [
            {
                "project_name": "Batch Project 1",
                "description": "First batch project",
                "teams": [{"name": "Team 1", "description": "First team"}]
            },
            {
                "project_name": "Batch Project 2", 
                "description": "Second batch project",
                "teams": [{"name": "Team 2", "description": "Second team"}]
            }
        ]
        
        response = client.post("/api/v1/azure-devops/batch/projects", json=projects_data)
        assert response.status_code == 200
        data = response.json()
        assert "Batch project creation initiated for 2 projects" in data["message"]
        assert data["project_count"] == 2
        assert data["status"] == "in_progress"


class TestTemplates:
    """Test template endpoints"""
    
    def test_get_project_templates(self, client):
        """Test getting project templates"""
        response = client.get("/api/v1/azure-devops/templates/projects")
        assert response.status_code == 200
        data = response.json()
        assert "templates" in data
        assert len(data["templates"]) == 3
        assert data["templates"][0]["id"] == "enterprise_web_app"
    
    def test_get_pipeline_templates(self, client):
        """Test getting pipeline templates"""
        response = client.get("/api/v1/azure-devops/templates/pipelines")
        assert response.status_code == 200
        data = response.json()
        assert "templates" in data
        assert len(data["templates"]) == 3
        assert data["templates"][0]["id"] == "dotnet_webapp"


# Performance and Load Testing
class TestPerformance:
    """Performance and load testing"""
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, async_client, mock_wrapper_service):
        """Test handling concurrent requests"""
        tasks = []
        for i in range(10):
            task = async_client.get("/api/v1/azure-devops/projects")
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2


# Integration Testing with Real Azure DevOps (Optional)
class TestRealIntegration:
    """Integration tests with real Azure DevOps (requires credentials)"""
    
    @pytest.mark.integration
    @pytest.mark.skipif(not pytest.config.getoption("--integration"), reason="Integration tests not enabled")
    async def test_real_connection(self):
        """Test real connection to Azure DevOps"""
        # This would test with real credentials if available
        # Skip by default to avoid requiring real credentials
        pass


# Fixtures for authentication
@pytest.fixture
def mock_auth():
    """Mock authentication"""
    with patch('src.core.auth.get_current_user') as mock_user:
        mock_user.return_value = {"user_id": "test-user", "roles": ["admin"]}
        yield mock_user


# Apply mock auth to all tests
@pytest.fixture(autouse=True)
def setup_auth(mock_auth):
    """Auto-apply auth mock to all tests"""
    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
