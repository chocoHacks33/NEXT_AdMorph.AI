"use client"

import { useState } from "react"
import VoiceInterface from "@/components/voice-interface"
import ProcessingPanel from "@/components/processing-panel"
import AdGallery from "@/components/ad-gallery"
import AdPerformanceDashboard from "@/components/ad-performance-dashboard"
import Sidebar from "@/components/sidebar"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Sparkles } from "lucide-react"
import UploadInterface from "@/components/upload-interface"
import PerformanceTrackingDashboard from "@/components/performance-tracking-dashboard"

// Add a new step for performance tracking
type FlowStep = "chat" | "upload" | "processing" | "gallery" | "performance" | "tracking" | "final"

interface BusinessData {
  targetEngagement: string
  budget: string
  audience: string
  themes: string[]
  originalAd?: File
}

export default function AdMorphApp() {
  const [currentStep, setCurrentStep] = useState<FlowStep>("chat")
  const [businessData, setBusinessData] = useState<BusinessData>({
    targetEngagement: "",
    budget: "",
    audience: "",
    themes: [],
  })
  const [selectedAds, setSelectedAds] = useState<string[]>([])
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [selectedAdForPerformance, setSelectedAdForPerformance] = useState<string | null>(null)
  const [launchedCampaigns, setLaunchedCampaigns] = useState<
    Array<{
      id: string
      name: string
      thumbnail: string
      status: "active" | "completed"
      launchDate: Date
      selectedAds: string[]
      businessData: BusinessData
    }>
  >([])

  const handleChatComplete = (data: BusinessData) => {
    setBusinessData(data)
    setCurrentStep("upload")
  }

  const handleUploadComplete = (file?: File) => {
    if (file) {
      setBusinessData((prev) => ({ ...prev, originalAd: file }))
    }
    setCurrentStep("processing")

    setTimeout(() => {
      setCurrentStep("gallery")
    }, 6000)
  }

  // In the handleAdSelection function, change the flow to go to tracking instead of final
  const handleAdSelection = (adIds: string[]) => {
    setSelectedAds(adIds)
    setCurrentStep("tracking") // Changed from "final" to "tracking"
  }

  const handleAdPerformanceView = (adId: string) => {
    setSelectedAdForPerformance(adId)
    setCurrentStep("performance")
  }

  const resetFlow = () => {
    setCurrentStep("chat")
    setBusinessData({
      targetEngagement: "",
      budget: "",
      audience: "",
      themes: [],
    })
    setSelectedAds([])
    setSelectedAdForPerformance(null)
  }

  // Add a new handler for when tracking is complete
  const handleTrackingComplete = () => {
    // Add campaign to launched campaigns
    const newCampaign = {
      id: Date.now().toString(),
      name: `${businessData.audience.split(" ").slice(0, 2).join(" ")} Campaign`,
      thumbnail: "/placeholder.svg?height=60&width=60&text=Campaign",
      status: "completed" as const,
      launchDate: new Date(),
      selectedAds,
      businessData,
    }

    setLaunchedCampaigns((prev) => [newCampaign, ...prev])
    setCurrentStep("final")
  }

  // Show full-width for chat and upload
  const showSidebar = !["chat", "upload"].includes(currentStep)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 via-pink-950 to-slate-950 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-purple-900/20 via-slate-900/20 to-pink-900/20" />
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-pink-500/10 rounded-full blur-3xl animate-pulse delay-1000" />

      <div className="flex relative z-10">
        {/* Sidebar */}
        {showSidebar && (
          <Sidebar
            isCollapsed={sidebarCollapsed}
            onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
            launchedCampaigns={launchedCampaigns}
            onCampaignSelect={(campaignId) => {
              // Optional: Add functionality to view campaign details
              console.log("Selected campaign:", campaignId)
            }}
          />
        )}

        {/* Main Content */}
        <div className="flex-1">
          {/* Header */}
          <header className="bg-slate-950/80 backdrop-blur-xl border-b border-purple-500/20 relative">
            <div className="absolute inset-0 bg-gradient-to-r from-pink-500/5 via-purple-500/5 to-blue-500/5" />
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
              <div className="flex justify-between items-center h-20">
                <div className="flex items-center space-x-6">
                  {currentStep !== "chat" && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={resetFlow}
                      className="flex items-center space-x-2 text-purple-300 hover:text-white hover:bg-purple-500/20 rounded-xl transition-all duration-300"
                    >
                      <ArrowLeft className="h-4 w-4" />
                      <span className="font-medium">New Campaign</span>
                    </Button>
                  )}
                  <div className="flex items-center space-x-4">
                    <div className="relative">
                      <img src="/admorph-logo.png" alt="AdMorph.AI" className="h-10 w-auto" />
                      <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-pulse" />
                    </div>
                    <div>
                      <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-400 via-purple-400 to-blue-400 bg-clip-text text-transparent">
                        AdMorph.AI
                      </h1>
                      <p className="text-purple-300 text-sm">Every audience. One engine.</p>
                    </div>
                  </div>
                </div>

                {/* Progress Indicators */}
                <div className="flex items-center space-x-3">
                  {["chat", "upload", "processing", "gallery", "final"].map((step, index) => (
                    <div key={step} className="flex items-center">
                      <div
                        className={`w-3 h-3 rounded-full transition-all duration-500 ${
                          currentStep === step
                            ? "bg-gradient-to-r from-pink-500 to-purple-500 scale-125 shadow-lg shadow-purple-500/50"
                            : "bg-slate-600"
                        }`}
                      />
                      {index < 4 && <div className="w-8 h-0.5 bg-slate-600 mx-2" />}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className={`${showSidebar ? "" : "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"} py-8 relative`}>
            {currentStep === "chat" && <VoiceInterface onComplete={handleChatComplete} />}
            {currentStep === "upload" && (
              <UploadInterface businessData={businessData} onComplete={handleUploadComplete} />
            )}
            {currentStep === "processing" && <ProcessingPanel businessData={businessData} />}
            {currentStep === "gallery" && (
              <AdGallery
                businessData={businessData}
                onSelectionComplete={handleAdSelection}
                onAdPerformanceView={handleAdPerformanceView}
              />
            )}
            {currentStep === "performance" && selectedAdForPerformance && (
              <AdPerformanceDashboard adId={selectedAdForPerformance} onBack={() => setCurrentStep("gallery")} />
            )}
            {/* Add a new handler for when tracking is complete */}
            {currentStep === "tracking" && (
              <PerformanceTrackingDashboard
                selectedAds={selectedAds}
                businessData={businessData}
                onComplete={handleTrackingComplete}
              />
            )}
            {currentStep === "final" && (
              <div className="text-center py-16 max-w-4xl mx-auto px-6">
                <div className="bg-slate-900/50 backdrop-blur-xl rounded-3xl p-12 border border-purple-500/20 shadow-2xl shadow-purple-500/10 relative overflow-hidden">
                  {/* Background Effects */}
                  <div className="absolute inset-0 bg-gradient-to-br from-green-500/5 via-emerald-500/5 to-teal-500/5" />
                  <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-green-400 via-emerald-400 to-teal-400" />

                  <div className="relative">
                    <div className="w-20 h-20 bg-gradient-to-r from-green-400 via-emerald-500 to-teal-500 rounded-full flex items-center justify-center mx-auto mb-8 shadow-lg shadow-green-500/25">
                      <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <h2 className="text-4xl font-bold text-white mb-6">Campaign Successfully Launched!</h2>
                    <p className="text-xl text-slate-300 mb-10 leading-relaxed">
                      Your {selectedAds.length} selected ad variants are now live and will automatically optimize based
                      on real-time performance data.
                    </p>

                    <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 mb-10 border border-slate-700/50">
                      <h3 className="text-2xl font-bold mb-6 text-white flex items-center justify-center">
                        <Sparkles className="h-6 w-6 mr-3 text-purple-400" />
                        Campaign Summary
                      </h3>
                      <div className="grid grid-cols-2 gap-6 text-base">
                        <div className="p-4 bg-slate-700/30 rounded-xl">
                          <span className="font-bold text-purple-300">Target Audience:</span>
                          <p className="text-slate-300 mt-1">{businessData.audience}</p>
                        </div>
                        <div className="p-4 bg-slate-700/30 rounded-xl">
                          <span className="font-bold text-pink-300">Budget:</span>
                          <p className="text-slate-300 mt-1">{businessData.budget}</p>
                        </div>
                        <div className="p-4 bg-slate-700/30 rounded-xl">
                          <span className="font-bold text-blue-300">Selected Variants:</span>
                          <p className="text-slate-300 mt-1">{selectedAds.length} ads</p>
                        </div>
                        <div className="p-4 bg-slate-700/30 rounded-xl">
                          <span className="font-bold text-green-300">Auto-Optimization:</span>
                          <p className="text-slate-300 mt-1">Enabled</p>
                        </div>
                      </div>
                    </div>

                    <Button
                      onClick={resetFlow}
                      size="lg"
                      className="bg-gradient-to-r from-pink-500 via-purple-600 to-blue-600 hover:from-pink-600 hover:via-purple-700 hover:to-blue-700 text-white px-10 py-4 rounded-2xl text-lg font-bold shadow-lg shadow-purple-500/25 transition-all duration-300 hover:scale-105"
                    >
                      <Sparkles className="h-5 w-5 mr-2" />
                      Create Another Campaign
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  )
}
