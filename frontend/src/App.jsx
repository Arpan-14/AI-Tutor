import React, { useState, useRef, useEffect } from 'react'
import ChatMessage from './components/ChatMessage'
import QuickActions from './components/QuickActions'
import TypingIndicator from './components/TypingIndicator'
import HistoryPanel from './components/HistoryPanel'
import { sendChatMessage, fetchUserHistory, fetchUserStats } from './api'

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your AI Tutor Bot. I'm here to help you learn new topics and test your knowledge. What would you like to explore today?",
      sender: 'bot',
      timestamp: new Date()
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [userName, setUserName] = useState('')
  const [currentTopic, setCurrentTopic] = useState('')
  const [showHistory, setShowHistory] = useState(false)
  const [userStats, setUserStats] = useState(null)
  const [isReturningUser, setIsReturningUser] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return

    const userMessage = {
      id: Date.now(),
      text: messageText,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsTyping(true)

    try {
      const botResponse = await sendChatMessage(messageText, userName, currentTopic)
      const botMessage = {
        id: Date.now() + 1,
        text: botResponse,
        sender: 'bot',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I'm having trouble connecting right now. Please try again later.",
        sender: 'bot',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsTyping(false)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    sendMessage(inputMessage)
  }

  const handleQuickAction = (action) => {
    switch (action) {
      case 'learn':
        sendMessage("I'd like to learn about a new topic.")
        break
      case 'test':
        sendMessage("I'd like to test my knowledge.")
        break
      case 'explain':
        sendMessage("Can you explain this concept in detail?")
        break
      case 'practice':
        sendMessage("I need practice problems.")
        break
    }
  }

  const handleNameSubmit = async (name) => {
    setUserName(name)
    try {
      // Check if user has previous history
      const historyData = await fetchUserHistory(name)
      if (historyData.history && historyData.history.length > 0) {
        setIsReturningUser(true)
        // Load previous conversation history
        const previousMessages = historyData.history.map((msg, index) => ({
          id: index + 1000,
          text: msg.message,
          sender: msg.sender,
          timestamp: new Date(msg.timestamp)
        }))
        // Keep initial bot message and add previous history
        setMessages(prev => [
          ...prev,
          {
            id: Date.now(),
            text: `Welcome back, ${name}! 🎉 I can see we've had some great learning sessions together. I remember our previous conversations and I'm excited to continue helping you learn and grow!`,
            sender: 'bot',
            timestamp: new Date()
          },
          ...previousMessages.slice(-10)
        ])
      } else {
        // New user
        const welcomeMessage = {
          id: Date.now(),
          text: `Nice to meet you, ${name}! 🌟 I'm excited to start this learning journey with you. What subject interests you today?`,
          sender: 'bot',
          timestamp: new Date()
        }
        setMessages(prev => [...prev, welcomeMessage])
      }
      // Get user statistics
      const statsData = await fetchUserStats(name)
      setUserStats(statsData)
    } catch (error) {
      console.error('Error loading user data:', error)
      // Fallback welcome message
      const welcomeMessage = {
        id: Date.now(),
        text: `Nice to meet you, ${name}! I'm excited to help you on your learning journey. What subject interests you today?`,
        sender: 'bot',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, welcomeMessage])
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50">
      <div className="container mx-auto px-4 py-6 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-8 relative">
          <div className="flex items-center justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-lg mr-4">
              <span className="text-3xl">🤖</span>
            </div>
            <div>
              <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
                AI Tutor Bot
              </h1>
              <p className="text-gray-600 text-lg">
                Your intelligent learning companion powered by AI
              </p>
            </div>
          </div>
          
          {/* Enhanced Stats Bar */}
          {userName && (
            <div className="flex justify-center space-x-6 mb-6">
              <div className="bg-white rounded-lg shadow-md px-4 py-2 border-l-4 border-blue-500">
                <div className="text-sm text-gray-600">This Session</div>
                <div className="text-lg font-semibold text-blue-600">{messages.length - 1} messages</div>
              </div>
              
              {userStats && userStats.total_messages > 0 && (
                <div className="bg-white rounded-lg shadow-md px-4 py-2 border-l-4 border-green-500">
                  <div className="text-sm text-gray-600">Total Messages</div>
                  <div className="text-lg font-semibold text-green-600">{userStats.total_messages}</div>
                </div>
              )}
              
              {isReturningUser && (
                <div className="bg-white rounded-lg shadow-md px-4 py-2 border-l-4 border-purple-500">
                  <div className="text-sm text-gray-600">Status</div>
                  <div className="text-lg font-semibold text-purple-600">Returning Learner</div>
                </div>
              )}
              
              {userStats && userStats.favorite_topics && userStats.favorite_topics.length > 0 && (
                <div className="bg-white rounded-lg shadow-md px-4 py-2 border-l-4 border-orange-500">
                  <div className="text-sm text-gray-600">Favorite Topic</div>
                  <div className="text-lg font-semibold text-orange-600 capitalize">
                    {userStats.favorite_topics[0][0]}
                  </div>
                </div>
              )}
            </div>
          )}
          
          {/* History Button */}
          {userName && (
            <button
              onClick={() => setShowHistory(!showHistory)}
              className="absolute top-0 right-0 bg-gradient-to-r from-gray-100 to-gray-200 hover:from-gray-200 hover:to-gray-300 text-gray-700 px-6 py-3 rounded-full transition-all duration-200 shadow-md hover:shadow-lg transform hover:scale-105"
              title="View conversation history"
            >
              <span className="flex items-center">
                📚 <span className="ml-2 font-medium">History</span>
              </span>
            </button>
          )}
        </div>

        {/* User Info Panel */}
        {!userName && (
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8 border border-gray-100">
            <div className="text-center mb-6">
              <div className="w-20 h-20 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-4xl">👋</span>
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">Welcome to AI Tutor!</h3>
              <p className="text-gray-600">Let's start your personalized learning journey</p>
            </div>
            <form onSubmit={(e) => {
              e.preventDefault()
              const name = e.target.name.value.trim()
              if (name) handleNameSubmit(name)
            }} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  What's your name?
                </label>
                <input
                  type="text"
                  name="name"
                  placeholder="Enter your name here..."
                  className="w-full p-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-lg"
                  required
                />
              </div>
              <button
                type="submit"
                className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all duration-200 font-semibold text-lg shadow-lg hover:shadow-xl transform hover:scale-[1.02]"
              >
                🚀 Start Learning Adventure
              </button>
            </form>
          </div>
        )}

        {/* Chat Container */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
          {/* Chat Header */}
          {userName && (
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 px-6 py-4 text-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="w-10 h-10 bg-white bg-opacity-20 rounded-full flex items-center justify-center mr-3">
                    <span className="text-lg">👨‍🎓</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg">Hello, {userName}!</h3>
                    <p className="text-blue-100 text-sm">Ready to learn something new?</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                  <span className="text-sm text-blue-100">Online</span>
                </div>
              </div>
            </div>
          )}
          
          {/* Messages Area */}
          <div className="h-96 overflow-y-auto p-6 space-y-4 bg-gray-50">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {isTyping && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-6 bg-white border-t border-gray-100">
            <form onSubmit={handleSubmit} className="flex space-x-4">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Ask me anything about your studies..."
                className="flex-1 p-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-lg"
                disabled={isTyping}
              />
              <button
                type="submit"
                disabled={isTyping || !inputMessage.trim()}
                className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl hover:from-blue-600 hover:to-purple-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all duration-200 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 disabled:transform-none"
              >
                {isTyping ? (
                  <span className="flex items-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Thinking...
                  </span>
                ) : (
                  <span className="flex items-center">
                    Send <span className="ml-2">🚀</span>
                  </span>
                )}
              </button>
            </form>
          </div>
        </div>

        {/* Quick Actions */}
        <QuickActions onAction={handleQuickAction} disabled={isTyping} />
        
        {/* History Panel */}
        <HistoryPanel 
          userName={userName}
          isVisible={showHistory}
          onToggle={() => setShowHistory(!showHistory)}
        />
      </div>
    </div>
  )
}

export default App
