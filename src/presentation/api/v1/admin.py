"""Admin REST API endpoints for managing mocks."""

import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from src.core.dependencies import get_mock_repository
from src.domain.repositories.mock_repository import MockRepository
from src.application.dtos.mock_dtos import (
    CreateMockDTO,
    UpdateMockDTO,
    MockResponseDTO,
    MockListResponseDTO,
    ErrorResponseDTO,
)
from src.application.mappers.mock_mapper import MockMapper


router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/mocks", response_model=MockResponseDTO, status_code=201)
async def create_mock(
    dto: CreateMockDTO, repo: MockRepository = Depends(get_mock_repository)
) -> MockResponseDTO:
    """Create a new mock definition."""
    entity = MockMapper.dto_to_entity(dto)
    created = await repo.create(entity)
    return MockMapper.entity_to_dto(created)


@router.get("/mocks", response_model=MockListResponseDTO)
async def list_mocks(
    repo: MockRepository = Depends(get_mock_repository),
) -> MockListResponseDTO:
    """List all mock definitions."""
    mocks = await repo.get_all()
    dtos = [MockMapper.entity_to_dto(m) for m in mocks]
    return MockListResponseDTO(mocks=dtos, count=len(dtos))


@router.get("/mocks/{mock_id}", response_model=MockResponseDTO)
async def get_mock(
    mock_id: str, repo: MockRepository = Depends(get_mock_repository)
) -> MockResponseDTO:
    """Get a specific mock definition by ID."""
    mock = await repo.get_by_id(mock_id)
    if not mock:
        raise HTTPException(status_code=404, detail=f"Mock {mock_id} not found")
    return MockMapper.entity_to_dto(mock)


@router.put("/mocks/{mock_id}", response_model=MockResponseDTO)
async def update_mock(
    mock_id: str,
    dto: UpdateMockDTO,
    repo: MockRepository = Depends(get_mock_repository),
) -> MockResponseDTO:
    """Update an existing mock definition."""
    existing = await repo.get_by_id(mock_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Mock {mock_id} not found")

    updated = MockMapper.apply_update(existing, dto)
    result = await repo.update(updated)
    return MockMapper.entity_to_dto(result)


@router.delete("/mocks/{mock_id}", status_code=204)
async def delete_mock(
    mock_id: str, repo: MockRepository = Depends(get_mock_repository)
) -> None:
    """Delete a mock definition."""
    existing = await repo.get_by_id(mock_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Mock {mock_id} not found")

    await repo.delete(mock_id)


@router.post("/mocks/{mock_id}/toggle", response_model=MockResponseDTO)
async def toggle_mock(
    mock_id: str, repo: MockRepository = Depends(get_mock_repository)
) -> MockResponseDTO:
    """Toggle mock enabled/disabled status."""
    mock = await repo.get_by_id(mock_id)
    if not mock:
        raise HTTPException(status_code=404, detail=f"Mock {mock_id} not found")

    mock.mock_enabled = not mock.mock_enabled
    updated = await repo.update(mock)
    return MockMapper.entity_to_dto(updated)


@router.post("/mocks/bulk-import")
async def bulk_import_mocks(
    repo: MockRepository = Depends(get_mock_repository),
    file: UploadFile = File(None),
    json_data: str = None,
) -> dict:
    """Bulk import mocks from JSON file or raw JSON."""
    try:
        if file:
            content = await file.read()
            data = json.loads(content.decode())
        elif json_data:
            data = json.loads(json_data)
        else:
            raise ValueError("Must provide either file or json_data")

        mocks_data = data.get("mocks", [])
        created_mocks = []
        errors = []

        for idx, mock_data in enumerate(mocks_data):
            try:
                dto = CreateMockDTO(**mock_data)
                entity = MockMapper.dto_to_entity(dto)
                created = await repo.create(entity)
                created_mocks.append(MockMapper.entity_to_dto(created))
            except Exception as e:
                errors.append({"index": idx, "error": str(e)})

        return {
            "created": len(created_mocks),
            "errors": len(errors),
            "mocks": created_mocks,
            "error_details": errors,
        }

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
