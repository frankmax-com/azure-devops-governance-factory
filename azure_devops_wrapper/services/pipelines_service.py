"""
Pipelines service for Azure DevOps - YAML Pipelines, Runs, Approvals, etc.
"""

from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from datetime import datetime
from ..core import HTTPClient, create_paginator
from ..models import (
    Pipeline, PipelineRun, PipelineApproval, PipelineEnvironment, PipelineStage,
    PipelineJob, PipelineTask, PipelineVariable, PipelineTemplate, PipelineArtifact,
    PipelinesResponse, PipelineRunsResponse, PipelineApprovalsResponse,
    PipelineEnvironmentsResponse, PipelineLog, PipelinePreview
)


class PipelinesService:
    """Service for Pipelines operations in Azure DevOps."""
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    # Pipelines
    async def list_pipelines(
        self,
        project: str,
        order_by: Optional[str] = None,
        top: Optional[int] = None,
        continuation_token: Optional[str] = None
    ) -> List[Pipeline]:
        """
        List pipelines in a project.
        
        Args:
            project: Project ID or name
            order_by: Order by field
            top: Maximum number of pipelines
            continuation_token: Continuation token for pagination
            
        Returns:
            List of pipelines
        """
        params = {}
        if order_by:
            params['orderBy'] = order_by
        if top:
            params['$top'] = top
        if continuation_token:
            params['continuationToken'] = continuation_token
        
        endpoint = f"projects/{project}/pipelines"
        response_data = await self.client.get_json(endpoint, params=params)
        response = PipelinesResponse(**response_data)
        return response.value
    
    async def get_pipeline(
        self,
        project: str,
        pipeline_id: int,
        pipeline_version: Optional[int] = None
    ) -> Pipeline:
        """
        Get a specific pipeline.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
            pipeline_version: Pipeline version
            
        Returns:
            Pipeline details
        """
        params = {}
        if pipeline_version:
            params['pipelineVersion'] = pipeline_version
        
        endpoint = f"projects/{project}/pipelines/{pipeline_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return Pipeline(**response_data)
    
    async def create_pipeline(
        self,
        project: str,
        pipeline_data: Dict[str, Any]
    ) -> Pipeline:
        """
        Create a new pipeline.
        
        Args:
            project: Project ID or name
            pipeline_data: Pipeline creation data
            
        Returns:
            Created pipeline
        """
        endpoint = f"projects/{project}/pipelines"
        response_data = await self.client.post_json(endpoint, data=pipeline_data)
        return Pipeline(**response_data)
    
    async def update_pipeline(
        self,
        project: str,
        pipeline_id: int,
        pipeline_data: Dict[str, Any]
    ) -> Pipeline:
        """
        Update a pipeline.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
            pipeline_data: Pipeline update data
            
        Returns:
            Updated pipeline
        """
        endpoint = f"projects/{project}/pipelines/{pipeline_id}"
        response_data = await self.client.put_json(endpoint, data=pipeline_data)
        return Pipeline(**response_data)
    
    async def delete_pipeline(
        self,
        project: str,
        pipeline_id: int
    ) -> None:
        """
        Delete a pipeline.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
        """
        endpoint = f"projects/{project}/pipelines/{pipeline_id}"
        await self.client.delete(endpoint)
    
    # Pipeline Runs
    async def list_pipeline_runs(
        self,
        project: str,
        pipeline_id: Optional[int] = None,
        top: Optional[int] = None,
        continuation_token: Optional[str] = None
    ) -> List[PipelineRun]:
        """
        List pipeline runs.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID filter
            top: Maximum number of runs
            continuation_token: Continuation token for pagination
            
        Returns:
            List of pipeline runs
        """
        params = {}
        if top:
            params['$top'] = top
        if continuation_token:
            params['continuationToken'] = continuation_token
        
        if pipeline_id:
            endpoint = f"projects/{project}/pipelines/{pipeline_id}/runs"
        else:
            endpoint = f"projects/{project}/pipelines/runs"
        
        response_data = await self.client.get_json(endpoint, params=params)
        response = PipelineRunsResponse(**response_data)
        return response.value
    
    async def get_pipeline_run(
        self,
        project: str,
        pipeline_id: int,
        run_id: int
    ) -> PipelineRun:
        """
        Get a specific pipeline run.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
            run_id: Run ID
            
        Returns:
            Pipeline run details
        """
        endpoint = f"projects/{project}/pipelines/{pipeline_id}/runs/{run_id}"
        response_data = await self.client.get_json(endpoint)
        return PipelineRun(**response_data)
    
    async def run_pipeline(
        self,
        project: str,
        pipeline_id: int,
        run_parameters: Optional[Dict[str, Any]] = None,
        template_parameters: Optional[Dict[str, Any]] = None,
        variables: Optional[Dict[str, Any]] = None,
        yaml_override: Optional[str] = None,
        resources: Optional[Dict[str, Any]] = None,
        staging_only: Optional[bool] = None
    ) -> PipelineRun:
        """
        Run a pipeline.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
            run_parameters: Run parameters
            template_parameters: Template parameters
            variables: Pipeline variables
            yaml_override: YAML override content
            resources: Pipeline resources
            staging_only: Staging only run
            
        Returns:
            Started pipeline run
        """
        run_data = {}
        
        if run_parameters:
            run_data.update(run_parameters)
        
        if template_parameters:
            run_data['templateParameters'] = template_parameters
        
        if variables:
            run_data['variables'] = variables
        
        if yaml_override:
            run_data['yamlOverride'] = yaml_override
        
        if resources:
            run_data['resources'] = resources
        
        if staging_only:
            run_data['stagingOnly'] = staging_only
        
        endpoint = f"projects/{project}/pipelines/{pipeline_id}/runs"
        response_data = await self.client.post_json(endpoint, data=run_data)
        return PipelineRun(**response_data)
    
    async def cancel_pipeline_run(
        self,
        project: str,
        pipeline_id: int,
        run_id: int,
        comment: Optional[str] = None
    ) -> PipelineRun:
        """
        Cancel a pipeline run.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
            run_id: Run ID
            comment: Cancellation comment
            
        Returns:
            Cancelled pipeline run
        """
        cancel_data = {"state": "cancelling"}
        if comment:
            cancel_data["comment"] = comment
        
        endpoint = f"projects/{project}/pipelines/{pipeline_id}/runs/{run_id}"
        response_data = await self.client.patch_json(endpoint, data=cancel_data)
        return PipelineRun(**response_data)
    
    # Pipeline Run Logs
    async def get_pipeline_run_logs(
        self,
        project: str,
        pipeline_id: int,
        run_id: int,
        expand: Optional[str] = None
    ) -> List[PipelineLog]:
        """
        Get pipeline run logs.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
            run_id: Run ID
            expand: Expand options
            
        Returns:
            List of pipeline logs
        """
        params = {}
        if expand:
            params['$expand'] = expand
        
        endpoint = f"projects/{project}/pipelines/{pipeline_id}/runs/{run_id}/logs"
        response_data = await self.client.get_json(endpoint, params=params)
        logs = response_data.get('logs', [])
        return [PipelineLog(**log) for log in logs]
    
    async def get_pipeline_run_log(
        self,
        project: str,
        pipeline_id: int,
        run_id: int,
        log_id: int,
        expand: Optional[str] = None
    ) -> str:
        """
        Get a specific pipeline run log.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
            run_id: Run ID
            log_id: Log ID
            expand: Expand options
            
        Returns:
            Log content as text
        """
        params = {}
        if expand:
            params['$expand'] = expand
        
        endpoint = f"projects/{project}/pipelines/{pipeline_id}/runs/{run_id}/logs/{log_id}"
        return await self.client.get_text(endpoint, params=params)
    
    # Pipeline Artifacts
    async def get_pipeline_run_artifacts(
        self,
        project: str,
        pipeline_id: int,
        run_id: int,
        artifact_name: Optional[str] = None,
        expand: Optional[str] = None
    ) -> List[PipelineArtifact]:
        """
        Get pipeline run artifacts.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
            run_id: Run ID
            artifact_name: Specific artifact name
            expand: Expand options
            
        Returns:
            List of pipeline artifacts
        """
        params = {}
        if artifact_name:
            params['artifactName'] = artifact_name
        if expand:
            params['$expand'] = expand
        
        endpoint = f"projects/{project}/pipelines/{pipeline_id}/runs/{run_id}/artifacts"
        response_data = await self.client.get_json(endpoint, params=params)
        artifacts = response_data.get('value', [])
        return [PipelineArtifact(**artifact) for artifact in artifacts]
    
    # Pipeline Approvals
    async def list_pipeline_approvals(
        self,
        project: str,
        assignedto_filter: Optional[str] = None,
        status_filter: Optional[str] = None,
        type_filter: Optional[str] = None,
        top: Optional[int] = None,
        continuation_token: Optional[str] = None
    ) -> List[PipelineApproval]:
        """
        List pipeline approvals.
        
        Args:
            project: Project ID or name
            assignedto_filter: Assigned to filter
            status_filter: Status filter
            type_filter: Type filter
            top: Maximum number of approvals
            continuation_token: Continuation token
            
        Returns:
            List of pipeline approvals
        """
        params = {}
        if assignedto_filter:
            params['assignedToFilter'] = assignedto_filter
        if status_filter:
            params['statusFilter'] = status_filter
        if type_filter:
            params['typeFilter'] = type_filter
        if top:
            params['$top'] = top
        if continuation_token:
            params['continuationToken'] = continuation_token
        
        endpoint = f"projects/{project}/pipelines/approvals"
        response_data = await self.client.get_json(endpoint, params=params)
        response = PipelineApprovalsResponse(**response_data)
        return response.value
    
    async def get_pipeline_approval(
        self,
        project: str,
        approval_id: str
    ) -> PipelineApproval:
        """
        Get a specific pipeline approval.
        
        Args:
            project: Project ID or name
            approval_id: Approval ID
            
        Returns:
            Pipeline approval details
        """
        endpoint = f"projects/{project}/pipelines/approvals/{approval_id}"
        response_data = await self.client.get_json(endpoint)
        return PipelineApproval(**response_data)
    
    async def update_pipeline_approval(
        self,
        project: str,
        approval_id: str,
        status: str,
        comment: Optional[str] = None,
        instructions: Optional[str] = None
    ) -> PipelineApproval:
        """
        Update a pipeline approval (approve/reject).
        
        Args:
            project: Project ID or name
            approval_id: Approval ID
            status: Approval status (approved, rejected, pending, etc.)
            comment: Approval comment
            instructions: Approval instructions
            
        Returns:
            Updated pipeline approval
        """
        approval_data = {"status": status}
        if comment:
            approval_data["comment"] = comment
        if instructions:
            approval_data["instructions"] = instructions
        
        endpoint = f"projects/{project}/pipelines/approvals/{approval_id}"
        response_data = await self.client.patch_json(endpoint, data=approval_data)
        return PipelineApproval(**response_data)
    
    async def approve_pipeline(
        self,
        project: str,
        approval_id: str,
        comment: Optional[str] = None
    ) -> PipelineApproval:
        """
        Approve a pipeline approval.
        
        Args:
            project: Project ID or name
            approval_id: Approval ID
            comment: Approval comment
            
        Returns:
            Approved pipeline approval
        """
        return await self.update_pipeline_approval(
            project=project,
            approval_id=approval_id,
            status="approved",
            comment=comment
        )
    
    async def reject_pipeline(
        self,
        project: str,
        approval_id: str,
        comment: Optional[str] = None
    ) -> PipelineApproval:
        """
        Reject a pipeline approval.
        
        Args:
            project: Project ID or name
            approval_id: Approval ID
            comment: Rejection comment
            
        Returns:
            Rejected pipeline approval
        """
        return await self.update_pipeline_approval(
            project=project,
            approval_id=approval_id,
            status="rejected",
            comment=comment
        )
    
    # Pipeline Environments
    async def list_pipeline_environments(
        self,
        project: str,
        name: Optional[str] = None,
        top: Optional[int] = None,
        continuation_token: Optional[str] = None
    ) -> List[PipelineEnvironment]:
        """
        List pipeline environments.
        
        Args:
            project: Project ID or name
            name: Environment name filter
            top: Maximum number of environments
            continuation_token: Continuation token
            
        Returns:
            List of pipeline environments
        """
        params = {}
        if name:
            params['name'] = name
        if top:
            params['$top'] = top
        if continuation_token:
            params['continuationToken'] = continuation_token
        
        endpoint = f"projects/{project}/environments"
        response_data = await self.client.get_json(endpoint, params=params)
        response = PipelineEnvironmentsResponse(**response_data)
        return response.value
    
    async def get_pipeline_environment(
        self,
        project: str,
        environment_id: int,
        expand_resource: Optional[str] = None
    ) -> PipelineEnvironment:
        """
        Get a specific pipeline environment.
        
        Args:
            project: Project ID or name
            environment_id: Environment ID
            expand_resource: Expand resource options
            
        Returns:
            Pipeline environment details
        """
        params = {}
        if expand_resource:
            params['$expandResource'] = expand_resource
        
        endpoint = f"projects/{project}/environments/{environment_id}"
        response_data = await self.client.get_json(endpoint, params=params)
        return PipelineEnvironment(**response_data)
    
    async def create_pipeline_environment(
        self,
        project: str,
        environment_data: Dict[str, Any]
    ) -> PipelineEnvironment:
        """
        Create a pipeline environment.
        
        Args:
            project: Project ID or name
            environment_data: Environment creation data
            
        Returns:
            Created pipeline environment
        """
        endpoint = f"projects/{project}/environments"
        response_data = await self.client.post_json(endpoint, data=environment_data)
        return PipelineEnvironment(**response_data)
    
    async def update_pipeline_environment(
        self,
        project: str,
        environment_id: int,
        environment_data: Dict[str, Any]
    ) -> PipelineEnvironment:
        """
        Update a pipeline environment.
        
        Args:
            project: Project ID or name
            environment_id: Environment ID
            environment_data: Environment update data
            
        Returns:
            Updated pipeline environment
        """
        endpoint = f"projects/{project}/environments/{environment_id}"
        response_data = await self.client.patch_json(endpoint, data=environment_data)
        return PipelineEnvironment(**response_data)
    
    async def delete_pipeline_environment(
        self,
        project: str,
        environment_id: int
    ) -> None:
        """
        Delete a pipeline environment.
        
        Args:
            project: Project ID or name
            environment_id: Environment ID
        """
        endpoint = f"projects/{project}/environments/{environment_id}"
        await self.client.delete(endpoint)
    
    # Pipeline Preview
    async def preview_pipeline(
        self,
        project: str,
        pipeline_id: int,
        preview_run: Dict[str, Any]
    ) -> PipelinePreview:
        """
        Preview a pipeline run.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
            preview_run: Preview run data
            
        Returns:
            Pipeline preview
        """
        endpoint = f"projects/{project}/pipelines/{pipeline_id}/preview"
        response_data = await self.client.post_json(endpoint, data=preview_run)
        return PipelinePreview(**response_data)
    
    # Pipeline Variables
    async def get_pipeline_variables(
        self,
        project: str,
        pipeline_id: int,
        variable_group_id: Optional[int] = None
    ) -> Dict[str, PipelineVariable]:
        """
        Get pipeline variables.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
            variable_group_id: Variable group ID
            
        Returns:
            Dictionary of pipeline variables
        """
        params = {}
        if variable_group_id:
            params['variableGroupId'] = variable_group_id
        
        endpoint = f"projects/{project}/pipelines/{pipeline_id}/variables"
        response_data = await self.client.get_json(endpoint, params=params)
        
        variables = {}
        for name, var_data in response_data.get('variables', {}).items():
            variables[name] = PipelineVariable(**var_data)
        
        return variables
    
    async def update_pipeline_variables(
        self,
        project: str,
        pipeline_id: int,
        variables: Dict[str, PipelineVariable]
    ) -> Dict[str, PipelineVariable]:
        """
        Update pipeline variables.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
            variables: Dictionary of variables to update
            
        Returns:
            Updated pipeline variables
        """
        variables_data = {}
        for name, variable in variables.items():
            variables_data[name] = variable.dict_exclude_none()
        
        update_data = {"variables": variables_data}
        
        endpoint = f"projects/{project}/pipelines/{pipeline_id}/variables"
        response_data = await self.client.put_json(endpoint, data=update_data)
        
        result_variables = {}
        for name, var_data in response_data.get('variables', {}).items():
            result_variables[name] = PipelineVariable(**var_data)
        
        return result_variables
    
    # Utility methods
    async def get_latest_pipeline_run(
        self,
        project: str,
        pipeline_id: int,
        result_filter: Optional[str] = None,
        status_filter: Optional[str] = None
    ) -> Optional[PipelineRun]:
        """
        Get the latest pipeline run.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
            result_filter: Result filter
            status_filter: Status filter
            
        Returns:
            Latest pipeline run or None
        """
        runs = await self.list_pipeline_runs(
            project=project,
            pipeline_id=pipeline_id,
            top=1
        )
        
        if runs:
            # Apply filters if specified
            latest_run = runs[0]
            if result_filter and latest_run.result != result_filter:
                return None
            if status_filter and latest_run.state != status_filter:
                return None
            return latest_run
        
        return None
    
    async def wait_for_pipeline_completion(
        self,
        project: str,
        pipeline_id: int,
        run_id: int,
        timeout_seconds: int = 3600,
        poll_interval: int = 30
    ) -> PipelineRun:
        """
        Wait for a pipeline run to complete.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
            run_id: Run ID
            timeout_seconds: Maximum wait time
            poll_interval: Polling interval in seconds
            
        Returns:
            Completed pipeline run
            
        Raises:
            TimeoutError: If pipeline doesn't complete within timeout
        """
        import asyncio
        
        start_time = datetime.now()
        
        while True:
            run = await self.get_pipeline_run(
                project=project,
                pipeline_id=pipeline_id,
                run_id=run_id
            )
            
            if run.state in ["completed", "canceled"]:
                return run
            
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed >= timeout_seconds:
                raise TimeoutError(f"Pipeline run {run_id} did not complete within {timeout_seconds} seconds")
            
            await asyncio.sleep(poll_interval)
    
    async def get_pipeline_run_summary(
        self,
        project: str,
        pipeline_id: int,
        run_id: int
    ) -> Dict[str, Any]:
        """
        Get a comprehensive summary of a pipeline run.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID
            run_id: Run ID
            
        Returns:
            Pipeline run summary with logs and artifacts
        """
        # Get the run details
        run = await self.get_pipeline_run(project, pipeline_id, run_id)
        
        # Get logs
        try:
            logs = await self.get_pipeline_run_logs(project, pipeline_id, run_id)
        except Exception:
            logs = []
        
        # Get artifacts
        try:
            artifacts = await self.get_pipeline_run_artifacts(project, pipeline_id, run_id)
        except Exception:
            artifacts = []
        
        return {
            "run": run,
            "logs": logs,
            "artifacts": artifacts,
            "summary": {
                "pipeline_id": pipeline_id,
                "run_id": run_id,
                "state": run.state,
                "result": run.result,
                "created_date": run.created_date,
                "finished_date": run.finished_date,
                "log_count": len(logs),
                "artifact_count": len(artifacts)
            }
        }
    
    async def iterate_pipeline_runs(
        self,
        project: str,
        pipeline_id: Optional[int] = None,
        page_size: int = 100,
        **kwargs
    ) -> AsyncGenerator[PipelineRun, None]:
        """
        Iterate through all pipeline runs.
        
        Args:
            project: Project ID or name
            pipeline_id: Pipeline ID filter
            page_size: Number of runs per page
            
        Yields:
            Pipeline runs one by one
        """
        async def request_func(**params):
            runs = await self.list_pipeline_runs(
                project=project,
                pipeline_id=pipeline_id,
                top=page_size,
                **params,
                **kwargs
            )
            return {"value": runs, "count": len(runs)}
        
        paginator = create_paginator(request_func, page_size=page_size)
        async for run in paginator.iterate_items():
            yield run
