# Portfolio review flow

1. Run the setup and verification commands in [local_review.md](local_review.md).
2. Inspect `backend/dataset/synthetic_resume.txt` and
   `backend/dataset/sample_job_description.txt`; both are synthetic.
3. Generate `reports/local_match_report.md` and confirm the stable `69/100`
   result, matched criteria, missing criteria, and recommendations.
4. Start the API in mock mode and verify `/api/health` reports `mock`.
5. Start the frontend and render sample mode without uploading a resume.

The evidence demonstrates deterministic parsing and explainable keyword
coverage. It does not demonstrate hiring accuracy, candidate ranking validity,
fairness, compliance, or suitability for automated employment decisions.

Do not upload sensitive resumes to a public demo. For PDF-path testing, use a
synthetic text-based PDF only.
