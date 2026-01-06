"""Inspector API endpoints for request logging and audit."""

from fastapi import APIRouter, Depends, Query
from typing import Optional
from src.core.dependencies import (
    get_request_log_service,
)
from src.domain.services.request_log_service import RequestLogService
from src.application.dtos.request_log_dtos import (
    RequestLogDTO,
    RequestLogListResponseDTO,
)
from src.application.mappers.request_log_mapper import RequestLogMapper


router = APIRouter(prefix="/api/admin", tags=["inspector"])


@router.get("/inspector/requests", response_model=RequestLogListResponseDTO)
async def list_request_logs(
    session_id: Optional[str] = Query(None, description="Filter by session ID"),
    mock_id: Optional[str] = Query(None, description="Filter by mock ID"),
    limit: int = Query(50, ge=1, le=100, description="Limit number of results"),
    request_log_service: RequestLogService = Depends(get_request_log_service),
    mapper: RequestLogMapper = Depends(lambda: RequestLogMapper()),
) -> RequestLogListResponseDTO:
    """List request logs with optional filtering."""
    if session_id:
        logs = await request_log_service.get_logs_by_session(session_id, limit)
    elif mock_id:
        logs = await request_log_service.get_logs_by_mock(mock_id, limit)
    else:
        logs = await request_log_service.get_recent_logs(limit)

    dtos = [mapper.entity_to_dto(log) for log in logs]
    return RequestLogListResponseDTO(logs=dtos, count=len(dtos))


@router.get("/inspector/requests/{log_id}", response_model=RequestLogDTO)
async def get_request_log(
    log_id: str,
    request_log_service: RequestLogService = Depends(get_request_log_service),
    mapper: RequestLogMapper = Depends(lambda: RequestLogMapper()),
) -> RequestLogDTO:
    """Get a specific request log by ID."""
    log = await request_log_service.get_log_by_id(log_id)
    if not log:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Request log not found")

    return mapper.entity_to_dto(log)


@router.get(
    "/inspector/mocks/{mock_id}/requests", response_model=RequestLogListResponseDTO
)
async def get_requests_for_mock(
    mock_id: str,
    limit: int = Query(50, ge=1, le=100, description="Limit number of results"),
    request_log_service: RequestLogService = Depends(get_request_log_service),
    mapper: RequestLogMapper = Depends(lambda: RequestLogMapper()),
) -> RequestLogListResponseDTO:
    """Get request logs for a specific mock."""
    logs = await request_log_service.get_logs_by_mock(mock_id, limit)
    dtos = [mapper.entity_to_dto(log) for log in logs]
    return RequestLogListResponseDTO(logs=dtos, count=len(dtos))
