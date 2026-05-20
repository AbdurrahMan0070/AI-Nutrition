import os
import json
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import io

# --- Setup ---
app = Flask(__name__)
CORS(app)

# --- Configure Gemini API ---
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY not set! App will run but analysis won't work.")
    model = None
else:
    genai.configure(api_key=api_key)
    print(f"API Key configured: {api_key[:10]}...")
    
    # --- Setup model ---
    print("\nSetting up AI model...")
    model = None
    
    # List of models to try (in order of preference)
    models_to_try = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro-vision',
        'gemini-pro'
    ]
    
    for model_name in models_to_try:
        try:
            print(f"Trying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            print(f"✓ Successfully loaded: {model_name}")
            break
        except Exception as e:
            print(f"✗ Failed to load {model_name}: {str(e)}")
            continue
    
    if not model:
        print("WARNING: Could not load any model. Using fallback mode.")
        print("Check your API key at: https://makersuite.google.com/app/apikey")

# --- Routes ---
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None,
        'api_key_set': api_key is not None
    }), 200

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    print("\n" + "="*50)
    print("ANALYZE REQUEST RECEIVED")
    print("="*50)
    
    if 'image' not in request.files:
        print("ERROR: No image in request")
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    print(f"Image: {image_file.filename}")

    # Check if model is available
    if not model:
        print("ERROR: No model available")
        return jsonify({
            "meal_name": "Configuration Error",
            "calories": "500-600",
            "macros": {
                "protein": "25",
                "carbs": "50",
                "fat": "20"
            },
            "comment": "API key not configured. Please set GEMINI_API_KEY environment variable.",
            "health_score": "5",
            "ingredients": ["configuration", "error"]
        }), 200

    try:
        # Read and process image
        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        print(f"Image loaded: {img.size}, {img.format}, {img.mode}")

        # Create prompt
        prompt = """Analyze this food image.

Return ONLY a JSON object with this exact structure (no markdown, no extra text):
{
    "meal_name": "name of the dish",
    "calories": "estimated range like 400-500",
    "macros": {
        "protein": "30",
        "carbs": "45",
        "fat": "15"
    },
    "comment": "brief encouraging comment",
    "health_score": "7",
    "ingredients": ["ingredient1", "ingredient2", "ingredient3"]
}"""

        print("Sending to AI...")
        
        # Generate content with timeout
        response = model.generate_content([prompt, img])
        
        print("Response received!")
        
        # Get response text
        if not hasattr(response, 'text') or not response.text:
            print("ERROR: No text in response")
            raise Exception("AI returned empty response")
        
        response_text = response.text.strip()
        print(f"Response (first 200 chars): {response_text[:200]}")
        
        # Clean markdown if present
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        # Parse JSON
        try:
            data = json.loads(response_text)
            print("✓ JSON parsed successfully!")
            
            # Validate required fields
            required_fields = ['meal_name', 'calories', 'macros', 'comment', 'health_score', 'ingredients']
            for field in required_fields:
                if field not in data:
                    print(f"WARNING: Missing field: {field}")
                    data[field] = "Unknown" if field != 'ingredients' else []
            
            return jsonify(data), 200
            
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"Failed text: {response_text}")
            raise Exception("AI returned invalid JSON")
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        # Return fallback data
        return jsonify({
            "meal_name": "Analysis Unavailable",
            "calories": "500-600",
            "macros": {
                "protein": "25",
                "carbs": "50",
                "fat": "20"
            },
            "comment": f"Could not analyze image. Error: {str(e)[:100]}",
            "health_score": "5",
            "ingredients": ["error occurred"]
        }), 200

# --- Run ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "="*60)
    print("🚀 NutriScan AI Starting...")
    print("="*60)
    print(f"Port: {port}")
    print(f"API Key Set: {api_key is not None}")
    print(f"Model Loaded: {model is not None}")
    print("="*60 + "\n")
    
    # Start the app even if model isn't loaded
    app.run(host='0.0.0.0', port=port, debug=False)
