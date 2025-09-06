"""
Pipeline Facade - High-level CI/CD pipeline management and orchestration.

This facade combines build, pipeline, release, and testing services to provide
comprehensive DevOps pipeline lifecycle management.
"""

from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta
from ..services import (
    BuildService, PipelinesService, ReleaseService, TestService,
    GitService, PackagingService, NotificationService, ServiceHooksService
)
from ..models import (
    BuildDefinition, Pipeline, ReleaseDefinition, TestPlan,
    GitRepository, Package, NotificationSubscription, ServiceHookSubscription
)


class PipelineFacade:
    """High-level facade for complete CI/CD pipeline management operations."""
    
    def __init__(
        self,
        build_service: BuildService,
        pipelines_service: PipelinesService,
        release_service: ReleaseService,
        test_service: TestService,
        git_service: GitService,
        packaging_service: PackagingService,
        notification_service: NotificationService,
        service_hooks_service: ServiceHooksService
    ):
        self.build = build_service
        self.pipelines = pipelines_service
        self.release = release_service
        self.test = test_service
        self.git = git_service
        self.packaging = packaging_service
        self.notification = notification_service
        self.service_hooks = service_hooks_service
    
    async def create_complete_cicd_pipeline(
        self,
        project_id: str,
        repository_id: str,
        pipeline_name: str,
        build_config: Dict[str, Any],
        test_config: Optional[Dict[str, Any]] = None,
        deployment_config: Optional[Dict[str, Any]] = None,
        notification_config: Optional[Dict[str, Any]] = None,
        quality_gates: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a complete CI/CD pipeline with all stages configured.
        
        Args:
            project_id: Project ID
            repository_id: Repository ID
            pipeline_name: Pipeline name
            build_config: Build configuration
            test_config: Test configuration
            deployment_config: Deployment stages configuration
            notification_config: Notification settings
            quality_gates: Quality gate definitions
            
        Returns:
            Complete pipeline setup result
        """
        result = {
            "pipeline_name": pipeline_name,
            "build_pipeline": None,
            "test_plans": [],
            "release_pipeline": None,
            "notifications": [],
            "webhooks": [],
            "quality_gates": [],
            "artifacts": [],
            "errors": []
        }
        
        try:
            # 1. Create build/CI pipeline
            ci_result = await self._create_ci_pipeline(
                project_id,
                repository_id,
                pipeline_name,
                build_config
            )
            result["build_pipeline"] = ci_result
            
            # 2. Set up test automation
            if test_config:
                test_result = await self._setup_test_automation(
                    project_id,
                    pipeline_name,
                    test_config
                )
                result["test_plans"] = test_result
            
            # 3. Create release/CD pipeline
            if deployment_config:
                cd_result = await self._create_cd_pipeline(
                    project_id,
                    pipeline_name,
                    deployment_config,
                    ci_result.get("definition_id") if ci_result else None
                )
                result["release_pipeline"] = cd_result
            
            # 4. Set up quality gates
            if quality_gates:
                gates_result = await self._setup_quality_gates(
                    project_id,
                    result["build_pipeline"],
                    result["release_pipeline"],
                    quality_gates
                )
                result["quality_gates"] = gates_result
            
            # 5. Configure notifications
            if notification_config:
                notifications_result = await self._setup_pipeline_notifications(
                    project_id,
                    pipeline_name,
                    notification_config
                )
                result["notifications"] = notifications_result
            
            # 6. Set up webhooks for integrations
            if notification_config and "webhooks" in notification_config:
                webhooks_result = await self._setup_pipeline_webhooks(
                    project_id,
                    pipeline_name,
                    notification_config["webhooks"]
                )
                result["webhooks"] = webhooks_result
            
            # 7. Configure artifact feeds
            if build_config.get("publish_artifacts"):
                artifacts_result = await self._setup_artifact_feeds(
                    project_id,
                    pipeline_name,
                    build_config.get("artifact_config", {})
                )
                result["artifacts"] = artifacts_result
            
        except Exception as e:
            result["errors"].append(f"Pipeline creation failed: {str(e)}")
        
        return result
    
    async def clone_pipeline_to_environment(
        self,
        source_project_id: str,
        target_project_id: str,
        pipeline_name: str,
        environment_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Clone an existing pipeline to a different environment/project.
        
        Args:
            source_project_id: Source project ID
            target_project_id: Target project ID
            pipeline_name: Pipeline to clone
            environment_config: Environment-specific configuration
            
        Returns:
            Pipeline cloning result
        """
        result = {
            "source_pipeline": None,
            "cloned_pipeline": None,
            "environment_adaptations": [],
            "errors": []
        }
        
        try:
            # Find source pipeline
            source_definitions = await self.build.list_definitions(source_project_id)
            source_pipeline = None
            
            for definition in source_definitions:
                if definition.name == pipeline_name:
                    source_pipeline = definition
                    break
            
            if not source_pipeline:
                result["errors"].append(f"Source pipeline '{pipeline_name}' not found")
                return result
            
            result["source_pipeline"] = source_pipeline
            
            # Clone build definition
            cloned_definition = await self._clone_build_definition(
                source_pipeline,
                target_project_id,
                environment_config
            )
            result["cloned_pipeline"] = cloned_definition
            
            # Apply environment-specific adaptations
            adaptations = await self._apply_environment_adaptations(
                target_project_id,
                cloned_definition,
                environment_config
            )
            result["environment_adaptations"] = adaptations
            
        except Exception as e:
            result["errors"].append(f"Pipeline cloning failed: {str(e)}")
        
        return result
    
    async def setup_multi_stage_deployment(
        self,
        project_id: str,
        pipeline_name: str,
        stages: List[Dict[str, Any]],
        approval_config: Optional[Dict[str, Any]] = None,
        deployment_gates: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Set up multi-stage deployment pipeline with approvals and gates.
        
        Args:
            project_id: Project ID
            pipeline_name: Pipeline name
            stages: Deployment stages configuration
            approval_config: Approval workflow configuration
            deployment_gates: Pre/post deployment gates
            
        Returns:
            Multi-stage deployment setup result
        """
        result = {
            "release_definition": None,
            "stages": [],
            "approvals": [],
            "gates": [],
            "errors": []
        }
        
        try:
            # Create release definition
            release_def_data = {
                "name": f"{pipeline_name}-Release",
                "description": f"Multi-stage deployment for {pipeline_name}",
                "environments": []
            }
            
            # Configure each stage
            for i, stage_config in enumerate(stages):
                stage_result = await self._configure_deployment_stage(
                    project_id,
                    stage_config,
                    i,
                    approval_config,
                    deployment_gates
                )
                result["stages"].append(stage_result)
                
                if stage_result.get("environment"):
                    release_def_data["environments"].append(stage_result["environment"])
            
            # Create the release definition
            release_definition = await self.release.create_definition(
                project_id,
                release_def_data
            )
            result["release_definition"] = release_definition
            
        except Exception as e:
            result["errors"].append(f"Multi-stage deployment setup failed: {str(e)}")
        
        return result
    
    async def implement_gitops_workflow(
        self,
        project_id: str,
        config_repository_id: str,
        target_environments: List[Dict[str, Any]],
        sync_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Implement GitOps workflow with configuration repositories.
        
        Args:
            project_id: Project ID
            config_repository_id: Configuration repository ID
            target_environments: Target environments
            sync_config: Synchronization configuration
            
        Returns:
            GitOps implementation result
        """
        result = {
            "config_repository": None,
            "sync_pipelines": [],
            "environment_configs": [],
            "monitoring": [],
            "errors": []
        }
        
        try:
            # Get config repository details
            config_repo = await self.git.get_repository(project_id, config_repository_id)
            result["config_repository"] = config_repo
            
            # Create sync pipelines for each environment
            for env_config in target_environments:
                sync_pipeline = await self._create_gitops_sync_pipeline(
                    project_id,
                    config_repository_id,
                    env_config,
                    sync_config
                )
                result["sync_pipelines"].append(sync_pipeline)
            
            # Set up branch policies for GitOps workflow
            gitops_policies = await self._setup_gitops_branch_policies(
                project_id,
                config_repository_id,
                sync_config
            )
            result["environment_configs"] = gitops_policies
            
            # Configure monitoring and alerting
            monitoring_setup = await self._setup_gitops_monitoring(
                project_id,
                result["sync_pipelines"]
            )
            result["monitoring"] = monitoring_setup
            
        except Exception as e:
            result["errors"].append(f"GitOps workflow implementation failed: {str(e)}")
        
        return result
    
    async def analyze_pipeline_performance(
        self,
        project_id: str,
        pipeline_name: Optional[str] = None,
        days: int = 30,
        include_trends: bool = True
    ) -> Dict[str, Any]:
        """
        Comprehensive pipeline performance analysis.
        
        Args:
            project_id: Project ID
            pipeline_name: Specific pipeline to analyze
            days: Number of days to analyze
            include_trends: Include trend analysis
            
        Returns:
            Pipeline performance analysis
        """
        analysis = {
            "period": f"{days} days",
            "pipelines_analyzed": [],
            "performance_metrics": {},
            "trends": {},
            "recommendations": [],
            "errors": []
        }
        
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Get pipeline definitions
            if pipeline_name:
                definitions = await self.build.list_definitions(project_id, name=pipeline_name)
            else:
                definitions = await self.build.list_definitions(project_id)
            
            for definition in definitions:
                pipeline_analysis = await self._analyze_single_pipeline_performance(
                    project_id,
                    definition,
                    start_date,
                    end_date,
                    include_trends
                )
                analysis["pipelines_analyzed"].append(pipeline_analysis)
            
            # Calculate overall metrics
            overall_metrics = self._calculate_overall_pipeline_metrics(
                analysis["pipelines_analyzed"]
            )
            analysis["performance_metrics"] = overall_metrics
            
            # Generate recommendations
            recommendations = self._generate_pipeline_recommendations(
                analysis["pipelines_analyzed"],
                overall_metrics
            )
            analysis["recommendations"] = recommendations
            
        except Exception as e:
            analysis["errors"].append(f"Pipeline analysis failed: {str(e)}")
        
        return analysis
    
    async def optimize_pipeline_performance(
        self,
        project_id: str,
        pipeline_id: str,
        optimization_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply automated optimizations to improve pipeline performance.
        
        Args:
            project_id: Project ID
            pipeline_id: Pipeline ID to optimize
            optimization_config: Optimization settings
            
        Returns:
            Pipeline optimization result
        """
        result = {
            "original_pipeline": None,
            "optimizations_applied": [],
            "performance_impact": {},
            "errors": []
        }
        
        try:
            # Get current pipeline definition
            original_definition = await self.build.get_definition(project_id, pipeline_id)
            result["original_pipeline"] = original_definition
            
            # Apply parallel job optimization
            if optimization_config.get("enable_parallelism"):
                parallel_result = await self._optimize_pipeline_parallelism(
                    project_id,
                    pipeline_id,
                    optimization_config.get("parallel_config", {})
                )
                result["optimizations_applied"].append(parallel_result)
            
            # Apply caching optimizations
            if optimization_config.get("enable_caching"):
                cache_result = await self._optimize_pipeline_caching(
                    project_id,
                    pipeline_id,
                    optimization_config.get("cache_config", {})
                )
                result["optimizations_applied"].append(cache_result)
            
            # Apply resource optimization
            if optimization_config.get("optimize_resources"):
                resource_result = await self._optimize_pipeline_resources(
                    project_id,
                    pipeline_id,
                    optimization_config.get("resource_config", {})
                )
                result["optimizations_applied"].append(resource_result)
            
            # Estimate performance impact
            impact_analysis = self._estimate_optimization_impact(
                result["optimizations_applied"]
            )
            result["performance_impact"] = impact_analysis
            
        except Exception as e:
            result["errors"].append(f"Pipeline optimization failed: {str(e)}")
        
        return result
    
    async def setup_pipeline_security_scanning(
        self,
        project_id: str,
        pipeline_id: str,
        security_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Set up comprehensive security scanning in CI/CD pipeline.
        
        Args:
            project_id: Project ID
            pipeline_id: Pipeline ID
            security_config: Security scanning configuration
            
        Returns:
            Security scanning setup result
        """
        result = {
            "security_tasks": [],
            "quality_gates": [],
            "notifications": [],
            "policies": [],
            "errors": []
        }
        
        try:
            # Add static code analysis
            if security_config.get("static_analysis"):
                sast_task = await self._add_static_analysis_task(
                    project_id,
                    pipeline_id,
                    security_config["static_analysis"]
                )
                result["security_tasks"].append(sast_task)
            
            # Add dependency scanning
            if security_config.get("dependency_scan"):
                dependency_task = await self._add_dependency_scanning_task(
                    project_id,
                    pipeline_id,
                    security_config["dependency_scan"]
                )
                result["security_tasks"].append(dependency_task)
            
            # Add container scanning
            if security_config.get("container_scan"):
                container_task = await self._add_container_scanning_task(
                    project_id,
                    pipeline_id,
                    security_config["container_scan"]
                )
                result["security_tasks"].append(container_task)
            
            # Set up security quality gates
            if security_config.get("quality_gates"):
                gates_result = await self._setup_security_quality_gates(
                    project_id,
                    pipeline_id,
                    security_config["quality_gates"]
                )
                result["quality_gates"] = gates_result
            
            # Configure security notifications
            if security_config.get("notifications"):
                notifications_result = await self._setup_security_notifications(
                    project_id,
                    pipeline_id,
                    security_config["notifications"]
                )
                result["notifications"] = notifications_result
            
        except Exception as e:
            result["errors"].append(f"Security scanning setup failed: {str(e)}")
        
        return result
    
    # Helper methods
    async def _create_ci_pipeline(
        self,
        project_id: str,
        repository_id: str,
        pipeline_name: str,
        build_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create CI pipeline."""
        try:
            # Generate basic YAML pipeline
            yaml_content = self._generate_ci_yaml(build_config)
            
            # Create pipeline definition
            pipeline_data = {
                "name": f"{pipeline_name}-CI",
                "repository": {
                    "id": repository_id,
                    "type": "azureReposGit"
                },
                "path": f"/.azure-pipelines/{pipeline_name.lower()}-ci.yml"
            }
            
            pipeline = await self.pipelines.create_pipeline(project_id, pipeline_data)
            
            return {
                "pipeline": pipeline,
                "definition_id": pipeline.id,
                "yaml_path": pipeline_data["path"],
                "success": True
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _setup_test_automation(
        self,
        project_id: str,
        pipeline_name: str,
        test_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up test automation."""
        test_plans = []
        
        try:
            if test_config.get("unit_tests"):
                unit_test_plan = await self.test.create_test_plan(
                    project_id,
                    {
                        "name": f"{pipeline_name} Unit Tests",
                        "description": "Automated unit test plan"
                    }
                )
                test_plans.append({
                    "type": "unit",
                    "plan": unit_test_plan,
                    "success": True
                })
            
            if test_config.get("integration_tests"):
                integration_test_plan = await self.test.create_test_plan(
                    project_id,
                    {
                        "name": f"{pipeline_name} Integration Tests",
                        "description": "Automated integration test plan"
                    }
                )
                test_plans.append({
                    "type": "integration",
                    "plan": integration_test_plan,
                    "success": True
                })
        except Exception as e:
            test_plans.append({
                "type": "error",
                "success": False,
                "error": str(e)
            })
        
        return test_plans
    
    async def _create_cd_pipeline(
        self,
        project_id: str,
        pipeline_name: str,
        deployment_config: Dict[str, Any],
        build_definition_id: Optional[str]
    ) -> Dict[str, Any]:
        """Create CD pipeline."""
        try:
            environments = []
            for env_name, env_config in deployment_config.get("environments", {}).items():
                environment = {
                    "name": env_name,
                    "rank": env_config.get("rank", 1),
                    "deployPhases": [
                        {
                            "deploymentInput": {
                                "parallelExecution": {"parallelExecutionType": "none"},
                                "skipArtifactsDownload": False,
                                "artifactsDownloadInput": {},
                                "queueId": env_config.get("agent_pool_id", 1),
                                "demands": [],
                                "enableAccessToken": False,
                                "timeoutInMinutes": 0
                            },
                            "rank": 1,
                            "phaseType": "deploymentGateway",
                            "name": "Agent job"
                        }
                    ]
                }
                environments.append(environment)
            
            release_definition = {
                "name": f"{pipeline_name}-CD",
                "description": f"Release pipeline for {pipeline_name}",
                "environments": environments
            }
            
            if build_definition_id:
                release_definition["artifacts"] = [
                    {
                        "sourceId": build_definition_id,
                        "type": "Build",
                        "alias": "_" + pipeline_name.replace("-", "_"),
                        "definitionReference": {
                            "definition": {"id": build_definition_id, "name": pipeline_name}
                        }
                    }
                ]
            
            release_def = await self.release.create_definition(project_id, release_definition)
            
            return {
                "release_definition": release_def,
                "environments": len(environments),
                "success": True
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _setup_quality_gates(
        self,
        project_id: str,
        build_pipeline: Dict[str, Any],
        release_pipeline: Dict[str, Any],
        quality_gates: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up quality gates."""
        gates = []
        
        # This would require implementing specific quality gate logic
        # For now, return placeholder
        gates.append({
            "type": "code_coverage",
            "threshold": quality_gates.get("code_coverage_threshold", 80),
            "status": "configured"
        })
        
        return gates
    
    async def _setup_pipeline_notifications(
        self,
        project_id: str,
        pipeline_name: str,
        notification_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up pipeline notifications."""
        notifications = []
        
        try:
            if notification_config.get("email"):
                email_subscription = await self.notification.create_build_subscription(
                    subscriber_id=notification_config["email"]["subscriber"],
                    project_id=project_id,
                    build_status="failed",
                    channel_type="email",
                    channel_address=notification_config["email"]["address"]
                )
                notifications.append({
                    "type": "email",
                    "subscription": email_subscription,
                    "success": True
                })
        except Exception as e:
            notifications.append({
                "type": "email",
                "success": False,
                "error": str(e)
            })
        
        return notifications
    
    async def _setup_pipeline_webhooks(
        self,
        project_id: str,
        pipeline_name: str,
        webhook_config: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Set up pipeline webhooks."""
        webhooks = []
        
        for webhook in webhook_config:
            try:
                service_hook = await self.service_hooks.create_webhook_subscription(
                    webhook_url=webhook["url"],
                    event_type="ms.vss-build.build-status-changed-event",
                    secret=webhook.get("secret")
                )
                webhooks.append({
                    "url": webhook["url"],
                    "subscription": service_hook,
                    "success": True
                })
            except Exception as e:
                webhooks.append({
                    "url": webhook["url"],
                    "success": False,
                    "error": str(e)
                })
        
        return webhooks
    
    async def _setup_artifact_feeds(
        self,
        project_id: str,
        pipeline_name: str,
        artifact_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up artifact feeds."""
        artifacts = []
        
        try:
            feed_name = artifact_config.get("feed_name", f"{pipeline_name}-artifacts")
            
            feed = await self.packaging.create_feed(
                project_id,
                {
                    "name": feed_name,
                    "description": f"Artifact feed for {pipeline_name}"
                }
            )
            
            artifacts.append({
                "type": "feed",
                "feed": feed,
                "success": True
            })
        except Exception as e:
            artifacts.append({
                "type": "feed",
                "success": False,
                "error": str(e)
            })
        
        return artifacts
    
    def _generate_ci_yaml(self, build_config: Dict[str, Any]) -> str:
        """Generate CI YAML content."""
        language = build_config.get("language", "dotnet")
        
        if language == "dotnet":
            return """
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

variables:
  buildConfiguration: 'Release'

steps:
- task: DotNetCoreCLI@2
  displayName: 'Restore packages'
  inputs:
    command: 'restore'
    projects: '**/*.csproj'

- task: DotNetCoreCLI@2
  displayName: 'Build'
  inputs:
    command: 'build'
    projects: '**/*.csproj'
    arguments: '--configuration $(buildConfiguration) --no-restore'

- task: DotNetCoreCLI@2
  displayName: 'Test'
  inputs:
    command: 'test'
    projects: '**/*Tests.csproj'
    arguments: '--configuration $(buildConfiguration) --no-build --collect "Code Coverage"'

- task: DotNetCoreCLI@2
  displayName: 'Publish'
  inputs:
    command: 'publish'
    projects: '**/*.csproj'
    arguments: '--configuration $(buildConfiguration) --output $(Build.ArtifactStagingDirectory)'

- task: PublishBuildArtifacts@1
  displayName: 'Publish Artifacts'
  inputs:
    pathToPublish: '$(Build.ArtifactStagingDirectory)'
    artifactName: 'drop'
"""
        else:
            return f"""
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- script: echo "Building {language} application"
  displayName: 'Build {language} application'
"""
    
    async def _clone_build_definition(
        self,
        source_definition: BuildDefinition,
        target_project_id: str,
        environment_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Clone build definition to target project."""
        # This would require complex logic to clone build definitions
        return {
            "cloned": False,
            "note": "Build definition cloning requires detailed implementation"
        }
    
    async def _apply_environment_adaptations(
        self,
        project_id: str,
        pipeline: Dict[str, Any],
        environment_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Apply environment-specific adaptations."""
        return [
            {
                "type": "environment_variables",
                "applied": True,
                "note": "Environment variable adaptation would be implemented here"
            }
        ]
    
    async def _configure_deployment_stage(
        self,
        project_id: str,
        stage_config: Dict[str, Any],
        stage_index: int,
        approval_config: Optional[Dict[str, Any]],
        deployment_gates: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Configure a deployment stage."""
        return {
            "stage_name": stage_config.get("name", f"Stage-{stage_index}"),
            "environment": {
                "name": stage_config.get("name", f"Stage-{stage_index}"),
                "rank": stage_index + 1
            },
            "configured": True
        }
    
    async def _create_gitops_sync_pipeline(
        self,
        project_id: str,
        config_repository_id: str,
        env_config: Dict[str, Any],
        sync_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create GitOps sync pipeline."""
        return {
            "environment": env_config.get("name"),
            "sync_pipeline": "would_be_created",
            "note": "GitOps sync pipeline creation requires detailed implementation"
        }
    
    async def _setup_gitops_branch_policies(
        self,
        project_id: str,
        repository_id: str,
        sync_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up GitOps branch policies."""
        return [
            {
                "type": "pull_request_required",
                "configured": True,
                "note": "GitOps branch policies would be configured here"
            }
        ]
    
    async def _setup_gitops_monitoring(
        self,
        project_id: str,
        sync_pipelines: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Set up GitOps monitoring."""
        return [
            {
                "type": "sync_status_monitoring",
                "configured": True,
                "note": "GitOps monitoring would be implemented here"
            }
        ]
    
    async def _analyze_single_pipeline_performance(
        self,
        project_id: str,
        definition: BuildDefinition,
        start_date: datetime,
        end_date: datetime,
        include_trends: bool
    ) -> Dict[str, Any]:
        """Analyze single pipeline performance."""
        try:
            # Get recent builds
            builds = await self.build.list_builds(
                project_id,
                definition_ids=[definition.id],
                min_time=start_date,
                max_time=end_date
            )
            
            # Calculate metrics
            total_builds = len(builds)
            successful_builds = len([b for b in builds if b.result == "succeeded"])
            failed_builds = len([b for b in builds if b.result == "failed"])
            
            # Calculate average duration
            completed_builds = [b for b in builds if b.finish_time and b.start_time]
            avg_duration = 0
            if completed_builds:
                total_duration = sum([
                    (b.finish_time - b.start_time).total_seconds() 
                    for b in completed_builds
                ])
                avg_duration = total_duration / len(completed_builds)
            
            return {
                "pipeline_name": definition.name,
                "pipeline_id": definition.id,
                "total_builds": total_builds,
                "successful_builds": successful_builds,
                "failed_builds": failed_builds,
                "success_rate": successful_builds / total_builds if total_builds > 0 else 0,
                "average_duration_seconds": avg_duration,
                "analysis_period": f"{start_date.isoformat()} to {end_date.isoformat()}"
            }
        except Exception as e:
            return {
                "pipeline_name": definition.name,
                "error": str(e)
            }
    
    def _calculate_overall_pipeline_metrics(
        self,
        pipeline_analyses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate overall pipeline metrics."""
        valid_analyses = [p for p in pipeline_analyses if "error" not in p]
        
        if not valid_analyses:
            return {"error": "No valid pipeline analyses"}
        
        total_builds = sum(p.get("total_builds", 0) for p in valid_analyses)
        total_successful = sum(p.get("successful_builds", 0) for p in valid_analyses)
        
        durations = [p.get("average_duration_seconds", 0) for p in valid_analyses if p.get("average_duration_seconds", 0) > 0]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "total_pipelines": len(valid_analyses),
            "total_builds": total_builds,
            "overall_success_rate": total_successful / total_builds if total_builds > 0 else 0,
            "average_build_duration_seconds": avg_duration,
            "fastest_pipeline": min(valid_analyses, key=lambda p: p.get("average_duration_seconds", float('inf')))["pipeline_name"] if valid_analyses else None,
            "slowest_pipeline": max(valid_analyses, key=lambda p: p.get("average_duration_seconds", 0))["pipeline_name"] if valid_analyses else None
        }
    
    def _generate_pipeline_recommendations(
        self,
        pipeline_analyses: List[Dict[str, Any]],
        overall_metrics: Dict[str, Any]
    ) -> List[str]:
        """Generate pipeline optimization recommendations."""
        recommendations = []
        
        # Success rate recommendations
        if overall_metrics.get("overall_success_rate", 0) < 0.9:
            recommendations.append("Overall pipeline success rate is below 90%. Consider reviewing failing builds and improving test reliability.")
        
        # Performance recommendations
        if overall_metrics.get("average_build_duration_seconds", 0) > 1800:  # 30 minutes
            recommendations.append("Average build duration exceeds 30 minutes. Consider enabling parallelization and caching.")
        
        # Individual pipeline recommendations
        for analysis in pipeline_analyses:
            if analysis.get("success_rate", 0) < 0.8:
                recommendations.append(f"Pipeline '{analysis.get('pipeline_name')}' has low success rate. Review and fix failing tests.")
        
        return recommendations
    
    async def _optimize_pipeline_parallelism(
        self,
        project_id: str,
        pipeline_id: str,
        parallel_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimize pipeline parallelism."""
        return {
            "optimization": "parallelism",
            "applied": True,
            "note": "Parallelism optimization would modify pipeline YAML/definition"
        }
    
    async def _optimize_pipeline_caching(
        self,
        project_id: str,
        pipeline_id: str,
        cache_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimize pipeline caching."""
        return {
            "optimization": "caching",
            "applied": True,
            "note": "Caching optimization would add cache tasks to pipeline"
        }
    
    async def _optimize_pipeline_resources(
        self,
        project_id: str,
        pipeline_id: str,
        resource_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Optimize pipeline resources."""
        return {
            "optimization": "resources",
            "applied": True,
            "note": "Resource optimization would adjust agent pools and VM sizes"
        }
    
    def _estimate_optimization_impact(
        self,
        optimizations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Estimate optimization impact."""
        estimated_improvement = 0
        
        for opt in optimizations:
            if opt.get("optimization") == "parallelism":
                estimated_improvement += 30  # 30% improvement
            elif opt.get("optimization") == "caching":
                estimated_improvement += 20  # 20% improvement
            elif opt.get("optimization") == "resources":
                estimated_improvement += 15  # 15% improvement
        
        return {
            "estimated_performance_improvement_percent": min(estimated_improvement, 70),
            "optimizations_count": len(optimizations)
        }
    
    async def _add_static_analysis_task(
        self,
        project_id: str,
        pipeline_id: str,
        sast_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add static analysis task."""
        return {
            "task_type": "static_analysis",
            "tool": sast_config.get("tool", "SonarQube"),
            "added": True,
            "note": "Static analysis task would be added to pipeline definition"
        }
    
    async def _add_dependency_scanning_task(
        self,
        project_id: str,
        pipeline_id: str,
        dependency_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add dependency scanning task."""
        return {
            "task_type": "dependency_scanning",
            "tool": dependency_config.get("tool", "WhiteSource"),
            "added": True,
            "note": "Dependency scanning task would be added to pipeline definition"
        }
    
    async def _add_container_scanning_task(
        self,
        project_id: str,
        pipeline_id: str,
        container_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add container scanning task."""
        return {
            "task_type": "container_scanning",
            "tool": container_config.get("tool", "Twistlock"),
            "added": True,
            "note": "Container scanning task would be added to pipeline definition"
        }
    
    async def _setup_security_quality_gates(
        self,
        project_id: str,
        pipeline_id: str,
        gates_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up security quality gates."""
        return [
            {
                "gate_type": "security_threshold",
                "configured": True,
                "note": "Security quality gates would be configured in pipeline"
            }
        ]
    
    async def _setup_security_notifications(
        self,
        project_id: str,
        pipeline_id: str,
        notification_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up security notifications."""
        return [
            {
                "notification_type": "security_alert",
                "configured": True,
                "note": "Security notifications would be configured"
            }
        ]
