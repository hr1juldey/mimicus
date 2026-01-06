"""API endpoints for state management."""

from fastapi import APIRouter, Depends, HTTPException
from src.core.dependencies import (
    get_state_service,
)
from src.application.use_cases.get_state import GetStateUseCase
from src.application.use_cases.set_state import SetStateUseCase
from src.application.use_cases.increment_state import IncrementStateUseCase
from src.application.use_cases.delete_state import DeleteStateUseCase
from src.application.use_cases.list_session_state import ListSessionStateUseCase
from src.domain.services.state_service import StateService
from src.application.dtos.state_dtos import SetStateDTO, StateDTO, StateListDTO


router = APIRouter(prefix="/api/admin/state", tags=["state"])


@router.get("/{session_id}")
async def get_session_state(
    session_id: str,
    state_service: StateService = Depends(get_state_service),
) -> StateListDTO:
    """List all state for a session."""
    use_case = ListSessionStateUseCase(state_service)
    state_dict = await use_case.execute(session_id)
    states = [
        StateDTO(state_key=k, state_value=v, session_id=session_id)
        for k, v in state_dict.items()
    ]
    return StateListDTO(states=states, count=len(states))


@router.get("/{session_id}/{state_key}")
async def get_state(
    session_id: str,
    state_key: str,
    state_service: StateService = Depends(get_state_service),
) -> dict:
    """Get specific state value."""
    use_case = GetStateUseCase(state_service)
    value = await use_case.execute(state_key, session_id)
    if value is None:
        raise HTTPException(status_code=404, detail="State not found")
    return {"state_key": state_key, "state_value": value}


@router.post("/{session_id}")
async def set_state(
    session_id: str,
    dto: SetStateDTO,
    state_service: StateService = Depends(get_state_service),
) -> dict:
    """Set state value."""
    use_case = SetStateUseCase(state_service)
    await use_case.execute(dto.state_key, dto.state_value, session_id)
    return {"state_key": dto.state_key, "state_value": dto.state_value}


@router.put("/{session_id}/{state_key}/increment")
async def increment_state(
    session_id: str,
    state_key: str,
    delta: int = 1,
    state_service: StateService = Depends(get_state_service),
) -> dict:
    """Increment counter and return new value."""
    use_case = IncrementStateUseCase(state_service)
    new_value = await use_case.execute(state_key, session_id, delta)
    return {"state_key": state_key, "new_value": new_value}


@router.delete("/{session_id}/{state_key}")
async def delete_state(
    session_id: str,
    state_key: str,
    state_service: StateService = Depends(get_state_service),
) -> dict:
    """Delete state by key."""
    use_case = DeleteStateUseCase(state_service)
    deleted = await use_case.execute(state_key, session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="State not found")
    return {"deleted": True, "state_key": state_key}
