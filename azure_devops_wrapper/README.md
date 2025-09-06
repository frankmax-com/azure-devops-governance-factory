# Azure DevOps Wrapper - Comprehensive Python SDK

A comprehensive, enterprise-grade Python wrapper for the Azure DevOps REST API that simplifies complex DevOps workflows and provides developer-friendly interfaces for all ~2,125 API operations across 13 service categories.

## 🚀 Key Features

### Complete API Coverage
- **~2,125 API Operations** across all HTTP methods (GET, POST, PUT, PATCH, DELETE)
- **13 Service Categories**: Core, Git, Work Items, Build, Pipelines, Release, Test, Packaging, Security, Graph, Extensions, Notification, Service Hooks, Audit
- **Enterprise-Grade Architecture** with 4-layer modular design

### Authentication & Security
- **Multiple Auth Methods**: Personal Access Token (PAT), OAuth 2.0, Managed Identity, Service Principal
- **Automatic Token Refresh** with secure credential management
- **Zero-Trust Security Implementation** with comprehensive security governance

### Performance & Reliability
- **Async-First Design** for high-performance concurrent operations
- **Automatic Rate Limiting** with token bucket algorithm and exponential backoff
- **Intelligent Retry Logic** with configurable retry policies
- **Generic Pagination Support** with async iteration

### Enterprise Governance
- **Compliance Frameworks**: SOX, SOC2, GDPR, ISO27001 support
- **Risk Management**: Comprehensive risk assessment and mitigation
- **Audit Trails**: Complete activity logging and compliance reporting
- **Policy Enforcement**: Automated policy compliance monitoring

### Developer Experience
- **Type Safety**: Comprehensive Pydantic models with validation
- **Business Facades**: High-level abstractions for complex workflows
- **Comprehensive Documentation**: Detailed examples and API reference
- **Error Handling**: Structured exception hierarchy with context

## 📦 Installation

```bash
pip install azure-devops-wrapper
```

### Requirements
- Python 3.8+
- httpx
- pydantic
- asyncio

## 🔧 Quick Start

### Basic Usage

```python
from azure_devops_wrapper import AzureDevOpsClient, AuthConfig

# Initialize client with Personal Access Token
client = AzureDevOpsClient(
    organization="your-organization",
    auth_config=AuthConfig(
        auth_type="pat",
        personal_access_token="your-pat-token"
    )
)

# Test connection
connection_test = await client.test_connection()
print(f"Status: {connection_test['connection_status']}")

# Get projects using low-level service
projects = await client.services.core.get_projects()

# Create complete project using high-level facade
project_result = await client.facades.project.create_complete_project(
    project_name="MyProject",
    project_config={
        "description": "New project with complete setup",
        "source_control": "git",
        "work_item_process": "agile",
        "teams": [{"name": "Dev Team", "description": "Development team"}],
        "area_paths": ["Frontend", "Backend", "DevOps"],
        "iteration_paths": ["Sprint 1", "Sprint 2"]
    }
)

# Clean up
await client.close()
```

### Authentication Methods

```python
# Personal Access Token
auth_config = AuthConfig(
    auth_type="pat",
    personal_access_token="your-pat-token"
)

# OAuth 2.0
auth_config = AuthConfig(
    auth_type="oauth",
    client_id="your-client-id",
    client_secret="your-client-secret",
    tenant_id="your-tenant-id"
)

# Managed Identity
auth_config = AuthConfig(
    auth_type="managed_identity",
    client_id="your-managed-identity-client-id"  # Optional
)

# Service Principal
auth_config = AuthConfig(
    auth_type="service_principal",
    client_id="your-app-id",
    client_secret="your-app-secret",
    tenant_id="your-tenant-id"
)
```

## 🏗️ Architecture

### 4-Layer Modular Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Business Facade Layer                    │
│  ProjectFacade | PipelineFacade | SecurityFacade | etc.    │
├─────────────────────────────────────────────────────────────┤
│                    Service Client Layer                     │
│   CoreService | GitService | BuildService | etc. (13)     │
├─────────────────────────────────────────────────────────────┤
│                HTTP/Authentication Infrastructure            │
│    HTTPClient | AuthManager | RateLimiter | Pagination     │
├─────────────────────────────────────────────────────────────┤
│                  Azure DevOps REST API                     │
│              ~2,125 API Operations Available               │
└─────────────────────────────────────────────────────────────┘
```

### Service Categories (13 Total)

1. **CoreService** - Projects, teams, processes, organizational management
2. **GitService** - Repositories, branches, commits, pull requests, policies
3. **WorkItemsService** - Work items, queries, attachments, comments
4. **BuildService** - Build definitions, builds, artifacts, logs
5. **PipelinesService** - YAML pipelines, runs, approvals, environments
6. **ReleaseService** - Release definitions, releases, deployments
7. **TestService** - Test plans, suites, cases, runs, results
8. **PackagingService** - Feeds, packages, versions, permissions
9. **SecurityService** - Permissions, policies, tokens, access control
10. **GraphService** - Users, groups, memberships, Microsoft Graph integration
11. **ExtensionsService** - Extensions, installation, configuration
12. **NotificationService** - Subscriptions, events, delivery preferences
13. **ServiceHooksService** - Webhooks, subscriptions, external integrations

## 🎯 Business Facades

### ProjectFacade - Complete Project Management

```python
# Create complete project with full setup
project_result = await client.facades.project.create_complete_project(
    project_name="Enterprise-Project",
    project_config={
        "description": "Complete enterprise project setup",
        "source_control": "git",
        "work_item_process": "agile",
        "version_control": {
            "repository_name": "main",
            "initial_branch": "main",
            "gitignore_template": "VisualStudio"
        },
        "teams": [
            {"name": "Development Team", "description": "Core development"},
            {"name": "QA Team", "description": "Quality assurance"},
            {"name": "DevOps Team", "description": "Infrastructure and deployment"}
        ],
        "area_paths": ["Frontend", "Backend", "Mobile", "DevOps"],
        "iteration_paths": ["Sprint 1", "Sprint 2", "Sprint 3"],
        "security": {
            "inherit_permissions": False,
            "custom_permissions": [
                {"identity": "dev-team", "permissions": ["read", "write"]},
                {"identity": "qa-team", "permissions": ["read"]}
            ]
        }
    }
)

# Clone project structure from template
cloned_project = await client.facades.project.clone_project_structure(
    source_project_id="template-project-id",
    target_project_name="New-Project",
    clone_options={
        "include_work_items": True,
        "include_repositories": True,
        "include_pipelines": True,
        "include_permissions": False
    }
)

# Generate project health report
health_report = await client.facades.project.get_project_health_report(
    project_id="project-id",
    include_metrics=["activity", "quality", "security", "performance"]
)
```

### PipelineFacade - CI/CD Pipeline Orchestration

```python
# Create complete CI/CD pipeline with multi-stage deployment
pipeline_result = await client.facades.pipeline.create_complete_cicd_pipeline(
    project_id="project-id",
    pipeline_config={
        "name": "Production-CICD-Pipeline",
        "repository": {
            "name": "main",
            "branch": "main",
            "path": "/azure-pipelines.yml"
        },
        "build_stages": [
            {
                "name": "Build",
                "tasks": ["restore", "build", "test", "publish"],
                "parallel_jobs": 2,
                "timeout_minutes": 60
            },
            {
                "name": "Code-Analysis",
                "tasks": ["sonarqube", "dependency_check"],
                "depends_on": ["Build"]
            }
        ],
        "deployment_stages": [
            {
                "name": "Development",
                "environment": "dev",
                "approval_required": False,
                "deployment_strategy": "blue_green"
            },
            {
                "name": "Staging",
                "environment": "staging", 
                "approval_required": True,
                "approvers": ["staging-approvers"],
                "deployment_strategy": "canary"
            },
            {
                "name": "Production",
                "environment": "prod",
                "approval_required": True,
                "approvers": ["prod-approvers"],
                "deployment_strategy": "rolling"
            }
        ],
        "security_scanning": {
            "enabled": True,
            "tools": ["dependency_check", "container_scan", "code_analysis"],
            "fail_on_critical": True
        },
        "notifications": {
            "email": ["devops@company.com"],
            "slack_webhook": "https://hooks.slack.com/services/...",
            "teams_webhook": "https://company.webhook.office.com/..."
        }
    }
)

# Implement GitOps workflow
gitops_result = await client.facades.pipeline.implement_gitops_workflow(
    project_id="project-id",
    gitops_config={
        "config_repository": "gitops-config",
        "sync_frequency": "5m",
        "auto_sync": True,
        "prune": True,
        "self_heal": True
    }
)

# Analyze pipeline performance
performance_analysis = await client.facades.pipeline.analyze_pipeline_performance(
    project_id="project-id",
    analysis_period_days=30,
    include_metrics=["duration", "success_rate", "failure_analysis", "bottlenecks"]
)
```

### SecurityFacade - Zero-Trust Security & Governance

```python
# Implement zero-trust security framework
security_result = await client.facades.security.implement_zero_trust_security(
    security_config={
        "identity_verification": {
            "mfa_required": True,
            "conditional_access": True,
            "privileged_access_management": True
        },
        "least_privilege": {
            "enabled": True,
            "review_period_days": 90,
            "automatic_cleanup": True
        },
        "continuous_monitoring": {
            "enabled": True,
            "real_time_alerts": True,
            "alert_thresholds": {
                "failed_logins": 5,
                "privilege_escalation": 1,
                "unusual_access_patterns": 3
            }
        },
        "data_protection": {
            "encryption_required": True,
            "data_classification": True,
            "dlp_policies": True
        }
    }
)

# Set up role-based access control
rbac_result = await client.facades.security.setup_role_based_access_control(
    rbac_config={
        "roles": [
            {
                "name": "Developer",
                "permissions": ["code_read", "code_write", "build_queue"],
                "scope": "project"
            },
            {
                "name": "DevOps Engineer", 
                "permissions": ["pipeline_admin", "environment_admin"],
                "scope": "organization"
            }
        ],
        "inheritance": "enabled",
        "approval_workflow": "required"
    }
)

# Conduct comprehensive security audit
security_audit = await client.facades.security.conduct_security_audit(
    audit_scope=["permissions", "tokens", "policies", "vulnerabilities"],
    include_remediation=True
)
```

### IntegrationFacade - DevOps Integration Management

```python
# Set up complete DevOps integration ecosystem
integration_result = await client.facades.integration.setup_complete_devops_integration(
    project_id="project-id",
    integration_config={
        "chat_integrations": {
            "slack": {
                "channels": [
                    {"name": "dev-alerts", "webhook_url": "https://hooks.slack.com/..."},
                    {"name": "build-status", "webhook_url": "https://hooks.slack.com/..."}
                ]
            },
            "teams": {
                "channels": [
                    {"name": "DevOps Notifications", "webhook_url": "https://company.webhook.office.com/..."}
                ]
            }
        },
        "issue_tracking": {
            "jira": {
                "webhook_url": "https://company.atlassian.net/webhook",
                "secret": "jira-webhook-secret"
            }
        },
        "monitoring": {
            "datadog": {
                "webhook_url": "https://api.datadoghq.com/webhook",
                "api_key": "datadog-api-key"
            },
            "app_insights": {
                "instrumentation_key": "app-insights-key"
            }
        },
        "ci_cd_tools": {
            "github_actions": {
                "webhook_url": "https://api.github.com/webhook",
                "secret": "github-webhook-secret"
            },
            "jenkins": {
                "webhook_url": "https://jenkins.company.com/webhook",
                "token": "jenkins-token"
            }
        }
    }
)

# Implement event-driven automation
automation_result = await client.facades.integration.implement_event_driven_automation(
    project_id="project-id",
    automation_config={
        "events": [
            "ms.vss-code.git-push-event",
            "ms.vss-build.build-status-changed-event",
            "ms.vss-release.deployment-completed-event"
        ],
        "rules": [
            {
                "name": "Auto-deploy successful builds",
                "trigger": "build_success",
                "conditions": ["branch == 'main'", "all_tests_passed"],
                "action": "deploy_to_dev"
            },
            {
                "name": "Notify on deployment failures",
                "trigger": "deployment_failed",
                "action": "send_alert"
            }
        ],
        "escalations": [
            {
                "condition": "deployment_failed_3_times",
                "action": "page_on_call_engineer"
            }
        ]
    }
)
```

### GovernanceFacade - Enterprise Governance & Compliance

```python
# Implement enterprise governance framework
governance_result = await client.facades.governance.implement_enterprise_governance(
    governance_config={
        "organizational_policies": {
            "security": [
                {
                    "name": "Code Review Policy",
                    "description": "All code changes require peer review",
                    "type": "mandatory",
                    "enforcement": "automated"
                },
                {
                    "name": "Branch Protection Policy",
                    "description": "Main branch requires status checks",
                    "type": "security",
                    "enforcement": "strict"
                }
            ],
            "compliance": [
                {
                    "name": "SOX Compliance",
                    "description": "Sarbanes-Oxley compliance requirements",
                    "type": "regulatory",
                    "audit_frequency": "quarterly"
                }
            ]
        },
        "compliance_framework": {
            "standards": ["SOX", "SOC2", "GDPR", "ISO27001"],
            "reporting": {
                "frequency": "monthly",
                "recipients": ["compliance@company.com"],
                "automated": True
            },
            "assessments": {
                "frequency": "quarterly",
                "external_auditor": True
            }
        },
        "risk_management": {
            "enabled": True,
            "assessment_frequency": "quarterly",
            "risk_tolerance": "medium",
            "mitigation_required": True
        }
    }
)

# Establish compliance framework for multiple standards
compliance_result = await client.facades.governance.establish_compliance_framework(
    compliance_standards=["SOX", "SOC2", "GDPR"],
    compliance_config={
        "SOX": {
            "controls": ["access_controls", "change_management", "audit_trails"],
            "reporting_frequency": "quarterly"
        },
        "SOC2": {
            "controls": ["security", "availability", "confidentiality"],
            "monitoring": "continuous"
        },
        "GDPR": {
            "controls": ["data_protection", "consent_management", "breach_notification"],
            "data_retention": "automatic"
        }
    }
)

# Generate executive governance report
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=90)

executive_report = await client.facades.governance.generate_executive_governance_report(
    reporting_period=(start_date, end_date),
    report_config={
        "executive_summary": {"enabled": True},
        "governance_metrics": {"detailed": True},
        "compliance_status": {"all_standards": True},
        "risk_analysis": {"include_trends": True},
        "recommendations": {"prioritized": True}
    }
)
```

## 📊 Service Layer Examples

### Core Service - Project & Team Management

```python
# Project operations
projects = await client.services.core.get_projects()
project = await client.services.core.get_project("project-id")
new_project = await client.services.core.create_project({
    "name": "New Project",
    "description": "Project description",
    "capabilities": {
        "versioncontrol": {"sourceControlType": "Git"},
        "processTemplate": {"templateTypeId": "agile"}
    }
})

# Team operations
teams = await client.services.core.get_teams("project-id")
team = await client.services.core.create_team("project-id", {
    "name": "Development Team",
    "description": "Core development team"
})

# Process templates
processes = await client.services.core.get_processes()
```

### Git Service - Repository Management

```python
# Repository operations
repositories = await client.services.git.get_repositories("project-id")
repository = await client.services.git.create_repository("project-id", {
    "name": "new-repo",
    "project": {"id": "project-id"}
})

# Branch operations
branches = await client.services.git.get_branches("project-id", "repo-id")
branch = await client.services.git.create_branch("project-id", "repo-id", {
    "name": "feature/new-feature",
    "oldObjectId": "commit-sha"
})

# Commit operations
commits = await client.services.git.get_commits("project-id", "repo-id")
commit = await client.services.git.get_commit("project-id", "repo-id", "commit-id")

# Pull request operations
pull_requests = await client.services.git.get_pull_requests("project-id", "repo-id")
pr = await client.services.git.create_pull_request("project-id", "repo-id", {
    "sourceRefName": "refs/heads/feature/branch",
    "targetRefName": "refs/heads/main",
    "title": "Add new feature",
    "description": "Detailed description"
})

# Repository policies
policies = await client.services.git.get_repository_policies("project-id", "repo-id")
```

### Build Service - Build Management

```python
# Build definition operations
build_definitions = await client.services.build.get_build_definitions("project-id")
build_def = await client.services.build.create_build_definition("project-id", {
    "name": "CI Build",
    "repository": {"id": "repo-id", "type": "TfsGit"},
    "process": {"yamlFilename": "azure-pipelines.yml"}
})

# Build operations
builds = await client.services.build.get_builds("project-id")
build = await client.services.build.queue_build("project-id", {
    "definition": {"id": "build-def-id"},
    "sourceBranch": "refs/heads/main"
})

# Build artifacts
artifacts = await client.services.build.get_build_artifacts("project-id", "build-id")
```

### Pipeline Service - YAML Pipeline Management

```python
# Pipeline operations
pipelines = await client.services.pipelines.get_pipelines("project-id")
pipeline = await client.services.pipelines.create_pipeline("project-id", {
    "name": "Production Pipeline",
    "folder": "\\",
    "configuration": {
        "type": "yaml",
        "path": "/azure-pipelines.yml",
        "repository": {"id": "repo-id", "name": "main", "type": "azureReposGit"}
    }
})

# Pipeline runs
runs = await client.services.pipelines.get_pipeline_runs("project-id", "pipeline-id")
run = await client.services.pipelines.run_pipeline("project-id", "pipeline-id", {
    "resources": {
        "repositories": {
            "self": {
                "refName": "refs/heads/main"
            }
        }
    }
})

# Pipeline environments
environments = await client.services.pipelines.get_environments("project-id")
```

## 🔒 Security & Compliance

### Authentication Security

```python
# Token management
tokens = await client.services.security.get_personal_access_tokens()
token = await client.services.security.create_personal_access_token({
    "displayName": "CI/CD Token",
    "scope": "vso.build vso.release",
    "validTo": "2024-12-31T23:59:59Z"
})

# Service connections
connections = await client.services.security.get_service_connections("project-id")
connection = await client.services.security.create_service_connection("project-id", {
    "name": "Azure Subscription",
    "type": "azurerm",
    "authorization": {"scheme": "ServicePrincipal"}
})
```

### Access Control & Permissions

```python
# Security namespaces
namespaces = await client.services.security.get_security_namespaces()

# Access control lists
acls = await client.services.security.get_access_control_lists("namespace-id")
await client.services.security.set_access_control_lists("namespace-id", {
    "token": "project-token",
    "acesDictionary": {
        "identity-id": {
            "allow": 1,
            "deny": 0
        }
    }
})

# Permission evaluation
permissions = await client.services.security.evaluate_permissions(
    "namespace-id",
    "identity-id", 
    "resource-token"
)
```

## 📈 Monitoring & Analytics

### Integration Health Monitoring

```python
# Analyze integration health across organization
health_analysis = await client.facades.integration.analyze_integration_health(
    project_id="project-id",  # Optional - for specific project
    days=30
)

print(f"Overall Health: {health_analysis['overall_health']}")
print(f"Service Hooks: {health_analysis['service_hooks_health']['success_rate']}% success")
print(f"Notifications: {health_analysis['notification_health']['delivery_success_rate']}% delivered")
print(f"Extensions: {health_analysis['extension_health']['enabled_extensions']} active")

# Get performance trends
for trend in health_analysis['performance_trends']:
    print(f"Trend: {trend['metric']} - {trend['direction']} ({trend['change']}%)")

# Review recommendations
for recommendation in health_analysis['recommendations']:
    print(f"Recommendation: {recommendation}")
```

### Security Monitoring & Auditing

```python
# Continuous security monitoring
security_monitoring = await client.facades.security.setup_continuous_security_monitoring(
    monitoring_config={
        "real_time_alerts": True,
        "alert_channels": ["email", "slack"],
        "monitoring_frequency": "5m",
        "security_events": [
            "authentication_failures",
            "privilege_escalations", 
            "policy_violations",
            "unusual_access_patterns"
        ]
    }
)

# Security dashboard
security_dashboard = await client.facades.security.generate_security_dashboard(
    dashboard_config={
        "time_range": "30d",
        "include_metrics": [
            "authentication_success_rate",
            "policy_compliance_score",
            "vulnerability_count",
            "incident_response_time"
        ]
    }
)

# Compliance monitoring
compliance_monitoring = await client.facades.security.setup_continuous_compliance_monitoring(
    compliance_config={
        "standards": ["SOX", "SOC2", "GDPR"],
        "monitoring_frequency": "daily",
        "automatic_remediation": True,
        "alert_thresholds": {
            "policy_violations": 1,
            "access_anomalies": 3
        }
    }
)
```

## 🚀 Advanced Scenarios

### Cross-Platform Integration

```python
# Set up cross-platform integrations
cross_platform_result = await client.facades.integration.setup_cross_platform_integration(
    integration_matrix={
        "github": {
            "repositories": ["org/repo1", "org/repo2"],
            "sync_type": "bidirectional",
            "webhook_events": ["push", "pull_request", "issues"]
        },
        "jira": {
            "projects": ["PROJ1", "PROJ2"],
            "sync_work_items": True,
            "field_mappings": {
                "priority": "Priority",
                "status": "Status"
            }
        },
        "slack": {
            "channels": ["#dev-alerts", "#build-notifications"],
            "notification_types": ["builds", "deployments", "incidents"]
        }
    }
)
```

### GitOps Implementation

```python
# Implement GitOps workflow
gitops_result = await client.facades.integration.implement_gitops_automation(
    project_id="project-id",
    gitops_config={
        "config_repositories": [
            {
                "name": "infrastructure-config",
                "path": "/k8s-manifests",
                "sync_frequency": "5m"
            },
            {
                "name": "application-config", 
                "path": "/helm-charts",
                "sync_frequency": "10m"
            }
        ],
        "sync_config": {
            "auto_sync": True,
            "prune": True,
            "self_heal": True,
            "sync_timeout": "5m"
        },
        "deployment_config": {
            "strategy": "progressive",
            "health_checks": True,
            "rollback_on_failure": True
        }
    }
)
```

### Multi-Environment Pipeline

```python
# Set up multi-environment deployment pipeline
multi_env_pipeline = await client.facades.pipeline.setup_multi_stage_deployment(
    project_id="project-id",
    deployment_config={
        "environments": [
            {
                "name": "development",
                "approval_required": False,
                "auto_deploy": True,
                "health_checks": ["basic"],
                "rollback_strategy": "immediate"
            },
            {
                "name": "staging",
                "approval_required": True,
                "approvers": ["staging-team"],
                "health_checks": ["comprehensive"],
                "deployment_strategy": "blue_green"
            },
            {
                "name": "production",
                "approval_required": True,
                "approvers": ["prod-approvers", "security-team"],
                "health_checks": ["comprehensive", "security"],
                "deployment_strategy": "canary",
                "canary_config": {
                    "initial_percentage": 10,
                    "increment_percentage": 25,
                    "evaluation_duration": "10m"
                }
            }
        ],
        "global_settings": {
            "timeout_minutes": 60,
            "enable_diagnostics": True,
            "notification_hooks": [
                "slack://channel/deployments",
                "email://devops-team@company.com"
            ]
        }
    }
)
```

## 🔧 Configuration & Customization

### Rate Limiting Configuration

```python
from azure_devops_wrapper import RateLimitConfig

# Custom rate limiting
rate_limit_config = RateLimitConfig(
    requests_per_second=10.0,  # Requests per second
    burst_capacity=50,         # Burst capacity
    max_retries=3,            # Max retry attempts
    backoff_factor=2.0,       # Exponential backoff factor
    max_backoff_seconds=300   # Maximum backoff time
)

client = AzureDevOpsClient(
    organization="your-org",
    auth_config=auth_config,
    rate_limit_config=rate_limit_config
)
```

### HTTP Client Configuration

```python
from azure_devops_wrapper import ClientConfig

# Custom HTTP client settings
client_config = ClientConfig(
    timeout=60.0,              # Request timeout
    max_retries=5,            # Max HTTP retries
    retry_backoff_factor=1.5, # Retry backoff
    max_connections=100,      # Connection pool size
    user_agent="MyApp/1.0"    # Custom user agent
)
```

### Custom Error Handling

```python
from azure_devops_wrapper import (
    AzureDevOpsError, AuthenticationError, RateLimitError,
    ResourceNotFoundError, ValidationError
)

try:
    result = await client.services.core.get_project("invalid-id")
except AuthenticationError:
    print("Authentication failed - check credentials")
except ResourceNotFoundError:
    print("Project not found")
except RateLimitError as e:
    print(f"Rate limit exceeded - retry after {e.retry_after} seconds")
except ValidationError as e:
    print(f"Validation error: {e.details}")
except AzureDevOpsError as e:
    print(f"Azure DevOps API error: {e.status_code} - {e.message}")
```

## 📚 API Reference

### Service Layer Coverage

| Service | Operations | Description |
|---------|------------|-------------|
| **CoreService** | ~200 ops | Projects, teams, processes, organizational management |
| **GitService** | ~350 ops | Repositories, branches, commits, pull requests, policies |
| **WorkItemsService** | ~180 ops | Work items, queries, attachments, comments, links |
| **BuildService** | ~250 ops | Build definitions, builds, artifacts, logs, retention |
| **PipelinesService** | ~200 ops | YAML pipelines, runs, approvals, environments |
| **ReleaseService** | ~300 ops | Release definitions, releases, deployments, gates |
| **TestService** | ~220 ops | Test plans, suites, cases, runs, results, coverage |
| **PackagingService** | ~150 ops | Feeds, packages, versions, permissions, retention |
| **SecurityService** | ~180 ops | Permissions, policies, tokens, access control |
| **GraphService** | ~100 ops | Users, groups, memberships, Microsoft Graph |
| **ExtensionsService** | ~80 ops | Extensions, installation, configuration, management |
| **NotificationService** | ~70 ops | Subscriptions, events, delivery preferences |
| **ServiceHooksService** | ~65 ops | Webhooks, subscriptions, external integrations |

**Total: ~2,125+ API Operations**

### Business Facade Coverage

| Facade | Purpose | Key Methods |
|--------|---------|-------------|
| **ProjectFacade** | Complete project lifecycle | `create_complete_project()`, `clone_project_structure()`, `setup_project_governance()` |
| **PipelineFacade** | CI/CD orchestration | `create_complete_cicd_pipeline()`, `setup_multi_stage_deployment()`, `implement_gitops_workflow()` |
| **SecurityFacade** | Zero-trust security | `implement_zero_trust_security()`, `setup_role_based_access_control()`, `conduct_security_audit()` |
| **IntegrationFacade** | DevOps integrations | `setup_complete_devops_integration()`, `implement_event_driven_automation()` |
| **GovernanceFacade** | Enterprise governance | `implement_enterprise_governance()`, `establish_compliance_framework()` |

## 🧪 Testing

```python
# Test connection and authentication
connection_test = await client.test_connection()
assert connection_test['connection_status'] == 'success'
assert connection_test['auth_status'] == 'valid'

# Test service functionality
projects = await client.services.core.get_projects(top=1)
assert len(projects) >= 0

# Test facade functionality
if projects:
    health_report = await client.facades.project.get_project_health_report(
        project_id=projects[0]['id']
    )
    assert 'overall_health' in health_report
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/your-org/azure-devops-wrapper.git
cd azure-devops-wrapper
pip install -e ".[dev]"
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Azure DevOps REST API Documentation](https://docs.microsoft.com/en-us/rest/api/azure/devops/)
- [Python AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)

## 📞 Support

- **Documentation**: [Full API Documentation](https://azure-devops-wrapper.readthedocs.io/)
- **Issues**: [GitHub Issues](https://github.com/your-org/azure-devops-wrapper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/azure-devops-wrapper/discussions)
- **Email**: support@azuredevopswrapper.com

---

**Azure DevOps Wrapper** - Simplifying enterprise DevOps with comprehensive Python automation ⚡
