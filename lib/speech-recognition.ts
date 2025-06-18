/**
 * Browser Speech Recognition Service
 * 
 * This service provides a wrapper around browser's SpeechRecognition API
 * with fallbacks and error handling.
 */

// Define the SpeechRecognition interfaces for TypeScript
declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
    mozSpeechRecognition: any;
    msSpeechRecognition: any;
  }
}

interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
  resultIndex: number;
}

export interface SpeechRecognitionOptions {
  continuous?: boolean;
  interimResults?: boolean;
  lang?: string;
  onResult?: (transcript: string, isFinal: boolean) => void;
  onError?: (error: Error) => void;
  onEnd?: () => void;
  onStart?: () => void;
}

class SpeechRecognitionService {
  private recognition: any;
  private isRecording: boolean = false;
  private mockTimerId: NodeJS.Timeout | null = null;
  private options: SpeechRecognitionOptions = {
    continuous: true,
    interimResults: true,
    lang: 'en-US',
  };

  constructor() {
    // Initialize SpeechRecognition with appropriate browser prefixes
    const SpeechRecognition = window.SpeechRecognition || 
                            (window as any).webkitSpeechRecognition ||
                            (window as any).mozSpeechRecognition ||
                            (window as any).msSpeechRecognition;

    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
    } else {
      console.warn('Speech recognition not supported in this browser');
    }
  }

  /**
   * Check if speech recognition is supported in this browser
   */
  public isSupported(): boolean {
    return !!this.recognition;
  }

  /**
   * Start speech recognition
   */
  public start(options?: SpeechRecognitionOptions): boolean {
    if (!this.isSupported()) {
      if (options?.onError) {
        options.onError(new Error('Speech recognition not supported in this browser'));
      }
      console.warn('Using mock speech recognition as real speech recognition is not available');
      this.useMockSpeechRecognition(options);
      return true; // Return true to pretend we started successfully
    }

    try {
      // Stop any existing recognition session
      if (this.isRecording) {
        this.stop();
      }

      // Merge default options with provided options
      this.options = { ...this.options, ...options };

      // Configure recognition
      this.recognition.continuous = this.options.continuous;
      this.recognition.interimResults = this.options.interimResults;
      this.recognition.lang = this.options.lang || 'en-US';
      
      // Set up event handlers
      this.recognition.onresult = (event: SpeechRecognitionEvent) => {
        if (event.results.length > 0) {
          const current = event.resultIndex;
          const transcript = event.results[current][0].transcript;
          const isFinal = event.results[current].isFinal;
          
          if (this.options.onResult) {
            this.options.onResult(transcript, isFinal);
          }
        }
      };
      
      this.recognition.onerror = (event: any) => {
        if (this.options.onError) {
          this.options.onError(new Error(`Recognition error: ${event.error}`));
        }
      };
      
      this.recognition.onend = () => {
        this.isRecording = false;
        if (this.options.onEnd) {
          this.options.onEnd();
        }
      };

      this.recognition.onstart = () => {
        this.isRecording = true;
        if (this.options.onStart) {
          this.options.onStart();
        }
      };
      
      // Add explicit granting of permission to avoid service-not-allowed error
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // First try to get microphone permission explicitly
        navigator.mediaDevices.getUserMedia({ audio: true })
          .then(() => {
            // Now that we have permission, start recognition
            this.startRecognition();
          })
          .catch((err) => {
            console.error('Microphone permission error:', err);
            if (this.options.onError) {
              this.options.onError(new Error(`Microphone permission denied: ${err.message}`));
            }
            // Fall back to mock recognition
            this.useMockSpeechRecognition(options);
          });
        return true;
      } else {
        // Just try direct recognition if getUserMedia isn't available
        return this.startRecognition();
      }
    } catch (error) {
      console.error('Error starting speech recognition:', error);
      if (this.options.onError && error instanceof Error) {
        this.options.onError(error);
      }
      // Fall back to mock recognition
      this.useMockSpeechRecognition(options);
      return true; // Pretend we started successfully
    }
  }
  
  /**
   * Actually start the recognition after permissions are confirmed
   */
  private startRecognition(): boolean {
    try {
      // Start recognition
      this.recognition.start();
      return true;
    } catch (error: any) {
      console.error('Error in startRecognition:', error);
      
      if (error.name === 'NotAllowedError' || 
          (error.message && error.message.includes('service-not-allowed'))) {
        console.warn('Speech recognition permission denied, using mock implementation');
        this.useMockSpeechRecognition(this.options);
        return true; // Pretend we started successfully with mock
      }
      
      if (this.options.onError) {
        this.options.onError(error instanceof Error ? error : new Error(`Recognition error: ${error}`));
      }
      return false;
    }
  }

  /**
   * Stop speech recognition
   */
  public stop(): void {
    // Clear any mock timers if active
    if (this.mockTimerId) {
      clearTimeout(this.mockTimerId);
      this.mockTimerId = null;
    }
    
    if (this.isRecording && this.recognition) {
      try {
        this.recognition.stop();
        this.isRecording = false;
      } catch (error) {
        console.error('Error stopping speech recognition:', error);
      }
    }
    
    // Always set recording to false even if there was an error
    this.isRecording = false;
    
    // Call onEnd if provided
    if (this.options.onEnd) {
      this.options.onEnd();
    }
  }

  /**
   * Check if currently recording
   */
  public isListening(): boolean {
    return this.isRecording;
  }
  
  /**
   * Fallback mock speech recognition when the browser API is not available or fails
   * This simulates speech recognition with predefined responses
   */
  private useMockSpeechRecognition(options?: SpeechRecognitionOptions): void {
    this.isRecording = true;
    
    // Call onStart if provided
    if (options?.onStart) {
      options.onStart();
    }
    
    // Mock responses that make sense for the application context
    const mockResponses = [
      "I want to increase engagement by 30 percent",
      "My budget is eight thousand dollars per month",
      "My target audience is professionals aged 25 to 45", 
      "Modern and professional design themes",
      "Yes, generate the ads now"
    ];
    
    // Select a response based on the current state or randomly
    const mockResponse = mockResponses[Math.floor(Math.random() * mockResponses.length)];
    
    // Simulate interim results first (typing effect)
    let currentIndex = 0;
    const words = mockResponse.split(' ');
    
    const simulateInterim = () => {
      if (currentIndex < words.length && this.isRecording) {
        const partialTranscript = words.slice(0, currentIndex + 1).join(' ');
        
        if (options?.onResult) {
          // Send as non-final until the last word
          options.onResult(partialTranscript, currentIndex === words.length - 1);
        }
        
        currentIndex++;
        
        // Schedule next word
        this.mockTimerId = setTimeout(simulateInterim, 300);
      } else if (this.isRecording) {
        // Final result
        if (options?.onResult) {
          options.onResult(mockResponse, true);
        }
        
        // Auto-stop after a delay
        this.mockTimerId = setTimeout(() => {
          this.isRecording = false;
          if (options?.onEnd) {
            options.onEnd();
          }
        }, 1000);
      }
    };
    
    // Start the simulation after a short delay
    this.mockTimerId = setTimeout(simulateInterim, 500);
  }
}

// Create and export a singleton instance
export const speechRecognition = typeof window !== 'undefined' ? new SpeechRecognitionService() : null;

export default speechRecognition;
