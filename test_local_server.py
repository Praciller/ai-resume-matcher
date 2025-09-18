#!/usr/bin/env python3
"""
Test the local server with your job description
"""

import requests
import time
import json

def test_local_server():
    """Test the local server"""
    print("Testing Local AI Resume Matcher Server")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
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
    
    # Create a sample resume file
    resume_content = """John Doe
Senior Software Developer

EXPERIENCE:
• 3 years of full-stack development experience
• Built e-commerce platforms using React and Node.js
• Developed data analytics dashboards for financial data
• Experience with Python, JavaScript, SQL, Docker, AWS
• Strong code review participation
• Linux/Unix system administration

EDUCATION:
• Bachelor's in Computer Science
• Relevant coursework in algorithms, databases, web development

SKILLS:
• Frontend: React, JavaScript, HTML5, CSS3, TypeScript
• Backend: Python, Node.js, Express.js, FastAPI
• Databases: SQL, PostgreSQL, MongoDB
• DevOps: Docker, AWS, Git, Linux
• Tools: VS Code, Postman, Jira

PROJECTS:
• E-commerce Platform: Full-stack web application with React frontend and Node.js backend
• Financial Dashboard: Data visualization tool for market analysis
• Mobile App: Cross-platform mobile application using React Native"""
    
    # Save resume as text file
    with open("sample_resume.txt", "w") as f:
        f.write(resume_content)
    
    try:
        print("1. Testing health endpoint...")
        health_response = requests.get(f"{base_url}/api/health", timeout=10)
        print(f"   Status: {health_response.status_code}")
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   AI Available: {health_data.get('ai_available')}")
            print(f"   Gemini AI: {health_data.get('gemini_ai')}")
            print(f"   Has API Key: {health_data.get('has_gemini_key')}")
        
        print("\n2. Testing resume screening...")
        
        # Prepare the request
        files = {
            'resume': ('resume.txt', open('sample_resume.txt', 'rb'), 'text/plain')
        }
        data = {
            'jobDescription': job_description
        }
        
        # Send the request
        response = requests.post(
            f"{base_url}/api/screen-resume",
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n📊 RESULTS:")
            print(f"   Match Score: {result.get('match_score')}/100")
            print(f"   Summary: {result.get('match_summary', 'N/A')[:100]}...")
            
            detailed = result.get('detailed_analysis', {})
            if detailed:
                skills_matched = detailed.get('skill_matches', [])
                skills_gaps = detailed.get('skill_gaps', [])
                
                if skills_matched:
                    print(f"   Skills Matched: {', '.join(skills_matched[:3])}...")
                if skills_gaps:
                    print(f"   Skill Gaps: {', '.join(skills_gaps[:3])}...")
            
            # Check if this is real AI analysis
            if result.get('match_score') != 50 or 'AI service error' not in result.get('match_summary', ''):
                print("\n✅ SUCCESS: Real AI analysis working!")
                print("   The system is providing personalized feedback!")
            else:
                print("\n⚠️  Using fallback response - check API key configuration")
                
        else:
            print(f"   Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to local server")
        print("   Make sure to run: python api/run_local_server.py")
        print("   in another terminal first")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Clean up
        try:
            import os
            os.remove("sample_resume.txt")
        except:
            pass

def test_different_jobs():
    """Test with different job descriptions to show variation"""
    print("\n" + "=" * 50)
    print("Testing with DIFFERENT job descriptions...")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    jobs = [
        {
            "name": "DevOps Engineer",
            "description": """DevOps Engineer
We need a DevOps engineer for cloud infrastructure.
Requirements: 5+ years DevOps, AWS, Kubernetes, Docker, Terraform, Jenkins"""
        },
        {
            "name": "Data Scientist", 
            "description": """Data Scientist
Looking for a data scientist for ML projects.
Requirements: Python, pandas, scikit-learn, TensorFlow, statistics, PhD preferred"""
        }
    ]
    
    resume_content = """John Doe - Software Developer
3 years full-stack development, Python, JavaScript, React, Node.js, SQL, Docker, AWS"""
    
    with open("sample_resume.txt", "w") as f:
        f.write(resume_content)
    
    try:
        for job in jobs:
            print(f"\nTesting: {job['name']}")
            
            files = {'resume': ('resume.txt', open('sample_resume.txt', 'rb'), 'text/plain')}
            data = {'jobDescription': job['description']}
            
            response = requests.post(f"{base_url}/api/screen-resume", files=files, data=data, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  Score: {result.get('match_score')}/100")
                print(f"  Summary: {result.get('match_summary', 'N/A')[:80]}...")
            else:
                print(f"  Error: {response.status_code}")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            import os
            os.remove("sample_resume.txt")
        except:
            pass

if __name__ == "__main__":
    print("🧪 AI Resume Matcher - Local Server Test")
    print("Make sure the local server is running first!")
    print("Run: python api/run_local_server.py")
    print("\nPress Enter to continue...")
    input()
    
    test_local_server()
    test_different_jobs()
    
    print("\n" + "=" * 50)
    print("✅ Local testing completed!")
    print("If the results show different scores for different jobs,")
    print("then your AI Resume Matcher is working perfectly!")
    print("=" * 50)
