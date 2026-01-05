"""Dependency injection configuration for image services."""

from src.domain.services.image_generator import ImageGenerator
from src.infrastructure.storage.image_storage import ImageStorage
from src.infrastructure.image.dimension_detector import DimensionDetector
from src.domain.repositories.image_repository import (
    ImageRepository,
    InMemoryImageRepository,
)
from src.application.use_cases.generate_image import GenerateImageUseCase
from src.application.use_cases.upload_user_image import UploadUserImageUseCase
from src.application.use_cases.get_responsive_set import (
    GetResponsiveSetUseCase,
)
from src.core.dependencies import get_file_storage
from src.core.config import get_settings

# Global singletons
_image_generator = ImageGenerator()
_dimension_detector = DimensionDetector()
_image_repository: ImageRepository = InMemoryImageRepository()
_image_storage: ImageStorage | None = None


def get_image_storage() -> ImageStorage:
    """Dependency: Get image storage instance."""
    global _image_storage
    if _image_storage is None:
        settings = get_settings()
        file_storage = get_file_storage()
        _image_storage = ImageStorage(
            file_storage=file_storage,
            base_dir=settings.image_storage_path,
        )
    return _image_storage


def get_image_generator() -> ImageGenerator:
    """Dependency: Get image generator instance."""
    return _image_generator


def get_dimension_detector() -> DimensionDetector:
    """Dependency: Get dimension detector instance."""
    return _dimension_detector


def get_image_repository() -> ImageRepository:
    """Dependency: Get image repository instance."""
    return _image_repository


def get_generate_image_use_case() -> GenerateImageUseCase:
    """Dependency: Get GenerateImageUseCase."""
    return GenerateImageUseCase(
        generator=_image_generator,
        storage=get_image_storage(),
        repository=_image_repository,
    )


def get_upload_user_image_use_case() -> UploadUserImageUseCase:
    """Dependency: Get UploadUserImageUseCase."""
    return UploadUserImageUseCase(
        storage=get_image_storage(),
        detector=_dimension_detector,
        repository=_image_repository,
    )


def get_responsive_set_use_case() -> GetResponsiveSetUseCase:
    """Dependency: Get GetResponsiveSetUseCase."""
    return GetResponsiveSetUseCase(
        generate_use_case=get_generate_image_use_case()
    )
