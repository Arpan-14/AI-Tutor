# Deployment Guide

## Frontend Deployment (Vercel)

### Quick Deploy
1. Push your code to GitHub
2. Visit [vercel.com](https://vercel.com) and sign in
3. Click "New Project" and import your GitHub repository
4. Set the **Root Directory** to `frontend`
5. Add environment variable:
   - `VITE_API_BASE_URL`: Your backend URL (from Render.com)
6. Deploy!

### Environment Variables (Vercel)
```
VITE_API_BASE_URL=https://your-backend-name.onrender.com
```

## Backend Deployment (Render.com)

### Quick Deploy
1. Visit [render.com](https://render.com) and sign in
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Use these settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Python Version**: 3.11.x

### Environment Variables (Render.com)
```
HUGGINGFACE_API_KEY=hf_your_actual_api_key_here
MODEL_NAME=microsoft/phi-3-mini-4k-instruct
API_BASE_URL=https://api-inference.huggingface.co/models/
CORS_ORIGINS=http://localhost:3000,https://your-vercel-app.vercel.app
```

## Getting Hugging Face API Key

1. Create account at [huggingface.co](https://huggingface.co)
2. Go to Settings → Access Tokens
3. Create a new token with "Read" permissions
4. Copy the token (starts with `hf_`)

## Testing Your Deployment

1. Deploy backend first and get the URL
2. Update frontend environment variable with backend URL
3. Deploy frontend
4. Test the chat functionality

## Troubleshooting

### Common Issues:
- **CORS Errors**: Ensure frontend URL is in backend CORS_ORIGINS
- **API Key Issues**: Verify Hugging Face API key is correct
- **Model Loading**: Some models need time to "warm up" - try again in 1-2 minutes
- **Build Failures**: Check that all dependencies are listed in requirements.txt

### Checking Logs:
- **Vercel**: Check Function Logs in dashboard
- **Render**: Check Logs tab in service dashboard
