# AI Tutor Bot

A fully web-based AI Tutor Bot built with React.js and FastAPI, featuring real-time chat interface with AI-powered educational assistance.

## 🚀 Features

- **Interactive Chat Interface**: Beautiful, responsive chat UI with typing animations
- **Quick Actions**: Predefined buttons for common learning activities
- **User Personalization**: Name and topic tracking for personalized responses
- **AI-Powered Responses**: Integration with Hugging Face Inference API
- **Real-time Communication**: Fast, responsive chat experience
- **Mobile Responsive**: Works seamlessly on all devices

## 🛠 Tech Stack

### Frontend
- **React.js** - Modern UI library
- **Vite** - Fast build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls

### Backend
- **FastAPI** - High-performance Python web framework
- **Hugging Face Inference API** - AI model integration
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### AI Models
- `microsoft/phi-3-mini-4k-instruct` (Primary)
- `openchat/openchat-3.5` (Alternative)

## 📦 Installation & Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Hugging Face account and API key

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Copy environment file and configure
cp .env.example .env
# Edit .env with your Hugging Face API key

# Run the server
uvicorn main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`

## 🔧 Environment Variables

### Backend (.env)
```env
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
MODEL_NAME=microsoft/phi-3-mini-4k-instruct
API_BASE_URL=https://api-inference.huggingface.co/models/
CORS_ORIGINS=http://localhost:3000,https://your-vercel-domain.vercel.app
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000
```

## 🚀 Deployment

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set environment variable: `VITE_API_BASE_URL` to your backend URL
3. Deploy automatically on push to main branch

### Backend (Render.com)
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set environment variables in Render dashboard
4. Use the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 📱 Usage

1. **Start Conversation**: Enter your name to begin
2. **Ask Questions**: Type any learning-related question
3. **Use Quick Actions**: Click preset buttons for common requests:
   - 📚 Learn Topic
   - 🧠 Test Knowledge  
   - 💡 Explain Concept
   - ✏️ Practice Problems
4. **Get AI Responses**: Receive personalized educational assistance

## 🎯 Features Overview

### Chat Interface
- Real-time messaging with typing indicators
- Message history with timestamps
- Responsive design for all screen sizes

### AI Integration
- Hugging Face Inference API integration
- Specialized educational prompts
- Error handling and fallback responses

### User Experience
- Smooth animations and transitions
- Accessibility-friendly design
- Fast loading and responsive interactions

## 🔗 API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /chat` - Main chat endpoint

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Hugging Face for providing free AI model inference
- Vercel for free frontend hosting
- Render.com for free backend hosting
- TailwindCSS for beautiful styling utilities
