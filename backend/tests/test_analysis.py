from backend.core.analysis import build_mock_analysis, make_analysis_id


def test_local_analysis_is_deterministic() -> None:
    first = build_mock_analysis(
        "Python React developer", "Need Python React AWS engineer"
    )
    second = build_mock_analysis(
        "Python React developer", "Need Python React AWS engineer"
    )
    assert first == second
    assert first.matched_skills == ["python", "react"]
    assert first.missing_skills == ["aws"]


def test_local_score_increases_with_explicit_skill_coverage() -> None:
    partial = build_mock_analysis("Python developer", "Need Python React AWS engineer")
    stronger = build_mock_analysis(
        "Python React AWS developer", "Need Python React AWS engineer"
    )
    assert stronger.match_score > partial.match_score
    assert stronger.missing_skills == []


def test_analysis_id_is_stable_and_input_sensitive() -> None:
    first = make_analysis_id("resume", "job")
    second = make_analysis_id("resume", "job")
    changed = make_analysis_id("resume changed", "job")
    assert first == second
    assert first != changed
