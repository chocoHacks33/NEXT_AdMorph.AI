// Using native fetch API instead of axios

export interface DiaTextToSpeechOptions {
  text: string;
  useTorchCompile?: boolean;
  seed?: number;
}

export class DiaService {
  private static instance: DiaService;
  private audioContext?: AudioContext;
  private activeSource?: AudioBufferSourceNode;

  // If you're running the Dia model locally via the Python server
  private apiUrl: string = process.env.NEXT_PUBLIC_DIA_API_URL || 'http://localhost:7860/api';

  /**
   * Get singleton instance
   */
  static getInstance(): DiaService {
    if (!DiaService.instance) {
      DiaService.instance = new DiaService();
    }
    return DiaService.instance;
  }

  /**
   * Convert text to interview/sales call style speech
   * Alternates between [S1] and [S2] speakers for natural dialogue
   */
  async textToSpeech(options: DiaTextToSpeechOptions): Promise<ArrayBuffer> {
    try {
      // Format the text for a sales call/interview style
      const formattedText = this.formatForSalesCall(options.text);

      // Call the Dia API - if running locally via their Gradio app
      const response = await fetch(`${this.apiUrl}/run/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          data: [
            formattedText,
            options.seed || Math.floor(Math.random() * 1000000), // Random seed if not provided
            options.useTorchCompile !== false, // Default to true
            null, // No audio prompt by default
            null, // No transcript by default
          ]
        })
      });

      if (!response.ok) {
        throw new Error(`Dia API error: ${response.status} ${response.statusText}`);
      }

      return await response.arrayBuffer();
    } catch (error) {
      console.error('Error in Dia text-to-speech:', error);
      throw new Error(`Dia API error: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Format regular text for Dia's sales call style using [S1] and [S2] tags
   */
  private formatForSalesCall(text: string): string {
    // If the text already contains [S1] or [S2] tags, assume it's already formatted
    if (text.includes('[S1]') || text.includes('[S2]')) {
      return text;
    }

    // Otherwise, format it as a sales rep [S1] talking to a potential customer [S2]
    return `[S1] ${text}`;
  }

  /**
   * Stop any currently playing audio
   */
  stopAudio(): void {
    if (this.activeSource) {
      try {
        this.activeSource.stop();
        this.activeSource.disconnect();
        this.activeSource = undefined;
      } catch (e) {
        console.error('Error stopping audio:', e);
      }
    }

    if (this.audioContext && this.audioContext.state !== 'closed') {
      try {
        this.audioContext.close();
        this.audioContext = undefined;
      } catch (e) {
        console.error('Error closing audio context:', e);
      }
    }
  }

  /**
   * Play audio from ArrayBuffer
   */
  async playAudio(audioBuffer: ArrayBuffer): Promise<void> {
    // Stop any currently playing audio first
    this.stopAudio();

    return new Promise((resolve) => {
      // Create new audio context
      this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      
      this.audioContext.decodeAudioData(audioBuffer, (buffer) => {
        this.activeSource = this.audioContext!.createBufferSource();
        this.activeSource.buffer = buffer;
        this.activeSource.connect(this.audioContext!.destination);
        this.activeSource.start(0);

        this.activeSource.onended = () => {
          resolve();
        };
      });
    });
  }

  /**
   * Generate and play speech
   */
  async speak(options: DiaTextToSpeechOptions): Promise<void> {
    this.stopAudio(); // Stop any currently playing audio

    try {
      const audio = await this.textToSpeech(options);
      await this.playAudio(audio);
    } catch (e) {
      console.error('Error speaking with Dia:', e);
      throw e;
    }
  }
}

export default DiaService.getInstance();
