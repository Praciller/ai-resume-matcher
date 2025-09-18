from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        if self.path == '/api/health':
            response = {"status": "healthy", "gemini_ai": "checking"}
        else:
            response = {"message": "API is running"}

        self.wfile.write(json.dumps(response).encode('utf-8'))
        return

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        if self.path == '/api/screen-resume':
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
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
