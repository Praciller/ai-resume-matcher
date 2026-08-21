"""Validated API and analysis response contracts."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _clean_unique(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        cleaned = " ".join(str(value).split()).strip()
        key = cleaned.casefold()
        if cleaned and key not in seen:
            seen.add(key)
            result.append(cleaned)
    return result


class LearningPlanItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    priority: Literal["high", "medium", "low"]
    skill: str = Field(min_length=1, max_length=120)
    reason: str = Field(min_length=1, max_length=500)
    suggested_action: str = Field(min_length=1, max_length=500)

    @field_validator("skill", "reason", "suggested_action")
    @classmethod
    def clean_text(cls, value: str) -> str:
        return " ".join(value.split()).strip()


class AnalysisResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    match_score: int = Field(ge=0, le=100)
    summary: str = Field(min_length=1, max_length=2_000)
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
    learning_plan: list[LearningPlanItem]
    interview_questions: list[str]
    risk_flags: list[str]

    @field_validator("summary")
    @classmethod
    def clean_summary(cls, value: str) -> str:
        return " ".join(value.split()).strip()

    @field_validator(
        "matched_skills",
        "missing_skills",
        "strengths",
        "weaknesses",
        "recommendations",
        "interview_questions",
        "risk_flags",
    )
    @classmethod
    def clean_lists(cls, values: list[str]) -> list[str]:
        return _clean_unique(values)

    def is_low_quality(self) -> bool:
        return (
            len(self.summary) < 40
            or not self.recommendations
            or not (self.matched_skills or self.missing_skills)
            or any(len(item) < 12 for item in self.recommendations)
        )


class AnalysisResponse(AnalysisResult):
    model_used: str
    provider_used: str
    cached: bool
    analysis_id: str
    warnings: list[str]


class HealthResponse(BaseModel):
    status: Literal["healthy"]
    mode: Literal["local"]
    configured_providers: list[str]
    primary_provider: str | None
    max_resume_file_mb: int
    max_resume_chars: int
    max_jd_chars: int
