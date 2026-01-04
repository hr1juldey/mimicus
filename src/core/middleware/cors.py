"""CORS middleware configuration."""

from fastapi.middleware.cors import CORSMiddleware


def setup_cors_middleware(app) -> None:
    """Configure CORS middleware for FastAPI application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for development
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
        expose_headers=[
            "Content-Type",
            "X-Request-ID",
            "X-Mock-Matched",
            "X-Response-Time-Ms",
        ],
    )
