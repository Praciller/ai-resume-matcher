"""Deterministic local-mode behavior."""

from dataclasses import replace

from fastapi.testclient import TestClient

import backend.main as main_module
from backend.core.analysis import build_mock_analysis
from backend.core.config import get_settings
from backend.tests.pdf_factory import make_text_pdf


def test_clean_environment_uses_local_configuration() -> None:
    settings = get_settings()
    assert settings.configured_providers() == []
    assert settings.max_resume_file_mb >= 1


def test_local_analysis_is_deterministic_and_explainable() -> None:
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


def test_api_path_returns_local_result_without_external_configuration(monkeypatch) -> None:
    monkeypatch.setattr(
        main_module,
        "settings",
        replace(main_module.settings, cache_enabled=False),
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
    assert response.json()["provider_used"] == "local"
    assert response.json()["model_used"] == "deterministic-local-v1"
