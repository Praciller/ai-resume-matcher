#!/usr/bin/env python3
"""
Test AI Resume Matcher with multiple job descriptions to demonstrate variation
"""

import requests
import json
import time

def test_job_variation():
    """Test with multiple different job descriptions"""
    print("AI Resume Matcher - Job Variation Test")
    print("=" * 60)
    
    # Sample resume (consistent across all tests)
    resume_content = """John Doe
Software Developer

EXPERIENCE:
• 3 years of full-stack development experience
• Built e-commerce platforms using React and Node.js
• Developed data analytics dashboards for financial data
• Experience with Python, JavaScript, SQL, Docker, AWS
• Strong code review participation
• Linux/Unix system administration

EDUCATION:
• Bachelor's in Computer Science

SKILLS:
• Frontend: React, JavaScript, HTML5, CSS3, TypeScript
• Backend: Python, Node.js, Express.js, FastAPI
• Databases: SQL, PostgreSQL, MongoDB
• DevOps: Docker, AWS, Git, Linux
• Tools: VS Code, Postman, Jira"""

    # Different job descriptions to test
    job_descriptions = [
        {
            "name": "1. YOUR KAPARA JOB",
            "description": """Fullstack Developer
At Kapara, we are focused on aggregating data and building a unique dashboard in the financial markets. We are looking to hire a Fullstack Developer (BackEnd & FrontEnd) to join us as in a full time role.

You must have full working rights in Thailand and able to work at our Old City Chiang Mai office. 

As a Fullstack Engineer at Kapara, you will coordinate cross-functionally with a team of front end & backend developers & graphic designers to design, develop, and maintain the frontend & backend systems that power our applications.

Required Experience:
- Robust, performant, modular, clean, and maintainable code
- Strong communication skills
- Strong participation in code reviews
- Experience with Linux based operating systems (or Mac)
- 2-4+ years of experience"""
        },
        {
            "name": "2. SENIOR DEVOPS ENGINEER",
            "description": """Senior DevOps Engineer
We are seeking a Senior DevOps Engineer to manage our cloud infrastructure and CI/CD pipelines.

Requirements:
- 5+ years DevOps experience
- AWS/Azure cloud platforms
- Kubernetes and Docker containerization
- Terraform or CloudFormation
- Jenkins, GitLab CI, or GitHub Actions
- Monitoring tools (Prometheus, Grafana)
- Linux system administration
- Python or Bash scripting
- On-call support experience"""
        },
        {
            "name": "3. DATA SCIENTIST",
            "description": """Data Scientist
We need a data scientist to analyze large datasets and build ML models.

Requirements:
- 3+ years data science experience
- Python (pandas, numpy, scikit-learn)
- SQL and database experience
- Statistical analysis and hypothesis testing
- Machine learning algorithms
- Data visualization (matplotlib, seaborn, Tableau)
- Jupyter notebooks and research experience
- PhD or Masters in related field preferred"""
        },
        {
            "name": "4. FRONTEND REACT DEVELOPER",
            "description": """Frontend React Developer
Looking for a skilled React developer to join our frontend team.

Requirements:
- 2+ years React experience
- JavaScript ES6+, TypeScript
- HTML5, CSS3, responsive design
- Redux or Context API
- RESTful API integration
- Git version control
- Testing frameworks (Jest, Cypress)
- UI/UX design collaboration
- Performance optimization"""
        },
        {
            "name": "5. BACKEND PYTHON DEVELOPER",
            "description": """Backend Python Developer
Join our backend team to build scalable APIs and services.

Requirements:
- 3+ years Python experience
- Django or Flask framework
- PostgreSQL or MySQL
- RESTful API design
- Docker containerization
- AWS or cloud platforms
- Unit testing and TDD
- Microservices architecture
- Redis caching, Celery queues"""
        }
    ]
    
    # Save resume as text file
    with open("test_resume.txt", "w") as f:
        f.write(resume_content)
    
    results = []
    
    try:
        print("Testing with the same resume against different job descriptions...")
        print("Resume Skills: React, JavaScript, Python, Node.js, SQL, Docker, AWS, Linux")
        print("\n" + "-" * 60)
        
        for i, job in enumerate(job_descriptions):
            print(f"\n{job['name']}")
            print("-" * 40)
            
            try:
                # Prepare request
                files = {'resume': ('resume.txt', open('test_resume.txt', 'rb'), 'text/plain')}
                data = {'jobDescription': job['description']}
                
                # Send request to local server
                response = requests.post(
                    "http://localhost:8000/api/screen-resume", 
                    files=files, 
                    data=data, 
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    match_score = result.get('match_score', 0)
                    summary = result.get('match_summary', 'N/A')
                    
                    print(f"Match Score: {match_score}/100")
                    print(f"Summary: {summary[:120]}...")
                    
                    detailed = result.get('detailed_analysis', {})
                    skills_matched = detailed.get('skill_matches', [])
                    skills_gaps = detailed.get('skill_gaps', [])
                    
                    if skills_matched:
                        print(f"Top Skills Matched: {', '.join(skills_matched[:3])}")
                    if skills_gaps:
                        print(f"Key Skill Gaps: {', '.join(skills_gaps[:3])}")
                    
                    results.append({
                        'job': job['name'],
                        'score': match_score,
                        'summary': summary,
                        'skills_matched': skills_matched,
                        'skills_gaps': skills_gaps
                    })
                    
                else:
                    print(f"Error: {response.status_code}")
                    print(response.text[:200])
                    
            except Exception as e:
                print(f"Error testing {job['name']}: {e}")
            
            # Small delay between requests
            time.sleep(1)
    
    finally:
        # Clean up
        try:
            import os
            os.remove("test_resume.txt")
        except:
            pass
    
    # Analyze results
    print("\n" + "=" * 60)
    print("VARIATION ANALYSIS")
    print("=" * 60)
    
    if len(results) >= 2:
        scores = [r['score'] for r in results]
        min_score = min(scores)
        max_score = max(scores)
        score_range = max_score - min_score
        
        print(f"Score Range: {min_score} - {max_score} (Variation: {score_range} points)")
        
        print("\nScore Summary:")
        for result in results:
            print(f"  {result['job']}: {result['score']}/100")
        
        if score_range >= 10:
            print(f"\nSUCCESS: Significant variation detected ({score_range} point range)")
            print("The AI is providing different analysis for different job types!")
        else:
            print(f"\nWARNING: Limited variation ({score_range} point range)")
            print("Results may need more diverse job descriptions for testing")
        
        # Show different skills matched
        print("\nSkills Matching Variation:")
        for result in results:
            if result['skills_matched']:
                print(f"  {result['job']}: {', '.join(result['skills_matched'][:3])}")
    
    print("\n" + "=" * 60)
    print("CONCLUSION:")
    if len(results) >= 3 and max(scores) - min(scores) >= 10:
        print("AI Resume Matcher is working correctly!")
        print("Different job descriptions produce meaningfully different results.")
    else:
        print("System is functional but may need tuning for more variation.")
    print("=" * 60)

if __name__ == "__main__":
    print("Make sure the local server is running:")
    print("cd api && python run_local_server.py")
    print("\nPress Enter to start testing...")
    input()
    
    test_job_variation()
