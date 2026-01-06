"""Template helper functions for Jinja2 templates."""

import random
from typing import Any, List, Union
from faker import Faker


class CollectionHelpers:
    """Collection manipulation helpers."""

    def sum_values(self, *args) -> Union[int, float]:
        """Calculate the sum of provided values."""
        total = 0
        for arg in args:
            if isinstance(arg, (int, float)):
                total += arg
            elif isinstance(arg, (list, tuple)):
                for item in arg:
                    if isinstance(item, (int, float)):
                        total += item
        return total

    def min_value(self, *args) -> Union[int, float, None]:
        """Find the minimum value among provided values."""
        values = []
        for arg in args:
            if isinstance(arg, (int, float)):
                values.append(arg)
            elif isinstance(arg, (list, tuple)):
                for item in arg:
                    if isinstance(item, (int, float)):
                        values.append(item)
        return min(values) if values else None

    def max_value(self, *args) -> Union[int, float, None]:
        """Find the maximum value among provided values."""
        values = []
        for arg in args:
            if isinstance(arg, (int, float)):
                values.append(arg)
            elif isinstance(arg, (list, tuple)):
                for item in arg:
                    if isinstance(item, (int, float)):
                        values.append(item)
        return max(values) if values else None

    def avg_value(self, *args) -> Union[float, None]:
        """Calculate the average of provided values."""
        values = []
        for arg in args:
            if isinstance(arg, (int, float)):
                values.append(arg)
            elif isinstance(arg, (list, tuple)):
                for item in arg:
                    if isinstance(item, (int, float)):
                        values.append(item)
        return sum(values) / len(values) if values else None

    def random_choice(self, items: List[Any]) -> Any:
        """Randomly select an item from a list."""
        if not items:
            return None
        return random.choice(items)


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
