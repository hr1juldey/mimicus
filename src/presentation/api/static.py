"""Static assets endpoints for Mimicus application."""

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["static"])


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Serve the default favicon."""
    favicon_path = Path("assets/favicon/favicon.ico")
    return FileResponse(favicon_path)


@router.get("/favicon-light.ico", include_in_schema=False)
async def favicon_light():
    """Serve the light mode favicon."""
    favicon_path = Path(
        "assets/favicon/favicon-96x96.png"
    )  # Using existing file as light favicon
    return FileResponse(favicon_path)


@router.get("/favicon-dark.ico", include_in_schema=False)
async def favicon_dark():
    """Serve the dark mode favicon."""
    favicon_path = Path(
        "assets/favicon/favicon.svg"
    )  # Using existing file as dark favicon
    return FileResponse(favicon_path)


# Reserved paths that should not be handled by the catch-all mock route
# These are defined here to ensure they take precedence over the catch-all route in mocks.py
@router.get("/docs", include_in_schema=False)
async def swagger_docs():
    """Placeholder for Swagger docs - this will be overridden in app.py"""
    # This is just a placeholder to ensure the path is registered before the catch-all
    # The actual implementation will be in app.py with custom favicon
    pass


@router.get("/redoc", include_in_schema=False)
async def redoc_docs():
    """Placeholder for ReDoc docs - this will be overridden in app.py"""
    # This is just a placeholder to ensure the path is registered before the catch-all
    # The actual implementation will be in app.py with custom favicon
    pass
