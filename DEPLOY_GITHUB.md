# GitHub deployment guide for Climate Risk Prediction AI

## 🚀 Deploy to GitHub in 3 steps:

### Step 1: Initialize Git Repository
```bash
cd c:\Users\91770\Documents\Hackathons
git init
git add .
git commit -m "Initial commit: Climate Risk Prediction AI System"
```

### Step 2: Connect to GitHub
```bash
git remote add origin https://github.com/AnandShadow/final-hackathon.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Connect your GitHub account
3. Select repository: `AnandShadow/final-hackathon`
4. Set main file path: `streamlit_app.py`
5. Add secrets in Advanced settings:
   ```
   OPENWEATHER_API_KEY = "your_api_key_here"
   AQICN_API_KEY = "your_token_here"
   ```
6. Click "Deploy!"

## 🔧 Required Files for GitHub Deployment:

✅ Created:
- `streamlit_app.py` - Main entry point for Streamlit Cloud
- `requirements.txt` - Dependencies
- `.streamlit/config.toml` - Streamlit configuration
- `.streamlit/secrets_example.toml` - Example secrets file
- `README_GITHUB.md` - Professional GitHub README
- `deploy_streamlit.sh` - Deployment script

## 🌐 Your app will be available at:
`https://final-hackathon-climate-ai.streamlit.app`

## 📋 Checklist before pushing:
- [ ] API keys added to secrets
- [ ] Repository is public (for free Streamlit hosting)
- [ ] All required files are included
- [ ] streamlit_app.py works locally