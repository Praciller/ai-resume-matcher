"""Synthetic counterfactual fixtures for the deterministic local matcher."""

from __future__ import annotations

from dataclasses import dataclass

from backend.core.analysis import AnalysisResult, build_mock_analysis


INVARIANT_FIELDS = (
    "match_score",
    "matched_skills",
    "missing_skills",
    "learning_plan",
    "risk_flags",
)
COUNTERFACTUAL_GROUP_IDS = (
    "display-name",
    "equivalent-wording",
    "irrelevant-text-order",
    "skill-preserving",
)
NEGATIVE_CONTROL_IDS = ("add-docker-evidence",)


@dataclass(frozen=True)
class CounterfactualVariant:
    label: str
    resume_text: str


@dataclass(frozen=True)
class CounterfactualGroup:
    identifier: str
    title: str
    job_description: str
    variants: tuple[CounterfactualVariant, ...]


@dataclass(frozen=True)
class GroupAudit:
    group_identifier: str
    group_title: str
    checked_fields: tuple[str, ...]
    changed_fields: tuple[str, ...]
    passed: bool


@dataclass(frozen=True)
class NegativeControl:
    identifier: str
    title: str
    job_description: str
    baseline_resume: str
    changed_resume: str
    required_changed_fields: tuple[str, ...]


@dataclass(frozen=True)
class NegativeControlAudit:
    control_identifier: str
    control_title: str
    checked_fields: tuple[str, ...]
    changed_fields: tuple[str, ...]
    passed: bool


@dataclass(frozen=True)
class AuditRun:
    group_audits: tuple[GroupAudit, ...]
    negative_control_audits: tuple[NegativeControlAudit, ...]

    @property
    def passed(self) -> bool:
        return all(
            audit.passed
            for audit in (*self.group_audits, *self.negative_control_audits)
        )


def _result_snapshot(result: AnalysisResult) -> dict[str, object]:
    payload = result.model_dump(mode="json")
    return {field: payload[field] for field in INVARIANT_FIELDS}


def _analyze_resume(resume_text: str, job_description: str) -> dict[str, object]:
    return _result_snapshot(build_mock_analysis(resume_text, job_description))


def audit_group(group: CounterfactualGroup) -> GroupAudit:
    baseline, *variants = group.variants
    baseline_snapshot = _analyze_resume(baseline.resume_text, group.job_description)
    changed_fields = set()
    for variant in variants:
        snapshot = _analyze_resume(variant.resume_text, group.job_description)
        changed_fields.update(
            field
            for field in INVARIANT_FIELDS
            if snapshot[field] != baseline_snapshot[field]
        )
    ordered_changes = tuple(
        field for field in INVARIANT_FIELDS if field in changed_fields
    )
    return GroupAudit(
        group_identifier=group.identifier,
        group_title=group.title,
        checked_fields=INVARIANT_FIELDS,
        changed_fields=ordered_changes,
        passed=not ordered_changes,
    )


def audit_negative_control(control: NegativeControl) -> NegativeControlAudit:
    baseline_snapshot = _analyze_resume(
        control.baseline_resume, control.job_description
    )
    changed_snapshot = _analyze_resume(control.changed_resume, control.job_description)
    changed_fields = tuple(
        field
        for field in INVARIANT_FIELDS
        if baseline_snapshot[field] != changed_snapshot[field]
    )
    return NegativeControlAudit(
        control_identifier=control.identifier,
        control_title=control.title,
        checked_fields=INVARIANT_FIELDS,
        changed_fields=changed_fields,
        passed=all(
            field in changed_fields for field in control.required_changed_fields
        ),
    )


def get_counterfactual_group(identifier: str) -> CounterfactualGroup:
    if identifier == "display-name":
        return CounterfactualGroup(
            identifier="display-name",
            title="Irrelevant display-name variation",
            job_description="Need Python, SQL, and Docker experience for this synthetic role.",
            variants=(
                CounterfactualVariant(
                    label="python-display-name",
                    resume_text=(
                        "Display name: Synthetic Python Profile\n"
                        "Contact placeholder: display-one@example.test\n\n"
                        "Skills: Python, SQL\n"
                        "Experience: Built reporting tools with Python and SQL.\n"
                        "Projects: Created a synthetic data dashboard.\n"
                        "Education: Bachelor of Science in Computer Science."
                    ),
                ),
                CounterfactualVariant(
                    label="docker-display-name",
                    resume_text=(
                        "Display name: Synthetic Docker Profile\n"
                        "Contact placeholder: display-two@example.test\n\n"
                        "Skills: Python, SQL\n"
                        "Experience: Built reporting tools with Python and SQL.\n"
                        "Projects: Created a synthetic data dashboard.\n"
                        "Education: Bachelor of Science in Computer Science."
                    ),
                ),
            ),
        )
    if identifier == "equivalent-wording":
        return CounterfactualGroup(
            identifier="equivalent-wording",
            title="Equivalent qualification wording",
            job_description="Need Python, FastAPI, and SQL experience for this synthetic role.",
            variants=(
                CounterfactualVariant(
                    label="direct-wording",
                    resume_text=(
                        "Skills: Python, FastAPI, SQL\n"
                        "Experience: Built a Python FastAPI service and optimized SQL reports.\n"
                        "Projects: Delivered an API reporting project.\n"
                        "Education: Bachelor of Science in Computer Science."
                    ),
                ),
                CounterfactualVariant(
                    label="reordered-wording",
                    resume_text=(
                        "Skills: Python, FastAPI, SQL\n"
                        "Experience: Optimized SQL reports while building a FastAPI service in Python.\n"
                        "Projects: Delivered an API reporting project.\n"
                        "Education: Bachelor of Science in Computer Science."
                    ),
                ),
            ),
        )
    if identifier == "irrelevant-text-order":
        common_evidence = (
            "Skills: Python, SQL\n"
            "Experience: Built reporting tools with Python and SQL.\n"
            "Projects: Created a synthetic data dashboard.\n"
            "Education: Bachelor of Science in Computer Science."
        )
        return CounterfactualGroup(
            identifier="irrelevant-text-order",
            title="Irrelevant biography and metadata ordering",
            job_description="Need Python, SQL, and Docker experience for this synthetic role.",
            variants=(
                CounterfactualVariant(
                    label="metadata-before-evidence",
                    resume_text=(
                        "Display name: Synthetic SQL Profile\n"
                        "Biography: Optional synthetic note about Docker tools.\n"
                        "Pronoun wording: neutral wording used for this fixture.\n"
                        "Contact placeholder: order-one@example.test\n"
                        f"{common_evidence}"
                    ),
                ),
                CounterfactualVariant(
                    label="metadata-after-evidence",
                    resume_text=(
                        f"{common_evidence}\n"
                        "Contact placeholder: order-two@example.test\n"
                        "Pronoun wording: pronouns are omitted in this fixture.\n"
                        "Biography: Optional synthetic note about Python tools.\n"
                        "Display name: Synthetic Docker Profile"
                    ),
                ),
            ),
        )
    if identifier == "skill-preserving":
        return CounterfactualGroup(
            identifier="skill-preserving",
            title="Skill-preserving resume presentation change",
            job_description="Need Python, FastAPI, and SQL experience for this synthetic role.",
            variants=(
                CounterfactualVariant(
                    label="standard-sections",
                    resume_text=(
                        "Honorific wording: title omitted.\n"
                        "Skills: Python, FastAPI, SQL\n"
                        "Experience: Built and tested a Python FastAPI service backed by SQL.\n"
                        "Projects: Delivered an API reporting project.\n"
                        "Education: Bachelor of Science in Computer Science."
                    ),
                ),
                CounterfactualVariant(
                    label="alternative-sections",
                    resume_text=(
                        "Technical toolkit: Python; FastAPI; SQL\n"
                        "Experience: Tested a FastAPI API implemented in Python and using SQL.\n"
                        "Projects: Delivered an API reporting project.\n"
                        "Education: B.S. in Computer Science.\n"
                        "Honorific: not included."
                    ),
                ),
            ),
        )
    raise KeyError(f"Unknown counterfactual group: {identifier}")


def get_negative_control(identifier: str) -> NegativeControl:
    if identifier != "add-docker-evidence":
        raise KeyError(f"Unknown negative control: {identifier}")
    baseline = (
        "Skills: Python, SQL\n"
        "Experience: Built reporting tools with Python and SQL.\n"
        "Projects: Created a synthetic data dashboard.\n"
        "Education: Bachelor of Science in Computer Science."
    )
    changed = (
        "Skills: Python, SQL, Docker\n"
        "Experience: Built reporting tools with Python and SQL, then packaged them with Docker.\n"
        "Projects: Created a synthetic data dashboard.\n"
        "Education: Bachelor of Science in Computer Science."
    )
    return NegativeControl(
        identifier="add-docker-evidence",
        title="Relevant Docker evidence added",
        job_description="Need Python, SQL, and Docker experience for this synthetic role.",
        baseline_resume=baseline,
        changed_resume=changed,
        required_changed_fields=(
            "match_score",
            "matched_skills",
            "missing_skills",
            "learning_plan",
        ),
    )


def run_audit() -> AuditRun:
    return AuditRun(
        group_audits=tuple(
            audit_group(get_counterfactual_group(identifier))
            for identifier in COUNTERFACTUAL_GROUP_IDS
        ),
        negative_control_audits=tuple(
            audit_negative_control(get_negative_control(identifier))
            for identifier in NEGATIVE_CONTROL_IDS
        ),
    )
