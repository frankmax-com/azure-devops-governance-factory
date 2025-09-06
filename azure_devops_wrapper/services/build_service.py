"""
Build service for Azure DevOps - Build Definitions, Build Runs, Artifacts, etc.
"""

from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from datetime import datetime
from ..core import HTTPClient, create_paginator
from ..models import (
    Build, BuildDefinition, BuildArtifact, BuildLog, BuildTimeline,
    BuildReport, BuildController, BuildQueue, BuildDefinitionTemplate,
    BuildsResponse, BuildDefinitionsResponse, BuildArtifactsResponse,
    BuildLogsResponse, BuildTimelineResponse, BuildDefinitionRevision
)


class BuildService:
    """Service for Build operations in Azure DevOps."""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    # Build Definitions
    async def list_build_definitions(
        self,
        project: str,
        name: Optional[str] = None,
        repository_id: Optional[str] = None,
        repository_type: Optional[str] = None,
        query_order: Optional[str] = None,
        top: Optional[int] = None,
        continuation_token: Optional[str] = None,
        min_metrics_time: Optional[datetime] = None,
        definition_ids: Optional[List[int]] = None,
        path: Optional[str] = None,
        built_after: Optional[datetime] = None,
        not_built_after: Optional[datetime] = None,
        include_all_properties: Optional[bool] = None,
        include_latest_builds: Optional[bool] = None,
        task_id_filter: Optional[str] = None,
        process_type: Optional[int] = None,
        yaml_filename: Optional[str] = None
    ) -> List[BuildDefinition]:
        """
        List build definitions.
        
        Args:
            project: Project ID or name
            name: Definition name filter
            repository_id: Repository ID filter
            repository_type: Repository type filter
            query_order: Sort order
            top: Maximum number of definitions
            continuation_token: Continuation token for pagination
            min_metrics_time: Minimum metrics time
            definition_ids: Specific definition IDs
            path: Definition path filter
            built_after: Built after date
            not_built_after: Not built after date
            include_all_properties: Include all properties
            include_latest_builds: Include latest builds
            task_id_filter: Task ID filter
            process_type: Process type filter
            yaml_filename: YAML filename filter
            
        Returns:
            List of build definitions
        """
        params = {}
        if name:
            params['name'] = name
        if repository_id:
            params['repositoryId'] = repository_id
        if repository_type:
            params['repositoryType'] = repository_type
        if query_order:
            params['queryOrder'] = query_order
        if top:
            params['$top'] = top
        if continuation_token:
            params['continuationToken'] = continuation_token
        if min_metrics_time:
            params['minMetricsTime'] = min_metrics_time.isoformat()
        if definition_ids:
            params['definitionIds'] = ','.join(map(str, definition_ids))
        if path:
            params['path'] = path
        if built_after:
            params['builtAfter'] = built_after.isoformat()
        if not_built_after:
            params['notBuiltAfter'] = not_built_after.isoformat()
        if include_all_properties:
            params['includeAllProperties'] = include_all_properties
        if include_latest_builds:
            params['includeLatestBuilds'] = include_latest_builds
        if task_id_filter:
            params['taskIdFilter'] = task_id_filter
        if process_type:
            params['processType'] = process_type
        if yaml_filename:
            params['yamlFilename'] = yaml_filename
        
        endpoint = f"projects/{project}/build/definitions"
        response_data = await self.client.get_json(endpoint, params=params)
        response = BuildDefinitionsResponse(**response_data)
        return response.value
    
    async def get_build_definition(
        self,
        project: str,
        definition_id: int,
        revision: Optional[int] = None,
        min_metrics_time: Optional[datetime] = None,
        property_filters: Optional[List[str]] = None,
        include_latest_builds: Optional[bool] = None
    ) -> BuildDefinition:
        """
        Get a specific build definition.
        
        Args:
            project: Project ID or name
            definition_id: Definition ID
            revision: Specific revision
            min_metrics_time: Minimum metrics time
            property_filters: Property filters
            include_latest_builds: Include latest builds
            
        Returns:
            Build definition details
        """
        params = {}
        if revision:
            params['revision'] = revision
        if min_metrics_time:
            params['minMetricsTime'] = min_metrics_time.isoformat()
        if property_filters:
            params['propertyFilters'] = ','.join(property_filters)
        if include_latest_builds:
            params['includeLatestBuilds'] = include_latest_builds
        
        endpoint = f"projects/{project}/build/definitions/{definition_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return BuildDefinition(**response_data)
    
    async def create_build_definition(
        self,
        project: str,
        definition: Dict[str, Any],
        definition_to_clone_id: Optional[int] = None,
        definition_to_clone_revision: Optional[int] = None
    ) -> BuildDefinition:
        """
        Create a new build definition.
        
        Args:
            project: Project ID or name
            definition: Build definition data
            definition_to_clone_id: Definition ID to clone from
            definition_to_clone_revision: Revision to clone from
            
        Returns:
            Created build definition
        """
        params = {}
        if definition_to_clone_id:
            params['definitionToCloneId'] = definition_to_clone_id
        if definition_to_clone_revision:
            params['definitionToCloneRevision'] = definition_to_clone_revision
        
        endpoint = f"projects/{project}/build/definitions"
        response_data = await self.client.post_json(endpoint, data=definition, params=params)
        return BuildDefinition(**response_data)
    
    async def update_build_definition(
        self,
        project: str,
        definition_id: int,
        definition: Dict[str, Any],
        secrets_source_definition_id: Optional[int] = None,
        secrets_source_definition_revision: Optional[int] = None
    ) -> BuildDefinition:
        """
        Update a build definition.
        
        Args:
            project: Project ID or name
            definition_id: Definition ID
            definition: Updated definition data
            secrets_source_definition_id: Secrets source definition ID
            secrets_source_definition_revision: Secrets source revision
            
        Returns:
            Updated build definition
        """
        params = {}
        if secrets_source_definition_id:
            params['secretsSourceDefinitionId'] = secrets_source_definition_id
        if secrets_source_definition_revision:
            params['secretsSourceDefinitionRevision'] = secrets_source_definition_revision
        
        endpoint = f"projects/{project}/build/definitions/{definition_id}"
        response_data = await self.client.put_json(endpoint, data=definition, params=params)
        return BuildDefinition(**response_data)
    
    async def delete_build_definition(
        self,
        project: str,
        definition_id: int
    ) -> None:
        """
        Delete a build definition.
        
        Args:
            project: Project ID or name
            definition_id: Definition ID
        """
        endpoint = f"projects/{project}/build/definitions/{definition_id}"
        await self.client.delete(endpoint)
    
    # Build Definition Revisions
    async def get_build_definition_revisions(
        self,
        project: str,
        definition_id: int
    ) -> List[BuildDefinitionRevision]:
        """
        Get build definition revisions.
        
        Args:
            project: Project ID or name
            definition_id: Definition ID
            
        Returns:
            List of definition revisions
        """
        endpoint = f"projects/{project}/build/definitions/{definition_id}/revisions"
        response_data = await self.client.get_json(endpoint)
        revisions = response_data.get('value', [])
        return [BuildDefinitionRevision(**revision) for revision in revisions]
    
    # Builds
    async def list_builds(
        self,
        project: str,
        definitions: Optional[List[int]] = None,
        queues: Optional[List[int]] = None,
        build_number: Optional[str] = None,
        min_time: Optional[datetime] = None,
        max_time: Optional[datetime] = None,
        requested_for: Optional[str] = None,
        reason_filter: Optional[str] = None,
        status_filter: Optional[str] = None,
        result_filter: Optional[str] = None,
        tag_filters: Optional[List[str]] = None,
        properties: Optional[List[str]] = None,
        top: Optional[int] = None,
        continuation_token: Optional[str] = None,
        max_builds_per_definition: Optional[int] = None,
        deleted_filter: Optional[str] = None,
        query_order: Optional[str] = None,
        branch_name: Optional[str] = None,
        build_ids: Optional[List[int]] = None,
        repository_id: Optional[str] = None,
        repository_type: Optional[str] = None
    ) -> List[Build]:
        """
        List builds.
        
        Args:
            project: Project ID or name
            definitions: Definition IDs filter
            queues: Queue IDs filter
            build_number: Build number filter
            min_time: Minimum finish time
            max_time: Maximum finish time
            requested_for: Requested for user filter
            reason_filter: Build reason filter
            status_filter: Build status filter
            result_filter: Build result filter
            tag_filters: Tag filters
            properties: Properties to include
            top: Maximum number of builds
            continuation_token: Continuation token
            max_builds_per_definition: Max builds per definition
            deleted_filter: Deleted filter
            query_order: Sort order
            branch_name: Branch name filter
            build_ids: Specific build IDs
            repository_id: Repository ID filter
            repository_type: Repository type filter
            
        Returns:
            List of builds
        """
        params = {}
        if definitions:
            params['definitions'] = ','.join(map(str, definitions))
        if queues:
            params['queues'] = ','.join(map(str, queues))
        if build_number:
            params['buildNumber'] = build_number
        if min_time:
            params['minTime'] = min_time.isoformat()
        if max_time:
            params['maxTime'] = max_time.isoformat()
        if requested_for:
            params['requestedFor'] = requested_for
        if reason_filter:
            params['reasonFilter'] = reason_filter
        if status_filter:
            params['statusFilter'] = status_filter
        if result_filter:
            params['resultFilter'] = result_filter
        if tag_filters:
            params['tagFilters'] = ','.join(tag_filters)
        if properties:
            params['properties'] = ','.join(properties)
        if top:
            params['$top'] = top
        if continuation_token:
            params['continuationToken'] = continuation_token
        if max_builds_per_definition:
            params['maxBuildsPerDefinition'] = max_builds_per_definition
        if deleted_filter:
            params['deletedFilter'] = deleted_filter
        if query_order:
            params['queryOrder'] = query_order
        if branch_name:
            params['branchName'] = branch_name
        if build_ids:
            params['buildIds'] = ','.join(map(str, build_ids))
        if repository_id:
            params['repositoryId'] = repository_id
        if repository_type:
            params['repositoryType'] = repository_type
        
        endpoint = f"projects/{project}/build/builds"
        response_data = await self.client.get_json(endpoint, params=params)
        response = BuildsResponse(**response_data)
        return response.value
    
    async def get_build(
        self,
        project: str,
        build_id: int,
        property_filters: Optional[str] = None
    ) -> Build:
        """
        Get a specific build.
        
        Args:
            project: Project ID or name
            build_id: Build ID
            property_filters: Property filters
            
        Returns:
            Build details
        """
        params = {}
        if property_filters:
            params['propertyFilters'] = property_filters
        
        endpoint = f"projects/{project}/build/builds/{build_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return Build(**response_data)
    
    async def queue_build(
        self,
        project: str,
        build_request: Dict[str, Any],
        ignore_warnings: Optional[bool] = None,
        check_in_ticket: Optional[str] = None
    ) -> Build:
        """
        Queue a new build.
        
        Args:
            project: Project ID or name
            build_request: Build request data
            ignore_warnings: Ignore warnings
            check_in_ticket: Check-in ticket
            
        Returns:
            Queued build
        """
        params = {}
        if ignore_warnings:
            params['ignoreWarnings'] = ignore_warnings
        if check_in_ticket:
            params['checkInTicket'] = check_in_ticket
        
        endpoint = f"projects/{project}/build/builds"
        response_data = await self.client.post_json(endpoint, data=build_request, params=params)
        return Build(**response_data)
    
    async def update_build(
        self,
        project: str,
        build_id: int,
        build_update: Dict[str, Any],
        retry: Optional[bool] = None
    ) -> Build:
        """
        Update a build.
        
        Args:
            project: Project ID or name
            build_id: Build ID
            build_update: Build update data
            retry: Retry build
            
        Returns:
            Updated build
        """
        params = {}
        if retry:
            params['retry'] = retry
        
        endpoint = f"projects/{project}/build/builds/{build_id}"
        response_data = await self.client.patch_json(endpoint, data=build_update, params=params)
        return Build(**response_data)
    
    async def delete_build(
        self,
        project: str,
        build_id: int
    ) -> None:
        """
        Delete a build.
        
        Args:
            project: Project ID or name
            build_id: Build ID
        """
        endpoint = f"projects/{project}/build/builds/{build_id}"
        await self.client.delete(endpoint)
    
    async def cancel_build(
        self,
        project: str,
        build_id: int
    ) -> Build:
        """
        Cancel a running build.
        
        Args:
            project: Project ID or name
            build_id: Build ID
            
        Returns:
            Cancelled build
        """
        return await self.update_build(
            project=project,
            build_id=build_id,
            build_update={"status": "cancelling"}
        )
    
    async def retry_build(
        self,
        project: str,
        build_id: int
    ) -> Build:
        """
        Retry a build.
        
        Args:
            project: Project ID or name
            build_id: Build ID
            
        Returns:
            Retried build
        """
        return await self.update_build(
            project=project,
            build_id=build_id,
            build_update={},
            retry=True
        )
    
    # Build Artifacts
    async def get_build_artifacts(
        self,
        project: str,
        build_id: int
    ) -> List[BuildArtifact]:
        """
        Get build artifacts.
        
        Args:
            project: Project ID or name
            build_id: Build ID
            
        Returns:
            List of build artifacts
        """
        endpoint = f"projects/{project}/build/builds/{build_id}/artifacts"
        response_data = await self.client.get_json(endpoint)
        response = BuildArtifactsResponse(**response_data)
        return response.value
    
    async def get_build_artifact(
        self,
        project: str,
        build_id: int,
        artifact_name: str
    ) -> BuildArtifact:
        """
        Get a specific build artifact.
        
        Args:
            project: Project ID or name
            build_id: Build ID
            artifact_name: Artifact name
            
        Returns:
            Build artifact details
        """
        endpoint = f"projects/{project}/build/builds/{build_id}/artifacts"
        params = {"artifactName": artifact_name}
        response_data = await self.client.get_json(endpoint, params=params)
        return BuildArtifact(**response_data)
    
    # Build Logs
    async def get_build_logs(
        self,
        project: str,
        build_id: int
    ) -> List[BuildLog]:
        """
        Get build logs.
        
        Args:
            project: Project ID or name
            build_id: Build ID
            
        Returns:
            List of build logs
        """
        endpoint = f"projects/{project}/build/builds/{build_id}/logs"
        response_data = await self.client.get_json(endpoint)
        response = BuildLogsResponse(**response_data)
        return response.value
    
    async def get_build_log(
        self,
        project: str,
        build_id: int,
        log_id: int,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None
    ) -> str:
        """
        Get a specific build log.
        
        Args:
            project: Project ID or name
            build_id: Build ID
            log_id: Log ID
            start_line: Start line number
            end_line: End line number
            
        Returns:
            Log content as text
        """
        params = {}
        if start_line:
            params['startLine'] = start_line
        if end_line:
            params['endLine'] = end_line
        
        endpoint = f"projects/{project}/build/builds/{build_id}/logs/{log_id}"
        return await self.client.get_text(endpoint, params=params)
    
    # Build Timeline
    async def get_build_timeline(
        self,
        project: str,
        build_id: int,
        timeline_id: Optional[str] = None,
        change_id: Optional[int] = None,
        plan_id: Optional[str] = None
    ) -> BuildTimeline:
        """
        Get build timeline.
        
        Args:
            project: Project ID or name
            build_id: Build ID
            timeline_id: Timeline ID
            change_id: Change ID
            plan_id: Plan ID
            
        Returns:
            Build timeline
        """
        params = {}
        if timeline_id:
            params['timelineId'] = timeline_id
        if change_id:
            params['changeId'] = change_id
        if plan_id:
            params['planId'] = plan_id
        
        endpoint = f"projects/{project}/build/builds/{build_id}/timeline"
        response_data = await self.client.get_json(endpoint, params=params)
        return BuildTimeline(**response_data)
    
    # Build Tags
    async def get_build_tags(
        self,
        project: str,
        build_id: int
    ) -> List[str]:
        """
        Get build tags.
        
        Args:
            project: Project ID or name
            build_id: Build ID
            
        Returns:
            List of build tags
        """
        endpoint = f"projects/{project}/build/builds/{build_id}/tags"
        response_data = await self.client.get_json(endpoint)
        return response_data.get('value', [])
    
    async def add_build_tag(
        self,
        project: str,
        build_id: int,
        tag: str
    ) -> List[str]:
        """
        Add a tag to a build.
        
        Args:
            project: Project ID or name
            build_id: Build ID
            tag: Tag to add
            
        Returns:
            Updated list of build tags
        """
        endpoint = f"projects/{project}/build/builds/{build_id}/tags/{tag}"
        response_data = await self.client.put_json(endpoint, data={})
        return response_data.get('value', [])
    
    async def remove_build_tag(
        self,
        project: str,
        build_id: int,
        tag: str
    ) -> List[str]:
        """
        Remove a tag from a build.
        
        Args:
            project: Project ID or name
            build_id: Build ID
            tag: Tag to remove
            
        Returns:
            Updated list of build tags
        """
        endpoint = f"projects/{project}/build/builds/{build_id}/tags/{tag}"
        response_data = await self.client.delete_json(endpoint)
        return response_data.get('value', [])
    
    # Build Controllers and Queues
    async def get_build_controllers(
        self,
        name: Optional[str] = None
    ) -> List[BuildController]:
        """
        Get build controllers.
        
        Args:
            name: Controller name filter
            
        Returns:
            List of build controllers
        """
        params = {}
        if name:
            params['name'] = name
        
        endpoint = "build/controllers"
        response_data = await self.client.get_json(endpoint, params=params)
        controllers = response_data.get('value', [])
        return [BuildController(**controller) for controller in controllers]
    
    async def get_build_queues(
        self,
        project: Optional[str] = None,
        name: Optional[str] = None,
        action_filter: Optional[str] = None
    ) -> List[BuildQueue]:
        """
        Get build queues.
        
        Args:
            project: Project ID or name
            name: Queue name filter
            action_filter: Action filter
            
        Returns:
            List of build queues
        """
        params = {}
        if name:
            params['name'] = name
        if action_filter:
            params['actionFilter'] = action_filter
        
        endpoint = "build/queues"
        if project:
            endpoint = f"projects/{project}/build/queues"
        
        response_data = await self.client.get_json(endpoint, params=params)
        queues = response_data.get('value', [])
        return [BuildQueue(**queue) for queue in queues]
    
    # Utility methods
    async def get_latest_build(
        self,
        project: str,
        definition_id: int,
        branch_name: Optional[str] = None
    ) -> Optional[Build]:
        """
        Get the latest build for a definition.
        
        Args:
            project: Project ID or name
            definition_id: Definition ID
            branch_name: Branch name filter
            
        Returns:
            Latest build or None
        """
        builds = await self.list_builds(
            project=project,
            definitions=[definition_id],
            branch_name=branch_name,
            top=1,
            query_order="finishTimeDescending"
        )
        return builds[0] if builds else None
    
    async def wait_for_build_completion(
        self,
        project: str,
        build_id: int,
        timeout_seconds: int = 3600,
        poll_interval: int = 30
    ) -> Build:
        """
        Wait for a build to complete.
        
        Args:
            project: Project ID or name
            build_id: Build ID
            timeout_seconds: Maximum wait time
            poll_interval: Polling interval in seconds
            
        Returns:
            Completed build
            
        Raises:
            TimeoutError: If build doesn't complete within timeout
        """
        import asyncio
        
        start_time = datetime.now()
        
        while True:
            build = await self.get_build(project=project, build_id=build_id)
            
            if build.status in ["completed", "cancelled"]:
                return build
            
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed >= timeout_seconds:
                raise TimeoutError(f"Build {build_id} did not complete within {timeout_seconds} seconds")
            
            await asyncio.sleep(poll_interval)
    
    async def iterate_builds(
        self,
        project: str,
        page_size: int = 100,
        **kwargs
    ) -> AsyncGenerator[Build, None]:
        """
        Iterate through all builds.
        
        Args:
            project: Project ID or name
            page_size: Number of builds per page
            
        Yields:
            Builds one by one
        """
        async def request_func(**params):
            builds = await self.list_builds(
                project=project,
                top=page_size,
                **params,
                **kwargs
            )
            return {"value": builds, "count": len(builds)}
        
        paginator = create_paginator(request_func, page_size=page_size)
        async for build in paginator.iterate_items():
            yield build
