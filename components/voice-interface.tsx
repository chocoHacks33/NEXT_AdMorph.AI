"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Mic, MicOff, Upload, SkipBackIcon as Skip, ArrowRight, CheckCircle, Loader2, Sparkles } from "lucide-react"

interface BusinessData {
  targetEngagement: string
  budget: string
  audience: string
  themes: string[]
  originalAd?: File
}

interface VoiceInterfaceProps {
  onComplete: (data: BusinessData) => void
}

type VoiceState = "idle" | "listening" | "processing"

interface AgentStep {
  id: string
  name: string
  status: "pending" | "active" | "completed"
}

export default function VoiceInterface({ onComplete }: VoiceInterfaceProps) {
  const [voiceState, setVoiceState] = useState<VoiceState>("idle")
  const [currentStep, setCurrentStep] = useState(0)
  const [currentTranscript, setCurrentTranscript] = useState("")
  const [audioLevels, setAudioLevels] = useState<number[]>(new Array(20).fill(0))
  const [businessData, setBusinessData] = useState<BusinessData>({
    targetEngagement: "",
    budget: "",
    audience: "",
    themes: [],
  })

  const [agentSteps, setAgentSteps] = useState<AgentStep[]>([
    { id: "1", name: "Requirements", status: "pending" },
    { id: "2", name: "Audience", status: "pending" },
    { id: "3", name: "Creative", status: "pending" },
    { id: "4", name: "Optimize", status: "pending" },
    { id: "5", name: "Ready", status: "pending" },
  ])

  const questions = [
    "What's your target engagement goal?",
    "What's your advertising budget?",
    "Who is your target audience?",
    "What themes should we maintain?",
    "Ready to generate your ads?",
  ]

  // Skip to processing
  const handleSkipVoice = () => {
    const defaultData: BusinessData = {
      targetEngagement: "Increase click-through rate by 25%",
      budget: "$8,000 per month",
      audience: "Young professionals aged 25-35",
      themes: ["Modern", "Professional"],
    }
    onComplete(defaultData)
  }

  // Generate waveform
  const generateWaveform = () => {
    return Array.from({ length: 20 }, () => Math.random() * 40 + 5)
  }

  // Start listening
  const startListening = () => {
    setVoiceState("listening")
    setCurrentTranscript("")

    const interval = setInterval(() => {
      setAudioLevels(generateWaveform())
    }, 150)

    setTimeout(() => {
      setVoiceState("processing")
      clearInterval(interval)
      setAudioLevels(new Array(20).fill(5))

      // Update agent step
      setAgentSteps((prev) =>
        prev.map((step, index) => ({
          ...step,
          status: index === currentStep ? "active" : index < currentStep ? "completed" : "pending",
        })),
      )

      setTimeout(() => {
        const mockResponses = [
          "Increase click-through rate by 25%",
          "$8,000 per month",
          "Young professionals aged 25-35",
          "Modern, professional tone",
          "Yes, let's generate!",
        ]

        const response = mockResponses[currentStep] || "Ready"
        setCurrentTranscript(response)
        handleVoiceInput(response)
      }, 1500)
    }, 3000)
  }

  const handleVoiceInput = (transcript: string) => {
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

    // Mark current step as completed
    setAgentSteps((prev) =>
      prev.map((step, index) => ({
        ...step,
        status: index <= currentStep ? "completed" : "pending",
      })),
    )

    if (currentStep < questions.length - 1) {
      setCurrentStep((prev) => prev + 1)
      setTimeout(() => {
        setVoiceState("idle")
        setCurrentTranscript("")
      }, 1000)
    } else {
      setTimeout(() => {
        onComplete(updatedData)
      }, 2000)
    }
  }

  const stopListening = () => {
    setVoiceState("idle")
    setAudioLevels(new Array(20).fill(5))
  }

  useEffect(() => {
    setAudioLevels(new Array(20).fill(5))
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-slate-900/10 to-pink-900/20" />
      <div className="absolute top-1/4 left-1/3 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 right-1/3 w-96 h-96 bg-pink-500/10 rounded-full blur-3xl animate-pulse delay-1000" />

      {/* Skip Button */}
      <div className="absolute top-8 right-8 z-20">
        <Button
          onClick={handleSkipVoice}
          variant="outline"
          className="bg-slate-900/80 backdrop-blur-xl border-purple-500/30 text-purple-300 hover:text-white hover:bg-purple-500/20 rounded-2xl px-6 py-3 shadow-lg shadow-purple-500/10 transition-all duration-300"
        >
          <Skip className="h-4 w-4 mr-2" />
          Skip
          <ArrowRight className="h-4 w-4 ml-2" />
        </Button>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-12 relative z-10">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="flex items-center justify-center mb-6">
            <div className="relative">
              <div className="w-16 h-16 bg-gradient-to-br from-pink-500 via-purple-500 to-blue-500 rounded-3xl flex items-center justify-center shadow-lg shadow-purple-500/25">
                <Sparkles className="h-8 w-8 text-white animate-pulse" />
              </div>
              <div className="absolute -top-2 -right-2 w-6 h-6 bg-green-400 rounded-full border-2 border-slate-950 animate-pulse" />
            </div>
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-pink-400 via-purple-400 to-blue-400 bg-clip-text text-transparent mb-4">
            AdMorph.AI
          </h1>
          <p className="text-xl text-purple-300 font-medium">Voice setup for your campaign</p>
          <p className="text-slate-400 mt-2">Every audience. One engine.</p>
        </div>

        {/* Step-by-step at the top */}
        <div className="mb-20">
          <div className="flex justify-center">
            <div className="grid grid-cols-5 gap-8 max-w-2xl w-full">
              {agentSteps.map((step, index) => (
                <div key={step.id} className="flex flex-col items-center">
                  <div
                    className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-500 shadow-lg ${
                      step.status === "completed"
                        ? "bg-gradient-to-r from-green-400 to-emerald-500 text-white scale-110 shadow-green-500/25"
                        : step.status === "active"
                          ? "bg-gradient-to-r from-pink-500 to-purple-600 text-white animate-pulse scale-110 shadow-purple-500/25"
                          : "bg-slate-800/50 text-slate-500 backdrop-blur-sm border border-slate-700/50"
                    }`}
                  >
                    {step.status === "completed" ? (
                      <CheckCircle className="h-6 w-6" />
                    ) : step.status === "active" ? (
                      <Loader2 className="h-6 w-6 animate-spin" />
                    ) : (
                      <span className="text-sm font-bold">{index + 1}</span>
                    )}
                  </div>
                  <p className="text-sm text-slate-400 mt-3 font-medium text-center">{step.name}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Voice Recording - Main Focus */}
        <div className="flex justify-center mb-20">
          <Card className="bg-slate-900/50 backdrop-blur-xl border-purple-500/20 shadow-2xl shadow-purple-500/10 rounded-3xl p-16 max-w-2xl w-full relative overflow-hidden">
            {/* Card Background Effects */}
            <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 via-pink-500/5 to-blue-500/5" />
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-pink-500 via-purple-500 to-blue-500" />

            <div className="text-center relative">
              <h2 className="text-2xl font-bold text-white mb-8">{questions[currentStep]}</h2>

              {/* Enhanced Waveform */}
              <div className="flex items-center justify-center space-x-1 h-24 mb-12">
                {audioLevels.map((level, index) => (
                  <div
                    key={index}
                    className={`w-1.5 rounded-full transition-all duration-200 ${
                      voiceState === "listening"
                        ? "bg-gradient-to-t from-pink-500 to-purple-500 shadow-sm shadow-purple-500/50"
                        : "bg-slate-600"
                    }`}
                    style={{ height: `${level}px` }}
                  />
                ))}
              </div>

              {/* Enhanced Microphone Button */}
              <Button
                size="lg"
                onClick={voiceState === "listening" ? stopListening : startListening}
                disabled={voiceState === "processing"}
                className={`w-28 h-28 rounded-full shadow-2xl transition-all duration-500 mb-8 ${
                  voiceState === "listening"
                    ? "bg-gradient-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700 shadow-red-500/25 scale-110"
                    : "bg-gradient-to-r from-pink-500 via-purple-600 to-blue-600 hover:from-pink-600 hover:via-purple-700 hover:to-blue-700 shadow-purple-500/25 hover:scale-110"
                }`}
              >
                {voiceState === "listening" ? (
                  <MicOff className="h-12 w-12 text-white" />
                ) : (
                  <Mic className="h-12 w-12 text-white" />
                )}
              </Button>

              <p className="text-lg text-slate-300 mb-6 font-medium">
                {voiceState === "idle" && "Tap to speak"}
                {voiceState === "listening" && "Listening..."}
                {voiceState === "processing" && "Processing..."}
              </p>

              {currentTranscript && (
                <div className="p-6 bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700/50">
                  <p className="text-slate-200 italic text-lg">"{currentTranscript}"</p>
                </div>
              )}
            </div>
          </Card>
        </div>

        {/* Upload Section - After voice */}
        {currentStep >= 4 && (
          <div className="flex justify-center">
            <Card className="bg-slate-900/50 backdrop-blur-xl border-orange-500/20 shadow-xl shadow-orange-500/10 rounded-2xl p-10 max-w-md w-full relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-orange-500/5 to-yellow-500/5" />
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-orange-500 to-yellow-500" />

              <div className="text-center relative">
                <div className="w-16 h-16 bg-gradient-to-r from-orange-500 to-yellow-500 rounded-2xl mx-auto mb-6 flex items-center justify-center shadow-lg shadow-orange-500/25">
                  <Upload className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-bold text-white mb-3">Upload Your Ad</h3>
                <p className="text-slate-400 mb-6">Add your current creative</p>

                <div className="relative">
                  <input
                    type="file"
                    accept="image/*,video/*"
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    onChange={(e) => {
                      const file = e.target.files?.[0]
                      if (file) {
                        setBusinessData((prev) => ({ ...prev, originalAd: file }))
                      }
                    }}
                  />
                  <Button
                    variant="outline"
                    className="w-full bg-slate-800/50 border-slate-600 text-slate-300 hover:bg-slate-700/50 hover:text-white rounded-xl py-3"
                  >
                    Choose File
                  </Button>
                </div>
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}
