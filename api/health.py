"""
Health check endpoint for Vercel serverless function.
"""
import json
import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(__file__))

from core.llm_extractor import test_gemini_connection

def handler(request):
    """Health check handler for Vercel."""
    try:
        # Set CORS headers
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'application/json'
        }
        
        # Handle preflight requests
        if request.get('method') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Test Gemini connection
        gemini_status = test_gemini_connection()
        
        response_body = {
            "status": "healthy",
            "gemini_ai": "connected" if gemini_status else "disconnected"
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response_body)
        }
        
    except Exception as e:
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        }
        
        return {
            'statusCode': 503,
            'headers': headers,
            'body': json.dumps({"status": "unhealthy", "error": str(e)})
        }
