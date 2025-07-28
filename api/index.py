"""
Vercel serverless function entry point for FastAPI backend.
"""
from fastapi import FastAPI
from mangum import Mangum
from main import app

# Create the handler for Vercel
handler = Mangum(app, lifespan="off")
