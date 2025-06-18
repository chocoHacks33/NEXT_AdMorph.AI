"use client"

import type React from "react"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { motion, useMotionValue, useTransform, PanInfo } from "framer-motion"
import {
  Heart,
  X,
  RotateCcw,
  Check,
  Loader2,
  Sparkles,
  CheckCircle,
  Brain,
  Users,
  Palette,
  Target,
  Zap,
  TrendingUp,
  Eye,
  MousePointer,
  DollarSign,
  BarChart3,
} from "lucide-react"
import { useGenerationUpdates, usePerformanceMetrics } from "@/lib/websocket-client"
import { toast } from "sonner"

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
  realTimeMetrics?: {
    impressions: number
    clicks: number
    ctr: number
    conversions: number
    spend: number
    revenue: number
  }
}

interface Agent {
  id: string
  name: string
  description: string
  icon: React.ReactNode
  status: "pending" | "active" | "completed"
}

export default function AdGallery({ businessData, onSelectionComplete, onAdPerformanceView }: AdGalleryProps) {
  const [selectedAds, setSelectedAds] = useState<string[]>([])
  const [currentAdIndex, setCurrentAdIndex] = useState(0)
  const [viewMode, setViewMode] = useState<"swipe" | "gallery">("swipe")
  const [isGenerating, setIsGenerating] = useState(false)
  const [showLaunchConfirm, setShowLaunchConfirm] = useState(false)
  const [isLaunched, setIsLaunched] = useState(false)
  const [currentAgentIndex, setCurrentAgentIndex] = useState(0)
  const [adVariants, setAdVariants] = useState<AdVariant[]>([])

  // Motion values for swipe gestures
  const x = useMotionValue(0)
  const y = useMotionValue(0)
  const rotate = useTransform(x, [-200, 200], [-30, 30])
  const opacity = useTransform(x, [-200, -150, 0, 150, 200], [0, 1, 1, 1, 0])

  // WebSocket connections
  const { isConnected: generationConnected, lastMessage: generationMessage } = useGenerationUpdates()
  const { isConnected: metricsConnected, lastMessage: metricsMessage } = usePerformanceMetrics()

  // Refs
  const constraintsRef = useRef(null)

  const agents: Agent[] = [
    {
      id: "psychographic",
      name: "PsychoGrapher",
      description: "Analyzing psychological profiles",
      icon: <Brain className="h-4 w-4" />,
      status: "pending",
    },
    {
      id: "demographic",
      name: "DemoDetective",
      description: "Identifying demographics",
      icon: <Users className="h-4 w-4" />,
      status: "pending",
    },
    {
      id: "creative",
      name: "VisualVirtuoso",
      description: "Crafting creative variations",
      icon: <Palette className="h-4 w-4" />,
      status: "pending",
    },
    {
      id: "optimizer",
      name: "PerformanceProdigy",
      description: "Optimizing performance",
      icon: <Target className="h-4 w-4" />,
      status: "pending",
    },
    {
      id: "deployer",
      name: "LaunchLord",
      description: "Finalizing deployment",
      icon: <Zap className="h-4 w-4" />,
      status: "pending",
    },
  ]

  const [agentStates, setAgentStates] = useState<Agent[]>(agents)

  // Initialize ad variants with real-time metrics
  useEffect(() => {
    const initialVariants: AdVariant[] = [
    {
      id: "1",
      title: "Young Professional Focus",
      demographic: "Ages 25-35, Urban Professionals",
      interests: ["Career Growth", "Technology", "Productivity"],
      imageUrl: "/ad-young-professional.png",
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
      imageUrl: "/ad-family-oriented.png",
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
      imageUrl: "/ad-gen-z.png",
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
      imageUrl: "/ad-premium-segment.png",
      description: "Sophisticated design emphasizing premium quality",
      estimatedCTR: 2.5,
      confidence: 96,
      audienceSize: "890K",
      realTimeMetrics: {
        impressions: 0,
        clicks: 0,
        ctr: 0,
        conversions: 0,
        spend: 0,
        revenue: 0
      }
    },
  ]

  setAdVariants(initialVariants)
}, [])

// Handle generation updates
useEffect(() => {
  if (generationMessage) {
    const message = generationMessage as any

    if (message.type === 'generation_update') {
      const { status, result } = message

      if (status === 'completed' && result?.ad_variants) {
        // Update ad variants with generated data
        setAdVariants(prev => prev.map((variant, index) => ({
          ...variant,
          ...result.ad_variants[index],
          realTimeMetrics: variant.realTimeMetrics
        })))
        toast.success('New ad variants generated!')
      }
    }
  }
}, [generationMessage])

// Handle performance metrics updates
useEffect(() => {
  if (metricsMessage) {
    const message = metricsMessage as any

    if (message.type === 'performance_update') {
      const { metrics } = message

      // Update real-time metrics for ads
      setAdVariants(prev => prev.map(variant => ({
        ...variant,
        realTimeMetrics: {
          impressions: metrics.impressions || variant.realTimeMetrics?.impressions || 0,
          clicks: metrics.clicks || variant.realTimeMetrics?.clicks || 0,
          ctr: metrics.ctr || variant.realTimeMetrics?.ctr || 0,
          conversions: metrics.conversions || variant.realTimeMetrics?.conversions || 0,
          spend: metrics.spend || variant.realTimeMetrics?.spend || 0,
          revenue: metrics.revenue || variant.realTimeMetrics?.revenue || 0
        }
      })))
    }
  }
}, [metricsMessage])

  // Agent workflow animation during generation
  useEffect(() => {
    if (isGenerating) {
      setCurrentAgentIndex(0)
      setAgentStates(agents.map((agent) => ({ ...agent, status: "pending" })))

      const agentInterval = setInterval(() => {
        setCurrentAgentIndex((prev) => {
          const next = prev + 1

          setAgentStates((currentAgents) =>
            currentAgents.map((agent, index) => ({
              ...agent,
              status: index < prev ? "completed" : index === prev ? "active" : "pending",
            })),
          )

          if (next >= agents.length) {
            clearInterval(agentInterval)
            return prev
          }
          return next
        })
      }, 800)

      return () => clearInterval(agentInterval)
    }
  }, [isGenerating])

  const handleSwipeAction = (action: "like" | "dislike" | "regenerate") => {
    const currentAd = adVariants[currentAdIndex]

    if (action === "like") {
      setSelectedAds((prev) => [...prev, currentAd.id])
      toast.success(`Added "${currentAd.title}" to selection`)
    } else if (action === "dislike") {
      toast.info(`Skipped "${currentAd.title}"`)
    } else if (action === "regenerate") {
      setIsGenerating(true)
      toast.info("Regenerating ad variant...")
      setTimeout(() => setIsGenerating(false), 4000)
      return
    }

    // Move to next ad
    if (currentAdIndex < adVariants.length - 1) {
      setCurrentAdIndex((prev) => prev + 1)
      // Reset motion values
      x.set(0)
      y.set(0)
    } else {
      setViewMode("gallery")
    }
  }

  const handleDragEnd = (event: any, info: PanInfo) => {
    const threshold = 100

    if (info.offset.x > threshold) {
      // Swiped right - like
      handleSwipeAction("like")
    } else if (info.offset.x < -threshold) {
      // Swiped left - dislike
      handleSwipeAction("dislike")
    } else {
      // Snap back to center
      x.set(0)
      y.set(0)
    }
  }

  const handleLaunch = () => {
    setShowLaunchConfirm(true)
  }

  const confirmLaunch = () => {
    setIsLaunched(true)
    setShowLaunchConfirm(false)
  }

  if (viewMode === "swipe" && currentAdIndex < adVariants.length) {
    const currentAd = adVariants[currentAdIndex]

    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/10 via-transparent to-pink-900/10" />

        <div className="max-w-4xl mx-auto px-6 py-16 relative z-10">
          {/* Agent Workflow Nodes */}
          <div className="mb-12">
            <div className="flex justify-center">
              <div className="flex items-center space-x-4 max-w-4xl overflow-x-auto pb-4">
                {agentStates.map((agent, i) => (
                  <div key={agent.id} className="flex flex-col items-center min-w-0 relative">
                    {/* Connection Line */}
                    {i > 0 && (
                      <div
                        className={`
                        w-12 h-1 mb-6 -ml-16 mt-6 rounded-full transition-all duration-500
                        ${
                          agentStates[i - 1].status === "completed"
                            ? "bg-gradient-to-r from-green-400 to-blue-500"
                            : "bg-slate-700"
                        }
                      `}
                      />
                    )}

                    {/* Agent Node */}
                    <div
                      className={`
                      w-16 h-16 rounded-2xl flex items-center justify-center transition-all duration-500 mb-3 shadow-xl
                      ${
                        agent.status === "completed"
                          ? "bg-gradient-to-r from-green-400 to-emerald-500 text-white scale-110"
                          : agent.status === "active"
                            ? "bg-gradient-to-r from-pink-500 to-purple-600 text-white animate-pulse scale-110"
                            : "bg-slate-800/50 text-slate-500 backdrop-blur-sm border border-slate-700/50"
                      }
                    `}
                    >
                      {agent.status === "completed" ? (
                        <CheckCircle className="h-6 w-6" />
                      ) : agent.status === "active" ? (
                        <Loader2 className="h-6 w-6 animate-spin" />
                      ) : (
                        agent.icon
                      )}
                    </div>

                    {/* Agent Info */}
                    <div className="text-center max-w-24">
                      <p
                        className={`text-xs font-bold mb-1 ${
                          agent.status === "active"
                            ? "text-pink-400"
                            : agent.status === "completed"
                              ? "text-green-400"
                              : "text-slate-500"
                        }`}
                      >
                        {agent.name}
                      </p>
                      <p className="text-xs text-slate-500 leading-tight">{agent.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Header */}
          <div className="text-center mb-12">
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

          {/* Ad Card with Motion */}
          <div ref={constraintsRef} className="flex justify-center mb-16 h-[600px] relative">
            <motion.div
              className={`relative w-full max-w-sm cursor-grab active:cursor-grabbing ${
                isGenerating ? "opacity-75 scale-95" : "opacity-100 scale-100"
              }`}
              style={{ x, y, rotate, opacity }}
              drag
              dragConstraints={constraintsRef}
              dragElastic={0.2}
              onDragEnd={handleDragEnd}
              whileDrag={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
            >
              <Card className="bg-slate-900/40 backdrop-blur-2xl border-slate-700/30 shadow-2xl rounded-3xl overflow-hidden h-full">
                {/* Swipe Indicators */}
                <motion.div
                  className="absolute top-8 left-8 z-10 bg-red-500/90 text-white px-4 py-2 rounded-full font-bold text-lg"
                  style={{ opacity: useTransform(x, [-100, -50, 0], [1, 0.5, 0]) }}
                >
                  SKIP
                </motion.div>
                <motion.div
                  className="absolute top-8 right-8 z-10 bg-green-500/90 text-white px-4 py-2 rounded-full font-bold text-lg"
                  style={{ opacity: useTransform(x, [0, 50, 100], [0, 0.5, 1]) }}
                >
                  LIKE
                </motion.div>
              <div className="relative h-96">
                <img
                  src={currentAd.imageUrl || "/placeholder.svg"}
                  alt={currentAd.title}
                  className="w-full h-full object-cover"
                />

                <div className="absolute top-4 left-4 right-4 flex justify-between">
                  <Badge className="bg-slate-900/80 backdrop-blur-sm text-white border-0 rounded-full px-3 py-1">
                    {currentAd.realTimeMetrics?.ctr > 0 ?
                      `${currentAd.realTimeMetrics.ctr.toFixed(2)}% CTR` :
                      `${currentAd.estimatedCTR}% Est. CTR`
                    }
                  </Badge>
                  <Badge className="bg-green-500/90 backdrop-blur-sm text-white border-0 rounded-full px-3 py-1">
                    {currentAd.confidence}% Match
                  </Badge>
                </div>

                {/* Real-time Performance Metrics */}
                {currentAd.realTimeMetrics && currentAd.realTimeMetrics.impressions > 0 && (
                  <div className="absolute bottom-4 left-4 right-4">
                    <div className="bg-slate-900/90 backdrop-blur-sm rounded-2xl p-3 border border-slate-700/50">
                      <div className="grid grid-cols-4 gap-2 text-center">
                        <div>
                          <div className="flex items-center justify-center mb-1">
                            <Eye className="h-3 w-3 text-blue-400 mr-1" />
                          </div>
                          <div className="text-xs text-white font-bold">
                            {currentAd.realTimeMetrics.impressions.toLocaleString()}
                          </div>
                          <div className="text-xs text-slate-400">Views</div>
                        </div>
                        <div>
                          <div className="flex items-center justify-center mb-1">
                            <MousePointer className="h-3 w-3 text-green-400 mr-1" />
                          </div>
                          <div className="text-xs text-white font-bold">
                            {currentAd.realTimeMetrics.clicks}
                          </div>
                          <div className="text-xs text-slate-400">Clicks</div>
                        </div>
                        <div>
                          <div className="flex items-center justify-center mb-1">
                            <TrendingUp className="h-3 w-3 text-purple-400 mr-1" />
                          </div>
                          <div className="text-xs text-white font-bold">
                            {currentAd.realTimeMetrics.conversions}
                          </div>
                          <div className="text-xs text-slate-400">Conv.</div>
                        </div>
                        <div>
                          <div className="flex items-center justify-center mb-1">
                            <DollarSign className="h-3 w-3 text-yellow-400 mr-1" />
                          </div>
                          <div className="text-xs text-white font-bold">
                            ${currentAd.realTimeMetrics.revenue.toFixed(0)}
                          </div>
                          <div className="text-xs text-slate-400">Revenue</div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {isGenerating && (
                  <div className="absolute inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center">
                    <div className="bg-slate-900/90 backdrop-blur-xl rounded-2xl p-6 shadow-xl text-center">
                      <div className="w-12 h-12 bg-gradient-to-r from-pink-500 to-purple-600 rounded-xl mx-auto mb-3 flex items-center justify-center">
                        {agentStates[currentAgentIndex]?.icon || (
                          <Loader2 className="h-6 w-6 animate-spin text-white" />
                        )}
                      </div>
                      <p className="text-sm font-medium text-white mb-1">
                        {agentStates[currentAgentIndex]?.name} is working...
                      </p>
                      <p className="text-xs text-slate-400">{agentStates[currentAgentIndex]?.description}</p>
                    </div>
                  </div>
                )}
              </div>

                <CardContent className="p-8">
                  <h3 className="text-xl font-semibold text-white mb-2">{currentAd.title}</h3>
                  <p className="text-slate-400 mb-4">{currentAd.description}</p>
                  <div className="flex items-center justify-between text-sm text-slate-400 mb-4">
                    <span>{currentAd.demographic}</span>
                    <span>{currentAd.audienceSize} reach</span>
                  </div>

                  {/* Interest Tags */}
                  <div className="flex flex-wrap gap-2">
                    {currentAd.interests.map((interest, index) => (
                      <Badge
                        key={index}
                        variant="outline"
                        className="bg-slate-800/50 border-slate-600 text-slate-300 text-xs"
                      >
                        {interest}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </div>

          {/* Action Buttons */}
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
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/10 via-transparent to-pink-900/10" />

      <div className="max-w-5xl mx-auto px-6 py-16 relative z-10">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-light bg-gradient-to-r from-white via-purple-200 to-pink-200 bg-clip-text text-transparent mb-4">
            Your Ad Gallery
          </h1>
          <div className="inline-flex items-center space-x-2 bg-slate-900/50 backdrop-blur-xl rounded-full px-4 py-2">
            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
            <span className="text-sm text-slate-300">{selectedAds.length} ads selected</span>
          </div>
        </div>

        {/* Ad Grid - No reselection, just display */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
          {adVariants
            .filter((ad) => selectedAds.includes(ad.id))
            .map((ad) => (
              <Card
                key={ad.id}
                className="bg-slate-900/40 backdrop-blur-2xl border-slate-700/30 shadow-xl rounded-3xl overflow-hidden"
              >
                <div className="relative">
                  <img src={ad.imageUrl || "/placeholder.svg"} alt={ad.title} className="w-full h-64 object-cover" />
                  <div className="absolute top-4 right-4 w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center shadow-lg">
                    <Check className="h-5 w-5 text-white" />
                  </div>
                  <div className="absolute top-4 left-4">
                    <Badge className="bg-slate-900/80 backdrop-blur-sm text-white border-0 rounded-full">
                      {ad.estimatedCTR}% CTR
                    </Badge>
                  </div>
                </div>

                <CardContent className="p-6">
                  <h3 className="font-semibold text-white mb-2">{ad.title}</h3>
                  <p className="text-sm text-slate-400 mb-4">{ad.demographic}</p>

                  {/* Real-time Performance Grid */}
                  {ad.realTimeMetrics && ad.realTimeMetrics.impressions > 0 && (
                    <div className="grid grid-cols-2 gap-3 mb-4">
                      <div className="bg-slate-800/30 rounded-xl p-3 text-center">
                        <div className="flex items-center justify-center mb-1">
                          <BarChart3 className="h-4 w-4 text-blue-400 mr-1" />
                          <span className="text-xs text-blue-400 font-bold">CTR</span>
                        </div>
                        <div className="text-lg font-bold text-white">
                          {ad.realTimeMetrics.ctr.toFixed(2)}%
                        </div>
                      </div>
                      <div className="bg-slate-800/30 rounded-xl p-3 text-center">
                        <div className="flex items-center justify-center mb-1">
                          <DollarSign className="h-4 w-4 text-green-400 mr-1" />
                          <span className="text-xs text-green-400 font-bold">ROI</span>
                        </div>
                        <div className="text-lg font-bold text-white">
                          {ad.realTimeMetrics.spend > 0 ?
                            `${((ad.realTimeMetrics.revenue / ad.realTimeMetrics.spend - 1) * 100).toFixed(0)}%` :
                            '0%'
                          }
                        </div>
                      </div>
                    </div>
                  )}

                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => onAdPerformanceView?.(ad.id)}
                    className="w-full bg-slate-800/50 backdrop-blur-sm border-slate-600/50 text-slate-300 hover:bg-slate-700/50 hover:text-white rounded-xl"
                  >
                    <BarChart3 className="h-4 w-4 mr-2" />
                    View Performance
                  </Button>
                </CardContent>
              </Card>
            ))}
        </div>

        {/* Launch Button - Only show if not launched */}
        {!isLaunched && (
          <div className="text-center">
            <Button
              onClick={handleLaunch}
              disabled={selectedAds.length === 0}
              size="lg"
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-2xl px-12 py-4 text-lg font-medium shadow-xl shadow-purple-500/25 transition-all duration-300 hover:scale-105 disabled:opacity-50 disabled:scale-100"
            >
              <Sparkles className="h-5 w-5 mr-2" />
              Launch {selectedAds.length} Selected Ads
            </Button>
          </div>
        )}

        {/* Launch Confirmation Modal */}
        {showLaunchConfirm && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
            <Card className="bg-slate-900/90 backdrop-blur-xl border-slate-700/50 rounded-3xl p-8 max-w-md mx-4">
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Sparkles className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-4">Launch Campaign?</h3>
                <p className="text-slate-300 mb-8">
                  Are you ready to launch {selectedAds.length} ad variants? This will start your campaign with real-time
                  AI optimization.
                </p>
                <div className="flex space-x-4">
                  <Button
                    variant="outline"
                    onClick={() => setShowLaunchConfirm(false)}
                    className="flex-1 border-slate-600 text-slate-300 hover:bg-slate-800"
                  >
                    Cancel
                  </Button>
                  <Button
                    onClick={confirmLaunch}
                    className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
                  >
                    Launch Campaign
                  </Button>
                </div>
              </div>
            </Card>
          </div>
        )}

        {/* Success Message - Show after launch */}
        {isLaunched && (
          <div className="text-center">
            <div className="bg-green-500/20 border border-green-500/30 rounded-2xl p-6 max-w-md mx-auto">
              <div className="flex items-center justify-center space-x-2 text-green-400">
                <CheckCircle className="h-5 w-5" />
                <span className="font-medium">Campaign Successfully Launched!</span>
              </div>
              <p className="text-slate-300 text-sm mt-2">Your ads are now live and optimizing automatically.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
