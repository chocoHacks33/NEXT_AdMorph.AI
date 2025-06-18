import { useState, useCallback } from 'react';
import diaService, { DiaTextToSpeechOptions } from '../dia';

interface UseDialogueSpeechOptions {
  salesCallStyle?: boolean; // Whether to format speech as a sales call dialogue
}

interface DialogueSpeechOptions {
  text: string;
  seed?: number;
}

export function useDialogueSpeech(options: UseDialogueSpeechOptions = {}) {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  // Format text for sales call style if enabled
  const formatSalesText = (text: string): string => {
    if (!options.salesCallStyle || text.includes('[S1]') || text.includes('[S2]')) {
      return text;
    }
    
    // For a sales conversation, format as alternating dialogue
    // Split on sentences to alternate speakers
    const sentences = text.split(/(?<=[.!?])\s+/);
    
    let formattedText = '';
    sentences.forEach((sentence, index) => {
      // Sales rep speaks first, then customer
      const speakerTag = index % 2 === 0 ? '[S1]' : '[S2]';
      formattedText += `${speakerTag} ${sentence} `;
    });
    
    return formattedText.trim();
  };

  // Speak text using Dia
  const speak = useCallback(async (options: DialogueSpeechOptions) => {
    try {
      setError(null);
      setIsSpeaking(true);

      const text = formatSalesText(options.text);
      
      await diaService.speak({
        text,
        seed: options.seed,
        useTorchCompile: true
      });
      
      setIsSpeaking(false);
    } catch (err) {
      console.error('Error in dialogue speech:', err);
      setError(err instanceof Error ? err : new Error('Unknown error in dialogue speech'));
      setIsSpeaking(false);
      
      // Fallback to browser speech synthesis
      if ('speechSynthesis' in window) {
        try {
          const utterance = new SpeechSynthesisUtterance(options.text);
          utterance.rate = 0.9;
          utterance.pitch = 1.1;
          utterance.volume = 0.8;
          
          utterance.onend = () => setIsSpeaking(false);
          window.speechSynthesis.speak(utterance);
        } catch (synthErr) {
          console.error('Error in fallback speech synthesis:', synthErr);
        }
      }
    }
  }, [options.salesCallStyle]);

  // Stop speaking
  const stop = useCallback(() => {
    diaService.stopAudio();
    
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    
    setIsSpeaking(false);
  }, []);

  return {
    speak,
    stop,
    isSpeaking,
    error
  };
}

export default useDialogueSpeech;
