"""Synthetic counterfactual-invariance audit tests."""

from pathlib import Path

from backend.core.counterfactual import (
    INVARIANT_FIELDS,
    audit_group,
    audit_negative_control,
    get_counterfactual_group,
    get_negative_control,
    run_audit,
)
from backend.core.analysis import build_mock_analysis
from scripts.generate_counterfactual_invariance_report import render_report


def test_irrelevant_display_name_variation_does_not_change_qualification() -> None:
    group = get_counterfactual_group("display-name")
    audit = audit_group(group)

    assert audit.passed
    assert audit.changed_fields == ()
    assert audit.checked_fields == INVARIANT_FIELDS

    first, second = group.variants
    assert build_mock_analysis(
        first.resume_text, group.job_description
    ) == build_mock_analysis(second.resume_text, group.job_description)


def test_equivalent_qualification_wording_is_invariant() -> None:
    audit = audit_group(get_counterfactual_group("equivalent-wording"))

    assert audit.passed
    assert audit.changed_fields == ()


def test_irrelevant_text_order_is_invariant() -> None:
    audit = audit_group(get_counterfactual_group("irrelevant-text-order"))

    assert audit.passed
    assert audit.changed_fields == ()


def test_skill_preserving_counterfactual_is_invariant() -> None:
    audit = audit_group(get_counterfactual_group("skill-preserving"))

    assert audit.passed
    assert audit.changed_fields == ()


def test_qualification_changing_negative_control_changes_outcome() -> None:
    audit = audit_negative_control(get_negative_control("add-docker-evidence"))

    assert audit.passed
    assert set(audit.changed_fields) >= {
        "match_score",
        "matched_skills",
        "missing_skills",
        "learning_plan",
    }


def test_audit_is_repeatable_and_all_groups_pass() -> None:
    first = run_audit()
    second = run_audit()

    assert first == second
    assert first.passed
    assert len(first.group_audits) == 4
    assert len(first.negative_control_audits) == 1


def test_counterfactual_report_is_reproducible() -> None:
    first = render_report()
    second = render_report()

    assert first == second
    assert "Synthetic diagnostic only" in first
    assert "not a fairness certification" in first


def test_checked_in_counterfactual_report_matches_generator() -> None:
    report_path = (
        Path(__file__).resolve().parents[2] / "reports/counterfactual_invariance.md"
    )

    assert report_path.read_text(encoding="utf-8") == render_report()
