"""
Authentication service for Azure DevOps Governance Factory
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
import bcrypt
from azure.identity import DefaultAzureCredential
import structlog

from src.core.config import get_settings
from src.core.cache import cache_manager
from src.models.auth import User, Token, TokenData

settings = get_settings()
logger = structlog.get_logger(__name__)


class AuthService:
    """Authentication service"""
    
    def __init__(self):
        self.azure_credential = DefaultAzureCredential()
    
    async def authenticate_user(self, username: str, password: str) -> Optional[Token]:
        """Authenticate user with username/password"""
        try:
            # For development, we'll implement basic auth
            # In production, this would integrate with Azure AD
            
            # TODO: Implement actual user authentication
            # This is a placeholder implementation
            if username == "admin" and password == "admin123":
                return await self._create_token(
                    user_id=1,
                    username=username,
                    scopes=["admin", "read", "write"]
                )
            
            return None
            
        except Exception as e:
            logger.error("Authentication failed", username=username, error=str(e))
            return None
    
    async def authenticate_azure_ad(self, token: str) -> Optional[TokenData]:
        """Authenticate user with Azure AD token"""
        try:
            # TODO: Implement Azure AD token validation
            # This would validate the JWT token from Azure AD
            # and extract user information
            
            # Placeholder implementation
            return TokenData(
                user_id=1,
                username="azure_user",
                scopes=["read", "write"]
            )
            
        except Exception as e:
            logger.error("Azure AD authentication failed", error=str(e))
            return None
    
    async def get_current_user(self, token: str) -> Optional[User]:
        """Get current user from token"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            user_id: int = payload.get("sub")
            if user_id is None:
                return None
            
            # Check if token is in cache (not revoked)
            cache_key = f"token:{user_id}:{token[:20]}"
            if not await cache_manager.exists(cache_key):
                return None
            
            # TODO: Fetch user from database
            # Placeholder user data
            return User(
                id=user_id,
                username=payload.get("username"),
                email=payload.get("email", ""),
                full_name=payload.get("full_name", ""),
                is_active=True,
                is_admin=payload.get("is_admin", False),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.JWTError as e:
            logger.warning("Invalid token", error=str(e))
            return None
        except Exception as e:
            logger.error("Get current user failed", error=str(e))
            return None
    
    async def refresh_token(self, token: str) -> Optional[Token]:
        """Refresh access token"""
        try:
            # Validate current token
            user = await self.get_current_user(token)
            if not user:
                return None
            
            # Create new token
            return await self._create_token(
                user_id=user.id,
                username=user.username,
                scopes=["read", "write"]  # TODO: Get actual user scopes
            )
            
        except Exception as e:
            logger.error("Token refresh failed", error=str(e))
            return None
    
    async def invalidate_token(self, token: str) -> bool:
        """Invalidate token (logout)"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            user_id: int = payload.get("sub")
            if user_id:
                cache_key = f"token:{user_id}:{token[:20]}"
                await cache_manager.delete(cache_key)
            
            return True
            
        except Exception as e:
            logger.error("Token invalidation failed", error=str(e))
            return False
    
    async def _create_token(
        self,
        user_id: int,
        username: str,
        scopes: list = None
    ) -> Token:
        """Create JWT token"""
        if scopes is None:
            scopes = []
        
        expires_delta = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        expire = datetime.utcnow() + expires_delta
        
        payload = {
            "sub": user_id,
            "username": username,
            "scopes": scopes,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        access_token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        # Store token in cache for validation
        cache_key = f"token:{user_id}:{access_token[:20]}"
        await cache_manager.set(
            cache_key,
            {"user_id": user_id, "username": username, "scopes": scopes},
            ttl=int(expires_delta.total_seconds())
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=int(expires_delta.total_seconds()),
            user_id=user_id,
            scopes=scopes
        )
    
    def _hash_password(self, password: str) -> str:
        """Hash password"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
