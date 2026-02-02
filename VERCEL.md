# Vercel Deployment Guide

## Deploy to Vercel

1. Push code to GitHub
2. Import in Vercel: https://vercel.com/new
3. Framework: Python
4. Deploy

## Auto-Refresh Setup

Vercel Functions have a 10-second timeout, so we use **external cron**.

### Step 1: Deploy to Vercel

### Step 2: Set up free cron job

1. Go to https://cron-job.org (free account)
2. Create new job:
   - URL: `https://your-project.vercel.app/api/generate`
   - Schedule: `0 */6 * * *` (every 6 hours)
   - Method: `POST`

### Step 3: Verify

Visit `https://your-project.vercel.app/` to see the latest digest.

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run API locally
python -c "from api.generate import main; print(main())"

# Or run Flask app
python app.py
```

## Project Structure

```
├── api/
│   ├── generate.py    # Vercel serverless function
│   └── health.py      # Health check endpoint
├── templates/         # HTML templates
├── app.py            # Flask app (local only)
├── config.yaml       # Configuration
├── vercel.json       # Vercel config
└── requirements.txt
```
