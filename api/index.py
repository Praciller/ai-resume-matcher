from http.server import BaseHTTPRequestHandler
import json
import sys
import os
import io
import cgi
from urllib.parse import parse_qs

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from core.parser import parse_pdf_to_text, validate_pdf_file
    from core.llm_extractor import extract_resume_data, compare_resume_to_jd, test_gemini_api
    AI_AVAILABLE = True
except Exception as e:
    print(f"AI modules not available: {e}")
    AI_AVAILABLE = False

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        if self.path == '/api/health':
            if AI_AVAILABLE:
                try:
                    gemini_status = test_gemini_api()
                    response = {"status": "healthy", "gemini_ai": gemini_status.get("status", "checking")}
                except Exception as e:
                    response = {"status": "healthy", "gemini_ai": f"error: {str(e)}"}
            else:
                response = {"status": "healthy", "gemini_ai": "modules not loaded"}
        else:
            response = {"message": "API is running"}

        self.wfile.write(json.dumps(response).encode('utf-8'))
        return

    def do_POST(self):
        try:
            if self.path == '/api/screen-resume':
                response = self._process_resume_screening()
            else:
                response = {"message": "POST endpoint"}

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            # Return error in the expected format to avoid JSON parsing issues
            error_response = {
                "match_score": 0,
                "match_summary": f"Error processing resume: {str(e)}",
                "detailed_analysis": {
                    "skill_matches": [],
                    "skill_gaps": [],
                    "experience_match": "Unable to analyze due to error",
                    "education_match": "Unable to analyze due to error",
                    "overall_recommendation": "Please try again or contact support"
                }
            }
            self.send_response(200)  # Still return 200 to avoid frontend JSON parsing errors
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
        return

    def _process_resume_screening(self):
        """Process resume screening with real AI integration."""
        if not AI_AVAILABLE:
            return {
                "match_score": 0,
                "match_summary": "AI processing modules are not available. Please check server configuration.",
                "detailed_analysis": {
                    "skill_matches": [],
                    "skill_gaps": [],
                    "experience_match": "AI modules not loaded",
                    "education_match": "AI modules not loaded",
                    "overall_recommendation": "Cannot process - server configuration issue"
                }
            }

        try:
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
                boundary = boundary[1:-1]  # Remove quotes if present
            boundary = boundary.encode()

            parts = post_data.split(b'--' + boundary)

            resume_file_data = None
            job_description = None

            for part in parts:
                if b'Content-Disposition' in part and len(part.strip()) > 0:
                    # Look for file upload (resume)
                    if (b'name="resume"' in part or b'name="resumeFile"' in part or
                        b'filename=' in part):
                        # Extract file data
                        header_end = part.find(b'\r\n\r\n')
                        if header_end != -1:
                            resume_file_data = part[header_end + 4:]
                            # Clean up the data
                            while resume_file_data.endswith(b'\r\n'):
                                resume_file_data = resume_file_data[:-2]
                            while resume_file_data.endswith(b'\n'):
                                resume_file_data = resume_file_data[:-1]
                            while resume_file_data.endswith(b'\r'):
                                resume_file_data = resume_file_data[:-1]

                    # Look for job description text
                    elif (b'name="jobDescription"' in part or b'name="jd_text"' in part or
                          b'name="job_description"' in part):
                        # Extract job description text
                        header_end = part.find(b'\r\n\r\n')
                        if header_end != -1:
                            job_description = part[header_end + 4:].decode('utf-8', errors='ignore').strip()
                            # Clean up the text
                            while job_description.endswith('\r\n'):
                                job_description = job_description[:-2]
                            while job_description.endswith('\n'):
                                job_description = job_description[:-1]
                            while job_description.endswith('\r'):
                                job_description = job_description[:-1]

            if not resume_file_data:
                raise ValueError("No resume file found in request")

            if not job_description:
                raise ValueError("No job description found in request")

            # Validate PDF file
            if not validate_pdf_file(resume_file_data):
                raise ValueError("Invalid PDF file or file is corrupted")

            # Step 1: Extract text from PDF
            resume_text = parse_pdf_to_text(resume_file_data)

            # Step 2: Extract structured data from resume
            resume_data = extract_resume_data(resume_text)

            # Step 3: Compare resume to job description
            comparison_result = compare_resume_to_jd(resume_data, job_description)

            # Format response to match frontend expectations
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

            return response

        except Exception as e:
            # Return a structured error response
            return {
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

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
