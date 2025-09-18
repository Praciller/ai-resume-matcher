#!/usr/bin/env python3
"""
Final test of production deployment
"""

import requests
import json

def test_production():
    """Test the production deployment"""
    print("Testing Production AI Resume Matcher")
    print("=" * 50)
    
    # Your job description
    job_description = """Fullstack Developer
At Kapara, we are focused on aggregating data and building a unique dashboard in the financial markets. We are looking to hire a Fullstack Developer (BackEnd & FrontEnd) to join us as in a full time role.

Required Experience:
- Robust, performant, modular, clean, and maintainable code
- Strong communication skills
- Strong participation in code reviews
- Experience with Linux based operating systems (or Mac)
- 2-4+ years of experience"""
    
    # Sample resume
    resume_content = """John Doe - Software Developer

EXPERIENCE:
3 years of full-stack development experience
Built e-commerce platforms using React and Node.js
Developed data analytics dashboards for financial data
Experience with Python, JavaScript, SQL, Docker, AWS

EDUCATION:
Bachelor's in Computer Science

SKILLS:
Frontend: React, JavaScript, HTML5, CSS3, TypeScript
Backend: Python, Node.js, Express.js, FastAPI
Databases: SQL, PostgreSQL, MongoDB
DevOps: Docker, AWS, Git, Linux"""
    
    # Save resume as text file
    with open("test_resume.txt", "w") as f:
        f.write(resume_content)
    
    try:
        print("1. Testing health endpoint...")
        health_response = requests.get("https://ai-resume-matcher-chi.vercel.app/api/health")
        print(f"   Status: {health_response.status_code}")
        print(f"   Response: {health_response.text}")
        
        print("\n2. Testing resume screening...")
        
        # Test the resume screening endpoint
        files = {'resume': ('resume.txt', open('test_resume.txt', 'rb'), 'text/plain')}
        data = {'jobDescription': job_description}
        
        response = requests.post(
            "https://ai-resume-matcher-chi.vercel.app/api/screen-resume",
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'unknown')}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                
                print(f"\n📊 PRODUCTION RESULTS:")
                print(f"   Match Score: {result.get('match_score')}/100")
                print(f"   Summary: {result.get('match_summary', 'N/A')[:100]}...")
                
                detailed = result.get('detailed_analysis', {})
                if detailed:
                    skills_matched = detailed.get('skill_matches', [])
                    if skills_matched:
                        print(f"   Skills Matched: {', '.join(skills_matched[:3])}")
                
                print("\n✅ SUCCESS: Production deployment is working!")
                print("   Real AI analysis in production!")
                
            except json.JSONDecodeError as e:
                print(f"\n❌ JSON DECODE ERROR: {e}")
                print(f"   Raw response: {response.text[:200]}...")
                print("   This is the 'UNEXPECTED TOKEN' error you mentioned!")
                
        else:
            print(f"\n❌ HTTP ERROR: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"\n❌ REQUEST ERROR: {e}")
    
    finally:
        # Clean up
        try:
            import os
            os.remove("test_resume.txt")
        except:
            pass

if __name__ == "__main__":
    test_production()
