"""
Test cases for the Azure DevOps Governance Factory
"""

import pytest
from unittest.mock import Mock, AsyncMock
from fastapi.testclient import TestClient
from src.main import app
from src.services.auth_service import AuthService
from src.core.governance_engine import GovernanceEngine
from src.core.compliance_engine import ComplianceEngine


@pytest.fixture
def client():
    """Test client for API endpoints"""
    return TestClient(app)


@pytest.fixture
def mock_auth_service():
    """Mock authentication service"""
    auth_service = Mock(spec=AuthService)
    auth_service.get_current_user = AsyncMock()
    return auth_service


@pytest.fixture
def governance_engine():
    """Governance engine instance"""
    return GovernanceEngine()


@pytest.fixture
def compliance_engine():
    """Compliance engine instance"""
    return ComplianceEngine()


class TestGovernanceEngine:
    """Test governance engine functionality"""
    
    @pytest.mark.asyncio
    async def test_evaluate_pull_request_policy(self, governance_engine):
        """Test pull request policy evaluation"""
        
        context = {
            "type": "pull_request",
            "reviewers": ["user1"],  # Less than required 2
            "work_items": [],  # No linked work items
            "has_tests": False
        }
        
        result = await governance_engine.evaluate_policies(context)
        
        assert result["policy_set"] == "default"
        assert len(result["results"]) == 1
        assert result["results"][0]["type"] == "pull_request"
        
        # Check for violations
        violations = result["results"][0]["violations"]
        assert len(violations) == 1
        assert violations[0]["rule"] == "PR_MIN_REVIEWERS"
        
        # Check for warnings
        warnings = result["results"][0]["warnings"]
        assert len(warnings) == 1
        assert warnings[0]["rule"] == "PR_LINKED_WORK_ITEM"
    
    @pytest.mark.asyncio
    async def test_evaluate_pipeline_policy(self, governance_engine):
        """Test pipeline policy evaluation"""
        
        context = {
            "type": "pipeline",
            "has_security_scan": False,
            "has_tests": True,
            "has_approvals": True
        }
        
        result = await governance_engine.evaluate_policies(context)
        
        assert result["policy_set"] == "default"
        assert len(result["results"]) == 1
        assert result["results"][0]["type"] == "pipeline"
        
        # Check for violations
        violations = result["results"][0]["violations"]
        assert len(violations) == 1
        assert violations[0]["rule"] == "PIPELINE_SECURITY_SCAN"
    
    @pytest.mark.asyncio
    async def test_enforce_policy(self, governance_engine):
        """Test policy enforcement"""
        
        context = {"type": "pull_request", "id": "PR-123"}
        
        result = await governance_engine.enforce_policy(
            "PR_MIN_REVIEWERS",
            context,
            "block"
        )
        
        assert result["policy_id"] == "PR_MIN_REVIEWERS"
        assert result["action"] == "block"
        assert result["result"] == "success"
        assert result["blocked"] is True


class TestComplianceEngine:
    """Test compliance engine functionality"""
    
    @pytest.mark.asyncio
    async def test_cmmi_validation_compliant(self, compliance_engine):
        """Test CMMI compliance validation - compliant case"""
        
        project_data = {
            "requirements_traceability": True,
            "project_plan": True,
            "version_control": True,
            "quality_assurance": True
        }
        
        result = await compliance_engine.validate_compliance("cmmi", project_data)
        
        assert result["framework"] == "CMMI"
        assert result["level"] == 3
        assert result["status"] == "compliant"
        assert result["score"] == 100
        assert len(result["violations"]) == 0
    
    @pytest.mark.asyncio
    async def test_cmmi_validation_non_compliant(self, compliance_engine):
        """Test CMMI compliance validation - non-compliant case"""
        
        project_data = {
            "requirements_traceability": False,
            "project_plan": False,
            "version_control": True,
            "quality_assurance": True
        }
        
        result = await compliance_engine.validate_compliance("cmmi", project_data)
        
        assert result["framework"] == "CMMI"
        assert result["status"] == "non_compliant"
        assert result["score"] == 70  # 100 - 15 - 15 = 70
        assert len(result["violations"]) == 2
    
    @pytest.mark.asyncio
    async def test_sox_validation(self, compliance_engine):
        """Test SOX compliance validation"""
        
        project_data = {
            "management_certification": True,
            "internal_controls": False,
            "audit_trail": True
        }
        
        result = await compliance_engine.validate_compliance("sox", project_data)
        
        assert result["framework"] == "SOX"
        assert result["status"] == "compliant"  # Score 75 (100-25) >= 75
        assert len(result["violations"]) == 1
    
    @pytest.mark.asyncio
    async def test_gdpr_validation(self, compliance_engine):
        """Test GDPR compliance validation"""
        
        project_data = {
            "privacy_by_design": True,
            "data_subject_rights": True,
            "breach_notification": False
        }
        
        result = await compliance_engine.validate_compliance("gdpr", project_data)
        
        assert result["framework"] == "GDPR"
        assert result["status"] == "compliant"  # Score 85 (100-15) >= 80
        assert len(result["violations"]) == 1
    
    @pytest.mark.asyncio
    async def test_generate_compliance_report(self, compliance_engine):
        """Test compliance report generation"""
        
        validation_results = {
            "status": "compliant",
            "score": 85,
            "recommendations": ["Implement additional security measures"]
        }
        
        report = await compliance_engine.generate_compliance_report(
            "cmmi",
            "project_123",
            validation_results
        )
        
        assert "report_id" in report
        assert report["framework"] == "cmmi"
        assert report["project_id"] == "project_123"
        assert report["overall_status"] == "compliant"
        assert report["compliance_score"] == 85


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_auth_login_endpoint(self, client):
        """Test authentication login endpoint"""
        login_data = {
            "username": "test@example.com",
            "password": "testpassword"
        }
        
        # This will fail authentication but test the endpoint structure
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code in [200, 401, 422]  # Valid HTTP responses


class TestIntegration:
    """Integration test cases"""
    
    @pytest.mark.asyncio
    async def test_governance_compliance_integration(self, governance_engine, compliance_engine):
        """Test integration between governance and compliance engines"""
        
        # Evaluate governance policies
        context = {
            "type": "work_item",
            "area_path": "MyProject\\Development",
            "effort": 8,
            "acceptance_criteria": "Feature must work correctly"
        }
        
        governance_result = await governance_engine.evaluate_policies(context)
        
        # Convert governance results to compliance validation
        project_data = {
            "requirements_traceability": True,  # Based on governance results
            "project_plan": True,
            "version_control": True,
            "quality_assurance": len(governance_result["results"][0]["violations"]) == 0
        }
        
        compliance_result = await compliance_engine.validate_compliance("cmmi", project_data)
        
        assert governance_result is not None
        assert compliance_result is not None
        assert compliance_result["framework"] == "CMMI"


if __name__ == "__main__":
    pytest.main([__file__])
