"""
Vercel serverless function entry point for FastAPI backend.
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from mangum import Mangum
    import main

    # Create the handler for Vercel
    handler = Mangum(main.app, lifespan="off")

except ImportError as e:
    print(f"Import error: {e}")
    # Fallback handler
    def handler(event, context):
        return {
            "statusCode": 500,
            "body": f"Import error: {str(e)}"
        }
except Exception as e:
    print(f"Handler creation error: {e}")
    # Fallback handler
    def handler(event, context):
        return {
            "statusCode": 500,
            "body": f"Handler error: {str(e)}"
        }
