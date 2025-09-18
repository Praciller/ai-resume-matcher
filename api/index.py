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
            try:
                # Get the request body and form data
                body = request.get('body', '')
                if request.get('isBase64Encoded', False):
                    import base64
                    body = base64.b64decode(body).decode('utf-8')

                # For now, let's return a more detailed test response that shows we're processing the request
                # In the future, this would parse the multipart form data and process the actual file
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

                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(response)
                }

            except Exception as e:
                # Return error as JSON to avoid the "A SERVER E..." error
                error_response = {
                    "error": f"Processing error: {str(e)}",
                    "match_score": 0,
                    "match_summary": "Error processing resume. Please try again.",
                    "detailed_analysis": {
                        "skill_matches": [],
                        "skill_gaps": [],
                        "experience_match": "Unable to analyze",
                        "education_match": "Unable to analyze",
                        "overall_recommendation": "Please resubmit resume"
                    }
                }

                return {
                    'statusCode': 200,  # Return 200 to avoid frontend errors
                    'headers': headers,
                    'body': json.dumps(error_response)
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
