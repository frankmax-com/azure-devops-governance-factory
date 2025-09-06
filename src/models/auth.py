"""
Authentication and user models
"""

from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship

from src.core.database import Base


class User(Base):
    """User database model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    azure_ad_id = Column(String(100), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)


class UserRole(Base):
    """User role database model"""
    __tablename__ = "user_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    role_name = Column(String(100), nullable=False)
    scope = Column(String(255))  # project, organization, global
    scope_id = Column(String(100))  # specific project/org ID
    granted_by = Column(Integer)
    granted_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)


class ApiToken(Base):
    """API token database model"""
    __tablename__ = "api_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    token_hash = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    scopes = Column(Text)  # JSON array of scopes
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    last_used = Column(DateTime)


# Pydantic models for API
class UserBase(BaseModel):
    """Base user model"""
    username: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., max_length=255)
    full_name: str = Field(..., max_length=255)
    is_active: bool = True
    is_admin: bool = False


class UserCreate(UserBase):
    """User creation model"""
    password: Optional[str] = None
    azure_ad_id: Optional[str] = None


class UserUpdate(BaseModel):
    """User update model"""
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class UserResponse(UserBase):
    """User response model"""
    id: int
    azure_ad_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Login request model"""
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None


class Token(BaseModel):
    """Token model"""
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    user_id: int
    scopes: List[str] = []


class TokenData(BaseModel):
    """Token data model"""
    user_id: Optional[int] = None
    username: Optional[str] = None
    scopes: List[str] = []


class RoleAssignment(BaseModel):
    """Role assignment model"""
    user_id: int
    role_name: str
    scope: Optional[str] = None
    scope_id: Optional[str] = None
    expires_at: Optional[datetime] = None


class ApiTokenCreate(BaseModel):
    """API token creation model"""
    name: str = Field(..., min_length=1, max_length=100)
    scopes: List[str] = []
    expires_in_days: Optional[int] = 90


class ApiTokenResponse(BaseModel):
    """API token response model"""
    id: int
    name: str
    token: str  # Only returned on creation
    scopes: List[str]
    created_at: datetime
    expires_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
