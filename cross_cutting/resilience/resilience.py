from functools import wraps
from typing import Callable, Any
from .circuit_breaker import CircuitBreaker
from .rate_limiter import RateLimiter

def resilient(
    max_calls: int = 10, 
    time_frame: int = 60, 
    failure_threshold: int = 5, 
    recovery_timeout: int = 30
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    circuit_breaker = CircuitBreaker(failure_threshold, recovery_timeout)
    rate_limiter = RateLimiter(max_calls, time_frame)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        @circuit_breaker
        @rate_limiter
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper
    
    return decorator

# Example usage
# @resilient(max_calls=5, time_frame=10, failure_threshold=3, recovery_timeout=20)
# async def resilient_function():
#     # Your function logic here
#     pass