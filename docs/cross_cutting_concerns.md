## Caching

This implementation uses Redis for caching, which can significantly improve performance in your RAG-powered microservice by storing and retrieving frequently accessed data quickly.


```python
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

```

Now, let's break down this implementation:

1. We define a `CacheConfig` class to store Redis connection details and caching parameters.

2. We create a `CacheMetrics` class to track cache hits and misses.

3. The `RedisCache` class provides the core functionality:
   - Asynchronous methods for getting, setting, and deleting cache entries.
   - Key prefixing to avoid key collisions.
   - Serialization and deserialization of values (supporting both JSON for simple types and pickle for complex objects).
   - TTL support for cache entries.

4. We provide a `cached` decorator that can be used to easily cache function results.

5. A global `cache` instance is created for easy access throughout the application.

6. We include utility functions for manual cache operations and retrieving cache metrics.

To use this in your application:

1. First, ensure you have the required dependencies installed:
   ```
   pip install redis pydantic
   ```

2. You can use the decorator on functions that you want to cache:

   ```python
   from cross_cutting.caching.redis_cache import cached

   @cached(ttl=600)  # Cache for 10 minutes
   async def my_expensive_rag_function(query: str) -> dict:
       # Your expensive RAG logic here
       result = await perform_rag_operation(query)
       return result
   ```

3. For manual cache operations:

   ```python
   from cross_cutting.caching.redis_cache import manual_cache_operation

   async def some_function():
       # Manually set a cache entry
       await manual_cache_operation("set", "my_key", "my_value", ttl=300)
       
       # Manually get a cache entry
       value = await manual_cache_operation("get", "my_key")
       
       # Manually delete a cache entry
       await manual_cache_operation("delete", "my_key")
   ```

4. To get cache metrics:

   ```python
   from cross_cutting.caching.redis_cache import get_cache_metrics

   async def log_cache_metrics():
       metrics = await get_cache_metrics()
       print(f"Cache hits: {metrics.hits}")
       print(f"Cache misses: {metrics.misses}")
   ```

5. If you need to customize the Redis connection, you can do so when initializing your application:

   ```python
   from cross_cutting.caching.redis_cache import RedisCache, CacheConfig, cache

   custom_config = CacheConfig(host="my-redis-server.com", port=6380, prefix="myapp:")
   cache = RedisCache(custom_config)
   ```

This implementation provides several benefits:

1. **Performance Improvement**: By caching expensive operations, you can significantly reduce response times for frequently accessed data.

2. **Flexibility**: The decorator allows for easy integration into existing code, while the manual cache operations provide more control when needed.

3. **Metrics**: The built-in metrics for cache hits and misses can help you monitor and optimize your caching strategy.

4. **Asynchronous Operation**: The implementation is designed to work asynchronously, fitting well with FastAPI and other async frameworks.

5. **Serialization**: The cache can handle both simple and complex Python objects, making it versatile for different use cases.

Remember to monitor your cache usage and adjust TTLs as needed. Caching can greatly improve performance, but it's important to ensure that cached data doesn't become stale, especially in a RAG system where fresh, accurate information is crucial.

## Prompt Compression

This implementation uses LLMLingua for prompt compression, which can help reduce token usage and potentially improve performance in your RAG-powered microservice.

The implementation for `llm_lingua.py`:

```python
from llm_lingua import PromptCompressor
from functools import wraps
from typing import Callable, Any
import asyncio
from pydantic import BaseModel

class CompressionResult(BaseModel):
    original_prompt: str
    compressed_prompt: str
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float

class LLMCompressor:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.compressor = PromptCompressor(model_name=model_name)
    
    async def compress(self, prompt: str, ratio: float = 0.5) -> CompressionResult:
        loop = asyncio.get_event_loop()
        compressed_prompt = await loop.run_in_executor(
            None, self.compressor.compress_prompt, prompt, ratio
        )
        
        original_tokens = len(prompt.split())
        compressed_tokens = len(compressed_prompt.split())
        compression_ratio = 1 - (compressed_tokens / original_tokens)
        
        return CompressionResult(
            original_prompt=prompt,
            compressed_prompt=compressed_prompt,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=compression_ratio
        )

def compress_prompt(ratio: float = 0.5):
    compressor = LLMCompressor()
    
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if 'prompt' in kwargs:
                compression_result = await compressor.compress(kwargs['prompt'], ratio)
                kwargs['prompt'] = compression_result.compressed_prompt
                kwargs['compression_result'] = compression_result
            return await func(*args, **kwargs)
        return wrapper
    
    return decorator

# Example usage
@compress_prompt(ratio=0.6)
async def process_query(prompt: str, compression_result: CompressionResult = None):
    # Your query processing logic here
    print(f"Processing compressed prompt: {prompt}")
    if compression_result:
        print(f"Compression ratio: {compression_result.compression_ratio:.2%}")
    # ... rest of the processing logic

# Utility function for manual compression
async def manual_compress(prompt: str, ratio: float = 0.5) -> CompressionResult:
    compressor = LLMCompressor()
    return await compressor.compress(prompt, ratio)

```

Now, let's break down this implementation:

1. We define a `CompressionResult` class to store and return detailed information about the compression process.

2. The `LLMCompressor` class wraps the LLMLingua `PromptCompressor`, providing an asynchronous interface for compression.

3. The `compress_prompt` decorator can be used to automatically compress prompts in functions that accept a `prompt` keyword argument.

4. We provide a `manual_compress` function for cases where you need more control over the compression process.

5. The compression is performed asynchronously using `run_in_executor` to prevent blocking the event loop.

To use this in your application:

1. First, ensure you have LLMLingua installed:
   ```
   pip install llm-lingua
   ```

2. You can use the decorator on functions that process prompts:

   ```python
   from cross_cutting.compression.llm_lingua import compress_prompt, CompressionResult

   @compress_prompt(ratio=0.6)
   async def my_rag_function(prompt: str, compression_result: CompressionResult = None):
       # Your RAG logic here
       print(f"Original prompt tokens: {compression_result.original_tokens}")
       print(f"Compressed prompt tokens: {compression_result.compressed_tokens}")
       print(f"Compression ratio: {compression_result.compression_ratio:.2%}")
       # Use the compressed prompt for your LLM call
       response = await llm_call(prompt)
       return response
   ```

3. For manual compression:

   ```python
   from cross_cutting.compression.llm_lingua import manual_compress

   async def some_function():
       original_prompt = "Your long prompt here..."
       compression_result = await manual_compress(original_prompt, ratio=0.7)
       compressed_prompt = compression_result.compressed_prompt
       # Use compressed_prompt in your LLM call
   ```

This implementation provides several benefits:

1. **Token Reduction**: By compressing prompts, you can potentially reduce the number of tokens used in LLM calls, which can lead to cost savings and improved performance.

2. **Flexibility**: The decorator allows for easy integration into existing code, while the manual compression function provides more control when needed.

3. **Metrics**: The `CompressionResult` object provides detailed information about the compression process, which can be useful for monitoring and optimization.

4. **Asynchronous Operation**: The implementation is designed to work asynchronously, fitting well with FastAPI and other async frameworks.

Remember to monitor the quality of results when using compression, as there's always a trade-off between compression ratio and maintaining the original meaning of the prompt. You may need to adjust the compression ratio based on your specific use case and requirements.


## Observability 

This include implementations for logging, metrics, and tracing, which are crucial for maintaining observability in your RAG-powered microservice.



1. `logging.py`:

```python
import logging
import json
from pythonjsonlogger import jsonlogger
from functools import wraps
import asyncio

# Configure the JSON logger
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

def log_async(level, message, **kwargs):
    """
    Asynchronous logging function.
    """
    log_data = {
        "message": message,
        **kwargs
    }
    logger.log(level, json.dumps(log_data))

async def async_log_info(message, **kwargs):
    """
    Asynchronous info logging.
    """
    await asyncio.to_thread(log_async, logging.INFO, message, **kwargs)

async def async_log_error(message, **kwargs):
    """
    Asynchronous error logging.
    """
    await asyncio.to_thread(log_async, logging.ERROR, message, **kwargs)

def log_exception(func):
    """
    Decorator to log exceptions
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            await async_log_error(
                f"Exception in {func.__name__}",
                exception=str(e),
                args=str(args),
                kwargs=str(kwargs)
            )
            raise
    return wrapper

```

2. `metrics.py`:

```python
from prometheus_client import Counter, Histogram, Gauge
from functools import wraps
import time

# Define metrics
REQUESTS_TOTAL = Counter(
    'rag_requests_total', 
    'Total number of RAG requests',
    ['endpoint']
)

RESPONSE_TIME = Histogram(
    'rag_response_time_seconds', 
    'Response time in seconds',
    ['endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'rag_active_requests',
    'Number of active RAG requests',
    ['endpoint']
)

LLM_TOKEN_USAGE = Counter(
    'llm_token_usage_total',
    'Total number of tokens used by LLM',
    ['model']
)

def track_request_metrics(endpoint):
    """
    Decorator to track request metrics
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            REQUESTS_TOTAL.labels(endpoint=endpoint).inc()
            ACTIVE_REQUESTS.labels(endpoint=endpoint).inc()
            start_time = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                duration = time.time() - start_time
                RESPONSE_TIME.labels(endpoint=endpoint).observe(duration)
                ACTIVE_REQUESTS.labels(endpoint=endpoint).dec()
        return wrapper
    return decorator

def track_token_usage(model: str, token_count: int):
    """
    Track token usage for LLM
    """
    LLM_TOKEN_USAGE.labels(model=model).inc(token_count)

```

3. `tracing.py`:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from fastapi import FastAPI
from functools import wraps

# Initialize tracing
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

def init_tracing(app: FastAPI):
    """
    Initialize tracing for FastAPI app
    """
    FastAPIInstrumentor.instrument_app(app)

def trace_async(name: str):
    """
    Decorator to create a span for an async function
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(name):
                return await func(*args, **kwargs)
        return wrapper
    return decorator

async def add_span_event(span: trace.Span, name: str, attributes: dict = None):
    """
    Add an event to the current span
    """
    span.add_event(name, attributes=attributes)

async def set_span_attribute(span: trace.Span, key: str, value: str):
    """
    Set an attribute on the current span
    """
    span.set_attribute(key, value)

```

These implementations provide a solid foundation for observability in your RAG-powered microservice:

1. `logging.py`:
   - Uses JSON logging for structured logs.
   - Provides asynchronous logging functions.
   - Includes a decorator for exception logging.

2. `metrics.py`:
   - Defines Prometheus metrics for request count, response time, active requests, and LLM token usage.
   - Includes a decorator to track request metrics.
   - Provides a function to track LLM token usage.

3. `tracing.py`:
   - Sets up OpenTelemetry tracing with Jaeger exporter.
   - Provides a function to initialize tracing for a FastAPI app.
   - Includes a decorator for creating spans around async functions.
   - Offers utility functions for adding events and attributes to spans.

To use these in your application:

1. Install required dependencies:
   ```
   pip install python-json-logger prometheus-client opentelemetry-api opentelemetry-sdk opentelemetry-exporter-jaeger opentelemetry-instrumentation-fastapi
   ```

2. In your main FastAPI application file:
   ```python
   from fastapi import FastAPI
   from cross_cutting.observability.tracing import init_tracing
   
   app = FastAPI()
   init_tracing(app)
   ```

3. In your service functions:
   ```python
   from cross_cutting.observability.logging import async_log_info, log_exception
   from cross_cutting.observability.metrics import track_request_metrics, track_token_usage
   from cross_cutting.observability.tracing import trace_async

   @trace_async("process_query")
   @track_request_metrics("process_query")
   @log_exception
   async def process_query(query: str):
       await async_log_info("Processing query", query=query)
       # Your processing logic here
       track_token_usage("gpt-3.5-turbo", 100)  # Example token usage
       return result
   ```

This setup provides comprehensive observability for your RAG-powered microservice, allowing you to monitor performance, track errors, and analyze request flows effectively.

## Resilience

This include implementations for circuit breaker and rate limiter, which are crucial for building a resilient microservice.


1. `circuit_breaker.py`:

```python
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

    async def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
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

@circuit_breaker
async def example_function():
    # Your function logic here
    pass

```

2. `rate_limiter.py`:

```python
import asyncio
from functools import wraps
import time
from typing import Callable, Any

class RateLimiter:
    def __init__(self, max_calls: int, time_frame: int):
        self.max_calls = max_calls
        self.time_frame = time_frame
        self.calls = []

    async def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
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

@rate_limiter
async def example_function():
    # Your function logic here
    pass

```

Now, let's create a `resilience.py` file that combines both circuit breaker and rate limiter functionalities:

```python
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
@resilient(max_calls=5, time_frame=10, failure_threshold=3, recovery_timeout=20)
async def resilient_function():
    # Your function logic here
    pass

```

These implementations provide a solid foundation for resilience in your RAG-powered microservice:

1. `circuit_breaker.py`:
   - Implements a circuit breaker pattern with three states: CLOSED, OPEN, and HALF-OPEN.
   - Tracks failures and opens the circuit when the failure threshold is reached.
   - Implements a recovery timeout before attempting to close the circuit again.

2. `rate_limiter.py`:
   - Implements a sliding window rate limiter.
   - Limits the number of calls to a function within a specified time frame.
   - Uses asyncio.sleep to delay execution when the rate limit is exceeded.

3. `resilience.py`:
   - Combines both circuit breaker and rate limiter into a single decorator.
   - Allows easy application of both resilience patterns to any async function.

To use these in your application:

1. Apply the resilience decorator to your service functions:

```python
from cross_cutting.resilience.resilience import resilient

@resilient(max_calls=100, time_frame=60, failure_threshold=5, recovery_timeout=30)
async def process_query(query: str):
    # Your processing logic here
    pass
```

This setup provides robust resilience for your RAG-powered microservice, protecting it from cascading failures and overload. The circuit breaker prevents repeated calls to failing services, while the rate limiter ensures that the service doesn't receive more requests than it can handle.

These implementations are designed to work with asynchronous functions, making them compatible with FastAPI and the rest of your async-based microservice architecture.

## Security

This include implementations for authentication and authorization, which are crucial for securing your RAG-powered microservice.

1. `authentication.py`:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

# Configuration
SECRET_KEY = "YOUR_SECRET_KEY"  # Change this!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

```

2. `authorization.py`:

```python
from fastapi import Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from .authentication import get_current_active_user

class UserInDB(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    hashed_password: str
    roles: List[str] = []

# This would typically come from a database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "roles": ["user"]
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderland",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "roles": ["user", "admin"]
    }
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def has_role(required_roles: List[str]):
    async def role_checker(current_user: UserInDB = Depends(get_current_active_user)):
        for role in required_roles:
            if role in current_user.roles:
                return current_user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return role_checker

# Example usage
async def get_admin_data(current_user: UserInDB = Depends(has_role(["admin"]))):
    return {"message": "This is admin data", "user": current_user.username}

async def get_user_data(current_user: UserInDB = Depends(has_role(["user"]))):
    return {"message": "This is user data", "user": current_user.username}

```

A `security.py` file that combines both authentication and authorization functionalities:

```python
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from .authentication import (
    Token, User, authenticate_user, create_access_token,
    get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from .authorization import has_role, get_admin_data, get_user_data
from datetime import timedelta

def setup_security(app: FastAPI):
    @app.post("/token", response_model=Token)
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        user = await authenticate_user(fake_users_db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @app.get("/users/me/", response_model=User)
    async def read_users_me(current_user: User = Depends(get_current_active_user)):
        return current_user

    @app.get("/admin/")
    async def read_admin_data(admin_data: dict = Depends(get_admin_data)):
        return admin_data

    @app.get("/user/")
    async def read_user_data(user_data: dict = Depends(get_user_data)):
        return user_data

# Usage in main.py
# from cross_cutting.security.security import setup_security
# app = FastAPI()
# setup_security(app)

```

These implementations provide a solid foundation for security in your RAG-powered microservice:

1. `authentication.py`:
   - Implements JWT-based authentication.
   - Provides functions for password hashing and verification.
   - Includes user management and token creation.

2. `authorization.py`:
   - Implements role-based access control.
   - Provides a decorator for checking user roles.
   - Includes example endpoints for different role levels.

3. `security.py`:
   - Combines authentication and authorization.
   - Sets up security-related endpoints (login, user info).
   - Provides a function to easily set up security in the main FastAPI app.

To use these in your application:

1. In your main FastAPI application file:

```python
from fastapi import FastAPI
from cross_cutting.security.security import setup_security

app = FastAPI()
setup_security(app)

# Your other routes and app setup here
```

2. In your service functions or routes:

```python
from fastapi import Depends
from cross_cutting.security.authentication import get_current_active_user
from cross_cutting.security.authorization import has_role

@app.get("/protected-route")
async def protected_route(current_user: User = Depends(get_current_active_user)):
    return {"message": "This is a protected route", "user": current_user.username}

@app.get("/admin-only")
async def admin_only(admin_user: User = Depends(has_role(["admin"]))):
    return {"message": "This is an admin-only route", "user": admin_user.username}
```

This setup provides robust security for your RAG-powered microservice, implementing both authentication and authorization. It uses JWT for stateless authentication and role-based access control for fine-grained permissions.

Remember to replace `"YOUR_SECRET_KEY"` in `authentication.py` with a strong, unique secret key for your application.

Also, note that the `fake_users_db` is just for demonstration. In a real application, you would replace this with actual database calls to retrieve user information.

