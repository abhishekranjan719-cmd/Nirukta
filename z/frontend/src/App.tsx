import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import ConversationList from './components/ConversationList'
import type { Conversation } from './types/chat'
import { v4 as uuidv4 } from 'uuid'

function App() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null)

  const activeConversation = conversations.find(c => c.id === activeConversationId)

  const handleNewConversation = () => {
    const newConversation: Conversation = {
      id: uuidv4(),
      messages: [],
      title: 'New Conversation',
      createdAt: new Date(),
      updatedAt: new Date(),
    }
    setConversations([newConversation, ...conversations])
    setActiveConversationId(newConversation.id)
  }

  const handleSelectConversation = (conversationId: string) => {
    setActiveConversationId(conversationId)
  }

  const handleUpdateConversation = (updatedConversation: Conversation) => {
    setConversations(prevConversations =>
      prevConversations.map(conv =>
        conv.id === updatedConversation.id ? updatedConversation : conv
      )
    )
  }

  return (
    <div className="app">
      <ConversationList
        conversations={conversations}
        activeConversationId={activeConversationId}
        onNewConversation={handleNewConversation}
        onSelectConversation={handleSelectConversation}
      />
      <ChatInterface
        conversation={activeConversation}
        onUpdateConversation={handleUpdateConversation}
        onNewConversation={handleNewConversation}
      />
    </div>
  )
}

export default App
