import asyncio
from functools import wraps
import time
from typing import Callable, Any

class RateLimiter:
    def __init__(self, max_calls: int, time_frame: int):
        self.max_calls = max_calls
        self.time_frame = time_frame
        self.calls = []

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_time = time.time()
            
            # Remove old calls
            self.calls = [call for call in self.calls if current_time - call < self.time_frame]
            
            if len(self.calls) >= self.max_calls:
                sleep_time = self.time_frame - (current_time - self.calls[0])
                await asyncio.sleep(sleep_time)
            
            self.calls.append(time.time())
            return await func(*args, **kwargs)
        
        return wrapper

# Example usage
rate_limiter = RateLimiter(max_calls=5, time_frame=10)  # 5 calls per 10 seconds

# @rate_limiter
# async def example_function():
#     # Your function logic here
#     pass