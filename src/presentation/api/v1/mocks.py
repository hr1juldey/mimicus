"""Mock handler endpoints - catch-all route for matching requests."""

import json
from fastapi import APIRouter, Request, Depends
from fastapi.responses import Response as FastAPIResponse
from src.core.dependencies import (
    get_mock_repository,
    get_matching_service,
    get_response_service,
)
from src.domain.repositories.mock_repository import MockRepository
from src.domain.services.matching_service import MatchingService
from src.domain.services.response_service import ResponseService
from src.domain.services.proxy_service import ProxyService
from src.infrastructure.external.http_client import HTTPClient
from src.domain.entities.request_context import RequestContext


router = APIRouter(tags=["mocks"])


async def build_request_context(request: Request) -> RequestContext:
    """Build RequestContext from FastAPI Request."""
    # Read body if present
    body = None
    request_json = None

    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.body()
            body_str = body.decode() if body else None

            # Try to parse as JSON
            if body_str:
                request_json = json.loads(body_str)
        except Exception:
            pass

    # Extract headers
    headers = dict(request.headers)

    # Extract query params
    query_params = dict(request.query_params)

    # Extract path params (will be added by matching service)
    path_params = {}

    # Extract session_id from headers (X-Session-ID)
    session_id = headers.get("X-Session-ID") or headers.get("x-session-id")

    # Extract client IP
    client_ip = None
    if request.client:
        client_ip = request.client.host

    return RequestContext(
        request_method=request.method,
        request_path=request.url.path,
        request_headers=headers,
        request_query_params=query_params,
        request_body=body.decode() if body else None,
        request_json=request_json,
        request_path_params=path_params,
        session_id=session_id,
        client_ip=client_ip,
    )


@router.api_route(
    "/{full_path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
)
async def handle_mock_request(
    request: Request,
    full_path: str,
    mock_repository: MockRepository = Depends(get_mock_repository),
    matching_service: MatchingService = Depends(get_matching_service),
    response_service: ResponseService = Depends(get_response_service),
) -> FastAPIResponse:
    """Handle incoming requests and match to mocks."""
    # Build request context
    request_context = await build_request_context(request)

    # Get all mocks from repository
    all_mocks = await mock_repository.get_all()

    # Find matching mock
    match_result = await matching_service.find_match(request_context, all_mocks)

    if not match_result:
        # No match found - return 404
        return FastAPIResponse(
            content=json.dumps(
                {
                    "error": "No matching mock found",
                    "path": request_context.request_path,
                    "method": request_context.request_method,
                }
            ),
            status_code=404,
            media_type="application/json",
        )

    # Extract matched mock and path params
    matched_mock, path_params = match_result

    # Update request context with path params
    request_context.request_path_params = path_params

    # Check mock mode and handle accordingly
    if matched_mock.mock_mode in ["proxy", "proxy-with-fallback", "passthrough"]:
        # Handle proxy modes
        proxy_service = ProxyService(http_client=HTTPClient())
        response = await proxy_service.handle_proxy_request(
            matched_mock, request_context, response_service
        )
    else:
        # Handle mock mode (default)
        response = await response_service.generate_response(
            matched_mock, request_context
        )

    return response
