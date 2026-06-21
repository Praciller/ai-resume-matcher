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
    mock_ai_mode: bool
    cache_enabled: bool
    cache_ttl_seconds: int
    timeout_seconds: int
    gemini_max_retries: int
    provider_order: tuple[str, ...]
    ninearm_api_key: str
    ninearm_base_url: str
    ninearm_model: str
    gemini_api_key: str
    gemini_model: str
    gemini_fallback_model: str
    groq_api_key: str
    groq_base_url: str
    groq_model: str
    cerebras_api_key: str
    cerebras_base_url: str
    cerebras_model: str

    @property
    def max_resume_file_mb(self) -> int:
        return self.max_resume_file_bytes // (1024 * 1024)

    def configured_providers(self) -> list[str]:
        keys = {
            "9arm": self.ninearm_api_key,
            "gemini": self.gemini_api_key,
            "groq": self.groq_api_key,
            "cerebras": self.cerebras_api_key,
        }
        return [name for name in self.provider_order if keys.get(name)]


def get_settings() -> Settings:
    max_file_mb = _as_int("MAX_RESUME_FILE_MB", 5, minimum=1)
    provider_order = tuple(
        name.strip().lower()
        for name in os.getenv(
            "AI_PROVIDER_ORDER", "9arm,gemini,groq,cerebras"
        ).split(",")
        if name.strip()
    )
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
        mock_ai_mode=_as_bool("MOCK_AI_MODE", True),
        cache_enabled=_as_bool("ENABLE_AI_ANALYSIS_CACHE", True),
        cache_ttl_seconds=_as_int(
            "AI_ANALYSIS_CACHE_TTL_SECONDS", 86_400, minimum=60
        ),
        timeout_seconds=_as_int("GEMINI_TIMEOUT_SECONDS", 30, minimum=5),
        gemini_max_retries=_as_int("GEMINI_MAX_RETRIES", 1, minimum=0),
        provider_order=provider_order,
        ninearm_api_key=os.getenv("NINEARM_API_KEY", "").strip(),
        ninearm_base_url=os.getenv(
            "NINEARM_BASE_URL", "https://gateway.9arm.co/v1"
        ).rstrip("/"),
        ninearm_model=os.getenv(
            "NINEARM_RESUME_MODEL", "qwen3.6-35b-a3b"
        ),
        gemini_api_key=os.getenv("GEMINI_API_KEY", "").strip(),
        gemini_model=os.getenv(
            "GEMINI_RESUME_MODEL", "gemini-2.5-flash-lite"
        ),
        gemini_fallback_model=os.getenv(
            "GEMINI_RESUME_FALLBACK_MODEL", "gemini-2.5-flash"
        ),
        groq_api_key=os.getenv("GROQ_API_KEY", "").strip(),
        groq_base_url=os.getenv(
            "GROQ_BASE_URL", "https://api.groq.com/openai/v1"
        ).rstrip("/"),
        groq_model=os.getenv(
            "GROQ_RESUME_MODEL", "openai/gpt-oss-20b"
        ),
        cerebras_api_key=os.getenv("CEREBRAS_API_KEY", "").strip(),
        cerebras_base_url=os.getenv(
            "CEREBRAS_BASE_URL", "https://api.cerebras.ai/v1"
        ).rstrip("/"),
        cerebras_model=os.getenv(
            "CEREBRAS_RESUME_MODEL", "gpt-oss-120b"
        ),
    )
