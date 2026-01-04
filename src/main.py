"""Mimicus application entry point."""

import uvicorn
from src.core.app import create_app
from src.core.config import get_settings


# Create FastAPI application
app = create_app()


def main():
    """Run the Mimicus mock server."""
    settings = get_settings()

    uvicorn.run(
        "src.main:app",
        host=settings.mock_server_host,
        port=settings.mock_server_port,
        reload=settings.mock_server_reload,
        log_level=settings.mock_log_level.lower(),
    )


if __name__ == "__main__":
    main()
