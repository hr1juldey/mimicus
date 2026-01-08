"""FastAPI application factory and configuration."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from src.core.config import get_settings
from src.core.middleware.cors import setup_cors_middleware
from src.core.middleware.logging import setup_logging_middleware
from src.infrastructure.database.connection import init_database
from src.presentation.api import health
from src.presentation.api.static import router as static_router
from src.presentation.api.v1 import mocks, auth, import_api, images, state_api


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    # Initialize settings
    settings = get_settings()

    # Create FastAPI instance with disabled default docs to allow custom implementation
    app = FastAPI(
        title="Mimicus",
        description="Universal HTTP Mock & Mimic Service",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
    )

    # Add documentation routes FIRST, before any other routes are registered
    from fastapi.responses import HTMLResponse

    async def custom_swagger_ui_html():
        # Create a custom HTML response with our favicon
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <link rel="shortcut icon" href="/favicon.ico">
        <title>{app.title} - Swagger UI</title>
        </head>
        <body>
        <div id="swagger-ui">
        </div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <!-- `SwaggerUIBundle` is now available on the page -->
        <script>
        const ui = SwaggerUIBundle({{
            url: '{app.openapi_url}',
            dom_id: '#swagger-ui',
            layout: 'BaseLayout',
            deepLinking: true,
            showExtensions: true,
            showCommonExtensions: true,
            oauth2RedirectUrl: window.location.origin + '/docs/oauth2-redirect',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.SwaggerUIStandalonePreset
            ],
        }})
        </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html)

    async def custom_redoc_html():
        # Create a custom HTML response with our favicon for Redoc
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>{app.title} - ReDoc</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="shortcut icon" href="/favicon.ico">
        <link href="https://cdn.jsdelivr.net/npm/redoc@latest/dist/redoc.min.css" rel="stylesheet">
        </head>
        <body>
        <noscript>
            <h1>Documentation</h1>
        </noscript>
        <div id="redoc-container"></div>
        <script src="https://cdn.jsdelivr.net/npm/redoc@latest/dist/redoc.min.js"></script>
        <script>
            var redoc = Redoc.create('{app.openapi_url}', {{
                scrollYOffset: 50,
                hideHostname: false,
            }}, document.getElementById('redoc-container'));
        </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html)

    # Add the documentation routes to the app with proper path matching
    app.get("/docs", include_in_schema=False)(custom_swagger_ui_html)
    app.get("/redoc", include_in_schema=False)(custom_redoc_html)

    # Setup middleware
    setup_cors_middleware(app)
    setup_logging_middleware(app)

    # Add middleware to handle reserved paths before they reach the catch-all mock handler
    @app.middleware("http")
    async def reserved_paths_middleware(request, call_next):
        # Check if the path is a reserved system path
        reserved_paths = ["/docs", "/redoc", "/openapi.json"]
        if request.url.path in reserved_paths:
            # Skip the normal request processing and continue to the next handler
            # This allows the documentation routes to handle these paths
            response = await call_next(request)
            return response
        else:
            # Process normally for non-reserved paths
            response = await call_next(request)
            return response

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

    # Mount static files directory
    app.mount(
        "/static",
        StaticFiles(directory=Path(__file__).parent.parent.parent / "assets"),
        name="static",
    )

    # Register static assets router before catch-all mock handler
    app.include_router(static_router)

    # Register routers (order matters - specific routes first, catch-all last)
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(images.router)
    app.include_router(import_api.router)
    app.include_router(state_api.router)

    # Register admin API BEFORE catch-all mock handler
    from src.presentation.api.v1 import admin, inspector_api

    app.include_router(admin.router)
    app.include_router(inspector_api.router)

    # Register catch-all mock handler last (matches any unhandled path)
    app.include_router(mocks.router)

    return app
