"""Tests for RateLimiterService."""

import time
from src.domain.services.rate_limiter_service import RateLimiterService


class TestRateLimiterBasic:
    """Test basic rate limiting functionality."""

    def test_allows_initial_requests(self):
        """Initial requests should be allowed."""
        limiter = RateLimiterService()
        assert limiter.is_allowed("mock1", "192.168.1.1")
        assert limiter.is_allowed("mock1", "192.168.1.1")
        assert limiter.is_allowed("mock1", "192.168.1.1")

    def test_burst_limit(self):
        """Burst limit should restrict rapid requests."""
        limiter = RateLimiterService()
        # With burst=5, limit_per_minute=5, should allow 5 requests max
        for i in range(5):
            assert limiter.is_allowed(
                "mock1", "192.168.1.1", burst=5, limit_per_minute=5
            )
        # 6th request should fail
        assert not limiter.is_allowed(
            "mock1", "192.168.1.1", burst=5, limit_per_minute=5
        )

    def test_different_clients_independent(self):
        """Different clients should have independent limits."""
        limiter = RateLimiterService()
        for i in range(5):
            assert limiter.is_allowed(
                "mock1", "192.168.1.1", burst=5, limit_per_minute=5
            )
        # Client 1 at limit
        assert not limiter.is_allowed(
            "mock1", "192.168.1.1", burst=5, limit_per_minute=5
        )
        # Client 2 should still work (independent tracking)
        for i in range(5):
            assert limiter.is_allowed(
                "mock1", "192.168.1.2", burst=5, limit_per_minute=5
            )
        # Client 2 now at limit
        assert not limiter.is_allowed(
            "mock1", "192.168.1.2", burst=5, limit_per_minute=5
        )

    def test_different_mocks_independent(self):
        """Different mocks should have independent limits."""
        limiter = RateLimiterService()
        for i in range(5):
            assert limiter.is_allowed(
                "mock1", "192.168.1.1", burst=5, limit_per_minute=5
            )
        # Mock1 at limit
        assert not limiter.is_allowed(
            "mock1", "192.168.1.1", burst=5, limit_per_minute=5
        )
        # Mock2 should still work (independent tracking)
        for i in range(5):
            assert limiter.is_allowed(
                "mock2", "192.168.1.1", burst=5, limit_per_minute=5
            )
        # Mock2 now at limit
        assert not limiter.is_allowed(
            "mock2", "192.168.1.1", burst=5, limit_per_minute=5
        )

    def test_unknown_client_ip(self):
        """Requests without client IP should be tracked as 'unknown'."""
        limiter = RateLimiterService()
        for i in range(5):
            assert limiter.is_allowed("mock1", None, burst=5, limit_per_minute=5)
        assert not limiter.is_allowed("mock1", None, burst=5, limit_per_minute=5)


class TestRateLimiterReset:
    """Test reset functionality."""

    def test_reset_specific_client(self):
        """Resetting specific client should clear their limit."""
        limiter = RateLimiterService()
        for i in range(5):
            assert limiter.is_allowed(
                "mock1", "192.168.1.1", burst=5, limit_per_minute=5
            )
        assert not limiter.is_allowed(
            "mock1", "192.168.1.1", burst=5, limit_per_minute=5
        )
        # Reset client
        limiter.reset(mock_id="mock1", client_ip="192.168.1.1")
        assert limiter.is_allowed("mock1", "192.168.1.1", burst=5, limit_per_minute=5)

    def test_reset_mock_all_clients(self):
        """Resetting mock should clear all clients for that mock."""
        limiter = RateLimiterService()
        for i in range(5):
            assert limiter.is_allowed(
                "mock1", "192.168.1.1", burst=5, limit_per_minute=5
            )
            assert limiter.is_allowed(
                "mock1", "192.168.1.2", burst=5, limit_per_minute=5
            )
        # Both clients at limit
        assert not limiter.is_allowed(
            "mock1", "192.168.1.1", burst=5, limit_per_minute=5
        )
        assert not limiter.is_allowed(
            "mock1", "192.168.1.2", burst=5, limit_per_minute=5
        )
        # Reset mock
        limiter.reset(mock_id="mock1")
        assert limiter.is_allowed("mock1", "192.168.1.1", burst=5, limit_per_minute=5)
        assert limiter.is_allowed("mock1", "192.168.1.2", burst=5, limit_per_minute=5)

    def test_reset_all(self):
        """Resetting all should clear everything."""
        limiter = RateLimiterService()
        for i in range(5):
            assert limiter.is_allowed(
                "mock1", "192.168.1.1", burst=5, limit_per_minute=5
            )
            assert limiter.is_allowed(
                "mock2", "192.168.1.2", burst=5, limit_per_minute=5
            )
        # Reset all
        limiter.reset()
        assert limiter.is_allowed("mock1", "192.168.1.1", burst=5, limit_per_minute=5)
        assert limiter.is_allowed("mock2", "192.168.1.2", burst=5, limit_per_minute=5)


class TestRateLimiterWindow:
    """Test time window behavior."""

    def test_requests_outside_window_removed(self):
        """Requests older than 60 seconds should be removed from window."""
        limiter = RateLimiterService()
        # Add some requests
        for i in range(5):
            assert limiter.is_allowed(
                "mock1", "192.168.1.1", burst=10, limit_per_minute=10
            )
        # Simulate time passing by manually manipulating timestamps
        limiter._request_timestamps["mock1:192.168.1.1"] = [time.time() - 70]
        # Should allow new request (old one outside window)
        assert limiter.is_allowed("mock1", "192.168.1.1", burst=10, limit_per_minute=10)

    def test_recent_requests_kept(self):
        """Recent requests should not be removed."""
        limiter = RateLimiterService()
        for i in range(3):
            assert limiter.is_allowed(
                "mock1", "192.168.1.1", burst=5, limit_per_minute=5
            )
        # All requests are recent, 3rd is allowed, 6th is rejected
        for i in range(3, 5):
            assert limiter.is_allowed(
                "mock1", "192.168.1.1", burst=5, limit_per_minute=5
            )
        assert not limiter.is_allowed(
            "mock1", "192.168.1.1", burst=5, limit_per_minute=5
        )
