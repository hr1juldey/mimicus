"""Tests for Stage 4 - Proxy mode functionality."""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from src.core.app import create_app
from src.core.dependencies import get_mock_repository
from src.domain.services.mock_factory import MockFactory
from src.infrastructure.external.http_client import ProxyResponse


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


class TestProxyMode:
    """Tests for pure proxy mode."""

    def test_proxy_mode_requires_upstream(self, client):
        """Test that proxy mode requires upstream_url."""
        import asyncio

        repo = get_mock_repository()

        # Create proxy mock without upstream URL
        mock = MockFactory.create_proxy(
            upstream_url=None,
            mock_mode="proxy",
        )
        asyncio.run(repo.create(mock))

        # Should fail because no upstream configured
        response = client.get("/api/proxy")
        assert response.status_code == 500  # Server error due to missing upstream

    def test_proxy_mode_forwards_request(self, client):
        """Test that proxy mode forwards request to upstream."""
        import asyncio

        repo = get_mock_repository()

        # Create proxy mock
        mock = MockFactory.create_proxy(
            upstream_url="https://jsonplaceholder.typicode.com",
            match_path="/api/posts/1",
            mock_mode="proxy",
        )
        asyncio.run(repo.create(mock))

        # Mock the HTTP client to simulate upstream response
        with patch("src.presentation.api.v1.mocks.HTTPClient") as MockHTTPClient:
            proxy_response = ProxyResponse(
                status_code=200,
                headers={"Content-Type": "application/json"},
                content=b'{"id": 1, "title": "test post"}',
            )
            mock_http_instance = AsyncMock()
            mock_http_instance.proxy_request = AsyncMock(return_value=proxy_response)
            MockHTTPClient.return_value = mock_http_instance

            # Make request
            response = client.get("/api/posts/1")
            assert response.status_code == 200


class TestProxyWithFallback:
    """Tests for proxy-with-fallback mode."""

    def test_fallback_on_upstream_failure(self, client):
        """Test that fallback mode uses mock when upstream fails."""
        import asyncio

        repo = get_mock_repository()

        # Create proxy-with-fallback mock
        mock = MockFactory.create_proxy(
            upstream_url="https://nonexistent.invalid.example.com",
            mock_mode="proxy-with-fallback",
            body='{"fallback": true, "status": "offline"}',
        )
        asyncio.run(repo.create(mock))

        # Mock the HTTP client to simulate upstream failure
        with patch("src.presentation.api.v1.mocks.HTTPClient") as MockHTTPClient:
            mock_http_instance = AsyncMock()
            # Simulate upstream timeout
            mock_http_instance.proxy_request = AsyncMock(
                side_effect=TimeoutError("Upstream timeout")
            )
            MockHTTPClient.return_value = mock_http_instance

            # Should return fallback mock response
            response = client.get("/api/proxy")
            assert response.status_code == 200
            data = response.json()
            assert data["fallback"] is True

    def test_fallback_uses_upstream_on_success(self, client):
        """Test that fallback uses upstream when it's available."""
        import asyncio

        repo = get_mock_repository()

        # Create proxy-with-fallback mock
        mock = MockFactory.create_proxy(
            upstream_url="https://example.com",
            mock_mode="proxy-with-fallback",
            body='{"fallback": true}',
        )
        asyncio.run(repo.create(mock))

        # Mock the HTTP client to simulate successful upstream response
        with patch("src.presentation.api.v1.mocks.HTTPClient") as MockHTTPClient:
            proxy_response = ProxyResponse(
                status_code=200,
                headers={"Content-Type": "application/json"},
                content=b'{"from": "upstream"}',
            )
            mock_http_instance = AsyncMock()
            mock_http_instance.proxy_request = AsyncMock(return_value=proxy_response)
            MockHTTPClient.return_value = mock_http_instance

            # Should return upstream response
            response = client.get("/api/proxy")
            assert response.status_code == 200
            data = response.json()
            assert data["from"] == "upstream"


class TestPassthroughMode:
    """Tests for passthrough mode."""

    def test_passthrough_always_forwards(self, client):
        """Test that passthrough always forwards to upstream."""
        import asyncio

        repo = get_mock_repository()

        # Create passthrough mock
        mock = MockFactory.create_proxy(
            upstream_url="https://example.com",
            match_path="/api/pass",
            mock_mode="passthrough",
        )
        asyncio.run(repo.create(mock))

        # Mock the HTTP client
        with patch("src.presentation.api.v1.mocks.HTTPClient") as MockHTTPClient:
            proxy_response = ProxyResponse(
                status_code=200,
                headers={"Content-Type": "text/html"},
                content=b"<html>content</html>",
            )
            mock_http_instance = AsyncMock()
            mock_http_instance.proxy_request = AsyncMock(return_value=proxy_response)
            MockHTTPClient.return_value = mock_http_instance

            # Make request
            response = client.get("/api/pass")
            assert response.status_code == 200
            assert b"<html>content</html>" in response.content


class TestMockModeFallback:
    """Tests to ensure mock mode still works."""

    def test_mock_mode_returns_static_response(self, client):
        """Test that standard mock mode still works."""
        import asyncio

        repo = get_mock_repository()

        # Create regular mock
        mock = MockFactory.create_basic(
            name="Static Mock",
            path="/api/static",
            body='{"type": "mock", "data": "static"}',
            mock_mode="mock",
        )
        asyncio.run(repo.create(mock))

        # Should return mock response without trying to proxy
        response = client.get("/api/static")
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "mock"


class TestProxyConfiguration:
    """Tests for proxy configuration in mocks."""

    def test_create_proxy_mock_via_admin_api(self, client):
        """Test creating proxy mock via admin API."""
        payload = {
            "mock_name": "Proxy to Example",
            "match_method": "GET",
            "match_path": "/api/external",
            "response_body": '{"fallback": "offline"}',
            "mock_mode": "proxy-with-fallback",
            "upstream_url": "https://example.com",
            "timeout_seconds": 5,
        }

        response = client.post("/api/admin/mocks", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["mock_mode"] == "proxy-with-fallback"
        assert data["upstream_url"] == "https://example.com"

    def test_update_mock_to_proxy_mode(self, client):
        """Test updating mock to enable proxy mode."""
        import asyncio

        repo = get_mock_repository()

        # Create mock in mock mode
        mock = MockFactory.create_basic(path="/api/switch")
        mock_id = asyncio.run(repo.create(mock)).mock_id

        # Update to proxy mode
        update_payload = {
            "mock_mode": "proxy-with-fallback",
            "upstream_url": "https://api.example.com",
        }

        response = client.put(f"/api/admin/mocks/{mock_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["mock_mode"] == "proxy-with-fallback"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
