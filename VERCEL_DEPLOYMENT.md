# Vercel Deployment Guide for AI Resume Matcher

This guide will help you deploy your AI Resume Matcher application to Vercel with GitHub authentication.

## Prerequisites

1. **GitHub Account**: You need a GitHub account to deploy to Vercel
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com) using your GitHub account
3. **Supabase Account**: Sign up at [supabase.com](https://supabase.com) for authentication
4. **Google Gemini API Key**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Step 1: Set up Supabase for Authentication

1. **Create a new Supabase project**:
   - Go to [supabase.com](https://supabase.com)
   - Click "New Project"
   - Choose your organization and create the project

2. **Configure GitHub OAuth**:
   - In your Supabase dashboard, go to Authentication > Providers
   - Enable GitHub provider
   - You'll need to create a GitHub OAuth App:
     - Go to GitHub Settings > Developer settings > OAuth Apps
     - Click "New OAuth App"
     - Application name: `AI Resume Matcher`
     - Homepage URL: `https://your-app-name.vercel.app`
     - Authorization callback URL: `https://your-supabase-project.supabase.co/auth/v1/callback`
   - Copy the Client ID and Client Secret to Supabase

3. **Get Supabase credentials**:
   - Go to Settings > API
   - Copy the Project URL and anon public key

## Step 2: Deploy to Vercel

1. **Connect your GitHub repository**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository

2. **Configure build settings**:
   - Framework Preset: Other
   - Build Command: `cd frontend && npm run build`
   - Output Directory: `frontend/build`
   - Install Command: `cd frontend && npm install`

3. **Set environment variables**:
   In Vercel dashboard > Settings > Environment Variables, add:
   
   ```
   REACT_APP_SUPABASE_URL=your_supabase_project_url
   REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key
   REACT_APP_API_URL=https://your-vercel-app.vercel.app
   GEMINI_API_KEY=your_gemini_api_key
   ENVIRONMENT=production
   ```

4. **Deploy**:
   - Click "Deploy"
   - Wait for the deployment to complete

## Step 3: Update GitHub OAuth Settings

After deployment, update your GitHub OAuth App:
- Homepage URL: `https://your-actual-vercel-url.vercel.app`
- Authorization callback URL: `https://your-supabase-project.supabase.co/auth/v1/callback`

## Step 4: Update Supabase Site URL

In Supabase dashboard:
- Go to Authentication > URL Configuration
- Set Site URL to: `https://your-actual-vercel-url.vercel.app`
- Add your Vercel URL to Redirect URLs

## File Structure

Your project should have this structure:
```
ai-resume-matcher/
├── api/                    # FastAPI backend (serverless functions)
├── frontend/              # React frontend
├── backend/              # Alternative backend setup
├── vercel.json           # Vercel configuration
└── VERCEL_DEPLOYMENT.md  # This guide
```

## Environment Variables Summary

### Frontend (.env.production)
- `REACT_APP_SUPABASE_URL`: Your Supabase project URL
- `REACT_APP_SUPABASE_ANON_KEY`: Your Supabase anonymous key
- `REACT_APP_API_URL`: Your Vercel app URL

### Backend (Vercel Environment Variables)
- `GEMINI_API_KEY`: Your Google Gemini API key
- `ENVIRONMENT`: Set to "production"

## Troubleshooting

### Common Issues:

1. **Authentication not working**:
   - Check GitHub OAuth App settings
   - Verify Supabase Site URL configuration
   - Ensure environment variables are set correctly

2. **API endpoints not working**:
   - Check that `api/` directory contains Python files
   - Verify `vercel.json` configuration
   - Check Vercel function logs

3. **Build failures**:
   - Ensure all dependencies are in `frontend/package.json`
   - Check build command in Vercel settings
   - Review build logs for specific errors

### Testing the Deployment:

1. Visit your Vercel URL
2. Click "Sign in with GitHub"
3. Authorize the application
4. Test the resume screening functionality

## Security Notes

- Never commit `.env` files with real credentials
- Use Vercel environment variables for sensitive data
- Supabase handles OAuth securely
- API keys are server-side only

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Review Supabase authentication logs
3. Verify all environment variables are set
4. Test locally first with the same configuration
