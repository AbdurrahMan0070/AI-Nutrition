import os
import json
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import io
import base64

# Setup Flask
app = Flask(__name__)
CORS(app)

# Configure Gemini API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not set!")
    exit(1)

genai.configure(api_key=api_key)
print(f"API configured with key: {api_key[:10]}...")

# List all available models
print("\nListing available models...")
try:
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            print(f"  - {m.name}")
            print(f"    Methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"Could not list models: {e}")
    available_models = []

# Try to find a working vision model
model = None
vision_models = [
    'models/gemini-1.5-flash-latest',
    'models/gemini-1.5-flash',
    'models/gemini-1.5-pro-latest', 
    'models/gemini-1.5-pro',
    'models/gemini-pro-vision'
]

print("\nTrying vision models...")
for model_name in vision_models:
    try:
        print(f"Attempting: {model_name}")
        test_model = genai.GenerativeModel(model_name)
        # Don't test it yet, just create it
        model = test_model
        print(f"✓ Model created: {model_name}")
        break
    except Exception as e:
        print(f"✗ Failed: {e}")

if not model:
    print("ERROR: Could not create any model!")
    exit(1)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'model': str(model._model_name) if model else None}), 200

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    print("\n" + "="*50)
    print("ANALYZE REQUEST")
    print("="*50)
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image'}), 400

    image_file = request.files['image']
    print(f"Image: {image_file.filename}")

    try:
        # Load image
        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes))
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        print(f"Loaded: {img.size}, {img.format}")

        # Prompt
        prompt = """Analyze this food image and return ONLY a JSON object with this structure:
{
    "meal_name": "name of the dish",
    "calories": "estimated range like 400-500",
    "macros": {
        "protein": "30",
        "carbs": "45",
        "fat": "15"
    },
    "comment": "brief encouraging comment about the meal",
    "health_score": "7",
    "ingredients": ["ingredient1", "ingredient2", "ingredient3"]
}

Return ONLY the JSON, no markdown, no extra text."""

        print(f"Calling AI with model: {model._model_name}")
        
        # Try to generate content
        try:
            response = model.generate_content([prompt, img])
            print("✓ Got response from AI")
        except Exception as api_error:
            print(f"✗ API Error: {api_error}")
            # Return fallback with the actual error
            return jsonify({
                "meal_name": "API Error",
                "calories": "500",
                "macros": {"protein": "25", "carbs": "50", "fat": "20"},
                "comment": f"API Error: {str(api_error)[:200]}. Your API key may not have access to vision models. Get a new key from https://makersuite.google.com/app/apikey",
                "health_score": "5",
                "ingredients": ["error"]
            }), 200
        
        # Get text
        text = response.text.strip()
        print(f"Response (first 150 chars): {text[:150]}")
        
        # Clean JSON
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0]
        elif '```' in text:
            text = text.split('```')[1].split('```')[0]
        
        text = text.strip()
        
        # Parse
        data = json.loads(text)
        print("✓ Parsed successfully")
        
        return jsonify(data), 200
        
    except json.JSONDecodeError as e:
        print(f"✗ JSON parse error: {e}")
        return jsonify({
            "meal_name": "Parse Error",
            "calories": "500",
            "macros": {"protein": "25", "carbs": "50", "fat": "20"},
            "comment": "AI returned invalid JSON. Try a clearer image.",
            "health_score": "5",
            "ingredients": ["parse error"]
        }), 200
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "meal_name": "Error",
            "calories": "500",
            "macros": {"protein": "25", "carbs": "50", "fat": "20"},
            "comment": str(e)[:200],
            "health_score": "5",
            "ingredients": ["error"]
        }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n{'='*60}")
    print(f"Starting on port {port}...")
    print(f"Model: {model._model_name if model else 'None'}")
    print(f"{'='*60}\n")
    app.run(host='0.0.0.0', port=port, debug=False)
