from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)

# Try to import AI modules
AI_AVAILABLE = False
try:
    from core.parser import parse_pdf_to_text, validate_pdf_file
    from core.llm_extractor import extract_resume_data, compare_resume_to_jd
    AI_AVAILABLE = True
except Exception as e:
    print(f"AI modules not available: {e}")
    AI_AVAILABLE = False

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            if not AI_AVAILABLE:
                response = {
                    "match_score": 0,
                    "match_summary": "AI processing modules are not available in production",
                    "detailed_analysis": {
                        "skill_matches": [],
                        "skill_gaps": [],
                        "experience_match": "AI modules not loaded",
                        "education_match": "AI modules not loaded",
                        "overall_recommendation": "Cannot process - server configuration issue"
                    }
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # Parse multipart form data
            content_type = self.headers.get('Content-Type', '')
            if not content_type.startswith('multipart/form-data'):
                raise ValueError("Expected multipart/form-data")
            
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                raise ValueError("No data received")
            
            # Read the request body
            post_data = self.rfile.read(content_length)
            
            # Parse the multipart data
            boundary = content_type.split('boundary=')[1]
            if boundary.startswith('"') and boundary.endswith('"'):
                boundary = boundary[1:-1]
            boundary = boundary.encode()
            
            parts = post_data.split(b'--' + boundary)
            
            resume_file_data = None
            job_description = None
            
            for part in parts:
                if b'Content-Disposition' in part and len(part.strip()) > 0:
                    # Look for file upload (resume)
                    if (b'name="resume"' in part or b'name="resumeFile"' in part or
                        b'filename=' in part):
                        header_end = part.find(b'\r\n\r\n')
                        if header_end != -1:
                            resume_file_data = part[header_end + 4:]
                            # Clean up the data
                            while resume_file_data.endswith(b'\r\n'):
                                resume_file_data = resume_file_data[:-2]
                    
                    # Look for job description text
                    elif (b'name="jobDescription"' in part or b'name="jd_text"' in part):
                        header_end = part.find(b'\r\n\r\n')
                        if header_end != -1:
                            job_description = part[header_end + 4:].decode('utf-8', errors='ignore').strip()
                            while job_description.endswith('\r\n'):
                                job_description = job_description[:-2]
            
            if not resume_file_data:
                raise ValueError("No resume file found in request")
            
            if not job_description:
                raise ValueError("No job description found in request")
            
            # Process the resume
            if not validate_pdf_file(resume_file_data):
                # Treat as text file
                resume_text = resume_file_data.decode('utf-8', errors='ignore')
            else:
                resume_text = parse_pdf_to_text(resume_file_data)
            
            # Extract structured data from resume
            resume_data = extract_resume_data(resume_text)
            
            # Compare resume to job description
            comparison_result = compare_resume_to_jd(resume_data, job_description)
            
            # Format response
            response = {
                "match_score": comparison_result.get("match_score", 0),
                "match_summary": comparison_result.get("match_summary", "Analysis completed"),
                "detailed_analysis": {
                    "skill_matches": comparison_result.get("skill_matches", []),
                    "skill_gaps": comparison_result.get("skill_gaps", []),
                    "experience_match": comparison_result.get("experience_match", ""),
                    "education_match": comparison_result.get("education_match", ""),
                    "overall_recommendation": comparison_result.get("overall_recommendation", "")
                }
            }
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            # Return error in the expected format
            error_response = {
                "match_score": 0,
                "match_summary": f"Processing failed: {str(e)}",
                "detailed_analysis": {
                    "skill_matches": [],
                    "skill_gaps": [],
                    "experience_match": "Error during processing",
                    "education_match": "Error during processing",
                    "overall_recommendation": "Unable to complete analysis - please try again"
                }
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
        return
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
