"use client"

import { useState, useEffect, useCallback, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Mic, MicOff, Upload, SkipBackIcon as Skip, ArrowRight, CheckCircle, Loader2, Sparkles, Volume2, VolumeX } from "lucide-react"
import useVoiceRecorder from "@/lib/hooks/useVoiceRecorder"
import useVoice from "@/lib/hooks/useVoice"
import speechRecognition from "@/lib/speech-recognition"

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
  const [isNarrationEnabled, setIsNarrationEnabled] = useState(true)
  
  // Voice recorder hook
  const {
    isRecording,
    isPermissionGranted,
    audioUrl,
    start: startRecording,
    stop: stopRecording,
    reset: resetRecording,
  } = useVoiceRecorder({
    onAudioLevels: setAudioLevels,
    onStop: (audioUrl, blob) => {
      // Here we would normally send the blob to a transcription service
      // For now we'll simulate it with a timeout
      handleRecordingComplete();
    },
  })
  
  // Unified voice system hook (supports both Eleven Labs and Dia)
  const {
    isSpeaking,
    speak,
    stop: stopSpeaking,
    error: voiceError
  } = useVoice()

  const [agentSteps, setAgentSteps] = useState<AgentStep[]>([
    { id: "1", name: "Requirements", status: "pending" },
    { id: "2", name: "Audience", status: "pending" },
    { id: "3", name: "Creative", status: "pending" },
    { id: "4", name: "Optimize", status: "pending" },
    { id: "5", name: "Ready", status: "pending" },
  ])

  // Enhanced sales conversation with more natural, engaging dialogue
  const conversationFlow = [
    {
      id: "intro",
      agent: "Hi there! I'm Emma from AdMorph AI. I help businesses create more effective advertising campaigns. I'd love to learn about your goals so we can craft the perfect ad strategy for you. What specific engagement metrics are you hoping to improve with your next campaign?",
      shortPrompt: "What's your target engagement goal?",
      expectedResponseType: "engagement",
    },
    {
      id: "budget",
      agent: "That's a great goal! To help us tailor our recommendations, could you share what kind of monthly budget you're working with for this campaign?",
      shortPrompt: "What's your advertising budget?",
      expectedResponseType: "budget",
    },
    {
      id: "audience",
      agent: "Perfect, thanks for sharing that. Now, let's make sure we're targeting the right people. Could you tell me a bit about your ideal customer? Who are you trying to reach with these ads?",
      shortPrompt: "Who is your target audience?",
      expectedResponseType: "audience",
    },
    {
      id: "themes",
      agent: "That's exactly the information we need! Now I have one more question about your brand style. Are there specific themes, colors, or messaging elements you'd like to maintain across all your ad creative?",
      shortPrompt: "What themes should we maintain?",
      expectedResponseType: "themes",
    },
    {
      id: "finalize",
      agent: "Fantastic! Based on everything you've shared, we have all we need to create a campaign that will really resonate with your audience. Would you like us to generate some ad concepts for you now?",
      shortPrompt: "Ready to generate your ads?",
      expectedResponseType: "confirmation",
    },
  ]
  
  // Simplified access to just the questions when needed
  const questions = conversationFlow.map(item => item.shortPrompt)

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

  // Generate waveform with more natural voice-like patterns
  const generateWaveform = () => {
    // Create a more natural voice pattern with higher middle values
    const baseValues = Array.from({ length: 20 }, (_, i) => {
      // Create a bell curve effect with higher values in the middle
      const distFromCenter = Math.abs(i - 10)
      const base = 30 - distFromCenter * 2
      // Add some randomness
      return base + (Math.random() * 15)
    })
    
    return baseValues
  }

  // Handle recording completion and process transcription
  const handleRecordingComplete = () => {
    setVoiceState("processing")
    
    // Update agent step
    setAgentSteps((prev) =>
      prev.map((step, index) => ({
        ...step,
        status: index === currentStep ? "active" : index < currentStep ? "completed" : "pending",
      })),
    )

    // We'll rely on real transcription or the mock transcription service
    // Show a loading state briefly to simulate processing
    setTimeout(() => {
      // If no transcript was received yet, use a fallback
      if (!currentTranscript) {
        const fallbackResponses = [
          "Increase click-through rate by 25%",
          "$8,000 per month",
          "Young professionals aged 25-35",
          "Modern, professional tone",
          "Yes, let's generate!",
        ]

        const fallbackResponse = fallbackResponses[currentStep] || "Ready"
        setCurrentTranscript(fallbackResponse)
        handleVoiceInput(fallbackResponse)
      } else {
        // Use the transcript that was already captured during listening
        handleVoiceInput(currentTranscript)
      }
    }, 1000)
  }

  // Start listening with real recording
  const startListening = async () => {
    setVoiceState("listening")
    setCurrentTranscript("")
    
    try {
      if (speechRecognition && speechRecognition.isSupported()) {
        speechRecognition.start({
          continuous: true,
          interimResults: true,
          lang: "en-US",
          onResult: (transcript, isFinal) => {
            // Update state with the latest transcript
            setCurrentTranscript(transcript)
            
            // Visual feedback as user speaks
            const levels = generateWaveform()
            setAudioLevels(levels)
            
            if (isFinal) {
              stopListening()
            }
          },
          onError: (error) => {
            console.error("Speech recognition error:", error)
            stopListening()
          }
        })
      } else {
        // Fallback - start recording via basic voice recorder
        startRecording()
      }
    } catch (error) {
      console.error("Error starting speech recognition:", error)
      // Fallback to simple recording
      startRecording()
    }
  }

  const handleVoiceInput = (transcript: string) => {
    // Store the response in the appropriate field based on current step
    const updatedData = { ...businessData }
    
    // Process voice response based on current step
    switch (currentStep) {
      case 0: // Target Engagement
        updatedData.targetEngagement = transcript
        break
        
      case 1: // Budget
        updatedData.budget = transcript
        break
        
      case 2: // Audience
        updatedData.audience = transcript
        break
        
      case 3: // Themes
        updatedData.themes = transcript.split(",").map(theme => theme.trim())
        break
        
      case 4: // Final confirmation
        // Add acknowledgment response
        setTimeout(() => {
          // Final acknowledgment before completing
          if (isNarrationEnabled) {
            speak({ 
              text: "Excellent! I'll create some amazing ad concepts based on your requirements. Let's make your campaign a success!"
            })
          }
          
          // Wait for voice to finish before completing
          setTimeout(() => {
            onComplete(updatedData)
          }, 3000)
        }, 500)
        return
    }
    
    setBusinessData(updatedData)
    
    // Update the agent steps
    setAgentSteps(prev => 
      prev.map((step, index) => ({
        ...step,
        status: index === currentStep ? "completed" : 
                index === currentStep + 1 ? "active" : 
                index < currentStep ? "completed" : "pending"
      }))
    )
    
    // Provide confirmation of the user's answer before moving to next question
    const confirmationResponses = [
      `Great! A ${updatedData.targetEngagement} goal is ambitious but achievable with the right strategy.`,
      `Perfect! A budget of ${updatedData.budget} will give us good flexibility for your campaign.`,
      `Excellent! We'll make sure your ads really connect with ${updatedData.audience}.`,
      `Those are fantastic themes to work with! We'll make sure your brand identity shines through.`,
    ]
    
    if (isNarrationEnabled && currentStep < 4) {
      // Speak confirmation of current answer
      setTimeout(() => {
        speak({ text: confirmationResponses[currentStep] })
      }, 500)
    }
    
    // Move to next step after acknowledgment
    setTimeout(() => {
      setCurrentStep(prevStep => prevStep + 1)
      setVoiceState("idle")
      setCurrentTranscript("")
      
      // Speak the next question after a delay for a more natural conversation flow
      setTimeout(() => {
        speakQuestion(currentStep + 1)
      }, 1500) // Longer delay for more natural conversation pace
    }, 3500) // Wait longer to allow for confirmation speech
  }

  const stopListening = () => {
    setVoiceState("idle")
    stopRecording()
    if (speechRecognition && speechRecognition.isSupported()) {
      speechRecognition.stop()
    }
    setAudioLevels(new Array(20).fill(5))
  }

  // Speak the current part of the conversation using the configured voice system
  const speakQuestion = useCallback((stepIndex: number) => {
    if (isNarrationEnabled && conversationFlow[stepIndex]) {
      // Use the full conversational prompt instead of just the short question
      speak({ text: conversationFlow[stepIndex].agent })
    }
  }, [isNarrationEnabled, conversationFlow, speak])

  // Toggle narration on/off
  const toggleNarration = () => {
    if (isSpeaking) {
      stopSpeaking()
    }
    setIsNarrationEnabled(!isNarrationEnabled)
  }

  // Effect to initialize audio levels
  useEffect(() => {
    setAudioLevels(new Array(20).fill(5))
  }, [])
  
  // Track initial render using ref to prevent repeated execution
  const initialRender = useRef(true);
  
  // Separate effect to speak questions without causing infinite loops
  useEffect(() => {
    // Only run on initial render
    if (initialRender.current && currentStep === 0 && isNarrationEnabled) {
      initialRender.current = false;
      
      // Use a timeout to delay initial speech
      const timer = setTimeout(() => {
        // Call speak directly to avoid dependencies
        if (questions[0]) {
          speak({ text: questions[0] });
        }
      }, 1000);
      
      // Cleanup timer on unmount
      return () => clearTimeout(timer);
    }
  }, []) // Empty dependency array - only run once on mount

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
          
          {/* Voice AI Narration Control */}
          <div className="mt-4 inline-flex items-center gap-2 bg-slate-800/50 backdrop-blur-sm rounded-full px-4 py-2 border border-slate-700/50">
            <Button
              size="sm"
              variant="ghost"
              onClick={toggleNarration}
              className={`rounded-full ${isNarrationEnabled ? 'text-purple-400' : 'text-slate-500'}`}
            >
              {isNarrationEnabled ? 
                <Volume2 className={`h-4 w-4 ${isSpeaking ? 'animate-pulse' : ''}`} /> : 
                <VolumeX className="h-4 w-4" />
              }
            </Button>
            <span className="text-xs text-slate-400">{isNarrationEnabled ? 'AI Voice Active' : 'AI Voice Off'}</span>
          </div>
        </div>

        {/* Step-by-step at the top */}
        <div className="mb-20">
          <div className="flex justify-center">
            <div className="flex items-center space-x-8">
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
                  <p className="text-sm text-slate-400 mt-3 font-medium">{step.name}</p>
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
