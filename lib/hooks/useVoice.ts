import { useState, useCallback, useEffect, useRef, useMemo } from 'react';
import elevenLabsService from '../elevenlabs';
import diaService from '../dia';
import openAIService from '../openai';
import useTextToSpeech from './useTextToSpeech';
import useDialogueSpeech from './useDialogueSpeech';
import useOpenAISpeech from './useOpenAISpeech';

// Common interface for both voice systems
export interface VoiceOptions {
  text: string;
  [key: string]: any;
}

interface UseVoiceReturn {
  speak: (options: VoiceOptions) => Promise<void>;
  stop: () => void;
  isSpeaking: boolean;
  error: Error | null;
}

/**
 * Hook that provides voice capabilities using the configured voice model
 * Switches between Eleven Labs and Dia based on NEXT_PUBLIC_VOICE_MODEL
 */
export function useVoice(): UseVoiceReturn {
  // Use useRef for the voice model to avoid re-renders
  const voiceModelRef = useRef<string>('openai');
  const [error, setError] = useState<Error | null>(null);
  
  // Get instances of all voice hooks
  const elevenLabs = useTextToSpeech();
  const dia = useDialogueSpeech({ salesCallStyle: true });
  const openai = useOpenAISpeech({ salesCallStyle: true });
  
  // Read voice model from environment only on mount
  useEffect(() => {
    const configuredModel = process.env.NEXT_PUBLIC_VOICE_MODEL || 'openai';
    voiceModelRef.current = configuredModel.toLowerCase();
  }, []);

  // Speak using the selected voice model
  const speak = useCallback(async (options: VoiceOptions) => {
    try {
      setError(null);
      
      switch (voiceModelRef.current) {
        case 'dia':
          await dia.speak({ text: options.text });
          break;
        case 'openai':
          await openai.speak({ text: options.text });
          break;
        default:
          // Default to Eleven Labs
          await elevenLabs.speak(options.text);
          break;
      }
    } catch (err) {
      console.error('Voice error:', err);
      setError(err instanceof Error ? err : new Error('Unknown voice error'));
    }
  }, [elevenLabs, dia, openai]); // Remove voiceModel as it's now accessed via ref

  // Stop any currently playing voice
  const stop = useCallback(() => {
    switch (voiceModelRef.current) {
      case 'dia':
        dia.stop();
        break;
      case 'openai':
        openai.stop();
        break;
      default:
        elevenLabs.stop();
        break;
    }
  }, [elevenLabs, dia, openai]); // Remove voiceModel as it's now accessed via ref

  // Determine if any voice is speaking - memoize this value
  const isSpeaking = useMemo(() => {
    return voiceModelRef.current === 'dia' ? dia.isSpeaking :
           voiceModelRef.current === 'openai' ? openai.isSpeaking :
           elevenLabs.isSpeaking;
  }, [dia.isSpeaking, openai.isSpeaking, elevenLabs.isSpeaking]);

  // Memoize the error to prevent unnecessary re-renders
  const combinedError = useMemo(() => {
    return error || 
           (voiceModelRef.current === 'dia' ? dia.error : 
            voiceModelRef.current === 'openai' ? openai.error : 
            elevenLabs.error);
  }, [error, dia.error, openai.error, elevenLabs.error]);

  return {
    speak,
    stop,
    isSpeaking,
    error: combinedError
  };
}

export default useVoice;
