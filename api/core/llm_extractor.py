"""
Gemini AI integration for resume data extraction and job matching.
"""
import json
import os
from typing import Dict, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)


def extract_resume_data(resume_text: str) -> Dict[str, Any]:
    """
    Extract structured data from resume text using Gemini AI.
    
    Args:
        resume_text: Raw text extracted from resume PDF
        
    Returns:
        dict: Structured resume data with skills, experience, education, etc.
        
    Raises:
        Exception: If AI extraction fails
    """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        prompt = f"""
        Extract structured information from the following resume text and return ONLY a valid JSON object with no additional text.

        Required JSON structure:
        {{
            "skills": ["skill1", "skill2", ...],
            "experience_years": number,
            "education": ["degree1", "degree2", ...],
            "previous_roles": ["role1", "role2", ...],
            "key_achievements": ["achievement1", "achievement2", ...],
            "contact_info": {{
                "name": "string",
                "email": "string",
                "phone": "string"
            }}
        }}

        Instructions:
        - Extract all technical and soft skills mentioned
        - Calculate total years of professional experience
        - List all educational qualifications
        - Include all job titles/roles held
        - Extract key achievements and accomplishments
        - Extract contact information if available
        - If information is not available, use empty arrays or null values
        - Return ONLY the JSON object, no explanations or additional text

        Resume text:
        {resume_text}

        JSON Response:"""
        
        response = model.generate_content(prompt)
        
        # Parse the JSON response
        response_text = response.text.strip()

        # Try to extract JSON from response if it contains extra text
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        elif response_text.startswith('```'):
            response_text = response_text.replace('```', '').strip()

        # Find JSON object in response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            response_text = response_text[start_idx:end_idx]

        resume_data = json.loads(response_text)
        
        # Validate required fields
        required_fields = ["skills", "experience_years", "education", "previous_roles", "key_achievements"]
        for field in required_fields:
            if field not in resume_data:
                resume_data[field] = [] if field != "experience_years" else 0
        
        return resume_data
        
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse AI response as JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Error extracting resume data: {str(e)}")


def compare_resume_to_jd(resume_data: Dict[str, Any], jd_text: str) -> Dict[str, Any]:
    """
    Compare resume data against job description and generate match score.
    
    Args:
        resume_data: Structured resume data from extract_resume_data
        jd_text: Job description text
        
    Returns:
        dict: Match analysis with score and summary
        
    Raises:
        Exception: If AI comparison fails
    """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        prompt = f"""
        Compare the following resume data against the job description and provide a detailed match analysis. Return ONLY a valid JSON object with no additional text.

        Resume Data:
        {json.dumps(resume_data, indent=2)}

        Job Description:
        {jd_text}

        Provide your analysis in the following JSON format:
        {{
            "match_score": number (0-100),
            "match_summary": "detailed explanation of the match",
            "skill_matches": ["matched skills"],
            "skill_gaps": ["missing skills"],
            "experience_match": "analysis of experience alignment",
            "education_match": "analysis of education requirements",
            "overall_recommendation": "hire/consider/reject with reasoning"
        }}

        Scoring criteria:
        - Skills match (40%): How many required skills does the candidate have?
        - Experience level (30%): Does experience years and roles align with requirements?
        - Education (20%): Does education meet the job requirements?
        - Overall fit (10%): General alignment with job responsibilities

        Be thorough in your analysis and provide specific examples.
        Return ONLY the JSON object, no explanations or additional text.

        JSON Response:"""
        
        response = model.generate_content(prompt)
        
        # Parse the JSON response
        response_text = response.text.strip()

        # Try to extract JSON from response if it contains extra text
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        elif response_text.startswith('```'):
            response_text = response_text.replace('```', '').strip()

        # Find JSON object in response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            response_text = response_text[start_idx:end_idx]

        match_analysis = json.loads(response_text)
        
        # Validate and ensure required fields
        if "match_score" not in match_analysis:
            match_analysis["match_score"] = 0
        if "match_summary" not in match_analysis:
            match_analysis["match_summary"] = "Unable to generate match summary"
        
        # Ensure match_score is within valid range
        match_analysis["match_score"] = max(0, min(100, int(match_analysis["match_score"])))
        
        return match_analysis
        
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse AI response as JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Error comparing resume to job description: {str(e)}")


def test_gemini_connection() -> bool:
    """
    Test if Gemini AI connection is working.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content("Hello, respond with 'OK' if you can hear me.")
        return "OK" in response.text.upper()
    except:
        return False
