import os
import json
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import io
import base64

# Setup Flask
app = Flask(__name__)
CORS(app)

# Get API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not set!")
    exit(1)

print(f"API Key: {api_key[:10]}...")

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
        # Load and convert image
        image_bytes = image_file.read()
        img = Image.open(io.BytesIO(image_bytes))
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large
        max_size = 1024
        if img.width > max_size or img.height > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        print(f"Image processed: {img.size}")

        # Prepare API request using REST API directly
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        payload = {
            "contents": [{
                "parts": [
                    {
                        "text": """Analyze this food image and return ONLY a JSON object:
{
    "meal_name": "name of dish",
    "calories": "400-500",
    "macros": {"protein": "30", "carbs": "45", "fat": "15"},
    "comment": "brief comment",
    "health_score": "7",
    "ingredients": ["item1", "item2", "item3"]
}
Return ONLY valid JSON, no markdown."""
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_base64
                        }
                    }
                ]
            }]
        }
        
        print("Calling Gemini API via REST...")
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error response: {response.text}")
            raise Exception(f"API returned {response.status_code}: {response.text[:200]}")
        
        result = response.json()
        print("Got response from API")
        
        # Extract text from response
        if 'candidates' in result and len(result['candidates']) > 0:
            text = result['candidates'][0]['content']['parts'][0]['text']
            print(f"Response text: {text[:150]}")
            
            # Clean JSON
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
            
            text = text.strip()
            
            # Parse JSON
            data = json.loads(text)
            print("✓ Success!")
            
            return jsonify(data), 200
        else:
            raise Exception("No response from API")
        
    except requests.exceptions.Timeout:
        print("✗ Timeout")
        return jsonify({
            "meal_name": "Timeout",
            "calories": "500",
            "macros": {"protein": "25", "carbs": "50", "fat": "20"},
            "comment": "Request timed out. Try again.",
            "health_score": "5",
            "ingredients": ["timeout"]
        }), 200
        
    except json.JSONDecodeError as e:
        print(f"✗ JSON error: {e}")
        return jsonify({
            "meal_name": "Parse Error",
            "calories": "500",
            "macros": {"protein": "25", "carbs": "50", "fat": "20"},
            "comment": "AI returned invalid JSON. Try a different image.",
            "health_score": "5",
            "ingredients": ["error"]
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
    print(f"\nStarting on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
