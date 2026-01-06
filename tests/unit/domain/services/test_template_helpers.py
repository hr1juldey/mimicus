"""Unit tests for template helper services."""

from src.domain.services.random_helpers import RandomHelpers
from src.domain.services.string_helpers import StringHelpers
from src.domain.services.collection_helpers import CollectionHelpers
from src.domain.services.faker_helpers import FakerHelpers


class TestRandomHelpers:
    """Tests for random data generation helpers."""

    def test_random_int(self):
        """Test random integer generation."""
        helper = RandomHelpers()
        result = helper.random_int(1, 10)
        assert 1 <= result <= 10

    def test_random_uuid(self):
        """Test random UUID generation."""
        helper = RandomHelpers()
        result = helper.random_uuid()
        assert isinstance(result, str)
        assert len(result) == 36  # UUID4 format

    def test_random_email(self):
        """Test random email generation."""
        helper = RandomHelpers()
        result = helper.random_email()
        assert "@" in result
        assert "." in result

    def test_random_phone(self):
        """Test random phone number generation."""
        helper = RandomHelpers()
        result = helper.random_phone()
        assert isinstance(result, str)

    def test_random_name(self):
        """Test random name generation."""
        helper = RandomHelpers()
        result = helper.random_name()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_random_address(self):
        """Test random address generation."""
        helper = RandomHelpers()
        result = helper.random_address()
        assert isinstance(result, str)
        assert len(result) > 0


class TestStringHelpers:
    """Tests for string manipulation helpers."""

    def test_uppercase(self):
        """Test uppercase conversion."""
        helper = StringHelpers()
        result = helper.uppercase("hello")
        assert result == "HELLO"

    def test_lowercase(self):
        """Test lowercase conversion."""
        helper = StringHelpers()
        result = helper.lowercase("HELLO")
        assert result == "hello"

    def test_md5(self):
        """Test MD5 hash generation."""
        helper = StringHelpers()
        result = helper.md5("test")
        assert isinstance(result, str)
        assert len(result) == 32

    def test_sha256(self):
        """Test SHA-256 hash generation."""
        helper = StringHelpers()
        result = helper.sha256("test")
        assert isinstance(result, str)
        assert len(result) == 64

    def test_base64_encode(self):
        """Test base64 encoding."""
        helper = StringHelpers()
        result = helper.base64_encode("test")
        assert result == "dGVzdA=="

    def test_base64_decode(self):
        """Test base64 decoding."""
        helper = StringHelpers()
        result = helper.base64_decode("dGVzdA==")
        assert result == "test"


class TestCollectionHelpers:
    """Tests for collection manipulation helpers."""

    def test_sum_values(self):
        """Test sum of values."""
        helper = CollectionHelpers()
        result = helper.sum_values(1, 2, 3)
        assert result == 6

        result = helper.sum_values([1, 2, 3])
        assert result == 6

        result = helper.sum_values(1, [2, 3], 4)
        assert result == 10

    def test_min_value(self):
        """Test minimum value."""
        helper = CollectionHelpers()
        result = helper.min_value(5, 2, 8)
        assert result == 2

        result = helper.min_value([5, 2, 8])
        assert result == 2

    def test_max_value(self):
        """Test maximum value."""
        helper = CollectionHelpers()
        result = helper.max_value(5, 2, 8)
        assert result == 8

        result = helper.max_value([5, 2, 8])
        assert result == 8

    def test_avg_value(self):
        """Test average value."""
        helper = CollectionHelpers()
        result = helper.avg_value(4, 6, 8)
        assert result == 6.0

        result = helper.avg_value([4, 6, 8])
        assert result == 6.0

    def test_random_choice(self):
        """Test random choice from list."""
        helper = CollectionHelpers()
        items = ["a", "b", "c"]
        result = helper.random_choice(items)
        assert result in items

        result = helper.random_choice([])
        assert result is None


class TestFakerHelpers:
    """Tests for faker data generation helpers."""

    def test_faker_data(self):
        """Test faker data generation."""
        helper = FakerHelpers()
        result = helper.faker_data("name")
        assert isinstance(result, str)
        assert len(result) > 0

        result = helper.faker_data("email")
        assert "@" in result

    def test_sequence(self):
        """Test sequence generation."""
        helper = FakerHelpers()
        result = helper.sequence("test_key", start=0, increment=1)
        assert result == 1  # start + increment

        result = helper.sequence("test_key", start=5, increment=2)
        assert result == 7  # start + increment
