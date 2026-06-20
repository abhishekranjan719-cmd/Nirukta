import { useState } from 'react'
import MessageList from './MessageList'
import MessageInput from './MessageInput'
import type { Conversation, Message } from '../types/chat'
import { sendMessage } from '../api/client'

interface ChatInterfaceProps {
  conversation: Conversation | undefined
  onUpdateConversation: (conversation: Conversation) => void
  onNewConversation: () => void
}

export default function ChatInterface({
  conversation,
  onUpdateConversation,
  onNewConversation,
}: ChatInterfaceProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [orchestrationMode, setOrchestrationMode] = useState<'workflow' | 'agent'>('workflow')

  const handleSendMessage = async (content: string) => {
    if (!conversation) {
      onNewConversation()
      return
    }

    setError(null)
    setIsLoading(true)

    // Add user message optimistically
    const userMessage: Message = {
      role: 'user',
      content,
      timestamp: new Date(),
    }

    const updatedConversation: Conversation = {
      ...conversation,
      messages: [...conversation.messages, userMessage],
      title:
        conversation.messages.length === 0
          ? content.slice(0, 30) + (content.length > 30 ? '...' : '')
          : conversation.title,
      updatedAt: new Date(),
    }

    onUpdateConversation(updatedConversation)

    try {
      // Send to backend with orchestration mode
      const response = await sendMessage({
        message: content,
        conversation_id: conversation.id,
        orchestration_mode: orchestrationMode,
      })

      // Add assistant message
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date(response.timestamp),
      }

      onUpdateConversation({
        ...updatedConversation,
        messages: [...updatedConversation.messages, assistantMessage],
        updatedAt: new Date(),
      })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message')
      console.error('Failed to send message:', err)
    } finally {
      setIsLoading(false)
    }
  }

  if (!conversation) {
    return (
      <div className="main-content">
        <div className="empty-state">
          <div className="empty-state-icon">💬</div>
          <h3>Welcome to Zuna</h3>
          <p>Select a conversation or create a new one to get started</p>
        </div>
      </div>
    )
  }

  return (
    <div className="main-content">
      <div className="chat-header">
        <h2>{conversation.title}</h2>
        <div className="orchestration-toggle">
          <label className="toggle-label">
            <span className={orchestrationMode === 'workflow' ? 'mode-active' : 'mode-inactive'}>
              Workflow
            </span>
            <label className="switch">
              <input
                type="checkbox"
                checked={orchestrationMode === 'agent'}
                onChange={(e) => setOrchestrationMode(e.target.checked ? 'agent' : 'workflow')}
                disabled={isLoading}
              />
              <span className="slider"></span>
            </label>
            <span className={orchestrationMode === 'agent' ? 'mode-active' : 'mode-inactive'}>
              Agent
            </span>
          </label>
          <div className="mode-description">
            {orchestrationMode === 'workflow'
              ? '🔗 Chain-based sequential processing'
              : '🤖 Agent-based autonomous reasoning'}
          </div>
        </div>
      </div>

      {error && (
        <div className="error-message">
          Error: {error}
        </div>
      )}

      <MessageList messages={conversation.messages} isLoading={isLoading} />
      <MessageInput onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  )
}
