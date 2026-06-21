from __future__ import annotations

from dataclasses import replace

from fastapi.testclient import TestClient

import backend.main as main
from backend.tests.pdf_factory import make_text_pdf


client = TestClient(main.app)


def test_health_endpoint() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_mock_analysis_endpoint() -> None:
    response = client.post("/api/mock-analyze")
    assert response.status_code == 200
    payload = response.json()
    assert payload["model_used"] == "deterministic-sample-v1"
    assert 0 <= payload["match_score"] <= 100


def test_full_mock_pdf_flow(monkeypatch) -> None:
    monkeypatch.setattr(
        main,
        "settings",
        replace(main.settings, mock_ai_mode=True, cache_enabled=False),
    )
    response = client.post(
        "/api/analyze",
        files={
            "resume_file": (
                "resume.pdf",
                make_text_pdf("Python React FastAPI Git"),
                "application/pdf",
            )
        },
        data={
            "job_description": (
                "Senior engineer role requiring Python, React, FastAPI, AWS, "
                "communication, and production delivery."
            )
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["provider_used"] == "mock"
    assert payload["matched_skills"]
    assert payload["analysis_id"]


def test_invalid_pdf_is_rejected() -> None:
    response = client.post(
        "/api/analyze",
        files={"resume_file": ("resume.pdf", b"not pdf", "application/pdf")},
        data={"job_description": "A valid job description with enough detail."},
    )
    assert response.status_code == 422
    assert "valid PDF header" in response.json()["detail"]


def test_empty_job_description_is_rejected() -> None:
    response = client.post(
        "/api/analyze",
        files={
            "resume_file": (
                "resume.pdf",
                make_text_pdf(),
                "application/pdf",
            )
        },
        data={"job_description": ""},
    )
    assert response.status_code == 422
