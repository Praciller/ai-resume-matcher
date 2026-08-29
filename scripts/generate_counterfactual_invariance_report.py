"""Generate the deterministic synthetic counterfactual audit report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.core.counterfactual import (  # noqa: E402
    COUNTERFACTUAL_GROUP_IDS,
    INVARIANT_FIELDS,
    get_counterfactual_group,
    run_audit,
)


DEFAULT_OUTPUT = ROOT / "reports/counterfactual_invariance.md"
EXPLANATION_FIELDS = (
    "summary",
    "strengths",
    "weaknesses",
    "recommendations",
    "interview_questions",
)


def _field_text(fields: tuple[str, ...]) -> str:
    return ", ".join(fields) if fields else "None"


def render_report() -> str:
    audit = run_audit()
    groups = [
        get_counterfactual_group(identifier) for identifier in COUNTERFACTUAL_GROUP_IDS
    ]
    fixture_count = sum(len(group.variants) for group in groups)
    passed_groups = sum(item.passed for item in audit.group_audits)
    failed_groups = len(audit.group_audits) - passed_groups
    passed_controls = sum(item.passed for item in audit.negative_control_audits)
    failed_controls = len(audit.negative_control_audits) - passed_controls

    group_rows = "\n".join(
        "| {title} | {variants} | {status} | {changed} |".format(
            title=item.group_title,
            variants=len(group.variants),
            status="PASS" if item.passed else "FAIL",
            changed=_field_text(item.changed_fields),
        )
        for item, group in zip(audit.group_audits, groups, strict=True)
    )
    control_rows = "\n".join(
        "| {title} | {status} | {changed} |".format(
            title=item.control_title,
            status="PASS" if item.passed else "FAIL",
            changed=_field_text(item.changed_fields),
        )
        for item in audit.negative_control_audits
    )

    return f"""# Counterfactual Invariance Audit

This reviewer artifact is generated from manually authored, synthetic fixtures by
`scripts/generate_counterfactual_invariance_report.py`. It is a deterministic
diagnostic for the local keyword matcher.

## Safety boundary

- Synthetic diagnostic only; this is not a fairness certification.
- This is not a hiring-outcome benchmark, legal assessment, or compliance certification.
- No real applicant data, external datasets, or live external AI providers are used.
- No protected or sensitive traits are inferred, classified, or assigned.
- The product remains human-review decision support only and must not determine candidate selection.

## Results

| Measure | Result |
| --- | --- |
| Fixture count | {fixture_count} synthetic resume variants |
| Invariance groups | {len(audit.group_audits)} |
| Passed groups | {passed_groups} |
| Failed groups | {failed_groups} |
| Negative controls | {len(audit.negative_control_audits)} |
| Passed negative controls | {passed_controls} |
| Failed negative controls | {failed_controls} |
| Overall audit | {"PASS" if audit.passed else "FAIL"} |

### Invariant fields checked

The audit compares these fields exactly between the first variant in each group
and every other variant:

`{", ".join(INVARIANT_FIELDS)}`

| Group | Variants | Result | Changed invariant fields |
| --- | ---: | --- | --- |
{group_rows}

### Negative controls

Negative controls intentionally change job-relevant evidence. A passing control
must change the expected qualification fields, so an always-equal implementation
cannot satisfy this audit.

| Control | Result | Changed invariant fields |
| --- | --- | --- |
{control_rows}

## Methodology

Each group uses the same synthetic job description for all variants. Job-relevant
skills, experience, projects, relevant education, and qualification evidence are
held equivalent. Only explicitly labelled presentation metadata or equivalent
prose is varied. The local matcher removes labelled presentation metadata before
keyword evaluation, then the audit compares the invariant fields above.

Purely textual explanation fields are intentionally not treated as qualification
invariants: `{", ".join(EXPLANATION_FIELDS)}`. They may change when display text
or ordering legitimately changes. API transport warnings are also outside this
qualification snapshot; they are input/runtime notices rather than qualification
evidence.

## Limitations

- The fixtures are small synthetic diagnostics, not representative applicant data.
- Exact keyword coverage does not assess proficiency, context, recency, synonyms, or transferable skills.
- A passing audit demonstrates only these fixture-level invariance properties; it does not establish fairness, absence of bias, legal compliance, or employment validity.
- The audit does not compare hiring outcomes and must not be used to automate or rank hiring decisions.
- External inference behavior is out of scope; the zero-key deterministic local path is the evidence target.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_report(), encoding="utf-8")
    print(args.output)
    return 0 if run_audit().passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
