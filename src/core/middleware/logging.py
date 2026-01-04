"""Request/response logging middleware."""

import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all requests and responses."""

    async def dispatch(self, request: Request, call_next: ASGIApp) -> Response:
        """Log request and response details."""
        start_time = time.time()

        # Log incoming request
        logger.info(
            f"Incoming: {request.method} {request.url.path}",
            extra={
                "request_method": request.method,
                "request_path": request.url.path,
                "request_query": str(request.url.query),
            },
        )

        # Call next middleware/endpoint
        response = await call_next(request)

        # Calculate response time
        response_time_ms = (time.time() - start_time) * 1000

        # Log response
        logger.info(
            f"Response: {response.status_code} ({response_time_ms:.2f}ms)",
            extra={
                "status_code": response.status_code,
                "response_time_ms": response_time_ms,
            },
        )

        # Add response headers
        response.headers["X-Response-Time-Ms"] = str(int(response_time_ms))

        return response


def setup_logging_middleware(app) -> None:
    """Configure logging middleware for FastAPI application."""
    app.add_middleware(LoggingMiddleware)

    # Configure basic logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
