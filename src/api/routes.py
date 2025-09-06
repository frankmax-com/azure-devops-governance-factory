"""
Main API router configuration
"""

from fastapi import APIRouter
from src.api.endpoints import (
    projects,
    work_items,
    repositories,
    pipelines,
    governance,
    compliance,
    auth
)

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(work_items.router, prefix="/work-items", tags=["work-items"])
api_router.include_router(repositories.router, prefix="/repositories", tags=["repositories"])
api_router.include_router(pipelines.router, prefix="/pipelines", tags=["pipelines"])
api_router.include_router(governance.router, prefix="/governance", tags=["governance"])
api_router.include_router(compliance.router, prefix="/compliance", tags=["compliance"])
