# ⚡ Ultra-Fast Image Generation API

**Generate high-quality images in 1-2 seconds | Unlimited | Completely Free | No API Keys**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Render-purple.svg)](https://render.com)

## 🚀 Features

- ⚡ **Ultra-Fast**: 1-2 seconds average response time
- 🆓 **Completely Free**: No API keys, no hidden costs
- ♾️ **Unlimited**: Generate as many images as you want
- 🎨 **High Quality**: SDXL & Flux Schnell models
- 🔄 **Smart Fallback**: Multiple APIs for 99%+ uptime
- 📊 **Statistics**: Built-in usage tracking
- 🌐 **Production Ready**: Deploy on Render/Railway/Heroku

## 🎯 Quick Start

### Generate Your First Image

```bash
curl -X POST https://fast-image-api.onrender.com/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A beautiful sunset over mountains"}'
```

**Response in 1-2 seconds:**
```json
{
  "success": true,
  "image": "base64_encoded_image_data",
  "prompt": "A beautiful sunset over mountains",
  "model": "pollinations-sdxl",
  "response_time": 1.23
}
```

## 📦 Deploy on Render (Free)

1. Fork this repository
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn image_api:app`
   - **Instance Type**: Free
6. Click "Create Web Service"
7. Done! API live in 2-3 minutes

## 💻 Usage Examples

### Python

```python
import requests
import base64

API_URL = "https://fast-image-api.onrender.com/generate"

def generate_image(prompt):
    response = requests.post(API_URL, json={"prompt": prompt})
    data = response.json()
    
    if data['success']:
        img_data = base64.b64decode(data['image'])
        with open('output.png', 'wb') as f:
            f.write(img_data)
        print(f"✅ Generated in {data['response_time']}s")

generate_image("A futuristic city at night")
```

### JavaScript

```javascript
async function generateImage(prompt) {
  const response = await fetch('https://fast-image-api.onrender.com/generate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({prompt})
  });
  
  const data = await response.json();
  if (data.success) {
    const img = document.createElement('img');
    img.src = `data:image/png;base64,${data.image}`;
    document.body.appendChild(img);
  }
}

generateImage('A magical forest');
```

## 📊 API Endpoints

### `POST /generate`
Generate image from text

**Request:**
```json
{
  "prompt": "Your description",
  "width": 512,
  "height": 512
}
```

**Response:**
```json
{
  "success": true,
  "image": "base64_data",
  "prompt": "Your prompt",
  "model": "pollinations-sdxl",
  "response_time": 1.23
}
```

### `GET /health`
Health check

### `GET /stats`
Usage statistics

### `GET /`
API information

## 🎨 Integration with Chatbot

```python
# In your chatbot (e.g., gpt.py)

IMAGE_API = "https://fast-image-api.onrender.com/generate"

def generate_image(prompt):
    response = requests.post(IMAGE_API, json={"prompt": prompt}, timeout=10)
    return response.json()

if "generate image" in message.lower():
    result = generate_image(prompt)
    if result['success']:
        return jsonify({
            "type": "image",
            "image": result['image']
        })
```

## 📈 Performance

- **Response Time**: 1-2 seconds
- **Success Rate**: 99%+
- **Uptime**: 99.9%
- **Rate Limits**: None
- **Cost**: $0

## 📝 License

MIT License - Free for all use

## ⭐ Support

If useful, please star the repo!

---

**Built with ❤️ by Aman Kumar** | [GitHub](https://github.com/Aman262626/fast-image-api)