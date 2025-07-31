# 🚀 Free LLM Setup Guide

## Get Your FREE Groq API Key (Recommended)

**Groq is completely free, fast, and doesn't require any GPU on your machine!**

### Step 1: Sign up for Groq
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with your email or GitHub account (free)
3. No credit card required!

### Step 2: Get Your API Key
1. Once logged in, go to [console.groq.com/keys](https://console.groq.com/keys)
2. Click "Create API Key"
3. Give it a name like "AI Tutor Bot"
4. Copy the API key (starts with `gsk_...`)

### Step 3: Add to Your Project
1. Open `backend/.env` file
2. Replace `your_groq_api_key_here` with your actual API key:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```
3. Save the file

### Step 4: Restart Backend
```bash
cd backend
python main.py
```

## ✨ Why Groq?

- **🆓 Completely Free**: No charges, no limits for reasonable use
- **⚡ Super Fast**: Responses in under 1 second
- **🎯 No GPU Needed**: Runs entirely on Groq's cloud infrastructure
- **🧠 High Quality**: Uses Llama 3.1 8B model for excellent responses
- **🔒 Secure**: Enterprise-grade security and privacy

## Alternative Options (if needed)

### Option 2: Keep Current Fallback System
If you prefer not to sign up for anything, the system will automatically use high-quality fallback responses that are educational and comprehensive.

### Option 3: Local Models (Advanced)
For completely offline operation:
- Install Ollama
- Download small models like Llama 3.2 3B
- Requires 8GB+ RAM but no GPU needed

## Current System Status

Your AI Tutor Bot is designed with multiple fallback layers:

1. **Primary**: Groq API (when key is provided)
2. **Backup**: Hugging Face API (current key working)
3. **Fallback**: High-quality educational responses (always available)

**The system works great even without any API keys!** But Groq will give you the most dynamic and conversational responses.

---

**🎓 Ready to learn? Your AI tutor is waiting!**
