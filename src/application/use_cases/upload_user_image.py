"""Use case for uploading and processing user-provided images."""

import uuid
from datetime import datetime
from src.infrastructure.storage.image_storage import ImageStorage
from src.infrastructure.image.dimension_detector import DimensionDetector
from src.domain.repositories.image_repository import ImageRepository
from src.domain.entities.image_metadata import ImageMetadata
from src.application.exceptions import ValidationError


class UploadUserImageUseCase:
    """Upload and process user-provided images.

    Business rules:
    - Validate image data
    - Detect dimensions automatically
    - Rename with dimension suffix
    - Store copy (preserve originals)
    - Save metadata
    """

    def __init__(
        self,
        storage: ImageStorage,
        detector: DimensionDetector,
        repository: ImageRepository,
    ) -> None:
        """Initialize use case with dependencies."""
        self.storage = storage
        self.detector = detector
        self.repository = repository

    async def execute(
        self, image_data: bytes, original_filename: str
    ) -> ImageMetadata:
        """Upload and process user image.

        Args:
            image_data: Raw image binary data
            original_filename: Original filename (e.g., 'product.jpg')

        Returns:
            ImageMetadata for stored image

        Raises:
            ValidationError: If image data is invalid
        """
        # Validate image data
        is_valid = await self.detector.validate(image_data)
        if not is_valid:
            raise ValidationError("Invalid image data or unsupported format")

        # Detect dimensions and format
        dimensions, fmt = await self.detector.detect(image_data)

        # Store with dimension-based name
        file_path = await self.storage.save_user_image(
            image_data, original_filename, dimensions.width, dimensions.height
        )

        # Create metadata
        metadata = ImageMetadata(
            image_id=str(uuid.uuid4()),
            original_filename=original_filename,
            dimensions=dimensions,
            format=fmt,
            file_path=file_path,
            file_size_bytes=len(image_data),
            created_at=datetime.now(),
            is_user_provided=True,
            checksum=self.storage.compute_checksum(image_data),
        )

        # Save metadata
        return await self.repository.save_metadata(metadata)
