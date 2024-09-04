from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # MongoDB settings
    MONGODB_URL: str = Field(..., env="MONGODB_URL")
    MONGODB_DB_NAME: str = Field("rag_db", env="MONGODB_DB_NAME")
    DOCUMENTS_COLLECTION: str = Field("documents", env="DOCUMENTS_COLLECTION")

    # LLM settings
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    OPENAI_LLM_MODEL_NAME: str = Field("gpt-3.5-turbo", env="LLM_MODEL_NAME")
    OPENAI_LLM_TEMPERATURE: float = Field(0.7, env="LLM_TEMPERATURE")
    OPENAI_LLM_MAX_TOKENS: int = Field(150, env="LLM_MAX_TOKENS")

    # Vector store settings
    VECTOR_STORE_PATH: str = Field("vector_store", env="VECTOR_STORE_PATH")

    # API settings
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
