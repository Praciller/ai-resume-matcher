from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add backend directory to Python path for imports
backend_dir = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_dir)

# Import AI modules
try:
    from core.parser import parse_pdf_to_text, validate_pdf_file
    from core.llm_extractor import extract_resume_data, compare_resume_to_jd
    AI_AVAILABLE = True
except Exception as e:
    print(f"AI modules not available: {e}")
    AI_AVAILABLE = False

class handler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        """Send CORS headers for all responses"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self._send_cors_headers()
            self.end_headers()

            if self.path == '/api/health':
                response = {
                    "status": "healthy",
                    "ai_available": AI_AVAILABLE,
                    "gemini_ai": "connected" if AI_AVAILABLE else "disconnected"
                }
            else:
                response = {
                    "message": "AI Resume Matcher API",
                    "status": "ready",
                    "endpoints": ["/api/health", "/api/screen-resume"]
                }

            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            error_response = {"status": "error", "error": str(e)}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def do_POST(self):
        try:
            if self.path == '/api/screen-resume':
                response = self._process_resume_screening()
            else:
                response = {"error": "Endpoint not found"}

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            error_response = {
                "match_score": 0,
                "match_summary": f"Error: {str(e)}",
                "detailed_analysis": {"skill_matches": [], "skill_gaps": []}
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def _process_resume_screening(self):
        """Process resume screening with AI integration."""
        if not AI_AVAILABLE:
            return {
                "match_score": 0,
                "match_summary": "AI modules not available",
                "detailed_analysis": {"skill_matches": [], "skill_gaps": []}
            }

        try:
            # Simple multipart parsing
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)

            # Extract boundary
            content_type = self.headers.get('Content-Type', '')
            boundary = content_type.split('boundary=')[1].strip('"').encode()

            # Split by boundary and extract data
            parts = post_data.split(b'--' + boundary)
            resume_file_data = None
            job_description = None

            for part in parts:
                if b'name="resume_file"' in part or b'filename=' in part:
                    header_end = part.find(b'\r\n\r\n')
                    if header_end != -1:
                        resume_file_data = part[header_end + 4:].rstrip(b'\r\n')
                elif b'name="jd_text"' in part:
                    header_end = part.find(b'\r\n\r\n')
                    if header_end != -1:
                        job_description = part[header_end + 4:].decode('utf-8').strip()

            if not resume_file_data or not job_description:
                raise ValueError("Missing resume file or job description")

            # Process the resume
            if not validate_pdf_file(resume_file_data):
                raise ValueError("Invalid PDF file")

            resume_text = parse_pdf_to_text(resume_file_data)
            resume_data = extract_resume_data(resume_text)
            ai_result = compare_resume_to_jd(resume_data, job_description)

            # Wrap the AI result in the expected structure for frontend
            result = {
                "match_score": ai_result.get("match_score", 0),
                "match_summary": ai_result.get("match_summary", ""),
                "detailed_analysis": {
                    "skill_matches": ai_result.get("skill_matches", []),
                    "skill_gaps": ai_result.get("skill_gaps", []),
                    "experience_match": ai_result.get("experience_match", ""),
                    "education_match": ai_result.get("education_match", ""),
                    "overall_recommendation": ai_result.get("overall_recommendation", ""),
                    "detailed_recommendations": ai_result.get("detailed_recommendations", {}),
                    "justification": ai_result.get("justification", "")
                }
            }

            return result

        except Exception as e:
            return {
                "match_score": 0,
                "match_summary": f"Error: {str(e)}",
                "detailed_analysis": {"skill_matches": [], "skill_gaps": []}
            }

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
