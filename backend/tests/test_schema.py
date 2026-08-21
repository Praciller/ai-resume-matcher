from __future__ import annotations

import pytest
from pydantic import ValidationError

from backend.core.schema import AnalysisResult


def valid_payload() -> dict:
    return {
        "match_score": 82,
        "summary": "The resume aligns with the core role requirements and shows useful delivery evidence.",
        "matched_skills": ["Python", "python", "React"],
        "missing_skills": ["AWS"],
        "strengths": ["API delivery"],
        "weaknesses": ["Cloud evidence is limited"],
        "recommendations": ["Add a quantified AWS deployment project to the resume."],
        "learning_plan": [
            {
                "priority": "high",
                "skill": "AWS",
                "reason": "The role requires cloud deployment experience.",
                "suggested_action": "Deploy one API and document reliability metrics.",
            }
        ],
        "interview_questions": ["How did you validate your API in production?"],
        "risk_flags": ["Cloud experience is not explicit."],
    }


def test_schema_deduplicates_skills_case_insensitively() -> None:
    result = AnalysisResult.model_validate(valid_payload())
    assert result.matched_skills == ["Python", "React"]


def test_schema_rejects_score_outside_range() -> None:
    payload = valid_payload()
    payload["match_score"] = 101
    with pytest.raises(ValidationError):
        AnalysisResult.model_validate(payload)


def test_schema_requires_all_arrays() -> None:
    payload = valid_payload()
    payload.pop("risk_flags")
    with pytest.raises(ValidationError):
        AnalysisResult.model_validate(payload)
