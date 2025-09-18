"""
Vercel serverless function entry point for FastAPI backend.
"""
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

def handler(request):
    """
    Vercel serverless function handler
    """
    try:
        method = request.get('method', 'GET')
        path = request.get('path', '/')

        # CORS headers
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }

        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }

        if path == '/api/health' and method == 'GET':
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

            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(response)
            }

        elif path == '/api/screen-resume' and method == 'POST':
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

            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(response)
            }

        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({"error": "Not found"})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({"error": f"Handler error: {str(e)}"})
        }
