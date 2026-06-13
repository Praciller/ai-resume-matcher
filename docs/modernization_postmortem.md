# Modernization Postmortem

## Summary

The repository appeared deployed but its health check, API contract, tests, dependency state, and tracked assets did not support a reliable production claim. Commit `6ca8699` rebuilt the application around one validated FastAPI backend and a tested Vite frontend.

## Symptom

- Health returned `200` without proving provider readiness.
- Local and Vercel backends implemented different behavior.
- Real provider JSON was not schema-enforced.
- Frontend tests and integration scripts did not exercise the actual workflow.
- Repository examples contained a live Gemini key.
- Roughly 118 MB of unused resume data was tracked.

## Root Cause

The project evolved through parallel local and serverless implementations without one shared contract or release gate. Deployment success was treated as evidence of application correctness.

## Why The Symptom Appeared

Import-only health checks and permissive HTTP `200` error payloads hid configuration and provider failures. Divergent schemas let frontend and backend changes pass independently.

## Fix

- Consolidated all API entry points on `backend.main`.
- Added Pydantic input/output contracts and controlled `422`/`503` failures.
- Added 9arm-first routing with Gemini, Groq, and Cerebras fallback.
- Added deterministic sample mode, caching, and provider metadata.
- Migrated the frontend to Vite/Vitest with unit, integration, and Chromium E2E coverage.
- Removed secrets from the current tree and removed the dataset from Git tracking.
- Deployed and verified the complete PDF-to-report flow on Vercel.

## How It Was Found

The audit reproduced imports, test scripts, provider calls, repository size, secret scans, local browser flows, and the existing live deployment before changes were made.

## Why It Slipped

There was no release checklist requiring a real provider request, schema validation, dependency audit, secret scan, or browser-level production test.

## Validation

- Backend: 21 tests passed.
- Frontend: 7 unit and 5 integration tests passed.
- Browser: 3 Chromium E2E tests passed.
- Dependency audit: 0 vulnerabilities.
- Production: home, health, sample analysis, and real 9arm PDF analysis returned `200`.

## Actions

- Revoke the Gemini key that remains exposed in Git history.
- Add automated accessibility scanning.
- Add evaluator fixtures for score calibration.
