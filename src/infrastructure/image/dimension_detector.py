"""Service for detecting image dimensions and validating image data."""

from io import BytesIO
from PIL import Image
from src.domain.entities.image_spec import ImageDimensions, ImageFormat


class DimensionDetector:
    """Detect dimensions and format from image binary data."""

    async def detect(self, image_data: bytes) -> tuple[ImageDimensions, ImageFormat]:
        """Detect dimensions and format from image bytes.

        Args:
            image_data: Raw image binary data

        Returns:
            Tuple of (ImageDimensions, ImageFormat)

        Raises:
            ValueError: If image data is invalid
        """
        try:
            img = Image.open(BytesIO(image_data))
            width, height = img.size

            # Map PIL format to our enum
            format_map = {
                "PNG": ImageFormat.PNG,
                "JPEG": ImageFormat.JPEG,
                "JPG": ImageFormat.JPEG,
                "WEBP": ImageFormat.WEBP,
            }

            img_format = format_map.get(
                img.format.upper() if img.format else "PNG",
                ImageFormat.PNG,
            )

            return ImageDimensions(width, height), img_format
        except (OSError, AttributeError) as e:
            msg = f"Invalid image data: {e}"
            raise ValueError(msg) from e

    async def validate(self, image_data: bytes) -> bool:
        """Validate that data is a valid image.

        Args:
            image_data: Raw image binary data

        Returns:
            True if valid, False otherwise
        """
        try:
            img = Image.open(BytesIO(image_data))
            img.verify()
            return True
        except Exception:
            return False
