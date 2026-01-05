"""Use case for generating responsive image sets."""

from typing import List, Tuple
from src.application.use_cases.generate_image import GenerateImageUseCase
from src.domain.entities.image_spec import ImageSpec, ImageDimensions, ImageFormat
from src.application.dtos.image_dtos import ResponsiveSetDTO, ImageRefDTO
from src.application.exceptions import ValidationError


class GetResponsiveSetUseCase:
    """Generate sets of images for responsive design.

    Business rules:
    - Accept preset name (mobile, tablet, desktop)
    - Generate multiple sizes for each device
    - Return URLs for all variants
    """

    # Device presets with (width, height) tuples
    DEVICE_PRESETS = {
        "mobile": [
            (320, 240),
            (480, 360),
            (640, 480),
        ],
        "tablet": [
            (768, 576),
            (1024, 768),
        ],
        "desktop": [
            (1280, 720),
            (1920, 1080),
            (2560, 1440),
        ],
        "all": [
            (320, 240),
            (480, 360),
            (768, 576),
            (1024, 768),
            (1280, 720),
            (1920, 1080),
            (2560, 1440),
        ],
    }

    def __init__(
        self, generate_use_case: GenerateImageUseCase
    ) -> None:
        """Initialize use case with dependency."""
        self.generate_use_case = generate_use_case

    async def execute(
        self,
        preset: str,
        format: ImageFormat = ImageFormat.WEBP,
    ) -> ResponsiveSetDTO:
        """Generate responsive image set.

        Args:
            preset: Device preset ('mobile', 'tablet', 'desktop', 'all')
            format: Image format for all variants

        Returns:
            ResponsiveSetDTO with image URLs for all sizes

        Raises:
            ValidationError: If preset is invalid
        """
        # Validate preset
        if preset not in self.DEVICE_PRESETS:
            valid = ", ".join(self.DEVICE_PRESETS.keys())
            raise ValidationError(f"Invalid preset. Choose from: {valid}")

        # Get dimension list from preset
        dimensions_list: List[Tuple[int, int]] = (
            self.DEVICE_PRESETS[preset]
        )

        # Generate all variants
        image_refs = []
        for width, height in dimensions_list:
            spec = ImageSpec(
                dimensions=ImageDimensions(width, height),
                format=format,
            )
            metadata = await self.generate_use_case.execute(spec)
            image_refs.append(
                ImageRefDTO(
                    width=width,
                    height=height,
                    url=metadata.get_url(),
                    format=format.value,
                )
            )

        return ResponsiveSetDTO(preset=preset, images=image_refs)
