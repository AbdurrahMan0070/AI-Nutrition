# Deploy to Render (Recommended)

## Why Render?
- ✅ **FREE** - No credit card needed
- ✅ **Easy** - Deploy in 5 minutes
- ✅ **Automatic HTTPS** - Secure by default
- ✅ **Environment Variables** - Easy API key management
- ✅ **Auto-deploy** - Updates automatically from GitHub

---

## Step-by-Step Guide

### Step 1: Prepare Your Code

1. **Create a GitHub account** (if you don't have one)
   - Go to github.com
   - Sign up for free

2. **Create a new repository**
   - Click "New repository"
   - Name it: `nutriscan-ai`
   - Make it Public
   - Don't initialize with README
   - Click "Create repository"

---

### Step 2: Push Your Code to GitHub

Open terminal in your project folder and run:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - NutriScan AI"

# Add your GitHub repo (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/nutriscan-ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note:** Replace `YOUR_USERNAME` with your actual GitHub username

---

### Step 3: Deploy on Render

1. **Go to Render**
   - Visit: https://render.com
   - Click "Get Started for Free"
   - Sign up with GitHub (easiest)

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Click "Connect" next to your `nutriscan-ai` repository

3. **Configure the Service**
   - **Name:** `nutriscan-ai` (or any name you want)
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** `Free`

4. **Add Environment Variable**
   - Scroll down to "Environment Variables"
   - Click "Add Environment Variable"
   - **Key:** `GEMINI_API_KEY`
   - **Value:** Your actual API key (paste it here)
   - Click "Add"

5. **Deploy!**
   - Click "Create Web Service"
   - Wait 2-5 minutes for deployment
   - You'll see build logs

---

### Step 4: Access Your App

Once deployed, you'll get a URL like:
```
https://nutriscan-ai.onrender.com
```

Open it in your browser and test!

---

## Updating Your App

Whenever you make changes:

```bash
git add .
git commit -m "Updated features"
git push
```

Render will automatically redeploy! 🚀

---

## Troubleshooting

### Build Failed
- Check build logs in Render dashboard
- Make sure `requirements.txt` is correct
- Make sure all files are pushed to GitHub

### App Crashes
- Check logs in Render dashboard
- Make sure `GEMINI_API_KEY` is set correctly
- Check if API key is valid

### Can't Access App
- Wait a few minutes after deployment
- Check if service is "Live" in dashboard
- Try the URL in incognito mode

---

## Free Tier Limits

Render free tier includes:
- ✅ 750 hours/month (enough for 24/7)
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⚠️ Spins down after 15 min of inactivity
- ⚠️ Takes ~30 seconds to wake up

**Note:** First request after inactivity will be slow (cold start)

---

## Custom Domain (Optional)

1. Buy a domain (e.g., from Namecheap, GoDaddy)
2. In Render dashboard, go to Settings
3. Add custom domain
4. Update DNS records as shown
5. Wait for DNS propagation (up to 24 hours)

---

## Monitoring

In Render dashboard you can:
- View logs
- See metrics (CPU, memory)
- Restart service
- Update environment variables
- See deployment history

---

## Cost

**Free tier:** $0/month
- Perfect for personal projects
- Spins down after inactivity

**Paid tier:** $7/month
- Always on (no spin down)
- More resources
- Better performance

---

## Your App is Now Live! 🎉

Share your URL with anyone:
```
https://nutriscan-ai.onrender.com
```

They can use it without installing anything!
