"""Integration tests for OpenAPI import endpoints."""

import json
import pytest
from io import BytesIO
from fastapi.testclient import TestClient
from src.core.app import create_app


app = create_app()
client = TestClient(app)


class TestOpenAPIImport:
    """Test OpenAPI specification import."""

    def test_import_openapi_json_file(self):
        """Test importing OpenAPI JSON file."""
        spec = {
            "openapi": "3.0.0",
            "info": {"title": "Test API", "version": "1.0.0"},
            "paths": {
                "/api/users": {
                    "get": {
                        "summary": "Get users",
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

        spec_bytes = json.dumps(spec).encode()
        response = client.post(
            "/api/import/openapi",
            files={"file": ("openapi.json", BytesIO(spec_bytes), "application/json")},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["mocks_created"] == 1
        assert len(data["mocks"]) == 1
        # DTOs use these names
        assert "/api/users" in str(data["mocks"][0])

    def test_import_multiple_endpoints(self):
        """Test importing spec with multiple endpoints."""
        spec = {
            "openapi": "3.0.0",
            "paths": {
                "/api/products": {
                    "get": {"responses": {"200": {"description": "List"}}},
                    "post": {"responses": {"201": {"description": "Created"}}},
                },
                "/api/products/{id}": {
                    "get": {"responses": {"200": {"description": "Get"}}},
                    "put": {"responses": {"200": {"description": "Update"}}},
                    "delete": {"responses": {"204": {"description": "Delete"}}},
                },
            }
        }

        spec_bytes = json.dumps(spec).encode()
        response = client.post(
            "/api/import/openapi",
            files={"file": ("api.json", BytesIO(spec_bytes), "application/json")},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["mocks_created"] == 5

    def test_import_with_yaml_extension(self):
        """Test that YAML extension is detected."""
        spec = {
            "openapi": "3.0.0",
            "paths": {
                "/api/test": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "OK",
                                "content": {
                                    "application/json": {"example": {"test": "data"}}
                                },
                            }
                        }
                    }
                }
            },
        }

        spec_bytes = json.dumps(spec).encode()
        response = client.post(
            "/api/import/openapi",
            files={"file": ("openapi.yaml", BytesIO(spec_bytes), "application/json")},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["mocks_created"] == 1

    def test_import_invalid_json(self):
        """Test importing invalid JSON file."""
        invalid_json = b"{ invalid json }"
        response = client.post(
            "/api/import/openapi",
            files={"file": ("invalid.json", BytesIO(invalid_json))},
        )

        assert response.status_code == 400

    def test_import_empty_spec(self):
        """Test importing spec with no paths."""
        spec = {"openapi": "3.0.0", "paths": {}}

        spec_bytes = json.dumps(spec).encode()
        response = client.post(
            "/api/import/openapi",
            files={"file": ("empty.json", BytesIO(spec_bytes), "application/json")},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["mocks_created"] == 0
        assert len(data["mocks"]) == 0

    def test_import_creates_usable_mocks(self):
        """Test that imported mocks are returned in the response."""
        spec = {
            "openapi": "3.0.0",
            "paths": {
                "/test/endpoint": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Success",
                                "content": {
                                    "application/json": {"example": {"status": "ok"}}
                                },
                            }
                        }
                    }
                }
            },
        }

        spec_bytes = json.dumps(spec).encode()
        import_response = client.post(
            "/api/import/openapi",
            files={"file": ("spec.json", BytesIO(spec_bytes), "application/json")},
        )

        assert import_response.status_code == 200
        data = import_response.json()
        # Verify mocks were created and returned in response
        assert data["mocks_created"] == 1
        assert len(data["mocks"]) == 1
        mock = data["mocks"][0]
        assert mock["match_path"] == "/test/endpoint"
        assert mock["match_method"] == "GET"

    def test_import_preserves_endpoint_structure(self):
        """Test that imported mocks preserve endpoint structure."""
        spec = {
            "openapi": "3.0.0",
            "paths": {
                "/api/v1/users/{id}": {
                    "get": {
                        "summary": "Get user by ID",
                        "responses": {
                            "200": {
                                "description": "User found",
                                "content": {
                                    "application/json": {
                                        "example": {"id": 123, "name": "Alice"}
                                    }
                                },
                            }
                        },
                    }
                }
            },
        }

        spec_bytes = json.dumps(spec).encode()
        response = client.post(
            "/api/import/openapi",
            files={"file": ("users.json", BytesIO(spec_bytes), "application/json")},
        )

        assert response.status_code == 200
        data = response.json()
        mock = data["mocks"][0]
        assert "/api/v1/users/{id}" in str(mock)
        assert "GET" in str(mock)

    def test_import_response_includes_spec_path(self):
        """Test that response includes spec file path."""
        spec = {
            "openapi": "3.0.0",
            "paths": {
                "/test": {"get": {"responses": {"200": {"description": "OK"}}}}
            },
        }

        spec_bytes = json.dumps(spec).encode()
        response = client.post(
            "/api/import/openapi",
            files={"file": ("my_api.json", BytesIO(spec_bytes), "application/json")},
        )

        assert response.status_code == 200
        data = response.json()
        assert "spec_path" in data
        assert "my_api.json" in data["spec_path"]
