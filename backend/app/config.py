from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


# Keep all application settings in one place.
class Settings(BaseSettings):
    database_url: str

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-120b"

    gemini_embedding_model: str = "gemini-embedding-2"
    embedding_dimensions: int = 768

    pinecone_api_key: str = ""
    pinecone_index: str = "trace99-logs"

    jwt_secret_key: str
    frontend_url: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


# Load settings once and reuse them.
@lru_cache
def get_settings() -> Settings:
    return Settings()
