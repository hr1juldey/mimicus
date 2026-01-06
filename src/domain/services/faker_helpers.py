"""Faker data generation helpers."""

from faker import Faker


class FakerHelpers:
    """Faker data generation helpers."""

    def __init__(self):
        """Initialize faker instance."""
        self.faker = Faker()

    def faker_data(self, field: str) -> str:
        """Generate fake data based on field type."""
        if hasattr(self.faker, field):
            return str(getattr(self.faker, field)())
        return self.faker.text()

    def sequence(self, key: str, start: int = 0, increment: int = 1) -> int:
        """
        Generate a sequence value (placeholder implementation).
        In a real implementation, this would interact with state service.
        """
        # This is a placeholder - in a real implementation, this would use the state service
        # to maintain sequence counters across requests
        return start + increment
