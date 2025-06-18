"use client"

import { useState, useRef, useEffect, useCallback } from "react"
import { Button } from "@/components/ui/button"
import { Mic, MicOff, Volume2, VolumeX, Send, Upload } from "lucide-react"
import { useVoice } from "@/lib/hooks/useVoice"
import useWhisperTranscription from "@/lib/hooks/useWhisperTranscription"
import useOpenAIStreaming from "@/lib/hooks/useOpenAIStreaming"

interface BusinessData {
  targetEngagement: string
  budget: string
  audience: string
  themes: string[]
  originalAd?: File
}

interface ChatInterfaceProps {
  onComplete: (data: BusinessData) => void
}

interface Message {
  id: string
  type: "ai" | "user" | "system"
  content: string
  timestamp: Date
  isStreaming?: boolean
}

// Voice recording states
type VoiceState = "idle" | "listening" | "processing" | "speaking"

export default function ChatInterface({ onComplete }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "ai",
      content:
        "Hi! I'm your AI marketing assistant. I'll help you create personalized ad variants for your campaign. Let's start by understanding your business needs. What's your target engagement goal?",
      timestamp: new Date(),
    },
  ])

  const [currentInput, setCurrentInput] = useState("")
  const [isListening, setIsListening] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [businessData, setBusinessData] = useState<BusinessData>({
    targetEngagement: "",
    budget: "",
    audience: "",
    themes: [],
  })

  const questions = [
    "What's your target engagement goal? (e.g., increase clicks by 25%, boost conversions)",
    "What's your advertising budget for this campaign?",
    "Who is your target audience? (Be as specific as possible)",
    "What themes or messaging should we maintain in your ads? Any restrictions?",
    "Please upload your original ad or describe it if you don't have a file ready.",
  ]

  const handleSendMessage = () => {
    if (!currentInput.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: currentInput,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])

    // Update business data based on current step
    const updatedData = { ...businessData }
    switch (currentStep) {
      case 0:
        updatedData.targetEngagement = currentInput
        break
      case 1:
        updatedData.budget = currentInput
        break
      case 2:
        updatedData.audience = currentInput
        break
      case 3:
        updatedData.themes = currentInput.split(",").map((t) => t.trim())
        break
    }
    setBusinessData(updatedData)

    setCurrentInput("")

    // Add AI response
    setTimeout(() => {
      if (currentStep < questions.length - 1) {
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: "ai",
          content: questions[currentStep + 1],
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, aiMessage])
        setCurrentStep((prev) => prev + 1)
      } else {
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: "ai",
          content:
            "Perfect! I have all the information I need. Let me process your requirements and generate personalized ad variants for different demographics and interest groups. This will take a moment...",
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, aiMessage])

        setTimeout(() => {
          onComplete(updatedData)
        }, 2000)
      }
    }, 1000)
  }

  const toggleVoice = () => {
    if (isListening) {
      stopListening()
    } else {
      startRecording()
    }
    setIsListening(!isListening)
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setBusinessData((prev) => ({ ...prev, originalAd: file }))
      const userMessage: Message = {
        id: Date.now().toString(),
        type: "user",
        content: `Uploaded file: ${file.name}`,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, userMessage])
    }
  }

  // Voice-first design states and refs
  const [voiceState, setVoiceState] = useState<VoiceState>("idle")
  const { speak, isSpeaking, isLoading, error: voiceError, stopSpeaking: stopVoiceSynthesis } = useVoice()
  const [interimTranscript, setInterimTranscript] = useState<string>("") // For displaying in UI

  // Setup Whisper transcription
  const { isRecording, isTranscribing, startRecording, stopRecording, error: transcriptionError } = useWhisperTranscription({
    onTranscriptionStart: () => {
      setVoiceState("processing")
      setInterimTranscript("Processing transcription...")
    },
    onTranscriptionComplete: async (transcript) => {
      setInterimTranscript("") // Clear interim transcript
      processUserMessage(transcript) // Handle the transcribed message
    },
    onTranscriptionError: (error) => {
      console.error("Transcription error:", error)
      setVoiceState("idle")
      setInterimTranscript("") // Clear interim transcript
      // Show error message in chat
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          type: "system",
          content: `Error: ${error.message || "Could not transcribe audio"}`,
          timestamp: new Date(),
        },
      ])
    },
  })

  const startRecording = () => {
    startRecording()
    setVoiceState("listening")
  }

  const stopListening = () => {
    stopRecording()
    setVoiceState("idle")
  }

  const processUserMessage = (transcript: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: transcript,
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, userMessage])

    // Update business data based on current step
    const updatedData = { ...businessData }
    switch (currentStep) {
      case 0:
        updatedData.targetEngagement = transcript
        break
      case 1:
        updatedData.budget = transcript
        break
      case 2:
        updatedData.audience = transcript
        break
      case 3:
        updatedData.themes = transcript.split(",").map((t) => t.trim())
        break
    }
    setBusinessData(updatedData)

    // Generate AI response based on current step
    let aiResponse = ""
    if (currentStep < questions.length - 1) {
      aiResponse = questions[currentStep + 1]

      // Add acknowledgment based on the transcript
      if (transcript.length > 0) {
        if (currentStep === 0) {
          aiResponse = `Great! ${transcript} is a solid goal. ${aiResponse}`
        } else if (currentStep === 1) {
          aiResponse = `A budget of ${transcript} works well. ${aiResponse}`
        } else if (currentStep === 2) {
          aiResponse = `Perfect! We'll focus on ${transcript}. ${aiResponse}`
        }
      }

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "ai",
        content: aiResponse,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, aiMessage])

      // Use voice synthesis to speak the response
      setVoiceState("speaking")
      speak({ text: aiResponse })

      setCurrentStep((prev) => prev + 1)
    } else {
      aiResponse = "Perfect! I have all the information I need. Let me process your requirements and generate personalized ad variants for different demographics and interest groups. This will take a moment..."

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "ai",
        content: aiResponse,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, aiMessage])

      // Use voice synthesis to speak the response
      setVoiceState("speaking")
      speak({ text: aiResponse })

      // Complete the process
      setTimeout(() => {
        onComplete(updatedData)
      }, 1000)
    }
  }

  useEffect(() => {
    if (voiceState === "speaking") {
      audioRef.current?.addEventListener("ended", () => {
        setVoiceState("idle")
        setInterimTranscript("")
      })
    }

    return () => {
      audioRef.current?.removeEventListener("ended", () => {
        setVoiceState("idle")
        setInterimTranscript("")
      })
    }
  }, [voiceState])

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-2xl shadow-xl overflow-hidden" style={{ height: "600px" }}>
        {/* Chat Header */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 p-4">
          <h2 className="text-white text-xl font-semibold">AI Marketing Assistant</h2>
          <p className="text-purple-100 text-sm">Let's create your perfect ad campaign</p>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4" style={{ height: "400px" }}>
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.type === "user" ? "bg-purple-600 text-white" : message.type === "system" ? "bg-red-600 text-white" : "bg-gray-100 text-gray-800"
                }`}
              >
                <p className="text-sm">{message.content}</p>
                <p className="text-xs opacity-70 mt-1">{message.timestamp.toLocaleTimeString()}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Voice-First Interface */}
        <div className="flex flex-col items-center justify-center h-full">
          {/* Speech-to-Text Display */}
          {interimTranscript && <div className="mb-4 p-2 rounded-md bg-gray-100 text-gray-800">{interimTranscript}</div>}

          {/* Waveform Visualization */}
          {voiceState === "listening" && (
            <div className="mb-4">
              <Waveform data={waveform} />
            </div>
          )}

          {/* Large Microphone Button */}
          <div className="relative flex h-12 items-center">
            {/* Mic button */}
            <button
              onClick={toggleMic}
              className={`flex h-10 w-10 items-center justify-center rounded-full ${voiceState === "idle" ? "bg-blue-500 hover:bg-blue-600" : voiceState === "listening" ? "bg-red-500 animate-pulse" : voiceState === "processing" ? "bg-yellow-500" : "bg-green-500"} text-white`}
              <div className="relative">
                <input
                  type="file"
                  accept="image/*,video/*"
                  onChange={handleFileUpload}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                <Button variant="outline" size="sm">
                  <Upload className="h-4 w-4" />
                </Button>
              </div>
            )}

            <Button
              variant="outline"
              size="sm"
              onClick={toggleVoice}
              className={isListening ? "bg-red-50 border-red-200" : ""}
            >
              {isListening ? <MicOff className="h-4 w-4 text-red-600" /> : <Mic className="h-4 w-4" />}
            </Button>

            <Button onClick={handleSendMessage} size="sm">
              <Send className="h-4 w-4" />
            </Button>
          </div>

          {/* Progress Indicator */}
        {/*   <div className="mt-3">
            <div className="flex justify-between text-xs text-gray-500 mb-1">
              <span>Progress</span>
              <span>
                {currentStep + 1} of {questions.length}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${((currentStep + 1) / questions.length) * 100}%` }}
              />
            </div>
          </div>
        </div> */}
      </div>
    </div>
  )
}

// Audio Visualization Component
const Waveform = ({ data }: { data: number[] }) => {
  return (
    <div className="flex items-center h-10">
      {data.map((value, index) => (
        <div
          key={index}
          className="mx-0.5"
          style={{
            width: "4px",
            height: `${value}px`,
            backgroundColor: "purple",
          }}
        />
      ))}
    </div>
  )
}
