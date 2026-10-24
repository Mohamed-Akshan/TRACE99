import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.utils.logging import setup_logging
from app.api.auth import router as auth_router


# Load settings and prepare logging.
settings = get_settings()
setup_logging()

logger = logging.getLogger(__name__)


# Create the FastAPI application.
app = FastAPI(
    title="TRACE99 API",
    description="AI-powered incident investigation platform",
    version="1.0.0"
)


# Allow our React frontend to contact FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


# Connect signup, login, and profile endpoints.
app.include_router(auth_router)


# Confirm that the API server is running.
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "application": "TRACE99"
    }


logger.info("TRACE99 API initialized")
