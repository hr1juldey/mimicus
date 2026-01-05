"""Image specification value objects."""

from dataclasses import dataclass
from typing import Optional, Tuple
from enum import Enum


class ImageFormat(str, Enum):
    """Supported image formats."""

    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"


@dataclass(frozen=True)
class ImageDimensions:
    """Immutable image dimensions value object."""

    width: int
    height: int

    def __post_init__(self) -> None:
        """Validate dimensions on creation."""
        if self.width <= 0 or self.height <= 0:
            msg = "Dimensions must be positive integers"
            raise ValueError(msg)
        if self.width > 8000 or self.height > 8000:
            msg = "Dimensions cannot exceed 8000px"
            raise ValueError(msg)

    def to_tuple(self) -> Tuple[int, int]:
        """Convert to (width, height) tuple."""
        return (self.width, self.height)

    @classmethod
    def from_string(cls, dim_str: str) -> "ImageDimensions":
        """Parse '300x200' format string."""
        try:
            parts = dim_str.split("x")
            if len(parts) != 2:
                msg = "Format must be 'WIDTHxHEIGHT', e.g., '300x200'"
                raise ValueError(msg)
            width, height = int(parts[0]), int(parts[1])
            return cls(width, height)
        except ValueError as e:
            msg = f"Invalid dimension format: {dim_str}"
            raise ValueError(msg) from e


@dataclass(frozen=True)
class ColorScheme:
    """Color scheme specification for generated images."""

    primary_min: Tuple[int, int, int]  # RGB
    primary_max: Tuple[int, int, int]  # RGB
    secondary_min: Tuple[int, int, int]  # RGB
    secondary_max: Tuple[int, int, int]  # RGB

    def __post_init__(self) -> None:
        """Validate RGB values."""
        for rgb in [self.primary_min, self.primary_max]:
            for val in rgb:
                if not 0 <= val <= 255:
                    msg = "RGB values must be 0-255"
                    raise ValueError(msg)


@dataclass
class ImageSpec:
    """Complete image specification for generation."""

    dimensions: ImageDimensions
    format: ImageFormat
    text_overlay: Optional[str] = None
    color_scheme: Optional[ColorScheme] = None
    identifier: Optional[str] = None
