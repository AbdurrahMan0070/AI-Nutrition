import os
import json
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import io

# Setup Flask
app = Flask(__name__)
CORS(app)

# Configure Gemini API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not set!")
    print("Set it with: set GEMINI_API_KEY=your_key_here")
    exit(1)

genai.configure(api_key=api_key)
print(f"API configured with key: {api_key[:10]}...")

# Create model - try multiple models until one works
model = None
models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro-vision']

for model_name in models_to_try:
    try:
        print(f"Trying model: {model_name}")
        model = genai.GenerativeModel(model_name)
        print(f"Model created: {model_name}")
        break
    except Exception as e:
        print(f"Failed {model_name}: {e}")
        continue

if not model:
    print("ERROR: No model available!")
    exit(1)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

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
        
        print(f"Loaded: {img.size}")

        # Simple prompt
        prompt = """Analyze this food and return ONLY a JSON object:
{
    "meal_name": "dish name",
    "calories": "400-500",
    "macros": {"protein": "30", "carbs": "45", "fat": "15"},
    "comment": "brief comment",
    "health_score": "7",
    "ingredients": ["item1", "item2"]
}"""

        print("Calling AI...")
        
        # Call API - version 0.3.2 way
        response = model.generate_content([prompt, img])
        
        print("Got response")
        
        # Get text
        text = response.text.strip()
        print(f"Response: {text[:100]}")
        
        # Clean JSON
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0]
        elif '```' in text:
            text = text.split('```')[1].split('```')[0]
        
        text = text.strip()
        
        # Parse
        data = json.loads(text)
        print("Parsed OK")
        
        return jsonify(data), 200
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        # Return something so it doesn't crash
        return jsonify({
            "meal_name": "Error",
            "calories": "500",
            "macros": {"protein": "25", "carbs": "50", "fat": "20"},
            "comment": str(e),
            "health_score": "5",
            "ingredients": ["error"]
        }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\nStarting on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
