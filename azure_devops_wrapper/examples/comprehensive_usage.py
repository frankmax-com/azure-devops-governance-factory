"""
Azure DevOps Wrapper - Comprehensive Usage Examples

This script demonstrates the full capabilities of the Azure DevOps wrapper,
showcasing both low-level service usage and high-level business facades.
"""

import asyncio
from datetime import datetime, timedelta
from azure_devops_wrapper import AzureDevOpsClient, AuthConfig


async def main():
    """Main example function demonstrating comprehensive Azure DevOps wrapper usage."""
    
    # Initialize the client with Personal Access Token
    client = AzureDevOpsClient(
        organization="your-organization",
        auth_config=AuthConfig(
            auth_type="pat",
            personal_access_token="your-pat-token"
        )
    )
    
    try:
        # Test connection
        print("Testing connection to Azure DevOps...")
        connection_test = await client.test_connection()
        print(f"Connection Status: {connection_test['connection_status']}")
        print(f"Auth Status: {connection_test['auth_status']}")
        print(f"Response Time: {connection_test['response_time']}ms")
        
        if connection_test['connection_status'] != 'success':
            print("Connection failed. Please check your credentials and organization.")
            return
        
        # Example 1: High-Level Business Facades
        print("\n" + "="*60)
        print("HIGH-LEVEL BUSINESS FACADE EXAMPLES")
        print("="*60)
        
        # Project Management Facade
        print("\n1. Complete Project Setup")
        project_result = await client.facades.project.create_complete_project(
            project_name="Demo-Project",
            project_config={
                "description": "Demonstration project with complete setup",
                "source_control": "git",
                "work_item_process": "agile",
                "version_control": {
                    "repository_name": "main",
                    "initial_branch": "main"
                },
                "teams": [
                    {"name": "Development Team", "description": "Core development team"},
                    {"name": "QA Team", "description": "Quality assurance team"}
                ],
                "area_paths": ["Frontend", "Backend", "DevOps"],
                "iteration_paths": ["Sprint 1", "Sprint 2", "Sprint 3"]
            }
        )
        print(f"Project Creation: {project_result.get('success', False)}")
        if project_result.get('project'):
            print(f"Project ID: {project_result['project'].get('id')}")
        
        # Pipeline Management Facade
        print("\n2. Complete CI/CD Pipeline Setup")
        pipeline_result = await client.facades.pipeline.create_complete_cicd_pipeline(
            project_id=project_result.get('project', {}).get('id'),
            pipeline_config={
                "name": "Complete-CICD-Pipeline",
                "repository": {
                    "name": "main",
                    "branch": "main"
                },
                "build_stages": [
                    {
                        "name": "Build",
                        "tasks": ["restore", "build", "test", "publish"]
                    }
                ],
                "deployment_stages": [
                    {
                        "name": "Development",
                        "environment": "dev",
                        "approval_required": False
                    },
                    {
                        "name": "Production", 
                        "environment": "prod",
                        "approval_required": True
                    }
                ],
                "security_scanning": {
                    "enabled": True,
                    "tools": ["dependency_check", "code_analysis"]
                },
                "notifications": {
                    "email": ["team@company.com"],
                    "slack_webhook": "https://hooks.slack.com/your-webhook"
                }
            }
        )
        print(f"Pipeline Creation: {pipeline_result.get('success', False)}")
        
        # Security Governance Facade
        print("\n3. Zero-Trust Security Implementation")
        security_result = await client.facades.security.implement_zero_trust_security(
            security_config={
                "identity_verification": {
                    "mfa_required": True,
                    "conditional_access": True
                },
                "least_privilege": {
                    "enabled": True,
                    "review_period_days": 90
                },
                "continuous_monitoring": {
                    "enabled": True,
                    "alert_thresholds": {
                        "failed_logins": 5,
                        "privilege_escalation": 1
                    }
                },
                "data_protection": {
                    "encryption_required": True,
                    "data_classification": True
                }
            }
        )
        print(f"Security Implementation: {security_result.get('success', False)}")
        
        # Integration Management Facade
        print("\n4. DevOps Integration Setup")
        integration_result = await client.facades.integration.setup_complete_devops_integration(
            project_id=project_result.get('project', {}).get('id'),
            integration_config={
                "chat_integrations": {
                    "slack": {
                        "channels": [
                            {
                                "name": "dev-notifications",
                                "webhook_url": "https://hooks.slack.com/dev-webhook"
                            }
                        ]
                    }
                },
                "monitoring": {
                    "datadog": {
                        "webhook_url": "https://api.datadoghq.com/webhook",
                        "api_key": "your-datadog-key"
                    }
                },
                "ci_cd_tools": {
                    "github_actions": {
                        "webhook_url": "https://api.github.com/webhook",
                        "secret": "your-github-secret"
                    }
                }
            }
        )
        print(f"Integration Setup: {integration_result.get('success', 'unknown')}")
        
        # Governance Framework Facade
        print("\n5. Enterprise Governance Implementation")
        governance_result = await client.facades.governance.implement_enterprise_governance(
            governance_config={
                "organizational_policies": {
                    "security": [
                        {
                            "name": "Code Review Policy",
                            "description": "All code must be reviewed before merge",
                            "type": "mandatory"
                        }
                    ],
                    "compliance": [
                        {
                            "name": "SOX Compliance",
                            "description": "Sarbanes-Oxley compliance requirements",
                            "type": "regulatory"
                        }
                    ]
                },
                "compliance_framework": {
                    "standards": ["SOX", "SOC2", "ISO27001"],
                    "reporting_frequency": "monthly"
                },
                "risk_management": {
                    "enabled": True,
                    "assessment_frequency": "quarterly"
                }
            }
        )
        print(f"Governance Implementation: {governance_result.get('success', 'unknown')}")
        
        # Example 2: Low-Level Service Usage
        print("\n" + "="*60)
        print("LOW-LEVEL SERVICE EXAMPLES")
        print("="*60)
        
        # Core Service - Project Operations
        print("\n1. Project Operations")
        projects = await client.services.core.get_projects(top=5)
        print(f"Found {len(projects)} projects")
        for project in projects:
            print(f"  - {project.get('name')} (ID: {project.get('id')})")
        
        # Git Service - Repository Operations
        if projects:
            project_id = projects[0].get('id')
            print(f"\n2. Git Repository Operations for Project: {project_id}")
            
            repositories = await client.services.git.get_repositories(project_id)
            print(f"Found {len(repositories)} repositories")
            
            if repositories:
                repo_id = repositories[0].get('id')
                commits = await client.services.git.get_commits(
                    project_id=project_id,
                    repository_id=repo_id,
                    top=3
                )
                print(f"Recent commits: {len(commits)}")
        
        # Build Service - Build Operations
        print("\n3. Build Operations")
        builds = await client.services.build.get_builds(top=5)
        print(f"Found {len(builds)} builds")
        
        build_definitions = await client.services.build.get_build_definitions(top=3)
        print(f"Found {len(build_definitions)} build definitions")
        
        # Work Items Service
        print("\n4. Work Item Operations")
        work_items = await client.services.work_items.query_work_items(
            wiql="SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.State] = 'Active'"
        )
        print(f"Found {len(work_items.get('workItems', []))} active work items")
        
        # Example 3: Advanced Analytics and Reporting
        print("\n" + "="*60)
        print("ADVANCED ANALYTICS AND REPORTING")
        print("="*60)
        
        # Integration Health Analysis
        print("\n1. Integration Health Analysis")
        health_analysis = await client.facades.integration.analyze_integration_health(days=30)
        print(f"Overall Integration Health: {health_analysis.get('overall_health')}")
        print(f"Service Hooks Health: {health_analysis.get('service_hooks_health', {}).get('health_status')}")
        print(f"Notification Health: {health_analysis.get('notification_health', {}).get('health_status')}")
        
        # Security Audit
        print("\n2. Security Audit")
        security_audit = await client.facades.security.conduct_security_audit()
        print(f"Security Score: {security_audit.get('overall_score', 'N/A')}")
        print(f"Critical Issues: {security_audit.get('critical_issues', 0)}")
        print(f"Recommendations: {len(security_audit.get('recommendations', []))}")
        
        # Governance Assessment
        print("\n3. Governance Assessment")
        governance_assessment = await client.facades.governance.conduct_governance_assessment(
            assessment_scope=["organization"],
            assessment_config={
                "policy_assessment": {"enabled": True},
                "security_assessment": {"enabled": True},
                "efficiency_assessment": {"enabled": True}
            }
        )
        print(f"Policy Compliance: {governance_assessment.get('policy_compliance', {}).get('compliance_score', 'N/A')}")
        print(f"Security Posture: {governance_assessment.get('security_posture', {}).get('security_score', 'N/A')}")
        
        # Executive Report Generation
        print("\n4. Executive Report Generation")
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        executive_report = await client.facades.governance.generate_executive_governance_report(
            reporting_period=(start_date, end_date),
            report_config={
                "executive_summary": {"enabled": True},
                "detailed_metrics": {"enabled": True}
            }
        )
        print(f"Report Period: {executive_report.get('reporting_period', {}).get('start')} to {executive_report.get('reporting_period', {}).get('end')}")
        print(f"Overall Health: {executive_report.get('governance_metrics', {}).get('overall_health', 'N/A')}")
        
        # Example 4: Real-time Monitoring Setup
        print("\n" + "="*60)
        print("REAL-TIME MONITORING SETUP")
        print("="*60)
        
        # Event-Driven Automation
        print("\n1. Event-Driven Automation Setup")
        automation_result = await client.facades.integration.implement_event_driven_automation(
            project_id=project_result.get('project', {}).get('id'),
            automation_config={
                "events": [
                    "ms.vss-code.git-push-event",
                    "ms.vss-build.build-status-changed-event",
                    "ms.vss-release.deployment-completed-event"
                ],
                "rules": [
                    {
                        "name": "Auto-deploy on successful build",
                        "trigger": "build_success",
                        "action": "deploy_to_dev"
                    }
                ],
                "monitoring": {
                    "alerts": True,
                    "dashboards": True
                }
            }
        )
        print(f"Automation Setup: {len(automation_result.get('event_subscriptions', []))} event subscriptions")
        print(f"Workflow Triggers: {len(automation_result.get('workflow_triggers', []))}")
        
        # Continuous Compliance Monitoring
        print("\n2. Continuous Compliance Monitoring")
        compliance_monitoring = await client.facades.security.setup_continuous_compliance_monitoring(
            compliance_config={
                "standards": ["SOX", "SOC2"],
                "monitoring_frequency": "daily",
                "alert_thresholds": {
                    "policy_violations": 1,
                    "security_incidents": 1
                },
                "reporting": {
                    "frequency": "weekly",
                    "recipients": ["compliance@company.com"]
                }
            }
        )
        print(f"Compliance Monitoring: {compliance_monitoring.get('success', False)}")
        
        print("\n" + "="*60)
        print("EXAMPLE EXECUTION COMPLETED SUCCESSFULLY")
        print("="*60)
        print("\nThe Azure DevOps Wrapper has demonstrated:")
        print("✓ Complete project lifecycle management")
        print("✓ Comprehensive CI/CD pipeline orchestration")
        print("✓ Zero-trust security implementation")
        print("✓ Enterprise integration management")
        print("✓ Advanced governance frameworks")
        print("✓ Real-time monitoring and automation")
        print("✓ Executive reporting and analytics")
        print("\nTotal API Operations Available: ~2,125 across 13 service categories")
        
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up resources
        await client.close()


if __name__ == "__main__":
    # Run the comprehensive example
    asyncio.run(main())
