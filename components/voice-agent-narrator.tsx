"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Volume2, VolumeX, Mic } from "lucide-react"
import useVoice from "@/lib/hooks/useVoice"
import { VOICE_IDS } from "@/lib/elevenlabs"

interface VoiceAgentNarratorProps {
  currentStep: number
  agentSteps: Array<{
    id: string
    name: string
    description: string
    status: "pending" | "active" | "completed"
  }>
  isEnabled: boolean
  onToggle: () => void
  onVoiceCommand: (command: string) => void
}

export default function VoiceAgentNarrator({
  currentStep,
  agentSteps,
  isEnabled,
  onToggle,
  onVoiceCommand,
}: VoiceAgentNarratorProps) {
  const [isListening, setIsListening] = useState(false)
  
  // Use our unified voice hook that supports both Eleven Labs and Dia
  const {
    isSpeaking,
    speak,
    stop: stopSpeaking,
    error: voiceError
  } = useVoice()

  const narrateStep = async (step: any) => {
    if (!isEnabled) return
    
    try {
      const narrateText = `Now ${step.description.toLowerCase()}. This helps ensure your ad resonates with the right audience.`;
      await speak({ text: narrateText });
    } catch (error) {
      console.error('Error with narration:', error);
      // Fall back to native speech synthesis if there's an error
      if ("speechSynthesis" in window) {
        const utterance = new SpeechSynthesisUtterance(
          `Now ${step.description.toLowerCase()}. This helps ensure your ad resonates with the right audience.`,
        );
        utterance.rate = 0.9;
        utterance.pitch = 1.1;
        utterance.volume = 0.7;
        speechSynthesis.speak(utterance);
      }
    }
  }

  const startVoiceCommands = () => {
    if (isSpeaking) {
      stopSpeaking();
    }
    
    setIsListening(true)
    
    // Start listening for voice commands using the browser's speech recognition
    if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
      const SpeechRecognition = window.SpeechRecognition || (window as any).webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';
      
      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript.toLowerCase();
        onVoiceCommand(transcript);
        setIsListening(false);
      };
      
      recognition.onerror = () => {
        setIsListening(false);
      };
      
      recognition.onend = () => {
        setIsListening(false);
      };
      
      recognition.start();
      
      // Fallback timeout in case recognition doesn't end properly
      setTimeout(() => {
        setIsListening(false);
      }, 5000);
    } else {
      // Fallback for browsers that don't support speech recognition
      setTimeout(() => {
        const commands = ["like this ad", "skip this one", "regenerate", "tell me more"];
        const randomCommand = commands[Math.floor(Math.random() * commands.length)];
        onVoiceCommand(randomCommand);
        setIsListening(false);
      }, 2000);
    }
  }

  useEffect(() => {
    const activeStep = agentSteps.find((step) => step.status === "active")
    if (activeStep && isEnabled) {
      setTimeout(() => narrateStep(activeStep), 500)
    }
    // narrateStep contains 'speak' which changes on every render
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentStep, agentSteps, isEnabled])

  return (
    <div className="flex items-center space-x-3 p-4 bg-purple-50 rounded-lg">
      <Button
        variant="ghost"
        size="sm"
        onClick={onToggle}
        className={`${isEnabled ? "text-purple-600" : "text-gray-400"}`}
      >
        {isEnabled ? <Volume2 className="h-4 w-4" /> : <VolumeX className="h-4 w-4" />}
      </Button>

      <div className="flex-1">
        <p className="text-sm font-medium text-purple-900">
          {isSpeaking ? "AI is explaining the current step..." : "Voice narration ready"}
        </p>
        <p className="text-xs text-purple-600">Say "like", "skip", or "regenerate" to control ads</p>
      </div>

      <Button
        variant="outline"
        size="sm"
        onClick={startVoiceCommands}
        disabled={isListening || isSpeaking}
        className={`${isListening ? "bg-red-50 border-red-200" : ""}`}
      >
        <Mic className={`h-4 w-4 ${isListening ? "text-red-600 animate-pulse" : ""}`} />
      </Button>
    </div>
  )
}
