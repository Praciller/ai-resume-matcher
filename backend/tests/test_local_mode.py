"""Zero-cost local-mode behavior."""

import pytest
from dataclasses import replace

from fastapi.testclient import TestClient

import backend.main as main_module
from backend.core.analysis import (
    AIAnalyzer,
    AnalysisUnavailableError,
    build_mock_analysis,
)
from backend.core.config import get_settings
from backend.tests.pdf_factory import make_text_pdf


def test_clean_environment_defaults_to_mock_mode(monkeypatch) -> None:
    monkeypatch.delenv("MOCK_AI_MODE", raising=False)

    assert get_settings().mock_ai_mode


def test_mock_analysis_is_deterministic_and_explainable() -> None:
    resume = "Python React FastAPI SQL Git communication"
    job = "Seeking Python React FastAPI SQL AWS Docker Git communication skills."

    first = build_mock_analysis(resume, job)
    second = build_mock_analysis(resume, job)

    assert first == second
    assert first.match_score == 80
    assert first.matched_skills == [
        "python",
        "react",
        "fastapi",
        "sql",
        "git",
        "communication",
    ]
    assert first.missing_skills == ["aws", "docker"]


def test_explicit_live_mode_without_keys_fails_before_network(monkeypatch) -> None:
    monkeypatch.setenv("MOCK_AI_MODE", "false")
    for name in (
        "NINEARM_API_KEY",
        "GEMINI_API_KEY",
        "GROQ_API_KEY",
        "CEREBRAS_API_KEY",
    ):
        monkeypatch.setenv(name, "")

    analyzer = AIAnalyzer(get_settings())

    with pytest.raises(AnalysisUnavailableError, match="not configured"):
        analyzer.analyze("Python resume", "Python role description")


def test_mock_api_path_never_calls_external_analyzer(monkeypatch) -> None:
    monkeypatch.setattr(
        main_module,
        "settings",
        replace(main_module.settings, mock_ai_mode=True, cache_enabled=False),
    )
    monkeypatch.setattr(
        main_module.analyzer,
        "analyze",
        lambda *_: pytest.fail("external analyzer was called"),
    )

    response = TestClient(main_module.app).post(
        "/api/analyze",
        files={
            "resume_file": (
                "synthetic-resume.pdf",
                make_text_pdf("Python React FastAPI SQL Git communication"),
                "application/pdf",
            )
        },
        data={
            "job_description": "Seeking Python React FastAPI SQL AWS Docker Git communication skills."
        },
    )

    assert response.status_code == 200
    assert response.json()["provider_used"] == "mock"
