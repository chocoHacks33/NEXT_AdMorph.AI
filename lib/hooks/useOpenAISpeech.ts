import { useState, useCallback, useEffect } from 'react';
import openAIService, { OpenAIVoiceIds } from '../openai';

export interface OpenAISpeechOptions {
  salesCallStyle?: boolean;
  defaultVoice?: string;
  alternateVoice?: string;
  speed?: number;
}

export interface OpenAISpeechState {
  speak: (options: { text: string }) => Promise<void>;
  stop: () => void;
  isSpeaking: boolean;
  error: Error | null;
}

/**
 * Hook for using OpenAI text-to-speech with dialogue support
 * Can alternate between two voices for interview/sales call style
 */
const useOpenAISpeech = (options: OpenAISpeechOptions = {}): OpenAISpeechState => {
  // Flag to track if a speech sequence should be aborted
  const [shouldAbort, setShouldAbort] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  
  // Default to sales call style if not specified
  const salesCallStyle = options.salesCallStyle ?? true;
  
  // Default and alternate voices for dialogue
  const defaultVoice = options.defaultVoice || OpenAIVoiceIds.NOVA; // Female voice
  const alternateVoice = options.alternateVoice || OpenAIVoiceIds.ONYX; // Male voice
  
  // Speed setting (1.0 is normal)
  const speed = options.speed || 1.0;
  
  // Clean up on unmount
  useEffect(() => {
    return () => {
      openAIService.stopAudio();
    };
  }, []);
  
  // Convert text to speech with dialogue support (alternating voices)
  const speak = useCallback(async ({ text }: { text: string }): Promise<void> => {
    try {
      setError(null);
      
      // Always stop any existing audio first
      openAIService.stopAudio();
      
      // Reset abort flag and set speaking state
      setShouldAbort(false);
      setIsSpeaking(true);
      
      if (salesCallStyle) {
        // Pre-process the text to combine adjacent segments from the same speaker
        const rawParts = text.split(/(\[S1\]|\[S2\])/g).filter(part => part.trim().length > 0);
        const processedParts: { speaker: string; text: string }[] = [];
        let currentSpeaker = '[S1]';
        let currentText = '';
        
        for (let i = 0; i < rawParts.length; i++) {
          const part = rawParts[i];
          
          if (part === '[S1]' || part === '[S2]') {
            if (currentText.trim().length > 0) {
              processedParts.push({ speaker: currentSpeaker, text: currentText.trim() });
              currentText = '';
            }
            currentSpeaker = part;
          } else {
            currentText += (currentText.length > 0 ? ' ' : '') + part.trim();
          }
        }
        
        if (currentText.trim().length > 0) {
          processedParts.push({ speaker: currentSpeaker, text: currentText.trim() });
        }
        
        // Process each part sequentially, checking for abort between each segment
        for (let i = 0; i < processedParts.length; i++) {
          if (shouldAbort) break; // Check if we should abort (user called stop)
          
          const segment = processedParts[i];
          const voice = segment.speaker === '[S1]' ? defaultVoice : alternateVoice;
          
          const audioBuffer = await openAIService.textToSpeech({
            text: segment.text,
            voice,
            speed
          });
          
          if (shouldAbort) break; // Again check if we should abort before playing
          
          await openAIService.playAudio(audioBuffer);
        }
      } else {
        // Non-dialogue style, just use the default voice
        const audioBuffer = await openAIService.textToSpeech({
          text,
          voice: defaultVoice,
          speed
        });
        
        await openAIService.playAudio(audioBuffer);
      }
      
      setIsSpeaking(false);
    } catch (err) {
      console.error("OpenAI speech error:", err);
      setIsSpeaking(false);
      setError(err instanceof Error ? err : new Error('Unknown OpenAI speech error'));
      
      // Fallback to browser speech synthesis
      if ("speechSynthesis" in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = speed;
        window.speechSynthesis.cancel(); // Cancel any ongoing speech
        window.speechSynthesis.speak(utterance);
      }
    }
  }, [isSpeaking, salesCallStyle, defaultVoice, alternateVoice, speed]);
  
  // Stop any currently playing speech
  const stop = useCallback(() => {
    setShouldAbort(true); // Signal the speak loop to abort
    openAIService.stopAudio();
    
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel(); // Also cancel browser fallback
    }
    
    setIsSpeaking(false);
  }, []);
  
  return {
    speak,
    stop,
    isSpeaking,
    error
  };
};

export default useOpenAISpeech;
