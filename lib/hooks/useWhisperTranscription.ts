/**
 * Custom hook for voice recording and OpenAI Whisper transcription
 */

import { useState, useRef, useCallback, useEffect } from 'react';
import whisperTranscription from '../whisper-transcription';

interface UseWhisperTranscriptionOptions {
  onTranscriptionComplete?: (transcript: string) => void;
  onTranscriptionStart?: () => void;
  onTranscriptionError?: (error: Error) => void;
}

export default function useWhisperTranscription(options: UseWhisperTranscriptionOptions = {}) {
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  
  // Audio recording related refs
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  
  // Clean up function to stop recording
  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }, [isRecording]);
  
  // Effect to clean up on unmount
  useEffect(() => {
    return () => {
      stopRecording();
    };
  }, [stopRecording]);
  
  // Start recording function
  const startRecording = useCallback(async () => {
    // Reset state
    setError(null);
    audioChunksRef.current = [];
    
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      
      mediaRecorder.onstop = async () => {
        // Get all audio data
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        
        // Check if the audio data is valid (not too small)
        if (audioBlob.size < 1000) {
          const tooShortError = new Error('Recording too short or no audio detected');
          setError(tooShortError);
          setIsTranscribing(false);
          
          if (options.onTranscriptionError) {
            options.onTranscriptionError(tooShortError);
          }
          return;
        }
        
        try {
          setIsTranscribing(true);
          
          // Send to Whisper API with retry logic for network issues
          let retries = 2;
          let transcript = "";
          let lastError = null;
          
          while (retries >= 0) {
            try {
              transcript = await whisperTranscription.transcribeAudio({
                audioBlob,
                onTranscriptionStart: options.onTranscriptionStart
              });
              
              // If we got here, transcription succeeded
              break;
            } catch (err) {
              lastError = err;
              retries--;
              if (retries >= 0) {
                // Wait before retrying
                await new Promise(resolve => setTimeout(resolve, 1000));
                console.log(`Retrying transcription, ${retries} attempts left`);
              }
            }
          }
          
          if (transcript) {
            setIsTranscribing(false);
            if (options.onTranscriptionComplete) {
              options.onTranscriptionComplete(transcript);
            }
          } else {
            throw lastError || new Error('Failed to transcribe after multiple attempts');
          }
        } catch (error) {
          console.error('Transcription error:', error);
          setError(error instanceof Error ? error : new Error(String(error)));
          setIsTranscribing(false);
          
          if (options.onTranscriptionError) {
            options.onTranscriptionError(error instanceof Error ? error : new Error(String(error)));
          }
        }
        
        // Stop all audio tracks
        stream.getTracks().forEach(track => track.stop());
      };
      
      // Start recording
      mediaRecorder.start(100); // Collect data every 100ms
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
      setError(error instanceof Error ? error : new Error(String(error)));
      
      if (options.onTranscriptionError) {
        options.onTranscriptionError(error instanceof Error ? error : new Error(String(error)));
      }
    }
  }, [options]);
  
  // Return the hook API
  return {
    isRecording,
    isTranscribing,
    error,
    startRecording,
    stopRecording
  };
}
