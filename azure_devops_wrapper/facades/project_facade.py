"""
Project Facade - High-level project management and onboarding operations.

This facade combines multiple Azure DevOps services to provide comprehensive
project lifecycle management, from creation to complete configuration.
"""

from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from ..services import (
    CoreService, GitService, WorkItemsService, BuildService, 
    PipelinesService, SecurityService, GraphService
)
from ..models import Project, Team, GitRepository, WorkItemType, ProcessTemplate


class ProjectFacade:
    """High-level facade for complete project management operations."""
    
    def __init__(
        self,
        core_service: CoreService,
        git_service: GitService,
        work_items_service: WorkItemsService,
        build_service: BuildService,
        pipelines_service: PipelinesService,
        security_service: SecurityService,
        graph_service: GraphService
    ):
        self.core = core_service
        self.git = git_service
        self.work_items = work_items_service
        self.build = build_service
        self.pipelines = pipelines_service
        self.security = security_service
        self.graph = graph_service
    
    async def create_complete_project(
        self,
        project_name: str,
        description: str,
        template_type: str = "Agile",
        visibility: str = "private",
        source_control_type: str = "Git",
        initial_repositories: Optional[List[str]] = None,
        team_members: Optional[List[str]] = None,
        project_admins: Optional[List[str]] = None,
        setup_default_pipelines: bool = True
    ) -> Dict[str, Any]:
        """
        Create a complete project with full configuration.
        
        Args:
            project_name: Project name
            description: Project description
            template_type: Process template (Agile, Scrum, CMMI, Basic)
            visibility: Project visibility (private, public)
            source_control_type: Source control type (Git, Tfvc)
            initial_repositories: List of repository names to create
            team_members: List of user emails to add as team members
            project_admins: List of user emails to add as project admins
            setup_default_pipelines: Create default CI/CD pipelines
            
        Returns:
            Complete project setup result
        """
        result = {
            "project": None,
            "repositories": [],
            "teams": [],
            "work_item_types": [],
            "pipelines": [],
            "security_setup": {},
            "errors": []
        }
        
        try:
            # 1. Create the project
            project_data = {
                "name": project_name,
                "description": description,
                "visibility": visibility,
                "capabilities": {
                    "versioncontrol": {"sourceControlType": source_control_type},
                    "processTemplate": {"templateTypeId": template_type}
                }
            }
            
            project = await self.core.create_project(project_data)
            result["project"] = project
            
            # Wait for project to be fully created
            await self._wait_for_project_creation(project.id)
            
            # 2. Create initial repositories
            if initial_repositories:
                for repo_name in initial_repositories:
                    try:
                        repo = await self.git.create_repository(
                            project_id=project.id,
                            repository_data={"name": repo_name}
                        )
                        result["repositories"].append(repo)
                    except Exception as e:
                        result["errors"].append(f"Failed to create repository {repo_name}: {str(e)}")
            
            # 3. Set up teams and permissions
            if team_members or project_admins:
                security_result = await self._setup_project_security(
                    project.id,
                    team_members or [],
                    project_admins or []
                )
                result["security_setup"] = security_result
            
            # 4. Configure work item types and areas
            work_item_setup = await self._setup_work_items(project.id)
            result["work_item_types"] = work_item_setup
            
            # 5. Create default pipelines if requested
            if setup_default_pipelines and result["repositories"]:
                pipeline_setup = await self._setup_default_pipelines(
                    project.id,
                    result["repositories"][0].id
                )
                result["pipelines"] = pipeline_setup
            
        except Exception as e:
            result["errors"].append(f"Project creation failed: {str(e)}")
        
        return result
    
    async def clone_project_structure(
        self,
        source_project_id: str,
        new_project_name: str,
        include_repositories: bool = True,
        include_work_items: bool = False,
        include_pipelines: bool = True,
        include_teams: bool = True
    ) -> Dict[str, Any]:
        """
        Clone the structure of an existing project to create a new one.
        
        Args:
            source_project_id: Source project to clone from
            new_project_name: Name for the new project
            include_repositories: Clone repository structure
            include_work_items: Clone work item configuration
            include_pipelines: Clone pipeline definitions
            include_teams: Clone team structure
            
        Returns:
            Cloning operation result
        """
        result = {
            "source_project": None,
            "new_project": None,
            "cloned_elements": {},
            "errors": []
        }
        
        try:
            # Get source project details
            source_project = await self.core.get_project(source_project_id)
            result["source_project"] = source_project
            
            # Create new project with same template
            project_data = {
                "name": new_project_name,
                "description": f"Cloned from {source_project.name}",
                "visibility": source_project.visibility,
                "capabilities": source_project.capabilities
            }
            
            new_project = await self.core.create_project(project_data)
            result["new_project"] = new_project
            
            await self._wait_for_project_creation(new_project.id)
            
            # Clone repositories
            if include_repositories:
                repos_result = await self._clone_repositories(
                    source_project_id,
                    new_project.id
                )
                result["cloned_elements"]["repositories"] = repos_result
            
            # Clone teams
            if include_teams:
                teams_result = await self._clone_teams(
                    source_project_id,
                    new_project.id
                )
                result["cloned_elements"]["teams"] = teams_result
            
            # Clone pipelines
            if include_pipelines:
                pipelines_result = await self._clone_pipelines(
                    source_project_id,
                    new_project.id
                )
                result["cloned_elements"]["pipelines"] = pipelines_result
            
            # Clone work item configuration
            if include_work_items:
                wi_result = await self._clone_work_item_config(
                    source_project_id,
                    new_project.id
                )
                result["cloned_elements"]["work_items"] = wi_result
            
        except Exception as e:
            result["errors"].append(f"Project cloning failed: {str(e)}")
        
        return result
    
    async def setup_project_governance(
        self,
        project_id: str,
        governance_policies: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Set up comprehensive governance policies for a project.
        
        Args:
            project_id: Project ID
            governance_policies: Governance configuration
            
        Returns:
            Governance setup result
        """
        result = {
            "branch_policies": [],
            "security_policies": {},
            "work_item_policies": {},
            "build_policies": {},
            "errors": []
        }
        
        try:
            # Set up branch policies
            if "branch_policies" in governance_policies:
                branch_result = await self._setup_branch_policies(
                    project_id,
                    governance_policies["branch_policies"]
                )
                result["branch_policies"] = branch_result
            
            # Set up security policies
            if "security_policies" in governance_policies:
                security_result = await self._setup_security_policies(
                    project_id,
                    governance_policies["security_policies"]
                )
                result["security_policies"] = security_result
            
            # Set up work item policies
            if "work_item_policies" in governance_policies:
                wi_result = await self._setup_work_item_policies(
                    project_id,
                    governance_policies["work_item_policies"]
                )
                result["work_item_policies"] = wi_result
            
            # Set up build policies
            if "build_policies" in governance_policies:
                build_result = await self._setup_build_policies(
                    project_id,
                    governance_policies["build_policies"]
                )
                result["build_policies"] = build_result
            
        except Exception as e:
            result["errors"].append(f"Governance setup failed: {str(e)}")
        
        return result
    
    async def onboard_team_to_project(
        self,
        project_id: str,
        team_name: str,
        team_members: List[str],
        team_lead: str,
        permissions: Optional[Dict[str, List[str]]] = None,
        repositories: Optional[List[str]] = None,
        area_paths: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Complete team onboarding to a project.
        
        Args:
            project_id: Project ID
            team_name: Team name
            team_members: List of team member emails
            team_lead: Team lead email
            permissions: Custom permissions for the team
            repositories: Repositories to grant access to
            area_paths: Area paths to assign to the team
            
        Returns:
            Team onboarding result
        """
        result = {
            "team": None,
            "members_added": [],
            "permissions_set": {},
            "area_paths_created": [],
            "errors": []
        }
        
        try:
            # Create team
            team_data = {
                "name": team_name,
                "description": f"Team {team_name}"
            }
            team = await self.core.create_team(project_id, team_data)
            result["team"] = team
            
            # Add team members
            for member_email in team_members:
                try:
                    # Find user
                    user = await self.graph.find_user_by_email(member_email)
                    if user:
                        await self.core.add_team_member(
                            project_id,
                            team.id,
                            user.descriptor
                        )
                        result["members_added"].append(member_email)
                except Exception as e:
                    result["errors"].append(f"Failed to add member {member_email}: {str(e)}")
            
            # Set team lead
            try:
                lead_user = await self.graph.find_user_by_email(team_lead)
                if lead_user:
                    # Add lead as team admin
                    await self.core.add_team_member(
                        project_id,
                        team.id,
                        lead_user.descriptor,
                        is_team_admin=True
                    )
            except Exception as e:
                result["errors"].append(f"Failed to set team lead {team_lead}: {str(e)}")
            
            # Set up area paths
            if area_paths:
                for area_path in area_paths:
                    try:
                        area = await self.work_items.create_classification_node(
                            project_id,
                            "areas",
                            {"name": area_path}
                        )
                        result["area_paths_created"].append(area)
                    except Exception as e:
                        result["errors"].append(f"Failed to create area path {area_path}: {str(e)}")
            
            # Set repository permissions
            if repositories:
                repo_permissions = await self._setup_team_repository_permissions(
                    project_id,
                    team.id,
                    repositories,
                    permissions
                )
                result["permissions_set"]["repositories"] = repo_permissions
            
        except Exception as e:
            result["errors"].append(f"Team onboarding failed: {str(e)}")
        
        return result
    
    async def get_project_health_report(
        self,
        project_id: str,
        include_metrics: bool = True,
        include_security: bool = True,
        include_compliance: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive project health report.
        
        Args:
            project_id: Project ID
            include_metrics: Include performance metrics
            include_security: Include security analysis
            include_compliance: Include compliance checks
            
        Returns:
            Project health report
        """
        report = {
            "project_id": project_id,
            "generated_at": datetime.utcnow().isoformat(),
            "overall_health": "unknown",
            "summary": {},
            "details": {},
            "recommendations": [],
            "errors": []
        }
        
        try:
            # Get project details
            project = await self.core.get_project(project_id)
            report["summary"]["project"] = {
                "name": project.name,
                "state": project.state,
                "visibility": project.visibility
            }
            
            # Repository analysis
            repositories = await self.git.list_repositories(project_id)
            repo_health = await self._analyze_repository_health(repositories)
            report["details"]["repositories"] = repo_health
            
            # Work item analysis
            if include_metrics:
                wi_metrics = await self._analyze_work_item_metrics(project_id)
                report["details"]["work_items"] = wi_metrics
            
            # Build/Pipeline analysis
            if include_metrics:
                pipeline_metrics = await self._analyze_pipeline_health(project_id)
                report["details"]["pipelines"] = pipeline_metrics
            
            # Security analysis
            if include_security:
                security_analysis = await self._analyze_project_security(project_id)
                report["details"]["security"] = security_analysis
            
            # Generate overall health score
            health_score = self._calculate_health_score(report["details"])
            report["overall_health"] = health_score["status"]
            report["summary"]["score"] = health_score["score"]
            report["recommendations"] = health_score["recommendations"]
            
        except Exception as e:
            report["errors"].append(f"Health report generation failed: {str(e)}")
        
        return report
    
    # Helper methods
    async def _wait_for_project_creation(
        self,
        project_id: str,
        max_wait_seconds: int = 60
    ) -> bool:
        """Wait for project creation to complete."""
        import asyncio
        
        for _ in range(max_wait_seconds):
            try:
                project = await self.core.get_project(project_id)
                if project.state == "wellFormed":
                    return True
            except:
                pass
            await asyncio.sleep(1)
        
        return False
    
    async def _setup_project_security(
        self,
        project_id: str,
        team_members: List[str],
        project_admins: List[str]
    ) -> Dict[str, Any]:
        """Set up initial project security."""
        security_result = {
            "team_members_added": [],
            "admins_added": [],
            "errors": []
        }
        
        # Add team members
        for member_email in team_members:
            try:
                user = await self.graph.find_user_by_email(member_email)
                if user:
                    # Add to Contributors group
                    contributors_group = await self.graph.find_group_by_name(
                        "Contributors",
                        scope_descriptor=f"project:{project_id}"
                    )
                    if contributors_group:
                        await self.graph.add_user_to_group(
                            user.descriptor,
                            contributors_group.descriptor
                        )
                        security_result["team_members_added"].append(member_email)
            except Exception as e:
                security_result["errors"].append(f"Failed to add member {member_email}: {str(e)}")
        
        # Add project admins
        for admin_email in project_admins:
            try:
                user = await self.graph.find_user_by_email(admin_email)
                if user:
                    # Add to Project Administrators group
                    admins_group = await self.graph.find_group_by_name(
                        "Project Administrators",
                        scope_descriptor=f"project:{project_id}"
                    )
                    if admins_group:
                        await self.graph.add_user_to_group(
                            user.descriptor,
                            admins_group.descriptor
                        )
                        security_result["admins_added"].append(admin_email)
            except Exception as e:
                security_result["errors"].append(f"Failed to add admin {admin_email}: {str(e)}")
        
        return security_result
    
    async def _setup_work_items(self, project_id: str) -> List[WorkItemType]:
        """Set up initial work item configuration."""
        try:
            # Get available work item types
            work_item_types = await self.work_items.list_work_item_types(project_id)
            
            # Create default area and iteration paths
            await self.work_items.create_classification_node(
                project_id,
                "areas",
                {"name": "Development"}
            )
            
            await self.work_items.create_classification_node(
                project_id,
                "iterations",
                {"name": "Sprint 1"}
            )
            
            return work_item_types
        except Exception:
            return []
    
    async def _setup_default_pipelines(
        self,
        project_id: str,
        repository_id: str
    ) -> List[Dict[str, Any]]:
        """Set up default CI/CD pipelines."""
        pipelines_created = []
        
        try:
            # Create a basic CI pipeline
            ci_pipeline_yaml = """
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: DotNetCoreCLI@2
  displayName: 'Build'
  inputs:
    command: 'build'
    projects: '**/*.csproj'
"""
            
            # Create CI pipeline
            ci_pipeline = await self.pipelines.create_pipeline(
                project_id,
                {
                    "name": "CI-Pipeline",
                    "repository": {
                        "id": repository_id,
                        "type": "azureReposGit"
                    },
                    "path": "/.azure-pipelines/ci.yml"
                }
            )
            pipelines_created.append({"type": "CI", "pipeline": ci_pipeline})
            
        except Exception as e:
            pipelines_created.append({"type": "CI", "error": str(e)})
        
        return pipelines_created
    
    async def _clone_repositories(
        self,
        source_project_id: str,
        target_project_id: str
    ) -> List[Dict[str, Any]]:
        """Clone repository structure between projects."""
        cloned_repos = []
        
        try:
            source_repos = await self.git.list_repositories(source_project_id)
            
            for repo in source_repos:
                try:
                    new_repo = await self.git.create_repository(
                        target_project_id,
                        {"name": repo.name}
                    )
                    cloned_repos.append({
                        "source": repo.name,
                        "target": new_repo.name,
                        "success": True
                    })
                except Exception as e:
                    cloned_repos.append({
                        "source": repo.name,
                        "success": False,
                        "error": str(e)
                    })
        except Exception:
            pass
        
        return cloned_repos
    
    async def _clone_teams(
        self,
        source_project_id: str,
        target_project_id: str
    ) -> List[Dict[str, Any]]:
        """Clone team structure between projects."""
        cloned_teams = []
        
        try:
            source_teams = await self.core.list_teams(source_project_id)
            
            for team in source_teams:
                if team.name != source_project_id:  # Skip default team
                    try:
                        new_team = await self.core.create_team(
                            target_project_id,
                            {
                                "name": team.name,
                                "description": team.description
                            }
                        )
                        cloned_teams.append({
                            "source": team.name,
                            "target": new_team.name,
                            "success": True
                        })
                    except Exception as e:
                        cloned_teams.append({
                            "source": team.name,
                            "success": False,
                            "error": str(e)
                        })
        except Exception:
            pass
        
        return cloned_teams
    
    async def _clone_pipelines(
        self,
        source_project_id: str,
        target_project_id: str
    ) -> List[Dict[str, Any]]:
        """Clone pipeline definitions between projects."""
        cloned_pipelines = []
        
        try:
            # Get build definitions
            build_definitions = await self.build.list_definitions(source_project_id)
            
            for definition in build_definitions:
                try:
                    # This would require more complex logic to clone build definitions
                    # For now, just track what we would clone
                    cloned_pipelines.append({
                        "source": definition.name,
                        "type": "build",
                        "success": False,
                        "note": "Build definition cloning requires complex implementation"
                    })
                except Exception as e:
                    cloned_pipelines.append({
                        "source": definition.name,
                        "type": "build",
                        "success": False,
                        "error": str(e)
                    })
        except Exception:
            pass
        
        return cloned_pipelines
    
    async def _clone_work_item_config(
        self,
        source_project_id: str,
        target_project_id: str
    ) -> Dict[str, Any]:
        """Clone work item configuration between projects."""
        return {
            "areas_cloned": [],
            "iterations_cloned": [],
            "note": "Work item configuration cloning requires process template modification"
        }
    
    async def _setup_branch_policies(
        self,
        project_id: str,
        policies: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up branch policies for repositories."""
        policies_created = []
        
        try:
            repositories = await self.git.list_repositories(project_id)
            
            for repo in repositories:
                if "require_pull_request" in policies:
                    # Create pull request policy for main branch
                    policy_data = {
                        "type": "fa4e907d-c16b-4a4c-9dfa-4906e5d171dd",  # Pull request policy
                        "isEnabled": True,
                        "isBlocking": True,
                        "settings": {
                            "minimumApproverCount": policies.get("min_reviewers", 1),
                            "creatorVoteCounts": False,
                            "scope": [
                                {
                                    "repositoryId": repo.id,
                                    "refName": "refs/heads/main",
                                    "matchKind": "exact"
                                }
                            ]
                        }
                    }
                    
                    try:
                        policy = await self.git.create_policy(project_id, policy_data)
                        policies_created.append({
                            "repository": repo.name,
                            "type": "pull_request",
                            "policy": policy,
                            "success": True
                        })
                    except Exception as e:
                        policies_created.append({
                            "repository": repo.name,
                            "type": "pull_request",
                            "success": False,
                            "error": str(e)
                        })
        except Exception:
            pass
        
        return policies_created
    
    async def _setup_security_policies(
        self,
        project_id: str,
        policies: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Set up security policies."""
        return {
            "note": "Security policy setup requires detailed ACL configuration",
            "policies_requested": list(policies.keys())
        }
    
    async def _setup_work_item_policies(
        self,
        project_id: str,
        policies: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Set up work item policies."""
        return {
            "note": "Work item policy setup requires process template customization",
            "policies_requested": list(policies.keys())
        }
    
    async def _setup_build_policies(
        self,
        project_id: str,
        policies: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Set up build policies."""
        return {
            "note": "Build policy setup requires pipeline definition modification",
            "policies_requested": list(policies.keys())
        }
    
    async def _setup_team_repository_permissions(
        self,
        project_id: str,
        team_id: str,
        repositories: List[str],
        permissions: Optional[Dict[str, List[str]]]
    ) -> Dict[str, Any]:
        """Set up team repository permissions."""
        return {
            "team_id": team_id,
            "repositories": repositories,
            "note": "Repository permission setup requires detailed ACL configuration"
        }
    
    async def _analyze_repository_health(
        self,
        repositories: List[GitRepository]
    ) -> Dict[str, Any]:
        """Analyze repository health metrics."""
        return {
            "total_repositories": len(repositories),
            "active_repositories": len([r for r in repositories if hasattr(r, 'size') and r.size > 0]),
            "empty_repositories": len([r for r in repositories if not hasattr(r, 'size') or r.size == 0]),
            "note": "Detailed repository analysis requires commit and branch data"
        }
    
    async def _analyze_work_item_metrics(self, project_id: str) -> Dict[str, Any]:
        """Analyze work item metrics."""
        try:
            # Get basic work item counts
            work_items = await self.work_items.query_by_wiql(
                project_id,
                {"query": "SELECT [System.Id] FROM WorkItems"}
            )
            
            return {
                "total_work_items": len(work_items.work_items) if work_items else 0,
                "note": "Detailed work item analysis requires state and type breakdown"
            }
        except Exception:
            return {
                "total_work_items": 0,
                "error": "Could not retrieve work item metrics"
            }
    
    async def _analyze_pipeline_health(self, project_id: str) -> Dict[str, Any]:
        """Analyze pipeline health metrics."""
        try:
            definitions = await self.build.list_definitions(project_id)
            
            return {
                "total_build_definitions": len(definitions),
                "note": "Detailed pipeline analysis requires build history data"
            }
        except Exception:
            return {
                "total_build_definitions": 0,
                "error": "Could not retrieve pipeline metrics"
            }
    
    async def _analyze_project_security(self, project_id: str) -> Dict[str, Any]:
        """Analyze project security configuration."""
        return {
            "note": "Security analysis requires detailed permission enumeration",
            "project_id": project_id
        }
    
    def _calculate_health_score(self, details: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall project health score."""
        score = 75  # Base score
        recommendations = []
        
        # Repository analysis
        if "repositories" in details:
            repo_data = details["repositories"]
            if repo_data.get("empty_repositories", 0) > 0:
                recommendations.append("Consider removing or populating empty repositories")
                score -= 5
        
        # Determine health status
        if score >= 90:
            status = "excellent"
        elif score >= 75:
            status = "good"
        elif score >= 60:
            status = "fair"
        else:
            status = "poor"
        
        return {
            "score": score,
            "status": status,
            "recommendations": recommendations
        }
