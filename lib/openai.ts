/**
 * OpenAI text-to-speech service
 * Uses OpenAI's TTS API to convert text to speech
 */

export enum OpenAIVoiceIds {
  ALLOY = 'alloy',
  ECHO = 'echo',
  FABLE = 'fable',
  ONYX = 'onyx',
  NOVA = 'nova',
  SHIMMER = 'shimmer',
}

export interface OpenAITTSOptions {
  text: string;
  voice?: string;
  model?: string;
  responseFormat?: 'mp3' | 'opus' | 'aac' | 'flac';
  speed?: number;
}

class OpenAIService {
  private apiKey: string | undefined;
  private currentAudio: HTMLAudioElement | null = null;
  // Track both audio sources for complete cleanup
  private _audioContext: AudioContext | null = null;
  private _audioSource: AudioBufferSourceNode | null = null;
  
  constructor() {
    this.apiKey = process.env.NEXT_PUBLIC_OPENAI_API_KEY;
  }
  
  /**
   * Check if the OpenAI API key is configured
   */
  isAvailable(): boolean {
    return !!this.apiKey && this.apiKey.length > 0;
  }
  
  /**
   * Convert text to speech using OpenAI's TTS API
   */
  async textToSpeech(options: OpenAITTSOptions): Promise<ArrayBuffer> {
    try {
      if (!this.isAvailable()) {
        throw new Error('OpenAI API key is not configured');
      }
      
      // Format text for dialogue if needed
      const text = options.text;
      
      // Call the OpenAI TTS API
      const response = await fetch('https://api.openai.com/v1/audio/speech', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({
          model: options.model || 'tts-1',
          voice: options.voice || OpenAIVoiceIds.NOVA,
          input: text,
          response_format: options.responseFormat || 'mp3',
          speed: options.speed || 1.0
        })
      });
      
      if (!response.ok) {
        throw new Error(`OpenAI API error: ${response.status} ${response.statusText}`);
      }
      
      return await response.arrayBuffer();
    } catch (error) {
      console.error('Error in OpenAI text-to-speech:', error);
      throw new Error(`OpenAI API error: ${error instanceof Error ? error.message : String(error)}`);
    }
  }
  
  /**
   * Format text for sales call/interview style using two different voices
   */
  formatForSalesCall(text: string): string {
    // OpenAI doesn't need special formatting like Dia
    // We'll handle this by using different voices in the hook
    return text;
  }
  
  // Audio context and source are already declared at the class level
  
  /**
   * Play audio from ArrayBuffer
   */
  playAudio(audioBuffer: ArrayBuffer): Promise<void> {
    return new Promise((resolve) => {
      // Stop any currently playing audio first
      this.stopAudio();
      
      // Create a new audio context and assign to class member
      this._audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      
      // Use the class member for decoding
      this._audioContext.decodeAudioData(audioBuffer, (decodedBuffer: AudioBuffer) => {
        if (!this._audioContext) return; // Context might have been cleaned up
        
        // Create and configure audio source using the class member context
        this._audioSource = this._audioContext.createBufferSource();
        this._audioSource.buffer = decodedBuffer;
        this._audioSource.connect(this._audioContext.destination);
        
        // Set up completion handler
        this._audioSource.onended = () => {
          this.stopAudio(); // Ensure cleanup after audio finishes
          resolve();
        };
        
        // Start playback
        this._audioSource.start(0);
      });
    });
  }
  
  /**
   * Stop any currently playing audio and clean up all resources
   */
  stopAudio(): void {
    // Stop and clean up Web Audio API resources
    if (this._audioSource) {
      try {
        this._audioSource.stop();
      } catch (e) {
        // Source might already be stopped or not started
      }
      this._audioSource.disconnect();
      this._audioSource = null;
    }
    
    // Clean up audio context
    if (this._audioContext) {
      try {
        if (this._audioContext.state !== 'closed') {
          this._audioContext.close();
        }
      } catch (e) {
        // Context might already be closed
      }
      this._audioContext = null;
    }
    
    // Clean up HTML Audio element (legacy cleanup)
    if (this.currentAudio) {
      this.currentAudio.pause();
      this.currentAudio.src = ''; // Free up memory
      try {
        if (this.currentAudio.src && this.currentAudio.src.startsWith('blob:')) {
          URL.revokeObjectURL(this.currentAudio.src);
        }
      } catch(e) {
        // Error revoking object URL
      }
      this.currentAudio = null;
    }
  }
}

// Singleton instance
const openAIService = new OpenAIService();
export default openAIService;
