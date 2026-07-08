"""Hourglass Pipeline cache: the Storm gets ahead while the topic is framed.

See docs/protocol.md, Branch C. `invalidate()` is the Kill & Fork primitive:
when the Framing Sentinel (V1) detects an explicit pivot, it invalidates the
stale cache entry so a fresh Storm run replaces it.
"""

import json
import threading
from datetime import UTC, datetime, timedelta
from pathlib import Path


class StormCache:
    """TTL cache for in-flight and completed Storm results, persisted to disk."""

    def __init__(self, cache_dir: Path = Path(".storm_cache")):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._data: dict[str, dict] = {}

    def set(self, key: str, value: dict, ttl_seconds: int = 3600) -> None:
        with self._lock:
            self._data[key] = {
                "value": value,
                "expires_at": (
                    datetime.now(UTC) + timedelta(seconds=ttl_seconds)
                ).isoformat(),
            }
            self._persist()

    def get(self, key: str) -> dict | None:
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                return None
            if datetime.now(UTC) < datetime.fromisoformat(entry["expires_at"]):
                return entry["value"]
            del self._data[key]
            self._persist()
            return None

    def invalidate(self, key: str) -> None:
        """Kill & Fork primitive: drop a stale entry on an explicit pivot."""
        with self._lock:
            if key in self._data:
                del self._data[key]
                self._persist()

    def load(self) -> None:
        cache_file = self.cache_dir / "cache.json"
        if cache_file.exists():
            with open(cache_file, encoding="utf-8") as f:
                self._data = json.load(f)

    def _persist(self) -> None:
        cache_file = self.cache_dir / "cache.json"
        tmp_file = cache_file.with_suffix(".tmp")
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)
        tmp_file.replace(cache_file)  # atomic on POSIX
