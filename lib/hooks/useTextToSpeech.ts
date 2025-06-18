import { useState, useCallback } from 'react';
import elevenLabsService, { VOICE_IDS } from '@/lib/elevenlabs';
import { config } from '@/lib/config';

interface TextToSpeechOptions {
  voiceId?: string;
  model?: string;
  stability?: number;
  similarityBoost?: number;
  style?: number;
  speakerBoost?: boolean;
}

interface TextToSpeechState {
  isSpeaking: boolean;
  error: Error | null;
  speak: (text: string, options?: TextToSpeechOptions) => Promise<void>;
  stop: () => void;
}

/**
 * Hook for using Eleven Labs text-to-speech functionality
 */
const useTextToSpeech = (defaultOptions?: TextToSpeechOptions): TextToSpeechState => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  
  // Initialize with API key
  const initializeService = useCallback(() => {
    const apiKey = config.elevenlabs.apiKey;
    if (!apiKey) {
      throw new Error('Eleven Labs API key not found. Please set NEXT_PUBLIC_ELEVENLABS_API_KEY in your .env.local file.');
    }
    
    elevenLabsService.configure({
      apiKey,
      defaultVoiceId: config.elevenlabs.defaultVoiceId,
      defaultModel: config.elevenlabs.defaultModel
    });
  }, []);

  // Maintain a flag to avoid repeated Eleven Labs API calls when it fails
  const [elevenlabsFailed, setElevenlabsFailed] = useState(false);

  // Speak text with fallback
  const speak = useCallback(async (text: string, options?: TextToSpeechOptions) => {
    try {
      setError(null);
      setIsSpeaking(true);

      // Skip Eleven Labs if it previously failed in this session
      if (!elevenlabsFailed) {
        try {
          initializeService();
          
          await elevenLabsService.speak({
            text,
            voiceId: options?.voiceId || config.elevenlabs.defaultVoiceId,
            model: options?.model || config.elevenlabs.defaultModel,
            stability: options?.stability,
            similarityBoost: options?.similarityBoost,
            style: options?.style,
            speakerBoost: options?.speakerBoost
          });
          setIsSpeaking(false);
          return;
        } catch (elevenlabsErr) {
          console.error('Error with Eleven Labs TTS:', elevenlabsErr);
          // Mark Eleven Labs as failed for this session to avoid repeated API calls
          setElevenlabsFailed(true);
          // Continue to browser fallback
        }
      }
      
      // Fallback to browser speech synthesis
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1.1;
        utterance.volume = 0.8;
        
        utterance.onend = () => setIsSpeaking(false);
        utterance.onerror = (event) => {
          console.error('Speech synthesis error:', event);
          setError(new Error('Browser speech synthesis failed'));
          setIsSpeaking(false);
        };
        
        window.speechSynthesis.speak(utterance);
      } else {
        console.error('No speech synthesis available');
        setError(new Error('Speech synthesis not supported in this browser'));
        setIsSpeaking(false);
      }
    } catch (err) {
      console.error('Error in text-to-speech:', err);
      setError(err instanceof Error ? err : new Error('Unknown error in text-to-speech'));
      setIsSpeaking(false);
    }
  }, [elevenlabsFailed, initializeService]);

  // Stop speaking
  const stop = useCallback(() => {
    // Stop both native speech synthesis and Eleven Labs audio
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    
    // Stop Eleven Labs audio
    try {
      elevenLabsService.stopAudio();
    } catch (err) {
      console.error('Error stopping Eleven Labs audio:', err);
    }
    
    setIsSpeaking(false);
  }, []);

  return {
    isSpeaking,
    error,
    speak,
    stop
  };
};

export default useTextToSpeech;
