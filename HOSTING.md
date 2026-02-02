# Free Hosting Alternatives

## Tier 1: Best Options

### 1. **Render** (Recommended)
- Free: 750 hours/month
- Auto-deploy from GitHub
- Persistent disk for data
- Cron jobs (free tier available)

**Deploy:**
1. Connect GitHub → New Web Service
2. Build: `pip install -r requirements.txt`
3. Start: `python app.py`
4. Environment: `TZ=UTC`

**Auto-refresh:** Render Scheduled Jobs (free)
- Create cron job calling `POST /generate` every 6 hours

---

### 2. **Railway**
- Free: $5 credit/month
- Auto-deploy from GitHub
- Simple setup

**Deploy:**
```bash
npm i -g @railway/cli
railway login
railway init
railway up
```

**Auto-refresh:** Use Railway's cron add-on or cron-job.org

---

### 3. **PythonAnywhere**
- Free tier: Always free
- Web hosting included
- Scheduled tasks (free)

**Setup:**
1. Sign up at pythonanywhere.com
2. Upload code or git clone
3. Configure WSGI file
4. Enable "Always-on" task (paid) or use scheduled tasks

**Auto-refresh:** PythonAnywhere's Tasks tab

---

## Tier 2: Good Alternatives

### 4. **Fly.io**
- Free: Unlimited compute (share $5/month)
- Edge locations worldwide
- Persistent volumes

**Deploy:**
```bash
brew install flyctl
fly auth login
fly launch
fly deploy
```

---

### 5. **Deno Deploy**
- Free: 100K requests/day
- Edge functions
- Deno/TypeScript native (Python via edge-functions)

**Note:** Would need to convert to JavaScript/TypeScript

---

### 6. **Cyclic**
- Free: Unlimited requests
- Full-stack hosting
- Auto-deploy from GitHub

---

## Comparison Table

| Service | Free Hours | Persistent Storage | Cron | Auto-deploy |
|---------|------------|-------------------|------|-------------|
| Render | 750/month | Yes (disk) | Yes (free tier) | Yes |
| Railway | $5 credit | Yes | Via add-on | Yes |
| PythonAnywhere | Always | Yes | Yes | No |
| Fly.io | Unlimited | Yes | Yes | Yes |
| Cyclic | Unlimited | No | ? | Yes |

---

## My Recommendation

**Render** is the best choice for your use case:
- ✅ Persistent storage (your digests persist)
- ✅ Free tier sufficient for personal use
- ✅ Cron jobs included
- ✅ Easy GitHub integration
- ✅ No credit card required

**Setup:**
1. https://render.com → New Web Service
2. Connect GitHub repo
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python app.py`
5. Add Environment Variable: `TZ=UTC`
6. Create Scheduled Job: `0 */6 * * *` → `POST /generate`
