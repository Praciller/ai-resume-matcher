# Counterfactual Invariance Audit

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
| Fixture count | 8 synthetic resume variants |
| Invariance groups | 4 |
| Passed groups | 4 |
| Failed groups | 0 |
| Negative controls | 1 |
| Passed negative controls | 1 |
| Failed negative controls | 0 |
| Overall audit | PASS |

### Invariant fields checked

The audit compares these fields exactly between the first variant in each group
and every other variant:

`match_score, matched_skills, missing_skills, learning_plan, risk_flags`

| Group | Variants | Result | Changed invariant fields |
| --- | ---: | --- | --- |
| Irrelevant display-name variation | 2 | PASS | None |
| Equivalent qualification wording | 2 | PASS | None |
| Irrelevant biography and metadata ordering | 2 | PASS | None |
| Skill-preserving resume presentation change | 2 | PASS | None |

### Negative controls

Negative controls intentionally change job-relevant evidence. A passing control
must change the expected qualification fields, so an always-equal implementation
cannot satisfy this audit.

| Control | Result | Changed invariant fields |
| --- | --- | --- |
| Relevant Docker evidence added | PASS | match_score, matched_skills, missing_skills, learning_plan |

## Methodology

Each group uses the same synthetic job description for all variants. Job-relevant
skills, experience, projects, relevant education, and qualification evidence are
held equivalent. Only explicitly labelled presentation metadata or equivalent
prose is varied. The local matcher removes labelled presentation metadata before
keyword evaluation, then the audit compares the invariant fields above.

Purely textual explanation fields are intentionally not treated as qualification
invariants: `summary, strengths, weaknesses, recommendations, interview_questions`. They may change when display text
or ordering legitimately changes. API transport warnings are also outside this
qualification snapshot; they are input/runtime notices rather than qualification
evidence.

## Limitations

- The fixtures are small synthetic diagnostics, not representative applicant data.
- Exact keyword coverage does not assess proficiency, context, recency, synonyms, or transferable skills.
- A passing audit demonstrates only these fixture-level invariance properties; it does not establish fairness, absence of bias, legal compliance, or employment validity.
- The audit does not compare hiring outcomes and must not be used to automate or rank hiring decisions.
- External inference behavior is out of scope; the zero-key deterministic local path is the evidence target.
