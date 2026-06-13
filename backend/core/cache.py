"""Small in-memory TTL cache for repeat analyses."""

from __future__ import annotations

import time
from dataclasses import dataclass

from backend.core.schema import AnalysisResult


@dataclass
class CacheEntry:
    expires_at: float
    result: AnalysisResult
    provider: str
    model: str


class AnalysisCache:
    def __init__(self) -> None:
        self._entries: dict[str, CacheEntry] = {}

    def get(self, key: str) -> CacheEntry | None:
        entry = self._entries.get(key)
        if not entry:
            return None
        if entry.expires_at <= time.time():
            self._entries.pop(key, None)
            return None
        return entry

    def set(
        self,
        key: str,
        result: AnalysisResult,
        provider: str,
        model: str,
        ttl_seconds: int,
    ) -> None:
        self._entries[key] = CacheEntry(
            expires_at=time.time() + ttl_seconds,
            result=result,
            provider=provider,
            model=model,
        )
