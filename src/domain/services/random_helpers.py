"""Random data generation helpers."""

import random
import uuid
from faker import Faker


class RandomHelpers:
    """Random data generation helpers."""

    def random_int(self, min_val: int = 0, max_val: int = 100) -> int:
        """Generate a random integer between min_val and max_val."""
        return random.randint(min_val, max_val)

    def random_uuid(self) -> str:
        """Generate a random UUID."""
        return str(uuid.uuid4())

    def random_email(self) -> str:
        """Generate a random email address."""
        return Faker().email()

    def random_phone(self) -> str:
        """Generate a random phone number."""
        return Faker().phone_number()

    def random_name(self) -> str:
        """Generate a random name."""
        return Faker().name()

    def random_address(self) -> str:
        """Generate a random address."""
        return Faker().address()
