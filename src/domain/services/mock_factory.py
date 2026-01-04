"""Factory pattern for creating mock objects."""

import uuid
from typing import Dict, Any, Optional
from src.domain.entities.mock_definition import (
    MockDefinition,
    MatchCriteria,
    ResponseConfig,
)


class MockFactory:
    """Factory for creating MockDefinition instances."""

    @staticmethod
    def create_basic(
        name: str = "Test Mock",
        method: str = "GET",
        path: str = "/api/test",
        status: int = 200,
        body: str = '{}',
        **kwargs
    ) -> MockDefinition:
        """Create a basic mock with sensible defaults."""
        return MockDefinition(
            mock_id=kwargs.get("mock_id", str(uuid.uuid4())),
            mock_name=name,
            mock_priority=kwargs.get("mock_priority", 100),
            mock_enabled=kwargs.get("mock_enabled", True),
            mock_mode=kwargs.get("mock_mode", "mock"),
            mock_match=MatchCriteria(
                match_method=method,
                match_path=path,
                match_headers=kwargs.get("match_headers"),
                match_query=kwargs.get("match_query"),
            ),
            mock_response=ResponseConfig(
                response_status=status,
                response_headers=kwargs.get("response_headers", {}),
                response_body=body,
                response_delay_ms=kwargs.get("response_delay_ms", 0),
                is_template=kwargs.get("is_template", False),
            ),
            upstream_url=kwargs.get("upstream_url"),
            timeout_seconds=kwargs.get("timeout_seconds", 10),
        )

    @staticmethod
    def create_template(
        name: str = "Template Mock",
        method: str = "POST",
        path: str = "/api/template",
        template_body: str = '{"data": "{{ request.json.data }}"}',
        **kwargs
    ) -> MockDefinition:
        """Create a mock with template response."""
        return MockFactory.create_basic(
            name=name,
            method=method,
            path=path,
            body=template_body,
            is_template=True,
            **kwargs
        )

    @staticmethod
    def create_proxy(
        name: str = "Proxy Mock",
        path: str = "/api/proxy",
        upstream_url: str = "https://example.com",
        **kwargs
    ) -> MockDefinition:
        """Create a mock configured for proxy mode."""
        mock_mode = kwargs.pop("mock_mode", "proxy")
        body = kwargs.pop("body", "")
        match_path = kwargs.pop("match_path", path)
        return MockFactory.create_basic(
            name=name,
            path=match_path,
            body=body,
            mock_mode=mock_mode,
            upstream_url=upstream_url,
            **kwargs
        )

    @staticmethod
    def create_error(
        name: str = "Error Response",
        method: str = "GET",
        path: str = "/api/error",
        status: int = 500,
        **kwargs
    ) -> MockDefinition:
        """Create a mock that returns an error response."""
        return MockFactory.create_basic(
            name=name,
            method=method,
            path=path,
            status=status,
            body=f'{{"error": "Internal Server Error", "code": {status}}}',
            **kwargs
        )

    @staticmethod
    def create_from_dict(data: Dict[str, Any]) -> MockDefinition:
        """Create a mock from a dictionary (e.g., from JSON)."""
        match_criteria = MatchCriteria(
            match_method=data.get("match_method", "GET"),
            match_path=data.get("match_path", "/"),
            match_headers=data.get("match_headers"),
            match_query=data.get("match_query"),
        )

        response_config = ResponseConfig(
            response_status=data.get("response_status", 200),
            response_headers=data.get("response_headers", {}),
            response_body=data.get("response_body", ""),
            response_delay_ms=data.get("response_delay_ms", 0),
            is_template=data.get("is_template", False),
        )

        return MockDefinition(
            mock_id=data.get("mock_id", str(uuid.uuid4())),
            mock_name=data.get("mock_name", "Imported Mock"),
            mock_priority=data.get("mock_priority", 100),
            mock_enabled=data.get("mock_enabled", True),
            mock_mode=data.get("mock_mode", "mock"),
            mock_match=match_criteria,
            mock_response=response_config,
            upstream_url=data.get("upstream_url"),
            timeout_seconds=data.get("timeout_seconds", 10),
        )
