"""Deterministic local resume analysis utilities."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from backend.core.schema import AnalysisResult, AnalysisResponse


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
_PRESENTATION_PREFIXES = (
    "candidate name:",
    "display name:",
    "name:",
    "pronoun wording:",
    "pronouns:",
    "honorific wording:",
    "honorific:",
    "contact placeholder:",
    "contact:",
    "email:",
    "phone:",
    "location:",
    "biography:",
    "bio:",
)


def _qualification_text(resume_text: str) -> str:
    """Exclude explicitly labelled presentation metadata from local matching."""
    evidence_lines = []
    for line in resume_text.splitlines():
        normalized = line.strip().casefold()
        if normalized.startswith(_PRESENTATION_PREFIXES):
            continue
        evidence_lines.append(line)
    return "\n".join(evidence_lines)


def make_analysis_id(resume_text: str, jd_text: str) -> str:
    digest = hashlib.sha256(f"{resume_text}\0{jd_text}".encode("utf-8")).hexdigest()
    return digest[:16]


def build_mock_analysis(resume_text: str, jd_text: str) -> AnalysisResult:
    resume_lower = _qualification_text(resume_text).casefold()
    jd_lower = jd_text.casefold()
    jd_skills = [skill for skill in SKILL_TERMS if skill in jd_lower]
    matched = [skill for skill in jd_skills if skill in resume_lower]
    missing = [skill for skill in jd_skills if skill not in resume_lower]
    coverage = len(matched) / max(1, len(jd_skills))
    score = round(48 + coverage * 42)

    recommendations = [
        f"Add one quantified resume bullet showing practical {skill} impact."
        for skill in missing[:3]
    ] or [
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
                "The strongest evidence is in the matched skills, while missing skills "
                "need clearer project or work examples before applying."
            ),
            "matched_skills": matched,
            "missing_skills": missing,
            "strengths": [f"Shows direct evidence of {skill}." for skill in matched[:4]],
            "weaknesses": [
                f"Does not yet show concrete evidence of {skill}." for skill in missing[:4]
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
                "How do you validate structured analytical output before rendering it?",
            ],
            "risk_flags": ["Cloud experience may be below the role's preferred level."],
        }
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
