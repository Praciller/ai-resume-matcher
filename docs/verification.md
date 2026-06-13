# Verification

Verification date: June 13, 2026.

## Local

| Check | Result |
| --- | --- |
| Backend dependency install | Passed |
| Backend tests | 21 passed |
| Frontend unit tests | 7 passed |
| Frontend integration tests | 5 passed |
| Chromium E2E | 3 passed |
| Vite production build | Passed |
| npm high-severity audit | 0 vulnerabilities |
| `/api/health` | Passed |
| Mock PDF analysis | Passed |
| Real PDF analysis through 9arm | Passed |
| Repeat request cache | Passed |
| Gemini structured output | Passed |
| Groq structured output | Passed |
| Cerebras structured output | Passed |
| Mobile width 375 px | No horizontal overflow |

## Input Cases

- Valid text PDF: accepted.
- Invalid PDF header: rejected with `422`.
- Wrong extension or MIME: rejected.
- Image-only PDF: controlled OCR-not-supported message.
- Empty/short JD: rejected.
- Long JD: normalized and truncated with warning.

## Production

Before modernization, the live alias loaded and `/api/health` returned `200`, but the old health route only proved module import and the old UI/API contract remained deployed.

Deployment `dpl_72nawM1Vt8mZrE1MD8Mgpeqv6ekB` was verified at [ai-resume-matcher-psi-one.vercel.app](https://ai-resume-matcher-psi-one.vercel.app).

| Check | Result |
| --- | --- |
| Deployment state | Ready |
| Frontend | `200` |
| `/api/health` | `healthy`, live mode, 9arm primary |
| `/api/mock-analyze` | `200`, validated sample schema |
| Real PDF `/api/analyze` | `200`, validated schema |
| Production provider | 9arm / `qwen3.6-35b-a3b` |
| Provider errors exposed | None |
