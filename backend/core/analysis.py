"""Deterministic local resume analysis utilities."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from backend.core.schema import AnalysisResult, AnalysisResponse, ScoreBreakdown, SkillEvidence


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

# Aliases are matched with word boundaries so short forms such as "js"
# cannot match inside unrelated words like "json". English-word or
# collision-prone forms ("node", "pm") are intentionally excluded.
_SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "javascript": ("js", "ecmascript"),
    "typescript": ("ts",),
    "node.js": ("nodejs",),
    "kubernetes": ("k8s",),
    "machine learning": ("ml",),
    "data analysis": ("analytics",),
}

_ALIAS_PATTERNS: dict[str, re.Pattern[str]] = {
    skill: re.compile(rf"(?<![a-z0-9])({'|'.join(re.escape(a) for a in aliases)})(?![a-z0-9])")
    for skill, aliases in _SKILL_ALIASES.items()
}

_EVIDENCE_MAX_CHARS = 200

_ANALYSIS_LIMITATIONS = (
    "Keyword-based matching cannot verify the depth, recency, or quality of experience.",
    "Skills are detected by literal text or a fixed alias table; other synonyms are missed.",
    "Scanned or image-only resumes cannot be analyzed.",
    "The match score is a coverage heuristic, not a prediction of job performance.",
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


def _has_alias(text: str, skill: str) -> bool:
    pattern = _ALIAS_PATTERNS.get(skill)
    return bool(pattern and pattern.search(text))


def _extract_evidence(resume_lines: list[str], resume_lower: str, skill: str) -> str | None:
    """Return the first resume line that literally evidences the skill."""
    for line in resume_lines:
        line_lower = line.casefold()
        if skill in line_lower or _has_alias(line_lower, skill):
            quote = " ".join(line.split())
            return quote[:_EVIDENCE_MAX_CHARS]
    if skill in resume_lower or _has_alias(resume_lower, skill):
        return resume_lower[:_EVIDENCE_MAX_CHARS]
    return None


def build_mock_analysis(resume_text: str, jd_text: str) -> AnalysisResult:
    qualification = _qualification_text(resume_text)
    resume_lines = [line for line in qualification.splitlines() if line.strip()]
    resume_lower = qualification.casefold()
    jd_lower = jd_text.casefold()
    jd_skills = [skill for skill in SKILL_TERMS if skill in jd_lower]
    matched = []
    partial = []
    missing = []
    for skill in jd_skills:
        if skill in resume_lower:
            matched.append(skill)
        elif _has_alias(resume_lower, skill):
            partial.append(skill)
        else:
            missing.append(skill)
    coverage = len(matched) / max(1, len(jd_skills))
    score = round(48 + coverage * 42)

    skill_evidence = []
    for skill, status in [(s, "matched") for s in matched] + [
        (s, "partial") for s in partial
    ]:
        quote = _extract_evidence(resume_lines, resume_lower, skill)
        if quote:
            skill_evidence.append(
                SkillEvidence(
                    skill=skill,
                    status=status,
                    source="resume",
                    evidence_quote=quote,
                )
            )

    score_breakdown = ScoreBreakdown(
        skills_considered=len(jd_skills),
        matched_count=len(matched),
        partial_count=len(partial),
        missing_count=len(missing),
        coverage=round(coverage, 4),
        formula="round(48 + matched/considered * 42); aliases are evidence only, not score",
    )

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
            ]
            + [
                f"Only indirect alias evidence of {skill} was found."
                for skill in partial[:2]
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
            "skill_evidence": [
                evidence.model_dump() for evidence in skill_evidence
            ],
            "score_breakdown": score_breakdown.model_dump(),
            "limitations": list(_ANALYSIS_LIMITATIONS),
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
            "skill_evidence": [
                {
                    "skill": "React",
                    "status": "matched",
                    "source": "resume",
                    "evidence_quote": "Built user-facing React applications.",
                },
                {
                    "skill": "Python",
                    "status": "matched",
                    "source": "resume",
                    "evidence_quote": "Connected Python APIs to production interfaces.",
                },
            ],
            "score_breakdown": {
                "skills_considered": 7,
                "matched_count": 5,
                "partial_count": 0,
                "missing_count": 2,
                "coverage": 0.7143,
                "formula": "round(48 + matched/considered * 42); aliases are evidence only, not score",
            },
            "limitations": list(_ANALYSIS_LIMITATIONS),
        }
    )


def to_response(
    result: ProviderResult,
    analysis_id: str,
    cached: bool,
    warnings: list[str],
    latency_ms: int | None = None,
) -> AnalysisResponse:
    return AnalysisResponse.model_validate(
        {
            **result.analysis.model_dump(),
            "model_used": result.model,
            "provider_used": result.provider,
            "cached": cached,
            "analysis_id": analysis_id,
            "warnings": warnings,
            "latency_ms": latency_ms,
        }
    )
