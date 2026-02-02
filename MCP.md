# TechCrunch Digest MCP Server

This MCP (Model Context Protocol) server provides access to the TechCrunch Daily Digest.

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Latest digest HTML |
| `/generate` | POST | Generate new digest |
| `/stats` | GET | Storage statistics |
| `/health` | GET | Health check |
| `/progress` | GET | Progress page |
| `/api/status` | GET | Generation status |
| `/api/digest/{date}` | GET | Digest by date |

## Usage with OpenCode

1. Copy `mcp-server.json` to your OpenCode MCP config directory
2. Restart OpenCode to load the new server
3. Use the tools to interact with the digest

## Example API Calls

```bash
# Generate new digest
curl -X POST https://techcrunch-7fgx.onrender.com/generate

# Get stats
curl https://techcrunch-7fgx.onrender.com/stats

# Health check
curl https://techcrunch-7fgx.onrender.com/health

# Get specific digest
curl https://techcrunch-7fgx.onrender.com/api/digest/2026-02-02
```

## Features

- Auto-fetches TechCrunch RSS feed
- Extracts article images from og:image meta tags
- Generates AI insights using OpenRouter (free tier)
- Scheduled auto-refresh every 6 hours
- Dark mode UI with Carbon Design System
