"""
Redis cache configuration and initialization
"""

import redis.asyncio as redis
import json
from typing import Optional, Any
import structlog

from src.core.config import get_settings

settings = get_settings()
logger = structlog.get_logger(__name__)

# Redis connection pool
redis_pool: Optional[redis.ConnectionPool] = None
redis_client: Optional[redis.Redis] = None


async def init_cache():
    """Initialize Redis cache connection"""
    global redis_pool, redis_client
    
    try:
        logger.info("Initializing Redis cache connection")
        
        redis_pool = redis.ConnectionPool.from_url(
            settings.REDIS_URL,
            max_connections=20,
            retry_on_timeout=True
        )
        
        redis_client = redis.Redis(connection_pool=redis_pool)
        
        # Test connection
        await redis_client.ping()
        
        logger.info("Redis cache initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize Redis cache", error=str(e))
        raise


async def get_cache() -> redis.Redis:
    """Get Redis client instance"""
    if redis_client is None:
        await init_cache()
    return redis_client


class CacheManager:
    """Redis cache management utilities"""
    
    def __init__(self):
        self.redis = None
    
    async def _get_redis(self):
        """Get Redis client"""
        if self.redis is None:
            self.redis = await get_cache()
        return self.redis
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            redis_client = await self._get_redis()
            value = await redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error("Cache get error", key=key, error=str(e))
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Set value in cache with TTL"""
        try:
            redis_client = await self._get_redis()
            serialized_value = json.dumps(value, default=str)
            await redis_client.setex(key, ttl, serialized_value)
            return True
        except Exception as e:
            logger.error("Cache set error", key=key, error=str(e))
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            redis_client = await self._get_redis()
            await redis_client.delete(key)
            return True
        except Exception as e:
            logger.error("Cache delete error", key=key, error=str(e))
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            redis_client = await self._get_redis()
            return await redis_client.exists(key) > 0
        except Exception as e:
            logger.error("Cache exists error", key=key, error=str(e))
            return False
    
    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern"""
        try:
            redis_client = await self._get_redis()
            keys = await redis_client.keys(pattern)
            if keys:
                return await redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error("Cache invalidate pattern error", pattern=pattern, error=str(e))
            return 0


# Global cache manager instance
cache_manager = CacheManager()
