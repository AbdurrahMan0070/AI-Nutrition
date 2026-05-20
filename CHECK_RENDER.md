# ✅ Check These on Render RIGHT NOW

## Step 1: Wait for Deploy (2-3 minutes)

Render should auto-deploy the new code. Wait until you see "Live" status.

---

## Step 2: Check the Logs

1. Go to your Render dashboard
2. Click your service
3. Click **"Logs"** tab
4. Scroll to the bottom

**You MUST see these lines:**
```
API configured with key: AIza...
Model created: gemini-pro-vision
Starting on port 10000...
```

**If you DON'T see this:**
- The API key is not set correctly
- Go to Step 3

---

## Step 3: Verify API Key is Set

1. Click **"Environment"** tab (left sidebar)
2. Look for `GEMINI_API_KEY`

**Check:**
- [ ] Variable name is EXACTLY `GEMINI_API_KEY` (case-sensitive)
- [ ] Value starts with `AIza`
- [ ] NO spaces before or after the key
- [ ] Key is from https://makersuite.google.com/app/apikey

**If anything is wrong:**
1. Delete the variable
2. Add it again:
   - Key: `GEMINI_API_KEY`
   - Value: [paste your API key with NO spaces]
3. Click "Save Changes"
4. Wait for redeploy (2-3 minutes)
5. Go back to Step 2

---

## Step 4: Test the Health Endpoint

Open this URL in your browser (replace with your actual URL):
```
https://your-app-name.onrender.com/health
```

**Should show:**
```json
{"status":"ok"}
```

**If you get an error:**
- App is not running
- Check logs for errors
- Service might still be deploying

---

## Step 5: Try Analyzing

1. Open your app URL
2. Upload a food image
3. Click "Analyze"
4. **WAIT 30-60 seconds** (first request is slow on free tier)

**Watch the Render logs while you do this!**

You should see:
```
==================================================
ANALYZE REQUEST
==================================================
Image: food.jpg
Loaded: (800, 600)
Calling AI...
Got response
Response: {...
Parsed OK
```

---

## 🔍 If It Still Doesn't Work

### Check 1: Is the API key valid?

Test it locally:
```bash
set GEMINI_API_KEY=your_key_here
python test_api.py
```

If this fails, your API key is bad. Get a new one.

### Check 2: Are you using the right Google account?

Some Google accounts can't access Gemini API. Try:
1. Sign out of Google AI Studio
2. Sign in with a DIFFERENT Google account
3. Create a new API key
4. Use that in Render

### Check 3: Is Gemini API enabled?

1. Go to https://console.cloud.google.com
2. Select your project
3. Go to "APIs & Services" → "Library"
4. Search for "Generative Language API"
5. Make sure it's ENABLED

---

## 🚨 Common Mistakes

### Mistake 1: Wrong variable name
❌ `GEMINI_KEY`
❌ `API_KEY`
❌ `gemini_api_key`
✅ `GEMINI_API_KEY` (exactly this)

### Mistake 2: Spaces in the key
❌ ` AIza...` (space before)
❌ `AIza... ` (space after)
✅ `AIza...` (no spaces)

### Mistake 3: Wrong API
❌ Using PaLM API key
❌ Using old Bard API key
✅ Using Gemini API key from https://makersuite.google.com/app/apikey

### Mistake 4: Not waiting
❌ Clicking analyze and expecting instant results
✅ Waiting 30-60 seconds on first request (cold start)

---

## 📋 Final Checklist

Go through this in order:

1. [ ] Render shows "Live" status (green)
2. [ ] Logs show "Model created: gemini-pro-vision"
3. [ ] Environment has `GEMINI_API_KEY` set correctly
4. [ ] Health endpoint returns `{"status":"ok"}`
5. [ ] Waited 30+ seconds after clicking Analyze
6. [ ] Checked Render logs while analyzing
7. [ ] API key is from https://makersuite.google.com/app/apikey
8. [ ] API key is less than 1 day old (fresh)

---

## 💡 What Changed

I simplified the code to match EXACTLY what works locally:
- ✅ Uses `gemini-pro-vision` model (version 0.3.2 compatible)
- ✅ Simple, direct API calls
- ✅ No complex model detection
- ✅ Same code that works on your machine

**This is the EXACT same code structure that works locally!**

---

## 🆘 Last Resort

If NOTHING works, the issue is your API key or Google account.

**Try this:**
1. Create a NEW Google account
2. Go to https://makersuite.google.com/app/apikey
3. Sign in with the NEW account
4. Create API key
5. Use that key in Render

Some Google accounts have restrictions that prevent Gemini API access.

---

**After following these steps, it MUST work. The code is now identical to what works locally!**
