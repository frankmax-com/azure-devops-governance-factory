"""
Rate limiting for Azure DevOps API requests
"""

import time
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from collections import defaultdict, deque

from .exceptions import RateLimitError


@dataclass
class RateLimitConfig:
    """Rate limiting configuration."""
    requests_per_second: float = 10.0  # Azure DevOps default limit
    burst_size: int = 50  # Allow burst of requests
    retry_after_delay: float = 1.0  # Base delay for retry after rate limit
    max_retry_attempts: int = 3  # Maximum retry attempts
    backoff_multiplier: float = 2.0  # Exponential backoff multiplier


@dataclass
class RequestRecord:
    """Record of a request for rate limiting."""
    timestamp: float
    endpoint: str
    method: str


class TokenBucket:
    """Token bucket algorithm for rate limiting."""
    
    def __init__(self, rate: float, capacity: int):
        self.rate = rate  # Tokens per second
        self.capacity = capacity  # Maximum tokens
        self.tokens = capacity  # Current tokens
        self.last_refill = time.time()
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens. Returns True if successful."""
        self._refill()
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        
        # Add tokens based on elapsed time
        tokens_to_add = elapsed * self.rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def time_until_available(self, tokens: int = 1) -> float:
        """Calculate time until specified tokens are available."""
        self._refill()
        
        if self.tokens >= tokens:
            return 0.0
        
        tokens_needed = tokens - self.tokens
        return tokens_needed / self.rate


class RateLimiter:
    """Rate limiter for Azure DevOps API requests."""
    
    def __init__(self, config: Optional[RateLimitConfig] = None):
        self.config = config or RateLimitConfig()
        self.token_bucket = TokenBucket(
            rate=self.config.requests_per_second,
            capacity=self.config.burst_size
        )
        self.request_history: deque = deque(maxlen=1000)  # Keep last 1000 requests
        self.retry_delays: Dict[str, float] = defaultdict(float)
    
    async def acquire(self, endpoint: str = "", method: str = "GET") -> None:
        """Acquire permission to make a request."""
        attempt = 0
        
        while attempt < self.config.max_retry_attempts:
            if self.token_bucket.consume():
                # Record successful request
                self.request_history.append(RequestRecord(
                    timestamp=time.time(),
                    endpoint=endpoint,
                    method=method
                ))
                return
            
            # Calculate delay
            delay = self.token_bucket.time_until_available()
            if delay > 0:
                # Add exponential backoff for repeated failures
                retry_key = f"{method}:{endpoint}"
                if retry_key in self.retry_delays:
                    delay = max(delay, self.retry_delays[retry_key])
                    self.retry_delays[retry_key] *= self.config.backoff_multiplier
                else:
                    self.retry_delays[retry_key] = self.config.retry_after_delay
                
                await asyncio.sleep(delay)
                attempt += 1
            else:
                break
        
        if attempt >= self.config.max_retry_attempts:
            raise RateLimitError(
                f"Rate limit exceeded after {attempt} attempts for {method} {endpoint}",
                retry_after=int(self.token_bucket.time_until_available())
            )
    
    def handle_rate_limit_response(self, retry_after: Optional[str] = None) -> None:
        """Handle rate limit response from server."""
        if retry_after:
            try:
                delay = float(retry_after)
                # Update token bucket to reflect server-imposed delay
                self.token_bucket.tokens = 0
                self.token_bucket.last_refill = time.time() + delay
            except ValueError:
                pass  # Invalid retry-after header
    
    def get_stats(self) -> Dict[str, Any]:
        """Get rate limiting statistics."""
        now = time.time()
        recent_requests = [
            r for r in self.request_history 
            if now - r.timestamp < 60  # Last minute
        ]
        
        endpoint_stats = defaultdict(int)
        method_stats = defaultdict(int)
        
        for request in recent_requests:
            endpoint_stats[request.endpoint] += 1
            method_stats[request.method] += 1
        
        return {
            "current_tokens": self.token_bucket.tokens,
            "max_tokens": self.token_bucket.capacity,
            "requests_per_second": self.config.requests_per_second,
            "recent_requests_count": len(recent_requests),
            "endpoint_stats": dict(endpoint_stats),
            "method_stats": dict(method_stats),
            "retry_delays": dict(self.retry_delays)
        }
    
    def reset_retry_delays(self) -> None:
        """Reset retry delays (useful after successful requests)."""
        self.retry_delays.clear()


class GlobalRateLimiter:
    """Global rate limiter singleton for sharing across clients."""
    
    _instance: Optional[RateLimiter] = None
    _config: Optional[RateLimitConfig] = None
    
    @classmethod
    def get_instance(cls, config: Optional[RateLimitConfig] = None) -> RateLimiter:
        """Get global rate limiter instance."""
        if cls._instance is None or (config and config != cls._config):
            cls._config = config
            cls._instance = RateLimiter(config)
        return cls._instance
    
    @classmethod
    def reset(cls) -> None:
        """Reset global rate limiter."""
        cls._instance = None
        cls._config = None
