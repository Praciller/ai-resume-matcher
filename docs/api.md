# API

## Health

```http
GET /api/health
```

Default local response:

```json
{
  "status": "healthy",
  "mode": "local",
  "configured_providers": [],
  "primary_provider": "local",
  "max_resume_file_mb": 5,
  "max_resume_chars": 20000,
  "max_jd_chars": 20000
}
```

When the generic external GenAI route is explicitly enabled and `EXTERNAL_GENAI_URL` is configured, health reports:

```json
{
  "status": "healthy",
  "mode": "hybrid",
  "configured_providers": ["external"],
  "primary_provider": "external",
  "max_resume_file_mb": 5,
  "max_resume_chars": 20000,
  "max_jd_chars": 20000
}
```

Health reports configuration only. It does not call the external endpoint and never exposes the endpoint URL or credential.

## Analyze

```http
POST /api/analyze
Content-Type: multipart/form-data
```

Fields:

| Name | Type | Rules |
| --- | --- | --- |
| `resume_file` | PDF | `.pdf`, `application/pdf`, valid header, configured size limit |
| `job_description` | text | Minimum 20 characters, normalized, configured character limit |

Legacy `jd_text` and `/api/screen-resume` remain accepted for compatibility.

Success includes the required analysis schema plus:

- `model_used`
- `provider_used`
- `cached`
- `analysis_id`
- `warnings`

The default response uses `provider_used: "local"`. With external GenAI explicitly enabled, a validated remote result uses `provider_used: "external"`. External failures, malformed JSON, schema violations, or low-quality output fall back to deterministic local analysis and add a controlled warning.

Input-validation errors return `422`. External inference failure does not become a `503` because the deterministic local path remains available.

Raw external response bodies, exception details, endpoint URLs, and credentials are never returned.

## Generic external GenAI contract

When enabled, the backend sends bounded extracted text to the configured server-side endpoint:

```json
{
  "task": "resume_job_match",
  "resume_text": "bounded extracted resume text",
  "job_description": "bounded submitted job description",
  "model": "general",
  "response_format": "analysis_result_v1"
}
```

The endpoint must return:

```json
{
  "analysis": {
    "match_score": 78,
    "summary": "A sufficiently detailed evidence-based summary...",
    "matched_skills": ["Python"],
    "missing_skills": ["AWS"],
    "strengths": ["Shows direct Python evidence."],
    "weaknesses": ["Cloud evidence is limited."],
    "recommendations": ["Add a quantified cloud deployment example."],
    "learning_plan": [],
    "interview_questions": ["Describe a production deployment you owned."],
    "risk_flags": []
  },
  "model": "remote-model-label"
}
```

The `analysis` object is validated using `AnalysisResult` with extra fields forbidden and then checked by the existing quality gate before it can reach the frontend.

## Sample

```http
POST /api/mock-analyze
```

Returns deterministic demonstration data without a resume upload or external inference.
