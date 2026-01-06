"""FastAPI application factory and configuration."""

from fastapi import FastAPI
from src.core.config import get_settings
from src.core.middleware.cors import setup_cors_middleware
from src.core.middleware.logging import setup_logging_middleware
from src.infrastructure.database.connection import init_database
from src.presentation.api import health
from src.presentation.api.v1 import mocks, auth, import_api, images, state_api


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    # Initialize settings
    settings = get_settings()

    # Create FastAPI instance
    app = FastAPI(
        title="Mimicus",
        description="Universal HTTP Mock & Mimic Service",
        version="0.1.0",
    )

    # Setup middleware
    setup_cors_middleware(app)
    setup_logging_middleware(app)
    # Note: AuthMiddleware disabled by default for MVP testing
    # Enable for production with proper auth token management
    # jwt_svc = get_jwt_service()
    # app.add_middleware(AuthMiddleware, jwt_service=jwt_svc)

    # Initialize database
    async def startup():
        """Initialize database on startup."""
        db = init_database(settings.config_database_url)
        await db.init_db()

    async def shutdown():
        """Close database on shutdown."""
        from src.infrastructure.database.connection import get_database
        db = get_database()
        if db:
            await db.close()

    app.add_event_handler("startup", startup)
    app.add_event_handler("shutdown", shutdown)

    # Register routers (order matters - specific routes first, catch-all last)
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(images.router)
    app.include_router(import_api.router)
    app.include_router(state_api.router)

    # Register admin API BEFORE catch-all mock handler
    from src.presentation.api.v1 import admin
    app.include_router(admin.router)

    # Register catch-all mock handler last (matches any unhandled path)
    app.include_router(mocks.router)

    return app
