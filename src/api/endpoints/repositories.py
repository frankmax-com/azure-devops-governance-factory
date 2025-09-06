"""
Repository management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
import structlog

from src.services.azure_devops_service import AzureDevOpsClient
from src.services.auth_service import AuthService
from src.models.auth import User

router = APIRouter()
logger = structlog.get_logger(__name__)


@router.get("/")
async def get_repositories(
    project_id: str,
    azure_client: AzureDevOpsClient = Depends(),
    current_user: User = Depends(AuthService().get_current_user)
):
    """Get repositories in project"""
    try:
        repositories = await azure_client.get_repositories(project_id)
        
        logger.info(
            "Repositories retrieved",
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
            "Failed to get repositories",
            user_id=current_user.id,
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve repositories"
        )
