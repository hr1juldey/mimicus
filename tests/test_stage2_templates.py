"""Tests for Stage 2 - Template engine functionality."""

import pytest
import asyncio
from fastapi.testclient import TestClient
from src.core.app import create_app
from src.core.dependencies import get_mock_repository, get_template_service
from src.domain.entities.mock_definition import (
    MockDefinition,
    MatchCriteria,
    ResponseConfig,
)
from src.domain.entities.request_context import RequestContext
from src.domain.services.template_service import TemplateService


@pytest.fixture
def template_service():
    """Get template service instance."""
    return get_template_service()


@pytest.fixture
def request_context():
    """Create a sample request context."""
    return RequestContext(
        request_method="POST",
        request_path="/api/login",
        request_headers={"Content-Type": "application/json"},
        request_query_params={"source": "mobile"},
        request_json={"username": "alice@example.com", "password": "secret"},
        request_path_params={"user_id": "123"},
    )


class TestTemplateService:
    """Tests for TemplateService."""

    @pytest.mark.asyncio
    async def test_is_template_detection(self, template_service):
        """Test template detection."""
        assert template_service.is_template("hello {{ name }}")
        assert template_service.is_template("hello {% if x %}yes{% endif %}")
        assert not template_service.is_template("hello world")
        assert not template_service.is_template("")

    @pytest.mark.asyncio
    async def test_simple_variable_interpolation(self, template_service, request_context):
        """Test simple variable interpolation."""
        template = '{"username": "{{ request.json.username }}"}'
        rendered = await template_service.render_template(template, request_context)
        assert "alice@example.com" in rendered

    @pytest.mark.asyncio
    async def test_request_headers_access(self, template_service, request_context):
        """Test accessing request headers in template."""
        template = '{"content_type": "{{ request.headers[\'Content-Type\'] }}"}'
        rendered = await template_service.render_template(template, request_context)
        assert "application/json" in rendered

    @pytest.mark.asyncio
    async def test_request_query_access(self, template_service, request_context):
        """Test accessing query parameters."""
        template = '{"source": "{{ request.query.source }}"}'
        rendered = await template_service.render_template(template, request_context)
        assert "mobile" in rendered

    @pytest.mark.asyncio
    async def test_path_params_access(self, template_service, request_context):
        """Test accessing path parameters."""
        template = '{"user_id": "{{ request.path_params.user_id }}"}'
        rendered = await template_service.render_template(template, request_context)
        assert "123" in rendered

    @pytest.mark.asyncio
    async def test_random_token_helper(self, template_service, request_context):
        """Test random_token helper function."""
        template = '{"token": "{{ random_token() }}"}'
        rendered = await template_service.render_template(template, request_context)
        result = rendered
        assert "token" in result
        # Token should be a hex string
        assert '"token"' in result

    @pytest.mark.asyncio
    async def test_now_helper(self, template_service, request_context):
        """Test now helper function."""
        template = '{"timestamp": "{{ now() }}"}'
        rendered = await template_service.render_template(template, request_context)
        assert "timestamp" in rendered
        assert "T" in rendered  # ISO format includes T

    @pytest.mark.asyncio
    async def test_faker_helper(self, template_service, request_context):
        """Test faker helper for data generation."""
        template = '{"email": "{{ faker.email() }}"}'
        rendered = await template_service.render_template(template, request_context)
        assert "@" in rendered  # Email should contain @
        assert "email" in rendered

    @pytest.mark.asyncio
    async def test_conditional_template(self, template_service, request_context):
        """Test conditional logic in templates."""
        template = '{% if request.json.username %}{"user": "{{ request.json.username }}"}{% else %}{"user": "anonymous"}{% endif %}'
        rendered = await template_service.render_template(template, request_context)
        assert "alice@example.com" in rendered

    @pytest.mark.asyncio
    async def test_loop_template(self, template_service):
        """Test loop logic in templates."""
        ctx = RequestContext(
            request_method="GET",
            request_path="/api/list",
            request_json={"numbers": [1, 2, 3]},
        )
        template = '{"items": [{% for num in request.json.numbers %}{{ num }}{% if not loop.last %},{% endif %}{% endfor %}]}'
        rendered = await template_service.render_template(template, ctx)
        assert "1" in rendered
        assert "2" in rendered
        assert "3" in rendered

    @pytest.mark.asyncio
    async def test_template_error_handling(self, template_service, request_context):
        """Test error handling in template rendering."""
        # Invalid template syntax
        template = '{{ undefined_var | nonexistent_filter }}'
        rendered = await template_service.render_template(template, request_context)
        # Should contain error message
        assert "error" in rendered.lower()

    @pytest.mark.asyncio
    async def test_json_dumps_helper(self, template_service):
        """Test json_dumps helper."""
        ctx = RequestContext(
            request_method="GET",
            request_path="/",
            request_json={"key": "value"},
        )
        template = '{{ json_dumps(request.json) }}'
        rendered = await template_service.render_template(template, ctx)
        assert "key" in rendered
        assert "value" in rendered


class TestTemplateIntegration:
    """Integration tests for template responses."""

    @pytest.fixture
    def app(self):
        """Create test app."""
        return create_app()

    @pytest.fixture
    def client(self, app):
        """Create test client."""
        return TestClient(app)

    @pytest.mark.asyncio
    async def test_template_response_with_request_echo(self, client):
        """Test template response that echoes request data."""
        mock_repo = get_mock_repository()

        # Create mock with template that echoes username
        mock = MockDefinition(
            mock_id="login-response",
            mock_name="Login with Echo",
            mock_match=MatchCriteria(match_method="POST", match_path="/api/login"),
            mock_response=ResponseConfig(
                response_status=200,
                response_body='{"user": "{{ request.json.username }}", "token": "{{ random_token() }}"}',
                is_template=True,
            ),
        )
        await mock_repo.create(mock)

        # Send request
        response = client.post(
            "/api/login", json={"username": "bob@example.com", "password": "secret"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["user"] == "bob@example.com"
        assert "token" in data
        assert len(data["token"]) > 0

    @pytest.mark.asyncio
    async def test_template_with_conditional_logic(self, client):
        """Test template with conditional logic."""
        mock_repo = get_mock_repository()

        # Clear any existing mocks
        all_mocks = await mock_repo.get_all()
        for m in all_mocks:
            await mock_repo.delete(m.mock_id)

        mock = MockDefinition(
            mock_id="user-status",
            mock_name="User Status",
            mock_match=MatchCriteria(match_method="GET", match_path="/api/users/{id}"),
            mock_response=ResponseConfig(
                response_status=200,
                response_body='{% if request.path_params.id == "1" %}{"name": "Admin", "role": "admin"}{% else %}{"name": "User", "role": "user"}{% endif %}',
                is_template=True,
            ),
        )
        await mock_repo.create(mock)

        # Test admin user
        response = client.get("/api/users/1")
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "admin"

        # Test regular user
        response = client.get("/api/users/2")
        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "user"

    @pytest.mark.asyncio
    async def test_static_response_still_works(self, client):
        """Test that static responses still work (is_template=False)."""
        mock_repo = get_mock_repository()

        mock = MockDefinition(
            mock_id="static-response",
            mock_name="Static Data",
            mock_match=MatchCriteria(match_method="GET", match_path="/api/static"),
            mock_response=ResponseConfig(
                response_status=200,
                response_body='{"data": "{{ this_should_not_render }}"}',
                is_template=False,  # Explicitly static
            ),
        )
        await mock_repo.create(mock)

        response = client.get("/api/static")
        assert response.status_code == 200
        data = response.json()
        # Template syntax should not be rendered
        assert "{{ this_should_not_render }}" in data["data"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
