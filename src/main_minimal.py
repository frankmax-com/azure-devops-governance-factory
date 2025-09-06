"""
Azure DevOps Governance Factory - Minimal Main Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog
import os

# Setup basic logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.dev.ConsoleRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Azure DevOps Governance Factory",
    description="Enterprise Azure DevOps integration and governance platform",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Azure DevOps Governance Factory",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Azure DevOps Governance Factory API",
        "docs": "/api/v1/docs",
        "health": "/health"
    }

# Basic API endpoints
@app.get("/api/v1/azure-devops/templates/projects")
async def get_project_templates():
    """Get available project templates"""
    return {
        "templates": [
            {
                "id": "basic-web-app",
                "name": "Basic Web Application",
                "description": "Standard web application with CI/CD pipeline"
            },
            {
                "id": "microservice",
                "name": "Microservice",
                "description": "Containerized microservice with full DevOps pipeline"
            }
        ]
    }

@app.get("/api/v1/azure-devops/templates/pipelines")
async def get_pipeline_templates():
    """Get available pipeline templates"""
    return {
        "templates": [
            {
                "id": "basic-ci-cd",
                "name": "Basic CI/CD",
                "description": "Standard build and deployment pipeline"
            },
            {
                "id": "advanced-ci-cd",
                "name": "Advanced CI/CD",
                "description": "Multi-stage pipeline with security scanning"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
