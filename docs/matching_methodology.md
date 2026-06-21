# Matching methodology

## Deterministic local score

Local mode case-folds resume and job-description text, recognizes a fixed set
of skill terms, and divides matched job skills by recognized job skills:

```text
score = round(48 + skill_coverage * 42)
```

The bounded `48-90` score is a presentation heuristic, not a probability. The
response exposes matched skills, missing skills, strengths, weaknesses,
recommendations, a learning plan, interview questions, and neutral risk flags.

## Fixture strategy

`backend/dataset/synthetic_resume.txt` and
`backend/dataset/sample_job_description.txt` are synthetic. Running
`scripts/generate_local_match_report.py` always produces the same `69/100`
result and writes ignored evidence to `reports/local_match_report.md`.

Tests verify deterministic output, the no-key default, prevention of external
provider calls in mock mode, and controlled failure when live mode has no key.

## Limitations

- Exact term matching misses synonyms and context.
- The score does not assess proficiency, recency, work authorization, or culture fit.
- No validation against hiring outcomes has been performed.
- No fairness, bias, accessibility, or regulatory compliance audit has been performed.
- External-model results can vary and send submitted text to the selected provider.

This project supplies inspectable decision-support evidence for a human reviewer.
It must not rank candidates or make hiring decisions.
