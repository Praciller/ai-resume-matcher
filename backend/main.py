"""
FastAPI application for Intelligent Resume Screener.
"""
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from typing import Dict, Any
from dotenv import load_dotenv

from core.parser import parse_pdf_to_text, validate_pdf_file
from core.llm_extractor import extract_resume_data, compare_resume_to_jd, test_gemini_connection

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Intelligent Resume Screener",
    description="AI-powered resume screening and job matching application",
    version="1.0.0"
)

# Get environment variables
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,https://*.vercel.app").split(",")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Configure CORS for production
if ENVIRONMENT == "production":
    # In production, allow Vercel domains and Railway
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for Railway deployment
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )
else:
    # In development, use specific origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Intelligent Resume Screener API", "status": "running"}


@app.get("/health")
async def health_check():
    """Detailed health check including AI service status."""
    try:
        gemini_status = test_gemini_connection()
        return {
            "status": "healthy",
            "gemini_ai": "connected" if gemini_status else "disconnected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )


@app.post("/screen-resume")
async def screen_resume(
    resume_file: UploadFile = File(..., description="PDF resume file"),
    jd_text: str = Form(..., description="Job description text")
) -> Dict[str, Any]:
    """
    Screen a resume against a job description.
    
    Args:
        resume_file: Uploaded PDF resume file
        jd_text: Job description text to match against
        
    Returns:
        dict: Match score and detailed analysis
        
    Raises:
        HTTPException: For various error conditions
    """
    try:
        # Validate file type
        if not resume_file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )
        
        # Read file bytes
        file_bytes = await resume_file.read()
        
        # Validate PDF file
        if not validate_pdf_file(file_bytes):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file or file is corrupted"
            )
        
        # Validate job description
        if not jd_text or len(jd_text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Job description must be at least 10 characters long"
            )
        
        logger.info(f"Processing resume: {resume_file.filename}")
        
        # Step 1: Extract text from PDF
        try:
            resume_text = parse_pdf_to_text(file_bytes)
            logger.info("Successfully extracted text from PDF")
        except Exception as e:
            logger.error(f"PDF parsing failed: {str(e)}")
            raise HTTPException(
                status_code=422,
                detail=f"Failed to extract text from PDF: {str(e)}"
            )
        
        # Step 2: Extract structured data from resume
        try:
            resume_data = extract_resume_data(resume_text)
            logger.info("Successfully extracted resume data using AI")
        except Exception as e:
            logger.error(f"Resume data extraction failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to extract resume data: {str(e)}"
            )
        
        # Step 3: Compare resume to job description
        try:
            match_analysis = compare_resume_to_jd(resume_data, jd_text)
            logger.info(f"Match analysis completed with score: {match_analysis.get('match_score', 0)}")
        except Exception as e:
            logger.error(f"Resume comparison failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to compare resume to job description: {str(e)}"
            )
        
        # Return the required format
        return {
            "match_score": match_analysis.get("match_score", 0),
            "match_summary": match_analysis.get("match_summary", "No summary available"),
            "detailed_analysis": match_analysis  # Include full analysis for debugging
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in screen_resume: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/extract-resume")
async def extract_resume_only(
    resume_file: UploadFile = File(..., description="PDF resume file")
) -> Dict[str, Any]:
    """
    Extract structured data from resume only (for testing purposes).
    
    Args:
        resume_file: Uploaded PDF resume file
        
    Returns:
        dict: Extracted resume data
    """
    try:
        # Validate file type
        if not resume_file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )
        
        # Read and validate file
        file_bytes = await resume_file.read()
        if not validate_pdf_file(file_bytes):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file or file is corrupted"
            )
        
        # Extract text and data
        resume_text = parse_pdf_to_text(file_bytes)
        resume_data = extract_resume_data(resume_text)
        
        return {
            "extracted_data": resume_data,
            "raw_text_preview": resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in extract_resume_only: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract resume data: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
