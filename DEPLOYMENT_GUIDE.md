# 🚀 Free Deployment Guide

## Deploy to **Render.com** (Recommended - Easiest & Free)

### Step 1: Prepare Code ✅
Already done! Your code is production-ready.

### Step 2: Push to GitHub
```powershell
cd g:\Projects\ml-fastapi-project
git add -A
git commit -m "Deploy: Ready for production"
git push origin main
```

### Step 3: Deploy on Render.com (5 minutes)

1. **Go to:** https://render.com
2. **Sign up** with GitHub (easiest)
3. **Click:** "New +" → "Web Service"
4. **Select:** Your GitHub repository
5. **Configure:**
   - **Name:** `mice-protein-api`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT app.main_simple:app`
   - **Plan:** Free (auto-sleep after 15 min inactivity)

6. **Click:** "Create Web Service"
7. **Wait:** ~2-3 minutes for deployment ⏳
8. **Get URL:** `https://mice-protein-api.onrender.com` ✅

### Step 4: Test Live API
```
Swagger UI:     https://mice-protein-api.onrender.com/docs
Health Check:   https://mice-protein-api.onrender.com/health
Predictions:    https://mice-protein-api.onrender.com/predict
```

---

## Alternative Free Options

### **Railway.app** (Currently Free Credits)
- **Pros:** Better uptime, free $5 credit/month
- **Cons:** Will charge after free credits
- **Deploy:** Similar process, very user-friendly

### **Fly.io** (True Free Tier)
- **Pros:** Truly free tier, fast
- **Cons:** Requires CLI setup
- **Deploy:** `flyctl launch`

---

## Important Notes for Free Tier

⚠️ **Render.com Free Tier:**
- ✅ Unlimited API calls
- ✅ Always publicly accessible
- ❌ App sleeps after 15 min inactivity (wakes up on request)
- ❌ First request takes ~30 seconds
- 🔄 Auto-restart daily

**For Production Use:** Upgrade to Paid plan ($7/month) for always-on performance

---

## Cost Breakdown

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| **Render.com** | Basic (sleeps) | $7/month always-on |
| **Railway.app** | $5 credits/month | Pay as you go |
| **Fly.io** | Always-on (small) | $1.94/month minimum |
| **Heroku** | ❌ Ended 11/2022 | $9+/month |

---

## Quick Deployment Command (All-in-One)

After GitHub push:
1. Go to https://render.com and connect your repo
2. Render will auto-detect `Procfile`
3. Click deploy!

**That's it!** Your API will be live in 3 minutes. 🎉

---

## Monitor Your Deployment

**Render.com Dashboard:**
- View logs in real-time
- Check deployment status
- Monitor resource usage

---

## Example Live API Calls

Once deployed to `https://mice-protein-api.onrender.com`:

```powershell
# Test single prediction
$body = @{
    features = @(0.503, -0.196, ..., 0.189)  # 77 values
    model_type = "svm"
    classification_type = "binary"
} | ConvertTo-Json

Invoke-WebRequest -Uri "https://mice-protein-api.onrender.com/predict" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```

---

## Need Help?

- **Render Docs:** https://render.com/docs
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/
- **Your Repo:** Check main branch for all files

**Ready to deploy? Follow Step 1-4 above!** ✨
