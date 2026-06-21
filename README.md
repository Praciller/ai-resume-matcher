# AI Resume Matcher

Compare a PDF resume with a job description and receive a validated match report: fit score, evidence, skill gaps, actions, learning priorities, interview questions, and neutral risk flags.

**Live demo:** [ai-resume-matcher-psi-one.vercel.app](https://ai-resume-matcher-psi-one.vercel.app)
**Health:** [ai-resume-matcher-psi-one.vercel.app/api/health](https://ai-resume-matcher-psi-one.vercel.app/api/health)

![Structured AI resume analysis report](docs/screenshots/analysis-report.png)

## Product Flow

```text
PDF resume + job description
  -> React validation and upload
  -> FastAPI /api/analyze
  -> PDF text extraction and limits
  -> 9arm-first provider routing
  -> strict Pydantic schema validation
  -> score, evidence, gaps, actions, interview prep
  -> safe React report rendering
```

## Highlights

- Validates PDF extension, MIME type, file size, extractable text, and JD length.
- Keeps provider keys server-side.
- Routes `9arm -> Gemini Lite -> Gemini Flash -> Groq -> Cerebras`.
- Rejects malformed or low-quality model output before rendering.
- Supports deterministic mock and sample modes without API quota.
- Caches repeated analyses in process with a configurable TTL.
- Uses one FastAPI app for local development and Vercel.
- Includes unit, integration, API, schema, fallback, build, and browser tests.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | React 18, Vite 8, Tailwind CSS, Lucide |
| Backend | Python 3.12, FastAPI, Pydantic v2, HTTPX |
| PDF | pypdf |
| AI | 9arm, Gemini, Groq, Cerebras |
| Testing | pytest, Vitest, Testing Library, Playwright |
| Deployment | Vercel |

## Local Setup

```powershell
git clone https://github.com/Praciller/ai-resume-matcher.git
cd ai-resume-matcher
```

No API key or real resume is required. Mock analysis is the default.

Backend:

```powershell
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

Generate deterministic evidence from synthetic text fixtures:

```powershell
$env:PYTHONPATH="."
backend/.venv/Scripts/python.exe scripts/generate_local_match_report.py
Get-Content reports/local_match_report.md
```

Expected fixture result: `69/100`, with matched and missing criteria listed in
`reports/local_match_report.md`. The generated report is gitignored.

## Environment

See [.env.example](.env.example) for the complete contract.

External provider routing is optional and explicitly enabled by setting
`MOCK_AI_MODE=false` plus a server-side key:

```env
AI_PROVIDER_ORDER=9arm,gemini,groq,cerebras
NINEARM_API_KEY=
NINEARM_RESUME_MODEL=qwen3.6-35b-a3b
```

Gemini requirements-compatible defaults:

```env
GEMINI_API_KEY=
GEMINI_RESUME_MODEL=gemini-2.5-flash-lite
GEMINI_RESUME_FALLBACK_MODEL=gemini-2.5-flash
GEMINI_TIMEOUT_SECONDS=30
GEMINI_MAX_RETRIES=1
```

Never put API keys in frontend variables or commit them to Git. Rotate any key that has ever appeared in repository history.

## API

### `GET /api/health`

Returns mode, configured providers, primary provider, and input limits. It does not spend AI quota.

### `POST /api/analyze`

Multipart fields:

- `resume_file`: PDF
- `job_description`: job-description text

Response follows the strict schema documented in [docs/api.md](docs/api.md), including:

```json
{
  "match_score": 78,
  "summary": "Evidence-based role fit summary.",
  "matched_skills": [],
  "missing_skills": [],
  "strengths": [],
  "weaknesses": [],
  "recommendations": [],
  "learning_plan": [],
  "interview_questions": [],
  "risk_flags": [],
  "model_used": "qwen3.6-35b-a3b",
  "provider_used": "9arm",
  "cached": false,
  "analysis_id": "string",
  "warnings": []
}
```

### `POST /api/mock-analyze`

Returns a deterministic sample report without a resume or provider call.

## Mock AI Mode

Mock mode is the default. The explicit setting is:

```env
MOCK_AI_MODE=true
```

The full PDF and JD validation path still runs. Analysis becomes deterministic and local.

## Safety and scope

- This is a portfolio decision-support demo, not an automated hiring authority.
- Synthetic samples are the default reviewer inputs.
- The scoring heuristic is not calibrated to hiring outcomes.
- The project has not been fairness or compliance audited.
- Do not upload sensitive resumes to a public deployment.

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

## Deployment

Vercel builds `frontend/dist` and exposes the FastAPI app from `api/index.py`.

Configure the server-side variables from `.env.example` in Vercel. Do not add `VITE_*` secrets. After deployment, verify:

1. `/` loads.
2. `/api/health` reports the intended provider order.
3. Sample mode renders.
4. A text-based PDF completes real analysis.
5. Invalid and scanned PDFs fail with controlled messages.

## Known Limitations

- No OCR for scanned or image-only PDFs.
- Cache is process-local and can reset between serverless instances.
- Match score is model-generated, not calibrated against hiring outcomes.
- Provider quotas, model availability, and latency can change.
- Resume and JD text are sent to the first available configured provider.
- Keyword coverage misses synonyms, context, proficiency, recency, and transferable skills.
- Results support human review only and must not determine candidate selection.

## Future Improvements

- Add rubric-based score evaluation fixtures.
- Add OCR as an explicit opt-in path.
- Add multiple-resume comparison.
- Add saved analysis history with user-controlled retention.
- Export reports to PDF.
- Add a local embedding similarity baseline.

## Resume Bullet

Modernized an AI resume matching platform using React, FastAPI, multi-provider structured analysis, PDF validation, Pydantic schema enforcement, provider fallback, mock mode, and Vercel deployment verification to generate explainable skill-gap and interview-preparation reports.

## Documentation

- [Architecture](docs/architecture.md)
- [API](docs/api.md)
- [Model routing](docs/model_routing.md)
- [Gemini analysis](docs/gemini_resume_analysis.md)
- [Testing](docs/testing.md)
- [Verification](docs/verification.md)
- [Portfolio review](PORTFOLIO_REVIEW.md)
- [Local review](docs/local_review.md)
- [Portfolio reviewer flow](docs/portfolio_review.md)
- [Matching methodology](docs/matching_methodology.md)

## License

MIT
