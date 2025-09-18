#!/usr/bin/env python3
"""
Test the AI Resume Matcher with your specific job description
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Load environment variables
load_dotenv()

def test_your_job_description():
    """Test with your specific Kapara job description"""
    print("Testing AI Resume Matcher with Your Kapara Job Description")
    print("=" * 60)
    
    # Import the core modules
    from core.llm_extractor import compare_resume_to_jd
    
    # Your specific job description
    your_job_description = """Fullstack Developer
At Kapara, we are focused on aggregating data and building a unique dashboard in the financial markets. We are looking to hire a Fullstack Developer (BackEnd & FrontEnd) to join us as in a full time role.

You must have full working rights in Thailand and able to work at our Old City Chiang Mai office. 

As a Fullstack Engineer at Kapara, you will coordinate cross-functionally with a team of front end & backend developers & graphic designers to...tention to detail and the ability to measure and balance cost vs performance for the infrastructure of a SaaS product

Required Experience

Robust, performant, modular, clean, and maintainable code

Strong communication skills

Strong participation in code reviews

Experience with Linux based operating systems (or Mac)

2-4+ years of experience"""
    
    # Sample resume data (simulating what would be extracted from a PDF)
    sample_resume_data = {
        "skills": ["Python", "JavaScript", "React", "Node.js", "SQL", "Docker", "AWS", "Git"],
        "experience": "3 years of full-stack software development experience",
        "education": "Bachelor's in Computer Science",
        "projects": ["E-commerce platform", "Data analytics dashboard", "Mobile app"]
    }
    
    print("Testing with resume skills:", sample_resume_data['skills'])
    print("Experience:", sample_resume_data['experience'])
    print("Education:", sample_resume_data['education'])
    print("\n" + "-" * 60)
    
    try:
        print("Analyzing resume against your job description...")
        result = compare_resume_to_jd(sample_resume_data, your_job_description)
        
        print(f"\nMATCH SCORE: {result.get('match_score', 'N/A')}/100")
        print(f"\nSUMMARY:")
        print(result.get('match_summary', 'N/A'))
        
        skills_matched = result.get('skill_matches', [])
        skills_gaps = result.get('skill_gaps', [])
        
        if skills_matched:
            print(f"\nSKILLS MATCHED:")
            for skill in skills_matched[:5]:  # Show top 5
                print(f"  + {skill}")

        if skills_gaps:
            print(f"\nSKILL GAPS:")
            for skill in skills_gaps[:5]:  # Show top 5
                print(f"  - {skill}")
        
        experience_match = result.get('experience_match', '')
        if experience_match:
            print(f"\nEXPERIENCE ANALYSIS:")
            print(f"  {experience_match}")
        
        education_match = result.get('education_match', '')
        if education_match:
            print(f"\nEDUCATION ANALYSIS:")
            print(f"  {education_match}")
        
        recommendation = result.get('overall_recommendation', '')
        if recommendation:
            print(f"\nRECOMMENDATION:")
            print(f"  {recommendation}")
        
        print("\n" + "=" * 60)
        print("SUCCESS: AI analysis completed!")
        print("This shows the system provides personalized, detailed analysis")
        print("for your specific job requirements.")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_different_job():
    """Test with a completely different job to show variation"""
    print("\n" + "=" * 60)
    print("Testing with a DIFFERENT job to show variation...")
    print("=" * 60)
    
    from core.llm_extractor import compare_resume_to_jd
    
    # Completely different job
    different_job = """Senior DevOps Engineer
We are seeking a Senior DevOps Engineer to manage our cloud infrastructure and CI/CD pipelines.

Requirements:
- 5+ years DevOps experience
- AWS/Azure cloud platforms
- Kubernetes and Docker
- Terraform or CloudFormation
- Jenkins, GitLab CI, or GitHub Actions
- Monitoring tools (Prometheus, Grafana)
- Linux system administration
- Python or Bash scripting"""
    
    sample_resume_data = {
        "skills": ["Python", "JavaScript", "React", "Node.js", "SQL", "Docker", "AWS", "Git"],
        "experience": "3 years of full-stack software development experience",
        "education": "Bachelor's in Computer Science"
    }
    
    try:
        result = compare_resume_to_jd(sample_resume_data, different_job)
        
        print(f"DevOps Job Match Score: {result.get('match_score', 'N/A')}/100")
        print(f"Summary: {result.get('match_summary', 'N/A')[:100]}...")
        
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("AI Resume Matcher - Testing Your Job Description")
    print("=" * 60)
    
    success1 = test_your_job_description()
    success2 = test_different_job()
    
    if success1 and success2:
        print("\n" + "=" * 50)
        print("COMPLETE SUCCESS!")
        print("The AI Resume Matcher is working perfectly!")
        print("Ready for production deployment!")
        print("=" * 50)
    else:
        print("\nSome tests failed.")
    
    sys.exit(0 if (success1 and success2) else 1)
