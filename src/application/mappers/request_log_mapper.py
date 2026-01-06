"""Mappers for request log entities and DTOs."""

from src.domain.entities.request_log import RequestLog
from src.application.dtos.request_log_dtos import RequestLogDTO


class RequestLogMapper:
    """Mapper for RequestLog entity and DTO conversions."""

    def entity_to_dto(self, entity: RequestLog) -> RequestLogDTO:
        """Convert RequestLog entity to RequestLogDTO."""
        return RequestLogDTO(
            log_id=entity.log_id,
            request_method=entity.request_method,
            request_path=entity.request_path,
            request_headers=entity.request_headers,
            request_body=entity.request_body,
            matched_mock_id=entity.matched_mock_id,
            template_context=entity.template_context,
            response_status=entity.response_status,
            response_body=entity.response_body,
            client_ip=entity.client_ip,
            session_id=entity.session_id,
            created_at=entity.created_at,
        )
