# Azure DevOps Governance Factory

A comprehensive enterprise-grade platform for Azure DevOps governance, compliance, and operational excellence. This platform provides automated governance policy enforcement, multi-framework compliance validation, and intelligent insights for Azure DevOps environments.

## 🚀 Platform Overview

The Azure DevOps Governance Factory is a microservice-based platform that enables organizations to:

- **Enforce Governance Policies**: Automated policy evaluation and enforcement across projects, repositories, pipelines, and work items
- **Validate Compliance**: Multi-framework compliance validation (CMMI, SOX, GDPR, ISO 27001, HIPAA)
- **Monitor Operations**: Real-time monitoring and alerting for governance violations
- **Generate Reports**: Comprehensive compliance and governance reporting
- **Integrate Seamlessly**: Native Azure DevOps integration with minimal setup

## 🏗️ Architecture

### Core Components

- **Governance Engine**: Policy evaluation and enforcement engine
- **Compliance Engine**: Multi-framework compliance validation
- **Azure DevOps Integration**: Native Azure DevOps API integration
- **Authentication Service**: JWT-based authentication with Azure AD support
- **Monitoring & Alerting**: Prometheus metrics and structured logging
- **Caching Layer**: Redis-based caching for performance optimization

### Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **Authentication**: JWT with Azure AD integration
- **Monitoring**: Prometheus + Grafana
- **Logging**: Structured logging with ELK stack support
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest with async support

## 📦 Installation & Setup

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for development)
- Azure DevOps organization access
- Azure AD tenant (optional, for SSO)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd azure-devops-governance-factory
   ```

2. **Configure environment**
   ```bash
   cp config/.env.example config/.env
   # Edit config/.env with your Azure DevOps settings
   ```

3. **Start the platform**
   ```bash
   docker-compose up -d
   ```

4. **Verify installation**
   ```bash
   curl http://localhost:8000/health
   ```

## 🎯 Implementation Status

### ✅ Completed Components

- **Project Foundation**: Complete directory structure, Docker configuration, requirements management
- **Core Infrastructure**: Configuration management, structured logging, database layer, Redis caching, security middleware
- **Authentication System**: JWT-based authentication with user management and role-based access control
- **API Framework**: FastAPI application with routing structure and OpenAPI documentation
- **Azure DevOps Integration**: Core Azure DevOps service with project and work item management
- **Governance Engine**: Policy evaluation engine with support for pull requests, pipelines, and work items
- **Compliance Engine**: Multi-framework compliance validation (CMMI, SOX, GDPR, ISO 27001)
- **Pipeline Service**: Azure DevOps Pipelines integration with security analysis
- **API Endpoints**: Complete REST API implementation for all core functionality
- **Testing Framework**: Comprehensive test suite with pytest and async support

### 🔧 Ready for Deployment

The platform is fully implemented and ready for deployment with:

- **Docker Environment**: Complete containerization with docker-compose configuration
- **Database Support**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **Monitoring**: Prometheus metrics and structured logging
- **Security**: JWT authentication, RBAC, and security middleware
- **Documentation**: Comprehensive API documentation with Swagger UI

### 🚀 Getting Started

1. **Environment Setup**
   ```bash
   # Configure your Azure DevOps credentials
   cp config/.env.example config/.env
   # Edit config/.env with your settings
   ```

2. **Launch Platform**
   ```bash
   # Start all services
   docker-compose up -d
   
   # Check service health
   curl http://localhost:8000/health
   ```

3. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🔧 API Reference

### Authentication

```bash
# Login
POST /api/v1/auth/login
{
    "username": "user@example.com",
    "password": "password"
}
```

### Governance Endpoints

```bash
# Evaluate governance policies
POST /api/v1/governance/evaluate
{
    "context": {
        "type": "pull_request",
        "reviewers": ["user1", "user2"],
        "work_items": ["12345"],
        "has_tests": true
    },
    "policy_set": "default"
}
```

### Compliance Endpoints

```bash
# Validate CMMI compliance
POST /api/v1/compliance/validate/cmmi
{
    "project_data": {
        "requirements_traceability": true,
        "project_plan": true,
        "version_control": true,
        "quality_assurance": true
    }
}
```

### Azure DevOps Integration

```bash
# Get projects
GET /api/v1/projects

# Get work items with WIQL
POST /api/v1/work-items/query
{
    "wiql": "SELECT [System.Id] FROM WorkItems WHERE [System.State] = 'Active'"
}

# Run pipeline
POST /api/v1/pipelines/{pipeline_id}/run
{
    "branch": "main",
    "variables": {
        "BuildConfiguration": "Release"
    }
}
```

## 🧪 Testing

```bash
# Run all tests
docker-compose -f docker-compose.test.yml up --build

# Run specific test categories
pytest tests/test_governance.py -v
pytest tests/test_compliance.py -v
pytest tests/test_api.py -v
```

## 📖 Documentation

### Implementation Details

See the `/specs` directory for detailed documentation:
- [Service Overview](specs/README.md) - Complete service specification
- [Business Requirements](specs/business/requirements.md) - Business requirements and value proposition
- [Functional Requirements](specs/functional/requirements.md) - Detailed functional specifications
- [Implementation Architecture](specs/implementation/architecture.md) - Technical architecture details
- [Task Breakdown](specs/implementation/task-breakdown.md) - Implementation roadmap

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## 🔒 Security

- JWT token-based authentication
- Role-based access control (RBAC)
- Azure AD integration support
- Secrets management with Azure Key Vault
- TLS encryption and audit logging

## 🚀 Deployment

### Docker Deployment

```bash
# Production deployment
docker-compose -f docker-compose.production.yml up -d

# With monitoring stack
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

## 🤝 Integration

Part of the AI DevOps ecosystem:
- Orchestrator Service
- Dev Agent Service  
- QA Agent Service
- Security Agent Service
- Release Agent Service
- PM Agent Service

## 📄 License

Enterprise software - All rights reserved

---

**Built with ❤️ for Azure DevOps governance and compliance**
