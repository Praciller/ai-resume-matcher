# Zero-cost local review

The default path uses synthetic fixtures and deterministic local matching. It
requires no provider key, hosted service, or private resume.

Keep optional bulk or private datasets under the ignored
`backend/dataset/resumes/` directory. Repository checks reject tracked files in
that directory and files larger than 5 MiB; the default review uses
`backend/dataset/synthetic_resume.txt`.

## Windows PowerShell

From the repository root:

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install -r backend/requirements-dev.txt
$env:PYTHONPATH="."
$env:MOCK_AI_MODE="true"
backend/.venv/Scripts/python.exe -m pytest -q backend/tests
backend/.venv/Scripts/python.exe scripts/generate_local_match_report.py
Get-Content reports/local_match_report.md
backend/.venv/Scripts/python.exe -m uvicorn backend.main:app --reload --port 8000
```

Expected evidence includes a `69/100` match score, matched criteria, missing
criteria, recommendations, and the non-hiring-decision disclaimer.

In a second terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Open `http://localhost:5173` and choose sample mode. The API health response at
`http://localhost:8000/api/health` should report `"mode":"mock"`.

## Optional external providers

Copy `.env.example` to `.env`, set `MOCK_AI_MODE=false`, and add only the
server-side provider key you intend to test. Missing keys do not affect mock
mode. Live mode without a configured key returns a controlled `503` response.

## Troubleshooting

- `No module named pytest`: use `backend/.venv/Scripts/python.exe`, not global Python.
- Pytest temp permission errors: create `C:\tmp\ai-resume-temp`, set `TEMP` and
  `TMP` to it, then add `--basetemp=C:/tmp/pytest-ai-resume`.
- Scanned PDFs fail intentionally because OCR is not implemented.
