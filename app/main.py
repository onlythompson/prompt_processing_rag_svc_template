import signal
from cross_cutting.resilience.resilience import resilient
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.core.config import Settings
from app.core.dependencies import get_data_sync_service, get_llm_service, get_settings, get_mongodb, get_vector_store
from app.db.mongodb import MongoDB
from app.db.vector_store import VectorStore
from app.core.exceptions import RAGBaseException, rag_exception_handler
from app.services.data_sync_service import DataSyncService
from app.services.llm_service import LLMService
from app.api.v1.routes import admin_routes, query_routes


def create_app() -> FastAPI:
    app = FastAPI(
        title="Microservice RAG",
        description="A Retrieval-Augmented Generation (RAG) Powered Microservice",
        summary="This microservice provides an API for querying and managing documents.",
        version="0.0.1",
        )
    app.include_router(query_routes, prefix="/api/v1", tags=["queries"])
    app.include_router(admin_routes, prefix="/api/vi/admin", tags=["admin"])

    @app.exception_handler(RAGBaseException)
    async def handle_rag_exception(request: Request, exc: RAGBaseException):
        http_exc = rag_exception_handler(exc)
        return JSONResponse(
            status_code=http_exc.status_code,
            content={"detail": http_exc.detail}
        )

    @app.on_event("startup")
    @resilient(max_calls=5, time_frame=60, failure_threshold=3, recovery_timeout=30)
    async def startup_event():
        try:
            settings = get_settings()
            mongodb = get_mongodb(settings)
            vector_store = get_vector_store()
            llm_service = get_llm_service()
            data_sync_service = get_data_sync_service()

            # Initialize MongoDB connection
            await mongodb.connect(settings.MONGODB_DB_NAME)

            # Initialize vector store with documents from MongoDB
            documents = await mongodb.find_documents(settings.DOCUMENTS_COLLECTION, {})
            await vector_store.initialize(documents, settings.OPENAI_API_KEY)

            # Initialize LLM service
            llm_service.initialize(settings)
            await data_sync_service.initialize(mongodb, llm_service, vector_store)
        except Exception as e:
            app.state.startup_error = str(e)
            raise HTTPException(status_code=500, detail=f"Startup failed: {str(e)}")

    @app.on_event("shutdown")
    @resilient(max_calls=5, time_frame=60, failure_threshold=3, recovery_timeout=30)
    async def shutdown_event():
        try:
            settings = get_settings()
            mongodb = get_mongodb(settings)
            # Close MongoDB connection
            await mongodb.close()
        except Exception as e:
            print(f"Shutdown error: {str(e)}")

    @app.middleware("http")
    async def check_startup_error(request: Request, call_next):
        if hasattr(request.app.state, 'startup_error'):
            return JSONResponse(
                status_code=503,
                content={"detail": f"Application is not ready: {request.app.state.startup_error}"}
            )
        return await call_next(request)

    return app


app = create_app()

def handle_sigterm(*args):
    raise KeyboardInterrupt()

if __name__ == "__main__":
    import uvicorn
    
    signal.signal(signal.SIGINT, handle_sigterm)
    signal.signal(signal.SIGTERM, handle_sigterm)
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)