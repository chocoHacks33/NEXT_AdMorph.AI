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

export default function StreamingChatInterface({ onComplete }: ChatInterfaceProps) {
  // Chat state
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "ai",
      content:
        "Hi! I'm your AI marketing assistant. I'll help you create personalized ad variants for your campaign. Let's start by understanding your business needs. What's your target engagement goal?",
      timestamp: new Date(),
    },
  ])
  const [currentStep, setCurrentStep] = useState(0)
  const [businessData, setBusinessData] = useState<BusinessData>({
    targetEngagement: "",
    budget: "",
    audience: "",
    themes: [],
  })

  // Voice UI state
  const [voiceState, setVoiceState] = useState<VoiceState>("idle")
  const [interimTranscript, setInterimTranscript] = useState("")
  const messageEndRef = useRef<HTMLDivElement>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const shouldAutoSpeak = useRef<boolean>(true)

  // Questions for the conversation flow
  const questions = [
    "What's your target engagement goal? (e.g., increase clicks by 25%, boost conversions)",
    "What's your advertising budget for this campaign?",
    "Who is your target audience? (Be as specific as possible)",
    "What themes or messaging should we maintain in your ads? Any restrictions?",
    "Please upload your original ad or describe it if you don't have a file ready.",
  ]

  // Initialize hooks
  const { speak, stop, isSpeaking } = useVoice()
  const { 
    isRecording, 
    isTranscribing, 
    startRecording, 
    stopRecording, 
    error: transcriptionError 
  } = useWhisperTranscription({
    onTranscriptionStart: () => {
      setVoiceState("processing")
      setInterimTranscript("Processing transcription...")
    },
    onTranscriptionComplete: (transcript) => {
      handleUserMessage(transcript)
    },
    onTranscriptionError: (error) => {
      console.error("Transcription error:", error)
      setVoiceState("idle")
      setInterimTranscript("")
      
      // Add error as system message
      addMessage({
        type: "system",
        content: `Error with voice input: ${error.message}. Please try again.`,
      })
    }
  })

  // Streaming response hook
  const { 
    streamResponse, 
    isStreaming, 
    streamedText, 
    stopStreaming, 
    error: streamingError
  } = useOpenAIStreaming({
    systemMessage: "You are an AI marketing assistant having a natural sales conversation. Be friendly, personable, and use conversational language. Acknowledge the user's responses and show understanding before moving on to the next question.",
    onStreamingStart: () => {
      // Add a new AI message that will be updated as streaming progresses
      const streamingMessage: Message = {
        id: Date.now().toString(),
        type: "ai",
        content: "",
        timestamp: new Date(),
        isStreaming: true,
      }
      setMessages(prev => [...prev, streamingMessage])
    },
    onStreamingComplete: (fullText) => {
      // Update the last message with complete text and remove streaming flag
      setMessages(prev => {
        const updatedMessages = [...prev]
        const lastMessage = updatedMessages[updatedMessages.length - 1]
        if (lastMessage && lastMessage.isStreaming) {
          lastMessage.content = fullText
          lastMessage.isStreaming = false
        }
        return updatedMessages
      })
      
      // Speak the AI response
      if (shouldAutoSpeak.current) {
        speakAIResponse(fullText)
      }
    }
  })

  // Scroll to bottom when messages change
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, streamedText])

  // Update the streaming message as new tokens arrive
  useEffect(() => {
    if (isStreaming && streamedText) {
      setMessages(prev => {
        const updatedMessages = [...prev]
        const lastMessage = updatedMessages[updatedMessages.length - 1]
        if (lastMessage && lastMessage.isStreaming) {
          lastMessage.content = streamedText
        }
        return updatedMessages
      })
    }
  }, [isStreaming, streamedText])

  // Handle errors from streaming
  useEffect(() => {
    if (streamingError) {
      addMessage({
        type: "system",
        content: `Error with AI response: ${streamingError.message}. Please try again.`,
      })
    }
  }, [streamingError])

  // Add a new message to the chat
  const addMessage = useCallback((message: Partial<Message>) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      type: message.type || "user",
      content: message.content || "",
      timestamp: new Date(),
      isStreaming: message.isStreaming,
    }
    
    setMessages(prev => [...prev, newMessage])
    return newMessage
  }, [])

  // Handle user message (from text or voice transcription)
  const handleUserMessage = useCallback((text: string) => {
    if (!text.trim()) return
    
    // Stop any current AI speech
    stop()
    setVoiceState("idle")
    setInterimTranscript("")
    
    // Add user message to chat
    addMessage({
      type: "user",
      content: text,
    })
    
    // Update business data based on current step
    const updatedData = { ...businessData }
    switch (currentStep) {
      case 0:
        updatedData.targetEngagement = text
        break
      case 1:
        updatedData.budget = text
        break
      case 2:
        updatedData.audience = text
        break
      case 3:
        updatedData.themes = text.split(",").map((t) => t.trim())
        break
    }
    setBusinessData(updatedData)
    
    // Generate AI streaming response
    generateStreamingResponse(text)
  }, [currentStep, businessData, stop, addMessage])

  // Generate streaming response based on user input
  const generateStreamingResponse = useCallback((userText: string) => {
    // Personalized acknowledgment based on the user's input
    let acknowledgment = ""
    if (userText.length > 0) {
      if (currentStep === 0) {
        acknowledgment = `Thanks for sharing your engagement goal of "${userText}". That gives me a good starting point. `
      } else if (currentStep === 1) {
        acknowledgment = `A budget of ${userText} works well. `
      } else if (currentStep === 2) {
        acknowledgment = `I understand your target audience is ${userText}. That's a great demographic to focus on. `
      } else if (currentStep === 3) {
        acknowledgment = `I'll make sure to incorporate these themes and messaging priorities. `
      }
    }
    
    // Stream the AI response
    if (currentStep < questions.length - 1) {
      const nextQuestion = questions[currentStep + 1]
      streamResponse(`${acknowledgment}${nextQuestion}`)
      setCurrentStep(prev => prev + 1)
    } else {
      streamResponse(`${acknowledgment}Perfect! I have all the information I need. Let me process your requirements and generate personalized ad variants for different demographics and interest groups. This will take a moment...`)
      
      // Complete the business data collection after response
      setTimeout(() => {
        onComplete(businessData)
      }, 3000)
    }
  }, [currentStep, questions, businessData, streamResponse, onComplete])

  // Speak AI response using voice synthesis
  const speakAIResponse = useCallback((text: string) => {
    setVoiceState("speaking")
    speak({ text })
      .then(() => {
        setVoiceState("idle")
      })
      .catch((error) => {
        console.error("Voice error:", error)
        setVoiceState("idle")
        
        // Add error as system message
        addMessage({
          type: "system",
          content: `Error with voice output: ${error.message}`,
        })
      })
  }, [speak, addMessage])

  // Toggle microphone
  const toggleMicrophone = useCallback(() => {
    if (voiceState === "idle") {
      // Start recording
      setVoiceState("listening")
      startRecording()
    } else if (voiceState === "listening") {
      // Stop recording and process transcription
      stopRecording()
    } else if (voiceState === "speaking") {
      // Stop speaking
      stop()
      setVoiceState("idle")
    }
  }, [voiceState, startRecording, stopRecording, stop])

  // Handle file upload
  const handleFileUpload = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setBusinessData(prev => ({ ...prev, originalAd: file }))
      
      const userMessage = `Uploaded file: ${file.name}`
      handleUserMessage(userMessage)
    }
  }, [handleUserMessage])

  // Visualize recording with simple animation
  const waveformBars = Array.from({ length: 10 }, (_, i) => 
    Math.round(Math.random() * (voiceState === "listening" ? 20 : 5))
  )

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
                  message.type === "user" ? "bg-purple-600 text-white" : 
                  message.type === "system" ? "bg-red-600 text-white" : 
                  "bg-gray-100 text-gray-800"
                }`}
              >
                <p className="text-sm">{message.content}</p>
                <p className="text-xs opacity-70 mt-1">{message.timestamp.toLocaleTimeString()}</p>
              </div>
            </div>
          ))}
          <div ref={messageEndRef} />
        </div>

        {/* Voice Interface Controls */}
        <div className="p-4 border-t">
          {/* Interim transcript display */}
          {interimTranscript && (
            <div className="mb-4 p-2 rounded-md bg-gray-100 text-gray-800">
              {interimTranscript}
            </div>
          )}
          
          {/* Audio recording visualization */}
          {voiceState === "listening" && (
            <div className="flex items-center justify-center h-8 mb-2">
              {waveformBars.map((height, index) => (
                <div
                  key={index}
                  className="mx-0.5 bg-purple-500 rounded-full w-1"
                  style={{ 
                    height: `${height}px`,
                    transition: 'height 150ms ease-in-out'
                  }}
                />
              ))}
            </div>
          )}
          
          {/* Voice controls */}
          <div className="flex items-center space-x-2">
            {/* Microphone button */}
            <Button
              onClick={toggleMicrophone}
              variant={voiceState === "listening" ? "destructive" : "default"}
              size="icon"
              className="w-10 h-10 rounded-full"
            >
              {voiceState === "listening" ? (
                <MicOff className="h-5 w-5" />
              ) : (
                <Mic className="h-5 w-5" />
              )}
            </Button>
            
            {/* Voice status indicator */}
            <div className="text-sm text-gray-500">
              {voiceState === "idle" && "Click mic to speak"}
              {voiceState === "listening" && "Listening..."}
              {voiceState === "processing" && "Processing..."}
              {voiceState === "speaking" && "Speaking..."}
            </div>
            
            {/* Right-aligned controls */}
            <div className="flex-1"></div>
            
            {/* File upload */}
            <div className="relative">
              <input
                type="file"
                accept="image/*,video/*"
                onChange={handleFileUpload}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
              <Button variant="outline" size="icon">
                <Upload className="h-4 w-4" />
              </Button>
            </div>
            
            {/* Stop voice button */}
            {voiceState === "speaking" && (
              <Button
                onClick={() => {
                  stop()
                  setVoiceState("idle")
                }}
                variant="outline"
                size="icon"
              >
                <VolumeX className="h-4 w-4" />
              </Button>
            )}
          </div>
          
          {/* Progress indicator */}
          <div className="mt-3">
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
        </div>
      </div>
    </div>
  )
}
