"""Score-provenance and evidence-traceability tests for local matching."""

from __future__ import annotations

from backend.core.analysis import build_mock_analysis

JD = """
Requirements: Python, React, SQL, Kubernetes, and project management experience.
"""

RESUME = """
Candidate name: Test Candidate
Experienced engineer with Python and React delivery.
Comfortable writing SQL queries and migrations.
Familiar with K8s clusters from a platform team.
Led delivery work with light project management duties.
"""


def test_every_evidence_quote_appears_in_resume() -> None:
    result = build_mock_analysis(RESUME, JD)
    assert result.skill_evidence, "expected skill evidence entries"
    folded_resume = RESUME.casefold()
    for evidence in result.skill_evidence:
        quote = evidence.evidence_quote.casefold()
        assert quote in folded_resume, (
            f"Evidence for {evidence.skill} is not traceable to resume text"
        )


def test_alias_counts_as_evidence_but_not_score() -> None:
    result = build_mock_analysis(RESUME, JD)
    assert "kubernetes" not in result.matched_skills
    partial_skills = {
        evidence.skill for evidence in result.skill_evidence
        if evidence.status == "partial"
    }
    assert "kubernetes" in partial_skills
    assert result.score_breakdown is not None
    assert result.score_breakdown.partial_count >= 1
    assert result.score_breakdown.matched_count == len(result.matched_skills)


def test_score_breakdown_matches_reported_skills() -> None:
    result = build_mock_analysis(RESUME, JD)
    breakdown = result.score_breakdown
    assert breakdown is not None
    assert breakdown.matched_count == len(result.matched_skills)
    assert breakdown.missing_count == len(result.missing_skills)
    assert (
        breakdown.matched_count + breakdown.partial_count + breakdown.missing_count
        == breakdown.skills_considered
    )
    expected = round(48 + breakdown.matched_count / breakdown.skills_considered * 42)
    assert result.match_score == expected


def test_short_alias_does_not_match_inside_words() -> None:
    resume = "Configured JSON exports and managed node processes."
    result = build_mock_analysis(resume, "Requirements: JavaScript, Node.js")
    assert "javascript" not in result.matched_skills
    assert "node.js" not in result.matched_skills
    assert not any(
        evidence.skill in ("javascript", "node.js")
        for evidence in result.skill_evidence
    )


def test_local_analysis_includes_limitations() -> None:
    result = build_mock_analysis(RESUME, JD)
    assert result.limitations
    assert any("coverage heuristic" in item for item in result.limitations)
    assert all(len(item) > 20 for item in result.limitations)
