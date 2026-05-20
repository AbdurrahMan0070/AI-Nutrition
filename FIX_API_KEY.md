# 🔑 Fix "No Working Model Found" Error

## The Problem

You're seeing this error:
```
ERROR: No working model found!
Worker exited with code 1
```

This means your **API key is invalid or doesn't have access to Gemini models**.

---

## ✅ Solution: Get a NEW API Key

### Step 1: Get a Fresh API Key

1. **Go to Google AI Studio:**
   ```
   https://makersuite.google.com/app/apikey
   ```

2. **Sign in** with your Google account

3. **Click "Create API Key"**
   - Choose "Create API key in new project" (easiest)
   - OR select an existing project

4. **Copy the key** (starts with `AIza...`)

---

### Step 2: Update API Key in Render

1. **Go to your Render dashboard:**
   ```
   https://dashboard.render.com
   ```

2. **Click on your service** (nutriscan-ai or whatever you named it)

3. **Go to "Environment" tab** (left sidebar)

4. **Find `GEMINI_API_KEY`**
   - If it exists: Click "Edit" → Paste new key → Save
   - If it doesn't exist: Click "Add Environment Variable"
     - Key: `GEMINI_API_KEY`
     - Value: [paste your new key]
     - Click "Save Changes"

5. **Wait for auto-redeploy** (2-3 minutes)

---

### Step 3: Verify It Works

1. **Check the Logs:**
   - Go to "Logs" tab in Render
   - Look for:
     ```
     ✓ Successfully loaded: gemini-1.5-flash
     Model Loaded: True
     ```

2. **Test the Health Endpoint:**
   ```
   https://your-app-name.onrender.com/health
   ```
   
   Should return:
   ```json
   {
     "status": "ok",
     "model_loaded": true,
     "api_key_set": true
   }
   ```

3. **Try analyzing an image!**

---

## 🔍 Common API Key Issues

### Issue 1: Old/Expired Key
**Solution:** Generate a new key from Google AI Studio

### Issue 2: Wrong API
**Solution:** Make sure you're using **Gemini API**, not PaLM or other APIs

### Issue 3: API Not Enabled
**Solution:** 
1. Go to https://console.cloud.google.com
2. Select your project
3. Enable "Generative Language API"

### Issue 4: Spaces in Key
**Solution:** Make sure there are NO spaces before or after the key in Render

### Issue 5: Wrong Environment Variable Name
**Solution:** Must be exactly `GEMINI_API_KEY` (case-sensitive)

---

## 🧪 Test Locally First

Before deploying, test locally:

```bash
# Set your API key
set GEMINI_API_KEY=your_new_key_here

# Test the API
python test_api.py

# If test passes, run the app
python app.py
```

If `test_api.py` shows "SUCCESS", your key is valid!

---

## 📋 Checklist

- [ ] Got NEW API key from https://makersuite.google.com/app/apikey
- [ ] Key starts with `AIza...`
- [ ] Updated in Render Environment tab
- [ ] No spaces before/after the key
- [ ] Variable name is exactly `GEMINI_API_KEY`
- [ ] Waited for Render to redeploy
- [ ] Checked logs show "Model Loaded: True"
- [ ] Health endpoint returns `"model_loaded": true`

---

## 🆘 Still Not Working?

### Option 1: Try a Different Google Account

Some Google accounts have restrictions. Try:
1. Sign out of Google AI Studio
2. Sign in with a different Google account
3. Create a new API key
4. Use that key in Render

### Option 2: Use Railway Instead

Railway is more reliable:

1. Go to https://railway.app
2. Sign in with GitHub
3. New Project → Deploy from GitHub
4. Select your `AI-Nutrition` repo
5. Add environment variable:
   - Key: `GEMINI_API_KEY`
   - Value: [your API key]
6. Deploy!

Railway URL will be: `https://your-app.up.railway.app`

---

## 💡 Pro Tips

1. **Keep your API key secret** - Never share it publicly
2. **Test locally first** - Run `python test_api.py` before deploying
3. **Check quotas** - Free tier has limits (60 requests/minute)
4. **Monitor usage** - Check Google AI Studio for usage stats

---

## ✅ Expected Behavior After Fix

**In Render Logs:**
```
🚀 NutriScan AI Starting...
Port: 10000
API Key Set: True
Model Loaded: True
✓ Successfully loaded: gemini-1.5-flash
```

**Health Endpoint:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "api_key_set": true
}
```

**When Analyzing:**
```
ANALYZE REQUEST RECEIVED
Image: food.jpg
Image loaded: (800, 600), JPEG, RGB
Sending to AI...
Response received!
✓ JSON parsed successfully!
```

---

**Once you see "Model Loaded: True" in the logs, it will work!** 🚀
