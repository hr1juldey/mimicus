"""OpenAPI specification importer for auto-generating mocks."""

import json
import yaml
from typing import List, Dict, Any

from src.domain.entities.mock_definition import MockDefinition
from src.domain.services.mock_factory import MockFactory
from src.infrastructure.external.openapi_schema_helper import SchemaToExampleConverter


class OpenAPIImporter:
    """Import OpenAPI specifications and generate mock definitions."""

    def __init__(self, factory: MockFactory):
        """Initialize OpenAPI importer.

        Args:
            factory: Factory for creating mock entities
        """
        self.factory = factory

    async def import_spec(
        self, spec_content: str, is_yaml: bool = False
    ) -> List[MockDefinition]:
        """Parse OpenAPI spec and generate mocks.

        Args:
            spec_content: OpenAPI specification content
            is_yaml: True if YAML format, False if JSON

        Returns:
            List of generated MockDefinition entities

        Raises:
            ValueError: If spec is invalid
        """
        try:
            if is_yaml:
                spec = yaml.safe_load(spec_content)
            else:
                spec = json.loads(spec_content)
        except Exception as e:
            raise ValueError(f"Invalid OpenAPI spec: {str(e)}")

        if not spec or not isinstance(spec, dict):
            raise ValueError("Invalid OpenAPI specification")

        mocks = []
        paths = spec.get("paths", {})

        for path, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue

            for method, operation in path_item.items():
                if method not in ["get", "post", "put", "delete", "patch"]:
                    continue

                if not isinstance(operation, dict):
                    continue

                mock = self._create_mock_from_operation(
                    path, method.upper(), operation
                )
                if mock:
                    mocks.append(mock)

        return mocks

    def _create_mock_from_operation(
        self, path: str, method: str, operation: Dict[str, Any]
    ) -> MockDefinition | None:
        """Create mock from OpenAPI operation."""
        try:
            summary = operation.get("summary", f"{method} {path}")
            response_body = self._extract_example_response(operation)

            return self.factory.create_basic(
                name=summary,
                method=method,
                path=path,
                body=response_body,
                status=200,
                mock_mode="mock",
            )
        except Exception:
            return None

    def _extract_example_response(self, operation: Dict[str, Any]) -> str:
        """Extract example response from operation."""
        responses = operation.get("responses", {})

        for status, response in responses.items():
            if not isinstance(response, dict):
                continue

            content = response.get("content", {})
            if "application/json" not in content:
                continue

            json_content = content["application/json"]
            example = json_content.get("example")

            if example:
                if isinstance(example, str):
                    return example
                return json.dumps(example)

            schema = json_content.get("schema", {})
            if isinstance(schema, dict):
                example_data = SchemaToExampleConverter.convert(schema)
                return json.dumps(example_data)

        return "{}"
