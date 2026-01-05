"""Image metadata entity."""

from dataclasses import dataclass
from datetime import datetime
from src.domain.entities.image_spec import ImageDimensions, ImageFormat


@dataclass
class ImageMetadata:
    """Entity representing stored image metadata."""

    image_id: str
    original_filename: str
    dimensions: ImageDimensions
    format: ImageFormat
    file_path: str
    file_size_bytes: int
    created_at: datetime
    is_user_provided: bool
    checksum: str

    def is_same_dimensions(
        self, width: int, height: int
    ) -> bool:
        """Check if dimensions match."""
        return (
            self.dimensions.width == width
            and self.dimensions.height == height
        )

    def get_url(self, base_url: str = "/api/images") -> str:
        """Generate URL for this image."""
        return f"{base_url}/{self.image_id}"

    def get_dimension_string(self) -> str:
        """Get dimension as 'WIDTHxHEIGHT' string."""
        return f"{self.dimensions.width}x{self.dimensions.height}"
