# TechCrunch Daily Digest - Deployment Guide

## Quick Deploy (Free Options)

### Option 1: Render.com (Recommended)

1. Push your code to GitHub
2. Create account at https://render.com
3. New Web Service → Connect your GitHub repo
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Environment Variables: Add `TZ=UTC`
5. Create

**Auto-refresh:** Use Render's Scheduled Jobs (free tier):
- Every 6 hours: `curl https://your-app.onrender.com/generate`

### Option 2: Railway

1. Install Railway CLI: `npm i -g @railway/cli`
2. `railway login`
3. `railway init`
4. `railway up`

### Option 3: Fly.io

1. Install flyctl: https://fly.io/docs/installing/
2. `fly auth login`
3. `fly launch`
4. `fly deploy`

## Auto-Refresh Setup

Use cron-job.org (free) to call `POST https://your-app.com/generate` every 6 hours.

## Health Check

The app includes a `/health` endpoint for uptime monitors.

## Recommended Free Tier Hosting Comparison

| Service | Free Hours | Auto-deploy | Region |
|---------|-----------|-------------|--------|
| Render | 750 hrs/month | Yes | US/EU |
| Railway | 500 hrs/month | Yes | Global |
| Fly.io | Unlimited | Yes | Global |
| PythonAnywhere | Always free | No | UK |
