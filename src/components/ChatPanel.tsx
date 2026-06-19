// ChatPanel.tsx

import React, { useEffect, useRef, useState } from "react";
import starImg from "../assets/img/stars-01.svg";
import plusIcon from "../assets/img/chat-button-plus.png";
import enterImg from "../assets/img/enter-img.png";
import micImg from "../assets/img/chat-mic-button.png";
import { useNavigate } from "react-router-dom";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface Props {
  onClose: () => void;
  chatInput: string;
  setChatInput: (value: string) => void;
}

const ChatPanel: React.FC<Props> = ({
  onClose,
  chatInput,
  setChatInput,
}) => {
  const navigate = useNavigate();
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const [messages, setMessages] = useState<Message[]>([]);
  const [thinkingStep, setThinkingStep] = useState<string | null>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSend = async () => {
    if (!chatInput.trim()) return;

    const userMessage = chatInput;

    setMessages((prev) => [
      ...prev,
      { role: "user", content: userMessage },
    ]);

    setChatInput("");


    setThinkingStep("Thinking...");
    await delay(2000);


    setThinkingStep(null);

    navigate("/chat-experience", {
      state: { query: userMessage },
    });
  };

  const delay = (ms: number) =>
    new Promise((res) => setTimeout(res, ms));

  return (
    <div className="chat-panel open">
      <div className="chat-header">
        <h3 className="chat-title">Chat</h3>
        <button className="chat-close" onClick={onClose}>
          ✕
        </button>
      </div>

      <div className="chat-content">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.role}`}>
            <p>{msg.content}</p>
          </div>
        ))}

        {thinkingStep && (
          <div className="chat-message assistant thinking">
            <div className="thinking-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <p>{thinkingStep}</p>
          </div>
        )}
      </div>

      
      <div className="chat-input-area">
        <textarea
          ref={inputRef}
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          placeholder="Ask me anything..."
          className="chat-input"
          rows={1}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />

        <span className="chat-input-icons">
          <span className="left-align">
            <img src={plusIcon} alt="plus" className="icons" />
          </span>

          <span className="right-align">
            <img
              src={starImg}
              alt="star"
              className="icons"
              onClick={() => navigate("/prompt-gallery")}/>
            <img
              src={micImg}
              alt="mic"
              className="icons"
            />
            <img
              src={enterImg}
              alt="send"
              className="icons"
              onClick={handleSend}
            />
          </span>
        </span>
      </div>
    </div>
  );
};

export default ChatPanel;




