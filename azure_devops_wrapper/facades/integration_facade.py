"""
Integration Facade - High-level integration and automation operations.

This facade combines service hooks, notifications, and extensions to provide
comprehensive integration management and workflow automation.
"""

from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta
from ..services import (
    ServiceHooksService, NotificationService, ExtensionsService,
    CoreService, GitService, BuildService, PipelinesService
)
from ..models import (
    ServiceHookSubscription, NotificationSubscription, Extension,
    Project, GitRepository, BuildDefinition, Pipeline
)


class IntegrationFacade:
    """High-level facade for comprehensive integration and automation operations."""
    
    def __init__(
        self,
        service_hooks_service: ServiceHooksService,
        notification_service: NotificationService,
        extensions_service: ExtensionsService,
        core_service: CoreService,
        git_service: GitService,
        build_service: BuildService,
        pipelines_service: PipelinesService
    ):
        self.service_hooks = service_hooks_service
        self.notification = notification_service
        self.extensions = extensions_service
        self.core = core_service
        self.git = git_service
        self.build = build_service
        self.pipelines = pipelines_service
    
    async def setup_complete_devops_integration(
        self,
        project_id: str,
        integration_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Set up complete DevOps integration ecosystem.
        
        Args:
            project_id: Project ID
            integration_config: Integration configuration
            
        Returns:
            Complete integration setup result
        """
        result = {
            "project_id": project_id,
            "chat_integrations": [],
            "issue_tracking_integrations": [],
            "monitoring_integrations": [],
            "ci_cd_integrations": [],
            "notification_channels": [],
            "automation_workflows": [],
            "dashboard_integrations": [],
            "errors": []
        }
        
        try:
            # 1. Set up chat integrations (Slack, Teams, Discord)
            if "chat_integrations" in integration_config:
                chat_integrations = await self._setup_chat_integrations(
                    project_id,
                    integration_config["chat_integrations"]
                )
                result["chat_integrations"] = chat_integrations
            
            # 2. Set up issue tracking integrations (Jira, GitHub Issues)
            if "issue_tracking" in integration_config:
                issue_integrations = await self._setup_issue_tracking_integrations(
                    project_id,
                    integration_config["issue_tracking"]
                )
                result["issue_tracking_integrations"] = issue_integrations
            
            # 3. Set up monitoring and observability integrations
            if "monitoring" in integration_config:
                monitoring_integrations = await self._setup_monitoring_integrations(
                    project_id,
                    integration_config["monitoring"]
                )
                result["monitoring_integrations"] = monitoring_integrations
            
            # 4. Set up CI/CD tool integrations
            if "ci_cd_tools" in integration_config:
                cicd_integrations = await self._setup_cicd_integrations(
                    project_id,
                    integration_config["ci_cd_tools"]
                )
                result["ci_cd_integrations"] = cicd_integrations
            
            # 5. Configure notification channels
            if "notifications" in integration_config:
                notification_channels = await self._setup_notification_channels(
                    project_id,
                    integration_config["notifications"]
                )
                result["notification_channels"] = notification_channels
            
            # 6. Set up automation workflows
            if "automation" in integration_config:
                automation_workflows = await self._setup_automation_workflows(
                    project_id,
                    integration_config["automation"]
                )
                result["automation_workflows"] = automation_workflows
            
            # 7. Configure dashboard integrations
            if "dashboards" in integration_config:
                dashboard_integrations = await self._setup_dashboard_integrations(
                    project_id,
                    integration_config["dashboards"]
                )
                result["dashboard_integrations"] = dashboard_integrations
            
        except Exception as e:
            result["errors"].append(f"DevOps integration setup failed: {str(e)}")
        
        return result
    
    async def implement_gitops_automation(
        self,
        project_id: str,
        gitops_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Implement comprehensive GitOps automation workflows.
        
        Args:
            project_id: Project ID
            gitops_config: GitOps configuration
            
        Returns:
            GitOps automation implementation result
        """
        result = {
            "config_repositories": [],
            "sync_workflows": [],
            "deployment_automations": [],
            "rollback_mechanisms": [],
            "monitoring_integrations": [],
            "compliance_checks": [],
            "errors": []
        }
        
        try:
            # 1. Set up configuration repositories
            config_repos = await self._setup_gitops_config_repositories(
                project_id,
                gitops_config.get("config_repositories", [])
            )
            result["config_repositories"] = config_repos
            
            # 2. Implement sync workflows
            sync_workflows = await self._implement_gitops_sync_workflows(
                project_id,
                gitops_config.get("sync_config", {})
            )
            result["sync_workflows"] = sync_workflows
            
            # 3. Set up automated deployments
            deployment_automations = await self._setup_gitops_deployment_automation(
                project_id,
                gitops_config.get("deployment_config", {})
            )
            result["deployment_automations"] = deployment_automations
            
            # 4. Implement rollback mechanisms
            rollback_mechanisms = await self._implement_gitops_rollback_mechanisms(
                project_id,
                gitops_config.get("rollback_config", {})
            )
            result["rollback_mechanisms"] = rollback_mechanisms
            
            # 5. Set up monitoring and alerting
            monitoring_integrations = await self._setup_gitops_monitoring(
                project_id,
                gitops_config.get("monitoring_config", {})
            )
            result["monitoring_integrations"] = monitoring_integrations
            
            # 6. Implement compliance checks
            compliance_checks = await self._implement_gitops_compliance_checks(
                project_id,
                gitops_config.get("compliance_config", {})
            )
            result["compliance_checks"] = compliance_checks
            
        except Exception as e:
            result["errors"].append(f"GitOps automation implementation failed: {str(e)}")
        
        return result
    
    async def setup_cross_platform_integration(
        self,
        integration_matrix: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Set up cross-platform integrations across multiple systems.
        
        Args:
            integration_matrix: Matrix of platform integrations
            
        Returns:
            Cross-platform integration result
        """
        result = {
            "platform_connections": {},
            "data_sync_workflows": [],
            "unified_notifications": [],
            "cross_platform_automations": [],
            "monitoring_dashboards": [],
            "errors": []
        }
        
        try:
            # Process each platform integration
            for platform, config in integration_matrix.items():
                platform_result = await self._setup_platform_integration(platform, config)
                result["platform_connections"][platform] = platform_result
            
            # Set up data synchronization workflows
            if "data_sync" in integration_matrix:
                data_sync = await self._setup_cross_platform_data_sync(
                    integration_matrix["data_sync"]
                )
                result["data_sync_workflows"] = data_sync
            
            # Configure unified notifications
            unified_notifications = await self._setup_unified_notification_system(
                integration_matrix
            )
            result["unified_notifications"] = unified_notifications
            
            # Implement cross-platform automations
            automations = await self._implement_cross_platform_automations(
                integration_matrix
            )
            result["cross_platform_automations"] = automations
            
            # Set up monitoring dashboards
            dashboards = await self._setup_cross_platform_monitoring(
                integration_matrix
            )
            result["monitoring_dashboards"] = dashboards
            
        except Exception as e:
            result["errors"].append(f"Cross-platform integration failed: {str(e)}")
        
        return result
    
    async def implement_event_driven_automation(
        self,
        project_id: str,
        automation_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Implement comprehensive event-driven automation.
        
        Args:
            project_id: Project ID
            automation_config: Automation configuration
            
        Returns:
            Event-driven automation implementation result
        """
        result = {
            "event_subscriptions": [],
            "automation_rules": [],
            "workflow_triggers": [],
            "conditional_actions": [],
            "escalation_policies": [],
            "monitoring_setup": {},
            "errors": []
        }
        
        try:
            # 1. Set up event subscriptions
            event_subscriptions = await self._setup_event_subscriptions(
                project_id,
                automation_config.get("events", [])
            )
            result["event_subscriptions"] = event_subscriptions
            
            # 2. Create automation rules
            automation_rules = await self._create_automation_rules(
                project_id,
                automation_config.get("rules", [])
            )
            result["automation_rules"] = automation_rules
            
            # 3. Set up workflow triggers
            workflow_triggers = await self._setup_workflow_triggers(
                project_id,
                automation_config.get("triggers", [])
            )
            result["workflow_triggers"] = workflow_triggers
            
            # 4. Implement conditional actions
            conditional_actions = await self._implement_conditional_actions(
                project_id,
                automation_config.get("conditions", [])
            )
            result["conditional_actions"] = conditional_actions
            
            # 5. Set up escalation policies
            escalation_policies = await self._setup_escalation_policies(
                project_id,
                automation_config.get("escalations", [])
            )
            result["escalation_policies"] = escalation_policies
            
            # 6. Configure monitoring
            monitoring_setup = await self._setup_automation_monitoring(
                project_id,
                automation_config.get("monitoring", {})
            )
            result["monitoring_setup"] = monitoring_setup
            
        except Exception as e:
            result["errors"].append(f"Event-driven automation implementation failed: {str(e)}")
        
        return result
    
    async def setup_integration_marketplace(
        self,
        marketplace_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Set up integration marketplace with approved tools and workflows.
        
        Args:
            marketplace_config: Marketplace configuration
            
        Returns:
            Integration marketplace setup result
        """
        result = {
            "approved_integrations": [],
            "integration_templates": [],
            "self_service_portal": {},
            "governance_policies": {},
            "usage_analytics": {},
            "support_workflows": [],
            "errors": []
        }
        
        try:
            # 1. Define approved integrations catalog
            approved_integrations = await self._define_approved_integrations(
                marketplace_config.get("approved_tools", [])
            )
            result["approved_integrations"] = approved_integrations
            
            # 2. Create integration templates
            integration_templates = await self._create_integration_templates(
                marketplace_config.get("templates", [])
            )
            result["integration_templates"] = integration_templates
            
            # 3. Set up self-service portal
            self_service_portal = await self._setup_self_service_integration_portal(
                marketplace_config.get("portal_config", {})
            )
            result["self_service_portal"] = self_service_portal
            
            # 4. Implement governance policies
            governance_policies = await self._implement_integration_governance(
                marketplace_config.get("governance", {})
            )
            result["governance_policies"] = governance_policies
            
            # 5. Set up usage analytics
            usage_analytics = await self._setup_integration_usage_analytics(
                marketplace_config.get("analytics", {})
            )
            result["usage_analytics"] = usage_analytics
            
            # 6. Configure support workflows
            support_workflows = await self._setup_integration_support_workflows(
                marketplace_config.get("support", {})
            )
            result["support_workflows"] = support_workflows
            
        except Exception as e:
            result["errors"].append(f"Integration marketplace setup failed: {str(e)}")
        
        return result
    
    async def analyze_integration_health(
        self,
        project_id: Optional[str] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze health and performance of all integrations.
        
        Args:
            project_id: Project ID (optional, for organization-wide analysis)
            days: Number of days to analyze
            
        Returns:
            Integration health analysis
        """
        analysis = {
            "analysis_period": f"{days} days",
            "overall_health": "unknown",
            "service_hooks_health": {},
            "notification_health": {},
            "extension_health": {},
            "integration_metrics": {},
            "performance_trends": {},
            "failure_analysis": {},
            "recommendations": [],
            "errors": []
        }
        
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # 1. Analyze service hooks health
            service_hooks_health = await self._analyze_service_hooks_health(
                project_id,
                start_date,
                end_date
            )
            analysis["service_hooks_health"] = service_hooks_health
            
            # 2. Analyze notification system health
            notification_health = await self._analyze_notification_health(
                project_id,
                start_date,
                end_date
            )
            analysis["notification_health"] = notification_health
            
            # 3. Analyze extension ecosystem health
            extension_health = await self._analyze_extension_health(project_id)
            analysis["extension_health"] = extension_health
            
            # 4. Calculate integration metrics
            integration_metrics = await self._calculate_integration_metrics(
                service_hooks_health,
                notification_health,
                extension_health
            )
            analysis["integration_metrics"] = integration_metrics
            
            # 5. Generate performance trends
            performance_trends = await self._generate_integration_performance_trends(
                project_id,
                start_date,
                end_date
            )
            analysis["performance_trends"] = performance_trends
            
            # 6. Analyze failures
            failure_analysis = await self._analyze_integration_failures(
                project_id,
                start_date,
                end_date
            )
            analysis["failure_analysis"] = failure_analysis
            
            # 7. Calculate overall health
            overall_health = self._calculate_overall_integration_health(analysis)
            analysis["overall_health"] = overall_health
            
            # 8. Generate recommendations
            recommendations = self._generate_integration_recommendations(analysis)
            analysis["recommendations"] = recommendations
            
        except Exception as e:
            analysis["errors"].append(f"Integration health analysis failed: {str(e)}")
        
        return analysis
    
    # Helper methods
    async def _setup_chat_integrations(
        self,
        project_id: str,
        chat_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up chat platform integrations."""
        integrations = []
        
        # Slack integration
        if "slack" in chat_config:
            slack_config = chat_config["slack"]
            for channel_config in slack_config.get("channels", []):
                try:
                    slack_subscription = await self.service_hooks.create_slack_subscription(
                        webhook_url=channel_config["webhook_url"],
                        event_type="ms.vss-build.build-status-changed-event",
                        channel=channel_config.get("channel")
                    )
                    integrations.append({
                        "platform": "slack",
                        "channel": channel_config.get("channel"),
                        "subscription": slack_subscription,
                        "success": True
                    })
                except Exception as e:
                    integrations.append({
                        "platform": "slack",
                        "channel": channel_config.get("channel"),
                        "success": False,
                        "error": str(e)
                    })
        
        # Microsoft Teams integration
        if "teams" in chat_config:
            teams_config = chat_config["teams"]
            for channel_config in teams_config.get("channels", []):
                try:
                    teams_subscription = await self.service_hooks.create_teams_subscription(
                        webhook_url=channel_config["webhook_url"],
                        event_type="ms.vss-build.build-status-changed-event"
                    )
                    integrations.append({
                        "platform": "teams",
                        "channel": channel_config.get("name"),
                        "subscription": teams_subscription,
                        "success": True
                    })
                except Exception as e:
                    integrations.append({
                        "platform": "teams",
                        "channel": channel_config.get("name"),
                        "success": False,
                        "error": str(e)
                    })
        
        return integrations
    
    async def _setup_issue_tracking_integrations(
        self,
        project_id: str,
        issue_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up issue tracking integrations."""
        integrations = []
        
        # Jira integration
        if "jira" in issue_config:
            jira_config = issue_config["jira"]
            try:
                # Create webhook for Jira integration
                jira_webhook = await self.service_hooks.create_webhook_subscription(
                    webhook_url=jira_config["webhook_url"],
                    event_type="ms.vss-work.workitem-changed-event",
                    secret=jira_config.get("secret")
                )
                integrations.append({
                    "platform": "jira",
                    "webhook": jira_webhook,
                    "success": True
                })
            except Exception as e:
                integrations.append({
                    "platform": "jira",
                    "success": False,
                    "error": str(e)
                })
        
        # GitHub Issues integration
        if "github_issues" in issue_config:
            github_config = issue_config["github_issues"]
            try:
                github_webhook = await self.service_hooks.create_webhook_subscription(
                    webhook_url=github_config["webhook_url"],
                    event_type="ms.vss-work.workitem-changed-event",
                    secret=github_config.get("secret")
                )
                integrations.append({
                    "platform": "github_issues",
                    "webhook": github_webhook,
                    "success": True
                })
            except Exception as e:
                integrations.append({
                    "platform": "github_issues",
                    "success": False,
                    "error": str(e)
                })
        
        return integrations
    
    async def _setup_monitoring_integrations(
        self,
        project_id: str,
        monitoring_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up monitoring and observability integrations."""
        integrations = []
        
        # Application Insights integration
        if "app_insights" in monitoring_config:
            app_insights_config = monitoring_config["app_insights"]
            try:
                # This would integrate with Application Insights
                integrations.append({
                    "platform": "application_insights",
                    "configured": True,
                    "note": "Application Insights integration would be implemented here"
                })
            except Exception as e:
                integrations.append({
                    "platform": "application_insights",
                    "success": False,
                    "error": str(e)
                })
        
        # Datadog integration
        if "datadog" in monitoring_config:
            datadog_config = monitoring_config["datadog"]
            try:
                datadog_webhook = await self.service_hooks.create_webhook_subscription(
                    webhook_url=datadog_config["webhook_url"],
                    event_type="ms.vss-release.deployment-completed-event",
                    secret=datadog_config.get("api_key")
                )
                integrations.append({
                    "platform": "datadog",
                    "webhook": datadog_webhook,
                    "success": True
                })
            except Exception as e:
                integrations.append({
                    "platform": "datadog",
                    "success": False,
                    "error": str(e)
                })
        
        return integrations
    
    async def _setup_cicd_integrations(
        self,
        project_id: str,
        cicd_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up CI/CD tool integrations."""
        integrations = []
        
        # Jenkins integration
        if "jenkins" in cicd_config:
            jenkins_config = cicd_config["jenkins"]
            try:
                jenkins_webhook = await self.service_hooks.create_webhook_subscription(
                    webhook_url=jenkins_config["webhook_url"],
                    event_type="ms.vss-code.git-push-event",
                    secret=jenkins_config.get("token")
                )
                integrations.append({
                    "platform": "jenkins",
                    "webhook": jenkins_webhook,
                    "success": True
                })
            except Exception as e:
                integrations.append({
                    "platform": "jenkins",
                    "success": False,
                    "error": str(e)
                })
        
        # GitHub Actions integration
        if "github_actions" in cicd_config:
            github_config = cicd_config["github_actions"]
            try:
                github_webhook = await self.service_hooks.create_webhook_subscription(
                    webhook_url=github_config["webhook_url"],
                    event_type="ms.vss-code.git-push-event",
                    secret=github_config.get("secret")
                )
                integrations.append({
                    "platform": "github_actions",
                    "webhook": github_webhook,
                    "success": True
                })
            except Exception as e:
                integrations.append({
                    "platform": "github_actions",
                    "success": False,
                    "error": str(e)
                })
        
        return integrations
    
    async def _setup_notification_channels(
        self,
        project_id: str,
        notification_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up notification channels."""
        channels = []
        
        # Email notifications
        if "email" in notification_config:
            email_config = notification_config["email"]
            for subscription_config in email_config.get("subscriptions", []):
                try:
                    email_subscription = await self.notification.create_email_subscription(
                        email_addresses=subscription_config["recipients"],
                        event_type=subscription_config["event_type"]
                    )
                    channels.append({
                        "type": "email",
                        "subscription": email_subscription,
                        "success": True
                    })
                except Exception as e:
                    channels.append({
                        "type": "email",
                        "success": False,
                        "error": str(e)
                    })
        
        return channels
    
    async def _setup_automation_workflows(
        self,
        project_id: str,
        automation_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up automation workflows."""
        workflows = []
        
        # Auto-merge workflows
        if "auto_merge" in automation_config:
            auto_merge_config = automation_config["auto_merge"]
            workflows.append({
                "type": "auto_merge",
                "configured": True,
                "note": "Auto-merge workflow would be implemented here"
            })
        
        # Auto-deployment workflows
        if "auto_deploy" in automation_config:
            auto_deploy_config = automation_config["auto_deploy"]
            workflows.append({
                "type": "auto_deploy",
                "configured": True,
                "note": "Auto-deployment workflow would be implemented here"
            })
        
        return workflows
    
    async def _setup_dashboard_integrations(
        self,
        project_id: str,
        dashboard_config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Set up dashboard integrations."""
        integrations = []
        
        # Power BI integration
        if "power_bi" in dashboard_config:
            power_bi_config = dashboard_config["power_bi"]
            integrations.append({
                "platform": "power_bi",
                "configured": True,
                "note": "Power BI integration would be implemented here"
            })
        
        # Grafana integration
        if "grafana" in dashboard_config:
            grafana_config = dashboard_config["grafana"]
            integrations.append({
                "platform": "grafana",
                "configured": True,
                "note": "Grafana integration would be implemented here"
            })
        
        return integrations
    
    # Additional helper methods would continue here...
    # (Implementing remaining methods with similar patterns)
    
    async def _analyze_service_hooks_health(
        self,
        project_id: Optional[str],
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Analyze service hooks health."""
        try:
            if project_id:
                summary = await self.service_hooks.get_service_hooks_summary(
                    days=(end_date - start_date).days
                )
            else:
                summary = await self.service_hooks.get_service_hooks_summary(
                    days=(end_date - start_date).days
                )
            
            return {
                "total_hooks": summary.get("total_subscriptions", 0),
                "success_rate": summary.get("success_rate", 0),
                "failed_deliveries": summary.get("failed_notifications", 0),
                "health_status": "healthy" if summary.get("success_rate", 0) > 0.9 else "degraded"
            }
        except Exception as e:
            return {
                "error": str(e),
                "health_status": "unknown"
            }
    
    async def _analyze_notification_health(
        self,
        project_id: Optional[str],
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Analyze notification system health."""
        try:
            summary = await self.notification.get_notification_summary(
                days=(end_date - start_date).days
            )
            
            return {
                "total_subscriptions": summary.get("total_subscriptions", 0),
                "delivery_success_rate": summary.get("delivery_success_rate", 0),
                "total_events": summary.get("total_events", 0),
                "health_status": "healthy" if summary.get("delivery_success_rate", 0) > 0.9 else "degraded"
            }
        except Exception as e:
            return {
                "error": str(e),
                "health_status": "unknown"
            }
    
    async def _analyze_extension_health(self, project_id: Optional[str]) -> Dict[str, Any]:
        """Analyze extension ecosystem health."""
        try:
            summary = await self.extensions.get_organization_extension_summary()
            
            return {
                "total_extensions": summary.get("total_installed", 0),
                "enabled_extensions": summary.get("enabled_count", 0),
                "disabled_extensions": summary.get("disabled_count", 0),
                "error_extensions": summary.get("error_count", 0),
                "health_status": "healthy" if summary.get("error_count", 0) == 0 else "degraded"
            }
        except Exception as e:
            return {
                "error": str(e),
                "health_status": "unknown"
            }
    
    def _calculate_overall_integration_health(self, analysis: Dict[str, Any]) -> str:
        """Calculate overall integration health."""
        health_scores = []
        
        # Service hooks health
        if analysis["service_hooks_health"].get("health_status") == "healthy":
            health_scores.append(100)
        elif analysis["service_hooks_health"].get("health_status") == "degraded":
            health_scores.append(60)
        else:
            health_scores.append(20)
        
        # Notification health
        if analysis["notification_health"].get("health_status") == "healthy":
            health_scores.append(100)
        elif analysis["notification_health"].get("health_status") == "degraded":
            health_scores.append(60)
        else:
            health_scores.append(20)
        
        # Extension health
        if analysis["extension_health"].get("health_status") == "healthy":
            health_scores.append(100)
        elif analysis["extension_health"].get("health_status") == "degraded":
            health_scores.append(60)
        else:
            health_scores.append(20)
        
        if not health_scores:
            return "unknown"
        
        avg_score = sum(health_scores) / len(health_scores)
        
        if avg_score >= 90:
            return "excellent"
        elif avg_score >= 75:
            return "good"
        elif avg_score >= 50:
            return "fair"
        else:
            return "poor"
    
    def _generate_integration_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate integration recommendations."""
        recommendations = []
        
        # Service hooks recommendations
        service_hooks_health = analysis.get("service_hooks_health", {})
        if service_hooks_health.get("success_rate", 0) < 0.9:
            recommendations.append("Review and fix failing service hook deliveries")
        
        # Notification recommendations
        notification_health = analysis.get("notification_health", {})
        if notification_health.get("delivery_success_rate", 0) < 0.9:
            recommendations.append("Investigate notification delivery issues")
        
        # Extension recommendations
        extension_health = analysis.get("extension_health", {})
        if extension_health.get("error_extensions", 0) > 0:
            recommendations.append("Address extension errors and update problematic extensions")
        
        return recommendations
