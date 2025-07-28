"""
Test script for the Resume Screener API
"""
import requests
import json

# Test configuration
API_BASE_URL = "http://localhost:8000"
SAMPLE_JD = """
Senior Software Engineer - Full Stack Development

We are seeking a highly skilled Senior Software Engineer with 5+ years of experience.

Required Skills:
- JavaScript, Python, React.js
- Node.js and Express.js
- AWS cloud platform experience
- Docker and Kubernetes
- RESTful API development
- Bachelor's degree in Computer Science

Responsibilities:
- Design and develop scalable web applications
- Lead technical projects and mentor junior developers
- Collaborate with cross-functional teams
- Optimize application performance
"""

def test_health_endpoint():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Health Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_text_extraction():
    """Test text extraction with sample text"""
    print("\nTesting text-based resume analysis...")
    try:
        # Read sample resume text
        with open("test_resume_text.txt", "r") as f:
            resume_text = f.read()
        
        # Test the LLM extractor directly
        from core.llm_extractor import extract_resume_data, compare_resume_to_jd
        
        print("Extracting resume data...")
        resume_data = extract_resume_data(resume_text)
        print("Resume data extracted successfully:")
        print(json.dumps(resume_data, indent=2))
        
        print("\nComparing to job description...")
        match_result = compare_resume_to_jd(resume_data, SAMPLE_JD)
        print("Match analysis completed:")
        print(json.dumps(match_result, indent=2))
        
        return True
        
    except Exception as e:
        print(f"Text extraction test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Resume Screener API Tests ===\n")
    
    # Test 1: Health check
    health_ok = test_health_endpoint()
    
    # Test 2: Text extraction and analysis
    text_ok = test_text_extraction()
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"Health Check: {'✓ PASS' if health_ok else '✗ FAIL'}")
    print(f"Text Analysis: {'✓ PASS' if text_ok else '✗ FAIL'}")
    
    if health_ok and text_ok:
        print("\n🎉 All tests passed! The application is ready for use.")
        print("\nNext steps:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Paste the sample job description")
        print("3. Upload a PDF resume to test the full workflow")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
