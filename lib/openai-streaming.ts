/**
 * OpenAI Streaming Client
 * Handles streaming responses from OpenAI for a more natural conversation flow
 */

export interface OpenAIStreamingConfig {
  apiKey?: string;
  model?: string;
}

export interface OpenAIStreamingOptions {
  prompt: string;
  systemMessage?: string;
  onToken?: (token: string) => void;
  onComplete?: (fullText: string) => void;
  onError?: (error: Error) => void;
  model?: string;
}

export class OpenAIStreamingService {
  private apiKey: string;
  private defaultModel: string;

  constructor(config: OpenAIStreamingConfig = {}) {
    this.apiKey = config.apiKey || process.env.NEXT_PUBLIC_OPENAI_API_KEY || '';
    this.defaultModel = config.model || 'gpt-3.5-turbo';
  }

  isAvailable(): boolean {
    return !!this.apiKey && this.apiKey.length > 0;
  }

  async streamCompletion(options: OpenAIStreamingOptions): Promise<string> {
    if (!this.isAvailable()) {
      throw new Error('OpenAI API key is not configured');
    }

    let fullText = '';

    try {
      const messages = [
        ...(options.systemMessage 
          ? [{ role: 'system', content: options.systemMessage }] 
          : []),
        { role: 'user', content: options.prompt }
      ];

      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({
          model: options.model || this.defaultModel,
          messages,
          stream: true
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`OpenAI API error: ${response.status} ${JSON.stringify(errorData)}`);
      }

      // Process the streaming response
      const reader = response.body?.getReader();
      const decoder = new TextDecoder('utf-8');
      
      if (!reader) {
        throw new Error('Failed to create stream reader');
      }

      // Read the stream
      let done = false;
      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        
        if (done) break;
        
        // Decode and process the chunk
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk
          .split('\n')
          .filter(line => line.trim() !== '' && line.trim() !== 'data: [DONE]');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const jsonStr = line.slice(6); // Remove 'data: '
              if (jsonStr === '[DONE]') continue;
              
              const json = JSON.parse(jsonStr);
              const content = json.choices[0]?.delta?.content || '';
              
              if (content) {
                fullText += content;
                if (options.onToken) {
                  options.onToken(content);
                }
              }
            } catch (err) {
              console.warn('Error parsing SSE line:', err);
            }
          }
        }
      }

      if (options.onComplete) {
        options.onComplete(fullText);
      }
      
      return fullText;
    } catch (error) {
      console.error('Error in OpenAI streaming:', error);
      if (options.onError) {
        options.onError(error instanceof Error ? error : new Error(String(error)));
      }
      throw error;
    }
  }
}

// Create and export a singleton instance
const openAIStreaming = new OpenAIStreamingService();
export default openAIStreaming;
