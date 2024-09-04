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