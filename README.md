# AI Resume Matcher

Compare a PDF resume with a job description and receive a validated match report with fit score, evidence, skill gaps, recommended actions, learning priorities, interview questions, and neutral risk flags.

**Live demo:** https://ai-resume-matcher-psi-one.vercel.app  
**Health:** https://ai-resume-matcher-psi-one.vercel.app/api/health

![Structured resume analysis report](docs/screenshots/analysis-report.png)

## Product flow

```text
PDF resume + job description
  -> React validation and upload
  -> FastAPI /api/analyze
  -> PDF text extraction and limits
  -> deterministic local analysis by default
  -> optional generic external GenAI when explicitly enabled
  -> strict Pydantic validation and quality gate
  -> safe local fallback on external failure
  -> score, evidence, gaps, actions, interview prep
  -> React report rendering
```

## Highlights

- Validates PDF extension, MIME type, file size, extractable text, and job-description length.
- Keeps deterministic local matching as the zero-key default and reviewer path.
- Preserves external GenAI through one vendor-neutral server-side HTTP adapter rather than a provider SDK.
- Validates external output against the same strict schema and quality gate used by the API.
- Falls back to deterministic local analysis when external inference is unavailable or invalid.
- Separates local and external cache keys so changing inference mode cannot return a stale result from another route.
- Supports sample mode for reviewer-friendly demonstrations.
- Includes unit, integration, API, schema, build, guardrail, and dependency-audit checks.

## Tech stack

| Layer | Technology |
| --- | --- |
| Frontend | React 18, Vite 8, Tailwind CSS, Lucide |
| Backend | Python 3.12, FastAPI, Pydantic v2, HTTPX |
| PDF | pypdf |
| Default analysis | Deterministic evidence and skill-gap matching |
| Optional GenAI | Generic server-side JSON endpoint |
| Testing | pytest, Vitest, Testing Library, Playwright |
| Deployment | Vercel |

## Local setup

```powershell
git clone https://github.com/Praciller/ai-resume-matcher.git
cd ai-resume-matcher
python -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install -r backend/requirements-dev.txt
backend/.venv/Scripts/python.exe -m uvicorn backend.main:app --reload --port 8000
```

Frontend:

```powershell
cd frontend
npm ci
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api` to `http://127.0.0.1:8000`.

Generate deterministic evidence from synthetic fixtures:

```powershell
$env:PYTHONPATH="."
backend/.venv/Scripts/python.exe scripts/generate_local_match_report.py
Get-Content reports/local_match_report.md
```

No real resumes or bulk resume datasets are tracked. Reviewer fixtures are synthetic; optional local datasets belong under the ignored `backend/dataset/resumes/` directory.

## Environment

Local analysis is the default and requires no external credential. See [.env.example](.env.example).

To explicitly enable the optional server-side GenAI route:

```env
ENABLE_EXTERNAL_GENAI=true
EXTERNAL_GENAI_URL=https://your-controlled-endpoint.example/v1/resume-match
EXTERNAL_GENAI_API_KEY=
EXTERNAL_GENAI_MODEL=general
EXTERNAL_GENAI_TIMEOUT_SECONDS=30
```

The endpoint receives extracted resume text and the submitted job description. Do not enable this route for sensitive documents unless that data flow and endpoint are approved. Credentials remain server-side and are never exposed to the browser or health response.

The endpoint accepts a neutral JSON request with `task`, `resume_text`, `job_description`, `model`, and `response_format`. It returns an `analysis` object matching the strict `AnalysisResult` schema and may include a `model` label.

## API

### `GET /api/health`

Reports `local` mode by default. When external GenAI is explicitly enabled and configured, it reports `hybrid`, `configured_providers: ["external"]`, and `primary_provider: "external"`. The endpoint never performs an inference call or returns endpoint URLs or credentials.

### `POST /api/analyze`

Multipart fields:

- `resume_file`: PDF
- `job_description`: job-description text

The response follows the strict schema documented in [docs/api.md](docs/api.md), including score, matched and missing skills, recommendations, learning plan, interview questions, warnings, inference metadata, and an analysis identifier.

External output is treated as untrusted. Invalid JSON, schema violations, low-quality results, network failures, and non-success HTTP responses trigger the deterministic local fallback with a controlled warning.

### `POST /api/mock-analyze`

Returns a deterministic sample report without a resume upload or external inference.

## Matching method

The default matcher extracts a bounded set of explicit skill terms from the job description, checks whether those terms occur in the resume, computes a reproducible coverage-based score, and generates recommendations for missing evidence. It does not infer hidden experience or make hiring decisions.

The optional external route must return the same structured analysis contract. Its output is still schema-validated and remains decision support for human review.

## Safety and scope

- This is a portfolio decision-support demo, not an automated hiring authority.
- Synthetic samples and deterministic local analysis are the default reviewer inputs/path.
- The score is a portfolio heuristic, not calibrated to hiring outcomes.
- The project has not been fairness or compliance audited.
- Do not upload sensitive resumes to a public deployment.
- Enabling external GenAI transmits extracted resume/JD text to the configured external endpoint.
- Results support human review only and must not determine candidate selection.

## Testing

```powershell
backend/.venv/Scripts/python.exe -m pytest -q backend/tests
backend/.venv/Scripts/python.exe -m ruff check backend scripts
backend/.venv/Scripts/python.exe scripts/check_repo_guardrails.py

cd frontend
npm run test:unit
npm run test:integration
npm run test:e2e
npm run build
npm audit --audit-level=high
```

See [docs/testing.md](docs/testing.md) and [docs/verification.md](docs/verification.md).

## Known limitations

- No OCR for scanned or image-only PDFs.
- Cache is process-local and can reset between serverless instances.
- The default score is based on bounded explicit skill matching and misses synonyms, proficiency, recency, and transferable skills.
- The external endpoint contract does not by itself establish model quality, fairness, privacy, or policy compliance.
- The result is not a predictor of interview or hiring outcomes.

## Documentation

- [Architecture](docs/architecture.md)
- [API](docs/api.md)
- [Testing](docs/testing.md)
- [Verification](docs/verification.md)
- [Portfolio review](PORTFOLIO_REVIEW.md)
- [Local review](docs/local_review.md)
- [Portfolio reviewer flow](docs/portfolio_review.md)
- [Matching methodology](docs/matching_methodology.md)

## License

MIT
