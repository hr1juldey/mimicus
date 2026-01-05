"""Service for generating placeholder images using Pillow."""

import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from src.domain.entities.image_spec import (
    ImageSpec,
    ColorScheme,
    ImageFormat,
)


class ImageGenerator:
    """Generate placeholder images with patterns and text overlays."""

    def __init__(self) -> None:
        """Initialize with default color scheme."""
        self._default_scheme = ColorScheme(
            primary_min=(200, 200, 200),
            primary_max=(255, 255, 255),
            secondary_min=(100, 100, 100),
            secondary_max=(150, 150, 150),
        )

    async def generate(self, spec: ImageSpec) -> bytes:
        """Generate image from specification.

        Args:
            spec: Image specification with dimensions and formatting

        Returns:
            Image data as bytes
        """
        img = self._create_checkerboard(spec)
        if spec.text_overlay or spec.identifier:
            img = self._add_text_overlay(img, spec)
        return self._image_to_bytes(img, spec.format)

    def _create_checkerboard(self, spec: ImageSpec) -> Image.Image:
        """Create checkerboard pattern image."""
        width, height = spec.dimensions.to_tuple()
        scheme = spec.color_scheme or self._default_scheme
        img = Image.new("RGB", (width, height), "white")
        pixels = img.load()
        square_size = max(1, min(width, height) // 20)
        color1 = self._random_color(scheme.primary_min, scheme.primary_max)
        color2 = self._random_color(scheme.secondary_min, scheme.secondary_max)
        for y in range(height):
            for x in range(width):
                is_primary = ((x // square_size) + (y // square_size)) % 2 == 0
                pixels[x, y] = color1 if is_primary else color2
        return img

    def _add_text_overlay(
        self, img: Image.Image, spec: ImageSpec
    ) -> Image.Image:
        """Add text overlay to image."""
        draw = ImageDraw.Draw(img)
        text_parts = []
        if spec.identifier:
            text_parts.append(spec.identifier)
        if spec.text_overlay:
            text_parts.append(spec.text_overlay)
        text_parts.append(spec.dimensions.get_dimension_string())
        text = "\n".join(text_parts)
        font = ImageFont.load_default()
        width, height = img.size
        draw.text(
            (width // 2, height // 2),
            text,
            fill=(255, 255, 255),
            font=font,
            anchor="mm",
        )
        return img

    def _image_to_bytes(
        self, img: Image.Image, fmt: ImageFormat
    ) -> bytes:
        """Convert PIL Image to bytes."""
        buffer = BytesIO()
        fmt_map = {
            ImageFormat.PNG: "PNG",
            ImageFormat.JPEG: "JPEG",
            ImageFormat.WEBP: "WEBP",
        }
        img.save(buffer, format=fmt_map.get(fmt, "PNG"))
        buffer.seek(0)
        return buffer.getvalue()

    def _random_color(
        self, min_rgb: tuple, max_rgb: tuple
    ) -> tuple:
        """Generate random RGB color within specified ranges."""
        return (
            random.randint(min_rgb[0], max_rgb[0]),
            random.randint(min_rgb[1], max_rgb[1]),
            random.randint(min_rgb[2], max_rgb[2]),
        )
