"""
Pipeline management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
import structlog

from src.services.auth_service import AuthService
from src.services.pipeline_service import PipelineService
from src.core.azure_devops_client import AzureDevOpsClient
from src.models.auth import User

router = APIRouter()
logger = structlog.get_logger(__name__)


async def get_pipeline_service() -> PipelineService:
    """Get pipeline service instance"""
    azure_client = AzureDevOpsClient()
    pipeline_service = PipelineService(azure_client)
    await pipeline_service.initialize()
    return pipeline_service


@router.get("/")
async def get_pipelines(
    project_id: str,
    folder_path: Optional[str] = None,
    current_user: User = Depends(AuthService().get_current_user),
    pipeline_service: PipelineService = Depends(get_pipeline_service)
):
    """Get pipelines for project"""
    
    try:
        pipelines = await pipeline_service.get_pipelines(
            project_id=project_id,
            folder_path=folder_path
        )
        
        logger.info(
            "Retrieved pipelines",
            user_id=current_user.id,
            project_id=project_id,
            count=len(pipelines)
        )
        
        return {
            "pipelines": pipelines,
            "project_id": project_id,
            "total_count": len(pipelines)
        }
        
    except Exception as e:
        logger.error(
            "Failed to get pipelines",
            user_id=current_user.id,
            project_id=project_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve pipelines: {str(e)}"
        )


@router.get("/{pipeline_id}")
async def get_pipeline(
    pipeline_id: int,
    project_id: str,
    current_user: User = Depends(AuthService().get_current_user),
    pipeline_service: PipelineService = Depends(get_pipeline_service)
):
    """Get specific pipeline"""
    
    try:
        pipeline = await pipeline_service.get_pipeline(
            project_id=project_id,
            pipeline_id=pipeline_id
        )
        
        logger.info(
            "Retrieved pipeline",
            user_id=current_user.id,
            project_id=project_id,
            pipeline_id=pipeline_id
        )
        
        return pipeline
        
    except Exception as e:
        logger.error(
            "Failed to get pipeline",
            user_id=current_user.id,
            project_id=project_id,
            pipeline_id=pipeline_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline not found: {str(e)}"
        )


@router.post("/{pipeline_id}/run")
async def run_pipeline(
    pipeline_id: int,
    project_id: str,
    branch: Optional[str] = None,
    variables: Optional[Dict[str, str]] = None,
    current_user: User = Depends(AuthService().get_current_user),
    pipeline_service: PipelineService = Depends(get_pipeline_service)
):
    """Run a pipeline"""
    
    try:
        run_result = await pipeline_service.run_pipeline(
            project_id=project_id,
            pipeline_id=pipeline_id,
            branch=branch,
            variables=variables
        )
        
        logger.info(
            "Pipeline run started",
            user_id=current_user.id,
            project_id=project_id,
            pipeline_id=pipeline_id,
            run_id=run_result.get("id")
        )
        
        return run_result
        
    except Exception as e:
        logger.error(
            "Failed to run pipeline",
            user_id=current_user.id,
            project_id=project_id,
            pipeline_id=pipeline_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to run pipeline: {str(e)}"
        )


@router.get("/{pipeline_id}/runs")
async def get_pipeline_runs(
    pipeline_id: int,
    project_id: str,
    top: int = 50,
    current_user: User = Depends(AuthService().get_current_user),
    pipeline_service: PipelineService = Depends(get_pipeline_service)
):
    """Get pipeline runs"""
    
    try:
        runs = await pipeline_service.get_pipeline_runs(
            project_id=project_id,
            pipeline_id=pipeline_id,
            top=top
        )
        
        logger.info(
            "Retrieved pipeline runs",
            user_id=current_user.id,
            project_id=project_id,
            pipeline_id=pipeline_id,
            count=len(runs)
        )
        
        return {
            "runs": runs,
            "pipeline_id": pipeline_id,
            "total_count": len(runs)
        }
        
    except Exception as e:
        logger.error(
            "Failed to get pipeline runs",
            user_id=current_user.id,
            project_id=project_id,
            pipeline_id=pipeline_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve pipeline runs: {str(e)}"
        )


@router.get("/{pipeline_id}/runs/{run_id}/logs")
async def get_pipeline_run_logs(
    pipeline_id: int,
    run_id: int,
    project_id: str,
    current_user: User = Depends(AuthService().get_current_user),
    pipeline_service: PipelineService = Depends(get_pipeline_service)
):
    """Get pipeline run logs"""
    
    try:
        logs = await pipeline_service.get_pipeline_run_logs(
            project_id=project_id,
            pipeline_id=pipeline_id,
            run_id=run_id
        )
        
        logger.info(
            "Retrieved pipeline run logs",
            user_id=current_user.id,
            project_id=project_id,
            pipeline_id=pipeline_id,
            run_id=run_id
        )
        
        return logs
        
    except Exception as e:
        logger.error(
            "Failed to get pipeline run logs",
            user_id=current_user.id,
            project_id=project_id,
            pipeline_id=pipeline_id,
            run_id=run_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline run logs not found: {str(e)}"
        )


@router.get("/{pipeline_id}/security-analysis")
async def analyze_pipeline_security(
    pipeline_id: int,
    project_id: str,
    current_user: User = Depends(AuthService().get_current_user),
    pipeline_service: PipelineService = Depends(get_pipeline_service)
):
    """Analyze pipeline security compliance"""
    
    try:
        analysis = await pipeline_service.analyze_pipeline_security(
            project_id=project_id,
            pipeline_id=pipeline_id
        )
        
        logger.info(
            "Pipeline security analysis completed",
            user_id=current_user.id,
            project_id=project_id,
            pipeline_id=pipeline_id,
            security_score=analysis.get("security_score")
        )
        
        return analysis
        
    except Exception as e:
        logger.error(
            "Failed to analyze pipeline security",
            user_id=current_user.id,
            project_id=project_id,
            pipeline_id=pipeline_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze pipeline security: {str(e)}"
        )
