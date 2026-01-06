"""Jinja2 template rendering service with request context."""

import secrets
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from jinja2 import Environment, BaseLoader, TemplateError
from faker import Faker
from src.domain.entities.request_context import RequestContext


class TemplateService:
    """Service for rendering Jinja2 templates with request context."""

    def __init__(self, state_service: Optional[Any] = None):
        """Initialize Jinja2 environment with custom filters."""
        self.env = Environment(loader=BaseLoader())
        self.faker = Faker()
        self.state_service = state_service
        self._register_filters()

    def _register_filters(self) -> None:
        """Register custom Jinja2 filters and globals."""
        # Helper functions
        self.env.globals["random_token"] = self._random_token
        self.env.globals["faker"] = self.faker
        self.env.globals["now"] = self._now
        self.env.globals["json_dumps"] = json.dumps
        self.env.globals["json_loads"] = json.loads

    @staticmethod
    def _random_token(length: int = 32) -> str:
        """Generate random token."""
        return secrets.token_hex(length // 2)

    @staticmethod
    def _now() -> str:
        """Get current timestamp in ISO format."""
        return datetime.now(timezone.utc).isoformat()

    def _build_context(self, request_context: RequestContext) -> Dict[str, Any]:
        """Build template context from request."""
        context = {
            "request": {
                "method": request_context.request_method,
                "path": request_context.request_path,
                "headers": request_context.request_headers,
                "query": request_context.request_query_params,
                "json": request_context.request_json,
                "body": request_context.request_body,
                "path_params": request_context.request_path_params,
            },
            "env": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        }

        # Add session/state info if available
        if request_context.session_id:
            context["session_id"] = request_context.session_id
        if request_context.client_ip:
            context["client_ip"] = request_context.client_ip

        return context

    async def render_template(
        self, template_str: str, request_context: RequestContext
    ) -> str:
        """Render Jinja2 template with request context."""
        try:
            # Build template context
            context = self._build_context(request_context)

            # Compile and render template
            template = self.env.from_string(template_str)
            rendered = template.render(**context)

            return rendered
        except TemplateError as e:
            # Return error message in JSON format
            error_msg = f"Template error: {str(e)}"
            return json.dumps({"error": error_msg})
        except Exception as e:
            # Catch any other errors
            error_msg = f"Template rendering error: {str(e)}"
            return json.dumps({"error": error_msg})

    @staticmethod
    def is_template(text: str) -> bool:
        """Check if text contains template syntax."""
        if not text or not isinstance(text, str):
            return False
        return "{{" in text or "{%" in text
