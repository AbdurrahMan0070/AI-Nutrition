# Deploy to Railway

## Why Railway?
- ✅ **$5 free credit/month** - Generous free tier
- ✅ **Super fast** - Deploys in seconds
- ✅ **Modern UI** - Beautiful dashboard
- ✅ **Easy setup** - One-click deploy
- ✅ **Great for Python** - Excellent Python support

---

## Step-by-Step Guide

### Step 1: Push to GitHub

1. **Create GitHub repository**
   - Go to github.com
   - Create new repo: `nutriscan-ai`

2. **Push your code**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/nutriscan-ai.git
git branch -M main
git push -u origin main
```

---

### Step 2: Deploy on Railway

1. **Go to Railway**
   - Visit: https://railway.app
   - Click "Login" → Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `nutriscan-ai` repository
   - Click "Deploy Now"

3. **Add Environment Variable**
   - Click on your service
   - Go to "Variables" tab
   - Click "New Variable"
   - **Variable:** `GEMINI_API_KEY`
   - **Value:** Your API key
   - Click "Add"

4. **Wait for Deployment**
   - Railway will automatically detect it's a Python app
   - Build takes 1-2 minutes
   - You'll see "Active" when ready

---

### Step 3: Get Your URL

1. Click on your service
2. Go to "Settings" tab
3. Scroll to "Domains"
4. Click "Generate Domain"
5. You'll get a URL like: `nutriscan-ai.up.railway.app`

---

## Your App is Live! 🚀

Open your Railway URL and test the app!

---

## Updating Your App

```bash
git add .
git commit -m "Updates"
git push
```

Railway auto-deploys on every push!

---

## Free Tier

Railway gives you:
- ✅ $5 free credit per month
- ✅ ~500 hours of runtime
- ✅ No credit card needed initially
- ⚠️ Need to add card after trial

---

## Monitoring

Railway dashboard shows:
- Real-time logs
- Metrics (CPU, RAM, Network)
- Deployment history
- Build logs

---

## Troubleshooting

### Build Failed
- Check logs in Railway dashboard
- Verify `requirements.txt` is correct

### App Not Responding
- Check if service is "Active"
- View logs for errors
- Verify `GEMINI_API_KEY` is set

### Out of Credits
- Add payment method
- Or wait for next month's $5 credit

---

## Cost

**Free:** $5 credit/month
**Paid:** Pay as you go after credits

Typical usage: ~$2-5/month for small apps

---

Your app is now deployed on Railway! 🎉
