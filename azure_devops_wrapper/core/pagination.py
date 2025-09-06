"""
Pagination helper for Azure DevOps API responses
"""

import re
from typing import Optional, Dict, Any, List, AsyncGenerator, Callable, Awaitable, TypeVar, Generic
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

from .exceptions import PaginationError

T = TypeVar('T')


@dataclass
class PaginationInfo:
    """Information about pagination state."""
    continuation_token: Optional[str] = None
    total_count: Optional[int] = None
    page_size: Optional[int] = None
    has_more: bool = False
    current_page: int = 1


class PaginationHelper(Generic[T]):
    """Helper class for handling Azure DevOps API pagination."""
    
    def __init__(
        self,
        request_func: Callable[..., Awaitable[Dict[str, Any]]],
        page_size: int = 100,
        max_pages: Optional[int] = None
    ):
        self.request_func = request_func
        self.page_size = page_size
        self.max_pages = max_pages
        self.pagination_info = PaginationInfo(page_size=page_size)
    
    async def get_page(
        self,
        continuation_token: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Get a single page of results."""
        params = kwargs.copy()
        
        # Add pagination parameters
        if self.page_size:
            params['$top'] = self.page_size
        
        if continuation_token:
            params['continuationToken'] = continuation_token
        
        try:
            response = await self.request_func(**params)
            return response
        except Exception as e:
            raise PaginationError(f"Failed to fetch page: {str(e)}") from e
    
    async def get_all_pages(self, **kwargs) -> List[Dict[str, Any]]:
        """Get all pages and return combined results."""
        all_items = []
        continuation_token = None
        page_count = 0
        
        while True:
            if self.max_pages and page_count >= self.max_pages:
                break
            
            response = await self.get_page(continuation_token=continuation_token, **kwargs)
            
            # Extract items from response
            items = self._extract_items(response)
            if items:
                all_items.extend(items)
            
            # Check for continuation
            continuation_token = self._extract_continuation_token(response)
            if not continuation_token:
                break
            
            page_count += 1
            self.pagination_info.current_page = page_count + 1
        
        return all_items
    
    async def iterate_pages(self, **kwargs) -> AsyncGenerator[List[T], None]:
        """Iterate through pages yielding items from each page."""
        continuation_token = None
        page_count = 0
        
        while True:
            if self.max_pages and page_count >= self.max_pages:
                break
            
            response = await self.get_page(continuation_token=continuation_token, **kwargs)
            
            # Extract items from response
            items = self._extract_items(response)
            if items:
                yield items
            
            # Update pagination info
            self.pagination_info.continuation_token = continuation_token
            self.pagination_info.total_count = response.get('count')
            self.pagination_info.current_page = page_count + 1
            
            # Check for continuation
            continuation_token = self._extract_continuation_token(response)
            self.pagination_info.has_more = bool(continuation_token)
            
            if not continuation_token:
                break
            
            page_count += 1
    
    async def iterate_items(self, **kwargs) -> AsyncGenerator[T, None]:
        """Iterate through all items across all pages."""
        async for page_items in self.iterate_pages(**kwargs):
            for item in page_items:
                yield item
    
    def _extract_items(self, response: Dict[str, Any]) -> List[Any]:
        """Extract items from API response."""
        # Common patterns in Azure DevOps API responses
        if 'value' in response:
            return response['value']
        elif 'results' in response:
            return response['results']
        elif 'items' in response:
            return response['items']
        elif isinstance(response, list):
            return response
        else:
            # If response is a single item, wrap in list
            return [response] if response else []
    
    def _extract_continuation_token(self, response: Dict[str, Any]) -> Optional[str]:
        """Extract continuation token from API response."""
        # Check common locations for continuation tokens
        if 'continuationToken' in response:
            return response['continuationToken']
        elif 'x-ms-continuationtoken' in response:
            return response['x-ms-continuationtoken']
        elif 'nextLink' in response:
            return self._extract_token_from_url(response['nextLink'])
        elif '@odata.nextLink' in response:
            return self._extract_token_from_url(response['@odata.nextLink'])
        
        return None
    
    def _extract_token_from_url(self, url: str) -> Optional[str]:
        """Extract continuation token from URL."""
        try:
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)
            
            # Check various parameter names used for continuation tokens
            token_params = ['continuationToken', '$skip', 'skipToken', 'token']
            
            for param in token_params:
                if param in query_params:
                    return query_params[param][0]
            
            return None
        except Exception:
            return None


class CursorPagination:
    """Cursor-based pagination for APIs that support it."""
    
    def __init__(self, page_size: int = 100):
        self.page_size = page_size
        self.cursor: Optional[str] = None
        self.has_more = True
    
    def get_params(self) -> Dict[str, Any]:
        """Get pagination parameters for API request."""
        params = {'$top': self.page_size}
        if self.cursor:
            params['$skip'] = self.cursor
        return params
    
    def update_from_response(self, response: Dict[str, Any]) -> None:
        """Update pagination state from API response."""
        items = response.get('value', [])
        
        if len(items) < self.page_size:
            self.has_more = False
        else:
            # For skip-based pagination, increment by page size
            current_skip = int(self.cursor) if self.cursor else 0
            self.cursor = str(current_skip + self.page_size)


class OffsetPagination:
    """Offset-based pagination."""
    
    def __init__(self, page_size: int = 100):
        self.page_size = page_size
        self.offset = 0
        self.total_count: Optional[int] = None
        self.has_more = True
    
    def get_params(self) -> Dict[str, Any]:
        """Get pagination parameters for API request."""
        return {
            '$top': self.page_size,
            '$skip': self.offset
        }
    
    def update_from_response(self, response: Dict[str, Any]) -> None:
        """Update pagination state from API response."""
        items = response.get('value', [])
        self.total_count = response.get('count')
        
        if len(items) < self.page_size:
            self.has_more = False
        elif self.total_count and (self.offset + len(items)) >= self.total_count:
            self.has_more = False
        else:
            self.offset += len(items)


def create_paginator(
    request_func: Callable[..., Awaitable[Dict[str, Any]]],
    pagination_type: str = "continuation",
    page_size: int = 100,
    max_pages: Optional[int] = None
) -> PaginationHelper:
    """Factory function to create appropriate paginator."""
    return PaginationHelper(
        request_func=request_func,
        page_size=page_size,
        max_pages=max_pages
    )
