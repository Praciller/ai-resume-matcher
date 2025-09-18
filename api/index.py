"""
Vercel serverless function entry point for FastAPI backend.
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from urllib.parse import parse_qs
import io

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
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

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

            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/screen-resume':
            try:
                # Set CORS headers
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()

                # For now, return a simple response to test if the handler works
                response = {
                    "match_score": 75,
                    "match_summary": "Test response - handler is working",
                    "detailed_analysis": {
                        "skill_matches": ["Python", "JavaScript"],
                        "skill_gaps": ["LangChain"],
                        "experience_match": "Good match",
                        "education_match": "Relevant background",
                        "overall_recommendation": "Recommended for interview"
                    }
                }

                self.wfile.write(json.dumps(response).encode())

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"error": f"Handler error: {str(e)}"}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
