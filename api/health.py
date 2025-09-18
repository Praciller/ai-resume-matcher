from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set CORS headers
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        try:
            # Simple health check without Gemini for now
            response_body = {
                "status": "healthy",
                "timestamp": "2025-01-18-v5.0",
                "deployment_version": "v5.0",
                "gemini_ai": "checking",
                "has_gemini_key": bool(os.getenv('GEMINI_API_KEY')),
                "message": "Deployment successful - health endpoint working!"
            }

            self.wfile.write(json.dumps(response_body).encode())

        except Exception as e:
            response_body = {"status": "unhealthy", "error": str(e)}
            self.wfile.write(json.dumps(response_body).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
