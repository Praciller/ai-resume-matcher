# Local Development Setup with Authentication

## Quick Start for Local Development

If you want to test the authentication locally before deploying:

### 1. Set up Supabase (Required for Authentication)

1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Go to Settings > API and copy:
   - Project URL
   - anon public key

### 2. Configure Environment Variables

Create `frontend/.env.local`:
```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_SUPABASE_URL=your_supabase_project_url
REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 3. Set up GitHub OAuth for Local Development

1. Go to GitHub Settings > Developer settings > OAuth Apps
2. Create a new OAuth App:
   - Application name: `AI Resume Matcher (Local)`
   - Homepage URL: `http://localhost:3000`
   - Authorization callback URL: `https://your-supabase-project.supabase.co/auth/v1/callback`

3. In Supabase dashboard:
   - Go to Authentication > Providers
   - Enable GitHub provider
   - Add your GitHub OAuth App credentials

4. Set Site URL in Supabase:
   - Go to Authentication > URL Configuration
   - Site URL: `http://localhost:3000`
   - Add `http://localhost:3000/**` to Redirect URLs

### 4. Start Development Servers

```bash
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
python main.py

# Terminal 2 - Frontend
cd frontend
npm install
npm start
```

### 5. Test Authentication

1. Go to `http://localhost:3000`
2. Click "Sign in with GitHub"
3. Authorize the application
4. You should be redirected back and see the main application

## Skip Authentication for Development

If you want to develop without authentication, you can temporarily modify `frontend/src/App.js`:

```javascript
// Comment out the authentication check
function AppContent() {
  const { user, loading } = useAuth();

  // Temporarily skip auth for development
  // if (loading) { ... }
  // if (!user) { return <Auth />; }

  return (
    <div className="App">
      <ResumeScreener />
    </div>
  );
}
```

Remember to uncomment this before deploying to production!
