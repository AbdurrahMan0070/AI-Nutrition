#!/usr/bin/env python
"""
Test script to verify the Gemini API is working
"""

import os
import sys

print("="*60)
print("GEMINI API TEST")
print("="*60)

# Check API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("\n❌ ERROR: GEMINI_API_KEY not set!")
    print("\nTo fix:")
    print("  Windows: set GEMINI_API_KEY=your_key_here")
    print("  Linux/Mac: export GEMINI_API_KEY=your_key_here")
    print("\nGet your key from: https://makersuite.google.com/app/apikey")
    sys.exit(1)

print(f"\n✓ API Key found: {api_key[:10]}...")

# Try to import and configure
try:
    import google.generativeai as genai
    print("✓ google-generativeai package installed")
except ImportError:
    print("\n❌ ERROR: google-generativeai not installed!")
    print("Run: pip install google-generativeai")
    sys.exit(1)

# Configure API
try:
    genai.configure(api_key=api_key)
    print("✓ API configured")
except Exception as e:
    print(f"\n❌ ERROR configuring API: {e}")
    sys.exit(1)

# Try to create a model
print("\nTrying models...")
models_to_try = [
    'gemini-1.5-flash',
    'gemini-1.5-pro',
    'gemini-pro-vision',
    'gemini-pro'
]

working_model = None
for model_name in models_to_try:
    try:
        print(f"  Testing: {model_name}...", end=" ")
        model = genai.GenerativeModel(model_name)
        
        # Try a simple generation
        response = model.generate_content("Say 'Hello'")
        if response.text:
            print("✓ WORKS!")
            working_model = model_name
            break
    except Exception as e:
        print(f"✗ Failed: {str(e)[:50]}")

if working_model:
    print("\n" + "="*60)
    print("✅ SUCCESS!")
    print("="*60)
    print(f"Working model: {working_model}")
    print("\nYour API key is valid and working!")
    print("You can now run: python app.py")
else:
    print("\n" + "="*60)
    print("❌ FAILED")
    print("="*60)
    print("No working model found.")
    print("\nPossible issues:")
    print("1. API key is invalid or expired")
    print("2. API key doesn't have access to Gemini models")
    print("3. You need to enable Gemini API in Google Cloud")
    print("\nGet a new key from: https://makersuite.google.com/app/apikey")
    sys.exit(1)

