"""Mappers between DTOs and domain entities."""

import uuid
from src.application.dtos.mock_dtos import (
    CreateMockDTO,
    UpdateMockDTO,
    MockResponseDTO,
)
from src.domain.entities.mock_definition import (
    MockDefinition,
    MatchCriteria,
    ResponseConfig,
)


class MockMapper:
    """Mapper for MockDefinition conversions."""

    @staticmethod
    def dto_to_entity(dto: CreateMockDTO) -> MockDefinition:
        """Convert CreateMockDTO to MockDefinition entity."""
        mock_id = str(uuid.uuid4())

        match_criteria = MatchCriteria(
            match_method=dto.match_method,
            match_path=dto.match_path,
            match_headers=dto.match_headers,
            match_query=dto.match_query,
        )

        response_config = ResponseConfig(
            response_status=dto.response_status,
            response_headers=dto.response_headers,
            response_body=dto.response_body,
            response_delay_ms=dto.response_delay_ms,
            is_template=dto.is_template,
        )

        return MockDefinition(
            mock_id=mock_id,
            mock_name=dto.mock_name,
            mock_priority=dto.mock_priority,
            mock_enabled=dto.mock_enabled,
            mock_mode=dto.mock_mode,
            mock_match=match_criteria,
            mock_response=response_config,
            upstream_url=dto.upstream_url,
            timeout_seconds=dto.timeout_seconds,
        )

    @staticmethod
    def entity_to_dto(entity: MockDefinition) -> MockResponseDTO:
        """Convert MockDefinition entity to MockResponseDTO."""
        return MockResponseDTO(
            mock_id=entity.mock_id,
            mock_name=entity.mock_name,
            mock_priority=entity.mock_priority,
            mock_enabled=entity.mock_enabled,
            mock_mode=entity.mock_mode,
            response_status=entity.mock_response.response_status,
            response_headers=entity.mock_response.response_headers,
            response_body=entity.mock_response.response_body,
            response_delay_ms=entity.mock_response.response_delay_ms,
            is_template=entity.mock_response.is_template,
            upstream_url=entity.upstream_url,
        )

    @staticmethod
    def apply_update(
        entity: MockDefinition, update_dto: UpdateMockDTO
    ) -> MockDefinition:
        """Apply UpdateMockDTO changes to existing entity."""
        if update_dto.mock_name is not None:
            entity.mock_name = update_dto.mock_name
        if update_dto.mock_priority is not None:
            entity.mock_priority = update_dto.mock_priority
        if update_dto.mock_enabled is not None:
            entity.mock_enabled = update_dto.mock_enabled
        if update_dto.mock_mode is not None:
            entity.mock_mode = update_dto.mock_mode

        if update_dto.response_status is not None:
            entity.mock_response.response_status = update_dto.response_status
        if update_dto.response_headers is not None:
            entity.mock_response.response_headers = update_dto.response_headers
        if update_dto.response_body is not None:
            entity.mock_response.response_body = update_dto.response_body
        if update_dto.response_delay_ms is not None:
            entity.mock_response.response_delay_ms = update_dto.response_delay_ms
        if update_dto.is_template is not None:
            entity.mock_response.is_template = update_dto.is_template
        if update_dto.upstream_url is not None:
            entity.upstream_url = update_dto.upstream_url
        if update_dto.timeout_seconds is not None:
            entity.timeout_seconds = update_dto.timeout_seconds

        return entity
