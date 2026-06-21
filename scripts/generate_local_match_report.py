"""Generate deterministic matching evidence from synthetic text fixtures."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.core.analysis import build_mock_analysis  # noqa: E402


DEFAULT_RESUME = ROOT / "backend/dataset/synthetic_resume.txt"
DEFAULT_JOB = ROOT / "backend/dataset/sample_job_description.txt"
DEFAULT_OUTPUT = ROOT / "reports/local_match_report.md"


def render_report(resume_path: Path, job_path: Path) -> str:
    result = build_mock_analysis(
        resume_path.read_text(encoding="utf-8"),
        job_path.read_text(encoding="utf-8"),
    )
    matched = ", ".join(result.matched_skills) or "None recognized"
    missing = ", ".join(result.missing_skills) or "None recognized"
    recognized = len(result.matched_skills) + len(result.missing_skills)
    coverage = round(100 * len(result.matched_skills) / max(1, recognized))
    recommendations = "\n".join(f"- {item}" for item in result.recommendations)
    return f"""# Local Match Report

Both inputs are synthetic portfolio fixtures.

| Field | Result |
| --- | --- |
| Resume | `{resume_path.relative_to(ROOT).as_posix()}` |
| Job description | `{job_path.relative_to(ROOT).as_posix()}` |
| Match score | {result.match_score}/100 |
| Recognized requirement coverage | {coverage}% ({len(result.matched_skills)}/{recognized}) |
| Matched criteria | {matched} |
| Missing criteria | {missing} |
| Experience alignment | Not assessed by the local keyword heuristic |

## Recommendation summary

{recommendations}

## Interpretation

The score is deterministic keyword coverage for review evidence, not a probability,
candidate ranking, or hiring decision. This portfolio demo is not fairness or
compliance audited and must not replace human assessment.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", type=Path, default=DEFAULT_RESUME)
    parser.add_argument("--job", type=Path, default=DEFAULT_JOB)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_report(args.resume, args.job), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
