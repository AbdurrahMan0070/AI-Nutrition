# 🍽️ NutriScan AI - Smart Nutrition Analysis

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![AI](https://img.shields.io/badge/AI-Gemini-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**AI-powered nutrition analyzer that instantly provides detailed nutritional information from food images**

[Live Demo](#) • [Features](#features) • [Installation](#installation) • [Deployment](#deployment)

</div>

---

## 📸 What is NutriScan AI?

NutriScan AI is a modern web application that uses Google's Gemini AI to analyze food images and provide comprehensive nutritional information. Simply upload a photo of your meal, and get instant insights about calories, macronutrients, health score, and ingredients!

### ✨ Key Features

- 🤖 **AI-Powered Analysis** - Uses Google Gemini Pro Vision for accurate food recognition
- 📊 **Comprehensive Data** - Get calories, protein, carbs, fat, and more
- 💯 **Health Score** - Visual 1-10 rating with color-coded progress bar
- 🥗 **Ingredient Detection** - Automatically identifies visible ingredients
- 🎨 **Premium UI/UX** - Beautiful purple gradient design with smooth animations
- 📱 **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- 🚀 **Drag & Drop** - Easy image upload with drag and drop support
- ⚡ **Real-time Analysis** - Get results in seconds

---

## 🎯 How It Works

1. **Upload** - Click or drag & drop a food image
2. **Analyze** - AI processes the image in seconds
3. **Results** - View detailed nutrition information:
   - Meal name
   - Calorie estimate
   - Macronutrient breakdown (Protein, Carbs, Fat)
   - Health score (1-10)
   - Detected ingredients
   - AI-generated comment

---

## 🖼️ Screenshots

### Upload Interface
Clean, modern interface with drag & drop support

### Analysis Results
Comprehensive nutrition data with visual health score

### Mobile Responsive
Works beautifully on all devices

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one free here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/AbdurrahMan0070/AI-Nutrition.git
cd AI-Nutrition
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your API key**

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY=your_api_key_here
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
```
http://127.0.0.1:5000
```

---

## 🎨 Features in Detail

### AI-Powered Analysis
- Uses Google's latest Gemini Pro Vision model
- Accurate food recognition
- Estimates nutritional values
- Identifies multiple ingredients

### Health Score System
- Visual 1-10 rating
- Color-coded progress bar:
  - 🟢 Green (7-10): Healthy meal
  - 🟠 Orange (4-6): Moderate
  - 🔴 Red (1-3): Less healthy
- Based on nutrient density and balance

### Premium User Interface
- Modern purple gradient theme
- High-quality Lucide icons
- Smooth animations and transitions
- Glassmorphism effects
- Professional typography (Inter + Poppins)
- Fully responsive design

### Ingredient Detection
- Lists all visible ingredients
- Displayed as clean, rounded tags
- Helps identify allergens
- Useful for meal tracking

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **AI Model:** Google Gemini Pro Vision
- **Frontend:** HTML5, CSS3, JavaScript
- **Icons:** Lucide Icons
- **Fonts:** Google Fonts (Inter & Poppins)
- **Deployment:** Gunicorn, Docker-ready

---

## 📦 Project Structure

```
AI-Nutrition/
├── app.py                 # Flask backend
├── index.html            # Frontend UI
├── requirements.txt      # Python dependencies
├── Procfile             # Deployment config
├── Dockerfile           # Docker config
├── runtime.txt          # Python version
├── render.yaml          # Render config
├── test_api.py          # API testing script
├── .gitignore           # Git ignore rules
├── DEPLOY_RENDER.md     # Render deployment guide
├── DEPLOY_RAILWAY.md    # Railway deployment guide
└── README.md            # This file
```

---

## 🌐 Deployment

Deploy your app to the cloud in minutes!

### Recommended: Render (Free)

1. Push your code to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service
4. Connect your GitHub repository
5. Add environment variable: `GEMINI_API_KEY`
6. Deploy!

**Detailed guides:**
- [Deploy to Render](DEPLOY_RENDER.md) - Complete guide
- [Deploy to Railway](DEPLOY_RAILWAY.md) - Alternative platform

### Other Options

- **Railway** - Fast, modern, $5 free credit/month
- **Fly.io** - Global edge deployment
- **PythonAnywhere** - Python-specific hosting
- **Google Cloud Run** - Serverless, auto-scaling
- **Heroku** - Classic platform ($7/month)

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | Yes |
| `PORT` | Port to run the app (default: 5000) | No |

### API Key Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. Set it as an environment variable

---

## 🧪 Testing

Test your API connection:
```bash
python test_api.py
```

This will verify:
- API key is valid
- Available models
- Connection to Gemini AI

---

## 📱 Usage Tips

### For Best Results

- **Good Lighting** - Use natural light when possible
- **Clear View** - Show the entire meal
- **Close Enough** - Fill the frame with food
- **Focus** - Avoid blurry images
- **Angle** - Slightly above works best

### Supported Formats

- JPEG/JPG
- PNG
- WEBP
- GIF (first frame)
- BMP

### File Size

- Recommended: Under 5MB
- Maximum: 10MB

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🐛 Troubleshooting

### Common Issues

**"GEMINI_API_KEY not set"**
- Make sure you set the environment variable in the same terminal where you run the app

**"Module not found"**
- Run: `pip install -r requirements.txt`

**Image uploads but doesn't analyze**
- Check terminal for error messages
- Verify API key is valid
- Try a different, clearer image

**Can't connect to server**
- Make sure Flask is running
- Check if port 5000 is available
- Try `http://localhost:5000` instead

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini AI** - For the powerful vision model
- **Lucide Icons** - For the beautiful icon set
- **Google Fonts** - For Inter and Poppins fonts
- **Flask** - For the lightweight web framework

---

## 📞 Contact

**Abdurrahman**
- GitHub: [@AbdurrahMan0070](https://github.com/AbdurrahMan0070)
- Project Link: [https://github.com/AbdurrahMan0070/AI-Nutrition](https://github.com/AbdurrahMan0070/AI-Nutrition)

---

## 🌟 Show Your Support

If you like this project, please give it a ⭐ on GitHub!

---

<div align="center">

**Made with ❤️ and AI**

[⬆ Back to Top](#-nutriscan-ai---smart-nutrition-analysis)

</div>
