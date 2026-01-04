"""Service for generating HTTP responses from mock definitions."""

import json
import asyncio
from typing import Any, Dict, Union
from fastapi import Response
from src.domain.entities.mock_definition import MockDefinition
from src.domain.entities.request_context import RequestContext


class ResponseService:
    """Service to generate responses from mock definitions."""

    @staticmethod
    def _prepare_body(
        body: Union[str, Dict, Any], is_template: bool = False
    ) -> str:
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
        # Get response config
        response_config = mock_def.mock_response

        # Apply delay if configured
        if response_config.response_delay_ms > 0:
            await asyncio.sleep(response_config.response_delay_ms / 1000.0)

        # Prepare body
        body = self._prepare_body(response_config.response_body)

        # Prepare headers
        headers = self._prepare_headers(response_config.response_headers.copy())

        # Create and return FastAPI Response
        return Response(
            content=body,
            status_code=response_config.response_status,
            headers=headers,
            media_type=headers.get("Content-Type", "application/json"),
        )
