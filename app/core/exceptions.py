from fastapi import HTTPException, status

class RAGBaseException(Exception):
    """Base exception class for RAG microservice"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class RAGNotFoundException(RAGBaseException):
    """Raised when a requested resource is not found"""
    def __init__(self, resource: str, identifier: str):
        super().__init__(f"{resource} with identifier {identifier} not found")

class RAGDatabaseException(RAGBaseException):
    """Raised when there's an issue with database operations"""
    pass

class RAGVectorStoreException(RAGBaseException):
    """Raised when there's an issue with vector store operations"""
    pass

class RAGLLMException(RAGBaseException):
    """Raised when there's an issue with LLM operations"""
    pass

class RAGQueryProcessingException(RAGBaseException):
    """Raised when there's an error processing a query"""
    pass

class RAGAuthenticationException(RAGBaseException):
    """Raised when there's an authentication error"""
    pass

class RAGAuthorizationException(RAGBaseException):
    """Raised when there's an authorization error"""
    pass

class RAGRateLimitException(RAGBaseException):
    """Raised when rate limit is exceeded"""
    pass

class RAGInvalidInputException(RAGBaseException):
    """Raised when input validation fails"""
    pass

def rag_exception_handler(exc: RAGBaseException):
    """Converts RAG exceptions to HTTPExceptions"""
    if isinstance(exc, RAGNotFoundException):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    elif isinstance(exc, RAGDatabaseException):
        return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database error occurred")
    elif isinstance(exc, RAGVectorStoreException):
        return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Vector store error occurred")
    elif isinstance(exc, RAGLLMException):
        return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="LLM service error occurred")
    elif isinstance(exc, RAGQueryProcessingException):
        return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    elif isinstance(exc, RAGAuthenticationException):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    elif isinstance(exc, RAGAuthorizationException):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    elif isinstance(exc, RAGRateLimitException):
        return HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
    elif isinstance(exc, RAGInvalidInputException):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    else:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")