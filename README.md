# AI Resume Matcher

AI-powered resume and job-description matching platform. The app parses PDF resumes, compares them against job descriptions with Gemini, and returns match scoring, skill gaps, career recommendations, and interview preparation guidance.

Live demo: https://ai-resume-matcher-chi.vercel.app

## Role Fit

| Target role | Evidence shown in this repo |
| --- | --- |
| AI Engineer | LLM-based document analysis, structured extraction, scoring workflow, API integration |
| GenAI Engineer | Gemini prompt design, structured response contract, career guidance generation |
| Data Analyst | Skill-gap analysis, match scoring, explainable summary, ranked recommendations |
| Full-Stack / Frontend | React UI, Python API, Vercel deployment, file upload workflow |

## AI Problem Solved

Resume screening is hard because resumes and job descriptions are unstructured documents. This project converts both into structured comparison output so a user can see fit score, matched skills, missing skills, learning priorities, and interview preparation points.

## Architecture

```text
PDF resume + job description
  -> React upload and JD form
  -> Python/Vercel API endpoint
  -> PDF text extraction
  -> Gemini analysis prompt
  -> Structured JSON response
  -> Match score, skill gaps, recommendations
  -> React results dashboard
```

## AI and Data Flow

- Extracts text from uploaded PDF resumes.
- Accepts raw job-description text from the user.
- Sends both documents to Gemini with a structured matching rubric.
- Produces score, summary, matched skills, missing skills, development plan, and interview guidance.
- Displays the result in a recruiter/candidate-friendly UI.

## Key Engineering Highlights

- End-to-end document AI workflow from file upload to recommendation output.
- Structured response design for reliable UI rendering.
- Serverless Python backend for AI analysis.
- React frontend with clear state handling and user feedback.
- Health endpoint for checking backend/API readiness.
- Test commands for unit, integration, E2E, and coverage workflows.

## Tech Stack

| Layer | Tools |
| --- | --- |
| Frontend | React 18, shadcn/ui, Tailwind CSS |
| Backend | Python, Vercel serverless functions, FastAPI-compatible local backend |
| AI | Google Gemini 2.0 Flash |
| Parsing | PDF text extraction |
| Testing | Jest, React Testing Library, Playwright |
| Deployment | Vercel |

## Evaluation and Testing

Recommended evaluation cases:

| Case | Expected behavior |
| --- | --- |
| Strong resume / matching JD | High score, accurate strengths, few gaps |
| Weak resume / senior JD | Lower score, clear skill gaps, realistic guidance |
| Missing JD details | Asks for or infers with caution, avoids unsupported claims |
| Long resume | Extracts relevant skills and does not over-focus on noise |
| Non-technical resume | Returns useful analysis without crashing |

Available frontend checks:

```bash
cd frontend
npm run test:unit
npm run test:integration
npm run test:e2e
npm run test:coverage
```

Backend health check:

```text
GET /api/health
```

## Local Setup

```bash
git clone https://github.com/Praciller/ai-resume-matcher.git
cd ai-resume-matcher
```

Install frontend dependencies:

```bash
cd frontend
npm install
```

Install backend dependencies for local development:

```bash
cd ../backend
pip install -r requirements.txt
```

Create `.env` with:

```env
GEMINI_API_KEY=your_google_gemini_key
```

Run locally:

```bash
# Terminal 1
cd backend
python main.py

# Terminal 2
cd frontend
npm start
```

## Deployment

The production app is deployed on Vercel. Required environment variable:

```env
GEMINI_API_KEY=your_google_gemini_key
```

Verify deployment by checking:

- Frontend loads.
- `/api/health` returns healthy status.
- PDF upload works.
- Gemini analysis returns structured results.

## Why This Repo Matters

This repo supports AI Engineer and GenAI Engineer applications because it demonstrates practical document understanding, prompt-to-structured-output design, and user-facing AI workflow delivery. It also supports data analyst positioning because the output is essentially a structured gap analysis and recommendation report.

## License

MIT
