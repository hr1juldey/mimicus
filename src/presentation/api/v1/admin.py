"""Admin REST API endpoints for managing mocks."""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from src.core.dependencies import (
    get_create_mock_use_case,
    get_update_mock_use_case,
    get_delete_mock_use_case,
    get_list_mocks_use_case,
    get_get_mock_use_case,
    get_toggle_mock_use_case,
    get_bulk_import_use_case,
    get_mock_mapper,
)
from src.application.use_cases import (
    CreateMockUseCase,
    UpdateMockUseCase,
    DeleteMockUseCase,
    ListMocksUseCase,
    GetMockUseCase,
    ToggleMockUseCase,
    BulkImportUseCase,
)
from src.application.dtos.mock_dtos import (
    CreateMockDTO,
    UpdateMockDTO,
    MockResponseDTO,
    MockListResponseDTO,
)
from src.application.exceptions import MockNotFoundError, InvalidJSONError
from src.application.mappers.mock_mapper import MockMapper


router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/mocks", response_model=MockResponseDTO, status_code=201)
async def create_mock(
    dto: CreateMockDTO,
    use_case: CreateMockUseCase = Depends(get_create_mock_use_case),
    mapper: MockMapper = Depends(get_mock_mapper),
) -> MockResponseDTO:
    """Create a new mock definition."""
    created = await use_case.execute(dto)
    return mapper.entity_to_dto(created)


@router.get("/mocks", response_model=MockListResponseDTO)
async def list_mocks(
    use_case: ListMocksUseCase = Depends(get_list_mocks_use_case),
    mapper: MockMapper = Depends(get_mock_mapper),
) -> MockListResponseDTO:
    """List all mock definitions."""
    mocks = await use_case.execute()
    dtos = [mapper.entity_to_dto(m) for m in mocks]
    return MockListResponseDTO(mocks=dtos, count=len(dtos))


@router.get("/mocks/{mock_id}", response_model=MockResponseDTO)
async def get_mock(
    mock_id: str,
    use_case: GetMockUseCase = Depends(get_get_mock_use_case),
    mapper: MockMapper = Depends(get_mock_mapper),
) -> MockResponseDTO:
    """Get a specific mock definition by ID."""
    try:
        mock = await use_case.execute(mock_id)
        return mapper.entity_to_dto(mock)
    except MockNotFoundError:
        raise HTTPException(status_code=404, detail=f"Mock {mock_id} not found")


@router.put("/mocks/{mock_id}", response_model=MockResponseDTO)
async def update_mock(
    mock_id: str,
    dto: UpdateMockDTO,
    use_case: UpdateMockUseCase = Depends(get_update_mock_use_case),
    mapper: MockMapper = Depends(get_mock_mapper),
) -> MockResponseDTO:
    """Update an existing mock definition."""
    try:
        updated = await use_case.execute(mock_id, dto)
        return mapper.entity_to_dto(updated)
    except MockNotFoundError:
        raise HTTPException(status_code=404, detail=f"Mock {mock_id} not found")


@router.delete("/mocks/{mock_id}", status_code=204)
async def delete_mock(
    mock_id: str,
    use_case: DeleteMockUseCase = Depends(get_delete_mock_use_case),
) -> None:
    """Delete a mock definition."""
    try:
        await use_case.execute(mock_id)
    except MockNotFoundError:
        raise HTTPException(status_code=404, detail=f"Mock {mock_id} not found")


@router.post("/mocks/{mock_id}/toggle", response_model=MockResponseDTO)
async def toggle_mock(
    mock_id: str,
    use_case: ToggleMockUseCase = Depends(get_toggle_mock_use_case),
    mapper: MockMapper = Depends(get_mock_mapper),
) -> MockResponseDTO:
    """Toggle mock enabled/disabled status."""
    try:
        updated = await use_case.execute(mock_id)
        return mapper.entity_to_dto(updated)
    except MockNotFoundError:
        raise HTTPException(status_code=404, detail=f"Mock {mock_id} not found")


@router.post("/mocks/bulk-import")
async def bulk_import_mocks(
    use_case: BulkImportUseCase = Depends(get_bulk_import_use_case),
    mapper: MockMapper = Depends(get_mock_mapper),
    file: UploadFile = File(None),
    json_data: str = None,
) -> dict:
    """Bulk import mocks from JSON file or raw JSON."""
    try:
        if file:
            content = await file.read()
            json_str = content.decode()
        elif json_data:
            json_str = json_data
        else:
            raise ValueError("Must provide either file or json_data")

        result = await use_case.execute(json_str)
        mocks_dtos = [mapper.entity_to_dto(m) for m in result["mocks"]]
        return {
            "created": result["created"],
            "errors": result["errors"],
            "mocks": mocks_dtos,
            "error_details": result["error_details"],
        }
    except InvalidJSONError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
