"""Portfolio evidence and repository-safety checks."""

from pathlib import Path

import scripts.check_repo_guardrails as guardrails
from scripts.generate_local_match_report import DEFAULT_JOB, DEFAULT_RESUME, render_report


def test_synthetic_report_has_stable_evidence_and_safety_disclaimer() -> None:
    report = render_report(DEFAULT_RESUME, DEFAULT_JOB)

    assert "Match score | 69/100" in report
    assert "Recognized requirement coverage | 50% (6/12)" in report
    assert "Matched criteria | python, javascript, react, sql, git, communication" in report
    assert "Missing criteria | node.js, aws, azure, docker, kubernetes, machine learning" in report
    assert "not a probability" in report
    assert "not fairness or\ncompliance audited" in report


def test_guardrails_reject_private_resume_and_secret(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(guardrails, "ROOT", tmp_path)
    resume = tmp_path / "uploads/private-resume.pdf"
    secret = tmp_path / ".env.example"
    resume.parent.mkdir()
    resume.write_bytes(b"%PDF-private")
    secret.write_text("EXAMPLE_" + "API_KEY=real-secret", encoding="utf-8")

    failures = guardrails.violations([resume, secret])

    assert failures == [
        "unsafe tracked artifact: uploads/private-resume.pdf",
        "possible credential assignment: .env.example",
    ]
