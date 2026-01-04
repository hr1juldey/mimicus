"""Integration tests for Stage 1 - Core mock engine."""

import pytest
from fastapi.testclient import TestClient
from src.core.app import create_app
from src.core.dependencies import get_mock_repository
from src.domain.entities.mock_definition import (
    MockDefinition,
    MatchCriteria,
    ResponseConfig,
)


@pytest.fixture
def app():
    """Create test FastAPI application."""
    return create_app()


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_repo():
    """Get mock repository from app."""
    return get_mock_repository()


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self, client):
        """Test /health endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "mimicus"

    def test_readiness_check(self, client):
        """Test /ready endpoint returns ready status."""
        response = client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["ready"] is True


class TestMockMatching:
    """Tests for mock matching functionality."""

    @pytest.mark.asyncio
    async def test_exact_path_matching(self, client, mock_repo):
        """Test exact path matching."""
        # Create a mock
        mock = MockDefinition(
            mock_id="test-1",
            mock_name="Test Mock",
            mock_match=MatchCriteria(match_method="GET", match_path="/api/test"),
            mock_response=ResponseConfig(
                response_status=200, response_body='{"message": "success"}'
            ),
        )
        await mock_repo.create(mock)

        # Test request to matching path
        response = client.get("/api/test")
        assert response.status_code == 200
        assert response.json() == {"message": "success"}

    @pytest.mark.asyncio
    async def test_template_path_matching(self, client, mock_repo):
        """Test path template matching with parameters."""
        # Create a mock with path template
        mock = MockDefinition(
            mock_id="test-2",
            mock_name="User Mock",
            mock_match=MatchCriteria(match_method="GET", match_path="/api/users/{id}"),
            mock_response=ResponseConfig(
                response_status=200,
                response_body='{"user_id": "123"}',
            ),
        )
        await mock_repo.create(mock)

        # Test request to template path
        response = client.get("/api/users/123")
        assert response.status_code == 200
        assert response.json() == {"user_id": "123"}

        # Test another user ID
        response = client.get("/api/users/456")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_no_matching_mock(self, client, mock_repo):
        """Test request with no matching mock returns 404."""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
        data = response.json()
        assert "error" in data


class TestResponseGeneration:
    """Tests for response generation."""

    @pytest.mark.asyncio
    async def test_static_json_response(self, client, mock_repo):
        """Test static JSON response."""
        mock = MockDefinition(
            mock_id="test-3",
            mock_name="JSON Response",
            mock_match=MatchCriteria(match_method="GET", match_path="/api/data"),
            mock_response=ResponseConfig(
                response_status=200,
                response_headers={"Content-Type": "application/json"},
                response_body='{"key": "value"}',
            ),
        )
        await mock_repo.create(mock)

        response = client.get("/api/data")
        assert response.status_code == 200
        assert response.json() == {"key": "value"}

    @pytest.mark.asyncio
    async def test_custom_status_code(self, client, mock_repo):
        """Test custom status code in response."""
        mock = MockDefinition(
            mock_id="test-4",
            mock_name="Not Found",
            mock_match=MatchCriteria(match_method="GET", match_path="/api/missing"),
            mock_response=ResponseConfig(
                response_status=404,
                response_body='{"error": "not found"}',
            ),
        )
        await mock_repo.create(mock)

        response = client.get("/api/missing")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_custom_headers(self, client, mock_repo):
        """Test custom response headers."""
        mock = MockDefinition(
            mock_id="test-5",
            mock_name="Custom Headers",
            mock_match=MatchCriteria(match_method="GET", match_path="/api/headers"),
            mock_response=ResponseConfig(
                response_status=200,
                response_headers={
                    "X-Custom-Header": "custom-value",
                    "X-Another-Header": "another-value",
                },
                response_body='{}',
            ),
        )
        await mock_repo.create(mock)

        response = client.get("/api/headers")
        assert response.headers.get("X-Custom-Header") == "custom-value"
        assert response.headers.get("X-Another-Header") == "another-value"


class TestMockPriority:
    """Tests for mock priority-based selection."""

    @pytest.mark.asyncio
    async def test_higher_priority_match_wins(self, client, mock_repo):
        """Test that higher priority mock is selected."""
        # Create two mocks with same path
        mock1 = MockDefinition(
            mock_id="test-6a",
            mock_name="Low Priority",
            mock_priority=10,
            mock_match=MatchCriteria(match_method="GET", match_path="/api/priority"),
            mock_response=ResponseConfig(
                response_status=200, response_body='{"mock": "low"}'
            ),
        )
        mock2 = MockDefinition(
            mock_id="test-6b",
            mock_name="High Priority",
            mock_priority=100,
            mock_match=MatchCriteria(match_method="GET", match_path="/api/priority"),
            mock_response=ResponseConfig(
                response_status=200, response_body='{"mock": "high"}'
            ),
        )

        await mock_repo.create(mock1)
        await mock_repo.create(mock2)

        response = client.get("/api/priority")
        assert response.status_code == 200
        # Should match high priority mock
        assert response.json() == {"mock": "high"}


class TestMethodMatching:
    """Tests for HTTP method matching."""

    @pytest.mark.asyncio
    async def test_post_method_matching(self, client, mock_repo):
        """Test POST method matching."""
        mock = MockDefinition(
            mock_id="test-7",
            mock_name="POST Handler",
            mock_match=MatchCriteria(match_method="POST", match_path="/api/create"),
            mock_response=ResponseConfig(
                response_status=201, response_body='{"created": true}'
            ),
        )
        await mock_repo.create(mock)

        # POST should match
        response = client.post("/api/create")
        assert response.status_code == 201

        # GET should not match
        response = client.get("/api/create")
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
