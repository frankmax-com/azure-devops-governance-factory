"""
Project management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
import structlog

from src.services.azure_devops_service import AzureDevOpsClient
from src.services.auth_service import AuthService
from src.models.auth import User

router = APIRouter()
logger = structlog.get_logger(__name__)


class ProjectResponse:
    """Project response model"""
    pass


class ProjectCreateRequest:
    """Project creation request model"""
    pass


@router.get("/", response_model=List[dict])
async def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    azure_client: AzureDevOpsClient = Depends(),
    current_user: User = Depends(AuthService().get_current_user)
):
    """Get all projects in the organization"""
    try:
        projects = await azure_client.get_projects()
        
        # Apply pagination
        total = len(projects)
        paginated_projects = projects[skip:skip + limit]
        
        logger.info(
            "Projects retrieved",
            user_id=current_user.id,
            total=total,
            returned=len(paginated_projects)
        )
        
        return {
            "projects": paginated_projects,
            "total": total,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error("Failed to get projects", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve projects"
        )


@router.get("/{project_id}")
async def get_project(
    project_id: str,
    azure_client: AzureDevOpsClient = Depends(),
    current_user: User = Depends(AuthService().get_current_user)
):
    """Get specific project by ID"""
    try:
        project = await azure_client.get_project(project_id)
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        logger.info(
            "Project retrieved",
            user_id=current_user.id,
            project_id=project_id,
            project_name=project.get("name")
        )
        
        return project
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to get project",
            user_id=current_user.id,
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve project"
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_project(
    name: str,
    description: str = "",
    process_template: str = "Agile",
    source_control_type: str = "Git",
    azure_client: AzureDevOpsClient = Depends(),
    current_user: User = Depends(AuthService().get_current_user)
):
    """Create new project"""
    try:
        # Check if user has admin permissions
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to create project"
            )
        
        project = await azure_client.create_project(
            name=name,
            description=description,
            process_template=process_template,
            source_control_type=source_control_type
        )
        
        logger.info(
            "Project created",
            user_id=current_user.id,
            project_id=project.get("id"),
            project_name=name
        )
        
        return project
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to create project",
            user_id=current_user.id,
            project_name=name,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project"
        )


@router.get("/{project_id}/repositories")
async def get_project_repositories(
    project_id: str,
    azure_client: AzureDevOpsClient = Depends(),
    current_user: User = Depends(AuthService().get_current_user)
):
    """Get repositories in project"""
    try:
        repositories = await azure_client.get_repositories(project_id)
        
        logger.info(
            "Project repositories retrieved",
            user_id=current_user.id,
            project_id=project_id,
            repository_count=len(repositories)
        )
        
        return {
            "project_id": project_id,
            "repositories": repositories,
            "total": len(repositories)
        }
        
    except Exception as e:
        logger.error(
            "Failed to get project repositories",
            user_id=current_user.id,
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve project repositories"
        )
