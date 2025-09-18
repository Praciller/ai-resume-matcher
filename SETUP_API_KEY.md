# API Key Setup Guide

## Get Your Gemini API Key

1. **Go to Google AI Studio**: https://aistudio.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click "Create API Key"**
4. **Copy the generated API key**

## Set Up for Local Testing

1. **Edit the `.env` file** in the `api/` directory
2. **Replace** `your_actual_gemini_api_key_here` with your actual API key:

```
GEMINI_API_KEY=AIzaSyC-your-actual-api-key-here
```

3. **Test locally**:
```bash
cd api
python test_local.py
```

## Set Up for Vercel Production

1. **Go to your Vercel project dashboard**
2. **Click Settings → Environment Variables**
3. **Add new variable**:
   - Name: `GEMINI_API_KEY`
   - Value: Your actual API key
   - Environment: Production
4. **Click Save**
5. **Redeploy** your project

## Expected Results After Setup

✅ **Local testing**: Different job descriptions should produce different AI analysis results  
✅ **Production**: The live application should provide personalized resume analysis  
✅ **Verification**: Match scores and recommendations should vary based on job requirements  

## Test Commands

```bash
# Test locally
cd api
python test_local.py

# Test production health
curl https://ai-resume-matcher-chi.vercel.app/api/health

# Test production with resume
curl -X POST "https://ai-resume-matcher-chi.vercel.app/api/screen-resume" \
  -F "jobDescription=Your job description here" \
  -F "resume=@path/to/resume.pdf"
```
