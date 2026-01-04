"""Async HTTP client for proxying requests to upstream services."""

import httpx
from typing import Dict
from src.domain.entities.request_context import RequestContext


class ProxyResponse:
    """Response from proxied request."""

    def __init__(
        self,
        status_code: int,
        headers: Dict[str, str],
        content: bytes,
    ):
        """Initialize proxy response."""
        self.status_code = status_code
        self.headers = headers
        self.content = content


class HTTPClient:
    """Async HTTP client for proxying requests."""

    def __init__(self, timeout: int = 10):
        """Initialize HTTP client."""
        self.timeout = timeout
        self.client = None

    async def __aenter__(self):
        """Context manager entry."""
        self.client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.client:
            await self.client.aclose()

    async def proxy_request(
        self,
        upstream_url: str,
        request_context: RequestContext,
    ) -> ProxyResponse:
        """Forward request to upstream service."""
        if not self.client:
            self.client = httpx.AsyncClient(timeout=self.timeout)

        try:
            # Build full URL
            url = f"{upstream_url.rstrip('/')}{request_context.request_path}"

            # Filter headers to forward (skip content-length and similar)
            skip_headers = {
                "content-length",
                "transfer-encoding",
                "host",
                "connection",
            }
            headers = {
                k: v
                for k, v in request_context.request_headers.items()
                if k.lower() not in skip_headers
            }

            # Make request
            response = await self.client.request(
                method=request_context.request_method,
                url=url,
                headers=headers,
                params=request_context.request_query_params,
                content=request_context.request_body,
            )

            # Return proxy response
            return ProxyResponse(
                status_code=response.status_code,
                headers=dict(response.headers),
                content=response.content,
            )

        except httpx.TimeoutException as e:
            raise TimeoutError(f"Upstream request timeout: {str(e)}")
        except Exception as e:
            raise ConnectionError(f"Failed to reach upstream: {str(e)}")
