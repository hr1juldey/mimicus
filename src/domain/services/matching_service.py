"""Service for matching incoming requests to mock definitions."""

import re
from typing import List, Optional, Tuple, Dict
from src.domain.entities.mock_definition import MockDefinition
from src.domain.entities.request_context import RequestContext


class MatchingService:
    """Service to match incoming requests against mock definitions."""

    @staticmethod
    def _extract_path_params(
        template_path: str, request_path: str
    ) -> Optional[Dict[str, str]]:
        """Extract path parameters from request path using template pattern."""
        # Convert template path like /users/{id} to regex pattern
        pattern = re.sub(r"\{(\w+)\}", r"(?P<\1>[^/]+)", template_path)
        pattern = f"^{pattern}$"

        match = re.match(pattern, request_path)
        if match:
            return match.groupdict()
        return None

    @staticmethod
    def _matches_path(mock_path: str, request_path: str) -> Tuple[bool, Dict[str, str]]:
        """Check if request path matches mock path (exact or template)."""
        # First try exact match
        if mock_path == request_path:
            return True, {}

        # Then try template matching with parameter extraction
        params = MatchingService._extract_path_params(mock_path, request_path)
        if params is not None:
            return True, params

        return False, {}

    @staticmethod
    def _matches_method(mock_method: str, request_method: str) -> bool:
        """Check if HTTP method matches."""
        return mock_method.upper() == request_method.upper()

    @staticmethod
    def _score_match(
        mock: MockDefinition, request: RequestContext, path_params: Dict[str, str]
    ) -> int:
        """Score a match based on specificity. Higher score = better match."""
        score = mock.mock_priority

        # Bonus for exact path match (no template params)
        if not path_params:
            score += 1000

        # Bonus for header match
        if mock.mock_match.match_headers:
            headers_match = all(
                request.get_request_header(k) == v
                for k, v in mock.mock_match.match_headers.items()
            )
            if headers_match:
                score += 500

        return score

    async def find_match(
        self, request: RequestContext, mocks: List[MockDefinition]
    ) -> Optional[Tuple[MockDefinition, Dict[str, str]]]:
        """Find best matching mock definition for incoming request."""
        candidates = []

        for mock in mocks:
            if not mock.is_active():
                continue

            # Check method match
            method = request.request_method
            if not self._matches_method(mock.mock_match.match_method, method):
                continue

            # Check path match
            path_matched, path_params = self._matches_path(
                mock.get_match_path(), request.request_path
            )
            if not path_matched:
                continue

            # Calculate match score
            score = self._score_match(mock, request, path_params)

            candidates.append((mock, path_params, score))

        if not candidates:
            return None

        # Return best scoring match
        best_match = max(candidates, key=lambda x: x[2])
        return (best_match[0], best_match[1])
