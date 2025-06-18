/**
 * Whisper Transcription Service
 * 
 * Uses OpenAI's Whisper API to convert speech to text
 */

import openAIService from './openai';

interface WhisperTranscriptionOptions {
  audioBlob: Blob;
  onTranscriptionStart?: () => void;
  onTranscriptionComplete?: (transcript: string) => void;
  onTranscriptionError?: (error: Error) => void;
}

class WhisperTranscriptionService {
  // No longer need to store API key here as it's handled server-side
  
  constructor() {}
  
  /**
   * Check if the service is available (always true now, relies on server config)
   */
  isAvailable(): boolean {
    return true; 
  }
  
  /**
   * Transcribe audio using the internal /api/transcribe route
   */
  async transcribeAudio(options: WhisperTranscriptionOptions): Promise<string> {
    try {
      if (options.onTranscriptionStart) {
        options.onTranscriptionStart();
      }
      
      // Create form data for the API request to our backend
      const formData = new FormData();
      formData.append('file', options.audioBlob, 'recording.webm');
      // No need to append model, language, etc. here as the API route handles it
      
      // Call our internal API route
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 20000); // 20 second timeout for internal API
      
      let response;
      try {
        response = await fetch('/api/transcribe', {
          method: 'POST',
          body: formData,
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({ error: 'Failed to parse error response from /api/transcribe' }));
          const serverErrorMessage = errorData.error || `API route error: ${response.status} ${response.statusText}`;
          const detailedError = errorData.details ? JSON.stringify(errorData.details) : '';
          throw new Error(`Transcription failed: ${serverErrorMessage} ${detailedError}`);
        }
        
        const data = await response.json();
        if (data.error) {
          throw new Error(`Transcription error from server: ${data.error}`);
        }
        const transcript = data.transcript;
        
        if (options.onTranscriptionComplete) {
          options.onTranscriptionComplete(transcript);
        }
        
        return transcript;

      } catch (error: unknown) {
        clearTimeout(timeoutId);
        if (error instanceof Error && error.name === 'AbortError') {
          throw new Error('Request to /api/transcribe timed out. Please check your connection and server status.');
        }
        // Re-throw other fetch-related or parsing errors
        throw error;
      }
    } catch (error) {
      console.error('Error in WhisperTranscriptionService (client-side):', error);
      if (options.onTranscriptionError) {
        options.onTranscriptionError(error instanceof Error ? error : new Error(String(error)));
      }
      throw error;
    }
  }
}

// Create and export a singleton instance
const whisperTranscription = new WhisperTranscriptionService();
export default whisperTranscription;
