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

@app.route('/test-models')
def test_models():
    """Test which models are available with this API key"""
    results = []
    
    # Test different API versions and models
    test_configs = [
        ("v1", "gemini-pro"),
        ("v1", "gemini-pro-vision"),
        ("v1beta", "gemini-1.5-flash"),
        ("v1beta", "gemini-1.5-flash-latest"),
        ("v1beta", "gemini-1.5-pro"),
        ("v1beta", "gemini-1.5-pro-latest"),
        ("v1beta", "gemini-pro"),
        ("v1beta", "gemini-pro-vision"),
    ]
    
    for api_version, model_name in test_configs:
        try:
            url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model_name}?key={api_key}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                results.append({
                    "api_version": api_version,
                    "model": model_name,
                    "status": "✓ Available",
                    "details": response.json()
                })
            else:
                results.append({
                    "api_version": api_version,
                    "model": model_name,
                    "status": f"✗ Not available ({response.status_code})",
                    "error": response.text[:200]
                })
        except Exception as e:
            results.append({
                "api_version": api_version,
                "model": model_name,
                "status": "✗ Error",
                "error": str(e)
            })
    
    return jsonify({
        "api_key": f"{api_key[:10]}...",
        "models_tested": len(test_configs),
        "results": results
    }), 200

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
        # Try v1 API first (stable), then v1beta
        models_to_try = [
            ("v1", "gemini-pro-vision"),
            ("v1beta", "gemini-1.5-flash"),
            ("v1beta", "gemini-1.5-pro"),
        ]
        
        last_error = None
        
        for api_version, model_name in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model_name}:generateContent?key={api_key}"
                
                print(f"Trying: {api_version}/{model_name}")
                
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
                
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                
                print(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✓ Success with {api_version}/{model_name}")
                    
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
                        print("✓ Parsed successfully")
                        
                        return jsonify(data), 200
                    else:
                        raise Exception("No response from API")
                else:
                    last_error = f"{response.status_code}: {response.text[:200]}"
                    print(f"✗ Failed: {last_error}")
                    continue
                    
            except Exception as e:
                last_error = str(e)
                print(f"✗ Error with {api_version}/{model_name}: {e}")
                continue
        
        # If we get here, all models failed
        raise Exception(f"All models failed. Last error: {last_error}")
        
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
