"""File storage abstraction for saving and loading files."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class FileStorage(ABC):
    """Abstract file storage interface."""

    @abstractmethod
    async def save(self, file_path: str, content: bytes) -> str:
        """Save file content.

        Args:
            file_path: Path where file should be saved
            content: File content as bytes

        Returns:
            Actual file path where saved
        """
        pass

    @abstractmethod
    async def load(self, file_path: str) -> Optional[bytes]:
        """Load file content.

        Args:
            file_path: Path of file to load

        Returns:
            File content as bytes, or None if not found
        """
        pass

    @abstractmethod
    async def delete(self, file_path: str) -> None:
        """Delete a file.

        Args:
            file_path: Path of file to delete
        """
        pass

    @abstractmethod
    async def exists(self, file_path: str) -> bool:
        """Check if file exists.

        Args:
            file_path: Path to check

        Returns:
            True if file exists, False otherwise
        """
        pass


class LocalFileStorage(FileStorage):
    """Local filesystem storage implementation."""

    def __init__(self, base_path: str = "./storage"):
        """Initialize local file storage.

        Args:
            base_path: Base directory for file storage
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save(self, file_path: str, content: bytes) -> str:
        """Save file to local filesystem."""
        target = self.base_path / file_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return str(target)

    async def load(self, file_path: str) -> Optional[bytes]:
        """Load file from local filesystem."""
        target = self.base_path / file_path
        if target.exists():
            return target.read_bytes()
        return None

    async def delete(self, file_path: str) -> None:
        """Delete file from local filesystem."""
        target = self.base_path / file_path
        if target.exists():
            target.unlink()

    async def exists(self, file_path: str) -> bool:
        """Check if file exists locally."""
        target = self.base_path / file_path
        return target.exists()
