import os
import json
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import io
import base64

# --- 1. Setup ---
app = Flask(__name__)
CORS(app)

# --- 2. Configure Gemini API ---
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise KeyError("GEMINI_API_KEY not found")
    genai.configure(api_key=api_key)
    print("API configured successfully")
    print(f"API Key starts with: {api_key[:10]}...")
except KeyError:
    print("=" * 60)
    print("ERROR: GEMINI_API_KEY environment variable not set.")
    print("=" * 60)
    print("\nTo fix this:")
    print("1. Get your API key from: https://makersuite.google.com/app/apikey")
    print("2. Set it as an environment variable:")
    print("   Windows CMD: set GEMINI_API_KEY=your_api_key_here")
    print("   Windows PowerShell: $env:GEMINI_API_KEY='your_api_key_here'")
    print("   Then run: python app.py")
    print("=" * 60)
    exit(1)

# --- 3. List available models and choose the best one ---
print("\nChecking available models...")
try:
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            available_models.append(m.name)
            print(f"  - {m.name}")
    
    # Try to use the best vision model available
    model_name = None
    preferred_models = [
        'models/gemini-1.5-flash-latest',
        'models/gemini-1.5-flash',
        'models/gemini-pro-vision',
        'models/gemini-1.5-pro-latest',
        'models/gemini-1.5-pro'
    ]
    
    for preferred in preferred_models:
        if preferred in available_models:
            model_name = preferred
            break
    
    if not model_name and available_models:
        # Use the first available model
        model_name = available_models[0]
    
    if not model_name:
        raise Exception("No suitable model found")
    
    print(f"\nUsing model: {model_name}")
    model = genai.GenerativeModel(model_name)
    
except Exception as e:
    print(f"Error listing models: {e}")
    print("Falling back to gemini-pro-vision")
    model = genai.GenerativeModel('gemini-pro-vision')

# --- 4. Serve the HTML file ---
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# --- 5. The API Route for Image Analysis ---
@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    print("\n" + "="*50)
    print("RECEIVED IMAGE ANALYSIS REQUEST")
    print("="*50)
    
    if 'image' not in request.files:
        print("ERROR: No image file in request")
        return jsonify({'error': 'No image file provided.'}), 400

    image_file = request.files['image']
    print(f"Image filename: {image_file.filename}")
    print(f"Image content type: {image_file.content_type}")

    try:
        # Read and process image
        image_bytes = image_file.read()
        print(f"Image size: {len(image_bytes)} bytes")
        
        img = Image.open(io.BytesIO(image_bytes))
        print(f"Image loaded: {img.size} pixels, {img.format} format, {img.mode} mode")

        # Convert to RGB if needed
        if img.mode != 'RGB':
            print(f"Converting from {img.mode} to RGB")
            img = img.convert('RGB')

        print("Preparing prompt...")
        
        prompt = """Analyze this food image and provide nutritional information.

You MUST respond with ONLY a valid JSON object in this exact format (no other text):

{
    "meal_name": "A short name for this meal",
    "calories": "Estimated calorie range like 400-500",
    "macros": {
        "protein": "30",
        "carbs": "45",
        "fat": "15"
    },
    "comment": "A brief encouraging comment",
    "health_score": "7",
    "ingredients": ["ingredient1", "ingredient2", "ingredient3"]
}

Important: Return ONLY the JSON, nothing else. No markdown, no explanations."""
        
        print("Sending to Gemini AI...")
        print(f"Using model: {model._model_name}")
        
        # Try to generate content
        response = model.generate_content([prompt, img])
        
        print("Response received!")
        print(f"Response object type: {type(response)}")
        
        # Check if response has text
        if not hasattr(response, 'text'):
            print("ERROR: Response has no text attribute")
            print(f"Response attributes: {dir(response)}")
            return jsonify({'error': 'Invalid response from AI - no text'}), 500
        
        response_text = response.text.strip()
        print(f"Raw response length: {len(response_text)} characters")
        print(f"Raw response (first 200 chars): {response_text[:200]}")
        
        # Clean the response
        if response_text.startswith('```json'):
            response_text = response_text[7:]
            print("Removed ```json prefix")
        elif response_text.startswith('```'):
            response_text = response_text[3:]
            print("Removed ``` prefix")
        
        if response_text.endswith('```'):
            response_text = response_text[:-3]
            print("Removed ``` suffix")
        
        response_text = response_text.strip()
        print(f"Cleaned response (first 200 chars): {response_text[:200]}")
        
        # Try to parse JSON
        try:
            data = json.loads(response_text)
            print("JSON parsed successfully!")
            print(f"Parsed data keys: {data.keys()}")
            return jsonify(data), 200
            
        except json.JSONDecodeError as je:
            print(f"JSON DECODE ERROR: {je}")
            print(f"Failed to parse: {response_text}")
            
            # Return a fallback response
            fallback = {
                "meal_name": "Meal Analysis",
                "calories": "500-600",
                "macros": {
                    "protein": "25",
                    "carbs": "50",
                    "fat": "20"
                },
                "comment": "Unable to fully analyze. Please try with a clearer image.",
                "health_score": "5",
                "ingredients": ["various ingredients"]
            }
            print("Returning fallback response")
            return jsonify(fallback), 200
    
    except Exception as e:
        print(f"EXCEPTION OCCURRED: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return jsonify({'error': f'{type(e).__name__}: {str(e)}'}), 500

# --- 6. Health check endpoint ---
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'model': model._model_name if hasattr(model, '_model_name') else 'unknown'
    }), 200

# --- 7. Run the Server ---
if __name__ == '__main__':
    print("\n" + "="*60)
    print("AI NUTRITION APP STARTING...")
    print("="*60)
    print("Open your browser: http://127.0.0.1:5000")
    print("Health check: http://127.0.0.1:5000/health")
    print("="*60 + "\n")
    
    # Get port from environment variable (for deployment) or use 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run with gunicorn in production, Flask dev server locally
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
