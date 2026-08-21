"""Vendor-neutral external GenAI adapter for structured resume analysis."""

from __future__ import annotations

from typing import Any

import httpx

from backend.core.analysis import ProviderResult
from backend.core.schema import AnalysisResult


class ExternalAnalysisClient:
    def __init__(
        self,
        endpoint: str,
        api_key: str = "",
        model: str = "general",
        timeout_seconds: int = 30,
        client: httpx.Client | None = None,
    ) -> None:
        endpoint = endpoint.strip()
        if not endpoint:
            raise ValueError("External GenAI endpoint is required")
        self.endpoint = endpoint
        self.api_key = api_key.strip()
        self.model = model.strip() or "general"
        self._client = client or httpx.Client(timeout=timeout_seconds)

    def analyze(self, resume_text: str, job_description: str) -> ProviderResult:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        response = self._client.post(
            self.endpoint,
            headers=headers,
            json={
                "task": "resume_job_match",
                "resume_text": resume_text,
                "job_description": job_description,
                "model": self.model,
                "response_format": "analysis_result_v1",
            },
        )
        response.raise_for_status()
        payload: Any = response.json()
        if not isinstance(payload, dict):
            raise ValueError("External GenAI response must be a JSON object")

        analysis_payload = payload.get("analysis")
        if not isinstance(analysis_payload, dict):
            raise ValueError("External GenAI response must contain an analysis object")
        analysis = AnalysisResult.model_validate(analysis_payload)
        if analysis.is_low_quality():
            raise ValueError("External GenAI response did not meet the analysis quality gate")

        model = payload.get("model")
        if not isinstance(model, str) or not model.strip():
            model = self.model
        return ProviderResult(analysis=analysis, provider="external", model=model)
