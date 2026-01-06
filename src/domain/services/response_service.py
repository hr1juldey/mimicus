"""Service for generating HTTP responses from mock definitions."""

import json
import asyncio
import random
from typing import Any, Dict, Union, Optional
from fastapi import Response
from src.domain.entities.mock_definition import MockDefinition
from src.domain.entities.request_context import RequestContext


class ResponseService:
    """Service to generate responses from mock definitions."""

    def __init__(
        self,
        template_service: Optional[Any] = None,
        rate_limiter: Optional[Any] = None,
    ):
        """Initialize response service with optional template and rate limiter."""
        self.template_service = template_service
        self.rate_limiter = rate_limiter

    @staticmethod
    def _prepare_body(body: Union[str, Dict, Any], is_template: bool = False) -> str:
        """Prepare response body as string."""
        if isinstance(body, dict):
            return json.dumps(body)
        if isinstance(body, str):
            return body
        return json.dumps(body)

    @staticmethod
    def _prepare_headers(headers: Dict[str, str]) -> Dict[str, str]:
        """Prepare response headers."""
        # Ensure Content-Type is set if not provided
        if not any(k.lower() == "content-type" for k in headers.keys()):
            headers = {**headers, "Content-Type": "application/json"}
        return headers

    async def generate_response(
        self,
        mock_def: MockDefinition,
        request_context: RequestContext,
    ) -> Response:
        """Generate HTTP response from mock definition."""
        response_config = mock_def.mock_response
        client_ip = request_context.client_ip

        # Check rate limit first
        if self.rate_limiter:
            allowed = self.rate_limiter.is_allowed(mock_def.mock_id, client_ip)
            if not allowed:
                return Response(
                    content="Too Many Requests",
                    status_code=429,
                    headers={"Content-Type": "text/plain"},
                )

        # Check error rate (random injection)
        if response_config.error_rate > 0:
            if random.randint(0, 100) < response_config.error_rate:
                return Response(
                    content=response_config.error_body,
                    status_code=response_config.error_status_code,
                    headers=self._prepare_headers(
                        response_config.response_headers.copy()
                    ),
                    media_type="application/json",
                )

        # Apply delay if configured
        if response_config.response_delay_ms > 0:
            await asyncio.sleep(response_config.response_delay_ms / 1000.0)

        # Prepare body (with template rendering if needed)
        body_str = self._prepare_body(response_config.response_body)

        # Check if body is a template and render it
        if self.template_service and response_config.is_template:
            body_str = await self.template_service.render_template(
                body_str, request_context
            )

        # Prepare headers
        headers = self._prepare_headers(response_config.response_headers.copy())

        # Create and return FastAPI Response
        return Response(
            content=body_str,
            status_code=response_config.response_status,
            headers=headers,
            media_type=headers.get("Content-Type", "application/json"),
        )
