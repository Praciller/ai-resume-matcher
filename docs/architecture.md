# Architecture

## Runtime

```text
Browser
  -> React/Vite frontend
  -> multipart POST /api/analyze
  -> FastAPI validation
  -> pypdf extraction
  -> inference route selection
       -> deterministic local analysis (default)
       -> generic external GenAI endpoint (explicit opt-in)
  -> Pydantic schema + quality validation
  -> deterministic local fallback if external output fails validation
  -> metadata + structured result
  -> React report
```

`backend/main.py` owns the API. `api/index.py` only exports that FastAPI `app` for Vercel, preventing local/serverless drift.

## Backend Modules

| Module | Responsibility |
| --- | --- |
| `core/config.py` | Environment parsing, safe local defaults, external-route opt-in |
| `core/parser.py` | PDF, MIME, size, text, and JD validation |
| `core/schema.py` | Strict analysis and API response models |
| `core/analysis.py` | Deterministic analysis and response metadata helpers |
| `core/external.py` | Vendor-neutral external GenAI HTTP contract and output validation |
| `core/cache.py` | In-process TTL cache |

## Trust Boundaries

- Browser input is untrusted.
- PDF content is parsed only after extension, MIME, header, and size checks.
- Deterministic local analysis requires no external network inference.
- External GenAI is disabled by default and must be explicitly enabled with a server-side endpoint.
- Enabling external GenAI sends the bounded extracted resume text and submitted job description to that configured endpoint.
- External output is untrusted until Pydantic schema validation and the analysis quality gate succeed.
- External failures or invalid output produce a controlled warning and deterministic local fallback; raw response bodies and exception details are not returned.
- External endpoint credentials exist only in server-side environment variables.
- Local and external cache keys are separated by route/model to prevent cross-mode cache reuse.

## Generic External Contract

The server sends a JSON request containing `task`, bounded `resume_text`, bounded `job_description`, `model`, and `response_format`. The endpoint must return an `analysis` object matching `AnalysisResult`; an optional `model` label may identify the remote model. The repository does not prescribe a specific inference vendor or SDK.

## Deployment

Vercel builds the Vite frontend into `frontend/dist`. The rewrite sends `/api/*` to `api/index.py`, where Vercel runs the FastAPI ASGI app. Dataset and test files are excluded from the Python function bundle.

The public/local review path remains deterministic. Any deployment enabling external GenAI must separately approve the endpoint, data handling, credentials, retention, and model-evaluation policy.
