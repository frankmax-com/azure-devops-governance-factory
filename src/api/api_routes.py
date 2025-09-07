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
# Import routers from routes subdirectory 
from src.api.routes import azure_devops_enhanced_router, azure_devops_wrapper_direct_router, routes_available

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(work_items.router, prefix="/work-items", tags=["work-items"])
api_router.include_router(repositories.router, prefix="/repositories", tags=["repositories"])
api_router.include_router(pipelines.router, prefix="/pipelines", tags=["pipelines"])
api_router.include_router(governance.router, prefix="/governance", tags=["governance"])
api_router.include_router(compliance.router, prefix="/compliance", tags=["compliance"])

# Include enhanced Azure DevOps wrapper routes with all 2,125+ operations
if routes_available and azure_devops_enhanced_router:
    api_router.include_router(azure_devops_enhanced_router, tags=["Azure DevOps Enhanced"])
    # Include direct Azure DevOps wrapper API routes - ALL OPERATIONS EXPOSED
    api_router.include_router(azure_devops_wrapper_direct_router, tags=["Azure DevOps Direct API"])
else:
    print("Info: Azure DevOps wrapper routes are temporarily disabled due to missing dependencies")
