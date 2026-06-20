import axios from 'axios';
import type { ChatRequest, ChatResponse } from '../types/chat';

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const sendMessage = async (request: ChatRequest): Promise<ChatResponse> => {
  const response = await apiClient.post<ChatResponse>('/api/chat', request);
  return response.data;
};

export const getConversation = async (conversationId: string) => {
  const response = await apiClient.get(`/api/conversations/${conversationId}`);
  return response.data;
};

export const listConversations = async () => {
  const response = await apiClient.get('/api/conversations');
  return response.data;
};

export const checkHealth = async () => {
  const response = await apiClient.get('/health');
  return response.data;
};

export default apiClient;
