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