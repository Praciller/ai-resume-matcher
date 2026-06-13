# Portfolio Review

## Verdict

**Ready after production deployment and leaked-key rotation.**

The local project now demonstrates a credible document-AI workflow rather than a prompt wrapper. The remaining release blockers are operational: deploy the current code and revoke the key previously committed in `.env.example`.

## Initial Audit

| Severity | Finding |
| --- | --- |
| P0 | A real Gemini key was tracked in two example files and git history. |
| P1 | Backend import failed when a Gemini key was absent. |
| P1 | Vercel used handwritten multipart parsing and returned HTTP 200 for error-shaped results. |
| P1 | Hardcoded Gemini 2.0 model and unvalidated free-form provider JSON. |
| P1 | Frontend expected a different schema from the modernization requirements. |
| P1 | Unit and integration scripts were broken despite the default suite passing. |
| P1 | CRA dependency tree reported 49 vulnerabilities, including one critical. |
| P2 | Health reported AI availability without making or validating a provider request. |
| P2 | UI omitted file size, JD count, structured learning plan, and sample mode. |
| P2 | Repository tracked roughly 118 MB of unused resume dataset files. |

## What Changed

- Consolidated local and Vercel backends into one FastAPI app.
- Added strict input and output validation.
- Added 9arm-first routing with Gemini, Groq, and Cerebras fallback.
- Added deterministic mock and sample paths.
- Added safe errors, metadata, cache, and compatibility aliases.
- Migrated CRA/Jest to Vite/Vitest and removed vulnerable dependency chain.
- Split the frontend into required workflow and report components.
- Added responsive, keyboard-accessible product UI and reduced-motion support.
- Added backend, frontend, integration, E2E, build, and live-provider checks.
- Removed secrets from tracked templates.

## Impeccable Audit

| Dimension | Score | Evidence |
| --- | ---: | --- |
| Accessibility | 3/4 | Semantic headings, labels, alert/status regions, focus states, reduced motion, 44 px controls; automated WCAG scan still pending |
| Performance | 4/4 | 60 KB gzip JS, no expensive motion, small provider-free sample path |
| Responsive | 4/4 | Desktop and 375 px browser checks pass without horizontal overflow |
| Theming | 3/4 | Central OKLCH token system; no user-selectable dark theme |
| Anti-patterns | 4/4 | No gradient text, glass, nested cards, decorative motion, or hero metric layout |
| **Total** | **18/20** | **Excellent, minor operational polish remains** |

## Remaining Gaps

- Rotate the previously committed Gemini key. Removing it from the current tree does not revoke it.
- Deploy and re-run production PDF analysis.
- Add automated axe or Lighthouse accessibility checks.
- Add evaluator fixtures before presenting match score as calibrated.
- Add OCR only as an explicit future feature.

## Reviewer Path

1. Open the live demo.
2. Run sample mode to inspect the full report without quota.
3. Open `/api/health` to review provider configuration and limits.
4. Review `backend/core/analysis.py` for routing and validation.
5. Review backend fallback tests and frontend result-rendering tests.

## Resume Positioning

Best fit: AI Engineer, GenAI Engineer, Full-Stack Engineer with AI integration.

Resume bullet:

> Modernized an AI resume matching platform using React, FastAPI, multi-provider structured analysis, PDF validation, Pydantic schema enforcement, provider fallback, mock mode, and Vercel deployment verification to generate explainable skill-gap and interview-preparation reports.
