"use client"

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Volume2, VolumeX, Mic } from "lucide-react"

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
  const [isSpeaking, setIsSpeaking] = useState(false)

  const narrateStep = (step: any) => {
    if (!isEnabled || !("speechSynthesis" in window)) return

    setIsSpeaking(true)
    const utterance = new SpeechSynthesisUtterance(
      `Now ${step.description.toLowerCase()}. This helps ensure your ad resonates with the right audience.`,
    )

    utterance.rate = 0.9
    utterance.pitch = 1.1
    utterance.volume = 0.7

    utterance.onend = () => {
      setIsSpeaking(false)
    }

    speechSynthesis.speak(utterance)
  }

  const startVoiceCommands = () => {
    setIsListening(true)

    // Simulate voice recognition for commands
    setTimeout(() => {
      const commands = ["like this ad", "skip this one", "regenerate", "tell me more"]
      const randomCommand = commands[Math.floor(Math.random() * commands.length)]
      onVoiceCommand(randomCommand)
      setIsListening(false)
    }, 2000)
  }

  useEffect(() => {
    const activeStep = agentSteps.find((step) => step.status === "active")
    if (activeStep && isEnabled) {
      setTimeout(() => narrateStep(activeStep), 500)
    }
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
