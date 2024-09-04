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