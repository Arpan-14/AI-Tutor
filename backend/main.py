# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import httpx
# import os
# from dotenv import load_dotenv
# import logging
# from typing import Optional, List, Dict
# import json
# from datetime import datetime
# from pathlib import Path

# # Load environment variables
# load_dotenv()

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Print loaded environment variables for debugging
# HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
# logger.info(f"Hugging Face API Key loaded: {'Yes' if HUGGINGFACE_API_KEY else 'No'}")
# logger.info(f"Hugging Face API Key starts with: {HUGGINGFACE_API_KEY[:10]}..." if HUGGINGFACE_API_KEY else "No HF key")

# app = FastAPI(
#     title="AI Tutor Bot API",
#     description="Backend API for AI Tutor Bot with Hugging Face integration",
#     version="1.0.0"
# )

# # CORS configuration
# origins = os.getenv("CORS_ORIGINS", "http://localhost:3001").split(",")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Configuration
# HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "").strip()
# MODEL_NAME = os.getenv("MODEL_NAME", "microsoft/phi-3-mini-4k-instruct")
# API_BASE_URL = os.getenv("VITE_API_BASE_URL", "https://api-inference.huggingface.co/models/")

# # User data storage
# USER_DATA_DIR = Path("user_data")
# USER_DATA_DIR.mkdir(exist_ok=True)

# # Simple in-memory storage for conversation history (fallback)
# conversation_history: Dict[str, List[Dict]] = {}

# def get_user_file_path(user_name: str) -> Path:
#     """Get the file path for a user's conversation history"""
#     safe_name = "".join(c for c in user_name if c.isalnum() or c in (' ', '-', '_')).strip()
#     safe_name = safe_name.replace(' ', '_')
#     return USER_DATA_DIR / f"{safe_name}_conversations.json"

# def load_user_history(user_name: str) -> List[Dict]:
#     """Load conversation history for a specific user"""
#     file_path = get_user_file_path(user_name)
#     try:
#         if file_path.exists():
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 data = json.load(f)
#                 return data.get('conversations', [])
#     except Exception as e:
#         logger.error(f"Error loading user history for {user_name}: {str(e)}")
#     return []

# def save_user_history(user_name: str, conversations: List[Dict]) -> bool:
#     """Save conversation history for a specific user"""
#     file_path = get_user_file_path(user_name)
#     try:
#         user_data = {
#             'user_name': user_name,
#             'last_updated': datetime.now().isoformat(),
#             'total_messages': len(conversations),
#             'conversations': conversations[-50:]  # Keep only last 50 messages
#         }
#         with open(file_path, 'w', encoding='utf-8') as f:
#             json.dump(user_data, f, indent=2, ensure_ascii=False)
#         return True
#     except Exception as e:
#         logger.error(f"Error saving user history for {user_name}: {str(e)}")
#         return False

# def get_user_stats(user_name: str) -> Dict:
#     """Get user statistics"""
#     file_path = get_user_file_path(user_name)
#     stats = {
#         'total_sessions': 0,
#         'total_messages': 0,
#         'first_visit': None,
#         'last_visit': None,
#         'favorite_topics': []
#     }
    
#     try:
#         if file_path.exists():
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 data = json.load(f)
#                 conversations = data.get('conversations', [])
                
#                 if conversations:
#                     stats['total_messages'] = len([msg for msg in conversations if msg.get('sender') == 'user'])
#                     stats['first_visit'] = conversations[0].get('timestamp')
#                     stats['last_visit'] = conversations[-1].get('timestamp')
                    
#                     # Analyze topics mentioned
#                     topics = {}
#                     for msg in conversations:
#                         if msg.get('sender') == 'user':
#                             text = msg.get('message', '').lower()
#                             for topic in ['math', 'science', 'history', 'physics', 'chemistry', 'biology']:
#                                 if topic in text:
#                                     topics[topic] = topics.get(topic, 0) + 1
                    
#                     stats['favorite_topics'] = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:3]
#     except Exception as e:
#         logger.error(f"Error getting user stats for {user_name}: {str(e)}")
    
#     return stats

# # Hugging Face API query function
# async def query_huggingface(prompt: str) -> str:
#     """Query Hugging Face Inference API"""
#     if not HUGGINGFACE_API_KEY:
#         logger.warning("No Hugging Face API key found")
#         return None
    
#     headers = {
#         "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
#         "Content-Type": "application/json"
#     }
    
#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "max_new_tokens": 200,
#             "temperature": 0.7,
#             "return_full_text": False,
#             "do_sample": True
#         }
#     }
    
#     try:
#         async with httpx.AsyncClient(timeout=30.0) as client:
#             response = await client.post(
#                 f"{API_BASE_URL}{MODEL_NAME}",
#                 headers=headers,
#                 json=payload
#             )
            
#             if response.status_code == 200:
#                 result = response.json()
#                 if isinstance(result, list) and len(result) > 0:
#                     generated_text = result[0].get("generated_text", "").strip()
#                     if generated_text:
#                         return generated_text
#                 elif isinstance(result, dict):
#                     generated_text = result.get("generated_text", "").strip()
#                     if generated_text:
#                         return generated_text
                        
#             logger.warning(f"Hugging Face API response: {response.status_code} - {response.text}")
#             return None
            
#     except Exception as e:
#         logger.error(f"Error querying Hugging Face API: {str(e)}")
#         return None

# def create_advanced_tutor_prompt(message: str, user_name: Optional[str] = None, topic: Optional[str] = None, conversation_context: List = None) -> str:
#     """Create an advanced, context-aware prompt for the AI tutor"""
    
#     # Analyze conversation context for better responses
#     context_summary = ""
#     if conversation_context and len(conversation_context) > 1:
#         recent_topics = []
#         for msg in conversation_context[-5:]:  # Last 5 messages
#             if msg.get('sender') == 'user':
#                 recent_topics.append(msg.get('message', ''))
#         if recent_topics:
#             context_summary = f"Recent conversation topics: {'; '.join(recent_topics)}. "
    
#     base_prompt = f"""You are an exceptional AI tutor with expertise across all academic subjects. Your mission is to provide world-class educational support with the following characteristics:

# CORE PRINCIPLES:
# 1. Excellence in explanation - Make complex concepts crystal clear
# 2. Adaptive teaching - Match your approach to the student's learning style
# 3. Engagement through curiosity - Spark interest and deeper thinking
# 4. Practical application - Connect learning to real-world examples
# 5. Encouraging growth mindset - Build confidence and resilience

# RESPONSE QUALITY STANDARDS:
# - Provide comprehensive yet digestible explanations
# - Use vivid analogies and memorable examples
# - Include step-by-step breakdowns for complex topics
# - Offer multiple perspectives when helpful
# - Ask thought-provoking follow-up questions
# - Maintain enthusiasm and encouragement
# - Avoid generic or superficial responses

# TEACHING STRATEGIES:
# - Start with what the student knows and build systematically
# - Use scaffolding techniques to support learning
# - Provide immediate feedback and correction when needed
# - Encourage active learning and critical thinking
# - Connect new knowledge to prior learning
# - Use visual descriptions when explaining abstract concepts

# PERSONALIZATION:
# - Adapt language complexity to the student's level
# - Remember previous interactions and build upon them
# - Acknowledge progress and effort
# - Provide personalized study suggestions
# - Address individual learning challenges

# {context_summary}"""
    
#     if user_name:
#         base_prompt += f"Student name: {user_name}. Address them personally and warmly. "
    
#     if topic:
#         base_prompt += f"Current focus topic: {topic}. Maintain relevance to this subject. "
    
#     base_prompt += f"""

# STUDENT'S MESSAGE: "{message}"

# Provide an exceptional educational response that demonstrates deep knowledge, clear communication, and genuine care for the student's learning journey. Make this response engaging, informative, and inspiring:"""
    
#     return base_prompt

# class ChatRequest(BaseModel):
#     message: str
#     user_name: Optional[str] = None
#     topic: Optional[str] = None

# class ChatResponse(BaseModel):
#     response: str
#     status: str = "success"

# def get_premium_educational_response(message: str, user_name: Optional[str] = None, conversation_context: List = None) -> str:
#     """Generate high-quality, comprehensive educational responses"""
#     message_lower = message.lower()
#     name_part = f"{user_name}" if user_name else "there"
    
#     # Check conversation context for personalization
#     learning_progress = ""
#     if conversation_context and len(conversation_context) > 2:
#         msg_count = len([msg for msg in conversation_context if msg.get('sender') == 'user'])
#         if msg_count > 3:
#             learning_progress = f"I can see you're really engaged in our learning session - we've covered {msg_count} topics together! "
    
#     # Advanced topic detection and responses
#     if "gravity" in message_lower or "gravitational" in message_lower:
#         return f"""Hello {name_part}! 🌍 Gravity is one of the most fascinating forces in our universe!

# {learning_progress}Let me give you a comprehensive understanding of gravity:

# **The Fundamentals:**
# • Gravity is a fundamental force that attracts objects with mass toward each other
# • On Earth, it accelerates objects at 9.8 m/s² (that's why things fall at increasing speed!)
# • It's actually the weakest of the four fundamental forces, yet it shapes the entire cosmos

# **How It Works:**
# Think of space-time as a stretchy rubber sheet. When you place a heavy ball (like Earth) on it, it creates a dip. Smaller objects (like you!) naturally roll toward that dip - that's gravity in action!

# **Mind-Blowing Facts:**
# 🚀 Gravity travels at light speed - if the Sun vanished, we'd keep orbiting for 8 minutes!
# 🌙 The Moon's gravity creates ocean tides and is slowly moving away from Earth
# ⚖️ In a vacuum, a feather and hammer fall at exactly the same rate
# 🕳️ Black holes have gravity so strong that even light can't escape

# **Real-World Applications:**
# - GPS satellites must account for gravity's effect on time (yes, time runs differently!)
# - Understanding gravity helps us launch rockets and predict planetary movements
# - It's crucial for everything from building bridges to predicting asteroid paths

# What aspect of gravity intrigues you most? The physics behind it, its effects on space exploration, or how Einstein revolutionized our understanding of it?"""

#     elif any(word in message_lower for word in ["photosynthesis", "plants", "chlorophyll"]):
#         return f"""Excellent question about photosynthesis, {name_part}! 🌱 This is literally the process that powers most life on Earth!

# {learning_progress}**Photosynthesis: Nature's Solar Power System**

# **The Simple Version:**
# Plants are like living solar panels that convert sunlight into food! They take in carbon dioxide from air, water from soil, and use sunlight energy to create glucose (plant food) and oxygen.

# **The Detailed Process:**
# 1. **Light Absorption**: Chlorophyll (green pigment) captures photons from sunlight
# 2. **Water Splitting**: Plant breaks down water molecules (H₂O) using light energy
# 3. **Carbon Fixation**: CO₂ from air combines with other compounds
# 4. **Glucose Production**: All ingredients combine to create C₆H₁₂O₆ (sugar)
# 5. **Oxygen Release**: O₂ is released as a "waste" product (lucky for us!)

# **The Famous Equation:**
# 6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂ + ATP

# **Why It's Amazing:**
# 🌍 Produces virtually ALL oxygen we breathe
# 🌿 Forms the foundation of most food chains
# ⚡ Converts 100+ billion tons of CO₂ annually
# 🔋 Inspired solar panel technology
# 🌳 A single tree can produce oxygen for 2 people per day!

# **Two Amazing Stages:**
# - **Light Reactions**: Happen in chloroplasts, convert light to chemical energy
# - **Calvin Cycle**: Uses that energy to build glucose from CO₂

# Would you like to explore how different plants have adapted their photosynthesis for extreme environments, or are you curious about how this process evolved over billions of years?"""

#     elif any(word in message_lower for word in ["math", "mathematics", "algebra", "calculus", "geometry"]):
#         return f"""I'm thrilled you're diving into mathematics, {name_part}! 🧮 Math is the universal language that unlocks understanding of our entire world.

# {learning_progress}**Why Mathematics is Extraordinary:**
# Math isn't just numbers - it's pattern recognition, logical thinking, and problem-solving that applies to EVERYTHING around us!

# **Core Mathematical Thinking Skills:**
# 📊 **Pattern Recognition**: Seeing relationships and trends
# 🔍 **Logical Reasoning**: Building step-by-step arguments
# 🎯 **Problem Decomposition**: Breaking complex problems into manageable parts
# ⚖️ **Abstract Thinking**: Working with concepts beyond physical objects

# **Major Branches & Their Magic:**
# • **Algebra**: The art of finding unknowns (like detective work with numbers!)
# • **Geometry**: Understanding shapes, space, and spatial relationships
# • **Calculus**: Analyzing change and motion (powers rocket launches!)
# • **Statistics**: Making sense of data and probability
# • **Number Theory**: The deep patterns hidden in numbers themselves

# **Proven Study Strategies:**
# 1. **Work problems step-by-step** - show every detail of your thinking
# 2. **Explain your reasoning** - if you can teach it, you truly understand it
# 3. **Connect to real examples** - math is everywhere once you start looking!
# 4. **Practice consistently** - mathematical thinking is like building muscle memory
# 5. **Don't fear mistakes** - they're stepping stones to deeper understanding

# **Real-World Applications:**
# 💻 Computer graphics and gaming engines
# 🏗️ Architecture and engineering design
# 📈 Financial modeling and investment strategies
# 🧬 Medical imaging and drug development
# 🌌 Space exploration and satellite navigation

# What specific area of mathematics interests you? I can provide targeted strategies and fascinating applications for any mathematical concept you're exploring!"""

#     elif any(word in message_lower for word in ["science", "physics", "chemistry", "biology"]):
#         return f"""Science is absolutely incredible, {name_part}! 🔬 You're asking about humanity's greatest adventure - understanding how our universe works!

# {learning_progress}**The Beauty of Scientific Thinking:**
# Science teaches us to observe, question, hypothesize, test, and refine our understanding. It's like being a detective solving the mysteries of existence!

# **The Big Picture - Major Scientific Fields:**

# 🧬 **Biology** - The Science of Life:
# - How living systems work, from cells to ecosystems
# - Evolution, genetics, and the incredible diversity of life
# - Applications: Medicine, agriculture, biotechnology

# ⚛️ **Chemistry** - The Science of Matter:
# - How atoms combine to create everything we see
# - Chemical reactions that power life and technology
# - Applications: Drug development, materials science, energy

# 🌌 **Physics** - The Science of Reality:
# - Forces, energy, motion, and the fundamental laws of nature
# - From quantum mechanics to cosmic phenomena
# - Applications: Technology, space exploration, renewable energy

# 🌍 **Earth Science** - Our Planet's Systems:
# - Weather, climate, geology, and environmental processes
# - Understanding natural disasters and climate change
# - Applications: Meteorology, environmental protection, resource management

# **What Makes Science Extraordinary:**
# • **Predictive Power**: Science helps us predict eclipses, weather, and planetary movements
# • **Technological Innovation**: Every device you use exists because of scientific understanding
# • **Medical Breakthroughs**: From antibiotics to vaccines to genetic therapy
# • **Universal Principles**: The same laws govern atoms and galaxies!

# **Scientific Method in Action:**
# 1. **Observe** phenomena in the natural world
# 2. **Ask questions** about what you observe
# 3. **Form hypotheses** (educated guesses)
# 4. **Design experiments** to test your ideas
# 5. **Analyze results** and draw conclusions
# 6. **Share findings** with the scientific community

# Which branch of science captures your imagination most? I'd love to explore specific concepts, famous discoveries, or how scientific principles apply to your daily life!"""

#     elif any(word in message_lower for word in ["history", "historical", "ancient", "civilization"]):
#         return f"""History is fascinating, {name_part}! 📚 You're exploring the greatest story ever told - the human journey through time!

# {learning_progress}**Why History Matters:**
# History isn't just memorizing dates - it's understanding how we got here, learning from past experiences, and recognizing patterns that still shape our world today.

# **Epic Periods to Explore:**

# 🏛️ **Ancient Civilizations** (3500 BCE - 500 CE):
# - **Mesopotamia**: First cities, writing, and laws (Code of Hammurabi)
# - **Egypt**: Pyramids, pharaohs, and incredible engineering feats
# - **Greece**: Democracy, philosophy, and scientific thinking
# - **Rome**: Vast empire, legal systems, and architectural marvels

# 🏰 **Medieval Period** (500 - 1500 CE):
# - Rise of great religions and their global influence
# - Knights, castles, and the feudal system
# - Islamic Golden Age and preservation of knowledge
# - The Renaissance: rebirth of art, science, and learning

# 🌍 **Age of Exploration** (1400 - 1700):
# - European voyages connecting distant continents
# - Cultural exchanges that transformed societies
# - The Scientific Revolution changing how we see reality
# - Formation of global trade networks

# ⚙️ **Industrial Revolution** (1750 - 1900):
# - Steam power transforming transportation and manufacturing
# - Urbanization and massive social changes
# - Technological innovations changing daily life
# - Rise of new economic and political systems

# 🌐 **Modern Era** (1900 - Present):
# - Two World Wars reshaping global politics
# - Space age and technological revolution
# - Civil rights movements and social progress
# - Digital age transforming communication and learning

# **Key Historical Thinking Skills:**
# • **Chronological Thinking**: Understanding cause and effect over time
# • **Source Analysis**: Evaluating evidence and different perspectives
# • **Historical Empathy**: Understanding people's motivations in their context
# • **Pattern Recognition**: Seeing how past events connect to present situations

# What historical period or theme interests you most? I can dive deep into specific events, influential figures, or how historical developments connect to today's world!"""

#     elif any(word in message_lower for word in ["learn", "study", "understand", "help me"]):
#         return f"""I'm absolutely delighted to help you learn, {name_part}! 🎓 Your curiosity and desire to understand is the most important ingredient for success!

# {learning_progress}**The Science of Effective Learning:**

# 🧠 **How Your Brain Learns Best:**
# - **Active Retrieval**: Testing yourself is more effective than re-reading
# - **Spaced Repetition**: Review material at increasing intervals
# - **Elaborative Practice**: Connect new info to what you already know
# - **Interleaving**: Mix different types of problems/concepts in study sessions
# - **Dual Coding**: Combine visual and verbal information

# 💡 **Proven Learning Strategies:**

# **Before You Study:**
# • Set specific, achievable goals for each session
# • Choose a distraction-free environment
# • Gather all materials you'll need
# • Prime your brain with light physical activity

# **During Study Sessions:**
# • **Pomodoro Technique**: 25 minutes focused work, 5-minute breaks
# • **Active Note-Taking**: Summarize in your own words
# • **Question Everything**: Ask "why," "how," and "what if"
# • **Teach Back**: Explain concepts to someone else (or even your pet!)
# • **Visual Mapping**: Create diagrams, flowcharts, or mind maps

# **After Learning:**
# • **Self-Testing**: Quiz yourself without looking at notes
# • **Reflection**: What did you learn? What's still unclear?
# • **Application**: Find real-world examples of the concepts
# • **Connection**: Link new knowledge to previous learning

# **Memory Enhancement Techniques:**
# 🎭 **Storytelling**: Turn facts into memorable narratives
# 🏠 **Memory Palace**: Associate information with familiar locations
# 🎵 **Mnemonics**: Create acronyms, rhymes, or songs
# 🖼️ **Visualization**: Create vivid mental images
# 🔗 **Chunking**: Group related information together

# **Growth Mindset Principles:**
# • Embrace challenges as opportunities to grow
# • View effort as the path to mastery
# • Learn from feedback and criticism
# • Find inspiration in others' success
# • Understand that abilities can be developed

# What specific subject or learning challenge would you like to tackle? I can provide customized strategies, practice opportunities, and support for any area of study!"""

#     elif any(word in message_lower for word in ["quiz", "test", "practice", "exam"]):
#         return f"""Excellent approach, {name_part}! 🎯 Testing yourself is one of the most powerful learning strategies science has discovered!

# {learning_progress}**The Power of Self-Testing:**
# Research shows that retrieval practice (testing yourself) is far more effective than passive review. When you actively recall information, you strengthen neural pathways and identify knowledge gaps.

# **Smart Testing Strategies:**

# 📚 **Before the Test:**
# • **Spaced Practice**: Start reviewing weeks before, not days
# • **Active Recall**: Close your notes and try to remember key concepts
# • **Practice Testing**: Use flashcards, practice exams, or self-made quizzes
# • **Teach Others**: Explain concepts to friends, family, or study groups
# • **Mixed Practice**: Combine different types of problems/concepts

# 🧠 **During the Test:**
# • **Read Instructions Carefully**: Understand exactly what's being asked
# • **Time Management**: Allocate time based on point values
# • **Start with Confidence**: Begin with questions you know well
# • **Show Your Work**: Especially in math and science
# • **Review if Time Allows**: Check for careless errors

# **Subject-Specific Quiz Ideas:**

# 🔬 **Science Testing:**
# - "Explain the process of [concept] without looking at notes"
# - "What would happen if [variable] changed in this system?"
# - "Draw and label a diagram of [scientific process]"
# - "Compare and contrast [two related concepts]"

# 🧮 **Mathematics Practice:**
# - Work through problems step-by-step with explanations
# - Create your own word problems
# - Solve problems using different methods
# - Explain why each step is necessary

# 📚 **History/Literature Review:**
# - Timeline creation from memory
# - "What were the causes and effects of [event]?"
# - Character analysis and motivation explanations
# - Connect historical events to modern situations

# **Overcoming Test Anxiety:**
# • **Preparation**: Thorough preparation builds confidence
# • **Breathing**: Deep, slow breaths calm your nervous system
# • **Positive Self-Talk**: Replace "I can't" with "I'm learning"
# • **Perspective**: This test is one step in your learning journey
# • **Physical Care**: Good sleep, nutrition, and exercise support performance

# What subject would you like to practice with? I can create customized quiz questions, provide practice problems, or help you develop a comprehensive review strategy!"""

#     # Default comprehensive response
#     else:
#         return f"""Thank you for that thoughtful question, {name_part}! 🌟 I'm here to provide you with the highest quality educational support.

# {learning_progress}**I'm Your Comprehensive Learning Partner:**

# I can help you excel in virtually any academic area:

# 📚 **Core Subjects:**
# • **Mathematics**: From basic arithmetic to advanced calculus
# • **Sciences**: Biology, chemistry, physics, earth science
# • **Literature**: Reading comprehension, writing skills, analysis
# • **History**: World events, historical thinking, cause and effect
# • **Languages**: Grammar, vocabulary, communication skills

# 🎯 **Learning Support:**
# • **Study Strategies**: Evidence-based techniques for retention
# • **Test Preparation**: Practice questions and exam strategies
# • **Project Guidance**: Research methods and presentation skills
# • **Critical Thinking**: Analysis, evaluation, and logical reasoning
# • **Time Management**: Organizing study schedules and priorities

# 💡 **How I Can Help:**
# • **Detailed Explanations**: Break down complex concepts step-by-step
# • **Real-World Connections**: Show how knowledge applies to life
# • **Practice Opportunities**: Custom problems and scenarios
# • **Immediate Feedback**: Correct mistakes and reinforce learning
# • **Motivation**: Celebrate progress and overcome challenges

# **My Teaching Philosophy:**
# I believe every student has unique strengths and learning styles. My goal is to:
# - Meet you where you are and build from there
# - Make learning engaging and relevant to your interests
# - Provide multiple explanations until concepts click
# - Encourage questions and curiosity
# - Build confidence through incremental success

# What specific topic, subject, or learning goal would you like to explore today? I'm excited to help you discover new knowledge and master challenging concepts!"""

# @app.get("/")
# async def root():
#     """Health check endpoint"""
#     return {"message": "AI Tutor Bot API is running!", "status": "healthy"}

# @app.get("/health")
# async def health_check():
#     """Detailed health check"""
#     services = {
#         "huggingface_available": bool(HUGGINGFACE_API_KEY and HUGGINGFACE_API_KEY != "your_huggingface_api_key_here"),
#         "fallback_available": True
#     }
#     primary_service = "huggingface" if services["huggingface_available"] else "fallback"
#     return {
#         "status": "healthy",
#         "primary_llm_service": primary_service,
#         "available_services": services,
#         "model_info": {
#             "huggingface_model": MODEL_NAME if services["huggingface_available"] else None
#         }
#     }

# @app.post("/chat", response_model=ChatResponse)
# async def chat(request: ChatRequest):
#     """Main chat endpoint with persistent conversation history"""
#     try:
#         # Create user session key
#         session_key = request.user_name or "anonymous"
        
#         # Load user's conversation history from file
#         user_conversations = load_user_history(session_key)
        
#         # Also maintain in-memory for this session
#         if session_key not in conversation_history:
#             conversation_history[session_key] = user_conversations.copy()
        
#         # Add user message to history
#         user_entry = {
#             "timestamp": datetime.now().isoformat(),
#             "message": request.message,
#             "sender": "user",
#             "topic": request.topic
#         }
#         conversation_history[session_key].append(user_entry)
        
#         # Generate response using conversation context
#         # Priority order: 1. Hugging Face (primary), 2. Fallback
#         response_text = None
        
#         if HUGGINGFACE_API_KEY and HUGGINGFACE_API_KEY != "your_huggingface_api_key_here":
#             prompt = create_advanced_tutor_prompt(
#                 request.message, 
#                 request.user_name, 
#                 request.topic, 
#                 conversation_history[session_key]
#             )
#             response_text = await query_huggingface(prompt)
        
#         if not response_text:
#             response_text = get_premium_educational_response(
#                 request.message, 
#                 request.user_name, 
#                 conversation_history[session_key]
#             )
        
#         # Add bot response to history
#         bot_entry = {
#             "timestamp": datetime.now().isoformat(),
#             "message": response_text,
#             "sender": "bot",
#             "topic": request.topic
#         }
#         conversation_history[session_key].append(bot_entry)
        
#         # Save updated history to file (persistent storage)
#         if session_key != "anonymous":
#             save_user_history(session_key, conversation_history[session_key])
        
#         # Keep only last 20 messages in memory to prevent memory issues
#         if len(conversation_history[session_key]) > 20:
#             conversation_history[session_key] = conversation_history[session_key][-20:]
        
#         return ChatResponse(response=response_text)
        
#     except Exception as e:
#         logger.error(f"Error in chat endpoint: {str(e)}")
#         # Final fallback
#         return ChatResponse(response="I'm experiencing some technical difficulties, but I'm still here to help you learn! Could you try asking your question again? 🤔")

# @app.get("/history/{user_name}")
# async def get_conversation_history(user_name: str):
#     """Get conversation history for a user"""
#     try:
#         # Load from file (persistent storage)
#         conversations = load_user_history(user_name)
        
#         # Also check in-memory storage for current session
#         if user_name in conversation_history:
#             # Merge with current session data
#             session_conversations = conversation_history[user_name]
#             # Add any new messages from current session
#             for msg in session_conversations:
#                 if msg not in conversations:
#                     conversations.append(msg)
        
#         return {
#             "history": conversations,
#             "total_messages": len(conversations),
#             "user_name": user_name
#         }
#     except Exception as e:
#         logger.error(f"Error getting history for {user_name}: {str(e)}")
#         return {"history": [], "total_messages": 0, "user_name": user_name}

# @app.get("/users/{user_name}/stats")
# async def get_user_statistics(user_name: str):
#     """Get detailed user statistics"""
#     try:
#         stats = get_user_stats(user_name)
#         return {
#             "user_name": user_name,
#             "statistics": stats,
#             "status": "success"
#         }
#     except Exception as e:
#         logger.error(f"Error getting stats for {user_name}: {str(e)}")
#         return {
#             "user_name": user_name,
#             "statistics": {},
#             "status": "error",
#             "message": str(e)
#         }

# @app.delete("/users/{user_name}/history")
# async def clear_user_history(user_name: str):
#     """Clear conversation history for a user"""
#     try:
#         # Clear persistent storage
#         file_path = get_user_file_path(user_name)
#         if file_path.exists():
#             file_path.unlink()
        
#         # Clear in-memory storage
#         if user_name in conversation_history:
#             del conversation_history[user_name]
        
#         return {
#             "message": f"History cleared for user {user_name}",
#             "status": "success"
#         }
#     except Exception as e:
#         logger.error(f"Error clearing history for {user_name}: {str(e)}")
#         return {
#             "message": f"Error clearing history: {str(e)}",
#             "status": "error"
#         }

# @app.get("/users")
# async def list_users():
#     """List all users with stored conversations"""
#     try:
#         users = []
#         for file_path in USER_DATA_DIR.glob("*_conversations.json"):
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     data = json.load(f)
#                     user_info = {
#                         "user_name": data.get('user_name', 'Unknown'),
#                         "last_updated": data.get('last_updated'),
#                         "total_messages": data.get('total_messages', 0)
#                     }
#                     users.append(user_info)
#             except Exception as e:
#                 logger.warning(f"Error reading user file {file_path}: {str(e)}")
#                 continue
        
#         return {
#             "users": sorted(users, key=lambda x: x.get('last_updated', ''), reverse=True),
#             "total_users": len(users)
#         }
#     except Exception as e:
#         logger.error(f"Error listing users: {str(e)}")
#         return {"users": [], "total_users": 0}
    
# from fastapi import Request
# from fastapi import FastAPI, HTTPException, Request
# import httpx
# import os
# from dotenv import load_dotenv

# @app.post("/ask")
# async def ask_question(request: Request):
#     data = await request.json()
#     question = data.get("message")
#     return {"answer": f"You asked: {question}"}


# @app.get("/")
# def read_root():
#     return {"message": "AI Tutor Bot Backend is running!"}

# @app.post("/ask")
# async def ask_question(request: Request):
#     data = await request.json()
#     question = data.get("message")

#     if not HUGGINGFACE_API_KEY:
#         return {"answer": "⚠️ Hugging Face API key not configured."}

#     headers = {
#         "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "inputs": question
#     }

#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.post(
#                 "https://api-inference.huggingface.co/models/google/flan-t5-large",
#                 headers=headers,
#                 json=payload,
#             )
#             response_data = response.json()

#         if isinstance(response_data, list):
#             answer = response_data[0].get("generated_text", "⚠️ No answer generated.")
#         elif "error" in response_data:
#             answer = f"❌ Hugging Face Error: {response_data['error']}"
#         else:
#             answer = str(response_data)

#         return {"answer": answer}

#     except Exception as e:
#         return {"answer": f"❌ Internal error: {str(e)}"}

# if __name__ == "__main__":
#     import uvicorn
#     port = int(os.getenv("PORT", 8002))
#     uvicorn.run(app, host="0.0.0.0", port=port)

# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import httpx
# import os
# from dotenv import load_dotenv
# import logging
# from typing import Optional, List, Dict
# import json
# from datetime import datetime
# from pathlib import Path

# # Load environment variables
# load_dotenv()

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# # Print loaded environment variables for debugging
# HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# USE_GEMINI = bool(GEMINI_API_KEY)
# if USE_GEMINI:
#     logger.info("Google Gemini API Key loaded: Yes")
# else:
#     logger.info(f"Hugging Face API Key loaded: {'Yes' if HUGGINGFACE_API_KEY else 'No'}")
#     logger.info(f"Hugging Face API Key starts with: {HUGGINGFACE_API_KEY[:10]}..." if HUGGINGFACE_API_KEY else "No HF key")

# app = FastAPI(
#     title="AI Tutor Bot API",
#     description="Backend API for AI Tutor Bot with Hugging Face integration",
#     version="1.0.0"
# )

# # CORS configuration
# origins = os.getenv("CORS_ORIGINS", "http://localhost:3001").split(",")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # Configuration
# HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "").strip()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
# MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct")
# API_BASE_URL = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/models/")
# GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent")

# # User data storage
# USER_DATA_DIR = Path("user_data")
# USER_DATA_DIR.mkdir(exist_ok=True)

# # Simple in-memory storage for conversation history (fallback)
# conversation_history: Dict[str, List[Dict]] = {}

# def get_user_file_path(user_name: str) -> Path:
#     safe_name = "".join(c for c in user_name if c.isalnum() or c in (' ', '-', '_')).strip()
#     safe_name = safe_name.replace(' ', '_')
#     return USER_DATA_DIR / f"{safe_name}_conversations.json"

# def load_user_history(user_name: str) -> List[Dict]:
#     file_path = get_user_file_path(user_name)
#     try:
#         if file_path.exists():
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 data = json.load(f)
#                 return data.get('conversations', [])
#     except Exception as e:
#         logger.error(f"Error loading user history for {user_name}: {str(e)}")
#     return []

# def save_user_history(user_name: str, conversations: List[Dict]) -> bool:
#     file_path = get_user_file_path(user_name)
#     try:
#         user_data = {
#             'user_name': user_name,
#             'last_updated': datetime.now().isoformat(),
#             'total_messages': len(conversations),
#             'conversations': conversations[-50:]  # Keep only last 50 messages
#         }
#         with open(file_path, 'w', encoding='utf-8') as f:
#             json.dump(user_data, f, indent=2, ensure_ascii=False)
#         return True
#     except Exception as e:
#         logger.error(f"Error saving user history for {user_name}: {str(e)}")
#         return False

# def get_user_stats(user_name: str) -> Dict:
#     file_path = get_user_file_path(user_name)
#     stats = {
#         'total_sessions': 0,
#         'total_messages': 0,
#         'first_visit': None,
#         'last_visit': None,
#         'favorite_topics': []
#     }
#     try:
#         if file_path.exists():
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 data = json.load(f)
#                 conversations = data.get('conversations', [])

#                 if conversations:
#                     stats['total_messages'] = len([msg for msg in conversations if msg.get('sender') == 'user'])
#                     stats['first_visit'] = conversations[0].get('timestamp')
#                     stats['last_visit'] = conversations[-1].get('timestamp')
#                     # Analyze topics mentioned
#                     topics = {}
#                     for msg in conversations:
#                         if msg.get('sender') == 'user':
#                             text = msg.get('message', '').lower()
#                             for topic in ['math', 'science', 'history', 'physics', 'chemistry', 'biology']:
#                                 if topic in text:
#                                     topics[topic] = topics.get(topic, 0) + 1
#                     stats['favorite_topics'] = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:3]
#     except Exception as e:
#         logger.error(f"Error getting user stats for {user_name}: {str(e)}")
#     return stats


# # Unified LLM query function: Gemini (if key present) or Hugging Face
# async def query_llm(prompt: str) -> Optional[str]:
#     if GEMINI_API_KEY:
#         # Google Gemini API (v1): requires 'role' and 'parts' fields
#         headers = {
#             "Content-Type": "application/json"
#         }
#         params = {"key": GEMINI_API_KEY}
#         payload = {
#             "contents": [
#                 {
#                     "role": "user",
#                     "parts": [
#                         {"text": str(prompt)}
#                     ]
#                 }
#             ]
#         }
#         try:
#             async with httpx.AsyncClient(timeout=60.0) as client:
#                 response = await client.post(GEMINI_API_URL, headers=headers, params=params, json=payload)
#                 if response.status_code == 200:
#                     result = response.json()
#                     candidates = result.get("candidates", [])
#                     if candidates:
#                         parts = candidates[0].get("content", {}).get("parts", [])
#                         if parts and "text" in parts[0]:
#                             return parts[0]["text"].strip()
#                     logger.warning("Gemini API: No valid text in response.")
#                     return "Sorry, I couldn't generate a response. Please try again."
#                 else:
#                     logger.warning(f"Gemini API response: {response.status_code} - {response.text}")
#                     return f"Gemini API error: {response.status_code} - {response.text}"
#         except Exception as e:
#             logger.error(f"Error querying Gemini API: {str(e)}")
#             return f"Error querying Gemini API: {str(e)}"
#     elif HUGGINGFACE_API_KEY:
#         # Hugging Face API
#         headers = {
#             "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
#             "Content-Type": "application/json"
#         }
#         payload = {
#             "inputs": prompt,
#             "parameters": {
#                 "max_new_tokens": 200,
#                 "temperature": 0.7,
#                 "return_full_text": False,
#                 "do_sample": True
#             }
#         }
#         url = f"{API_BASE_URL}{MODEL_NAME}"
#         try:
#             async with httpx.AsyncClient(timeout=120.0) as client:
#                 response = await client.post(url, headers=headers, json=payload)
#                 if response.status_code == 200:
#                     result = response.json()
#                     if isinstance(result, list) and len(result) > 0:
#                         generated_text = result[0].get("generated_text", "").strip()
#                         if generated_text:
#                             return generated_text
#                     elif isinstance(result, dict):
#                         generated_text = result.get("generated_text", "").strip()
#                         if generated_text:
#                             return generated_text
#                 logger.warning(f"Hugging Face API response: {response.status_code} - {response.text}")
#                 return None
#         except Exception as e:
#             logger.error(f"Error querying Hugging Face API: {str(e)}")
#             return None
#     else:
#         logger.warning("No LLM API key found.")
#         return None

# def create_advanced_tutor_prompt(message: str, user_name: Optional[str] = None, topic: Optional[str] = None, conversation_context: List = None) -> str:
#     # [Identical to your current function. Redacted for brevity.]
#     # -- Insert your copy-pasted prompt creation logic here --
#     ...
#     # NOTE: No changes here; you can use your same logic.

# class ChatRequest(BaseModel):
#     message: str
#     user_name: Optional[str] = None
#     topic: Optional[str] = None

# class ChatResponse(BaseModel):
#     response: str
#     status: str = "success"

# def get_premium_educational_response(message: str, user_name: Optional[str] = None, conversation_context: List = None) -> str:
#     # [Identical to your current function. Redacted for brevity.]
#     ...
#     # NOTE: No changes here; you can use your same logic.

# @app.get("/")
# async def root():
#     """Health check endpoint"""
#     return {"message": "AI Tutor Bot API is running!", "status": "healthy"}

# @app.get("/health")
# async def health_check():
#     services = {
#         "huggingface_available": bool(HUGGINGFACE_API_KEY and HUGGINGFACE_API_KEY != "your_huggingface_api_key_here"),
#         "fallback_available": True
#     }
#     primary_service = "huggingface" if services["huggingface_available"] else "fallback"
#     return {
#         "status": "healthy",
#         "primary_llm_service": primary_service,
#         "available_services": services,
#         "model_info": {
#             "huggingface_model": MODEL_NAME if services["huggingface_available"] else None
#         }
#     }


# @app.post("/chat", response_model=ChatResponse)
# async def chat(request: ChatRequest):
#     try:
#         session_key = request.user_name or "anonymous"
#         user_conversations = load_user_history(session_key)
#         if session_key not in conversation_history:
#             conversation_history[session_key] = user_conversations.copy()

#         user_entry = {
#             "timestamp": datetime.now().isoformat(),
#             "message": request.message,
#             "sender": "user",
#             "topic": request.topic
#         }
#         conversation_history[session_key].append(user_entry)

#         response_text = None

#         prompt = create_advanced_tutor_prompt(
#             request.message,
#             request.user_name,
#             request.topic,
#             conversation_history[session_key]
#         )
#         response_text = await query_llm(prompt)

#         if not response_text:
#             response_text = get_premium_educational_response(
#                 request.message,
#                 request.user_name,
#                 conversation_history[session_key]
#             )

#         bot_entry = {
#             "timestamp": datetime.now().isoformat(),
#             "message": response_text,
#             "sender": "bot",
#             "topic": request.topic
#         }
#         conversation_history[session_key].append(bot_entry)

#         if session_key != "anonymous":
#             save_user_history(session_key, conversation_history[session_key])

#         if len(conversation_history[session_key]) > 20:
#             conversation_history[session_key] = conversation_history[session_key][-20:]

#         return ChatResponse(response=response_text)

#     except Exception as e:
#         logger.error(f"Error in chat endpoint: {str(e)}")
#         return ChatResponse(response="I'm experiencing some technical difficulties, but I'm still here to help you learn! Could you try asking your question again? 🤔")

# @app.get("/history/{user_name}")
# async def get_conversation_history(user_name: str):
#     try:
#         conversations = load_user_history(user_name)
#         if user_name in conversation_history:
#             session_conversations = conversation_history[user_name]
#             for msg in session_conversations:
#                 if msg not in conversations:
#                     conversations.append(msg)
#         return {
#             "history": conversations,
#             "total_messages": len(conversations),
#             "user_name": user_name
#         }
#     except Exception as e:
#         logger.error(f"Error getting history for {user_name}: {str(e)}")
#         return {"history": [], "total_messages": 0, "user_name": user_name}

# @app.get("/users/{user_name}/stats")
# async def get_user_statistics(user_name: str):
#     try:
#         stats = get_user_stats(user_name)
#         return {
#             "user_name": user_name,
#             "statistics": stats,
#             "status": "success"
#         }
#     except Exception as e:
#         logger.error(f"Error getting stats for {user_name}: {str(e)}")
#         return {
#             "user_name": user_name,
#             "statistics": {},
#             "status": "error",
#             "message": str(e)
#         }

# @app.delete("/users/{user_name}/history")
# async def clear_user_history(user_name: str):
#     try:
#         file_path = get_user_file_path(user_name)
#         if file_path.exists():
#             file_path.unlink()
#         if user_name in conversation_history:
#             del conversation_history[user_name]
#         return {
#             "message": f"History cleared for user {user_name}",
#             "status": "success"
#         }
#     except Exception as e:
#         logger.error(f"Error clearing history for {user_name}: {str(e)}")
#         return {
#             "message": f"Error clearing history: {str(e)}",
#             "status": "error"
#         }

# @app.get("/users")
# async def list_users():
#     try:
#         users = []
#         for file_path in USER_DATA_DIR.glob("*_conversations.json"):
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     data = json.load(f)
#                     user_info = {
#                         "user_name": data.get('user_name', 'Unknown'),
#                         "last_updated": data.get('last_updated'),
#                         "total_messages": data.get('total_messages', 0)
#                     }
#                     users.append(user_info)
#             except Exception as e:
#                 logger.warning(f"Error reading user file {file_path}: {str(e)}")
#                 continue
#         return {
#             "users": sorted(users, key=lambda x: x.get('last_updated', ''), reverse=True),
#             "total_users": len(users)
#         }
#     except Exception as e:
#         logger.error(f"Error listing users: {str(e)}")
#         return {"users": [], "total_users": 0}

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import httpx
# import os
# from dotenv import load_dotenv
# import logging
# from typing import Optional, List, Dict
# import json
# from datetime import datetime
# from pathlib import Path
# import asyncio
# from concurrent.futures import ThreadPoolExecutor

# # Load environment variables
# load_dotenv()

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
# GEMINI_API_URL = os.getenv(
#     "GEMINI_API_URL",
#     "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
# )

# if GEMINI_API_KEY:
#     logger.info("Google Gemini API Key loaded: Yes")
# else:
#     logger.warning("Google Gemini API Key loaded: No (GEMINI_API_KEY missing)")

# app = FastAPI(
#     title="AI Tutor Bot API",
#     description="Backend API for AI Tutor Bot with Gemini integration",
#     version="1.0.0"
# )

# origins = os.getenv("CORS_ORIGINS", "http://localhost:3001").split(",")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# USER_DATA_DIR = Path("user_data")
# USER_DATA_DIR.mkdir(exist_ok=True)

# conversation_history: Dict[str, List[Dict]] = {}

# def get_user_file_path(user_name: str) -> Path:
#     safe_name = "".join(c for c in user_name if c.isalnum() or c in (' ', '-', '_')).strip()
#     safe_name = safe_name.replace(' ', '_')
#     return USER_DATA_DIR / f"{safe_name}_conversations.json"

# def load_user_history(user_name: str) -> List[Dict]:
#     file_path = get_user_file_path(user_name)
#     try:
#         if file_path.exists():
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 data = json.load(f)
#                 return data.get('conversations', [])
#     except Exception as e:
#         logger.error(f"Error loading user history for {user_name}: {str(e)}")
#     return []

# def save_user_history(user_name: str, conversations: List[Dict]) -> bool:
#     file_path = get_user_file_path(user_name)
#     try:
#         user_data = {
#             'user_name': user_name,
#             'last_updated': datetime.now().isoformat(),
#             'total_messages': len(conversations),
#             'conversations': conversations[-50:]
#         }
#         with open(file_path, 'w', encoding='utf-8') as f:
#             json.dump(user_data, f, indent=2, ensure_ascii=False)
#         return True
#     except Exception as e:
#         logger.error(f"Error saving user history for {user_name}: {str(e)}")
#         return False

# def get_user_stats(user_name: str) -> Dict:
#     file_path = get_user_file_path(user_name)
#     stats = {
#         'total_sessions': 0,
#         'total_messages': 0,
#         'first_visit': None,
#         'last_visit': None,
#         'favorite_topics': []
#     }
#     try:
#         if file_path.exists():
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 data = json.load(f)
#                 conversations = data.get('conversations', [])
#                 if conversations:
#                     stats['total_messages'] = len([m for m in conversations if m.get('sender') == 'user'])
#                     stats['first_visit'] = conversations[0].get('timestamp')
#                     stats['last_visit'] = conversations[-1].get('timestamp')
#                     topics = {}
#                     for msg in conversations:
#                         if msg.get('sender') == 'user':
#                             msg_text = msg.get('message', '').lower()
#                             for topic in ['math', 'science', 'history', 'physics', 'chemistry', 'biology']:
#                                 if topic in msg_text:
#                                     topics[topic] = topics.get(topic, 0) + 1
#                     stats['favorite_topics'] = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:3]
#     except Exception as e:
#         logger.error(f"Error getting user stats for {user_name}: {str(e)}")
#     return stats

# async def query_gemini(prompt: str) -> str:
#     if not GEMINI_API_KEY:
#         logger.error("Google Gemini API key is missing.")
#         return "Gemini API key missing."
#     headers = {"Content-Type": "application/json"}
#     params = {"key": GEMINI_API_KEY}
#     payload = {
#         "contents": [
#             {
#                 "parts": [
#                     {"text": prompt}
#                 ]
#             }
#         ],
#         # Removed temperature and maxOutputTokens fields to avoid 400 error
#     }
#     try:
#         async with httpx.AsyncClient(timeout=60.0) as client:
#             response = await client.post(GEMINI_API_URL, headers=headers, params=params, json=payload)
#             if response.status_code == 200:
#                 data = response.json()
#                 candidates = data.get("candidates", [])
#                 if candidates:
#                     parts = candidates[0].get("content", {}).get("parts", [])
#                     if parts and "text" in parts[0]:
#                         return parts[0]["text"].strip()
#                 logger.warning("Gemini API: No valid text found in response.")
#                 return "Sorry, I couldn't generate a response. Please try again."
#             else:
#                 logger.warning(f"Gemini API response: {response.status_code} - {response.text}")
#                 return f"Gemini API error: {response.status_code} - {response.text}"
#     except Exception as e:
#         logger.error(f"Error querying Gemini API: {str(e)}")
#         return f"Error querying Gemini API: {str(e)}"

# # async def query_gemini(prompt: str) -> str:
# #     if not GEMINI_API_KEY:
# #         logger.error("Google Gemini API key is missing.")
# #         return "Gemini API key missing."
# #     headers = {"Content-Type": "application/json"}
# #     params = {"key": GEMINI_API_KEY}
# #     payload = {
# #         "contents": [
# #             {
# #                 "parts": [
# #                     {"text": prompt}
# #                 ]
# #             }
# #         ],
# #         "temperature": 0.7,
# #         "maxOutputTokens": 200
# #     }
# #     try:
# #         async with httpx.AsyncClient(timeout=60.0) as client:
# #             response = await client.post(GEMINI_API_URL, headers=headers, params=params, json=payload)
# #             if response.status_code == 200:
# #                 data = response.json()
# #                 candidates = data.get("candidates", [])
# #                 if candidates:
# #                     parts = candidates[0].get("content", {}).get("parts", [])
# #                     if parts and "text" in parts[0]:
# #                         return parts[0]["text"].strip()
# #                 logger.warning("Gemini API: No valid text found in response.")
# #                 return "Sorry, I couldn't generate a response. Please try again."
# #             else:
# #                 logger.warning(f"Gemini API response: {response.status_code} - {response.text}")
# #                 return f"Gemini API error: {response.status_code} - {response.text}"
# #     except Exception as e:
# #         logger.error(f"Error querying Gemini API: {str(e)}")
# #         return f"Error querying Gemini API: {str(e)}"

# def create_advanced_tutor_prompt(
#     message: str,
#     user_name: Optional[str] = None,
#     topic: Optional[str] = None,
#     conversation_context: List = None
# ) -> str:
#     # Use your full existing prompt template here
#     # Example simple prompt:
#     prompt = f"{user_name or 'Student'} asked: {message}\nProvide an educational, detailed, and inspiring answer."
#     return prompt

# def get_premium_educational_response(
#     message: str,
#     user_name: Optional[str] = None,
#     conversation_context: List = None
# ) -> str:
#     # Use your fallback logic or just a basic message
#     return "Sorry, I couldn't generate a response right now, but I'm here to help you learn! Try asking again in a moment."

# class ChatRequest(BaseModel):
#     message: str
#     user_name: Optional[str] = None
#     topic: Optional[str] = None

# class ChatResponse(BaseModel):
#     response: str
#     status: str = "success"

# @app.get("/")
# async def root():
#     return {"message": "AI Tutor Bot API is running!", "status": "healthy"}

# @app.get("/health")
# async def health_check():
#     return {
#         "status": "healthy",
#         "primary_llm_service": "gemini" if GEMINI_API_KEY else "none",
#         "available_services": {
#             "gemini_available": bool(GEMINI_API_KEY)
#         },
#         "model_info": {
#             "gemini_model": GEMINI_API_URL if GEMINI_API_KEY else None
#         }
#     }

# @app.post("/chat", response_model=ChatResponse)
# async def chat(request: ChatRequest):
#     try:
#         session_key = request.user_name or "anonymous"
#         user_conversations = load_user_history(session_key)
#         if session_key not in conversation_history:
#             conversation_history[session_key] = user_conversations.copy()

#         user_entry = {
#             "timestamp": datetime.now().isoformat(),
#             "message": request.message,
#             "sender": "user",
#             "topic": request.topic
#         }
#         conversation_history[session_key].append(user_entry)

#         prompt = create_advanced_tutor_prompt(
#             request.message,
#             request.user_name,
#             request.topic,
#             conversation_history[session_key]
#         )
#         response_text = await query_gemini(prompt)
#         if not response_text:
#             response_text = get_premium_educational_response(
#                 request.message,
#                 request.user_name,
#                 conversation_history[session_key]
#             )

#         bot_entry = {
#             "timestamp": datetime.now().isoformat(),
#             "message": response_text,
#             "sender": "bot",
#             "topic": request.topic
#         }
#         conversation_history[session_key].append(bot_entry)

#         if session_key != "anonymous":
#             save_user_history(session_key, conversation_history[session_key])

#         if len(conversation_history[session_key]) > 20:
#             conversation_history[session_key] = conversation_history[session_key][-20:]

#         return ChatResponse(response=response_text)

#     except Exception as e:
#         logger.error(f"Error in chat endpoint: {str(e)}")
#         return ChatResponse(
#             response="I'm experiencing some technical difficulties, but I'm still here to help you learn! Could you try asking your question again? 🤔"
#         )

# @app.get("/history/{user_name}")
# async def get_conversation_history(user_name: str):
#     try:
#         conversations = load_user_history(user_name)
#         if user_name in conversation_history:
#             session_conversations = conversation_history[user_name]
#             for msg in session_conversations:
#                 if msg not in conversations:
#                     conversations.append(msg)
#         return {
#             "history": conversations,
#             "total_messages": len(conversations),
#             "user_name": user_name
#         }
#     except Exception as e:
#         logger.error(f"Error getting history for {user_name}: {str(e)}")
#         return {"history": [], "total_messages": 0, "user_name": user_name}

# @app.get("/users/{user_name}/stats")
# async def get_user_statistics(user_name: str):
#     try:
#         stats = get_user_stats(user_name)
#         return {
#             "user_name": user_name,
#             "statistics": stats,
#             "status": "success"
#         }
#     except Exception as e:
#         logger.error(f"Error getting stats for {user_name}: {str(e)}")
#         return {
#             "user_name": user_name,
#             "statistics": {},
#             "status": "error",
#             "message": str(e)
#         }

# @app.delete("/users/{user_name}/history")
# async def clear_user_history(user_name: str):
#     try:
#         file_path = get_user_file_path(user_name)
#         if file_path.exists():
#             file_path.unlink()
#         if user_name in conversation_history:
#             del conversation_history[user_name]
#         return {
#             "message": f"History cleared for user {user_name}",
#             "status": "success"
#         }
#     except Exception as e:
#         logger.error(f"Error clearing history for {user_name}: {str(e)}")
#         return {
#             "message": f"Error clearing history: {str(e)}",
#             "status": "error"
#         }

# @app.get("/users")
# async def list_users():
#     try:
#         users = []
#         for file_path in USER_DATA_DIR.glob("*_conversations.json"):
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     data = json.load(f)
#                     users.append({
#                         "user_name": data.get('user_name', 'Unknown'),
#                         "last_updated": data.get('last_updated'),
#                         "total_messages": data.get('total_messages', 0)
#                     })
#             except Exception as e:
#                 logger.warning(f"Error reading user file {file_path}: {str(e)}")
#                 continue
#         return {
#             "users": sorted(users, key=lambda x: x.get('last_updated', ''), reverse=True),
#             "total_users": len(users)
#         }
#     except Exception as e:
#         logger.error(f"Error listing users: {str(e)}")
#         return {"users": [], "total_users": 0}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import logging
from typing import Optional, List, Dict
import json
from datetime import datetime
from pathlib import Path
import cohere

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COHERE_API_KEY = os.getenv("COHERE_API_KEY", "").strip()
if COHERE_API_KEY:
    logger.info("Cohere API Key loaded: Yes")
else:
    logger.warning("Cohere API Key loaded: No (COHERE_API_KEY missing)")

# Initialize Cohere client once (non-async Co here has no official async, so we'll run in threadpool)
cohere_client = cohere.Client(COHERE_API_KEY)

app = FastAPI(
    title="AI Tutor Bot API",
    description="Backend API for AI Tutor Bot with Cohere integration",
    version="1.0.0"
)

origins = os.getenv("CORS_ORIGINS", "http://localhost:3001").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USER_DATA_DIR = Path("user_data")
USER_DATA_DIR.mkdir(exist_ok=True)
conversation_history: Dict[str, List[Dict]] = {}

def get_user_file_path(user_name: str) -> Path:
    safe_name = "".join(c for c in user_name if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_name = safe_name.replace(' ', '_')
    return USER_DATA_DIR / f"{safe_name}_conversations.json"

def load_user_history(user_name: str) -> List[Dict]:
    file_path = get_user_file_path(user_name)
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('conversations', [])
    except Exception as e:
        logger.error(f"Error loading user history for {user_name}: {str(e)}")
    return []

def save_user_history(user_name: str, conversations: List[Dict]) -> bool:
    file_path = get_user_file_path(user_name)
    try:
        user_data = {
            'user_name': user_name,
            'last_updated': datetime.now().isoformat(),
            'total_messages': len(conversations),
            'conversations': conversations[-50:]
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Error saving user history for {user_name}: {str(e)}")
        return False

def get_user_stats(user_name: str) -> Dict:
    file_path = get_user_file_path(user_name)
    stats = {
        'total_sessions': 0,
        'total_messages': 0,
        'first_visit': None,
        'last_visit': None,
        'favorite_topics': []
    }
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                conversations = data.get('conversations', [])
                if conversations:
                    stats['total_messages'] = len([m for m in conversations if m.get('sender') == 'user'])
                    stats['first_visit'] = conversations[0].get('timestamp')
                    stats['last_visit'] = conversations[-1].get('timestamp')
                    topics = {}
                    for msg in conversations:
                        if msg.get('sender') == 'user':
                            msg_text = msg.get('message', '').lower()
                            for topic in ['math', 'science', 'history', 'physics', 'chemistry', 'biology']:
                                if topic in msg_text:
                                    topics[topic] = topics.get(topic, 0) + 1
                    stats['favorite_topics'] = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:3]
    except Exception as e:
        logger.error(f"Error getting user stats for {user_name}: {str(e)}")
    return stats

import asyncio
from concurrent.futures import ThreadPoolExecutor

async def query_cohere(prompt: str, history: list) -> str:
    if not COHERE_API_KEY:
        logger.error("Cohere API key is missing.")
        return "Cohere API key missing."

    # Format conversation history with proper roles (case-sensitive)
    chat_hist = []
    for turn in history[-5:]:
        sender = turn.get("sender", "user")
        if sender.lower() == "user":
            role = "User"
        else:
            role = "Chatbot"
        chat_hist.append({"role": role, "message": turn.get("message", "")})
    
    def sync_call():
        return cohere_client.chat(
            model="command-xlarge-nightly",
            chat_history=chat_hist,
            message=prompt,            # current user message
            max_tokens=200,
            temperature=0.7
        )
    
    with ThreadPoolExecutor() as pool:
        response = await asyncio.get_event_loop().run_in_executor(pool, sync_call)

    try:
        return response.text.strip()
    except Exception as e:
        logger.error(f"Cohere chat API error: {str(e)}")
        return "Sorry, I couldn't generate a response right now. Please try again soon."
# async def query_cohere(prompt: str, history: List[Dict]) -> str:
#     """
#     Call Cohere's `generate` endpoint.
#     Format conversation history for better context.
#     """
#     if not COHERE_API_KEY:
#         logger.error("Cohere API key is missing.")
#         return "Cohere API key missing."
    
#     # Compose conversation context as context for prompt.
#     conversation = ""
#     for turn in history[-5:]:
#         speaker = turn.get("sender", "user")
#         msg = turn.get("message","")
#         if speaker and msg:
#             conversation += f"{speaker}: {msg}\n"
#     conversation += f"user: {prompt}\nbot:"
    
#     def sync_call():
#         return cohere_client.generate(
#             model="command-xlarge-nightly",  # Replace with another public model if you wish
#             prompt=conversation,
#             max_tokens=200,
#             temperature=0.7,
#             stop_sequences=["user:", "bot:"]
#         )
    
#     with ThreadPoolExecutor() as pool:
#         gen = await asyncio.get_event_loop().run_in_executor(pool, sync_call)
#     try:
#         return gen.generations[0].text.strip()
#     except Exception as e:
#         logger.error(f"Cohere API error: {str(e)}")
#         return "Sorry, I couldn't generate a response right now. Please try again soon."

# def create_advanced_tutor_prompt(
#     message: str,
#     user_name: Optional[str] = None,
#     topic: Optional[str] = None,
#     conversation_context: List = None
# ) -> str:
#     # You can further expand this prompt if needed
#     prompt = f"{user_name or 'Student'} asked: {message}\nProvide an educational, detailed, and inspiring answer."
#     return prompt
def create_advanced_tutor_prompt(
    message: str,
    user_name: Optional[str] = None,
    topic: Optional[str] = None,
    conversation_context: List = None,
    continuation_mode: bool = False
) -> str:
    if continuation_mode:
        prompt = (
            f"{user_name or 'Student'} asked: {message}\n"
            "Please continue with a detailed and in-depth explanation."
        )
    else:
        prompt = (
            f"{user_name or 'Student'} asked: {message}\n"
            "Please provide a clear and concise answer, limited to a few sentences."
        )
    return prompt


def get_premium_educational_response(
    message: str,
    user_name: Optional[str] = None,
    conversation_context: List = None
) -> str:
    return "Sorry, I couldn't generate a response right now, but I'm here to help you learn! Try asking again in a moment."

class ChatRequest(BaseModel):
    message: str
    user_name: Optional[str] = None
    topic: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

@app.get("/")
async def root():
    return {"message": "AI Tutor Bot API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "primary_llm_service": "cohere" if COHERE_API_KEY else "none",
        "available_services": {
            "cohere_available": bool(COHERE_API_KEY)
        },
        "model_info": {
            "cohere_model": "command-xlarge-nightly" if COHERE_API_KEY else None
        }
    }
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        session_key = request.user_name or "anonymous"
        user_conversations = load_user_history(session_key)
        if session_key not in conversation_history:
            conversation_history[session_key] = user_conversations.copy()

        user_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": request.message,
            "sender": "user",
            "topic": request.topic
        }
        conversation_history[session_key].append(user_entry)

        # Detect if user wants continuation / more detail
        continuation_phrases = ['carry on', 'continue', 'tell me more', 'please elaborate', 'more details']
        user_message_lower = request.message.lower()
        continuation_mode = any(phrase in user_message_lower for phrase in continuation_phrases)

        # Pass the flag to prompt creation
        prompt = create_advanced_tutor_prompt(
            request.message,
            request.user_name,
            request.topic,
            conversation_history[session_key],
            continuation_mode=continuation_mode
        )

        response_text = await query_cohere(prompt, conversation_history[session_key])
        if not response_text:
            response_text = get_premium_educational_response(
                request.message,
                request.user_name,
                conversation_history[session_key]
            )

        bot_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": response_text,
            "sender": "bot",
            "topic": request.topic
        }
        conversation_history[session_key].append(bot_entry)

        if session_key != "anonymous":
            save_user_history(session_key, conversation_history[session_key])

        if len(conversation_history[session_key]) > 20:
            conversation_history[session_key] = conversation_history[session_key][-20:]

        return ChatResponse(response=response_text)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return ChatResponse(
            response="I'm experiencing some technical difficulties, but I'm still here to help you learn! Could you try asking your question again? 🤔"
        )

# @app.post("/chat", response_model=ChatResponse)
# async def chat(request: ChatRequest):
#     try:
#         session_key = request.user_name or "anonymous"
#         user_conversations = load_user_history(session_key)
#         if session_key not in conversation_history:
#             conversation_history[session_key] = user_conversations.copy()

#         user_entry = {
#             "timestamp": datetime.now().isoformat(),
#             "message": request.message,
#             "sender": "user",
#             "topic": request.topic
#         }
#         conversation_history[session_key].append(user_entry)

#         prompt = create_advanced_tutor_prompt(
#             request.message,
#             request.user_name,
#             request.topic,
#             conversation_history[session_key]
#         )
#         response_text = await query_cohere(prompt, conversation_history[session_key])
#         if not response_text:
#             response_text = get_premium_educational_response(
#                 request.message,
#                 request.user_name,
#                 conversation_history[session_key]
#             )

#         bot_entry = {
#             "timestamp": datetime.now().isoformat(),
#             "message": response_text,
#             "sender": "bot",
#             "topic": request.topic
#         }
#         conversation_history[session_key].append(bot_entry)

#         if session_key != "anonymous":
#             save_user_history(session_key, conversation_history[session_key])

#         if len(conversation_history[session_key]) > 20:
#             conversation_history[session_key] = conversation_history[session_key][-20:]

#         return ChatResponse(response=response_text)

#     except Exception as e:
#         logger.error(f"Error in chat endpoint: {str(e)}")
#         return ChatResponse(
#             response="I'm experiencing some technical difficulties, but I'm still here to help you learn! Could you try asking your question again? 🤔"
#         )

@app.get("/history/{user_name}")
async def get_conversation_history(user_name: str):
    try:
        conversations = load_user_history(user_name)
        if user_name in conversation_history:
            session_conversations = conversation_history[user_name]
            for msg in session_conversations:
                if msg not in conversations:
                    conversations.append(msg)
        return {
            "history": conversations,
            "total_messages": len(conversations),
            "user_name": user_name
        }
    except Exception as e:
        logger.error(f"Error getting history for {user_name}: {str(e)}")
        return {"history": [], "total_messages": 0, "user_name": user_name}

@app.get("/users/{user_name}/stats")
async def get_user_statistics(user_name: str):
    try:
        stats = get_user_stats(user_name)
        return {
            "user_name": user_name,
            "statistics": stats,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error getting stats for {user_name}: {str(e)}")
        return {
            "user_name": user_name,
            "statistics": {},
            "status": "error",
            "message": str(e)
        }

@app.delete("/users/{user_name}/history")
async def clear_user_history(user_name: str):
    try:
        file_path = get_user_file_path(user_name)
        if file_path.exists():
            file_path.unlink()
        if user_name in conversation_history:
            del conversation_history[user_name]
        return {
            "message": f"History cleared for user {user_name}",
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error clearing history for {user_name}: {str(e)}")
        return {
            "message": f"Error clearing history: {str(e)}",
            "status": "error"
        }

@app.get("/users")
async def list_users():
    try:
        users = []
        for file_path in USER_DATA_DIR.glob("*_conversations.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    users.append({
                        "user_name": data.get('user_name', 'Unknown'),
                        "last_updated": data.get('last_updated'),
                        "total_messages": data.get('total_messages', 0)
                    })
            except Exception as e:
                logger.warning(f"Error reading user file {file_path}: {str(e)}")
                continue
        return {
            "users": sorted(users, key=lambda x: x.get('last_updated', ''), reverse=True),
            "total_users": len(users)
        }
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        return {"users": [], "total_users": 0}
