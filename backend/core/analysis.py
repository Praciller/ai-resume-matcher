"""AI provider routing and deterministic mock analysis."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any

import httpx
from pydantic import ValidationError

from backend.core.config import Settings
from backend.core.schema import AnalysisResult, AnalysisResponse


class AnalysisUnavailableError(RuntimeError):
    """All configured providers failed validation or transport."""


@dataclass(frozen=True)
class ProviderResult:
    analysis: AnalysisResult
    provider: str
    model: str


SKILL_TERMS = (
    "python",
    "javascript",
    "typescript",
    "react",
    "node.js",
    "fastapi",
    "sql",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "git",
    "machine learning",
    "data analysis",
    "communication",
    "leadership",
    "project management",
)


def provider_json_schema() -> dict[str, Any]:
    unsupported = {"default", "examples", "maxLength", "minLength", "title"}

    def clean(value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: clean(item)
                for key, item in value.items()
                if key not in unsupported
            }
        if isinstance(value, list):
            return [clean(item) for item in value]
        return value

    return clean(AnalysisResult.model_json_schema())


def make_analysis_id(resume_text: str, jd_text: str) -> str:
    digest = hashlib.sha256(f"{resume_text}\0{jd_text}".encode("utf-8")).hexdigest()
    return digest[:16]


def build_mock_analysis(resume_text: str, jd_text: str) -> AnalysisResult:
    resume_lower = resume_text.casefold()
    jd_lower = jd_text.casefold()
    jd_skills = [skill for skill in SKILL_TERMS if skill in jd_lower]
    matched = [skill for skill in jd_skills if skill in resume_lower]
    missing = [skill for skill in jd_skills if skill not in resume_lower]
    coverage = len(matched) / max(1, len(jd_skills))
    score = round(48 + coverage * 42)
    recommendations = [
        f"Add one quantified resume bullet showing practical {skill} impact."
        for skill in missing[:3]
    ]
    if not recommendations:
        recommendations = [
            "Tailor the opening summary with two measurable outcomes relevant to this role."
        ]

    learning_plan = [
        {
            "priority": "high" if index == 0 else "medium",
            "skill": skill,
            "reason": f"The job description mentions {skill}, but the resume does not show direct evidence.",
            "suggested_action": f"Complete a focused {skill} project and add a quantified result to the resume.",
        }
        for index, skill in enumerate(missing[:3])
    ]

    return AnalysisResult.model_validate(
        {
            "match_score": score,
            "summary": (
                "The resume shows a credible foundation for this role. "
                "The strongest evidence is in the matched skills, while the missing "
                "skills need clearer project or work examples before applying."
            ),
            "matched_skills": matched,
            "missing_skills": missing,
            "strengths": [
                f"Shows direct evidence of {skill}." for skill in matched[:4]
            ],
            "weaknesses": [
                f"Does not yet show concrete evidence of {skill}."
                for skill in missing[:4]
            ],
            "recommendations": recommendations,
            "learning_plan": learning_plan,
            "interview_questions": [
                "Which project best demonstrates your impact on a role requirement?",
                "How do you prioritize learning when a job requires an unfamiliar skill?",
                "What measurable result are you most prepared to discuss?",
            ],
            "risk_flags": (
                ["The job description has few recognizable skill keywords."]
                if not jd_skills
                else []
            ),
        }
    )


def sample_analysis() -> AnalysisResult:
    return AnalysisResult.model_validate(
        {
            "match_score": 78,
            "summary": (
                "The candidate aligns well with the frontend and API requirements. "
                "Production cloud experience is the main gap to address before interviews."
            ),
            "matched_skills": ["React", "JavaScript", "Python", "FastAPI", "Git"],
            "missing_skills": ["AWS", "Kubernetes"],
            "strengths": [
                "Built user-facing React applications.",
                "Connected Python APIs to production interfaces.",
                "Shows practical testing and version-control experience.",
            ],
            "weaknesses": [
                "Cloud deployment impact is not quantified.",
                "No Kubernetes evidence appears in the resume.",
            ],
            "recommendations": [
                "Add a deployment bullet with latency, reliability, or usage metrics.",
                "Build a small AWS-hosted project and document the architecture.",
                "Prepare one story connecting product decisions to measurable outcomes.",
            ],
            "learning_plan": [
                {
                    "priority": "high",
                    "skill": "AWS",
                    "reason": "Cloud deployment is a core requirement in the job description.",
                    "suggested_action": "Deploy a FastAPI service on AWS and document cost, monitoring, and rollback steps.",
                },
                {
                    "priority": "medium",
                    "skill": "Kubernetes",
                    "reason": "The role expects container orchestration familiarity.",
                    "suggested_action": "Package the app with Docker and deploy it to a local Kubernetes cluster.",
                },
            ],
            "interview_questions": [
                "How would you design and deploy a reliable resume-analysis API?",
                "Describe a production issue you diagnosed across frontend and backend.",
                "How do you validate structured LLM output before rendering it?",
            ],
            "risk_flags": [
                "Cloud experience may be below the role's preferred level."
            ],
        }
    )


class AIAnalyzer:
    def __init__(
        self,
        settings: Settings,
        client: httpx.Client | None = None,
    ) -> None:
        self.settings = settings
        self.client = client or httpx.Client(
            timeout=httpx.Timeout(settings.timeout_seconds)
        )

    def analyze(self, resume_text: str, jd_text: str) -> ProviderResult:
        for provider in self.settings.provider_order:
            if provider == "9arm" and self.settings.ninearm_api_key:
                result = self._attempt_openai_provider(
                    provider="9arm",
                    base_url=self.settings.ninearm_base_url,
                    api_key=self.settings.ninearm_api_key,
                    model=self.settings.ninearm_model,
                    resume_text=resume_text,
                    jd_text=jd_text,
                    strict=False,
                )
                if result:
                    return result
            elif provider == "gemini" and self.settings.gemini_api_key:
                models = [self.settings.gemini_model]
                if self.settings.gemini_max_retries > 0:
                    models.append(self.settings.gemini_fallback_model)
                for model in dict.fromkeys(models):
                    result = self._attempt_gemini(
                        model=model,
                        resume_text=resume_text,
                        jd_text=jd_text,
                    )
                    if result:
                        return result
            elif provider == "groq" and self.settings.groq_api_key:
                result = self._attempt_openai_provider(
                    provider="groq",
                    base_url=self.settings.groq_base_url,
                    api_key=self.settings.groq_api_key,
                    model=self.settings.groq_model,
                    resume_text=resume_text,
                    jd_text=jd_text,
                    strict=True,
                )
                if result:
                    return result
            elif provider == "cerebras" and self.settings.cerebras_api_key:
                result = self._attempt_openai_provider(
                    provider="cerebras",
                    base_url=self.settings.cerebras_base_url,
                    api_key=self.settings.cerebras_api_key,
                    model=self.settings.cerebras_model,
                    resume_text=resume_text,
                    jd_text=jd_text,
                    strict=True,
                )
                if result:
                    return result

        if not self.settings.configured_providers():
            raise AnalysisUnavailableError(
                "AI analysis is not configured. Enable mock mode or add a server-side provider key."
            )
        raise AnalysisUnavailableError(
            "AI analysis is temporarily unavailable. Retry once or use sample mode."
        )

    def _attempt_openai_provider(
        self,
        provider: str,
        base_url: str,
        api_key: str,
        model: str,
        resume_text: str,
        jd_text: str,
        strict: bool,
    ) -> ProviderResult | None:
        payload: dict[str, Any] = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an evidence-based resume matcher. "
                        "Return only JSON. Never invent experience or use harsh judgments."
                    ),
                },
                {
                    "role": "user",
                    "content": self._prompt(resume_text, jd_text),
                },
            ],
            "temperature": 0.1,
        }
        if strict:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "resume_match_analysis",
                    "strict": True,
                    "schema": provider_json_schema(),
                },
            }

        try:
            response = self.client.post(
                f"{base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            analysis = self._validate_content(content)
            if analysis.is_low_quality():
                return None
            return ProviderResult(analysis, provider, model)
        except (
            httpx.HTTPError,
            KeyError,
            TypeError,
            ValueError,
            json.JSONDecodeError,
            ValidationError,
        ):
            return None

    def _attempt_gemini(
        self,
        model: str,
        resume_text: str,
        jd_text: str,
    ) -> ProviderResult | None:
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": self._prompt(resume_text, jd_text)}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "responseMimeType": "application/json",
                "responseJsonSchema": provider_json_schema(),
            },
        }
        try:
            response = self.client.post(
                (
                    "https://generativelanguage.googleapis.com/v1beta/models/"
                    f"{model}:generateContent"
                ),
                headers={
                    "x-goog-api-key": self.settings.gemini_api_key,
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            content = response.json()["candidates"][0]["content"]["parts"][0][
                "text"
            ]
            analysis = self._validate_content(content)
            if analysis.is_low_quality():
                return None
            return ProviderResult(analysis, "gemini", model)
        except (
            httpx.HTTPError,
            KeyError,
            TypeError,
            ValueError,
            json.JSONDecodeError,
            ValidationError,
        ):
            return None

    @staticmethod
    def _validate_content(content: str) -> AnalysisResult:
        cleaned = content.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("Provider did not return a JSON object.")
        return AnalysisResult.model_validate_json(cleaned[start : end + 1])

    @staticmethod
    def _prompt(resume_text: str, jd_text: str) -> str:
        schema = json.dumps(provider_json_schema(), separators=(",", ":"))
        return (
            "Compare the resume with the job description using only supplied evidence. "
            "Score 0-100. Keep arrays present even when empty. Deduplicate skills. "
            "Recommendations must start with concrete actions. Risk flags must be neutral "
            "warnings, not hiring verdicts. Return exactly one JSON object matching this schema:\n"
            f"{schema}\n\nRESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{jd_text}"
        )


def to_response(
    result: ProviderResult,
    analysis_id: str,
    cached: bool,
    warnings: list[str],
) -> AnalysisResponse:
    return AnalysisResponse.model_validate(
        {
            **result.analysis.model_dump(),
            "model_used": result.model,
            "provider_used": result.provider,
            "cached": cached,
            "analysis_id": analysis_id,
            "warnings": warnings,
        }
    )
