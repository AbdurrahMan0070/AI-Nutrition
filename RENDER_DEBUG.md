# 🔧 Render Debugging Guide

## If Analysis Still Doesn't Work on Render

### Step 1: Check Render Logs

1. Go to your Render dashboard
2. Click on your service
3. Click "Logs" tab
4. Look for these messages when you click Analyze:

**Good signs:**
```
ANALYZE REQUEST RECEIVED
Image: food.jpg
Image loaded: (800, 600), JPEG
Sending to AI...
Response received!
JSON parsed successfully!
```

**Bad signs:**
```
ERROR: GEMINI_API_KEY not set!
ERROR: No working model found!
```

---

### Step 2: Verify API Key is Set

1. In Render dashboard, go to your service
2. Click "Environment" tab
3. Check if `GEMINI_API_KEY` exists
4. Make sure there are no extra spaces
5. Try regenerating a new API key from Google

---

### Step 3: Check Build Logs

1. Go to "Events" tab in Render
2. Look at the latest deploy
3. Check if build succeeded
4. Look for errors during startup

**Should see:**
```
Finding available models...
Trying: gemini-1.5-flash
SUCCESS! Using: gemini-1.5-flash
```

---

### Step 4: Test the Health Endpoint

Open this URL in your browser:
```
https://your-app-name.onrender.com/health
```

Should return:
```json
{"status": "ok"}
```

If this doesn't work, the app isn't running at all.

---

### Step 5: Check Browser Console

1. Open your deployed app
2. Press F12
3. Go to Console tab
4. Upload image and click Analyze
5. Look for errors

**Common errors:**

**"Failed to fetch"**
- Backend is down
- Check Render logs

**"Request timeout"**
- Image too large
- Try smaller image

**"Network error"**
- CORS issue
- Check if app is running

---

### Step 6: Manual Redeploy

Sometimes Render needs a fresh deploy:

1. Go to your service in Render
2. Click "Manual Deploy"
3. Select "Clear build cache & deploy"
4. Wait for deployment
5. Try again

---

### Step 7: Check API Key Validity

Your API key might be invalid:

1. Go to https://makersuite.google.com/app/apikey
2. Create a NEW API key
3. In Render, update `GEMINI_API_KEY` with new key
4. Service will auto-redeploy
5. Try again

---

### Step 8: Check Free Tier Limits

Render free tier:
- Spins down after 15 min inactivity
- First request takes ~30 seconds to wake up
- This is NORMAL

**Solution:**
- Wait 30-60 seconds on first request
- Or upgrade to paid tier ($7/month)

---

## Common Issues & Solutions

### Issue: "It just goes back to preview"

**Cause:** JavaScript error or network issue

**Solution:**
1. Open browser console (F12)
2. Look for red errors
3. Check Render logs
4. Try different image

---

### Issue: "Stuck on loading forever"

**Cause:** Backend timeout or crash

**Solution:**
1. Check Render logs for errors
2. Verify API key is set
3. Try redeploying
4. Check if service is "Live"

---

### Issue: "Shows error in results"

**Cause:** AI returned error but app handled it

**Solution:**
- This is actually working! The app shows fallback data
- Check Render logs for actual error
- Usually means API key issue or model not available

---

## Quick Fixes

### Fix 1: Regenerate API Key
1. Get new key from Google
2. Update in Render environment
3. Wait for redeploy
4. Test again

### Fix 2: Clear Cache & Redeploy
1. Manual Deploy → Clear build cache
2. Wait for completion
3. Test again

### Fix 3: Check Service Status
1. Make sure service shows "Live" (green)
2. If not, check logs for errors
3. Restart service if needed

### Fix 4: Test Locally First
```bash
set GEMINI_API_KEY=your_key
python app.py
```
If it works locally but not on Render, it's a deployment issue.

---

## Still Not Working?

### Get Help:

1. **Check Render Logs** - Copy the full log output
2. **Check Browser Console** - Copy all error messages
3. **Test Health Endpoint** - Does `/health` work?
4. **Verify API Key** - Is it set correctly in Render?

### Share These:
- Render logs (when you click Analyze)
- Browser console output (F12)
- Your Render service URL
- Screenshot of environment variables (hide the key value)

---

## Expected Behavior

### First Request (Cold Start)
1. Click Analyze
2. Wait 30-60 seconds (app waking up)
3. See results

### Subsequent Requests
1. Click Analyze
2. Wait 5-10 seconds
3. See results

---

## Success Checklist

- [ ] Service is "Live" in Render
- [ ] `GEMINI_API_KEY` is set in Environment
- [ ] Health endpoint returns `{"status": "ok"}`
- [ ] Logs show "SUCCESS! Using: gemini-..."
- [ ] Browser console shows no errors
- [ ] Waited 30+ seconds on first request

If all checked, it should work!

---

## Alternative: Try Railway

If Render keeps failing, try Railway instead:

1. Go to https://railway.app
2. Sign in with GitHub
3. New Project → Deploy from GitHub
4. Select your repo
5. Add `GEMINI_API_KEY`
6. Deploy

Railway is faster and more reliable (but uses credits).

---

**The new code has better error handling and will show you exactly what's wrong!**
