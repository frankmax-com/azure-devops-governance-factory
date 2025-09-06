"""
Azure DevOps Governance Factory - Main Application Entry Point
Enterprise Azure DevOps integration and governance platform
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
import structlog
from contextlib import asynccontextmanager

from src.core.config import get_settings
from src.core.logging import setup_logging
from src.core.monitoring import setup_monitoring
from src.core.database import init_db
from src.core.cache import init_cache
from src.api.routes import api_router
from src.core.middleware import (
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
    AuditLoggingMiddleware
)

# Setup structured logging
setup_logging()
logger = structlog.get_logger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Azure DevOps Governance Factory")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Initialize cache
    await init_cache()
    logger.info("Cache initialized")
    
    # Setup monitoring
    setup_monitoring(app)
    logger.info("Monitoring configured")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Azure DevOps Governance Factory")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Enterprise Azure DevOps integration and governance platform",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    lifespan=lifespan
)

# Add security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.ENVIRONMENT == "development" else ["localhost"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.ENVIRONMENT == "development" else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuditLoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "azure-devops-governance-factory",
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Azure DevOps Governance Factory API",
        "version": settings.PROJECT_VERSION,
        "docs": f"{settings.API_V1_PREFIX}/docs"
    }


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    )
