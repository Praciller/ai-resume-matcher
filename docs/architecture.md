# Architecture

## Runtime

```text
Browser
  -> React/Vite frontend
  -> multipart POST /api/analyze
  -> FastAPI validation
  -> pypdf extraction
  -> provider router
  -> Pydantic validation
  -> metadata + structured result
  -> React report
```

`backend/main.py` owns the API. `api/index.py` only exports that FastAPI `app` for Vercel, preventing local/serverless drift.

## Backend Modules

| Module | Responsibility |
| --- | --- |
| `core/config.py` | Environment parsing and safe defaults |
| `core/parser.py` | PDF, MIME, size, text, and JD validation |
| `core/schema.py` | Strict analysis and API response models |
| `core/analysis.py` | Prompting, providers, fallback, mock output |
| `core/cache.py` | In-process TTL cache |

## Trust Boundaries

- Browser input is untrusted.
- PDF content is parsed only after extension, MIME, header, and size checks.
- Provider output is untrusted until Pydantic validation succeeds.
- Provider errors are logged without response bodies and replaced by controlled API messages.
- Secrets exist only in server-side environment variables.

## Deployment

Vercel builds the Vite frontend into `frontend/dist`. The rewrite sends `/api/*` to `api/index.py`, where Vercel runs the FastAPI ASGI app. Dataset and test files are excluded from the Python function bundle.
