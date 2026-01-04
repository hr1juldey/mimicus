"""Service for handling proxy requests with fallback logic."""

from fastapi import Response
from typing import Optional
from src.domain.entities.mock_definition import MockDefinition
from src.domain.entities.request_context import RequestContext
from src.infrastructure.external.http_client import HTTPClient


class ProxyService:
    """Service for proxy operations with fallback to mock responses."""

    def __init__(self, http_client: Optional[HTTPClient] = None):
        """Initialize proxy service with optional HTTP client."""
        self.http_client = http_client

    async def handle_proxy_request(
        self,
        mock_def: MockDefinition,
        request_context: RequestContext,
        response_service: Optional[object] = None,
    ) -> Response:
        """Handle proxy request based on mock mode."""
        if mock_def.mock_mode == "proxy":
            return await self._pure_proxy(mock_def, request_context)
        elif mock_def.mock_mode == "proxy-with-fallback":
            return await self._proxy_with_fallback(
                mock_def, request_context, response_service
            )
        elif mock_def.mock_mode == "passthrough":
            return await self._passthrough(mock_def, request_context)
        else:
            # Default to regular mock response
            if response_service:
                return await response_service.generate_response(
                    mock_def, request_context
                )
            raise ValueError(f"Unknown mock mode: {mock_def.mock_mode}")

    async def _pure_proxy(
        self, mock_def: MockDefinition, request_context: RequestContext
    ) -> Response:
        """Pure proxy - always forward to upstream."""
        if not mock_def.upstream_url:
            return Response(
                content='{"error": "Upstream URL not configured"}',
                status_code=500,
                media_type="application/json",
            )

        if not self.http_client:
            self.http_client = HTTPClient(timeout=mock_def.timeout_seconds)

        try:
            proxy_response = await self.http_client.proxy_request(
                mock_def.upstream_url, request_context
            )

            return Response(
                content=proxy_response.content,
                status_code=proxy_response.status_code,
                headers=proxy_response.headers,
            )
        except Exception as e:
            return Response(
                content=f'{{"error": "Proxy request failed: {str(e)}"}}',
                status_code=500,
                media_type="application/json",
            )

    async def _proxy_with_fallback(
        self,
        mock_def: MockDefinition,
        request_context: RequestContext,
        response_service: Optional[object],
    ) -> Response:
        """Proxy with fallback - try upstream, fallback to mock on failure."""
        if not mock_def.upstream_url:
            # No upstream, use mock response
            if response_service:
                return await response_service.generate_response(
                    mock_def, request_context
                )
            raise ValueError("No upstream URL and no mock response configured")

        if not self.http_client:
            self.http_client = HTTPClient(timeout=mock_def.timeout_seconds)

        try:
            proxy_response = await self.http_client.proxy_request(
                mock_def.upstream_url, request_context
            )

            return Response(
                content=proxy_response.content,
                status_code=proxy_response.status_code,
                headers=proxy_response.headers,
            )
        except (TimeoutError, ConnectionError):
            # Upstream failed, fallback to mock response
            if response_service:
                return await response_service.generate_response(
                    mock_def, request_context
                )
            raise

    async def _passthrough(
        self, mock_def: MockDefinition, request_context: RequestContext
    ) -> Response:
        """Passthrough - always forward, no mock fallback."""
        if not mock_def.upstream_url:
            raise ValueError("Upstream URL not configured for passthrough mode")

        if not self.http_client:
            self.http_client = HTTPClient(timeout=mock_def.timeout_seconds)

        proxy_response = await self.http_client.proxy_request(
            mock_def.upstream_url, request_context
        )

        return Response(
            content=proxy_response.content,
            status_code=proxy_response.status_code,
            headers=proxy_response.headers,
        )
