import requests

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

# Sample resume
resume_content = """John Doe
Senior Software Developer

EXPERIENCE:
3 years of full-stack development experience
Built e-commerce platforms using React and Node.js
Developed data analytics dashboards for financial data
Experience with Python, JavaScript, SQL, Docker, AWS
Strong code review participation
Linux/Unix system administration

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
    print("Testing AI Resume Matcher Local Server")
    print("=" * 50)
    
    # Test resume screening
    files = {'resume': ('resume.txt', open('test_resume.txt', 'rb'), 'text/plain')}
    data = {'jobDescription': job_description}
    
    response = requests.post("http://localhost:8000/api/screen-resume", files=files, data=data, timeout=30)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\nMATCH SCORE: {result.get('match_score')}/100")
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
        
        print("\n" + "=" * 50)
        print("SUCCESS: Local AI Resume Matcher is working!")
        
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Error: {e}")

finally:
    import os
    try:
        os.remove("test_resume.txt")
    except:
        pass
