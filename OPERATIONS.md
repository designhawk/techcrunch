# TechCrunch Daily Digest - Operations Guide

## Viewing Logs

### On Render

1. Go to your Web Service on Render
2. Click **Logs** tab in the dashboard
3. Real-time logs appear here
4. Filter by: All / Build / Runtime / Restart

![Render Logs](https://render.com/images/docs/logs.png)

**Common log patterns to watch:**
- `[INFO] Fetching images for X articles...` - Image extraction working
- `OpenRouter response for: ...` - AI insights generating
- `OpenRouter error: 429` - Rate limit hit (wait or upgrade)
- `Generated for: 2026-02-02` - Digest created successfully

### Local Development

```bash
# Run with verbose logging
python app.py

# Or set debug mode in config.yaml
debug: true
```

## Troubleshooting

### Issue: "No Digest Available"

**Cause:** Data directory not persisting

**Fix:**
1. Check Render disk is attached
2. Verify `data_dir: "data"` in config
3. Check logs for storage errors

### Issue: Images not showing

**Cause:** Image fetch failed or rate limited

**Fix:**
1. Check logs for `[DEBUG]` messages
2. OpenRouter rate limits affect image fetching too
3. Wait a few minutes, refresh again

### Issue: AI insights missing

**Cause:** OpenRouter quota exceeded

**Fix:**
- Free tier: Wait ~1 minute between requests
- Or upgrade OpenRouter plan

### Issue: Page shows old data

**Cause:** Browser cache

**Fix:**
- Hard refresh: `Ctrl+Shift+R`
- Or clear browser cache

## Scheduled Jobs on Render

1. Go to your Web Service
2. Click **Scheduled Jobs** in left sidebar
3. View job history and next run time
4. Logs appear in the main Logs tab

**Cron expression for 10 AM IST:**
- IST = UTC+5:30
- 10 AM IST = 4:30 AM UTC
- Render schedule: `30 4 * * *`

## Manual Refresh

If auto-refresh fails:

```bash
# Via curl
curl -X POST https://your-app.onrender.com/generate

# Via browser
# Visit: https://your-app.onrender.com/generate
```

## Performance Tips

1. **Image fetching** is slow - runs sequentially
2. **AI insights** - rate limited on free tier
3. **First load** after deploy is slowest
4. **Subsequent loads** use cached data (fast)

## Health Check

```bash
curl https://your-app.onrender.com/health
```

Returns: `{"status": "ok", "timestamp": "..."}`
