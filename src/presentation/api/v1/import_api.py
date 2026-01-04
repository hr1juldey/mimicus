"""API endpoints for importing specifications and bulk data."""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from src.core.dependencies import (
    get_bulk_import_use_case,
    get_mock_mapper,
)
from src.application.use_cases.bulk_import import BulkImportUseCase
from src.application.mappers.mock_mapper import MockMapper
from src.application.exceptions import InvalidJSONError


router = APIRouter(prefix="/api/import", tags=["import"])


@router.post("/json")
async def import_json_file(
    file: UploadFile = File(...),
    use_case: BulkImportUseCase = Depends(get_bulk_import_use_case),
    mapper: MockMapper = Depends(get_mock_mapper),
) -> dict:
    """Import mocks from JSON file.

    Args:
        file: JSON file with mocks array
        use_case: Bulk import use case
        mapper: Mock mapper for DTO conversion

    Returns:
        Dict with import results (created count, errors, mocks)

    Raises:
        HTTPException: If import fails
    """
    try:
        content = await file.read()
        json_str = content.decode()

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
