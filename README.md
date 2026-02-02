# TechCrunch Daily Digest

AI-powered daily news digest with article summaries and insights.

## Features

- 📰 Fetches latest TechCrunch articles via RSS
- 🤖 Generates AI insights using OpenRouter (free tier)
- 🖼️ Auto-fetches article featured images
- 📊 Carbon Design System UI
- 🔄 Auto-refresh via scheduled jobs

## Setup

```bash
# Clone and enter directory
cd techcrunch

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure
# Edit config.yaml and add your OpenRouter API key
```

## Configuration

Edit `config.yaml`:

```yaml
openrouter_api_key: "sk-or-v1-..."  # Get from https://openrouter.ai/keys
rss_url: "https://techcrunch.com/feed/"
fetch_time: "08:00"  # Daily auto-refresh time
```

## Run Locally

```bash
python app.py
```

Visit http://localhost:5000

## Deploy to Render (Free)

1. Push to GitHub

2. Create Web Service on Render:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Environment: `TZ=UTC`

3. Set up auto-refresh:
   - Go to Scheduled Jobs on Render
   - Create new job: `POST /generate` every 6 hours

## Deploy to Vercel

1. Push to GitHub

2. Import in Vercel:
   - Framework: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

3. Set up cron at https://cron-job.org:
   - URL: `https://your-app.vercel.app/api/generate`
   - Schedule: `0 */6 * * *`
   - Method: `POST`

## Project Structure

```
techcrunch/
├── app.py              # Flask web app
├── rss_parser.py       # RSS fetching & image extraction
├── openrouter_insights.py  # AI insights generation
├── storage.py          # JSON file storage
├── scheduler.py        # Daily digest scheduler
├── config.yaml         # Configuration
├── requirements.txt    # Dependencies
├── templates/
│   └── index.html      # Main UI
├── data/               # Stored digests
└── api/
    ├── generate.py     # Vercel serverless function
    └── health.py       # Health check
```

## Tech Stack

- **Flask** - Web framework
- **feedparser** - RSS parsing
- **OpenRouter** - Free AI API (tngtech/deepseek-r1t2-chimera:free)
- **Carbon Design System** - UI components
