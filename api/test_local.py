#!/usr/bin/env python3
"""
Local test script for AI Resume Matcher
Tests the AI integration without Vercel deployment
"""

import os
import sys
import json
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import google.generativeai as genai
        print("OK google.generativeai imported successfully")
    except ImportError as e:
        print(f"FAIL Failed to import google.generativeai: {e}")
        return False

    try:
        from pypdf import PdfReader
        print("OK pypdf imported successfully")
    except ImportError as e:
        print(f"FAIL Failed to import pypdf: {e}")
        return False

    try:
        from core.parser import parse_pdf_to_text, validate_pdf_file
        print("OK core.parser imported successfully")
    except ImportError as e:
        print(f"FAIL Failed to import core.parser: {e}")
        return False

    try:
        from core.llm_extractor import extract_resume_data, compare_resume_to_jd, test_gemini_api
        print("OK core.llm_extractor imported successfully")
    except ImportError as e:
        print(f"FAIL Failed to import core.llm_extractor: {e}")
        return False
    
    return True

def test_gemini_connection():
    """Test Gemini API connection"""
    print("\nTesting Gemini API connection...")
    
    # Check if API key is set
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_actual_gemini_api_key_here':
        print("FAIL GEMINI_API_KEY not set or using placeholder value")
        print("Please set your actual Gemini API key in the .env file")
        return False

    try:
        from core.llm_extractor import test_gemini_api
        result = test_gemini_api()
        print(f"OK Gemini API test result: {result}")
        return result.get('status') == 'connected'
    except Exception as e:
        print(f"FAIL Gemini API test failed: {e}")
        return False

def test_ai_analysis():
    """Test AI analysis with sample data"""
    print("\nTesting AI analysis with sample data...")
    
    # Sample job descriptions for testing
    job_descriptions = [
        {
            "name": "Fullstack Developer - Kapara",
            "description": """Fullstack Developer
At Kapara, we are focused on aggregating data and building a unique dashboard in the financial markets. We are looking to hire a Fullstack Developer (BackEnd & FrontEnd) to join us as in a full time role.

You must have full working rights in Thailand and able to work at our Old City Chiang Mai office. 

As a Fullstack Engineer at Kapara, you will coordinate cross-functionally with a team of front end & backend developers & graphic designers to design, develop, and maintain the frontend & backend systems that power our applications.

Required Experience:
- React, NextJS Framework, Typescript
- Postgresql, MikroORM
- Golang and Typescript
- APIs: GraphQL, REST
- Knowledge of containerization and orchestration (Docker, Kubernetes)
- Microservices driven architecture
- 2-4+ years of experience"""
        },
        {
            "name": "Python Data Scientist",
            "description": """Python Data Scientist
We are seeking a skilled Python Data Scientist to join our analytics team.

Requirements:
- Strong Python programming skills
- Experience with pandas, numpy, scikit-learn
- Machine learning and statistical analysis
- SQL and database experience
- Data visualization with matplotlib/seaborn
- 3+ years of experience in data science
- PhD or Masters in related field preferred"""
        }
    ]
    
    # Sample resume data (simulated)
    sample_resume_data = {
        "skills": ["Python", "JavaScript", "React", "Node.js", "SQL", "Docker"],
        "experience": "3 years of software development experience",
        "education": "Bachelor's in Computer Science"
    }
    
    try:
        from core.llm_extractor import compare_resume_to_jd
        
        for i, job in enumerate(job_descriptions, 1):
            print(f"\n--- Test {i}: {job['name']} ---")
            result = compare_resume_to_jd(sample_resume_data, job['description'])
            
            print(f"Match Score: {result.get('match_score', 'N/A')}")
            print(f"Summary: {result.get('match_summary', 'N/A')}")
            print(f"Skills Matched: {result.get('skill_matches', [])}")
            print(f"Skill Gaps: {result.get('skill_gaps', [])}")
            
            # Verify different results for different jobs
            if i == 1:
                first_result = result
            elif i == 2:
                if (result.get('match_score') != first_result.get('match_score') or
                    result.get('match_summary') != first_result.get('match_summary')):
                    print("OK Different job descriptions produce different results!")
                else:
                    print("WARN Same results for different job descriptions - may need tuning")
        
        return True
        
    except Exception as e:
        print(f"FAIL AI analysis test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("AI Resume Matcher - Local Testing")
    print("=" * 50)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run tests
    tests_passed = 0
    total_tests = 3
    
    if test_imports():
        tests_passed += 1
    
    if test_gemini_connection():
        tests_passed += 1
    
    if test_ai_analysis():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"Tests completed: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("All tests passed! Ready for deployment.")
        return True
    else:
        print("Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
