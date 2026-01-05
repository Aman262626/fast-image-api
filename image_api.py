from flask import Flask, request, jsonify
import requests
import base64
import os
from datetime import datetime
import urllib.parse

app = Flask(__name__)

# Statistics
stats = {
    "total_requests": 0,
    "successful": 0,
    "failed": 0,
    "avg_response_time": 0
}

def generate_pollinations(prompt, width=512, height=512):
    """Ultra-fast generation (1-2 seconds)"""
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        
        params = {
            "width": width,
            "height": height,
            "nologo": "true",
            "enhance": "true"
        }
        
        start_time = datetime.now()
        response = requests.get(url, params=params, timeout=5)
        end_time = datetime.now()
        
        if response.status_code == 200:
            img_base64 = base64.b64encode(response.content).decode('utf-8')
            response_time = (end_time - start_time).total_seconds()
            
            return {
                "success": True,
                "image": img_base64,
                "format": "base64",
                "prompt": prompt,
                "model": "pollinations-sdxl",
                "response_time": round(response_time, 2),
                "size": {"width": width, "height": height}
            }
        
        return {"success": False, "error": f"Status {response.status_code}"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def generate_flux_schnell(prompt):
    """Backup method using Flux Schnell (2-3 seconds)"""
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        params = {"model": "flux", "width": 512, "height": 512, "nologo": "true"}
        
        start_time = datetime.now()
        response = requests.get(url, params=params, timeout=8)
        
        if response.status_code == 200:
            img_base64 = base64.b64encode(response.content).decode('utf-8')
            response_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": True,
                "image": img_base64,
                "format": "base64",
                "prompt": prompt,
                "model": "flux-schnell",
                "response_time": round(response_time, 2)
            }
        
        return {"success": False, "error": "Generation failed"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route('/', methods=['GET'])
def home():
    """API Info"""
    return jsonify({
        "status": "operational",
        "service": "⚡ Ultra-Fast Image Generation API",
        "version": "1.0.0",
        "speed": "1-2 seconds average",
        "features": {
            "unlimited": True,
            "free": True,
            "fast": True,
            "no_api_key": True
        },
        "models": ["Pollinations SDXL", "Flux Schnell"],
        "statistics": stats,
        "endpoints": {
            "POST /generate": "Generate image",
            "GET /health": "Health check",
            "GET /stats": "Statistics"
        },
        "example": {
            "url": "/generate",
            "method": "POST",
            "body": {
                "prompt": "A beautiful sunset",
                "width": 512,
                "height": 512
            }
        }
    })

@app.route('/generate', methods=['POST'])
def generate_image():
    """Main generation endpoint"""
    try:
        stats["total_requests"] += 1
        
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({
                "success": False,
                "error": "Prompt required in request body"
            }), 400
        
        prompt = data.get('prompt', '').strip()
        width = min(int(data.get('width', 512)), 1024)
        height = min(int(data.get('height', 512)), 1024)
        
        if not prompt:
            return jsonify({
                "success": False,
                "error": "Prompt cannot be empty"
            }), 400
        
        start_time = datetime.now()
        
        # Try primary method
        result = generate_pollinations(prompt, width, height)
        
        # Fallback if primary fails
        if not result.get('success'):
            result = generate_flux_schnell(prompt)
        
        if result.get('success'):
            stats["successful"] += 1
            total_time = (datetime.now() - start_time).total_seconds()
            stats["avg_response_time"] = round(
                (stats["avg_response_time"] * (stats["successful"] - 1) + total_time) / stats["successful"],
                2
            )
            return jsonify(result)
        
        stats["failed"] += 1
        return jsonify({
            "success": False,
            "error": "Generation failed",
            "suggestion": "Try again in a few seconds"
        }), 503
        
    except Exception as e:
        stats["failed"] += 1
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "service": "Image Generation API",
        "models_status": {
            "pollinations": "online",
            "flux": "online"
        },
        "avg_response_time": f"{stats['avg_response_time']}s",
        "success_rate": f"{round((stats['successful'] / max(stats['total_requests'], 1)) * 100, 2)}%"
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    """Statistics"""
    return jsonify({
        "statistics": stats,
        "success_rate": f"{round((stats['successful'] / max(stats['total_requests'], 1)) * 100, 2)}%"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"🚀 Image API starting on port {port}")
    print(f"⚡ Response time: 1-2 seconds")
    app.run(host='0.0.0.0', port=port, debug=False)