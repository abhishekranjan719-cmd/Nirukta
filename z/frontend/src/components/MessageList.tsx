import { useEffect, useRef } from 'react'
import Message from './Message'
import type { Message as MessageType } from '../types/chat'

interface MessageListProps {
  messages: MessageType[]
  isLoading: boolean
}

export default function MessageList({ messages, isLoading }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Scroll the container to bottom, not the entire viewport
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight
    }
  }, [messages, isLoading])

  return (
    <div className="message-list" ref={containerRef}>
      {messages.map((message, index) => (
        <Message key={index} message={message} />
      ))}

      {isLoading && (
        <div className="message assistant">
          <div className="message-avatar">AI</div>
          <div className="message-content">
            <div className="message-bubble">
              <div className="loading-indicator">
                <div className="loading-dot"></div>
                <div className="loading-dot"></div>
                <div className="loading-dot"></div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  )
}
