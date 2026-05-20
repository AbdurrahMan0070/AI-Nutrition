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
    print("ERROR: GEMINI_API_KEY not set!")
    exit(1)

genai.configure(api_key=api_key)
print(f"API Key configured: {api_key[:10]}...")

# --- Try to find working model ---
print("\nFinding available models...")
model = None
model_names_to_try = [
    'gemini-1.5-flash',
    'gemini-1.5-pro', 
    'gemini-pro-vision',
    'gemini-pro'
]

for model_name in model_names_to_try:
    try:
        print(f"Trying: {model_name}")
        test_model = genai.GenerativeModel(model_name)
        # Test if it works
        test_model.generate_content("test")
        model = test_model
        print(f"SUCCESS! Using: {model_name}\n")
        break
    except Exception as e:
        print(f"Failed: {e}")
        continue

if not model:
    print("ERROR: No working model found!")
    exit(1)

# --- Routes ---
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

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

    try:
        # Read image
        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        print(f"Image loaded: {img.size}, {img.format}")

        # Create prompt
        prompt = """Look at this food image and analyze it.

Return ONLY a JSON object (no other text) with this structure:
{
    "meal_name": "name of the dish",
    "calories": "estimated calories like 400-500",
    "macros": {
        "protein": "30",
        "carbs": "45",
        "fat": "15"
    },
    "comment": "brief comment about the meal",
    "health_score": "7",
    "ingredients": ["ingredient1", "ingredient2", "ingredient3"]
}

Return ONLY the JSON, nothing else."""

        print("Sending to AI...")
        
        # Generate content
        response = model.generate_content([prompt, img])
        
        print("Response received!")
        print(f"Response text: {response.text[:200]}")
        
        # Clean response
        response_text = response.text.strip()
        
        # Remove markdown
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0]
        
        response_text = response_text.strip()
        
        # Parse JSON
        try:
            data = json.loads(response_text)
            print("JSON parsed successfully!")
            print(f"Data: {data}")
            return jsonify(data), 200
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"Text was: {response_text}")
            
            # Return fallback
            fallback = {
                "meal_name": "Delicious Meal",
                "calories": "500-600",
                "macros": {
                    "protein": "25",
                    "carbs": "50",
                    "fat": "20"
                },
                "comment": "Looks tasty! Try a clearer image for better analysis.",
                "health_score": "6",
                "ingredients": ["various ingredients"]
            }
            return jsonify(fallback), 200
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        # Return error with fallback
        return jsonify({
            "meal_name": "Analysis Error",
            "calories": "Unknown",
            "macros": {
                "protein": "0",
                "carbs": "0",
                "fat": "0"
            },
            "comment": f"Error: {str(e)}. Please try again.",
            "health_score": "0",
            "ingredients": ["error"]
        }), 200

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

# --- Run ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\nStarting on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
