"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { SendHorizontal, Mic, MicOff } from "lucide-react"
import useWhisperTranscription from "@/lib/hooks/useWhisperTranscription"

interface ProductInfo {
  productName: string;
  uniqueElements: string[];
  visualStyle: {
    include: string[];
    avoid: string[];
  };
}

type ConversationStage = 
  | "initial" // Opening greeting
  | "exploring" // General exploration of the product
  | "name_focus" // Specifically trying to get the name
  | "elements_focus" // Specifically asking about unique elements
  | "style_focus" // Asking about visual style preferences
  | "summary" // Summarizing what we've learned
  | "complete" // Conversation complete

export default function ProductVisAgent() {
  // Chat state
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([{
      role: "ai",
      content: "Hey! I'd love to get a feel for your product so we can bring it to life visually. Just describe it however feels natural."
    }])
  const [userInput, setUserInput] = useState("")
  const [isThinking, setIsThinking] = useState(false)
  
  // Voice recording state
  const [isListening, setIsListening] = useState(false)
  
  // Product information tracking
  const [productInfo, setProductInfo] = useState<ProductInfo>({
    productName: "",
    uniqueElements: [],
    visualStyle: {
      include: [],
      avoid: []
    }
  })
  
  // Conversation flow control
  const [stage, setStage] = useState<ConversationStage>("initial")
  const [questionCount, setQuestionCount] = useState(0)
  const messageEndRef = useRef<HTMLDivElement>(null)
  
  // Whisper transcription hook
  const { 
    isRecording, 
    isTranscribing, 
    startRecording, 
    stopRecording, 
    error: transcriptionError 
  } = useWhisperTranscription({
    onTranscriptionStart: () => {
      setIsThinking(true);
    },
    onTranscriptionComplete: (transcript) => {
      if (transcript && transcript.trim()) {
        // Process the transcribed text as user input
        processUserInput(transcript);
        
        // Add the transcript as a user message
        setMessages(prev => [...prev, { role: "user", content: transcript }]);
        
        // Generate AI response
        setTimeout(() => {
          const aiResponse = generateResponse();
          setMessages(prev => [...prev, { role: "ai", content: aiResponse }]);
          setIsThinking(false);
        }, 1000);
      } else {
        setIsThinking(false);
        // If transcript is empty, show an error message
        setMessages(prev => [
          ...prev, 
          { 
            role: "system", 
            content: "I couldn't hear what you said. Could you please try again?" 
          }
        ]);
      }
      
      // Update listening state
      setIsListening(false);
    },
    onTranscriptionError: (error) => {
      console.error("Transcription error:", error);
      setMessages(prev => [
        ...prev, 
        { 
          role: "system", 
          content: `Voice transcription error: ${error.message}. Please try typing instead.` 
        }
      ]);
      setIsThinking(false);
      setIsListening(false);
    }
  })
  
  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])
  
  // Handler for user messages
  const handleUserMessage = () => {
    if (!userInput.trim()) return
    
    // Add user message
    setMessages(prev => [...prev, { role: "user", content: userInput }])
    
    // Process the user's input
    processUserInput(userInput)
    
    // Clear input
    setUserInput("")
    
    // Show thinking state
    setIsThinking(true)
    
    // Generate AI response after a short delay for natural feel
    setTimeout(() => {
      const aiResponse = generateResponse()
      setMessages(prev => [...prev, { role: "ai", content: aiResponse }])  
      setIsThinking(false)
    }, 1000)
  }
  
  // Toggle voice recording
  const toggleRecording = () => {
    if (isRecording) {
      stopRecording()
      setIsListening(false)
    } else {
      setIsListening(true)
      startRecording()
    }
  }
  
  // Process user input to extract product information
  const processUserInput = (input: string) => {
    const lowerInput = input.toLowerCase()
    
    // Try to extract product name if we don't have it yet
    if (!productInfo.productName) {
      // Look for patterns like "my product is called X" or "it's an X called Y"
      const namePatterns = [
        /(?:called|named)\s+["']?([\w\s]+)["']?/i,
        /it(?:'s| is) (?:a|an)\s+([\w\s]+)/i,
        /(?:our|my|the)\s+([\w\s]+)(?:\s+is|\s+that)/i
      ]
      
      for (const pattern of namePatterns) {
        const match = lowerInput.match(pattern)
        if (match && match[1]) {
          // Found a potential product name
          setProductInfo(prev => ({
            ...prev,
            productName: match[1].trim()
          }))
          break
        }
      }
    }
    
    // Extract unique elements
    const elementKeywords = ['feature', 'unique', 'special', 'innovative', 'different', 'standout']
    if (elementKeywords.some(keyword => lowerInput.includes(keyword))) {
      const extractedElements = input
        .split(/[,.]/) // Split by commas or periods
        .filter(item => 
          elementKeywords.some(keyword => 
            item.toLowerCase().includes(keyword)
          )
        )
        .map(item => item.trim())
        
      if (extractedElements.length > 0) {
        setProductInfo(prev => ({
          ...prev,
          uniqueElements: [...prev.uniqueElements, ...extractedElements]
        }))
      }
    }
    
    // Look for visual style preferences
    const styleKeywords = ['style', 'look', 'design', 'aesthetic', 'visual', 'appearance']
    const avoidKeywords = ['avoid', 'don\'t', 'not', 'never']
    
    if (styleKeywords.some(keyword => lowerInput.includes(keyword))) {
      // Check if this is something to avoid
      const isAvoid = avoidKeywords.some(keyword => lowerInput.includes(keyword))
      
      // Extract style descriptions
      const styleDescription = input.trim()
      
      if (isAvoid) {
        setProductInfo(prev => ({
          ...prev,
          visualStyle: {
            ...prev.visualStyle,
            avoid: [...prev.visualStyle.avoid, styleDescription]
          }
        }))
      } else {
        setProductInfo(prev => ({
          ...prev,
          visualStyle: {
            ...prev.visualStyle,
            include: [...prev.visualStyle.include, styleDescription]
          }
        }))
      }
    }
  }
  
  // Generate appropriate AI response based on conversation stage
  const generateResponse = () => {
    // Increment question counter
    if (stage !== "summary" && stage !== "complete") {
      setQuestionCount(prev => prev + 1)
    }
    
    // Don't ask more than 5 questions total
    if (questionCount >= 5) {
      setStage("summary")
    }
  
    // Determine next stage based on current stage and product info
    switch (stage) {
      case "initial":
        if (productInfo.productName) {
          setStage("exploring")
          return "Great, thanks for sharing the name! Can you tell me more about what makes your product unique?"
        } else {
          setStage("name_focus")
          return "I didn't quite catch the name. Could you please tell me what your product is called?"
        }
      case "name_focus":
        if (productInfo.productName) {
          setStage("exploring")
          return "Thanks for sharing the name! Can you tell me more about what makes your product unique?"
        } else {
          return "I still didn't quite catch the name. Could you please tell me what your product is called?"
        }
      case "exploring":
        if (productInfo.uniqueElements.length > 0) {
          setStage("elements_focus")
          return "That's really interesting. Can you tell me more about what makes those elements unique?"
        } else {
          return "What makes your product stand out from the competition?"
        }
      case "elements_focus":
        if (productInfo.visualStyle.include.length > 0 || productInfo.visualStyle.avoid.length > 0) {
          setStage("style_focus")
          return "Great, thanks for sharing that! What kind of visual style are you aiming for with your product?"
        } else {
          return "Can you tell me more about what makes those elements unique?"
        }
      case "style_focus":
        if (productInfo.visualStyle.include.length > 0 || productInfo.visualStyle.avoid.length > 0) {
          setStage("summary")
          return "Great, thanks for sharing that! Let me summarize what I've learned so far..."
        } else {
          return "What kind of visual style are you aiming for with your product?"
        }
      case "summary":
        setStage("complete")
        return "Great, thanks for chatting with me! I think I have a good understanding of your product now."
      case "complete":
        return "It was great chatting with you! If you want to simulate another conversation, feel free to refresh the page."
      default:
        return "I'm not sure what to say next. Could you please try again?"
    }
  }
  
  // Generate a summary of collected information for the final stage
  const generateSummary = () => {
    let summary = "Here's what I've learned about your product:\n\n"
    
    if (productInfo.productName) {
      summary += `📝 Product Name: ${productInfo.productName}\n\n`
    } else {
      summary += "📝 Product Name: Not specified\n\n"
    }
    
    summary += "✨ Unique Elements:\n"
    if (productInfo.uniqueElements.length > 0) {
      productInfo.uniqueElements.forEach((element, i) => {
        summary += `${i + 1}. ${element}\n`
      })
    } else {
      summary += "- No specific unique elements identified\n"
    }
    summary += "\n"
    
    summary += "🎨 Visual Style Preferences:\n"
    if (productInfo.visualStyle.include.length > 0) {
      summary += "Include:\n"
      productInfo.visualStyle.include.forEach((style, i) => {
        summary += `- ${style}\n`
      })
    }
    
    if (productInfo.visualStyle.avoid.length > 0) {
      summary += "\nAvoid:\n"
      productInfo.visualStyle.avoid.forEach((style, i) => {
        summary += `- ${style}\n`
      })
    }
    
    if (productInfo.visualStyle.include.length === 0 && productInfo.visualStyle.avoid.length === 0) {
      summary += "- No specific style preferences identified\n"
    }
    
    return summary
  }
  
  return (
    <div className="container mx-auto max-w-2xl h-[600px] bg-white rounded-xl shadow-lg flex flex-col p-4">
      {/* Header */}
      <div className="py-3 px-4 border-b border-gray-200">
        <h2 className="text-lg font-medium text-gray-800">Product Visualization Assistant</h2>
        <p className="text-sm text-gray-500">I'll help understand your product for visualization</p>
      </div>
      
      {/* Chat messages */}
      <div className="flex-1 overflow-auto py-4 px-3 space-y-4">
        {messages.map((message, index) => (
          <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div 
              className={`max-w-[80%] rounded-lg p-3 ${
                message.role === 'user' ? 'bg-indigo-500 text-white' : 'bg-gray-100 text-gray-800'
              } ${message.role !== 'user' && stage === 'summary' && index === messages.length - 1 ? 'whitespace-pre-line' : ''}`}
            >
              {message.role !== 'user' && stage === 'summary' && index === messages.length - 1 
                ? generateSummary() 
                : message.content
              }
            </div>
          </div>
        ))}
        {isThinking && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-800 rounded-lg p-3 max-w-[80%] flex items-center">
              <span className="flex space-x-1">
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </span>
            </div>
          </div>
        )}
        <div ref={messageEndRef} />
      </div>
      
      {/* Progress indicator */}
      {questionCount <= 5 && stage !== "complete" && (
        <div className="px-4 mt-2 mb-3">
          <div className="flex justify-between text-xs text-gray-500 mb-1">
            <span>Questions asked</span>
            <span>{questionCount}/5</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-1">
            <div 
              className="bg-indigo-500 h-1 rounded-full transition-all duration-300"
              style={{ width: `${(questionCount / 5) * 100}%` }}
            />
          </div>
        </div>
      )}
      
      {/* Input area */}
      <div className="p-3 border-t border-gray-200">
        <div className="flex gap-2">
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleUserMessage()}
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            placeholder={isRecording ? "Listening..." : "Type your response..."}
            disabled={stage === "complete" || isRecording}
          />
          {/* Voice input button */}
          <Button
            onClick={toggleRecording}
            className={`${isRecording ? "bg-red-500 hover:bg-red-600" : "bg-blue-500 hover:bg-blue-600"} text-white`}
            disabled={stage === "complete" || isTranscribing || isThinking}
            title={isRecording ? "Stop recording" : "Start recording"}
          >
            {isRecording ? (
              <MicOff className="h-5 w-5" />
            ) : (
              <Mic className="h-5 w-5" />
            )}
          </Button>
          {/* Send button */}
          <Button 
            onClick={handleUserMessage}
            className="bg-indigo-500 hover:bg-indigo-600 text-white"
            disabled={userInput.trim() === '' || stage === "complete" || isThinking || isRecording}
          >
            <SendHorizontal className="h-5 w-5" />
          </Button>
        </div>
        
        {stage === "complete" && (
          <div className="mt-3 text-center">
            <p className="text-sm text-gray-500">This conversation is complete.</p>
            <Button 
              onClick={() => window.location.reload()}
              className="mt-2 bg-indigo-100 text-indigo-700 hover:bg-indigo-200"
            >
              Start New Conversation
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}
