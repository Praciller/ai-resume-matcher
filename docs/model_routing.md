# Analysis routing

## Current public path

The public application uses one deterministic local analysis path. It does not route resume or job-description text to an external inference service.

```text
validated PDF text + validated job description
  -> bounded skill extraction
  -> explicit matched/missing evidence
  -> reproducible coverage-based score
  -> schema-validated report
```

## Acceptance gate

Every result must:

1. Validate against `AnalysisResult`.
2. Keep score in `0..100`.
3. Include every required array.
4. Include a meaningful summary and actionable recommendations.
5. Deduplicate skill evidence through the bounded matching logic.

## Privacy

The analysis itself runs locally in the application process. Public deployments still receive the uploaded resume at the application server, so sensitive personal documents should not be sent to an untrusted deployment.

## Limitations

The matcher recognizes an intentionally bounded skill vocabulary and does not infer synonyms, proficiency, recency, or hidden experience. The score is a reproducible portfolio heuristic rather than a hiring prediction.
