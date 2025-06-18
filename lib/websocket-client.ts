/**
 * WebSocket client for real-time communication with AdMorph.AI backend
 */

import React from 'react';

export interface WebSocketMessage {
  type: string;
  data?: any;
  timestamp?: string;
}

export interface GenerationUpdate {
  job_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress?: number;
  result?: any;
}

export interface PersonalizationUpdate {
  job_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress?: number;
  result?: any;
}

export interface PerformanceMetrics {
  campaign_id?: string;
  impressions: number;
  clicks: number;
  ctr: number;
  conversions: number;
  spend: number;
  revenue?: number;
  roi?: number;
}

export interface AnalyticsData {
  active_campaigns: number;
  total_impressions: number;
  total_clicks: number;
  total_conversions: number;
  total_spend: number;
  roi: number;
}

export type WebSocketEventHandler = (data: any) => void;

class WebSocketClient {
  private connections: Map<string, WebSocket> = new Map();
  private eventHandlers: Map<string, Set<WebSocketEventHandler>> = new Map();
  private reconnectAttempts: Map<string, number> = new Map();
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  /**
   * Connect to a WebSocket endpoint
   */
  connect(endpoint: string, sessionId?: string): Promise<WebSocket> {
    return new Promise((resolve, reject) => {
      const wsUrl = this.buildWebSocketUrl(endpoint, sessionId);
      const connectionKey = sessionId ? `${endpoint}:${sessionId}` : endpoint;

      // Close existing connection if any
      if (this.connections.has(connectionKey)) {
        this.disconnect(connectionKey);
      }

      try {
        const ws = new WebSocket(wsUrl);

        ws.onopen = () => {
          console.log(`✅ WebSocket connected: ${endpoint}`);
          this.connections.set(connectionKey, ws);
          this.reconnectAttempts.set(connectionKey, 0);
          resolve(ws);
        };

        ws.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data);
            this.handleMessage(endpoint, message);
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        ws.onclose = (event) => {
          console.log(`🔌 WebSocket disconnected: ${endpoint}`, event.code);
          this.connections.delete(connectionKey);
          
          // Attempt reconnection if not intentional
          if (event.code !== 1000) {
            this.attemptReconnection(endpoint, sessionId);
          }
        };

        ws.onerror = (error) => {
          console.error(`❌ WebSocket error: ${endpoint}`, error);
          reject(error);
        };

      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Disconnect from a WebSocket endpoint
   */
  disconnect(connectionKey: string) {
    const ws = this.connections.get(connectionKey);
    if (ws) {
      ws.close(1000, 'Intentional disconnect');
      this.connections.delete(connectionKey);
    }
  }

  /**
   * Send message to WebSocket
   */
  send(endpoint: string, message: any, sessionId?: string) {
    const connectionKey = sessionId ? `${endpoint}:${sessionId}` : endpoint;
    const ws = this.connections.get(connectionKey);
    
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message));
    } else {
      console.warn(`WebSocket not connected: ${endpoint}`);
    }
  }

  /**
   * Subscribe to WebSocket events
   */
  on(eventType: string, handler: WebSocketEventHandler) {
    if (!this.eventHandlers.has(eventType)) {
      this.eventHandlers.set(eventType, new Set());
    }
    this.eventHandlers.get(eventType)!.add(handler);
  }

  /**
   * Unsubscribe from WebSocket events
   */
  off(eventType: string, handler: WebSocketEventHandler) {
    const handlers = this.eventHandlers.get(eventType);
    if (handlers) {
      handlers.delete(handler);
    }
  }

  /**
   * Connect to generation updates
   */
  async connectToGeneration(): Promise<WebSocket> {
    return this.connect('generation');
  }

  /**
   * Connect to performance metrics
   */
  async connectToPerformance(): Promise<WebSocket> {
    return this.connect('performance');
  }

  /**
   * Connect to personalization updates
   */
  async connectToPersonalization(): Promise<WebSocket> {
    return this.connect('personalization');
  }

  /**
   * Connect to A/B testing updates
   */
  async connectToABTesting(): Promise<WebSocket> {
    return this.connect('ab-testing');
  }

  /**
   * Connect to analytics updates
   */
  async connectToAnalytics(): Promise<WebSocket> {
    return this.connect('analytics');
  }

  /**
   * Connect to chat session
   */
  async connectToChat(sessionId: string): Promise<WebSocket> {
    return this.connect('chat', sessionId);
  }

  /**
   * Connect to voice processing
   */
  async connectToVoice(sessionId: string): Promise<WebSocket> {
    return this.connect('voice', sessionId);
  }

  /**
   * Send chat message
   */
  sendChatMessage(sessionId: string, message: string) {
    this.send('chat', { message }, sessionId);
  }

  /**
   * Send voice data
   */
  sendVoiceData(sessionId: string, audioData: string) {
    this.send('voice', { audio_data: audioData }, sessionId);
  }

  /**
   * Disconnect all connections
   */
  disconnectAll() {
    for (const [key, ws] of this.connections) {
      ws.close(1000, 'Cleanup');
    }
    this.connections.clear();
    this.eventHandlers.clear();
    this.reconnectAttempts.clear();
  }

  private buildWebSocketUrl(endpoint: string, sessionId?: string): string {
    const baseUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws';
    const url = sessionId ? `${baseUrl}/${endpoint}/${sessionId}` : `${baseUrl}/${endpoint}`;
    return url;
  }

  private handleMessage(endpoint: string, message: WebSocketMessage) {
    // Emit to specific event handlers
    const handlers = this.eventHandlers.get(message.type);
    if (handlers) {
      handlers.forEach(handler => handler(message.data || message));
    }

    // Emit to general endpoint handlers
    const endpointHandlers = this.eventHandlers.get(endpoint);
    if (endpointHandlers) {
      endpointHandlers.forEach(handler => handler(message));
    }
  }

  private async attemptReconnection(endpoint: string, sessionId?: string) {
    const connectionKey = sessionId ? `${endpoint}:${sessionId}` : endpoint;
    const attempts = this.reconnectAttempts.get(connectionKey) || 0;

    if (attempts < this.maxReconnectAttempts) {
      this.reconnectAttempts.set(connectionKey, attempts + 1);
      
      console.log(`🔄 Attempting to reconnect to ${endpoint} (attempt ${attempts + 1})`);
      
      setTimeout(async () => {
        try {
          await this.connect(endpoint, sessionId);
        } catch (error) {
          console.error(`Failed to reconnect to ${endpoint}:`, error);
        }
      }, this.reconnectDelay * Math.pow(2, attempts)); // Exponential backoff
    } else {
      console.error(`❌ Max reconnection attempts reached for ${endpoint}`);
    }
  }
}

// Global WebSocket client instance
export const wsClient = new WebSocketClient();

// React hook for WebSocket connections
export function useWebSocket(endpoint: string, sessionId?: string) {
  const [isConnected, setIsConnected] = React.useState(false);
  const [lastMessage, setLastMessage] = React.useState<WebSocketMessage | null>(null);

  React.useEffect(() => {
    let ws: WebSocket;

    const connect = async () => {
      try {
        ws = await wsClient.connect(endpoint, sessionId);
        setIsConnected(true);

        // Listen for messages
        const handleMessage = (message: WebSocketMessage) => {
          setLastMessage(message);
        };

        wsClient.on(endpoint, handleMessage);

        return () => {
          wsClient.off(endpoint, handleMessage);
        };
      } catch (error) {
        console.error(`Failed to connect to ${endpoint}:`, error);
        setIsConnected(false);
      }
    };

    connect();

    return () => {
      if (ws) {
        const connectionKey = sessionId ? `${endpoint}:${sessionId}` : endpoint;
        wsClient.disconnect(connectionKey);
        setIsConnected(false);
      }
    };
  }, [endpoint, sessionId]);

  const sendMessage = (message: any) => {
    wsClient.send(endpoint, message, sessionId);
  };

  return {
    isConnected,
    lastMessage,
    sendMessage
  };
}

// Specialized hooks for different WebSocket endpoints
export function useGenerationUpdates() {
  return useWebSocket('generation');
}

export function usePerformanceMetrics() {
  return useWebSocket('performance');
}

export function usePersonalizationUpdates() {
  return useWebSocket('personalization');
}

export function useAnalytics() {
  return useWebSocket('analytics');
}

export function useChat(sessionId: string) {
  return useWebSocket('chat', sessionId);
}

export function useVoiceProcessing(sessionId: string) {
  return useWebSocket('voice', sessionId);
}
