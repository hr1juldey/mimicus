"""Image generation and serving API endpoints."""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import Response
from src.core.dependencies_image import (
    get_generate_image_use_case,
    get_responsive_set_use_case,
    get_upload_user_image_use_case,
    get_image_storage,
)
from src.application.dtos.image_dtos import (
    GenerateImageRequestDTO,
    ImageMetadataResponseDTO,
    ResponsiveSetDTO,
    UploadImageResponseDTO,
    ImageListResponseDTO,
)
from src.domain.entities.image_spec import ImageSpec, ImageDimensions, ImageFormat
from src.application.exceptions import ValidationError

router = APIRouter(prefix="/api/images", tags=["images"])


@router.get("/{width}x{height}", response_class=Response)
async def generate_and_serve_image(
    width: int, height: int, format: str = "png",
    text: str = None, identifier: str = None,
    use_case = Depends(get_generate_image_use_case),
    storage = Depends(get_image_storage),
):
    """Generate or serve cached image by dimensions."""
    try:
        spec = ImageSpec(
            dimensions=ImageDimensions(width, height),
            format=ImageFormat(format),
            text_overlay=text, identifier=identifier,
        )
        metadata = await use_case.execute(spec)
        image_data = await storage.load_image(metadata.file_path)
        return Response(content=image_data, media_type=f"image/{format}",
                       headers={"Cache-Control": "public, max-age=86400"})
    except (ValueError, ValidationError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate", response_model=ImageMetadataResponseDTO)
async def generate_image_metadata(
    request: GenerateImageRequestDTO,
    use_case = Depends(get_generate_image_use_case),
):
    """Generate image and return metadata (not binary)."""
    try:
        spec = ImageSpec(
            dimensions=ImageDimensions(request.width, request.height),
            format=ImageFormat(request.format),
            text_overlay=request.text_overlay,
            identifier=request.identifier,
        )
        metadata = await use_case.execute(spec)
        return ImageMetadataResponseDTO(
            image_id=metadata.image_id,
            original_filename=metadata.original_filename,
            width=metadata.dimensions.width,
            height=metadata.dimensions.height,
            format=metadata.format.value,
            file_size_bytes=metadata.file_size_bytes,
            created_at=metadata.created_at.isoformat(),
            url=metadata.get_url(),
        )
    except (ValueError, ValidationError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/responsive/{preset}", response_model=ResponsiveSetDTO)
async def get_responsive_set(
    preset: str, use_case = Depends(get_responsive_set_use_case)
):
    """Get responsive image set URLs."""
    try:
        return await use_case.execute(preset)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload", response_model=UploadImageResponseDTO)
async def upload_user_image(
    file: UploadFile = File(...),
    use_case = Depends(get_upload_user_image_use_case),
):
    """Upload user-provided image."""
    try:
        content = await file.read()
        metadata = await use_case.execute(content, file.filename)
        return UploadImageResponseDTO(
            image_id=metadata.image_id, url=metadata.get_url(),
            dimensions={"width": metadata.dimensions.width,
                       "height": metadata.dimensions.height},
        )
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
