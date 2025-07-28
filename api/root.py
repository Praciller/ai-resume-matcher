"""
Root endpoint for Vercel serverless function.
"""
import json

def handler(request):
    """Root handler for Vercel."""
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
    
    response_body = {
        "message": "Intelligent Resume Screener API",
        "status": "running"
    }
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(response_body)
    }
