"""
Vercel serverless function entry point for FastAPI backend.
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    import main
    app = main.app
except Exception as e:
    print(f"Failed to import main app: {e}")
    app = None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            if self.path == '/api/health':
                if app:
                    try:
                        # Test Gemini API
                        from core.llm_extractor import test_gemini_api
                        gemini_status = test_gemini_api()
                        response = {"status": "healthy", "gemini_ai": gemini_status}
                    except Exception as e:
                        response = {"status": "healthy", "gemini_ai": f"error: {str(e)}"}
                else:
                    response = {"status": "error", "message": "App not loaded"}
            else:
                response = {"message": "API is running"}

            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {"error": f"GET error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            if self.path == '/api/screen-resume':
                # Test response for file upload
                response = {
                    "match_score": 85,
                    "match_summary": "Resume successfully processed! This is a test response showing the handler is working with file uploads.",
                    "detailed_analysis": {
                        "skill_matches": ["Python", "JavaScript", "AI/ML", "FastAPI"],
                        "skill_gaps": ["LangChain", "Vector Databases"],
                        "experience_match": "Strong technical background with relevant programming experience",
                        "education_match": "Technical education aligns well with requirements",
                        "overall_recommendation": "Highly recommended for interview - strong candidate with relevant skills"
                    }
                }
            else:
                response = {"message": "POST endpoint"}

            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {"error": f"POST error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def do_OPTIONS(self):
        try:
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
        except Exception as e:
            self.send_response(500)
            self.end_headers()
