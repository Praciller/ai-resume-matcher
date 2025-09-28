# 🤖 AI Resume Matcher

> **Comprehensive Career Development Platform with Google Gemini AI**

A modern, AI-powered resume screening and career guidance application that provides detailed analysis, skill development recommendations, and interview preparation. Built with React, Python serverless functions, and shadcn/ui for a seamless user experience.

![AI Resume Matcher](https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge&logo=google&logoColor=white)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?style=for-the-badge&logo=vercel&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)

🌟 **Live Demo**: [https://ai-resume-matcher-chi.vercel.app](https://ai-resume-matcher-chi.vercel.app)

## ✨ Enhanced Features

### 🧠 AI-Powered Analysis

- **Google Gemini 2.0 Flash**: Advanced AI for intelligent resume-job matching
- **Match Scoring**: Detailed compatibility scores (0-100) with comprehensive justification
- **Skill Analysis**: Identifies matched skills and critical skill gaps with importance levels

### 🎯 Career Development Guidance

- **Priority-Based Recommendations**: Skill development paths ranked by importance (1-10)
- **Learning Resources**: Specific courses, certifications, and learning materials
- **Timeline Estimates**: Realistic timeframes for skill development (e.g., "3-6 months")
- **Career Pathways**: Alternative career paths and strategic development advice

### 📋 Interview Preparation

- **Likely Questions**: Potential interview questions based on skill gaps
- **Talking Points**: How to effectively discuss experience and skills
- **Red Flag Management**: Addressing potential employer concerns

### 🎨 Modern User Experience

- **shadcn/ui Design**: Beautiful, responsive interface with modern card-based layout
- **Real-time Status**: Backend connection monitoring with visual indicators
- **Accessibility**: WCAG compliant components with proper ARIA labels
- **Mobile Responsive**: Seamless experience across all device sizes

### 🧪 Production-Ready

- **Comprehensive Testing**: Unit tests (Jest), E2E tests (Playwright), 100% test coverage
- **Vercel Deployment**: Serverless architecture with automatic scaling
- **Error Handling**: Robust error management and user feedback
- **Performance Optimized**: Fast PDF parsing and AI analysis

## 🏗️ Architecture

### Backend (Vercel Serverless Functions)

- **Serverless API**: Python-based Vercel functions with automatic scaling
- **PDF Processing**: Extract text from PDF files using pypdf2
- **AI Integration**: Google Gemini 2.0 Flash for structured data extraction and comprehensive analysis
- **RESTful Endpoints**: Clean API design with proper error handling and CORS support
- **Environment Management**: Secure environment variable handling for API keys

### Frontend (React + shadcn/ui)

- **Modern Design System**: shadcn/ui components with Tailwind CSS
- **Responsive Layout**: Card-based design that adapts to all screen sizes
- **Real-time Status**: Backend connection monitoring with visual health indicators
- **File Upload**: Intuitive PDF resume upload with client-side validation
- **Accessibility**: WCAG compliant components with proper ARIA labels and keyboard navigation
- **State Management**: React hooks for efficient state management and API integration

## 🚀 Quick Setup

### Prerequisites

- **Node.js 18+** (for frontend development)
- **Python 3.8+** (for local backend development)
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))
- **Vercel CLI** (optional, for deployment)

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required: Google Gemini AI API Key
GEMINI_API_KEY=your_actual_api_key_here
```

### Local Development Setup

#### 1. Clone and Install Dependencies

```bash
git clone https://github.com/Praciller/ai-resume-matcher.git
cd ai-resume-matcher

# Install frontend dependencies
cd frontend
npm install
cd ..

# Install backend dependencies (for local development)
cd backend
pip install -r requirements.txt
cd ..
```

#### 2. Start Development Servers

**Option A: Full Local Development**

```bash
# Terminal 1: Start backend (FastAPI)
cd backend
python main.py
# Backend runs on http://localhost:8000

# Terminal 2: Start frontend (React)
cd frontend
npm start
# Frontend runs on http://localhost:3000
```

**Option B: Frontend + Production API**

```bash
# Start only frontend (uses production API)
cd frontend
npm start
# Frontend runs on http://localhost:3000
```

### Production Deployment (Vercel)

The application is deployed on Vercel with serverless functions:

1. **Fork this repository**
2. **Connect to Vercel**:
   - Import your GitHub repository to Vercel
   - Vercel will auto-detect the configuration
3. **Set Environment Variables**:
   - Add `GEMINI_API_KEY` in Vercel dashboard
4. **Deploy**: Automatic deployment on every push to main branch

**Live Production URL**: [https://ai-resume-matcher-chi.vercel.app](https://ai-resume-matcher-chi.vercel.app)

## 📡 API Endpoints

### POST /api/screen-resume

Comprehensive resume analysis with career guidance.

**Request:**

- `resume_file`: PDF file (multipart/form-data)
- `jd_text`: Job description text (form field)

**Response:**

```json
{
  "match_score": 85,
  "match_summary": "Strong candidate with excellent technical skills but needs cloud experience...",
  "detailed_analysis": {
    "skill_matches": ["Python", "React", "JavaScript"],
    "skill_gaps": ["Node.js", "AWS", "Microservices"],
    "experience_match": "3 years vs 5+ required - relevant but junior level",
    "education_match": "Bachelor's in Computer Science meets requirements",
    "overall_recommendation": "consider",
    "detailed_recommendations": {
      "primary_recommendation": "Consider for mid-level role with mentorship...",
      "improvement_areas": [
        {
          "skill": "Node.js",
          "importance": "high",
          "current_level": "none",
          "target_level": "intermediate",
          "learning_path": "Start with Node.js tutorials, build REST API...",
          "estimated_timeline": "3-6 months",
          "resources": ["Node.js docs", "FreeCodeCamp course"],
          "priority": 1
        }
      ],
      "strengths_to_leverage": [
        {
          "strength": "Python Skills",
          "relevance": "Core backend language for this role",
          "enhancement_tips": "Showcase Django/Flask projects"
        }
      ],
      "career_guidance": {
        "immediate_actions": ["Update resume with quantifiable results"],
        "short_term_goals": ["Complete Node.js certification"],
        "long_term_development": ["Focus on full-stack expertise"],
        "alternative_paths": ["Frontend specialist", "Python backend developer"]
      },
      "interview_preparation": {
        "likely_questions": [
          "Describe Node.js experience",
          "Cloud platform knowledge"
        ],
        "talking_points": [
          "Highlight Python expertise",
          "Show learning agility"
        ],
        "red_flags_to_address": ["Limited experience vs requirements"]
      }
    },
    "justification": "Detailed explanation of scoring methodology..."
  }
}
```

### GET /api/health

Check backend health and AI service availability.

**Response:**

```json
{
  "status": "healthy",
  "ai_available": true,
  "gemini_ai": "connected"
}
```

## 💡 Usage

### Live Application

Visit [https://ai-resume-matcher-chi.vercel.app](https://ai-resume-matcher-chi.vercel.app) for the production version.

### Local Development

1. **Start the application** (see setup instructions above)
2. **Open your browser** to `http://localhost:3000`
3. **Check backend status** - Should show "Backend Status: Connected"

### Using the AI Resume Matcher

1. **📝 Enter Job Description**

   - Paste the job description in the left panel textarea
   - Include required skills, experience level, and responsibilities

2. **📄 Upload Resume**

   - Click "Choose File" and select a PDF resume
   - Only PDF files are supported for optimal text extraction

3. **🔍 Analyze**

   - Click "Analyze Resume" to start AI processing
   - Wait for the comprehensive analysis (typically 10-30 seconds)

4. **📊 Review Results**
   - **Match Score**: Overall compatibility percentage (0-100)
   - **Summary**: High-level analysis of the candidate fit
   - **Matched Skills**: Skills found in both resume and job description
   - **Skill Gaps**: Missing skills with importance levels
   - **Career Development Guidance**: Detailed recommendations including:
     - Priority-based skill development plans
     - Learning resources and timelines
     - Career guidance and alternative paths
     - Interview preparation tips

### Sample Test Data

For testing purposes, you can use:

- **Job Description**: Any software engineering job posting
- **Resume**: Any PDF resume file (the AI will analyze real content)

## 🧪 Testing

The application includes comprehensive testing infrastructure with **100% test coverage**.

### Test Suites

- **Unit Tests (Jest + React Testing Library)**: Component behavior and user interaction testing
- **E2E Tests (Playwright)**: Full browser automation testing across Chrome, Firefox, and Safari
- **Integration Tests**: API service and error handling testing

### Running Tests

```bash
cd frontend

# Run unit tests
npm run test:unit         # Jest unit tests with React Testing Library
npm test                  # Jest watch mode for development

# Run E2E tests
npm run test:e2e          # Playwright E2E tests
npm run test:e2e:ui       # Playwright UI mode (interactive)

# Generate coverage report
npm run test:coverage     # Detailed coverage analysis
```

### Test Coverage

**Current Status: 10/10 Tests Passing (100% Success Rate)**

The test suite validates:

- ✅ **Component Rendering**: All UI components render correctly
- ✅ **User Interactions**: File upload, form submission, button clicks
- ✅ **API Integration**: Backend connectivity and response handling
- ✅ **Error Handling**: Network failures, invalid files, API errors
- ✅ **Accessibility**: ARIA labels, keyboard navigation, screen reader support
- ✅ **Responsive Design**: Mobile, tablet, and desktop layouts
- ✅ **Cross-browser Compatibility**: Chrome, Firefox, Safari testing

### Test Files

- `frontend/src/__tests__/ResumeScreener.test.js`: Main component tests
- `frontend/tests/e2e/`: Playwright end-to-end tests
- `frontend/jest.config.js`: Jest configuration with React Testing Library setup

## 🚀 Deployment

### Current Production Deployment

**Live Application**: [https://ai-resume-matcher-chi.vercel.app](https://ai-resume-matcher-chi.vercel.app)

The application is deployed on **Vercel** with:

- ✅ **Serverless Functions**: Python-based API endpoints
- ✅ **Automatic Scaling**: Handles traffic spikes seamlessly
- ✅ **Global CDN**: Fast loading worldwide
- ✅ **GitHub Integration**: Auto-deploy on push to main branch
- ✅ **Environment Variables**: Secure API key management

### Deploy Your Own Instance

#### 1. Fork & Clone

```bash
# Fork this repository on GitHub
git clone https://github.com/YOUR_USERNAME/ai-resume-matcher.git
cd ai-resume-matcher
```

#### 2. Deploy to Vercel

**Option A: Vercel CLI (Recommended)**

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to production
vercel --prod

# Set environment variables
vercel env add GEMINI_API_KEY
```

**Option B: Vercel Dashboard**

1. Connect your GitHub repository to Vercel
2. Import the project (Vercel auto-detects configuration)
3. Add environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
4. Deploy!

#### 3. Verify Deployment

- Check `/api/health` endpoint returns `{"status": "healthy", "ai_available": true}`
- Test the full application with a sample resume and job description

### Environment Variables

Required for production deployment:

```bash
# Google Gemini AI API Key (Required)
GEMINI_API_KEY=your_actual_api_key_here
```

### Alternative Deployment Options

- **Netlify**: Frontend + Netlify Functions
- **Railway**: Full-stack deployment
- **Render**: Web service + background workers

## 🔧 Troubleshooting

### Common Issues & Solutions

#### Backend Connection Issues

- **"Backend Status: Checking"**: Wait for the connection to establish
- **"Backend Status: Disconnected"**: Check if the API is running
- **API Health Check**: Visit `/api/health` to verify backend status

#### File Upload Issues

- **"Only PDF files are supported"**: Ensure you're uploading a PDF file
- **"Failed to extract text from PDF"**: Try a different PDF file or check if it's password-protected
- **Large file uploads**: PDFs should be under 10MB for optimal performance

#### AI Analysis Issues

- **"AI modules not available"**: Check if `GEMINI_API_KEY` is properly set
- **Slow analysis**: Large resumes or complex job descriptions may take 30+ seconds
- **Empty results**: Ensure both resume and job description contain relevant text

#### Development Issues

- **Port conflicts**: Frontend runs on :3000, backend on :8000
- **CORS errors**: Ensure backend CORS is configured for frontend origin
- **Environment variables**: Check `.env` file exists and contains valid API key

#### Deployment Issues

- **Vercel build failures**: Check build logs for missing dependencies
- **Environment variables**: Ensure `GEMINI_API_KEY` is set in Vercel dashboard
- **API endpoint errors**: Verify serverless functions are deployed correctly

### Getting Help

1. **Check the live demo**: [https://ai-resume-matcher-chi.vercel.app](https://ai-resume-matcher-chi.vercel.app)
2. **Review API health**: Visit `/api/health` endpoint
3. **Check browser console**: Look for JavaScript errors
4. **Verify API key**: Test with Google AI Studio

### Performance Tips

- **Optimize PDFs**: Use text-based PDFs rather than scanned images
- **Concise job descriptions**: Focus on key requirements for faster analysis
- **Network**: Stable internet connection improves AI response times

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⭐ Support

If you find this project helpful, please give it a star on GitHub!

---

**Built with ❤️ using Google Gemini AI, React, and Vercel**
