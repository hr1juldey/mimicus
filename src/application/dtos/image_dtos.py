"""Data transfer objects for image operations."""

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class ImageDimensionsDTO(BaseModel):
    """DTO for image dimensions."""

    model_config = ConfigDict(from_attributes=True)

    width: int = Field(..., gt=0, le=8000, description="Width in pixels")
    height: int = Field(..., gt=0, le=8000, description="Height in pixels")


class GenerateImageRequestDTO(BaseModel):
    """DTO for image generation request."""

    width: int = Field(..., gt=0, le=8000)
    height: int = Field(..., gt=0, le=8000)
    format: str = Field(
        default="png", pattern="^(png|jpeg|webp)$"
    )
    text_overlay: Optional[str] = Field(None, max_length=200)
    identifier: Optional[str] = Field(None, max_length=100)


class ImageMetadataResponseDTO(BaseModel):
    """DTO for image metadata response."""

    model_config = ConfigDict(from_attributes=True)

    image_id: str
    original_filename: str
    width: int
    height: int
    format: str
    file_size_bytes: int
    created_at: str
    url: str


class ImageRefDTO(BaseModel):
    """DTO for image reference in responsive sets."""

    width: int
    height: int
    url: str
    format: str


class ResponsiveSetDTO(BaseModel):
    """DTO for responsive image set."""

    preset: str
    images: List[ImageRefDTO]


class UploadImageResponseDTO(BaseModel):
    """DTO for image upload response."""

    image_id: str
    url: str
    dimensions: ImageDimensionsDTO


class ImageListResponseDTO(BaseModel):
    """DTO for listing images."""

    images: List[ImageMetadataResponseDTO]
    total: int
