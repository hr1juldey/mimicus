"""Mapper for State entity and DTO conversions."""

from src.domain.entities.state import State
from src.application.dtos.state_dtos import StateDTO, SetStateDTO


class StateMapper:
    """Mapper between State entities and DTOs."""

    @staticmethod
    def entity_to_dto(entity: State) -> StateDTO:
        """Convert State entity to StateDTO."""
        return StateDTO(
            state_key=entity.state_key,
            state_value=entity.state_value,
            session_id=entity.session_id,
            mock_id=entity.mock_id,
            client_ip=entity.client_ip,
        )

    @staticmethod
    def dto_to_entity(dto: SetStateDTO, session_id: str) -> State:
        """Convert SetStateDTO to State entity."""
        return State.create(
            state_key=dto.state_key,
            state_value=dto.state_value,
            session_id=session_id,
        )
