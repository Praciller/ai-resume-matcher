# Testing

## Backend

```powershell
backend/.venv/Scripts/python.exe -m pytest -q backend/tests
```

Coverage includes:

- PDF extension, MIME, header, size, extraction, scanned-PDF detection
- JD minimum and maximum handling
- schema bounds, required arrays, and deduplication
- deterministic mock analysis
- 9arm-to-Gemini fallback
- Gemini Lite-to-Flash fallback
- health, sample, full mock PDF flow, invalid PDF, empty JD

## Frontend

```powershell
cd frontend
npm run test:unit
npm run test:integration
npm run test:e2e
npm run build
npm audit --audit-level=high
```

Unit tests cover form validity, PDF selection, invalid files, result rendering, sample mode, and controlled errors. Integration tests cover API URLs, multipart fields, responses, and network failures. Playwright covers desktop load, sample rendering, and mobile usability.

## Real Provider Smoke

Use a non-sensitive synthetic PDF and JD. Verify each configured provider independently before relying on fallback. Output should record only provider, model, score, metadata, and validation counts, never document text or keys.
