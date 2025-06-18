/**
 * Custom hook for OpenAI streaming conversations
 * Provides real-time streaming of OpenAI responses
 */

import { useState, useCallback, useRef } from 'react';
import openAIStreaming, { OpenAIStreamingOptions } from '../openai-streaming';

interface UseOpenAIStreamingOptions {
  systemMessage?: string;
  model?: string;
  onStreamingStart?: () => void;
  onStreamingComplete?: (fullText: string) => void;
  onStreamingError?: (error: Error) => void;
}

export default function useOpenAIStreaming(options: UseOpenAIStreamingOptions = {}) {
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [streamedText, setStreamedText] = useState('');
  const abortControllerRef = useRef<AbortController | null>(null);

  const streamResponse = useCallback(async (prompt: string) => {
    if (!prompt) return '';
    
    setIsStreaming(true);
    setError(null);
    setStreamedText('');
    
    // Create abort controller for cancellation
    abortControllerRef.current = new AbortController();
    
    try {
      if (options.onStreamingStart) {
        options.onStreamingStart();
      }
      
      // Use the streaming service
      const fullText = await openAIStreaming.streamCompletion({
        prompt,
        systemMessage: options.systemMessage || 'You are a helpful AI assistant having a conversation. Respond in a natural, conversational way.',
        model: options.model || 'gpt-3.5-turbo',
        onToken: (token) => {
          setStreamedText(prev => prev + token);
        },
        onComplete: (fullText) => {
          if (options.onStreamingComplete) {
            options.onStreamingComplete(fullText);
          }
        },
        onError: (error) => {
          setError(error);
          if (options.onStreamingError) {
            options.onStreamingError(error);
          }
        }
      });
      
      return fullText;
    } catch (error) {
      console.error('Error in OpenAI streaming:', error);
      setError(error instanceof Error ? error : new Error(String(error)));
      if (options.onStreamingError) {
        options.onStreamingError(error instanceof Error ? error : new Error(String(error)));
      }
      return '';
    } finally {
      setIsStreaming(false);
      abortControllerRef.current = null;
    }
  }, [options]);
  
  const stopStreaming = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsStreaming(false);
    }
  }, []);
  
  return {
    isStreaming,
    error,
    streamedText,
    streamResponse,
    stopStreaming
  };
}
