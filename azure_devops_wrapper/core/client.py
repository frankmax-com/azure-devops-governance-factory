"""
HTTP client for Azure DevOps API with retry logic and error handling
"""

import asyncio
import time
import json
from typing import Optional, Dict, Any, Union, List
from urllib.parse import urljoin, quote
import httpx

from .auth import AuthManager
from .rate_limiter import RateLimiter, RateLimitConfig
from .exceptions import (
    AzureDevOpsError,
    TimeoutError,
    ServerError,
    create_exception_from_response
)


class HTTPClient:
    """HTTP client for Azure DevOps API with built-in retry logic and error handling."""
    
    def __init__(
        self,
        auth_manager: AuthManager,
        rate_limiter: Optional[RateLimiter] = None,
        base_url: Optional[str] = None,
        api_version: str = "7.1",
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        retry_backoff: float = 2.0
    ):
        self.auth_manager = auth_manager
        self.rate_limiter = rate_limiter or RateLimiter()
        self.base_url = base_url or f"https://dev.azure.com/{auth_manager.config.organization}/_apis"
        self.api_version = api_version
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_backoff = retry_backoff
        
        # Create HTTP client with default configuration
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=50),
            follow_redirects=True
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        **kwargs
    ) -> httpx.Response:
        """Make HTTP request with retry logic and error handling."""
        
        # Prepare URL
        url = self._build_url(endpoint)
        
        # Prepare parameters
        request_params = self._prepare_params(params)
        
        # Prepare headers
        request_headers = self._prepare_headers(headers)
        
        # Prepare data
        request_data = self._prepare_data(data)
        
        # Apply rate limiting
        await self.rate_limiter.acquire(endpoint=endpoint, method=method)
        
        # Make request with retry logic
        return await self._request_with_retry(
            method=method,
            url=url,
            params=request_params,
            headers=request_headers,
            data=request_data,
            files=files,
            stream=stream,
            **kwargs
        )
    
    async def get(self, endpoint: str, **kwargs) -> httpx.Response:
        """Make GET request."""
        return await self.request("GET", endpoint, **kwargs)
    
    async def post(self, endpoint: str, **kwargs) -> httpx.Response:
        """Make POST request."""
        return await self.request("POST", endpoint, **kwargs)
    
    async def put(self, endpoint: str, **kwargs) -> httpx.Response:
        """Make PUT request."""
        return await self.request("PUT", endpoint, **kwargs)
    
    async def patch(self, endpoint: str, **kwargs) -> httpx.Response:
        """Make PATCH request."""
        return await self.request("PATCH", endpoint, **kwargs)
    
    async def delete(self, endpoint: str, **kwargs) -> httpx.Response:
        """Make DELETE request."""
        return await self.request("DELETE", endpoint, **kwargs)
    
    async def get_json(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make GET request and return JSON response."""
        response = await self.get(endpoint, **kwargs)
        return await self._parse_json_response(response)
    
    async def post_json(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make POST request and return JSON response."""
        response = await self.post(endpoint, **kwargs)
        return await self._parse_json_response(response)
    
    async def put_json(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make PUT request and return JSON response."""
        response = await self.put(endpoint, **kwargs)
        return await self._parse_json_response(response)
    
    async def patch_json(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make PATCH request and return JSON response."""
        response = await self.patch(endpoint, **kwargs)
        return await self._parse_json_response(response)
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        # Remove leading slash if present
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        
        return urljoin(self.base_url + "/", endpoint)
    
    def _prepare_params(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Prepare query parameters."""
        request_params = {}
        
        if params:
            request_params.update(params)
        
        # Always add API version
        request_params['api-version'] = self.api_version
        
        return request_params
    
    def _prepare_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        """Prepare request headers."""
        # Get authentication headers
        request_headers = self.auth_manager.get_auth_headers()
        
        # Add custom headers
        if headers:
            request_headers.update(headers)
        
        # Add user agent
        request_headers['User-Agent'] = 'Azure-DevOps-Wrapper/1.0.0'
        
        return request_headers
    
    def _prepare_data(self, data: Optional[Union[Dict[str, Any], str, bytes]]) -> Optional[Union[str, bytes]]:
        """Prepare request data."""
        if data is None:
            return None
        
        if isinstance(data, (str, bytes)):
            return data
        
        # Convert dict to JSON
        return json.dumps(data, default=str)
    
    async def _request_with_retry(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> httpx.Response:
        """Make HTTP request with retry logic."""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.request(method, url, **kwargs)
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = response.headers.get('Retry-After')
                    self.rate_limiter.handle_rate_limit_response(retry_after)
                    
                    if attempt < self.max_retries:
                        delay = float(retry_after) if retry_after else self.retry_delay * (self.retry_backoff ** attempt)
                        await asyncio.sleep(delay)
                        continue
                
                # Check for other errors
                if response.status_code >= 400:
                    await self._handle_error_response(response)
                
                return response
                
            except httpx.TimeoutException as e:
                last_exception = TimeoutError(f"Request timeout after {self.timeout}s")
                if attempt < self.max_retries:
                    delay = self.retry_delay * (self.retry_backoff ** attempt)
                    await asyncio.sleep(delay)
                    continue
                
            except httpx.ConnectError as e:
                last_exception = AzureDevOpsError(f"Connection error: {str(e)}")
                if attempt < self.max_retries:
                    delay = self.retry_delay * (self.retry_backoff ** attempt)
                    await asyncio.sleep(delay)
                    continue
                
            except Exception as e:
                last_exception = AzureDevOpsError(f"Unexpected error: {str(e)}")
                break
        
        # If we get here, all retries failed
        if last_exception:
            raise last_exception
        else:
            raise AzureDevOpsError("Request failed after all retry attempts")
    
    async def _handle_error_response(self, response: httpx.Response) -> None:
        """Handle error responses from API."""
        try:
            error_data = response.json()
        except:
            error_data = {"message": response.text}
        
        # Extract error message
        message = error_data.get('message') or error_data.get('error', {}).get('message') or f"HTTP {response.status_code}"
        
        # Extract request ID for debugging
        request_id = response.headers.get('x-ms-request-id')
        
        # Create appropriate exception
        exception = create_exception_from_response(
            status_code=response.status_code,
            message=message,
            response_data=error_data,
            request_id=request_id
        )
        
        raise exception
    
    async def _parse_json_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Parse JSON response with error handling."""
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise AzureDevOpsError(f"Invalid JSON response: {str(e)}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get client statistics."""
        return {
            "base_url": self.base_url,
            "api_version": self.api_version,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "rate_limiter_stats": self.rate_limiter.get_stats()
        }
