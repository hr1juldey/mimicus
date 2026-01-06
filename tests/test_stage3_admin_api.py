"""Tests for Stage 3 - Admin REST API."""

import pytest
import json
from fastapi.testclient import TestClient
from src.core.app import create_app
from src.core.dependencies import get_mock_repository


@pytest.fixture
def app():
    """Create test app."""
    return create_app()


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_mocks():
    """Clear all mocks before each test."""
    import asyncio

    repo = get_mock_repository()

    # Clear before test
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        all_mocks = loop.run_until_complete(repo.get_all())
        for mock in all_mocks:
            loop.run_until_complete(repo.delete(mock.mock_id))
    finally:
        loop.close()

    yield

    # Clear after test
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        all_mocks = loop.run_until_complete(repo.get_all())
        for mock in all_mocks:
            loop.run_until_complete(repo.delete(mock.mock_id))
    finally:
        loop.close()


@pytest.fixture
async def clean_repo():
    """Get clean repository."""
    repo = get_mock_repository()
    # Clear all mocks
    all_mocks = await repo.get_all()
    for mock in all_mocks:
        await repo.delete(mock.mock_id)
    return repo


class TestCreateMock:
    """Tests for creating mocks via API."""

    def test_create_mock_success(self, client):
        """Test creating a mock successfully."""
        payload = {
            "mock_name": "Test Mock",
            "mock_priority": 100,
            "match_method": "GET",
            "match_path": "/api/test",
            "response_status": 200,
            "response_body": '{"status": "ok"}',
            "is_template": False,
        }

        response = client.post("/api/admin/mocks", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["mock_name"] == "Test Mock"
        assert data["mock_id"]  # Should have auto-generated ID
        assert data["response_body"] == '{"status": "ok"}'

    def test_create_mock_with_template(self, client):
        """Test creating a mock with template response."""
        payload = {
            "mock_name": "Template Mock",
            "match_method": "POST",
            "match_path": "/api/login",
            "response_body": '{"user": "{{ request.json.username }}"}',
            "is_template": True,
        }

        response = client.post("/api/admin/mocks", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["is_template"] is True


class TestListMocks:
    """Tests for listing mocks."""

    def test_list_empty_mocks(self, client):
        """Test listing mocks when none exist."""
        response = client.get("/api/admin/mocks")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["mocks"] == []

    def test_list_multiple_mocks(self, client):
        """Test listing multiple mocks."""
        # Create multiple mocks
        for i in range(3):
            payload = {
                "mock_name": f"Mock {i}",
                "match_method": "GET",
                "match_path": f"/api/test{i}",
                "response_status": 200,
                "response_body": f'{{"id": {i}}}',
            }
            client.post("/api/admin/mocks", json=payload)

        # List them
        response = client.get("/api/admin/mocks")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 3
        assert len(data["mocks"]) == 3


class TestGetMock:
    """Tests for getting specific mock."""

    def test_get_existing_mock(self, client):
        """Test getting an existing mock."""
        # Create a mock
        payload = {
            "mock_name": "Get Test",
            "match_method": "GET",
            "match_path": "/api/get",
            "response_body": '{"test": "data"}',
        }
        create_response = client.post("/api/admin/mocks", json=payload)
        mock_id = create_response.json()["mock_id"]

        # Get it
        response = client.get(f"/api/admin/mocks/{mock_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["mock_id"] == mock_id
        assert data["mock_name"] == "Get Test"

    def test_get_nonexistent_mock(self, client):
        """Test getting a mock that doesn't exist."""
        response = client.get("/api/admin/mocks/nonexistent-id")
        assert response.status_code == 404


class TestUpdateMock:
    """Tests for updating mocks."""

    def test_update_mock_name(self, client):
        """Test updating mock name."""
        # Create mock
        payload = {
            "mock_name": "Original",
            "match_method": "GET",
            "match_path": "/api/update",
            "response_body": "{}",
        }
        create_response = client.post("/api/admin/mocks", json=payload)
        mock_id = create_response.json()["mock_id"]

        # Update it
        update_payload = {"mock_name": "Updated"}
        response = client.put(f"/api/admin/mocks/{mock_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["mock_name"] == "Updated"

    def test_update_response_body(self, client):
        """Test updating response body."""
        # Create mock
        payload = {
            "mock_name": "Body Test",
            "match_method": "GET",
            "match_path": "/api/body",
            "response_body": '{"old": "value"}',
        }
        create_response = client.post("/api/admin/mocks", json=payload)
        mock_id = create_response.json()["mock_id"]

        # Update response body
        update_payload = {"response_body": '{"new": "value"}'}
        response = client.put(f"/api/admin/mocks/{mock_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["response_body"] == '{"new": "value"}'

    def test_update_nonexistent_mock(self, client):
        """Test updating a mock that doesn't exist."""
        response = client.put(
            "/api/admin/mocks/nonexistent", json={"mock_name": "New Name"}
        )
        assert response.status_code == 404


class TestDeleteMock:
    """Tests for deleting mocks."""

    def test_delete_mock(self, client):
        """Test deleting a mock."""
        # Create mock
        payload = {
            "mock_name": "Delete Me",
            "match_method": "GET",
            "match_path": "/api/delete",
            "response_body": "{}",
        }
        create_response = client.post("/api/admin/mocks", json=payload)
        mock_id = create_response.json()["mock_id"]

        # Delete it
        response = client.delete(f"/api/admin/mocks/{mock_id}")
        assert response.status_code == 204

        # Verify it's gone
        response = client.get(f"/api/admin/mocks/{mock_id}")
        assert response.status_code == 404

    def test_delete_nonexistent_mock(self, client):
        """Test deleting a mock that doesn't exist."""
        response = client.delete("/api/admin/mocks/nonexistent")
        assert response.status_code == 404


class TestToggleMock:
    """Tests for toggling mock enabled status."""

    def test_toggle_mock_enabled(self, client):
        """Test toggling mock from enabled to disabled."""
        # Create mock (enabled by default)
        payload = {
            "mock_name": "Toggle Test",
            "match_method": "GET",
            "match_path": "/api/toggle",
            "response_body": "{}",
            "mock_enabled": True,
        }
        create_response = client.post("/api/admin/mocks", json=payload)
        mock_id = create_response.json()["mock_id"]

        # Toggle it
        response = client.post(f"/api/admin/mocks/{mock_id}/toggle")
        assert response.status_code == 200
        data = response.json()
        assert data["mock_enabled"] is False

        # Toggle again
        response = client.post(f"/api/admin/mocks/{mock_id}/toggle")
        assert response.status_code == 200
        data = response.json()
        assert data["mock_enabled"] is True

    def test_toggle_nonexistent_mock(self, client):
        """Test toggling a mock that doesn't exist."""
        response = client.post("/api/admin/mocks/nonexistent/toggle")
        assert response.status_code == 404


class TestBulkImport:
    """Tests for bulk importing mocks."""

    def test_bulk_import_from_json(self, client):
        """Test bulk importing mocks from JSON data."""
        json_payload = {
            "mocks": [
                {
                    "mock_name": "Mock 1",
                    "match_method": "GET",
                    "match_path": "/api/1",
                    "response_body": '{"id": 1}',
                },
                {
                    "mock_name": "Mock 2",
                    "match_method": "POST",
                    "match_path": "/api/2",
                    "response_body": '{"id": 2}',
                    "is_template": True,
                },
            ]
        }

        response = client.post(
            "/api/admin/mocks/bulk-import",
            params={"json_data": json.dumps(json_payload)},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["created"] == 2
        assert data["errors"] == 0
        assert len(data["mocks"]) == 2

    def test_bulk_import_partial_success(self, client):
        """Test bulk import with some invalid mocks."""
        json_payload = {
            "mocks": [
                {
                    "mock_name": "Valid Mock",
                    "match_method": "GET",
                    "match_path": "/api/valid",
                    "response_body": "{}",
                },
                {
                    "invalid_field": "This mock is missing required fields",
                },
            ]
        }

        response = client.post(
            "/api/admin/mocks/bulk-import",
            params={"json_data": json.dumps(json_payload)},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["created"] == 1
        assert data["errors"] == 1

    def test_bulk_import_invalid_json(self, client):
        """Test bulk import with invalid JSON."""
        response = client.post(
            "/api/admin/mocks/bulk-import",
            params={"json_data": "not valid json"},
        )
        assert response.status_code == 400


class TestEndToEndWorkflow:
    """End-to-end tests for complete workflows."""

    def test_create_enable_use_mock(self, client):
        """Test creating, enabling, and using a mock."""
        # Create mock
        payload = {
            "mock_name": "E2E Test",
            "match_method": "POST",
            "match_path": "/api/e2e",
            "response_status": 201,
            "response_body": '{"id": "123", "status": "created"}',
            "mock_enabled": True,
        }
        create_response = client.post("/api/admin/mocks", json=payload)
        assert create_response.status_code == 201

        # Use the mock (via mock handler)
        response = client.post("/api/e2e")
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == "123"

        # Get the mock via API
        mock_id = create_response.json()["mock_id"]
        response = client.get(f"/api/admin/mocks/{mock_id}")
        assert response.status_code == 200
        assert response.json()["mock_enabled"] is True

        # Disable it
        response = client.post(f"/api/admin/mocks/{mock_id}/toggle")
        assert response.status_code == 200

        # Mock should not match when disabled
        response = client.post("/api/e2e")
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
