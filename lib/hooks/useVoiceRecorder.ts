import { useState, useRef, useCallback, useEffect } from 'react';

interface VoiceRecorderOptions {
  onDataAvailable?: (data: Blob) => void;
  onStop?: (audioUrl: string, blob: Blob) => void;
  onError?: (error: Error) => void;
  onAudioLevels?: (levels: number[]) => void;
}

interface VoiceRecorderState {
  isRecording: boolean;
  isPermissionGranted: boolean | null;
  recordingTime: number;
  audioUrl: string | null;
  start: () => Promise<void>;
  stop: () => void;
  reset: () => void;
}

const useVoiceRecorder = (options: VoiceRecorderOptions = {}): VoiceRecorderState => {
  const [isRecording, setIsRecording] = useState(false);
  const [isPermissionGranted, setIsPermissionGranted] = useState<boolean | null>(null);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<number | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const dataArrayRef = useRef<Uint8Array | null>(null);

  // Clean up resources when unmounting
  useEffect(() => {
    return () => {
      if (timerRef.current) {
        window.clearInterval(timerRef.current);
      }
      stopMediaTracks();
    };
  }, []);

  const stopMediaTracks = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => {
        track.stop();
      });
    }

    // Clean up audio context
    if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
      audioContextRef.current.close().catch(console.error);
    }
  };

  const reset = useCallback(() => {
    setIsRecording(false);
    setRecordingTime(0);
    setAudioUrl(null);
    chunksRef.current = [];
    stopMediaTracks();
  }, []);

  const updateAudioLevels = useCallback(() => {
    if (
      !analyserRef.current || 
      !dataArrayRef.current || 
      !options.onAudioLevels ||
      !isRecording
    ) {
      return;
    }

    analyserRef.current.getByteFrequencyData(dataArrayRef.current);
    
    // Calculate audio level
    const bufferLength = analyserRef.current.frequencyBinCount;
    const levelCount = 20; // Number of levels we want
    const levelsPerSegment = Math.floor(bufferLength / levelCount);
    const levels = Array(levelCount).fill(0);
    
    for (let i = 0; i < levelCount; i++) {
      let sum = 0;
      const startIndex = i * levelsPerSegment;
      
      for (let j = 0; j < levelsPerSegment; j++) {
        const index = startIndex + j;
        if (index < bufferLength) {
          sum += dataArrayRef.current[index];
        }
      }
      
      const average = sum / levelsPerSegment;
      // Scale to a more visually appealing range
      levels[i] = Math.max(5, Math.min(40, average / 5));
    }
    
    options.onAudioLevels(levels);
    
    requestAnimationFrame(updateAudioLevels);
  }, [isRecording, options]);

  const start = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      setIsPermissionGranted(true);
      
      // Set up audio context for level visualization
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      analyserRef.current.fftSize = 256;
      
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);
      
      const bufferLength = analyserRef.current.frequencyBinCount;
      dataArrayRef.current = new Uint8Array(bufferLength);

      // Create media recorder
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.addEventListener('dataavailable', (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
          if (options.onDataAvailable) {
            options.onDataAvailable(event.data);
          }
        }
      });

      mediaRecorder.addEventListener('stop', () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        const url = URL.createObjectURL(blob);
        setAudioUrl(url);
        
        if (options.onStop) {
          options.onStop(url, blob);
        }
        
        if (timerRef.current) {
          window.clearInterval(timerRef.current);
          timerRef.current = null;
        }
      });

      // Start recording
      mediaRecorder.start(1000); // Capture data every second
      setIsRecording(true);
      
      // Start timer
      timerRef.current = window.setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);

      // Start updating audio levels
      if (options.onAudioLevels) {
        updateAudioLevels();
      }
    } catch (error) {
      console.error('Error starting voice recording:', error);
      if (error instanceof Error) {
        setIsPermissionGranted(false);
        if (options.onError) {
          options.onError(error);
        }
      }
    }
  }, [options, updateAudioLevels]);

  const stop = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }, [isRecording]);

  return {
    isRecording,
    isPermissionGranted,
    recordingTime,
    audioUrl,
    start,
    stop,
    reset,
  };
};

export default useVoiceRecorder;
