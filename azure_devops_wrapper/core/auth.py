"""
Authentication management for Azure DevOps API
"""

import base64
import json
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum

from .exceptions import AuthenticationError, ConfigurationError


class AuthType(Enum):
    """Supported authentication types."""
    PAT = "personal_access_token"
    OAUTH = "oauth"
    MANAGED_IDENTITY = "managed_identity"
    SERVICE_PRINCIPAL = "service_principal"


@dataclass
class AuthConfig:
    """Authentication configuration."""
    auth_type: AuthType
    organization: str
    token: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    tenant_id: Optional[str] = None
    scope: Optional[str] = None
    redirect_uri: Optional[str] = None


class AuthManager:
    """Manages authentication for Azure DevOps API requests."""
    
    def __init__(self, config: AuthConfig):
        self.config = config
        self._validate_config()
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._token_expires_at: Optional[float] = None
    
    def _validate_config(self) -> None:
        """Validate authentication configuration."""
        if not self.config.organization:
            raise ConfigurationError("Organization is required")
        
        if self.config.auth_type == AuthType.PAT:
            if not self.config.token:
                raise ConfigurationError("Personal Access Token is required for PAT authentication")
        
        elif self.config.auth_type == AuthType.OAUTH:
            if not all([self.config.client_id, self.config.client_secret, self.config.tenant_id]):
                raise ConfigurationError(
                    "client_id, client_secret, and tenant_id are required for OAuth authentication"
                )
        
        elif self.config.auth_type == AuthType.SERVICE_PRINCIPAL:
            if not all([self.config.client_id, self.config.client_secret, self.config.tenant_id]):
                raise ConfigurationError(
                    "client_id, client_secret, and tenant_id are required for Service Principal authentication"
                )
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests."""
        if self.config.auth_type == AuthType.PAT:
            return self._get_pat_headers()
        elif self.config.auth_type == AuthType.OAUTH:
            return self._get_oauth_headers()
        elif self.config.auth_type == AuthType.MANAGED_IDENTITY:
            return self._get_managed_identity_headers()
        elif self.config.auth_type == AuthType.SERVICE_PRINCIPAL:
            return self._get_service_principal_headers()
        else:
            raise AuthenticationError(f"Unsupported authentication type: {self.config.auth_type}")
    
    def _get_pat_headers(self) -> Dict[str, str]:
        """Get headers for Personal Access Token authentication."""
        if not self.config.token:
            raise AuthenticationError("Personal Access Token not provided")
        
        # Azure DevOps uses Basic Auth with empty username and PAT as password
        credentials = base64.b64encode(f":{self.config.token}".encode()).decode()
        
        return {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _get_oauth_headers(self) -> Dict[str, str]:
        """Get headers for OAuth authentication."""
        if not self._access_token or self._is_token_expired():
            self._refresh_oauth_token()
        
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _get_managed_identity_headers(self) -> Dict[str, str]:
        """Get headers for Managed Identity authentication."""
        if not self._access_token or self._is_token_expired():
            self._get_managed_identity_token()
        
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _get_service_principal_headers(self) -> Dict[str, str]:
        """Get headers for Service Principal authentication."""
        if not self._access_token or self._is_token_expired():
            self._get_service_principal_token()
        
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _is_token_expired(self) -> bool:
        """Check if the current token is expired."""
        if not self._token_expires_at:
            return True
        
        import time
        return time.time() >= self._token_expires_at
    
    def _refresh_oauth_token(self) -> None:
        """Refresh OAuth token."""
        try:
            import httpx
            import time
            
            token_url = f"https://login.microsoftonline.com/{self.config.tenant_id}/oauth2/v2.0/token"
            
            data = {
                "grant_type": "client_credentials",
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "scope": self.config.scope or "https://app.vssps.visualstudio.com/.default"
            }
            
            response = httpx.post(token_url, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self._access_token = token_data["access_token"]
            
            # Set expiration time with 5-minute buffer
            expires_in = token_data.get("expires_in", 3600)
            self._token_expires_at = time.time() + expires_in - 300
            
            if "refresh_token" in token_data:
                self._refresh_token = token_data["refresh_token"]
                
        except Exception as e:
            raise AuthenticationError(f"Failed to refresh OAuth token: {str(e)}")
    
    def _get_managed_identity_token(self) -> None:
        """Get token using Managed Identity."""
        try:
            import httpx
            import time
            import os
            
            # Azure Instance Metadata Service endpoint
            metadata_url = "http://169.254.169.254/metadata/identity/oauth2/token"
            
            params = {
                "api-version": "2018-02-01",
                "resource": "https://app.vssps.visualstudio.com"
            }
            
            headers = {"Metadata": "true"}
            
            response = httpx.get(metadata_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            token_data = response.json()
            self._access_token = token_data["access_token"]
            
            # Set expiration time with 5-minute buffer
            expires_in = int(token_data.get("expires_in", 3600))
            self._token_expires_at = time.time() + expires_in - 300
            
        except Exception as e:
            raise AuthenticationError(f"Failed to get Managed Identity token: {str(e)}")
    
    def _get_service_principal_token(self) -> None:
        """Get token using Service Principal."""
        try:
            import httpx
            import time
            
            token_url = f"https://login.microsoftonline.com/{self.config.tenant_id}/oauth2/v2.0/token"
            
            data = {
                "grant_type": "client_credentials",
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "scope": "https://app.vssps.visualstudio.com/.default"
            }
            
            response = httpx.post(token_url, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self._access_token = token_data["access_token"]
            
            # Set expiration time with 5-minute buffer
            expires_in = token_data.get("expires_in", 3600)
            self._token_expires_at = time.time() + expires_in - 300
            
        except Exception as e:
            raise AuthenticationError(f"Failed to get Service Principal token: {str(e)}")
    
    @classmethod
    def from_pat(cls, organization: str, token: str) -> "AuthManager":
        """Create AuthManager with Personal Access Token."""
        config = AuthConfig(
            auth_type=AuthType.PAT,
            organization=organization,
            token=token
        )
        return cls(config)
    
    @classmethod
    def from_oauth(
        cls, 
        organization: str, 
        client_id: str, 
        client_secret: str, 
        tenant_id: str,
        scope: Optional[str] = None
    ) -> "AuthManager":
        """Create AuthManager with OAuth."""
        config = AuthConfig(
            auth_type=AuthType.OAUTH,
            organization=organization,
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id,
            scope=scope
        )
        return cls(config)
    
    @classmethod
    def from_managed_identity(cls, organization: str) -> "AuthManager":
        """Create AuthManager with Managed Identity."""
        config = AuthConfig(
            auth_type=AuthType.MANAGED_IDENTITY,
            organization=organization
        )
        return cls(config)
    
    @classmethod
    def from_service_principal(
        cls, 
        organization: str, 
        client_id: str, 
        client_secret: str, 
        tenant_id: str
    ) -> "AuthManager":
        """Create AuthManager with Service Principal."""
        config = AuthConfig(
            auth_type=AuthType.SERVICE_PRINCIPAL,
            organization=organization,
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id
        )
        return cls(config)
