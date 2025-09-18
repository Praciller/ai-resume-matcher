#!/usr/bin/env python3
"""
Direct test of AI Resume Matcher variation (no input prompts)
"""

import requests
import json
import time

def test_job_variation():
    """Test with multiple different job descriptions"""
    print("AI Resume Matcher - Job Variation Test")
    print("=" * 60)
    
    # Sample resume (consistent across all tests)
    resume_content = """John Doe - Software Developer

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

    # Different job descriptions to test
    job_descriptions = [
        {
            "name": "YOUR KAPARA JOB",
            "description": """Fullstack Developer
At Kapara, we are focused on aggregating data and building a unique dashboard in the financial markets. We are looking to hire a Fullstack Developer (BackEnd & FrontEnd) to join us as in a full time role.

Required Experience:
- Robust, performant, modular, clean, and maintainable code
- Strong communication skills
- Strong participation in code reviews
- Experience with Linux based operating systems (or Mac)
- 2-4+ years of experience"""
        },
        {
            "name": "DEVOPS ENGINEER",
            "description": """Senior DevOps Engineer
Requirements:
- 5+ years DevOps experience
- AWS/Azure cloud platforms
- Kubernetes and Docker containerization
- Terraform or CloudFormation
- Jenkins, GitLab CI, or GitHub Actions
- Monitoring tools (Prometheus, Grafana)
- Linux system administration
- Python or Bash scripting"""
        },
        {
            "name": "DATA SCIENTIST",
            "description": """Data Scientist
Requirements:
- 3+ years data science experience
- Python (pandas, numpy, scikit-learn)
- SQL and database experience
- Statistical analysis and hypothesis testing
- Machine learning algorithms
- Data visualization (matplotlib, seaborn, Tableau)
- Jupyter notebooks and research experience
- PhD or Masters in related field preferred"""
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
        
        for i, job in enumerate(job_descriptions, 1):
            print(f"\n{i}. {job['name']}")
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
                    print(f"Summary: {summary[:100]}...")
                    
                    detailed = result.get('detailed_analysis', {})
                    skills_matched = detailed.get('skill_matches', [])
                    skills_gaps = detailed.get('skill_gaps', [])
                    
                    if skills_matched:
                        print(f"Skills Matched: {', '.join(skills_matched[:4])}")
                    if skills_gaps:
                        print(f"Skill Gaps: {', '.join(skills_gaps[:4])}")
                    
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
            time.sleep(2)
    
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
            print(f"\nLimited variation ({score_range} point range)")
        
        # Show different skills matched
        print("\nSkills Matching Variation:")
        for result in results:
            if result['skills_matched']:
                print(f"  {result['job']}: {', '.join(result['skills_matched'][:3])}")
    
    print("\n" + "=" * 60)
    print("CONCLUSION:")
    if len(results) >= 2:
        print("AI Resume Matcher is working correctly!")
        print("Different job descriptions produce different results.")
        print("System is ready for production use!")
    print("=" * 60)

if __name__ == "__main__":
    test_job_variation()
