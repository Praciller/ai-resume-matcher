# 🤖 AI Resume Matcher

> **Intelligent Resume Screening with Google Gemini AI**

A modern, AI-powered resume screening application that analyzes resumes against job descriptions using Google's Gemini AI. Built with React, FastAPI, and shadcn/ui for a seamless user experience.

![AI Resume Matcher](https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge&logo=google&logoColor=white)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=for-the-badge&logo=fastapi&logoColor=white)

## ✨ Features

- **🧠 AI-Powered Analysis**: Leverages Google Gemini AI for intelligent resume-job matching
- **📊 Match Scoring**: Provides detailed compatibility scores (0-100)
- **🎯 Skill Analysis**: Identifies matched skills and skill gaps
- **📱 Modern UI**: Built with shadcn/ui and Tailwind CSS for a beautiful, responsive design
- **🔍 Detailed Insights**: Comprehensive analysis with actionable recommendations
- **⚡ Real-time Processing**: Fast PDF parsing and analysis
- **🧪 Comprehensive Testing**: E2E, integration, and unit tests with Playwright and Jest

## Architecture

### Backend (FastAPI)

- **PDF Processing**: Extract text from PDF files using pypdf
- **AI Integration**: Google Gemini 2.0 Flash for structured data extraction and matching
- **RESTful API**: FastAPI endpoints with proper error handling and CORS support

### Frontend (React)

- **Modern Design**: shadcn/ui components with Scaled theme
- **Responsive Layout**: Card-based design that adapts to all screen sizes
- **Real-time Status**: Backend connection monitoring with visual indicators
- **File Upload**: Intuitive PDF resume upload with validation
- **Accessibility**: WCAG compliant components with proper ARIA labels

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

## 🧪 Testing

The application includes comprehensive testing infrastructure:

### Test Suites

- **E2E Tests (Playwright)**: Browser automation testing across Chrome, Firefox, and Safari
- **Integration Tests (Jest)**: API service integration testing
- **Unit Tests (Jest)**: Component and function behavior testing

### Running Tests

```bash
cd frontend

# Run all tests
npm run test:all

# Individual test suites
npm run test:e2e          # Playwright E2E tests
npm run test:unit         # Jest unit tests
npm run test:integration  # Jest integration tests
npm run test:coverage     # Generate coverage report

# Interactive test modes
npm run test:e2e:ui       # Playwright UI mode
npm test                  # Jest watch mode
```

### Test Coverage

The project maintains high test coverage with:

- Component rendering and interaction tests
- API service error handling tests
- Cross-browser compatibility tests
- Accessibility compliance tests
- Responsive design tests

## 🎨 Design System

The application uses **shadcn/ui** with the **Scaled** theme, featuring:

- **Modern Card-based Layout**: Clean, organized interface with proper spacing
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Dark/Light Mode Support**: Automatic theme switching based on system preferences
- **Accessible Components**: WCAG compliant UI elements with proper focus management
- **Smooth Animations**: Polished user interactions with subtle transitions
- **Typography**: Clean, readable fonts with proper hierarchy
- **Color System**: Semantic color tokens for consistent theming

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

This project supports multiple deployment options with built-in authentication.

### Vercel Deployment (Recommended)

Deploy the full-stack application to Vercel with GitHub authentication:

1. **Quick Setup**:

   ```bash
   node deploy-to-vercel.js  # Check deployment readiness
   ```

2. **Deploy to Vercel**:
   - Connect your GitHub repository to Vercel
   - Set up Supabase for GitHub OAuth
   - Configure environment variables
   - Deploy!

For detailed instructions, see [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md).

### Alternative Deployments

- **Frontend**: GitHub Pages, Netlify, or Vercel
- **Backend**: Railway, Render, or Heroku

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
#   D e p l o y m e n t   t r i g g e r   -   0 9 / 2 8 / 2 0 2 5   0 5 : 1 6 : 4 6  
 