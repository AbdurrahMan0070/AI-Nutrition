#!/usr/bin/env python
"""
Test script to verify the Gemini API is working
"""

import os
import google.generativeai as genai
from PIL import Image
import io

print("="*60)
print("GEMINI API TEST")
print("="*60)

# Check API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("\nERROR: GEMINI_API_KEY not set!")
    print("Set it with: set GEMINI_API_KEY=your_key_here")
    exit(1)

print(f"\nAPI Key found: {api_key[:10]}...")

# Configure API
try:
    genai.configure(api_key=api_key)
    print("API configured successfully")
except Exception as e:
    print(f"ERROR configuring API: {e}")
    exit(1)

# List available models
print("\nAvailable models:")
try:
    models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            models.append(m.name)
            print(f"  - {m.name}")
    
    if not models:
        print("  No models found!")
        exit(1)
        
except Exception as e:
    print(f"ERROR listing models: {e}")
    exit(1)

# Try to use a model
print("\nTesting model...")
try:
    # Try different models
    model_name = None
    for preferred in ['models/gemini-1.5-flash', 'models/gemini-pro-vision', 'models/gemini-pro']:
        if preferred in models:
            model_name = preferred
            break
    
    if not model_name:
        model_name = models[0]
    
    print(f"Using: {model_name}")
    model = genai.GenerativeModel(model_name)
    
    # Test with a simple text prompt
    print("\nTesting with text prompt...")
    response = model.generate_content("Say 'Hello, the API is working!'")
    print(f"Response: {response.text}")
    
    print("\n" + "="*60)
    print("SUCCESS! API is working correctly")
    print("="*60)
    print("\nYou can now run: python app.py")
    
except Exception as e:
    print(f"\nERROR testing model: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
