export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface Conversation {
  id: string;
  messages: Message[];
  title: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  orchestration_mode?: 'workflow' | 'agent';
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
  timestamp: string;
  orchestration_mode: string;
}
