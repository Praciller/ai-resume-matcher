#!/usr/bin/env node

/**
 * Deployment helper script for Vercel
 * This script helps validate the setup before deployment
 */

const fs = require('fs');
const path = require('path');

console.log('🚀 AI Resume Matcher - Vercel Deployment Checker\n');

// Check if required files exist
const requiredFiles = [
  'vercel.json',
  'frontend/package.json',
  'api/main.py',
  'api/requirements.txt',
  'api/index.py'
];

console.log('📁 Checking required files...');
let allFilesExist = true;

requiredFiles.forEach(file => {
  if (fs.existsSync(file)) {
    console.log(`✅ ${file}`);
  } else {
    console.log(`❌ ${file} - MISSING`);
    allFilesExist = false;
  }
});

// Check package.json dependencies
console.log('\n📦 Checking frontend dependencies...');
try {
  const packageJson = JSON.parse(fs.readFileSync('frontend/package.json', 'utf8'));
  const requiredDeps = [
    '@supabase/supabase-js',
    '@supabase/auth-ui-react',
    '@supabase/auth-ui-shared',
    'react',
    'react-dom'
  ];

  requiredDeps.forEach(dep => {
    if (packageJson.dependencies[dep]) {
      console.log(`✅ ${dep}`);
    } else {
      console.log(`❌ ${dep} - MISSING`);
      allFilesExist = false;
    }
  });
} catch (error) {
  console.log('❌ Could not read frontend/package.json');
  allFilesExist = false;
}

// Check environment variables setup
console.log('\n🔧 Environment Variables Checklist:');
console.log('Make sure to set these in Vercel dashboard:');
console.log('- REACT_APP_SUPABASE_URL');
console.log('- REACT_APP_SUPABASE_ANON_KEY');
console.log('- REACT_APP_API_URL');
console.log('- GEMINI_API_KEY');
console.log('- ENVIRONMENT=production');

// Final status
console.log('\n' + '='.repeat(50));
if (allFilesExist) {
  console.log('✅ All checks passed! Ready for Vercel deployment.');
  console.log('\nNext steps:');
  console.log('1. Push your code to GitHub');
  console.log('2. Connect your repo to Vercel');
  console.log('3. Set environment variables in Vercel');
  console.log('4. Deploy!');
} else {
  console.log('❌ Some files are missing. Please fix the issues above.');
}
console.log('='.repeat(50));

// Instructions
console.log('\n📖 For detailed instructions, see VERCEL_DEPLOYMENT.md');
