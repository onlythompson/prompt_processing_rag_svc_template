import asyncio
from functools import wraps
from datetime import datetime, timedelta
from typing import Callable, Any

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "CLOSED"

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if self.state == "OPEN":
                if datetime.now() - self.last_failure_time > timedelta(seconds=self.recovery_timeout):
                    self.state = "HALF-OPEN"
                else:
                    raise Exception("Circuit is OPEN")
            
            try:
                result = await func(*args, **kwargs)
                if self.state == "HALF-OPEN":
                    self.state = "CLOSED"
                    self.failures = 0
                return result
            except Exception as e:
                self.failures += 1
                self.last_failure_time = datetime.now()
                if self.failures >= self.failure_threshold:
                    self.state = "OPEN"
                raise e
        
        return wrapper

circuit_breaker = CircuitBreaker()

# @circuit_breaker
# async def example_function():
#     # Your function logic here
#     pass