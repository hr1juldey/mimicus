"""Use case for generating and caching placeholder images."""

import uuid
from datetime import datetime
from src.domain.services.image_generator import ImageGenerator
from src.infrastructure.storage.image_storage import ImageStorage
from src.domain.repositories.image_repository import ImageRepository
from src.domain.entities.image_spec import ImageSpec
from src.domain.entities.image_metadata import ImageMetadata


class GenerateImageUseCase:
    """Generate and store images with caching.

    Business rules:
    - Check cache for existing image with same dimensions
    - Generate only if not cached
    - Store both file and metadata
    - Return metadata with file path
    """

    def __init__(
        self,
        generator: ImageGenerator,
        storage: ImageStorage,
        repository: ImageRepository,
    ) -> None:
        """Initialize use case with dependencies."""
        self.generator = generator
        self.storage = storage
        self.repository = repository

    async def execute(self, spec: ImageSpec) -> ImageMetadata:
        """Generate or retrieve cached image.

        Args:
            spec: Image specification

        Returns:
            ImageMetadata with file path and details
        """
        # Check cache first
        existing = await self.repository.get_by_dimensions(
            spec.dimensions.width, spec.dimensions.height
        )
        if existing:
            return existing

        # Generate new image
        image_data = await self.generator.generate(spec)

        # Store file
        file_path = await self.storage.save_generated(
            image_data,
            spec.dimensions.width,
            spec.dimensions.height,
            spec.format,
        )

        # Create metadata
        metadata = ImageMetadata(
            image_id=str(uuid.uuid4()),
            original_filename=f"generated-{spec.dimensions.width}x"
            f"{spec.dimensions.height}",
            dimensions=spec.dimensions,
            format=spec.format,
            file_path=file_path,
            file_size_bytes=len(image_data),
            created_at=datetime.now(),
            is_user_provided=False,
            checksum=self.storage.compute_checksum(image_data),
        )

        # Save metadata
        return await self.repository.save_metadata(metadata)
