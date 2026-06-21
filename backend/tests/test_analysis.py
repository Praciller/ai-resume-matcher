from __future__ import annotations

import json
from dataclasses import replace

import httpx

from backend.core.analysis import AIAnalyzer, build_mock_analysis
from backend.core.config import get_settings
from backend.tests.test_schema import valid_payload


def test_mock_analysis_is_deterministic() -> None:
    first = build_mock_analysis(
        "Python React developer", "Need Python React AWS engineer"
    )
    second = build_mock_analysis(
        "Python React developer", "Need Python React AWS engineer"
    )
    assert first == second
    assert first.matched_skills == ["python", "react"]
    assert first.missing_skills == ["aws"]


def test_invalid_primary_falls_back_to_gemini() -> None:
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(str(request.url))
        if "gateway.9arm.co" in str(request.url):
            return httpx.Response(
                200,
                json={"choices": [{"message": {"content": "not json"}}]},
            )
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {
                        "content": {
                            "parts": [{"text": json.dumps(valid_payload())}]
                        }
                    }
                ]
            },
        )

    settings = replace(
        get_settings(),
        provider_order=("9arm", "gemini"),
        ninearm_api_key="test-ninearm",
        gemini_api_key="test-gemini",
        gemini_max_retries=1,
    )
    client = httpx.Client(transport=httpx.MockTransport(handler))
    result = AIAnalyzer(settings, client=client).analyze(
        "Python React delivery evidence",
        "Senior engineer role requiring Python and React",
    )

    assert result.provider == "gemini"
    assert result.model == settings.gemini_model
    assert len(calls) == 2


def test_invalid_gemini_primary_uses_fallback_model() -> None:
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(str(request.url))
        if "flash-lite" in str(request.url):
            return httpx.Response(500, json={"error": "temporary"})
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {
                        "content": {
                            "parts": [{"text": json.dumps(valid_payload())}]
                        }
                    }
                ]
            },
        )

    settings = replace(
        get_settings(),
        provider_order=("gemini",),
        gemini_api_key="test-gemini",
        gemini_model="gemini-2.5-flash-lite",
        gemini_fallback_model="gemini-2.5-flash",
        gemini_max_retries=1,
    )
    client = httpx.Client(transport=httpx.MockTransport(handler))
    result = AIAnalyzer(settings, client=client).analyze(
        "Python React delivery evidence",
        "Senior engineer role requiring Python and React",
    )

    assert result.model == "gemini-2.5-flash"
    assert len(calls) == 2
