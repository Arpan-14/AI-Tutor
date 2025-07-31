import React from 'react'

const TypingIndicator = () => {
  return (
    <div className="flex justify-start animate-fadeIn">
      <div className="flex items-end space-x-3">
        {/* Avatar */}
        <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center shadow-md">
          <span className="text-white">🤖</span>
        </div>
        
        {/* Typing Bubble */}
        <div className="bg-white border border-gray-200 px-6 py-4 rounded-2xl shadow-lg">
          <div className="flex items-center space-x-2">
            <div className="text-xs font-semibold text-blue-600 mb-1">
              🤖 AI Tutor is typing...
            </div>
          </div>
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TypingIndicator
