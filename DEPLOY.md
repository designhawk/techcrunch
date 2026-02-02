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

### Option A: Built-in Scheduler (Running 24/7)

The app already has a scheduler. Set in `config.yaml`:
```yaml
fetch_time: "08:00"
```

### Option B: External Cron Job

Add to your GitHub repository → Settings → Secrets:
- `CRON_API_TOKEN`: Generate a secret token

Create a workflow file `.github/workflows/refresh.yml`:

```yaml
name: Daily Refresh
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:
    inputs:
      manual_trigger:
        description: 'Manual trigger'

jobs:
  refresh:
    runs-on: ubuntu-latest
    if: github.event_name == 'workflow_dispatch' || github.event_name == 'schedule'
    steps:
      - name: Call refresh API
        run: |
          curl -X POST https://your-app.onrender.com/generate
```

### Option C: Easy Cron Services

1. https://cron-job.org (free)
2. https://www.easycron.com (free tier)
3. Set to call `POST https://your-app.com/generate` every 6 hours

## Environment Variables for Production

```bash
# config.yaml
host: "0.0.0.0"
port: 5000
debug: false  # Set to false in production
fetch_time: "08:00"
```

## Health Check

Add endpoint for uptime monitors:
```yaml
# Already included /health endpoint
```

## Recommended Free Tier Hosting Comparison

| Service | Free Hours | Auto-deploy | Region |
|---------|-----------|-------------|--------|
| Render | 750 hrs/month | Yes | US/EU |
| Railway | 500 hrs/month | Yes | Global |
| Fly.io | Unlimited | Yes | Global |
| PythonAnywhere | Always free | No | UK |
