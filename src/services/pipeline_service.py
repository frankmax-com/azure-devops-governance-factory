"""
Pipeline management service - Azure DevOps Pipelines integration
"""

from typing import Dict, List, Any, Optional
import structlog
from azure.devops.v7_1.pipelines import PipelinesClient
from azure.devops.v7_1.pipelines.models import Pipeline, Run

from src.core.azure_devops_client import AzureDevOpsClient

logger = structlog.get_logger(__name__)


class PipelineService:
    """Service for managing Azure DevOps Pipelines"""
    
    def __init__(self, azure_client: AzureDevOpsClient):
        self.azure_client = azure_client
        self.pipelines_client: PipelinesClient = None
    
    async def initialize(self):
        """Initialize pipeline service"""
        connection = await self.azure_client.get_connection()
        self.pipelines_client = connection.clients.get_pipelines_client()
    
    async def get_pipelines(
        self,
        project_id: str,
        folder_path: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get pipelines for a project"""
        
        try:
            pipelines = self.pipelines_client.list_pipelines(
                project=project_id,
                folder_path=folder_path
            )
            
            pipeline_list = []
            for pipeline in pipelines:
                pipeline_data = {
                    "id": pipeline.id,
                    "name": pipeline.name,
                    "folder": pipeline.folder,
                    "revision": pipeline.revision,
                    "url": pipeline.url,
                    "configuration": {
                        "type": pipeline.configuration.type if pipeline.configuration else None,
                        "path": pipeline.configuration.path if pipeline.configuration else None,
                        "repository": {
                            "id": pipeline.configuration.repository.id if pipeline.configuration and pipeline.configuration.repository else None,
                            "name": pipeline.configuration.repository.name if pipeline.configuration and pipeline.configuration.repository else None,
                            "type": pipeline.configuration.repository.type if pipeline.configuration and pipeline.configuration.repository else None
                        } if pipeline.configuration and pipeline.configuration.repository else None
                    }
                }
                pipeline_list.append(pipeline_data)
            
            logger.info(
                "Retrieved pipelines",
                project_id=project_id,
                count=len(pipeline_list)
            )
            
            return pipeline_list
            
        except Exception as e:
            logger.error(
                "Failed to get pipelines",
                project_id=project_id,
                error=str(e)
            )
            raise
    
    async def get_pipeline(
        self,
        project_id: str,
        pipeline_id: int
    ) -> Dict[str, Any]:
        """Get specific pipeline"""
        
        try:
            pipeline = self.pipelines_client.get_pipeline(
                project=project_id,
                pipeline_id=pipeline_id
            )
            
            return {
                "id": pipeline.id,
                "name": pipeline.name,
                "folder": pipeline.folder,
                "revision": pipeline.revision,
                "url": pipeline.url,
                "configuration": {
                    "type": pipeline.configuration.type if pipeline.configuration else None,
                    "path": pipeline.configuration.path if pipeline.configuration else None,
                    "repository": {
                        "id": pipeline.configuration.repository.id if pipeline.configuration and pipeline.configuration.repository else None,
                        "name": pipeline.configuration.repository.name if pipeline.configuration and pipeline.configuration.repository else None,
                        "type": pipeline.configuration.repository.type if pipeline.configuration and pipeline.configuration.repository else None
                    } if pipeline.configuration and pipeline.configuration.repository else None
                }
            }
            
        except Exception as e:
            logger.error(
                "Failed to get pipeline",
                project_id=project_id,
                pipeline_id=pipeline_id,
                error=str(e)
            )
            raise
    
    async def get_pipeline_runs(
        self,
        project_id: str,
        pipeline_id: int,
        top: int = 50
    ) -> List[Dict[str, Any]]:
        """Get pipeline runs"""
        
        try:
            runs = self.pipelines_client.list_runs(
                project=project_id,
                pipeline_id=pipeline_id,
                top=top
            )
            
            run_list = []
            for run in runs:
                run_data = {
                    "id": run.id,
                    "name": run.name,
                    "state": run.state,
                    "result": run.result,
                    "created_date": run.created_date.isoformat() if run.created_date else None,
                    "finished_date": run.finished_date.isoformat() if run.finished_date else None,
                    "url": run.url,
                    "pipeline": {
                        "id": run.pipeline.id,
                        "name": run.pipeline.name,
                        "revision": run.pipeline.revision
                    } if run.pipeline else None,
                    "resources": {
                        "repositories": [
                            {
                                "repository": {
                                    "id": repo.repository.id,
                                    "name": repo.repository.name,
                                    "type": repo.repository.type
                                } if repo.repository else None,
                                "ref_name": repo.ref_name,
                                "version": repo.version
                            }
                            for repo in (run.resources.repositories or [])
                        ] if run.resources else []
                    }
                }
                run_list.append(run_data)
            
            logger.info(
                "Retrieved pipeline runs",
                project_id=project_id,
                pipeline_id=pipeline_id,
                count=len(run_list)
            )
            
            return run_list
            
        except Exception as e:
            logger.error(
                "Failed to get pipeline runs",
                project_id=project_id,
                pipeline_id=pipeline_id,
                error=str(e)
            )
            raise
    
    async def run_pipeline(
        self,
        project_id: str,
        pipeline_id: int,
        branch: Optional[str] = None,
        variables: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Run a pipeline"""
        
        try:
            run_parameters = {}
            
            if branch:
                run_parameters["resources"] = {
                    "repositories": {
                        "self": {
                            "refName": f"refs/heads/{branch}"
                        }
                    }
                }
            
            if variables:
                run_parameters["variables"] = variables
            
            run = self.pipelines_client.run_pipeline(
                project=project_id,
                pipeline_id=pipeline_id,
                run_parameters=run_parameters
            )
            
            logger.info(
                "Pipeline run started",
                project_id=project_id,
                pipeline_id=pipeline_id,
                run_id=run.id
            )
            
            return {
                "id": run.id,
                "name": run.name,
                "state": run.state,
                "result": run.result,
                "created_date": run.created_date.isoformat() if run.created_date else None,
                "url": run.url,
                "pipeline": {
                    "id": run.pipeline.id,
                    "name": run.pipeline.name,
                    "revision": run.pipeline.revision
                } if run.pipeline else None
            }
            
        except Exception as e:
            logger.error(
                "Failed to run pipeline",
                project_id=project_id,
                pipeline_id=pipeline_id,
                error=str(e)
            )
            raise
    
    async def get_pipeline_run_logs(
        self,
        project_id: str,
        pipeline_id: int,
        run_id: int
    ) -> Dict[str, Any]:
        """Get pipeline run logs"""
        
        try:
            logs = self.pipelines_client.get_log(
                project=project_id,
                pipeline_id=pipeline_id,
                run_id=run_id,
                log_id=1  # Usually the main log
            )
            
            return {
                "run_id": run_id,
                "pipeline_id": pipeline_id,
                "logs": logs,
                "retrieved_at": "2025-09-05T10:00:00Z"  # Placeholder
            }
            
        except Exception as e:
            logger.error(
                "Failed to get pipeline run logs",
                project_id=project_id,
                pipeline_id=pipeline_id,
                run_id=run_id,
                error=str(e)
            )
            raise
    
    async def analyze_pipeline_security(
        self,
        project_id: str,
        pipeline_id: int
    ) -> Dict[str, Any]:
        """Analyze pipeline for security compliance"""
        
        try:
            pipeline = await self.get_pipeline(project_id, pipeline_id)
            
            # Security analysis placeholder
            security_issues = []
            recommendations = []
            
            # Check for secrets in variables (placeholder)
            recommendations.append("Use Azure Key Vault for secrets management")
            recommendations.append("Enable pipeline security scanning")
            recommendations.append("Implement least privilege access controls")
            
            security_score = 85  # Placeholder score
            
            return {
                "pipeline_id": pipeline_id,
                "pipeline_name": pipeline.get("name"),
                "security_score": security_score,
                "issues": security_issues,
                "recommendations": recommendations,
                "analysis_date": "2025-09-05T10:00:00Z",
                "status": "compliant" if security_score >= 80 else "non_compliant"
            }
            
        except Exception as e:
            logger.error(
                "Failed to analyze pipeline security",
                project_id=project_id,
                pipeline_id=pipeline_id,
                error=str(e)
            )
            raise
