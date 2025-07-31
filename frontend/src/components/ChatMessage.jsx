// import React from 'react'

// const ChatMessage = ({ message }) => {
//   const isBot = message.sender === 'bot'
  
//   return (
//     <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} animate-fadeIn`}>
//       <div className={`flex max-w-[80%] ${isBot ? 'flex-row' : 'flex-row-reverse'} items-end space-x-3`}>
//         {/* Avatar */}
//         <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 shadow-md ${
//           isBot 
//             ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white' 
//             : 'bg-gradient-to-r from-green-400 to-blue-500 text-white'
//         }`}>
//           {isBot ? '🤖' : '👤'}
//         </div>
        
//         {/* Message Bubble */}
//         <div className={`px-6 py-4 rounded-2xl shadow-lg transform transition-all duration-200 hover:scale-[1.02] ${
//           isBot
//             ? 'bg-white border border-gray-200 text-gray-800'
//             : 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
//         }`}>
//           {/* Sender Label */}
//           <div className={`text-xs font-semibold mb-2 ${
//             isBot ? 'text-blue-600' : 'text-blue-100'
//           }`}>
//             {isBot ? '🤖 AI Tutor' : 'You'}
//           </div>
          
//           {/* Message Content */}
//           <div className={`text-sm leading-relaxed ${
//             isBot ? 'text-gray-700' : 'text-white'
//           }`}>
//             {message.text}
//           </div>
          
//           {/* Timestamp */}
//           <div className={`text-xs mt-2 ${
//             isBot ? 'text-gray-400' : 'text-blue-100'
//           }`}>
//             {message.timestamp.toLocaleTimeString([], { 
//               hour: '2-digit', 
//               minute: '2-digit' 
//             })}
//           </div>
//         </div>
//       </div>
//     </div>
//   )
// }

// export default ChatMessage
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const ChatMessage = ({ message }) => {
  const isBot = message.sender === 'bot';

  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} animate-fadeIn`}>
      <div className={`flex max-w-[80%] ${isBot ? 'flex-row' : 'flex-row-reverse'} items-end space-x-3`}>
        {/* Avatar */}
        <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 shadow-md ${
          isBot
            ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
            : 'bg-gradient-to-r from-green-400 to-blue-500 text-white'
        }`}>
          {isBot ? '🤖' : '👤'}
        </div>

        {/* Message Bubble */}
        <div className={`px-6 py-4 rounded-2xl shadow-lg transform transition-all duration-200 hover:scale-[1.02] ${
          isBot
            ? 'bg-white border border-gray-200 text-gray-800'
            : 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
        }`}>
          {/* Sender Label */}
          <div className={`text-xs font-semibold mb-2 ${
            isBot ? 'text-blue-600' : 'text-blue-100'
          }`}>
            {isBot ? '🤖 AI Tutor' : 'You'}
          </div>

          {/* Message Content */}
          <div className={`text-sm leading-relaxed ${isBot ? 'text-gray-700' : 'text-white'}`}>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.text}
            </ReactMarkdown>
          </div>

          {/* Timestamp */}
          <div className={`text-xs mt-2 ${isBot ? 'text-gray-400' : 'text-blue-100'}`}>
            {message.timestamp.toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;
