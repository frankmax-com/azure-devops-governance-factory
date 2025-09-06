"""
Enhanced Azure DevOps API Routes using the comprehensive wrapper
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel, Field
from datetime import datetime

from src.services.azure_devops_wrapper_service import azure_devops_wrapper_service
from src.core.auth import get_current_user

# API Router
router = APIRouter(prefix="/azure-devops", tags=["Azure DevOps"])


# Request/Response Models
class ProjectCreationRequest(BaseModel):
    """Request model for creating a complete project"""
    project_name: str = Field(..., description="Name of the project to create")
    description: str = Field("", description="Project description")
    source_control: str = Field("git", description="Source control type")
    work_item_process: str = Field("agile", description="Work item process template")
    teams: List[Dict[str, str]] = Field(default=[], description="Teams to create")
    area_paths: List[str] = Field(default=[], description="Area paths to create")
    iteration_paths: List[str] = Field(default=[], description="Iteration paths to create")
    security_config: Dict[str, Any] = Field(default={}, description="Security configuration")


class PipelineCreationRequest(BaseModel):
    """Request model for creating a CI/CD pipeline"""
    project_id: str = Field(..., description="Target project ID")
    pipeline_name: str = Field(..., description="Pipeline name")
    repository: Dict[str, str] = Field(..., description="Repository configuration")
    build_stages: List[Dict[str, Any]] = Field(..., description="Build stages configuration")
    deployment_stages: List[Dict[str, Any]] = Field(..., description="Deployment stages configuration")
    security_scanning: Dict[str, Any] = Field(default={}, description="Security scanning configuration")
    notifications: Dict[str, Any] = Field(default={}, description="Notification configuration")


class SecurityGovernanceRequest(BaseModel):
    """Request model for implementing security governance"""
    identity_verification: Dict[str, Any] = Field(..., description="Identity verification settings")
    least_privilege: Dict[str, Any] = Field(..., description="Least privilege settings")
    continuous_monitoring: Dict[str, Any] = Field(..., description="Continuous monitoring settings")
    data_protection: Dict[str, Any] = Field(..., description="Data protection settings")


class IntegrationRequest(BaseModel):
    """Request model for DevOps integrations"""
    project_id: str = Field(..., description="Target project ID")
    chat_integrations: Dict[str, Any] = Field(default={}, description="Chat platform integrations")
    issue_tracking: Dict[str, Any] = Field(default={}, description="Issue tracking integrations")
    monitoring: Dict[str, Any] = Field(default={}, description="Monitoring integrations")
    ci_cd_tools: Dict[str, Any] = Field(default={}, description="CI/CD tool integrations")


class GovernanceRequest(BaseModel):
    """Request model for enterprise governance"""
    organizational_policies: Dict[str, Any] = Field(..., description="Organizational policies")
    project_governance: Dict[str, Any] = Field(default={}, description="Project governance")
    security_governance: Dict[str, Any] = Field(default={}, description="Security governance")
    compliance_framework: Dict[str, Any] = Field(default={}, description="Compliance framework")
    risk_management: Dict[str, Any] = Field(default={}, description="Risk management")


# Health and Status Endpoints
@router.get("/health")
async def health_check():
    """Check Azure DevOps service health"""
    return await azure_devops_wrapper_service.test_connection()


@router.get("/info")
async def get_client_info():
    """Get Azure DevOps client information"""
    return await azure_devops_wrapper_service.get_client_info()


# Project Management Endpoints
@router.get("/projects")
async def get_projects(current_user: dict = Depends(get_current_user)):
    """Get all Azure DevOps projects"""
    return await azure_devops_wrapper_service.get_projects()


@router.get("/projects/{project_id}")
async def get_project(
    project_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get specific Azure DevOps project"""
    return await azure_devops_wrapper_service.get_project(project_id)


@router.post("/projects/complete")
async def create_complete_project(
    request: ProjectCreationRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Create a complete project with full setup using the project facade"""
    project_config = {
        "description": request.description,
        "source_control": request.source_control,
        "work_item_process": request.work_item_process,
        "teams": request.teams,
        "area_paths": request.area_paths,
        "iteration_paths": request.iteration_paths,
        "security": request.security_config,
        "version_control": {
            "repository_name": "main",
            "initial_branch": "main"
        }
    }
    
    # Execute project creation in background for long-running operations
    background_tasks.add_task(
        azure_devops_wrapper_service.create_complete_project,
        request.project_name,
        project_config
    )
    
    return {
        "message": "Complete project creation initiated",
        "project_name": request.project_name,
        "status": "in_progress"
    }


# Pipeline Management Endpoints
@router.post("/pipelines/complete")
async def create_complete_pipeline(
    request: PipelineCreationRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Create a complete CI/CD pipeline using the pipeline facade"""
    pipeline_config = {
        "name": request.pipeline_name,
        "repository": request.repository,
        "build_stages": request.build_stages,
        "deployment_stages": request.deployment_stages,
        "security_scanning": request.security_scanning,
        "notifications": request.notifications
    }
    
    background_tasks.add_task(
        azure_devops_wrapper_service.setup_cicd_pipeline,
        request.project_id,
        pipeline_config
    )
    
    return {
        "message": "Complete CI/CD pipeline creation initiated",
        "project_id": request.project_id,
        "pipeline_name": request.pipeline_name,
        "status": "in_progress"
    }


@router.get("/builds")
async def get_builds(
    project_id: Optional[str] = Query(None, description="Project ID filter"),
    top: int = Query(50, description="Number of builds to return"),
    current_user: dict = Depends(get_current_user)
):
    """Get builds from Azure DevOps"""
    return await azure_devops_wrapper_service.get_builds(project_id=project_id, top=top)


# Repository Management Endpoints
@router.get("/projects/{project_id}/repositories")
async def get_repositories(
    project_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get repositories for a project"""
    return await azure_devops_wrapper_service.get_repositories(project_id)


# Security and Governance Endpoints
@router.post("/security/zero-trust")
async def implement_zero_trust_security(
    request: SecurityGovernanceRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Implement zero-trust security framework"""
    security_config = {
        "identity_verification": request.identity_verification,
        "least_privilege": request.least_privilege,
        "continuous_monitoring": request.continuous_monitoring,
        "data_protection": request.data_protection
    }
    
    background_tasks.add_task(
        azure_devops_wrapper_service.implement_security_governance,
        security_config
    )
    
    return {
        "message": "Zero-trust security implementation initiated",
        "status": "in_progress"
    }


@router.get("/security/audit")
async def conduct_security_audit(current_user: dict = Depends(get_current_user)):
    """Conduct comprehensive security audit"""
    return await azure_devops_wrapper_service.conduct_security_audit()


# Integration Management Endpoints
@router.post("/integrations/complete")
async def setup_complete_integrations(
    request: IntegrationRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Set up complete DevOps integrations"""
    integration_config = {
        "chat_integrations": request.chat_integrations,
        "issue_tracking": request.issue_tracking,
        "monitoring": request.monitoring,
        "ci_cd_tools": request.ci_cd_tools
    }
    
    background_tasks.add_task(
        azure_devops_wrapper_service.setup_devops_integrations,
        request.project_id,
        integration_config
    )
    
    return {
        "message": "Complete DevOps integrations setup initiated",
        "project_id": request.project_id,
        "status": "in_progress"
    }


@router.get("/integrations/health")
async def analyze_integration_health(
    project_id: Optional[str] = Query(None, description="Project ID filter"),
    days: int = Query(30, description="Analysis period in days"),
    current_user: dict = Depends(get_current_user)
):
    """Analyze integration health and performance"""
    return await azure_devops_wrapper_service.analyze_integration_health(
        project_id=project_id,
        days=days
    )


# Enterprise Governance Endpoints
@router.post("/governance/enterprise")
async def implement_enterprise_governance(
    request: GovernanceRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Implement enterprise governance framework"""
    governance_config = {
        "organizational_policies": request.organizational_policies,
        "project_governance": request.project_governance,
        "security_governance": request.security_governance,
        "compliance_framework": request.compliance_framework,
        "risk_management": request.risk_management
    }
    
    background_tasks.add_task(
        azure_devops_wrapper_service.implement_enterprise_governance,
        governance_config
    )
    
    return {
        "message": "Enterprise governance implementation initiated",
        "status": "in_progress"
    }


# Analytics and Reporting Endpoints
@router.get("/analytics/dashboard")
async def get_analytics_dashboard(
    project_id: Optional[str] = Query(None, description="Project ID filter"),
    time_range: str = Query("30d", description="Time range for analytics"),
    current_user: dict = Depends(get_current_user)
):
    """Get comprehensive analytics dashboard data"""
    # This would combine multiple analytics sources
    dashboard_data = {
        "integration_health": await azure_devops_wrapper_service.analyze_integration_health(
            project_id=project_id,
            days=30 if time_range == "30d" else 7
        ),
        "security_status": await azure_devops_wrapper_service.conduct_security_audit(),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    return dashboard_data


# Batch Operations Endpoints
@router.post("/batch/projects")
async def batch_create_projects(
    projects: List[ProjectCreationRequest],
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Create multiple projects in batch"""
    batch_id = f"batch_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    
    for project in projects:
        project_config = {
            "description": project.description,
            "source_control": project.source_control,
            "work_item_process": project.work_item_process,
            "teams": project.teams,
            "area_paths": project.area_paths,
            "iteration_paths": project.iteration_paths,
            "security": project.security_config
        }
        
        background_tasks.add_task(
            azure_devops_wrapper_service.create_complete_project,
            project.project_name,
            project_config
        )
    
    return {
        "message": f"Batch project creation initiated for {len(projects)} projects",
        "batch_id": batch_id,
        "project_count": len(projects),
        "status": "in_progress"
    }


# Template Management Endpoints
@router.get("/templates/projects")
async def get_project_templates():
    """Get available project templates"""
    return {
        "templates": [
            {
                "id": "enterprise_web_app",
                "name": "Enterprise Web Application",
                "description": "Full-stack web application with CI/CD",
                "includes": ["git_repo", "build_pipeline", "release_pipeline", "security_scanning"]
            },
            {
                "id": "microservices_platform",
                "name": "Microservices Platform",
                "description": "Multi-service architecture with container orchestration",
                "includes": ["multiple_repos", "container_pipeline", "kubernetes_deployment"]
            },
            {
                "id": "data_analytics_project",
                "name": "Data Analytics Project",
                "description": "Data science and analytics project setup",
                "includes": ["jupyter_notebooks", "data_pipeline", "ml_models"]
            }
        ]
    }


@router.get("/templates/pipelines")
async def get_pipeline_templates():
    """Get available pipeline templates"""
    return {
        "templates": [
            {
                "id": "dotnet_webapp",
                "name": ".NET Web Application",
                "description": "Complete .NET web app CI/CD pipeline",
                "stages": ["build", "test", "security_scan", "deploy"]
            },
            {
                "id": "node_microservice",
                "name": "Node.js Microservice",
                "description": "Node.js microservice with Docker deployment",
                "stages": ["build", "test", "docker_build", "deploy"]
            },
            {
                "id": "python_ml_pipeline",
                "name": "Python ML Pipeline",
                "description": "Machine learning model training and deployment",
                "stages": ["data_prep", "train", "evaluate", "deploy"]
            }
        ]
    }
