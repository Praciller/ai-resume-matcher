# API

## Health

```http
GET /api/health
```

```json
{
  "status": "healthy",
  "mode": "live",
  "configured_providers": ["9arm", "gemini", "groq", "cerebras"],
  "primary_provider": "9arm",
  "max_resume_file_mb": 5,
  "max_resume_chars": 20000,
  "max_jd_chars": 20000
}
```

Health reports configuration only. It does not call a provider.

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

Controlled errors:

| Status | Meaning |
| --- | --- |
| `422` | Invalid file, scanned PDF, empty/short JD, or extraction failure |
| `503` | No provider configured or all providers failed |

Raw provider error bodies and keys are never returned.

## Sample

```http
POST /api/mock-analyze
```

Returns deterministic demonstration data without provider quota.
