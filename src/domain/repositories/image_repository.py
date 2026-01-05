"""Repository interface for image metadata persistence."""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.image_metadata import ImageMetadata


class ImageRepository(ABC):
    """Abstract repository for image metadata operations."""

    @abstractmethod
    async def save_metadata(
        self, metadata: ImageMetadata
    ) -> ImageMetadata:
        """Save or update image metadata."""
        pass

    @abstractmethod
    async def get_by_id(
        self, image_id: str
    ) -> Optional[ImageMetadata]:
        """Retrieve image metadata by ID."""
        pass

    @abstractmethod
    async def get_by_dimensions(
        self, width: int, height: int
    ) -> Optional[ImageMetadata]:
        """Find image by exact dimensions (for caching)."""
        pass

    @abstractmethod
    async def list_all(self) -> List[ImageMetadata]:
        """List all stored image metadata."""
        pass

    @abstractmethod
    async def delete(self, image_id: str) -> None:
        """Delete image metadata."""
        pass


class InMemoryImageRepository(ImageRepository):
    """In-memory implementation of image repository."""

    def __init__(self) -> None:
        """Initialize empty store."""
        self._store: dict[str, ImageMetadata] = {}

    async def save_metadata(
        self, metadata: ImageMetadata
    ) -> ImageMetadata:
        """Save image metadata to memory."""
        self._store[metadata.image_id] = metadata
        return metadata

    async def get_by_id(
        self, image_id: str
    ) -> Optional[ImageMetadata]:
        """Get metadata by ID."""
        return self._store.get(image_id)

    async def get_by_dimensions(
        self, width: int, height: int
    ) -> Optional[ImageMetadata]:
        """Find first image with matching dimensions."""
        for metadata in self._store.values():
            if metadata.is_same_dimensions(width, height):
                return metadata
        return None

    async def list_all(self) -> List[ImageMetadata]:
        """List all stored metadata."""
        return list(self._store.values())

    async def delete(self, image_id: str) -> None:
        """Delete image metadata."""
        self._store.pop(image_id, None)
