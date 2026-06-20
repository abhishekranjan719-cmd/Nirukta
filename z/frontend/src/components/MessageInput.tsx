import { useState, KeyboardEvent } from 'react'

interface MessageInputProps {
  onSendMessage: (message: string) => void
  disabled?: boolean
}

export default function MessageInput({
  onSendMessage,
  disabled = false,
}: MessageInputProps) {
  const [message, setMessage] = useState('')

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSendMessage(message.trim())
      setMessage('')
    }
  }

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="message-input-container">
      <div className="message-input-wrapper">
        <input
          type="text"
          className="message-input"
          placeholder="Type your message..."
          value={message}
          onChange={e => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={disabled}
        />
        <button
          className="send-button"
          onClick={handleSend}
          disabled={disabled || !message.trim()}
        >
          {disabled ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  )
}
