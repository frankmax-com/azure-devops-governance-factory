"""
Work items management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
import structlog

from src.services.azure_devops_service import AzureDevOpsClient
from src.services.auth_service import AuthService
from src.models.auth import User

router = APIRouter()
logger = structlog.get_logger(__name__)


@router.get("/")
async def get_work_items(
    project_id: str = Query(..., description="Project ID"),
    wiql: Optional[str] = Query(None, description="WIQL query"),
    ids: Optional[str] = Query(None, description="Comma-separated work item IDs"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    azure_client: AzureDevOpsClient = Depends(),
    current_user: User = Depends(AuthService().get_current_user)
):
    """Get work items by query or IDs"""
    try:
        work_item_ids = None
        if ids:
            work_item_ids = [int(id.strip()) for id in ids.split(",") if id.strip()]
        
        work_items = await azure_client.get_work_items(
            project_id=project_id,
            wiql=wiql,
            ids=work_item_ids
        )
        
        # Apply pagination
        total = len(work_items)
        paginated_work_items = work_items[skip:skip + limit]
        
        logger.info(
            "Work items retrieved",
            user_id=current_user.id,
            project_id=project_id,
            total=total,
            returned=len(paginated_work_items)
        )
        
        return {
            "work_items": paginated_work_items,
            "total": total,
            "skip": skip,
            "limit": limit,
            "project_id": project_id
        }
        
    except Exception as e:
        logger.error(
            "Failed to get work items",
            user_id=current_user.id,
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve work items"
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_work_item(
    project_id: str,
    work_item_type: str,
    title: str,
    description: str = "",
    assigned_to: Optional[str] = None,
    area_path: Optional[str] = None,
    iteration_path: Optional[str] = None,
    fields: Optional[Dict[str, Any]] = None,
    azure_client: AzureDevOpsClient = Depends(),
    current_user: User = Depends(AuthService().get_current_user)
):
    """Create new work item"""
    try:
        work_item = await azure_client.create_work_item(
            project_id=project_id,
            work_item_type=work_item_type,
            title=title,
            description=description,
            assigned_to=assigned_to,
            area_path=area_path,
            iteration_path=iteration_path,
            fields=fields or {}
        )
        
        logger.info(
            "Work item created",
            user_id=current_user.id,
            project_id=project_id,
            work_item_id=work_item.get("id"),
            title=title
        )
        
        return work_item
        
    except Exception as e:
        logger.error(
            "Failed to create work item",
            user_id=current_user.id,
            project_id=project_id,
            title=title,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create work item"
        )


@router.get("/{work_item_id}")
async def get_work_item(
    work_item_id: int,
    project_id: str = Query(..., description="Project ID"),
    azure_client: AzureDevOpsClient = Depends(),
    current_user: User = Depends(AuthService().get_current_user)
):
    """Get specific work item by ID"""
    try:
        work_items = await azure_client.get_work_items(
            project_id=project_id,
            ids=[work_item_id]
        )
        
        if not work_items:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Work item not found"
            )
        
        work_item = work_items[0]
        
        logger.info(
            "Work item retrieved",
            user_id=current_user.id,
            project_id=project_id,
            work_item_id=work_item_id
        )
        
        return work_item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Failed to get work item",
            user_id=current_user.id,
            project_id=project_id,
            work_item_id=work_item_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve work item"
        )
