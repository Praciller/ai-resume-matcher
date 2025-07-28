# Intelligent Resume Screener

An AI-powered full-stack application that automatically extracts information from resumes and matches them against job descriptions using Google Gemini AI.

## Features

- **PDF Resume Parsing**: Extract text content from PDF resumes
- **AI-Powered Data Extraction**: Use Google Gemini AI to extract structured data (skills, experience, education, etc.)
- **Job Matching**: Compare resume data against job descriptions with compatibility scoring (0-100)
- **Brutalist UI Design**: Clean, functional interface with monospace fonts and high contrast
- **Real-time Analysis**: Get instant match scores and detailed summaries

## Architecture

### Backend (FastAPI)

- **PDF Processing**: Extract text from PDF files using pypdf
- **AI Integration**: Google Gemini 2.0 Flash for structured data extraction and matching
- **RESTful API**: FastAPI endpoints with proper error handling and CORS support

### Frontend (React)

- **Brutalist Design**: Monospace fonts, black borders, no rounded corners
- **Two-Panel Layout**: Job description input and results display
- **Real-time Status**: Backend connection monitoring
- **File Upload**: Drag-and-drop PDF resume upload

## Quick Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API key

### Automated Setup

Run the setup script for your operating system:

**Linux/macOS:**

```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**

```cmd
setup.bat
```

### Manual Setup Instructions

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
# Create a .env file in the backend directory
cp .env.example .env
# Edit .env and add your Gemini API key:
# GEMINI_API_KEY=your_actual_api_key_here
```

4. Start the FastAPI server:

```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install Node.js dependencies:

```bash
npm install
```

3. Start the React development server:

```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### POST /screen-resume

Screen a resume against a job description.

**Request:**

- `resume_file`: PDF file (multipart/form-data)
- `jd_text`: Job description text (form field)

**Response:**

```json
{
  "match_score": 85,
  "match_summary": "Strong candidate with excellent technical skills...",
  "detailed_analysis": {
    "skill_matches": ["Python", "React", "JavaScript"],
    "skill_gaps": ["Kubernetes", "AWS"],
    "experience_match": "5+ years experience aligns well",
    "education_match": "Bachelor's degree in Computer Science",
    "overall_recommendation": "hire - strong technical fit"
  }
}
```

### POST /extract-resume

Extract structured data from resume only (for testing).

**Request:**

- `resume_file`: PDF file (multipart/form-data)

**Response:**

```json
{
  "extracted_data": {
    "skills": ["Python", "JavaScript", "React"],
    "experience_years": 6,
    "education": ["Bachelor's in Computer Science"],
    "previous_roles": ["Software Engineer", "Full Stack Developer"],
    "key_achievements": [
      "Led team of 5 developers",
      "Increased performance by 40%"
    ],
    "contact_info": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-555-0123"
    }
  }
}
```

### GET /health

Check backend health and AI service status.

## Usage

1. **Start both servers** (backend on :8000, frontend on :3000)
2. **Open the application** in your browser at `http://localhost:3000`
3. **Paste a job description** in the left panel textarea
4. **Upload a PDF resume** using the file input
5. **Click "SCREEN RESUME"** to get AI-powered analysis
6. **View results** in the right panel with match score and detailed analysis

## Sample Data

Use the sample job description in `backend/dataset/sample_job_description.txt` for testing.

Place sample resume PDFs in `backend/dataset/resumes/` directory for testing purposes.

## Design System

The application follows a brutalist design philosophy:

- **Typography**: Monospace fonts only (Courier New)
- **Colors**: Pure black (#000000), white (#FFFFFF), light gray (#F5F5F5)
- **Borders**: 4px solid black on all interactive elements
- **Layout**: CSS Grid with 50/50 split panels
- **Text**: UPPERCASE for all headings
- **Buttons**: Black background with white text, instant color inversion on hover
- **No**: border-radius, gradients, smooth transitions, or shadows

## Error Handling

The application includes comprehensive error handling for:

- Invalid PDF files
- Network connectivity issues
- AI service failures
- File upload errors
- Backend unavailability

## Development

### Backend Development

- FastAPI with automatic OpenAPI documentation at `/docs`
- Structured logging for debugging
- Environment-based configuration
- Modular architecture with separate parser and AI modules

### Frontend Development

- React with functional components and hooks
- Tailwind CSS for styling
- API service abstraction
- Real-time status monitoring

## Deployment

This project includes comprehensive CI/CD setup for deployment to GitHub Pages (frontend) and various backend hosting services.

### Quick Deployment

1. Push your code to GitHub
2. Configure GitHub Pages in repository settings
3. Deploy backend to Railway, Render, or Vercel
4. Update frontend environment variables with backend URL

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Live Demo

- **Frontend**: [https://praciller.github.io/ai-resume-matcher](https://praciller.github.io/ai-resume-matcher)
- **Backend**: Deploy using the provided configurations

## Troubleshooting

### Backend Issues

- Ensure Python dependencies are installed: `pip install -r requirements.txt`
- Check that the Gemini API key is valid
- Verify the server is running on port 8000

### Frontend Issues

- Ensure Node.js dependencies are installed: `npm install`
- Check that the backend is running and accessible
- Verify CORS configuration allows frontend origin

### Common Errors

- **"BACKEND SERVER IS NOT RUNNING"**: Start the FastAPI server
- **"ONLY PDF FILES ARE SUPPORTED"**: Upload a valid PDF file
- **"FAILED TO EXTRACT TEXT FROM PDF"**: Try a different PDF file
- **"UNABLE TO CONNECT TO SERVER"**: Check backend server status

### Deployment Issues

- Check GitHub Actions logs for CI/CD errors
- Verify environment variables are correctly set
- Ensure API keys are valid and properly configured
- See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed troubleshooting
