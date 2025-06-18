"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Heart, X, RotateCcw, Check, Loader2, Sparkles } from "lucide-react"

interface BusinessData {
  targetEngagement: string
  budget: string
  audience: string
  themes: string[]
}

interface AdGalleryProps {
  businessData: BusinessData
  onSelectionComplete: (selectedAds: string[]) => void
  onAdPerformanceView?: (adId: string) => void
}

interface AdVariant {
  id: string
  title: string
  demographic: string
  interests: string[]
  imageUrl: string
  description: string
  estimatedCTR: number
  confidence: number
  audienceSize: string
}

export default function AdGallery({ businessData, onSelectionComplete, onAdPerformanceView }: AdGalleryProps) {
  const [selectedAds, setSelectedAds] = useState<string[]>([])
  const [currentAdIndex, setCurrentAdIndex] = useState(0)
  const [viewMode, setViewMode] = useState<"swipe" | "gallery">("swipe")
  const [isGenerating, setIsGenerating] = useState(false)
  const [cardTransform, setCardTransform] = useState({ x: 0, y: 0, rotate: 0 })

  const adVariants: AdVariant[] = [
    {
      id: "1",
      title: "Young Professional Focus",
      demographic: "Ages 25-35, Urban Professionals",
      interests: ["Career Growth", "Technology", "Productivity"],
      imageUrl: "/placeholder.svg?height=600&width=400",
      description: "Modern design targeting career-focused millennials",
      estimatedCTR: 3.2,
      confidence: 94,
      audienceSize: "2.4M",
    },
    {
      id: "2",
      title: "Family-Oriented Appeal",
      demographic: "Ages 30-45, Suburban Families",
      interests: ["Family", "Home", "Education"],
      imageUrl: "/placeholder.svg?height=600&width=400",
      description: "Warm, family-friendly messaging with trust elements",
      estimatedCTR: 2.8,
      confidence: 89,
      audienceSize: "1.8M",
    },
    {
      id: "3",
      title: "Gen Z Engagement",
      demographic: "Ages 18-25, Digital Natives",
      interests: ["Social Media", "Trends", "Gaming"],
      imageUrl: "/placeholder.svg?height=600&width=400",
      description: "Bold, trendy design with viral potential",
      estimatedCTR: 4.1,
      confidence: 91,
      audienceSize: "3.1M",
    },
    {
      id: "4",
      title: "Premium Segment",
      demographic: "Ages 35-55, High Income",
      interests: ["Luxury", "Quality", "Exclusivity"],
      imageUrl: "/placeholder.svg?height=600&width=400",
      description: "Sophisticated design emphasizing premium quality",
      estimatedCTR: 2.5,
      confidence: 96,
      audienceSize: "890K",
    },
  ]

  const handleSwipeAction = (action: "like" | "dislike" | "regenerate") => {
    const currentAd = adVariants[currentAdIndex]

    if (action === "like") {
      setCardTransform({ x: 300, y: -50, rotate: 15 })
      setSelectedAds((prev) => [...prev, currentAd.id])
    } else if (action === "dislike") {
      setCardTransform({ x: -300, y: -50, rotate: -15 })
    } else if (action === "regenerate") {
      setIsGenerating(true)
      setTimeout(() => setIsGenerating(false), 2000)
      return
    }

    setTimeout(() => {
      setCardTransform({ x: 0, y: 0, rotate: 0 })
      if (currentAdIndex < adVariants.length - 1) {
        setCurrentAdIndex((prev) => prev + 1)
      } else {
        setViewMode("gallery")
      }
    }, 300)
  }

  const toggleAdSelection = (adId: string) => {
    setSelectedAds((prev) => (prev.includes(adId) ? prev.filter((id) => id !== adId) : [...prev, adId]))
  }

  const handleComplete = () => {
    onSelectionComplete(selectedAds)
  }

  if (viewMode === "swipe" && currentAdIndex < adVariants.length) {
    const currentAd = adVariants[currentAdIndex]

    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 relative overflow-hidden">
        {/* Minimal Background Effects */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/10 via-transparent to-pink-900/10" />
        <div className="absolute top-1/3 left-1/2 transform -translate-x-1/2 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl animate-pulse" />

        <div className="max-w-2xl mx-auto px-6 py-16 relative z-10">
          {/* Minimal Header */}
          <div className="text-center mb-16">
            <h1 className="text-4xl font-light bg-gradient-to-r from-white via-purple-200 to-pink-200 bg-clip-text text-transparent mb-4">
              Review Your Ads
            </h1>
            <div className="inline-flex items-center space-x-2 bg-slate-900/50 backdrop-blur-xl rounded-full px-4 py-2">
              <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
              <span className="text-sm text-slate-300">
                {currentAdIndex + 1} of {adVariants.length}
              </span>
            </div>
          </div>

          {/* Clean Ad Card */}
          <div className="flex justify-center mb-16">
            <Card
              className={`relative w-full max-w-sm bg-slate-900/40 backdrop-blur-2xl border-slate-700/30 shadow-2xl rounded-3xl overflow-hidden transition-all duration-300 ${
                isGenerating ? "opacity-75 scale-95" : "opacity-100 scale-100"
              }`}
              style={{
                transform: `translateX(${cardTransform.x}px) translateY(${cardTransform.y}px) rotate(${cardTransform.rotate}deg)`,
                transition: cardTransform.x !== 0 ? "transform 0.3s ease-out" : "transform 0.3s ease-in-out",
              }}
            >
              {/* Clean Ad Image */}
              <div className="relative h-96">
                <img
                  src={currentAd.imageUrl || "/placeholder.svg"}
                  alt={currentAd.title}
                  className="w-full h-full object-cover"
                />

                {/* Minimal Overlay Info */}
                <div className="absolute top-4 left-4 right-4 flex justify-between">
                  <Badge className="bg-slate-900/80 backdrop-blur-sm text-white border-0 rounded-full px-3 py-1">
                    {currentAd.estimatedCTR}% CTR
                  </Badge>
                  <Badge className="bg-green-500/90 backdrop-blur-sm text-white border-0 rounded-full px-3 py-1">
                    {currentAd.confidence}% Match
                  </Badge>
                </div>

                {isGenerating && (
                  <div className="absolute inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center">
                    <div className="bg-slate-900/90 backdrop-blur-xl rounded-2xl p-6 shadow-xl">
                      <Loader2 className="h-8 w-8 animate-spin text-purple-400 mx-auto mb-3" />
                      <p className="text-sm font-medium text-white">Optimizing...</p>
                    </div>
                  </div>
                )}
              </div>

              {/* Minimal Content */}
              <CardContent className="p-8">
                <h3 className="text-xl font-semibold text-white mb-2">{currentAd.title}</h3>
                <p className="text-slate-400 mb-6">{currentAd.description}</p>

                <div className="flex items-center justify-between text-sm text-slate-400">
                  <span>{currentAd.demographic}</span>
                  <span>{currentAd.audienceSize} reach</span>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Clean Action Buttons */}
          <div className="flex justify-center space-x-8">
            <Button
              variant="ghost"
              size="lg"
              onClick={() => handleSwipeAction("dislike")}
              disabled={isGenerating}
              className="w-16 h-16 rounded-full bg-slate-900/40 backdrop-blur-xl border border-red-500/20 hover:border-red-500/40 hover:bg-red-500/10 transition-all duration-300"
            >
              <X className="h-6 w-6 text-red-400" />
            </Button>

            <Button
              variant="ghost"
              size="lg"
              onClick={() => handleSwipeAction("regenerate")}
              disabled={isGenerating}
              className="w-16 h-16 rounded-full bg-slate-900/40 backdrop-blur-xl border border-orange-500/20 hover:border-orange-500/40 hover:bg-orange-500/10 transition-all duration-300"
            >
              <RotateCcw className="h-6 w-6 text-orange-400" />
            </Button>

            <Button
              variant="ghost"
              size="lg"
              onClick={() => handleSwipeAction("like")}
              disabled={isGenerating}
              className="w-16 h-16 rounded-full bg-slate-900/40 backdrop-blur-xl border border-green-500/20 hover:border-green-500/40 hover:bg-green-500/10 transition-all duration-300"
            >
              <Heart className="h-6 w-6 text-green-400" />
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 relative overflow-hidden">
      {/* Clean Background */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/10 via-transparent to-pink-900/10" />

      <div className="max-w-5xl mx-auto px-6 py-16 relative z-10">
        {/* Clean Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-light bg-gradient-to-r from-white via-purple-200 to-pink-200 bg-clip-text text-transparent mb-4">
            Your Ad Gallery
          </h1>
          <div className="inline-flex items-center space-x-2 bg-slate-900/50 backdrop-blur-xl rounded-full px-4 py-2">
            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
            <span className="text-sm text-slate-300">{selectedAds.length} ads selected</span>
          </div>
        </div>

        {/* Clean Ad Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
          {adVariants.map((ad) => (
            <Card
              key={ad.id}
              className={`cursor-pointer transition-all duration-500 bg-slate-900/40 backdrop-blur-2xl border-slate-700/30 shadow-xl hover:shadow-2xl rounded-3xl overflow-hidden group ${
                selectedAds.includes(ad.id) ? "ring-2 ring-purple-500/50 scale-105" : "hover:scale-102"
              }`}
              onClick={() => toggleAdSelection(ad.id)}
            >
              <div className="relative">
                <img src={ad.imageUrl || "/placeholder.svg"} alt={ad.title} className="w-full h-64 object-cover" />
                {selectedAds.includes(ad.id) && (
                  <div className="absolute top-4 right-4 w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center shadow-lg">
                    <Check className="h-5 w-5 text-white" />
                  </div>
                )}
                <div className="absolute top-4 left-4">
                  <Badge className="bg-slate-900/80 backdrop-blur-sm text-white border-0 rounded-full">
                    {ad.estimatedCTR}% CTR
                  </Badge>
                </div>
              </div>

              <CardContent className="p-6">
                <h3 className="font-semibold text-white mb-2">{ad.title}</h3>
                <p className="text-sm text-slate-400 mb-4">{ad.demographic}</p>

                <Button
                  variant="outline"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation()
                    onAdPerformanceView?.(ad.id)
                  }}
                  className="w-full bg-slate-800/50 backdrop-blur-sm border-slate-600/50 text-slate-300 hover:bg-slate-700/50 hover:text-white rounded-xl"
                >
                  View Performance
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Clean Launch Button */}
        <div className="text-center">
          <Button
            onClick={handleComplete}
            disabled={selectedAds.length === 0}
            size="lg"
            className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-2xl px-12 py-4 text-lg font-medium shadow-xl shadow-purple-500/25 transition-all duration-300 hover:scale-105 disabled:opacity-50 disabled:scale-100"
          >
            <Sparkles className="h-5 w-5 mr-2" />
            Launch {selectedAds.length} Selected Ads
          </Button>
        </div>
      </div>
    </div>
  )
}
