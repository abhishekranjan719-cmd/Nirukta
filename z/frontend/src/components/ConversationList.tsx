import type { Conversation } from '../types/chat'

interface ConversationListProps {
  conversations: Conversation[]
  activeConversationId: string | null
  onNewConversation: () => void
  onSelectConversation: (conversationId: string) => void
}

export default function ConversationList({
  conversations,
  activeConversationId,
  onNewConversation,
  onSelectConversation,
}: ConversationListProps) {
  const formatTime = (date: Date) => {
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    const days = Math.floor(diff / 86400000)

    if (minutes < 1) return 'Just now'
    if (minutes < 60) return `${minutes}m ago`
    if (hours < 24) return `${hours}h ago`
    return `${days}d ago`
  }

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1>Zuna</h1>
        <p>Powered by FastAPI & React</p>
      </div>

      <button className="new-chat-button" onClick={onNewConversation}>
        + New Conversation
      </button>

      <div className="conversation-list">
        {conversations.map(conversation => (
          <div
            key={conversation.id}
            className={`conversation-item ${
              conversation.id === activeConversationId ? 'active' : ''
            }`}
            onClick={() => onSelectConversation(conversation.id)}
          >
            <div className="conversation-title">{conversation.title}</div>
            <div className="conversation-time">
              {formatTime(conversation.updatedAt)}
            </div>
          </div>
        ))}

        {conversations.length === 0 && (
          <div style={{ padding: '20px', color: '#95a5a6', textAlign: 'center' }}>
            No conversations yet.
            <br />
            Click "New Conversation" to start!
          </div>
        )}
      </div>
    </div>
  )
}
