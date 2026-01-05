"""Image file storage service."""

import hashlib
from typing import Optional
from pathlib import Path
from src.infrastructure.storage.file_storage import FileStorage
from src.domain.entities.image_spec import ImageFormat


class ImageStorage:
    """Service for storing and retrieving image files."""

    def __init__(
        self, file_storage: FileStorage, base_dir: str = "images"
    ) -> None:
        """Initialize image storage."""
        self.file_storage = file_storage
        self.base_dir = base_dir

    async def save_generated(
        self,
        image_data: bytes,
        width: int,
        height: int,
        fmt: ImageFormat,
    ) -> str:
        """Save generated image with dimension-based naming.

        Args:
            image_data: Image bytes
            width: Image width
            height: Image height
            fmt: Image format

        Returns:
            File path where image was saved
        """
        filename = f"generated-{width}x{height}.{fmt.value}"
        path = f"{self.base_dir}/generated/{filename}"
        await self.file_storage.save(path, image_data)
        return path

    async def save_user_image(
        self,
        image_data: bytes,
        original_name: str,
        width: int,
        height: int,
    ) -> str:
        """Save user-provided image with dimension suffix.

        Args:
            image_data: Image bytes
            original_name: Original filename (e.g., 'product.jpg')
            width: Detected width
            height: Detected height

        Returns:
            File path where image was saved
        """
        # Parse filename and extension
        path_obj = Path(original_name)
        stem = path_obj.stem
        ext = path_obj.suffix.lstrip(".")
        if not ext:
            ext = "jpg"

        # Create dimension-suffixed filename
        filename = f"{stem}-{width}x{height}.{ext}"
        path = f"{self.base_dir}/user/{filename}"
        await self.file_storage.save(path, image_data)
        return path

    async def load_image(self, file_path: str) -> Optional[bytes]:
        """Load image binary data from file."""
        return await self.file_storage.load(file_path)

    async def exists(self, file_path: str) -> bool:
        """Check if image file exists."""
        return await self.file_storage.exists(file_path)

    def compute_checksum(self, data: bytes) -> str:
        """Compute SHA256 checksum for image data."""
        return hashlib.sha256(data).hexdigest()
