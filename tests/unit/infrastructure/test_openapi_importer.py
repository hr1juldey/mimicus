"""Unit tests for OpenAPI importer."""

import json
import pytest
from src.infrastructure.external.openapi_importer import OpenAPIImporter
from src.domain.services.mock_factory import MockFactory


@pytest.fixture
def importer():
    """Fixture providing OpenAPI importer."""
    factory = MockFactory()
    return OpenAPIImporter(factory)


class TestOpenAPIImporter:
    """Test OpenAPI specification parsing and mock generation."""

    @pytest.mark.asyncio
    async def test_import_simple_openapi_json(self, importer):
        """Test importing simple OpenAPI JSON spec."""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": "Test API", "version": "1.0.0"},
            "paths": {
                "/users": {
                    "get": {
                        "summary": "List users",
                        "responses": {
                            "200": {
                                "description": "Success",
                                "content": {
                                    "application/json": {
                                        "example": [{"id": 1, "name": "John"}]
                                    }
                                },
                            }
                        },
                    }
                }
            },
        }

        spec_str = json.dumps(spec)
        mocks = await importer.import_spec(spec_str, is_yaml=False)

        assert len(mocks) == 1
        assert mocks[0].mock_match.match_method == "GET"
        assert mocks[0].mock_match.match_path == "/users"

    @pytest.mark.asyncio
    async def test_import_multiple_endpoints(self, importer):
        """Test importing spec with multiple endpoints."""
        spec = {
            "openapi": "3.0.0",
            "paths": {
                "/users": {
                    "get": {"responses": {"200": {"description": "OK"}}},
                    "post": {"responses": {"201": {"description": "Created"}}},
                },
                "/users/{id}": {
                    "get": {"responses": {"200": {"description": "OK"}}},
                    "put": {"responses": {"200": {"description": "Updated"}}},
                    "delete": {"responses": {"204": {"description": "Deleted"}}},
                },
            }
        }

        spec_str = json.dumps(spec)
        mocks = await importer.import_spec(spec_str)

        assert len(mocks) == 5
        methods = [m.mock_match.match_method for m in mocks]
        assert "GET" in methods
        assert "POST" in methods
        assert "PUT" in methods
        assert "DELETE" in methods

    @pytest.mark.asyncio
    async def test_import_with_schema(self, importer):
        """Test importing spec with JSON schema."""
        spec = {
            "openapi": "3.0.0",
            "paths": {
                "/products": {
                    "get": {
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "integer"},
                                                "name": {"type": "string"},
                                                "price": {"type": "number"},
                                            },
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
        }

        spec_str = json.dumps(spec)
        mocks = await importer.import_spec(spec_str)

        assert len(mocks) == 1
        mock = mocks[0]
        response = json.loads(mock.mock_response.response_body)
        assert "id" in response
        assert "name" in response
        assert "price" in response

    @pytest.mark.asyncio
    async def test_import_with_example(self, importer):
        """Test that example response is used when provided."""
        spec = {
            "openapi": "3.0.0",
            "paths": {
                "/users/1": {
                    "get": {
                        "responses": {
                            "200": {
                                "content": {
                                    "application/json": {
                                        "example": {
                                            "id": 1,
                                            "name": "Alice",
                                            "email": "alice@example.com",
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
        }

        spec_str = json.dumps(spec)
        mocks = await importer.import_spec(spec_str)

        assert len(mocks) == 1
        response = json.loads(mocks[0].mock_response.response_body)
        assert response["name"] == "Alice"

    @pytest.mark.asyncio
    async def test_import_empty_spec(self, importer):
        """Test importing empty spec returns empty list."""
        spec = {"openapi": "3.0.0", "paths": {}}
        spec_str = json.dumps(spec)
        mocks = await importer.import_spec(spec_str)

        assert len(mocks) == 0

    @pytest.mark.asyncio
    async def test_import_invalid_json(self, importer):
        """Test importing invalid JSON raises error."""
        with pytest.raises(ValueError):
            await importer.import_spec("invalid json {", is_yaml=False)

    @pytest.mark.asyncio
    async def test_import_missing_paths(self, importer):
        """Test spec without paths field."""
        spec = {"openapi": "3.0.0", "info": {"title": "API"}}
        spec_str = json.dumps(spec)
        mocks = await importer.import_spec(spec_str)

        assert len(mocks) == 0

    @pytest.mark.asyncio
    async def test_import_path_with_parameters(self, importer):
        """Test importing path with parameters."""
        spec = {
            "openapi": "3.0.0",
            "paths": {
                "/users/{userId}/posts/{postId}": {
                    "get": {"responses": {"200": {"description": "OK"}}}
                }
            },
        }

        spec_str = json.dumps(spec)
        mocks = await importer.import_spec(spec_str)

        assert len(mocks) == 1
        assert "{userId}" in mocks[0].mock_match.match_path
        assert "{postId}" in mocks[0].mock_match.match_path

    @pytest.mark.asyncio
    async def test_import_ignores_invalid_methods(self, importer):
        """Test that invalid HTTP methods are ignored."""
        spec = {
            "openapi": "3.0.0",
            "paths": {
                "/users": {
                    "get": {"responses": {"200": {"description": "OK"}}},
                    "invalid": {"responses": {"200": {"description": "OK"}}},
                    "trace": {"responses": {"200": {"description": "OK"}}},
                }
            },
        }

        spec_str = json.dumps(spec)
        mocks = await importer.import_spec(spec_str)

        assert len(mocks) == 1
        assert mocks[0].mock_match.match_method == "GET"
