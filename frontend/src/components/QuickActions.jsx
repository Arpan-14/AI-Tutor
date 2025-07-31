import React from 'react'

const QuickActions = ({ onAction, disabled }) => {
  const actions = [
    {
      id: 'learn',
      label: 'Learn Topic',
      icon: '📚',
      description: 'Explore a new subject',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      id: 'test',
      label: 'Test Knowledge',
      icon: '🧠',
      description: 'Quiz yourself',
      color: 'from-purple-500 to-pink-500'
    },
    {
      id: 'explain',
      label: 'Explain Concept',
      icon: '💡',
      description: 'Get detailed explanations',
      color: 'from-orange-500 to-red-500'
    },
    {
      id: 'practice',
      label: 'Practice Problems',
      icon: '✏️',
      description: 'Work on exercises',
      color: 'from-green-500 to-emerald-500'
    }
  ]

  return (
    <div className="mt-8">
      <div className="text-center mb-6">
        <h3 className="text-2xl font-bold text-gray-800 mb-2">Quick Learning Actions</h3>
        <p className="text-gray-600">Choose what you'd like to explore today</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {actions.map((action) => (
          <button
            key={action.id}
            onClick={() => onAction(action.id)}
            disabled={disabled}
            className={`group p-6 rounded-2xl bg-gradient-to-r ${action.color} text-white shadow-lg hover:shadow-xl transform transition-all duration-200 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none`}
          >
            <div className="flex flex-col items-center text-center">
              <div className="text-4xl mb-3 group-hover:scale-110 transition-transform duration-200">
                {action.icon}
              </div>
              <div className="font-semibold text-lg mb-1">
                {action.label}
              </div>
              <div className="text-sm opacity-90">
                {action.description}
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}

export default QuickActions
