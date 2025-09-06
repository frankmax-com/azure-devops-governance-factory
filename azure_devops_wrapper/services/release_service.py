"""
Release service for Azure DevOps - Release Definitions, Deployments, Environments, etc.
"""

from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from datetime import datetime
from ..core import HTTPClient, create_paginator
from ..models import (
    ReleaseDefinition, Release, ReleaseEnvironment, ReleaseDeployment, ReleaseApproval,
    ReleaseArtifact, ReleaseTask, ReleaseVariable, ReleaseTrigger, ReleaseGate,
    ReleaseDefinitionsResponse, ReleasesResponse, ReleaseEnvironmentsResponse,
    ReleaseDeploymentsResponse, ReleaseApprovalsResponse
)


class ReleaseService:
    """Service for Release Management operations in Azure DevOps."""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    # Release Definitions
    async def list_release_definitions(
        self,
        project: str,
        search_text: Optional[str] = None,
        expand: Optional[str] = None,
        artifact_type: Optional[str] = None,
        artifact_source_id: Optional[str] = None,
        top: Optional[int] = None,
        continuation_token: Optional[str] = None,
        query_order: Optional[str] = None,
        path: Optional[str] = None,
        is_exact_name_match: Optional[bool] = None,
        tag_filter: Optional[List[str]] = None,
        property_filters: Optional[List[str]] = None,
        definition_id_filter: Optional[List[int]] = None,
        is_deleted: Optional[bool] = None,
        search_text_contains_folder_name: Optional[bool] = None
    ) -> List[ReleaseDefinition]:
        """
        List release definitions.
        
        Args:
            project: Project ID or name
            search_text: Search text filter
            expand: Expand options
            artifact_type: Artifact type filter
            artifact_source_id: Artifact source ID filter
            top: Maximum number of definitions
            continuation_token: Continuation token
            query_order: Sort order
            path: Definition path filter
            is_exact_name_match: Exact name match
            tag_filter: Tag filters
            property_filters: Property filters
            definition_id_filter: Definition ID filters
            is_deleted: Include deleted definitions
            search_text_contains_folder_name: Search in folder names
            
        Returns:
            List of release definitions
        """
        params = {}
        if search_text:
            params['searchText'] = search_text
        if expand:
            params['$expand'] = expand
        if artifact_type:
            params['artifactType'] = artifact_type
        if artifact_source_id:
            params['artifactSourceId'] = artifact_source_id
        if top:
            params['$top'] = top
        if continuation_token:
            params['continuationToken'] = continuation_token
        if query_order:
            params['queryOrder'] = query_order
        if path:
            params['path'] = path
        if is_exact_name_match:
            params['isExactNameMatch'] = is_exact_name_match
        if tag_filter:
            params['tagFilter'] = ','.join(tag_filter)
        if property_filters:
            params['propertyFilters'] = ','.join(property_filters)
        if definition_id_filter:
            params['definitionIdFilter'] = ','.join(map(str, definition_id_filter))
        if is_deleted:
            params['isDeleted'] = is_deleted
        if search_text_contains_folder_name:
            params['searchTextContainsFolderName'] = search_text_contains_folder_name
        
        endpoint = f"projects/{project}/release/definitions"
        response_data = await self.client.get_json(endpoint, params=params)
        response = ReleaseDefinitionsResponse(**response_data)
        return response.value
    
    async def get_release_definition(
        self,
        project: str,
        definition_id: int,
        property_filters: Optional[List[str]] = None
    ) -> ReleaseDefinition:
        """
        Get a specific release definition.
        
        Args:
            project: Project ID or name
            definition_id: Definition ID
            property_filters: Property filters
            
        Returns:
            Release definition details
        """
        params = {}
        if property_filters:
            params['propertyFilters'] = ','.join(property_filters)
        
        endpoint = f"projects/{project}/release/definitions/{definition_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return ReleaseDefinition(**response_data)
    
    async def create_release_definition(
        self,
        project: str,
        definition_data: Dict[str, Any]
    ) -> ReleaseDefinition:
        """
        Create a new release definition.
        
        Args:
            project: Project ID or name
            definition_data: Release definition data
            
        Returns:
            Created release definition
        """
        endpoint = f"projects/{project}/release/definitions"
        response_data = await self.client.post_json(endpoint, data=definition_data)
        return ReleaseDefinition(**response_data)
    
    async def update_release_definition(
        self,
        project: str,
        definition_data: Dict[str, Any]
    ) -> ReleaseDefinition:
        """
        Update a release definition.
        
        Args:
            project: Project ID or name
            definition_data: Updated definition data
            
        Returns:
            Updated release definition
        """
        endpoint = f"projects/{project}/release/definitions"
        response_data = await self.client.put_json(endpoint, data=definition_data)
        return ReleaseDefinition(**response_data)
    
    async def delete_release_definition(
        self,
        project: str,
        definition_id: int,
        comment: Optional[str] = None,
        force_delete: Optional[bool] = None
    ) -> None:
        """
        Delete a release definition.
        
        Args:
            project: Project ID or name
            definition_id: Definition ID
            comment: Deletion comment
            force_delete: Force delete
        """
        params = {}
        if comment:
            params['comment'] = comment
        if force_delete:
            params['forceDelete'] = force_delete
        
        endpoint = f"projects/{project}/release/definitions/{definition_id}"
        await self.client.delete(endpoint, params=params)
    
    # Releases
    async def list_releases(
        self,
        project: str,
        definition_id: Optional[int] = None,
        definition_environment_id: Optional[int] = None,
        search_text: Optional[str] = None,
        created_by: Optional[str] = None,
        status_filter: Optional[str] = None,
        environment_status_filter: Optional[int] = None,
        min_created_time: Optional[datetime] = None,
        max_created_time: Optional[datetime] = None,
        query_order: Optional[str] = None,
        top: Optional[int] = None,
        continuation_token: Optional[str] = None,
        expand: Optional[str] = None,
        artifact_type_id: Optional[str] = None,
        source_id: Optional[str] = None,
        artifact_version_id: Optional[str] = None,
        source_branch_filter: Optional[str] = None,
        is_deleted: Optional[bool] = None,
        tag_filter: Optional[List[str]] = None,
        property_filters: Optional[List[str]] = None,
        release_id_filter: Optional[List[int]] = None,
        path: Optional[str] = None
    ) -> List[Release]:
        """
        List releases.
        
        Args:
            project: Project ID or name
            definition_id: Definition ID filter
            definition_environment_id: Environment ID filter
            search_text: Search text
            created_by: Created by filter
            status_filter: Status filter
            environment_status_filter: Environment status filter
            min_created_time: Minimum created time
            max_created_time: Maximum created time
            query_order: Sort order
            top: Maximum number of releases
            continuation_token: Continuation token
            expand: Expand options
            artifact_type_id: Artifact type ID
            source_id: Source ID
            artifact_version_id: Artifact version ID
            source_branch_filter: Source branch filter
            is_deleted: Include deleted releases
            tag_filter: Tag filters
            property_filters: Property filters
            release_id_filter: Release ID filters
            path: Path filter
            
        Returns:
            List of releases
        """
        params = {}
        if definition_id:
            params['definitionId'] = definition_id
        if definition_environment_id:
            params['definitionEnvironmentId'] = definition_environment_id
        if search_text:
            params['searchText'] = search_text
        if created_by:
            params['createdBy'] = created_by
        if status_filter:
            params['statusFilter'] = status_filter
        if environment_status_filter:
            params['environmentStatusFilter'] = environment_status_filter
        if min_created_time:
            params['minCreatedTime'] = min_created_time.isoformat()
        if max_created_time:
            params['maxCreatedTime'] = max_created_time.isoformat()
        if query_order:
            params['queryOrder'] = query_order
        if top:
            params['$top'] = top
        if continuation_token:
            params['continuationToken'] = continuation_token
        if expand:
            params['$expand'] = expand
        if artifact_type_id:
            params['artifactTypeId'] = artifact_type_id
        if source_id:
            params['sourceId'] = source_id
        if artifact_version_id:
            params['artifactVersionId'] = artifact_version_id
        if source_branch_filter:
            params['sourceBranchFilter'] = source_branch_filter
        if is_deleted:
            params['isDeleted'] = is_deleted
        if tag_filter:
            params['tagFilter'] = ','.join(tag_filter)
        if property_filters:
            params['propertyFilters'] = ','.join(property_filters)
        if release_id_filter:
            params['releaseIdFilter'] = ','.join(map(str, release_id_filter))
        if path:
            params['path'] = path
        
        endpoint = f"projects/{project}/release/releases"
        response_data = await self.client.get_json(endpoint, params=params)
        response = ReleasesResponse(**response_data)
        return response.value
    
    async def get_release(
        self,
        project: str,
        release_id: int,
        approval_filters: Optional[str] = None,
        property_filters: Optional[List[str]] = None,
        expand: Optional[str] = None,
        top_gate_records: Optional[int] = None,
        single_release_expands: Optional[str] = None
    ) -> Release:
        """
        Get a specific release.
        
        Args:
            project: Project ID or name
            release_id: Release ID
            approval_filters: Approval filters
            property_filters: Property filters
            expand: Expand options
            top_gate_records: Top gate records
            single_release_expands: Single release expand options
            
        Returns:
            Release details
        """
        params = {}
        if approval_filters:
            params['approvalFilters'] = approval_filters
        if property_filters:
            params['propertyFilters'] = ','.join(property_filters)
        if expand:
            params['$expand'] = expand
        if top_gate_records:
            params['$topGateRecords'] = top_gate_records
        if single_release_expands:
            params['singleReleaseExpands'] = single_release_expands
        
        endpoint = f"projects/{project}/release/releases/{release_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return Release(**response_data)
    
    async def create_release(
        self,
        project: str,
        release_data: Dict[str, Any]
    ) -> Release:
        """
        Create a new release.
        
        Args:
            project: Project ID or name
            release_data: Release creation data
            
        Returns:
            Created release
        """
        endpoint = f"projects/{project}/release/releases"
        response_data = await self.client.post_json(endpoint, data=release_data)
        return Release(**response_data)
    
    async def update_release(
        self,
        project: str,
        release_id: int,
        release_data: Dict[str, Any]
    ) -> Release:
        """
        Update a release.
        
        Args:
            project: Project ID or name
            release_id: Release ID
            release_data: Release update data
            
        Returns:
            Updated release
        """
        endpoint = f"projects/{project}/release/releases/{release_id}"
        response_data = await self.client.put_json(endpoint, data=release_data)
        return Release(**response_data)
    
    async def abandon_release(
        self,
        project: str,
        release_id: int,
        comment: Optional[str] = None
    ) -> Release:
        """
        Abandon a release.
        
        Args:
            project: Project ID or name
            release_id: Release ID
            comment: Abandon comment
            
        Returns:
            Abandoned release
        """
        abandon_data = {"status": "abandoned"}
        if comment:
            abandon_data["comment"] = comment
        
        return await self.update_release(
            project=project,
            release_id=release_id,
            release_data=abandon_data
        )
    
    # Release Environments
    async def update_release_environment(
        self,
        project: str,
        release_id: int,
        environment_id: int,
        environment_data: Dict[str, Any]
    ) -> ReleaseEnvironment:
        """
        Update a release environment.
        
        Args:
            project: Project ID or name
            release_id: Release ID
            environment_id: Environment ID
            environment_data: Environment update data
            
        Returns:
            Updated release environment
        """
        endpoint = f"projects/{project}/release/releases/{release_id}/environments/{environment_id}"
        response_data = await self.client.patch_json(endpoint, data=environment_data)
        return ReleaseEnvironment(**response_data)
    
    async def deploy_to_environment(
        self,
        project: str,
        release_id: int,
        environment_id: int,
        comment: Optional[str] = None
    ) -> ReleaseEnvironment:
        """
        Deploy a release to an environment.
        
        Args:
            project: Project ID or name
            release_id: Release ID
            environment_id: Environment ID
            comment: Deployment comment
            
        Returns:
            Updated release environment
        """
        deploy_data = {"status": "inProgress"}
        if comment:
            deploy_data["comment"] = comment
        
        return await self.update_release_environment(
            project=project,
            release_id=release_id,
            environment_id=environment_id,
            environment_data=deploy_data
        )
    
    async def cancel_environment_deployment(
        self,
        project: str,
        release_id: int,
        environment_id: int,
        comment: Optional[str] = None
    ) -> ReleaseEnvironment:
        """
        Cancel an environment deployment.
        
        Args:
            project: Project ID or name
            release_id: Release ID
            environment_id: Environment ID
            comment: Cancellation comment
            
        Returns:
            Updated release environment
        """
        cancel_data = {"status": "canceled"}
        if comment:
            cancel_data["comment"] = comment
        
        return await self.update_release_environment(
            project=project,
            release_id=release_id,
            environment_id=environment_id,
            environment_data=cancel_data
        )
    
    # Release Deployments
    async def get_deployments(
        self,
        project: str,
        definition_id: Optional[int] = None,
        definition_environment_id: Optional[int] = None,
        created_by: Optional[str] = None,
        min_modified_time: Optional[datetime] = None,
        max_modified_time: Optional[datetime] = None,
        deployment_status: Optional[str] = None,
        operation_status: Optional[str] = None,
        latest_attempts_only: Optional[bool] = None,
        query_order: Optional[str] = None,
        top: Optional[int] = None,
        continuation_token: Optional[str] = None,
        created_for: Optional[str] = None,
        min_started_time: Optional[datetime] = None,
        max_started_time: Optional[datetime] = None,
        source_branch: Optional[str] = None
    ) -> List[ReleaseDeployment]:
        """
        Get deployments.
        
        Args:
            project: Project ID or name
            definition_id: Definition ID filter
            definition_environment_id: Environment ID filter
            created_by: Created by filter
            min_modified_time: Minimum modified time
            max_modified_time: Maximum modified time
            deployment_status: Deployment status filter
            operation_status: Operation status filter
            latest_attempts_only: Latest attempts only
            query_order: Sort order
            top: Maximum number of deployments
            continuation_token: Continuation token
            created_for: Created for filter
            min_started_time: Minimum started time
            max_started_time: Maximum started time
            source_branch: Source branch filter
            
        Returns:
            List of deployments
        """
        params = {}
        if definition_id:
            params['definitionId'] = definition_id
        if definition_environment_id:
            params['definitionEnvironmentId'] = definition_environment_id
        if created_by:
            params['createdBy'] = created_by
        if min_modified_time:
            params['minModifiedTime'] = min_modified_time.isoformat()
        if max_modified_time:
            params['maxModifiedTime'] = max_modified_time.isoformat()
        if deployment_status:
            params['deploymentStatus'] = deployment_status
        if operation_status:
            params['operationStatus'] = operation_status
        if latest_attempts_only:
            params['latestAttemptsOnly'] = latest_attempts_only
        if query_order:
            params['queryOrder'] = query_order
        if top:
            params['$top'] = top
        if continuation_token:
            params['continuationToken'] = continuation_token
        if created_for:
            params['createdFor'] = created_for
        if min_started_time:
            params['minStartedTime'] = min_started_time.isoformat()
        if max_started_time:
            params['maxStartedTime'] = max_started_time.isoformat()
        if source_branch:
            params['sourceBranch'] = source_branch
        
        endpoint = f"projects/{project}/release/deployments"
        response_data = await self.client.get_json(endpoint, params=params)
        response = ReleaseDeploymentsResponse(**response_data)
        return response.value
    
    # Release Approvals
    async def list_release_approvals(
        self,
        project: str,
        assigned_to_filter: Optional[str] = None,
        status_filter: Optional[str] = None,
        release_ids_filter: Optional[List[int]] = None,
        type_filter: Optional[str] = None,
        top: Optional[int] = None,
        continuation_token: Optional[str] = None,
        query_order: Optional[str] = None,
        include_my_group_approvals: Optional[bool] = None
    ) -> List[ReleaseApproval]:
        """
        List release approvals.
        
        Args:
            project: Project ID or name
            assigned_to_filter: Assigned to filter
            status_filter: Status filter
            release_ids_filter: Release IDs filter
            type_filter: Type filter
            top: Maximum number of approvals
            continuation_token: Continuation token
            query_order: Sort order
            include_my_group_approvals: Include group approvals
            
        Returns:
            List of release approvals
        """
        params = {}
        if assigned_to_filter:
            params['assignedToFilter'] = assigned_to_filter
        if status_filter:
            params['statusFilter'] = status_filter
        if release_ids_filter:
            params['releaseIdsFilter'] = ','.join(map(str, release_ids_filter))
        if type_filter:
            params['typeFilter'] = type_filter
        if top:
            params['$top'] = top
        if continuation_token:
            params['continuationToken'] = continuation_token
        if query_order:
            params['queryOrder'] = query_order
        if include_my_group_approvals:
            params['includeMyGroupApprovals'] = include_my_group_approvals
        
        endpoint = f"projects/{project}/release/approvals"
        response_data = await self.client.get_json(endpoint, params=params)
        response = ReleaseApprovalsResponse(**response_data)
        return response.value
    
    async def get_release_approval(
        self,
        project: str,
        approval_id: int,
        include_history: Optional[bool] = None
    ) -> ReleaseApproval:
        """
        Get a specific release approval.
        
        Args:
            project: Project ID or name
            approval_id: Approval ID
            include_history: Include approval history
            
        Returns:
            Release approval details
        """
        params = {}
        if include_history:
            params['includeHistory'] = include_history
        
        endpoint = f"projects/{project}/release/approvals/{approval_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return ReleaseApproval(**response_data)
    
    async def update_release_approval(
        self,
        project: str,
        approval_id: int,
        approval_data: Dict[str, Any]
    ) -> ReleaseApproval:
        """
        Update a release approval.
        
        Args:
            project: Project ID or name
            approval_id: Approval ID
            approval_data: Approval update data
            
        Returns:
            Updated release approval
        """
        endpoint = f"projects/{project}/release/approvals/{approval_id}"
        response_data = await self.client.patch_json(endpoint, data=approval_data)
        return ReleaseApproval(**response_data)
    
    async def approve_release(
        self,
        project: str,
        approval_id: int,
        comment: Optional[str] = None
    ) -> ReleaseApproval:
        """
        Approve a release approval.
        
        Args:
            project: Project ID or name
            approval_id: Approval ID
            comment: Approval comment
            
        Returns:
            Approved release approval
        """
        approval_data = {"status": "approved"}
        if comment:
            approval_data["comments"] = comment
        
        return await self.update_release_approval(
            project=project,
            approval_id=approval_id,
            approval_data=approval_data
        )
    
    async def reject_release(
        self,
        project: str,
        approval_id: int,
        comment: Optional[str] = None
    ) -> ReleaseApproval:
        """
        Reject a release approval.
        
        Args:
            project: Project ID or name
            approval_id: Approval ID
            comment: Rejection comment
            
        Returns:
            Rejected release approval
        """
        approval_data = {"status": "rejected"}
        if comment:
            approval_data["comments"] = comment
        
        return await self.update_release_approval(
            project=project,
            approval_id=approval_id,
            approval_data=approval_data
        )
    
    # Utility methods
    async def get_latest_release(
        self,
        project: str,
        definition_id: int,
        status_filter: Optional[str] = None
    ) -> Optional[Release]:
        """
        Get the latest release for a definition.
        
        Args:
            project: Project ID or name
            definition_id: Definition ID
            status_filter: Status filter
            
        Returns:
            Latest release or None
        """
        releases = await self.list_releases(
            project=project,
            definition_id=definition_id,
            status_filter=status_filter,
            top=1,
            query_order="descending"
        )
        return releases[0] if releases else None
    
    async def wait_for_deployment_completion(
        self,
        project: str,
        release_id: int,
        environment_id: int,
        timeout_seconds: int = 3600,
        poll_interval: int = 30
    ) -> ReleaseEnvironment:
        """
        Wait for a deployment to complete.
        
        Args:
            project: Project ID or name
            release_id: Release ID
            environment_id: Environment ID
            timeout_seconds: Maximum wait time
            poll_interval: Polling interval in seconds
            
        Returns:
            Completed release environment
            
        Raises:
            TimeoutError: If deployment doesn't complete within timeout
        """
        import asyncio
        
        start_time = datetime.now()
        
        while True:
            release = await self.get_release(project=project, release_id=release_id)
            
            # Find the environment
            environment = None
            for env in release.environments or []:
                if env.id == environment_id:
                    environment = env
                    break
            
            if environment and environment.status in ["succeeded", "failed", "canceled", "rejected"]:
                return environment
            
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed >= timeout_seconds:
                raise TimeoutError(f"Deployment to environment {environment_id} did not complete within {timeout_seconds} seconds")
            
            await asyncio.sleep(poll_interval)
    
    async def get_release_summary(
        self,
        project: str,
        release_id: int
    ) -> Dict[str, Any]:
        """
        Get a comprehensive summary of a release.
        
        Args:
            project: Project ID or name
            release_id: Release ID
            
        Returns:
            Release summary with environments and deployments
        """
        # Get the release details
        release = await self.get_release(
            project=project,
            release_id=release_id,
            expand="environments,artifacts,variables"
        )
        
        # Get deployments for this release
        try:
            deployments = await self.get_deployments(
                project=project,
                definition_id=release.release_definition.id if release.release_definition else None
            )
            # Filter deployments for this specific release
            release_deployments = [d for d in deployments if d.release and d.release.id == release_id]
        except Exception:
            release_deployments = []
        
        # Get pending approvals for this release
        try:
            approvals = await self.list_release_approvals(
                project=project,
                release_ids_filter=[release_id],
                status_filter="pending"
            )
        except Exception:
            approvals = []
        
        return {
            "release": release,
            "deployments": release_deployments,
            "pending_approvals": approvals,
            "summary": {
                "release_id": release_id,
                "release_name": release.name,
                "status": release.status,
                "created_date": release.created_on,
                "environment_count": len(release.environments or []),
                "deployment_count": len(release_deployments),
                "pending_approval_count": len(approvals),
                "artifact_count": len(release.artifacts or [])
            }
        }
    
    async def iterate_releases(
        self,
        project: str,
        definition_id: Optional[int] = None,
        page_size: int = 100,
        **kwargs
    ) -> AsyncGenerator[Release, None]:
        """
        Iterate through all releases.
        
        Args:
            project: Project ID or name
            definition_id: Definition ID filter
            page_size: Number of releases per page
            
        Yields:
            Releases one by one
        """
        async def request_func(**params):
            releases = await self.list_releases(
                project=project,
                definition_id=definition_id,
                top=page_size,
                **params,
                **kwargs
            )
            return {"value": releases, "count": len(releases)}
        
        paginator = create_paginator(request_func, page_size=page_size)
        async for release in paginator.iterate_items():
            yield release
