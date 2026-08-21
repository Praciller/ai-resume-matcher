"""Environment-backed application settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env", override=False)
load_dotenv(ROOT_DIR / "backend" / ".env", override=False)


def _as_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_int(name: str, default: int, minimum: int = 0) -> int:
    try:
        return max(minimum, int(os.getenv(name, str(default))))
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    app_env: str
    frontend_origins: tuple[str, ...]
    max_resume_file_bytes: int
    max_resume_chars: int
    max_jd_chars: int
    cache_enabled: bool
    cache_ttl_seconds: int

    @property
    def max_resume_file_mb(self) -> int:
        return self.max_resume_file_bytes // (1024 * 1024)

    def configured_providers(self) -> list[str]:
        return []


def get_settings() -> Settings:
    max_file_mb = _as_int("MAX_RESUME_FILE_MB", 5, minimum=1)
    origins = tuple(
        origin.strip()
        for origin in os.getenv(
            "FRONTEND_ORIGIN", "http://localhost:3000,http://localhost:5173"
        ).split(",")
        if origin.strip()
    )
    return Settings(
        app_env=os.getenv("APP_ENV", "development"),
        frontend_origins=origins,
        max_resume_file_bytes=max_file_mb * 1024 * 1024,
        max_resume_chars=_as_int("MAX_RESUME_CHARS", 20_000, minimum=1_000),
        max_jd_chars=_as_int("MAX_JD_CHARS", 20_000, minimum=1_000),
        cache_enabled=_as_bool("ENABLE_AI_ANALYSIS_CACHE", True),
        cache_ttl_seconds=_as_int(
            "AI_ANALYSIS_CACHE_TTL_SECONDS", 86_400, minimum=60
        ),
    )
