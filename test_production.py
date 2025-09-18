#!/usr/bin/env python3
"""
Test the production deployment with a real resume screening request
"""

import requests
import json

def test_production_api():
    """Test the production API with your job description"""
    print("Testing Production AI Resume Matcher")
    print("=" * 50)
    
    # Your job description
    job_description = """Fullstack Developer
At Kapara, we are focused on aggregating data and building a unique dashboard in the financial markets. We are looking to hire a Fullstack Developer (BackEnd & FrontEnd) to join us as in a full time role.

You must have full working rights in Thailand and able to work at our Old City Chiang Mai office. 

As a Fullstack Engineer at Kapara, you will coordinate cross-functionally with a team of front end & backend developers & graphic designers to design, develop, and maintain the frontend & backend systems that power our applications.

Required Experience:
- Robust, performant, modular, clean, and maintainable code
- Strong communication skills
- Strong participation in code reviews
- Experience with Linux based operating systems (or Mac)
- 2-4+ years of experience"""
    
    # Create a simple text file to simulate a resume
    resume_content = """John Doe
Software Developer

EXPERIENCE:
- 3 years of full-stack development
- Built e-commerce platforms using React and Node.js
- Developed data analytics dashboards
- Experience with Python, JavaScript, SQL, Docker

EDUCATION:
- Bachelor's in Computer Science

SKILLS:
- Python, JavaScript, React, Node.js
- SQL, Docker, AWS, Git
- Linux/Unix systems
- Agile development"""
    
    # Save as a temporary text file (simulating PDF content)
    with open("temp_resume.txt", "w") as f:
        f.write(resume_content)
    
    try:
        print("Sending request to production API...")
        
        # Test the health endpoint first
        health_response = requests.get("https://ai-resume-matcher-chi.vercel.app/api/health")
        print(f"Health Status: {health_response.status_code}")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"AI Available: {health_data.get('ai_available', 'unknown')}")
            print(f"Gemini AI: {health_data.get('gemini_ai', 'unknown')}")
        
        print("\nTesting resume screening...")
        
        # Prepare the multipart form data
        files = {
            'resume': ('resume.txt', open('temp_resume.txt', 'rb'), 'text/plain')
        }
        data = {
            'jobDescription': job_description
        }
        
        # Send the request
        response = requests.post(
            "https://ai-resume-matcher-chi.vercel.app/api/screen-resume",
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\nMATCH SCORE: {result.get('match_score', 'N/A')}/100")
            print(f"\nSUMMARY:")
            print(result.get('match_summary', 'N/A'))
            
            detailed = result.get('detailed_analysis', {})
            if detailed:
                skills_matched = detailed.get('skill_matches', [])
                skills_gaps = detailed.get('skill_gaps', [])
                
                if skills_matched:
                    print(f"\nSKILLS MATCHED: {', '.join(skills_matched[:5])}")
                if skills_gaps:
                    print(f"SKILL GAPS: {', '.join(skills_gaps[:5])}")
                
                if detailed.get('experience_match'):
                    print(f"\nEXPERIENCE: {detailed.get('experience_match')}")
                
                if detailed.get('overall_recommendation'):
                    print(f"\nRECOMMENDATION: {detailed.get('overall_recommendation')}")
            
            # Check if this is real AI analysis or fallback
            if result.get('match_score') == 50 and 'AI service error' in result.get('match_summary', ''):
                print("\n⚠️  WARNING: Getting fallback response - API key may not be configured in production")
            else:
                print("\n✅ SUCCESS: Real AI analysis working in production!")
                
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error testing production: {e}")
    
    finally:
        # Clean up
        try:
            import os
            os.remove("temp_resume.txt")
        except:
            pass

if __name__ == "__main__":
    test_production_api()
