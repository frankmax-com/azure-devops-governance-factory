"""
Core service for Azure DevOps - Projects, Teams, Processes, etc.
"""

from typing import Optional, List, Dict, Any
from ..core import HTTPClient, create_paginator
from ..models import (
    TeamProject, WebApiTeam, Process, InstalledExtension, OrganizationInfo,
    ProjectCreateRequest, TeamCreateRequest, ProjectUpdateRequest,
    ProjectsResponse, TeamsResponse, ProcessesResponse, ExtensionsResponse,
    TeamMember, TeamMembersRef, OperationReference
)


class CoreService:
    """Service for Core Azure DevOps operations."""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    # Projects
    async def list_projects(
        self,
        state_filter: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        get_default_team_image_url: Optional[bool] = None
    ) -> List[TeamProject]:
        """
        List team projects in the organization.
        
        Args:
            state_filter: Filter projects by state (wellFormed, createPending, etc.)
            top: Maximum number of projects to return
            skip: Number of projects to skip
            get_default_team_image_url: Include default team image URL
            
        Returns:
            List of team projects
        """
        params = {}
        if state_filter:
            params['stateFilter'] = state_filter
        if top:
            params['$top'] = top
        if skip:
            params['$skip'] = skip
        if get_default_team_image_url:
            params['getDefaultTeamImageUrl'] = get_default_team_image_url
        
        response_data = await self.client.get_json("projects", params=params)
        response = ProjectsResponse(**response_data)
        return response.value
    
    async def get_project(
        self,
        project_id: str,
        include_capabilities: Optional[bool] = None,
        include_history: Optional[bool] = None
    ) -> TeamProject:
        """
        Get a specific project by ID or name.
        
        Args:
            project_id: Project ID or name
            include_capabilities: Include project capabilities
            include_history: Include project history
            
        Returns:
            Team project details
        """
        params = {}
        if include_capabilities:
            params['includeCapabilities'] = include_capabilities
        if include_history:
            params['includeHistory'] = include_history
        
        response_data = await self.client.get_json(f"projects/{project_id}", params=params)
        return TeamProject(**response_data)
    
    async def create_project(self, project_request: ProjectCreateRequest) -> OperationReference:
        """
        Create a new team project.
        
        Args:
            project_request: Project creation request
            
        Returns:
            Operation reference for tracking creation status
        """
        response_data = await self.client.post_json(
            "projects",
            data=project_request.dict_exclude_none()
        )
        return OperationReference(**response_data)
    
    async def update_project(
        self,
        project_id: str,
        project_update: ProjectUpdateRequest
    ) -> OperationReference:
        """
        Update an existing project.
        
        Args:
            project_id: Project ID or name
            project_update: Project update request
            
        Returns:
            Operation reference for tracking update status
        """
        response_data = await self.client.patch_json(
            f"projects/{project_id}",
            data=project_update.dict_exclude_none()
        )
        return OperationReference(**response_data)
    
    async def delete_project(self, project_id: str) -> OperationReference:
        """
        Delete a project.
        
        Args:
            project_id: Project ID or name
            
        Returns:
            Operation reference for tracking deletion status
        """
        response_data = await self.client.delete(f"projects/{project_id}")
        return OperationReference(**response_data.json())
    
    # Teams
    async def list_teams(
        self,
        project_id: Optional[str] = None,
        mine: Optional[bool] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[WebApiTeam]:
        """
        List teams in the organization or project.
        
        Args:
            project_id: Project ID to filter teams (if None, lists all teams)
            mine: Filter to teams the current user is a member of
            top: Maximum number of teams to return
            skip: Number of teams to skip
            
        Returns:
            List of teams
        """
        params = {}
        if mine:
            params['$mine'] = mine
        if top:
            params['$top'] = top
        if skip:
            params['$skip'] = skip
        
        endpoint = "teams" if not project_id else f"projects/{project_id}/teams"
        response_data = await self.client.get_json(endpoint, params=params)
        response = TeamsResponse(**response_data)
        return response.value
    
    async def get_team(self, project_id: str, team_id: str) -> WebApiTeam:
        """
        Get a specific team.
        
        Args:
            project_id: Project ID or name
            team_id: Team ID or name
            
        Returns:
            Team details
        """
        response_data = await self.client.get_json(f"projects/{project_id}/teams/{team_id}")
        return WebApiTeam(**response_data)
    
    async def create_team(
        self,
        project_id: str,
        team_request: TeamCreateRequest
    ) -> WebApiTeam:
        """
        Create a new team.
        
        Args:
            project_id: Project ID or name
            team_request: Team creation request
            
        Returns:
            Created team details
        """
        response_data = await self.client.post_json(
            f"projects/{project_id}/teams",
            data=team_request.dict_exclude_none()
        )
        return WebApiTeam(**response_data)
    
    async def update_team(
        self,
        project_id: str,
        team_id: str,
        team_update: TeamCreateRequest
    ) -> WebApiTeam:
        """
        Update an existing team.
        
        Args:
            project_id: Project ID or name
            team_id: Team ID or name
            team_update: Team update request
            
        Returns:
            Updated team details
        """
        response_data = await self.client.patch_json(
            f"projects/{project_id}/teams/{team_id}",
            data=team_update.dict_exclude_none()
        )
        return WebApiTeam(**response_data)
    
    async def delete_team(self, project_id: str, team_id: str) -> None:
        """
        Delete a team.
        
        Args:
            project_id: Project ID or name
            team_id: Team ID or name
        """
        await self.client.delete(f"projects/{project_id}/teams/{team_id}")
    
    async def get_team_members(
        self,
        project_id: str,
        team_id: str,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[TeamMember]:
        """
        Get team members.
        
        Args:
            project_id: Project ID or name
            team_id: Team ID or name
            top: Maximum number of members to return
            skip: Number of members to skip
            
        Returns:
            List of team members
        """
        params = {}
        if top:
            params['$top'] = top
        if skip:
            params['$skip'] = skip
        
        response_data = await self.client.get_json(
            f"projects/{project_id}/teams/{team_id}/members",
            params=params
        )
        response = TeamMembersRef(**response_data)
        return [TeamMember(identity=member) for member in response.members]
    
    async def add_team_member(
        self,
        project_id: str,
        team_id: str,
        user_id: str
    ) -> TeamMember:
        """
        Add a member to a team.
        
        Args:
            project_id: Project ID or name
            team_id: Team ID or name
            user_id: User ID to add
            
        Returns:
            Team member details
        """
        response_data = await self.client.put_json(
            f"projects/{project_id}/teams/{team_id}/members/{user_id}"
        )
        return TeamMember(**response_data)
    
    async def remove_team_member(
        self,
        project_id: str,
        team_id: str,
        user_id: str
    ) -> None:
        """
        Remove a member from a team.
        
        Args:
            project_id: Project ID or name
            team_id: Team ID or name
            user_id: User ID to remove
        """
        await self.client.delete(f"projects/{project_id}/teams/{team_id}/members/{user_id}")
    
    # Processes
    async def list_processes(self) -> List[Process]:
        """
        List work item processes.
        
        Returns:
            List of processes
        """
        response_data = await self.client.get_json("process/processes")
        response = ProcessesResponse(**response_data)
        return response.value
    
    async def get_process(self, process_id: str) -> Process:
        """
        Get a specific process.
        
        Args:
            process_id: Process ID
            
        Returns:
            Process details
        """
        response_data = await self.client.get_json(f"process/processes/{process_id}")
        return Process(**response_data)
    
    # Extensions
    async def list_installed_extensions(
        self,
        include_disabled_extensions: Optional[bool] = None,
        include_errors: Optional[bool] = None,
        asset_types: Optional[List[str]] = None,
        include_installation_issues: Optional[bool] = None
    ) -> List[InstalledExtension]:
        """
        List installed extensions.
        
        Args:
            include_disabled_extensions: Include disabled extensions
            include_errors: Include extensions with errors
            asset_types: Asset types to include
            include_installation_issues: Include installation issues
            
        Returns:
            List of installed extensions
        """
        params = {}
        if include_disabled_extensions:
            params['includeDisabledExtensions'] = include_disabled_extensions
        if include_errors:
            params['includeErrors'] = include_errors
        if asset_types:
            params['assetTypes'] = asset_types
        if include_installation_issues:
            params['includeInstallationIssues'] = include_installation_issues
        
        response_data = await self.client.get_json(
            "extensionmanagement/installedextensions",
            params=params
        )
        response = ExtensionsResponse(**response_data)
        return response.value
    
    async def get_installed_extension(
        self,
        publisher_name: str,
        extension_name: str,
        asset_types: Optional[List[str]] = None
    ) -> InstalledExtension:
        """
        Get a specific installed extension.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            asset_types: Asset types to include
            
        Returns:
            Installed extension details
        """
        params = {}
        if asset_types:
            params['assetTypes'] = asset_types
        
        response_data = await self.client.get_json(
            f"extensionmanagement/installedextensions/{publisher_name}/{extension_name}",
            params=params
        )
        return InstalledExtension(**response_data)
    
    async def install_extension_by_name(
        self,
        publisher_name: str,
        extension_name: str,
        version: Optional[str] = None
    ) -> InstalledExtension:
        """
        Install an extension by name.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            version: Specific version to install
            
        Returns:
            Installed extension details
        """
        params = {}
        if version:
            params['version'] = version
        
        response_data = await self.client.post_json(
            f"extensionmanagement/installedextensions/{publisher_name}/{extension_name}",
            params=params
        )
        return InstalledExtension(**response_data)
    
    async def uninstall_extension_by_name(
        self,
        publisher_name: str,
        extension_name: str,
        reason: Optional[str] = None,
        reason_code: Optional[str] = None
    ) -> None:
        """
        Uninstall an extension by name.
        
        Args:
            publisher_name: Publisher name
            extension_name: Extension name
            reason: Reason for uninstalling
            reason_code: Reason code
        """
        params = {}
        if reason:
            params['reason'] = reason
        if reason_code:
            params['reasonCode'] = reason_code
        
        await self.client.delete(
            f"extensionmanagement/installedextensions/{publisher_name}/{extension_name}",
            params=params
        )
    
    # Operations
    async def get_operation(self, operation_id: str) -> OperationReference:
        """
        Get the status of an operation.
        
        Args:
            operation_id: Operation ID
            
        Returns:
            Operation reference with current status
        """
        response_data = await self.client.get_json(f"operations/{operation_id}")
        return OperationReference(**response_data)
    
    # Organization
    async def get_organization_info(self) -> OrganizationInfo:
        """
        Get organization information.
        
        Returns:
            Organization details
        """
        # Note: This endpoint might vary based on organization setup
        response_data = await self.client.get_json("connectionData")
        return OrganizationInfo(**response_data.get('authenticatedUser', {}))
    
    # Utility methods
    async def get_all_projects(self, **kwargs) -> List[TeamProject]:
        """
        Get all projects using pagination.
        
        Returns:
            List of all projects
        """
        paginator = create_paginator(self.list_projects, page_size=100)
        return await paginator.get_all_pages(**kwargs)
    
    async def get_all_teams(self, project_id: Optional[str] = None, **kwargs) -> List[WebApiTeam]:
        """
        Get all teams using pagination.
        
        Args:
            project_id: Project ID to filter teams
            
        Returns:
            List of all teams
        """
        async def request_func(**params):
            teams = await self.list_teams(project_id=project_id, **params)
            return {"value": teams, "count": len(teams)}
        
        paginator = create_paginator(request_func, page_size=100)
        return await paginator.get_all_pages(**kwargs)
