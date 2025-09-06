"""
Configuration management for Azure DevOps Governance Factory
"""

from functools import lru_cache
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    PROJECT_NAME: str = Field(default="Azure DevOps Governance Factory")
    PROJECT_VERSION: str = Field(default="1.0.0")
    ENVIRONMENT: str = Field(default="development")
    API_V1_PREFIX: str = Field(default="/api/v1")
    
    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_EXPIRATION_HOURS: int = Field(default=24)
    
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    # Redis
    REDIS_URL: str = Field(..., env="REDIS_URL")
    
    # Azure Configuration
    AZURE_CLIENT_ID: str = Field(..., env="AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET: str = Field(..., env="AZURE_CLIENT_SECRET")
    AZURE_TENANT_ID: str = Field(..., env="AZURE_TENANT_ID")
    AZURE_DEVOPS_ORGANIZATION: str = Field(..., env="AZURE_DEVOPS_ORGANIZATION")
    AZURE_DEVOPS_API_VERSION: str = Field(default="7.1-preview.1")
    AZURE_DEVOPS_TIMEOUT: int = Field(default=30)
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(default="json")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(default=1000)
    RATE_LIMIT_BURST: int = Field(default=50)
    
    # Compliance
    CMMI_LEVEL: int = Field(default=3)
    ENABLE_SOX_COMPLIANCE: bool = Field(default=True)
    ENABLE_GDPR_COMPLIANCE: bool = Field(default=True)
    ENABLE_HIPAA_COMPLIANCE: bool = Field(default=False)
    ENABLE_ISO27001_COMPLIANCE: bool = Field(default=True)
    
    # Monitoring
    ENABLE_METRICS: bool = Field(default=True)
    METRICS_PORT: int = Field(default=9090)
    ENABLE_HEALTH_CHECKS: bool = Field(default=True)
    
    # Machine Learning
    ENABLE_ML_FEATURES: bool = Field(default=True)
    ML_MODEL_PATH: str = Field(default="/app/models")
    PREDICTION_CONFIDENCE_THRESHOLD: float = Field(default=0.85)
    
    # Azure DevOps Integration
    AZURE_DEVOPS_BASE_URL: str = Field(default="https://dev.azure.com")
    AZURE_DEVOPS_API_BASE_URL: str = Field(default="https://dev.azure.com")
    
    # Webhook Configuration
    WEBHOOK_SECRET: Optional[str] = Field(default=None, env="WEBHOOK_SECRET")
    WEBHOOK_TIMEOUT: int = Field(default=30)
    
    # Governance Configuration
    POLICY_CACHE_TTL: int = Field(default=300)  # 5 minutes
    GOVERNANCE_BATCH_SIZE: int = Field(default=100)
    COMPLIANCE_CHECK_INTERVAL: int = Field(default=3600)  # 1 hour
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
