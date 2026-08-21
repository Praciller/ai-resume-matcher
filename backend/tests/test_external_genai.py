"""Generic external GenAI contract and safe fallback behavior."""

from dataclasses import replace

import httpx
import pytest
from fastapi.testclient import TestClient

import backend.main as main
from backend.core.analysis import ProviderResult, sample_analysis
from backend.core.external import ExternalAnalysisClient
from backend.tests.pdf_factory import make_text_pdf


def test_external_client_uses_neutral_contract_and_validates_analysis() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["authorization"] = request.headers.get("Authorization")
        captured["body"] = request.read().decode("utf-8")
        return httpx.Response(
            200,
            json={
                "analysis": sample_analysis().model_dump(),
                "model": "remote-general",
            },
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    result = ExternalAnalysisClient(
        "https://analysis.example/v1/resume-match",
        api_key="server-secret",
        model="general",
        client=client,
    ).analyze("Python FastAPI", "Need Python FastAPI and AWS")

    assert result.provider == "external"
    assert result.model == "remote-general"
    assert result.analysis.match_score == 78
    assert captured["authorization"] == "Bearer server-secret"
    normalized = str(captured["body"]).replace(" ", "")
    assert '"task":"resume_job_match"' in normalized
    assert '"response_format":"analysis_result_v1"' in normalized


def test_external_client_rejects_low_quality_output() -> None:
    low_quality = sample_analysis().model_dump()
    low_quality["summary"] = "Too short"
    client = httpx.Client(
        transport=httpx.MockTransport(
            lambda _: httpx.Response(200, json={"analysis": low_quality})
        )
    )

    with pytest.raises(ValueError, match="quality gate"):
        ExternalAnalysisClient(
            "https://analysis.example/v1/resume-match", client=client
        ).analyze("resume", "job")


def test_api_falls_back_to_local_when_external_route_fails(monkeypatch) -> None:
    class FailingExternalClient:
        def __init__(self, **_: object) -> None:
            pass

        def analyze(self, resume_text: str, job_description: str) -> ProviderResult:
            raise httpx.ConnectError("unavailable")

    monkeypatch.setattr(main, "ExternalAnalysisClient", FailingExternalClient)
    monkeypatch.setattr(
        main,
        "settings",
        replace(
            main.settings,
            cache_enabled=False,
            enable_external_genai=True,
            external_genai_url="https://analysis.example/v1/resume-match",
        ),
    )

    response = TestClient(main.app).post(
        "/api/analyze",
        files={
            "resume_file": (
                "resume.pdf",
                make_text_pdf("Python React FastAPI Git"),
                "application/pdf",
            )
        },
        data={"job_description": "Need Python React FastAPI AWS communication."},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["provider_used"] == "local"
    assert payload["model_used"] == "deterministic-local-v1"
    assert any("External GenAI" in warning for warning in payload["warnings"])


def test_api_uses_valid_external_result_when_explicitly_enabled(monkeypatch) -> None:
    class SuccessfulExternalClient:
        def __init__(self, **_: object) -> None:
            pass

        def analyze(self, resume_text: str, job_description: str) -> ProviderResult:
            return ProviderResult(sample_analysis(), "external", "remote-general")

    monkeypatch.setattr(main, "ExternalAnalysisClient", SuccessfulExternalClient)
    monkeypatch.setattr(
        main,
        "settings",
        replace(
            main.settings,
            cache_enabled=False,
            enable_external_genai=True,
            external_genai_url="https://analysis.example/v1/resume-match",
        ),
    )

    response = TestClient(main.app).post(
        "/api/analyze",
        files={
            "resume_file": (
                "resume.pdf",
                make_text_pdf("Python React FastAPI Git"),
                "application/pdf",
            )
        },
        data={"job_description": "Need Python React FastAPI AWS communication."},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["provider_used"] == "external"
    assert payload["model_used"] == "remote-general"
