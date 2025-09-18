#!/usr/bin/env python3
"""
Local development server for AI Resume Matcher
Run this to test the full system locally with real file uploads
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Load environment variables
load_dotenv()

# Import our AI modules
try:
    from core.parser import parse_pdf_to_text, validate_pdf_file
    from core.llm_extractor import extract_resume_data, compare_resume_to_jd, test_gemini_api
    AI_AVAILABLE = True
    print("OK AI modules loaded successfully")
except Exception as e:
    print(f"FAIL Failed to load AI modules: {e}")
    AI_AVAILABLE = False

# Create FastAPI app
app = FastAPI(title="AI Resume Matcher", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    response = {
        "status": "healthy",
        "ai_available": AI_AVAILABLE,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "has_gemini_key": bool(os.getenv("GEMINI_API_KEY"))
    }
    
    if AI_AVAILABLE:
        try:
            gemini_status = test_gemini_api()
            response["gemini_ai"] = gemini_status.get("status", "unknown")
            response["gemini_message"] = gemini_status.get("message", "")
        except Exception as e:
            response["gemini_ai"] = f"error: {str(e)}"
    else:
        response["gemini_ai"] = "modules not loaded"
    
    return response

@app.post("/api/screen-resume")
async def screen_resume(
    jobDescription: str = Form(...),
    resume: UploadFile = File(...)
):
    """Screen resume against job description"""
    
    if not AI_AVAILABLE:
        return JSONResponse({
            "match_score": 0,
            "match_summary": "AI processing modules are not available",
            "detailed_analysis": {
                "skill_matches": [],
                "skill_gaps": [],
                "experience_match": "AI modules not loaded",
                "education_match": "AI modules not loaded",
                "overall_recommendation": "Cannot process - server configuration issue"
            }
        })
    
    try:
        # Read the uploaded file
        resume_content = await resume.read()
        
        # Validate if it's a PDF (basic check)
        if not validate_pdf_file(resume_content):
            # If not PDF, treat as text file for testing
            resume_text = resume_content.decode('utf-8', errors='ignore')
        else:
            # Parse PDF to text
            resume_text = parse_pdf_to_text(resume_content)
        
        # Extract structured data from resume
        resume_data = extract_resume_data(resume_text)
        
        # Compare resume to job description
        comparison_result = compare_resume_to_jd(resume_data, jobDescription)
        
        # Format response
        response = {
            "match_score": comparison_result.get("match_score", 0),
            "match_summary": comparison_result.get("match_summary", "Analysis completed"),
            "detailed_analysis": {
                "skill_matches": comparison_result.get("skill_matches", []),
                "skill_gaps": comparison_result.get("skill_gaps", []),
                "experience_match": comparison_result.get("experience_match", ""),
                "education_match": comparison_result.get("education_match", ""),
                "overall_recommendation": comparison_result.get("overall_recommendation", "")
            }
        }
        
        return response
        
    except Exception as e:
        return JSONResponse({
            "match_score": 0,
            "match_summary": f"Processing failed: {str(e)}",
            "detailed_analysis": {
                "skill_matches": [],
                "skill_gaps": [],
                "experience_match": "Error during processing",
                "education_match": "Error during processing", 
                "overall_recommendation": "Unable to complete analysis - please try again"
            }
        })

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AI Resume Matcher API is running", "version": "1.0.0"}

def main():
    """Run the local development server"""
    print("Starting AI Resume Matcher Local Server")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_actual_gemini_api_key_here':
        print("WARNING: GEMINI_API_KEY not set properly")
        print("Please check your .env file")
    else:
        print("OK Gemini API key configured")

    print(f"OK AI modules available: {AI_AVAILABLE}")
    print("\nServer will be available at:")
    print("   http://localhost:8000")
    print("   http://localhost:8000/api/health")
    print("   http://localhost:8000/api/screen-resume")
    print("\nTo test:")
    print("   1. Open http://localhost:8000/api/health in browser")
    print("   2. Use the frontend or curl to test resume screening")
    print("   3. Press Ctrl+C to stop the server")
    print("\n" + "=" * 50)
    
    # Run the server
    uvicorn.run(
        "run_local_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
