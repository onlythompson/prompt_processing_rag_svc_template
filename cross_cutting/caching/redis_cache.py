import redis.asyncio as redis
from functools import wraps
import json
from typing import Any, Callable
import pickle
from pydantic import BaseModel

class CacheConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    prefix: str = "rag:"
    ttl: int = 3600  # Default TTL: 1 hour

class CacheMetrics(BaseModel):
    hits: int = 0
    misses: int = 0

class RedisCache:
    def __init__(self, config: CacheConfig = CacheConfig()):
        self.config = config
        self.redis = redis.Redis(host=config.host, port=config.port, db=config.db)
        self.metrics = CacheMetrics()

    async def get(self, key: str) -> Any:
        full_key = f"{self.config.prefix}{key}"
        value = await self.redis.get(full_key)
        if value:
            self.metrics.hits += 1
            return self._deserialize(value)
        self.metrics.misses += 1
        return None

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        full_key = f"{self.config.prefix}{key}"
        serialized_value = self._serialize(value)
        if ttl is None:
            ttl = self.config.ttl
        await self.redis.set(full_key, serialized_value, ex=ttl)

    async def delete(self, key: str) -> None:
        full_key = f"{self.config.prefix}{key}"
        await self.redis.delete(full_key)

    async def clear(self) -> None:
        keys = await self.redis.keys(f"{self.config.prefix}*")
        if keys:
            await self.redis.delete(*keys)

    def _serialize(self, value: Any) -> bytes:
        if isinstance(value, (str, int, float, bool)):
            return json.dumps(value).encode('utf-8')
        return pickle.dumps(value)

    def _deserialize(self, value: bytes) -> Any:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return pickle.loads(value)

    async def get_metrics(self) -> CacheMetrics:
        return self.metrics

# Global cache instance
cache = RedisCache()

def cached(ttl: int = None):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create a cache key based on the function name and arguments
            key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get the result from cache
            cached_result = await cache.get(key)
            if cached_result is not None:
                return cached_result
            
            # If not in cache, call the function
            result = await func(*args, **kwargs)
            
            # Store the result in cache
            await cache.set(key, result, ttl)
            
            return result
        return wrapper
    return decorator

# Example usage
@cached(ttl=300)  # Cache for 5 minutes
async def get_expensive_data(param: str) -> dict:
    # Simulate an expensive operation
    # In a real scenario, this might be a database query or an API call
    return {"data": f"Expensive result for {param}"}

# Utility function to manually interact with cache
async def manual_cache_operation(operation: str, key: str, value: Any = None, ttl: int = None) -> Any:
    if operation == "get":
        return await cache.get(key)
    elif operation == "set":
        await cache.set(key, value, ttl)
    elif operation == "delete":
        await cache.delete(key)
    else:
        raise ValueError("Invalid operation. Use 'get', 'set', or 'delete'.")

# Function to get cache metrics
async def get_cache_metrics() -> CacheMetrics:
    return await cache.get_metrics()