/**
 * Eleven Labs API Client
 * 
 * This service handles interactions with the Eleven Labs API for text-to-speech functionality.
 */

// Voice IDs can be found in your Eleven Labs dashboard
// https://elevenlabs.io/app/voices
export const VOICE_IDS = {
  RACHEL: "21m00Tcm4TlvDq8ikWAM", // Female, conversational
  JOSH: "TxGEqnHWrfWFTfGW9XjX",   // Male, professional
  ADAM: "pNInz6obpgDQGcFmaJgB",   // Male, deep
  DOMI: "AZnzlk1XvdvUeBnXmlld",   // Female, casual
  BELLA: "EXAVITQu4vr4xnSDxMaL", // Female, young
  ANTONI: "ErXwobaYiN019PkySvjV", // Male, well-rounded
  ELLI: "MF3mGyEYCl7XYWbV9V6O",  // Female, emotional
  ARNOLD: "VR6AewLTigWG4xSOukaG", // Arnold
  YANNICK: "VR6AewLTigWG4xSOukaG", // Yannick
}

export type ElevenLabsVoiceId = keyof typeof VOICE_IDS;

interface TextToSpeechOptions {
  text: string;
  voiceId?: string;
  model?: string;
  apiKey?: string;
  stability?: number;
  similarityBoost?: number;
  style?: number;
  speakerBoost?: boolean;
}

export interface ElevenLabsConfig {
  apiKey: string;
  defaultVoiceId: string;
  defaultModel: string;
}

class ElevenLabsService {
  private audioContext: AudioContext | null = null;
  private activeSource: AudioBufferSourceNode | null = null;
  private apiKey: string;
  private defaultVoiceId: string;
  private defaultModel: string;
  private baseUrl = 'https://api.elevenlabs.io/v1';

  constructor(config?: Partial<ElevenLabsConfig>) {
    // These defaults will be overridden by environment variables or passed config
    this.apiKey = '';
    this.defaultVoiceId = VOICE_IDS.RACHEL;
    this.defaultModel = 'eleven_turbo_v2';
    
    if (config) {
      if (config.apiKey) this.apiKey = config.apiKey;
      if (config.defaultVoiceId) this.defaultVoiceId = config.defaultVoiceId;
      if (config.defaultModel) this.defaultModel = config.defaultModel;
    }
  }
  
  configure(config: Partial<ElevenLabsConfig>) {
    if (config.apiKey) this.apiKey = config.apiKey;
    if (config.defaultVoiceId) this.defaultVoiceId = config.defaultVoiceId;
    if (config.defaultModel) this.defaultModel = config.defaultModel;
  }

  /**
   * Convert text to speech using Eleven Labs API
   */
  async textToSpeech({
    text,
    voiceId = this.defaultVoiceId,
    model = this.defaultModel,
    apiKey = this.apiKey,
    stability = 0.5,
    similarityBoost = 0.75,
    style = 0,
    speakerBoost = true,
  }: TextToSpeechOptions): Promise<ArrayBuffer> {
    const url = `${this.baseUrl}/text-to-speech/${voiceId}`;

    // Check if API key is set
    if (!apiKey) {
      throw new Error('Eleven Labs API key is not set. Please configure the API key before using this service.');
    }

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'xi-api-key': apiKey,
      },
      body: JSON.stringify({
        text,
        model_id: model,
        voice_settings: {
          stability,
          similarity_boost: similarityBoost,
          style,
          use_speaker_boost: speakerBoost,
        },
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Eleven Labs API error: ${response.status} - ${errorText}`);
    }

    return await response.arrayBuffer();
  }

  /**
   * Play audio from ArrayBuffer
   */
  playAudio(audioBuffer: ArrayBuffer): Promise<void> {
    return new Promise((resolve) => {
      // Stop any currently playing audio
      this.stopAudio();
      
      // Create a new audio context if needed
      if (!this.audioContext) {
        this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      }
      
      this.audioContext.decodeAudioData(audioBuffer, (buffer) => {
        // Make sure we're not trying to play audio if the previous stop hasn't completed
        if (this.activeSource) {
          this.stopAudio();
        }
        
        const source = this.audioContext!.createBufferSource();
        this.activeSource = source;
        source.buffer = buffer;
        source.connect(this.audioContext!.destination);
        
        source.onended = () => {
          if (this.activeSource === source) {
            this.activeSource = null;
          }
          resolve();
        };
        
        source.start(0);
      });
    });
  }

  /**
   * Stop currently playing audio
   */
  stopAudio(): void {
    if (this.activeSource) {
      try {
        this.activeSource.onended = null;
        this.activeSource.stop();
        this.activeSource.disconnect();
      } catch (e) {
        // Ignore errors during cleanup
      }
      this.activeSource = null;
    }
  }

  /**
   * Send text-to-speech request to Eleven Labs API
   */
  async speak(params: TextToSpeechOptions): Promise<void> {
    this.stopAudio(); // Stop any currently playing audio

    try {
      // Check if API key exists before making the call
      if (!this.apiKey || this.apiKey.trim() === '') {
        throw new Error('Eleven Labs API key is missing or invalid');
      }
      
      const audio = await this.textToSpeech(params);
      await this.playAudio(audio);
    } catch (e) {
      console.error('Error speaking text:', e);
      throw e;
    }
  }

  /**
   * Get available voices from Eleven Labs
   */
  async getVoices() {
    const url = `${this.baseUrl}/voices`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'xi-api-key': this.apiKey,
      },
    });

    if (!response.ok) {
      throw new Error(`Eleven Labs API error: ${response.status}`);
    }

    return await response.json();
  }
}

// Create singleton instance
export const elevenLabsService = new ElevenLabsService();

export default elevenLabsService;
