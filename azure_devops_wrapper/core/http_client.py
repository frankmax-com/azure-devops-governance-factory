"""
HTTP Client for Azure DevOps API
"""

import asyncio
import json
from typing import Any, Dict, Optional, Union, List
from urllib.parse import urljoin, urlparse
import aiohttp
import structlog

from .exceptions import (
    AzureDevOpsError,
    NetworkError,
    RateLimitError,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    ValidationError,
    ServerError
)
from .rate_limiter import RateLimiter

logger = structlog.get_logger(__name__)


class HTTPClient:
    """HTTP client for Azure DevOps API calls"""
    
    def __init__(
        self,
        base_url: str,
        auth_header: Dict[str, str],
        timeout: int = 30,
        rate_limiter: Optional[RateLimiter] = None
    ):
        """Initialize HTTP client"""
        self.base_url = base_url.rstrip('/')
        self.auth_header = auth_header
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.rate_limiter = rate_limiter
        self._session = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.start()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
        
    async def start(self):
        """Start the HTTP session"""
        if self._session is None:
            connector = aiohttp.TCPConnector(
                limit=100,
                limit_per_host=10,
                keepalive_timeout=30
            )
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=self.timeout,
                headers=self.auth_header
            )
            
    async def close(self):
        """Close the HTTP session"""
        if self._session:
            await self._session.close()
            self._session = None
            
    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make GET request"""
        return await self._request('GET', endpoint, params=params, headers=headers)
    
    async def get_json(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make GET request and return JSON (alias for get)"""
        return await self.get(endpoint, params=params, headers=headers)
        
    async def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], List[Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make POST request"""
        return await self._request('POST', endpoint, data=data, params=params, headers=headers)
        
    async def put(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], List[Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make PUT request"""
        return await self._request('PUT', endpoint, data=data, params=params, headers=headers)
        
    async def patch(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], List[Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make PATCH request"""
        return await self._request('PATCH', endpoint, data=data, params=params, headers=headers)
        
    async def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make DELETE request"""
        return await self._request('DELETE', endpoint, params=params, headers=headers)
        
    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], List[Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with error handling and rate limiting"""
        
        # Apply rate limiting
        if self.rate_limiter:
            await self.rate_limiter.acquire()
            
        # Ensure session is started
        if not self._session:
            await self.start()
            
        # Build URL
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))
        
        # Prepare headers
        request_headers = {}
        if headers:
            request_headers.update(headers)
            
        # Prepare data
        json_data = None
        if data is not None:
            if isinstance(data, (dict, list)):
                json_data = data
                request_headers['Content-Type'] = 'application/json'
            else:
                raise ValidationError(f"Unsupported data type: {type(data)}")
                
        try:
            logger.debug(
                "Making HTTP request",
                method=method,
                url=url,
                params=params,
                headers=list(request_headers.keys()) if request_headers else None
            )
            
            async with self._session.request(
                method=method,
                url=url,
                json=json_data,
                params=params,
                headers=request_headers
            ) as response:
                
                # Handle rate limiting
                if response.status == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    raise RateLimitError(f"Rate limit exceeded. Retry after {retry_after} seconds")
                    
                # Read response text
                response_text = await response.text()
                
                # Parse JSON response if possible
                try:
                    response_data = json.loads(response_text) if response_text else {}
                except json.JSONDecodeError:
                    response_data = {"text": response_text}
                    
                # Handle HTTP errors
                if not response.ok:
                    await self._handle_error_response(response, response_data)
                    
                logger.debug(
                    "HTTP request successful",
                    method=method,
                    url=url,
                    status=response.status
                )
                
                return response_data
                
        except aiohttp.ClientError as e:
            logger.error("Network error during HTTP request", error=str(e), url=url)
            raise NetworkError(f"Network error: {e}")
        except asyncio.TimeoutError:
            logger.error("Timeout during HTTP request", url=url)
            raise NetworkError("Request timeout")
        except Exception as e:
            logger.error("Unexpected error during HTTP request", error=str(e), url=url)
            raise AzureDevOpsError(f"HTTP request failed: {e}")
            
    async def _handle_error_response(self, response: aiohttp.ClientResponse, data: Dict[str, Any]):
        """Handle HTTP error responses"""
        status_code = response.status
        error_message = data.get('message') or data.get('error', {}).get('message') or f"HTTP {status_code}"
        
        logger.warning(
            "HTTP error response",
            status=status_code,
            error=error_message,
            url=str(response.url)
        )
        
        if status_code == 401:
            raise AuthenticationError(f"Authentication failed: {error_message}")
        elif status_code == 403:
            raise AuthorizationError(f"Access forbidden: {error_message}")
        elif status_code == 404:
            raise ResourceNotFoundError(f"Resource not found: {error_message}")
        elif status_code == 400:
            raise ValidationError(f"Bad request: {error_message}")
        elif 500 <= status_code < 600:
            raise ServerError(f"Server error: {error_message}")
        else:
            raise AzureDevOpsError(f"HTTP {status_code}: {error_message}")
