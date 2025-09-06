"""
Azure DevOps integration service
"""

from typing import List, Optional, Dict, Any
import asyncio
from azure.devops.connection import Connection
from azure.devops.v7_1.core import CoreClient
from azure.devops.v7_1.work_item_tracking import WorkItemTrackingClient
from azure.devops.v7_1.git import GitClient
from azure.devops.v7_1.build import BuildClient
from azure.devops.v7_1.release import ReleaseClient
from msrest.authentication import BasicAuthentication
import structlog

from src.core.config import get_settings
from src.core.cache import cache_manager

settings = get_settings()
logger = structlog.get_logger(__name__)


class AzureDevOpsClient:
    """Azure DevOps API client"""
    
    def __init__(self):
        self.organization_url = f"{settings.AZURE_DEVOPS_BASE_URL}/{settings.AZURE_DEVOPS_ORGANIZATION}"
        self.credentials = BasicAuthentication('', settings.AZURE_CLIENT_SECRET)
        self.connection = Connection(
            base_url=self.organization_url,
            creds=self.credentials
        )
        
        # Initialize clients
        self.core_client = self.connection.clients.get_core_client()
        self.work_item_client = self.connection.clients.get_work_item_tracking_client()
        self.git_client = self.connection.clients.get_git_client()
        self.build_client = self.connection.clients.get_build_client()
        self.release_client = self.connection.clients.get_release_client()
    
    async def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects in the organization"""
        try:
            cache_key = "projects:all"
            cached_projects = await cache_manager.get(cache_key)
            
            if cached_projects:
                return cached_projects
            
            projects = self.core_client.get_projects()
            project_list = []
            
            for project in projects:
                project_dict = {
                    "id": project.id,
                    "name": project.name,
                    "description": project.description,
                    "url": project.url,
                    "state": project.state,
                    "revision": project.revision,
                    "visibility": project.visibility,
                    "last_update_time": project.last_update_time.isoformat() if project.last_update_time else None
                }
                project_list.append(project_dict)
            
            await cache_manager.set(cache_key, project_list, ttl=300)
            return project_list
            
        except Exception as e:
            logger.error("Failed to get projects", error=str(e))
            raise
    
    async def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get specific project by ID"""
        try:
            cache_key = f"project:{project_id}"
            cached_project = await cache_manager.get(cache_key)
            
            if cached_project:
                return cached_project
            
            project = self.core_client.get_project(project_id)
            if not project:
                return None
            
            project_dict = {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "url": project.url,
                "state": project.state,
                "revision": project.revision,
                "visibility": project.visibility,
                "last_update_time": project.last_update_time.isoformat() if project.last_update_time else None,
                "default_team": {
                    "id": project.default_team.id,
                    "name": project.default_team.name,
                    "url": project.default_team.url
                } if project.default_team else None
            }
            
            await cache_manager.set(cache_key, project_dict, ttl=300)
            return project_dict
            
        except Exception as e:
            logger.error("Failed to get project", project_id=project_id, error=str(e))
            raise
    
    async def create_project(
        self,
        name: str,
        description: str = "",
        process_template: str = "Agile",
        source_control_type: str = "Git"
    ) -> Dict[str, Any]:
        """Create new project"""
        try:
            from azure.devops.v7_1.core.models import TeamProject
            
            project_create_parameters = TeamProject(
                name=name,
                description=description,
                capabilities={
                    "versioncontrol": {
                        "sourceControlType": source_control_type
                    },
                    "processTemplate": {
                        "templateTypeId": self._get_process_template_id(process_template)
                    }
                }
            )
            
            # This is a long-running operation
            operation = self.core_client.queue_create_project(project_create_parameters)
            
            # Wait for completion (simplified for demo)
            # In production, this should be handled asynchronously
            await asyncio.sleep(10)
            
            # Get the created project
            project = self.core_client.get_project(name)
            
            project_dict = {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "url": project.url,
                "state": project.state
            }
            
            # Invalidate projects cache
            await cache_manager.delete("projects:all")
            
            logger.info("Project created successfully", project_name=name)
            return project_dict
            
        except Exception as e:
            logger.error("Failed to create project", project_name=name, error=str(e))
            raise
    
    async def get_work_items(
        self,
        project_id: str,
        wiql: str = None,
        ids: List[int] = None
    ) -> List[Dict[str, Any]]:
        """Get work items by query or IDs"""
        try:
            if wiql:
                # Execute WIQL query
                wiql_query = self.work_item_client.query_by_wiql(
                    wiql={"query": wiql},
                    project=project_id
                )
                
                if not wiql_query.work_items:
                    return []
                
                work_item_ids = [wi.id for wi in wiql_query.work_items]
            elif ids:
                work_item_ids = ids
            else:
                # Default query for recent work items
                wiql_query = self.work_item_client.query_by_wiql(
                    wiql={"query": f"SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = '{project_id}' ORDER BY [System.ChangedDate] DESC"},
                    project=project_id
                )
                work_item_ids = [wi.id for wi in wiql_query.work_items[:100]]  # Limit to 100
            
            if not work_item_ids:
                return []
            
            # Get work item details
            work_items = self.work_item_client.get_work_items(
                ids=work_item_ids,
                expand="All"
            )
            
            work_item_list = []
            for wi in work_items:
                work_item_dict = {
                    "id": wi.id,
                    "rev": wi.rev,
                    "url": wi.url,
                    "fields": wi.fields,
                    "relations": wi.relations if wi.relations else [],
                    "links": wi._links.__dict__ if wi._links else {}
                }
                work_item_list.append(work_item_dict)
            
            return work_item_list
            
        except Exception as e:
            logger.error("Failed to get work items", project_id=project_id, error=str(e))
            raise
    
    async def create_work_item(
        self,
        project_id: str,
        work_item_type: str,
        title: str,
        description: str = "",
        assigned_to: str = None,
        area_path: str = None,
        iteration_path: str = None,
        fields: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create new work item"""
        try:
            from azure.devops.v7_1.work_item_tracking.models import JsonPatchOperation
            
            # Build patch document
            patch_document = [
                JsonPatchOperation(
                    op="add",
                    path="/fields/System.Title",
                    value=title
                )
            ]
            
            if description:
                patch_document.append(JsonPatchOperation(
                    op="add",
                    path="/fields/System.Description",
                    value=description
                ))
            
            if assigned_to:
                patch_document.append(JsonPatchOperation(
                    op="add",
                    path="/fields/System.AssignedTo",
                    value=assigned_to
                ))
            
            if area_path:
                patch_document.append(JsonPatchOperation(
                    op="add",
                    path="/fields/System.AreaPath",
                    value=area_path
                ))
            
            if iteration_path:
                patch_document.append(JsonPatchOperation(
                    op="add",
                    path="/fields/System.IterationPath",
                    value=iteration_path
                ))
            
            # Add custom fields
            if fields:
                for field_name, field_value in fields.items():
                    patch_document.append(JsonPatchOperation(
                        op="add",
                        path=f"/fields/{field_name}",
                        value=field_value
                    ))
            
            # Create work item
            work_item = self.work_item_client.create_work_item(
                document=patch_document,
                project=project_id,
                type=work_item_type
            )
            
            work_item_dict = {
                "id": work_item.id,
                "rev": work_item.rev,
                "url": work_item.url,
                "fields": work_item.fields,
                "relations": work_item.relations if work_item.relations else [],
                "links": work_item._links.__dict__ if work_item._links else {}
            }
            
            logger.info("Work item created successfully", work_item_id=work_item.id, title=title)
            return work_item_dict
            
        except Exception as e:
            logger.error("Failed to create work item", project_id=project_id, title=title, error=str(e))
            raise
    
    async def get_repositories(self, project_id: str) -> List[Dict[str, Any]]:
        """Get repositories in project"""
        try:
            cache_key = f"repositories:{project_id}"
            cached_repos = await cache_manager.get(cache_key)
            
            if cached_repos:
                return cached_repos
            
            repositories = self.git_client.get_repositories(project=project_id)
            repo_list = []
            
            for repo in repositories:
                repo_dict = {
                    "id": repo.id,
                    "name": repo.name,
                    "url": repo.url,
                    "project": {
                        "id": repo.project.id,
                        "name": repo.project.name
                    } if repo.project else None,
                    "default_branch": repo.default_branch,
                    "size": repo.size,
                    "remote_url": repo.remote_url,
                    "ssh_url": repo.ssh_url,
                    "web_url": repo.web_url
                }
                repo_list.append(repo_dict)
            
            await cache_manager.set(cache_key, repo_list, ttl=300)
            return repo_list
            
        except Exception as e:
            logger.error("Failed to get repositories", project_id=project_id, error=str(e))
            raise
    
    def _get_process_template_id(self, template_name: str) -> str:
        """Get process template ID by name"""
        # Common process template IDs
        templates = {
            "Agile": "adcc42ab-9882-485e-a3ed-7678f01f66bc",
            "Scrum": "6b724908-ef14-45cf-84f8-768b5384da45",
            "CMMI": "27450541-8e31-4150-9947-dc59f998fc01",
            "Basic": "b8a3a935-7e91-48b8-a94c-606d37c3e9f2"
        }
        return templates.get(template_name, templates["Agile"])
