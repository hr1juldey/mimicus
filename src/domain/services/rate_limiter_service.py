"""Rate limiting service for mock responses."""

import time
from typing import Dict, List, Optional
from collections import defaultdict


class RateLimiterService:
    """In-memory rate limiter tracking requests by mock_id + client_ip."""

    def __init__(self):
        """Initialize rate limiter with empty tracking."""
        self._request_timestamps: Dict[str, List[float]] = defaultdict(list)

    def _get_key(self, mock_id: str, client_ip: Optional[str]) -> str:
        """Generate tracking key from mock_id and client_ip."""
        ip = client_ip or "unknown"
        return f"{mock_id}:{ip}"

    def is_allowed(
        self,
        mock_id: str,
        client_ip: Optional[str],
        limit_per_minute: int = 60,
        burst: int = 10,
    ) -> bool:
        """Check if request is allowed under rate limit."""
        key = self._get_key(mock_id, client_ip)
        now = time.time()
        cutoff = now - 60  # 1 minute window

        # Remove old timestamps outside the window
        self._request_timestamps[key] = [
            ts for ts in self._request_timestamps[key] if ts > cutoff
        ]

        # Check burst limit (allow immediate burst of N requests)
        if len(self._request_timestamps[key]) < burst:
            self._request_timestamps[key].append(now)
            return True

        # Check per-minute limit
        if len(self._request_timestamps[key]) < limit_per_minute:
            self._request_timestamps[key].append(now)
            return True

        return False

    def reset(self, mock_id: Optional[str] = None, client_ip: Optional[str] = None):
        """Reset rate limit tracking."""
        if mock_id and client_ip:
            key = self._get_key(mock_id, client_ip)
            if key in self._request_timestamps:
                del self._request_timestamps[key]
        elif mock_id:
            # Reset all entries for this mock_id
            keys_to_delete = [
                k for k in self._request_timestamps if k.startswith(f"{mock_id}:")
            ]
            for k in keys_to_delete:
                del self._request_timestamps[k]
        else:
            # Reset all
            self._request_timestamps.clear()
