"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import {
  TrendingUp,
  Eye,
  ShoppingCart,
  Brain,
  MessageSquare,
  Play,
  Pause,
  FastForward,
  BarChart3,
  Users,
  Heart,
} from "lucide-react"

interface BusinessData {
  targetEngagement: string
  budget: string
  audience: string
  themes: string[]
}

interface PerformanceTrackingProps {
  selectedAds: string[]
  businessData: BusinessData
  onComplete: () => void
}

interface EngagementData {
  day: number
  dayLabel: string
  engagement: number
  views: number
  conversions: number
  mutation?: {
    id: string
    type: string
    engagement: number
    description: string
    imageUrl: string
  }
}

interface Mutation {
  id: string
  day: number
  type: string
  engagement: number
  description: string
  imageUrl: string
  impact: string
}

export default function PerformanceTrackingDashboard({
  selectedAds,
  businessData,
  onComplete,
}: PerformanceTrackingProps) {
  const [currentDay, setCurrentDay] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [selectedTab, setSelectedTab] = useState<"engagement" | "views" | "conversions">("engagement")
  const [hoveredMutation, setHoveredMutation] = useState<Mutation | null>(null)

  // Add this function at the top of the component
  const generateCampaignThumbnail = () => {
    // Generate a thumbnail based on the campaign data
    const themes = businessData.themes.join("+")
    return `/placeholder.svg?height=60&width=60&text=${encodeURIComponent(themes || "Campaign")}`
  }

  // Generate realistic engagement data over 28 days
  const [engagementData, setEngagementData] = useState<EngagementData[]>(() => {
    const data: EngagementData[] = []
    let baseEngagement = 280

    for (let day = 0; day <= 28; day += 7) {
      // Add some realistic growth with mutations
      if (day === 7) baseEngagement += 50 // First optimization
      if (day === 14) baseEngagement += 80 // Major mutation
      if (day === 21) baseEngagement += 30 // Fine-tuning

      const mutation =
        day === 14
          ? {
              id: "mutation-2",
              type: "Gaming Integration",
              engagement: baseEngagement,
              description: "Added gaming elements to increase engagement",
              imageUrl: "/placeholder.svg?height=200&width=300&text=Gaming+Ad",
            }
          : undefined

      data.push({
        day,
        dayLabel: `Day ${day}`,
        engagement: baseEngagement + Math.random() * 20 - 10,
        views: Math.floor(baseEngagement * 3.2 + Math.random() * 100),
        conversions: Math.floor(baseEngagement * 0.15 + Math.random() * 10),
        mutation,
      })
    }
    return data
  })

  const mutations: Mutation[] = [
    {
      id: "mutation-1",
      day: 7,
      type: "Color Optimization",
      engagement: 330,
      description: "Adjusted color scheme for better visibility",
      imageUrl: "/placeholder.svg?height=200&width=300&text=Color+Optimized",
      impact: "+18% engagement",
    },
    {
      id: "mutation-2",
      day: 14,
      type: "Gaming Integration",
      engagement: 480,
      description: "Added gaming elements to increase engagement",
      imageUrl: "/placeholder.svg?height=200&width=300&text=Gaming+Ad",
      impact: "+45% engagement",
    },
    {
      id: "mutation-3",
      day: 21,
      type: "Audience Refinement",
      engagement: 520,
      description: "Refined targeting based on performance data",
      imageUrl: "/placeholder.svg?height=200&width=300&text=Targeted+Ad",
      impact: "+8% engagement",
    },
  ]

  // Auto-play simulation
  useEffect(() => {
    if (isPlaying && currentDay < 28) {
      const timer = setTimeout(() => {
        setCurrentDay((prev) => Math.min(prev + 1, 28))
      }, 500) // 500ms per day for smooth animation

      return () => clearTimeout(timer)
    }
  }, [isPlaying, currentDay])

  const skipDays = (days: number) => {
    setCurrentDay((prev) => Math.min(prev + days, 28))
  }

  const getCurrentData = () => {
    return engagementData.filter((d) => d.day <= currentDay)
  }

  const getCurrentMetric = () => {
    const data = getCurrentData()
    if (data.length === 0) return 0

    const latest = data[data.length - 1]
    switch (selectedTab) {
      case "engagement":
        return latest.engagement
      case "views":
        return latest.views
      case "conversions":
        return latest.conversions
      default:
        return latest.engagement
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/15 via-transparent to-pink-900/15" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/8 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-pink-500/8 rounded-full blur-3xl animate-pulse delay-1000" />

      <div className="max-w-7xl mx-auto p-6 relative z-10">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-light bg-gradient-to-r from-white via-purple-200 to-pink-200 bg-clip-text text-transparent mb-2">
              Campaign Performance Tracking
            </h1>
            <p className="text-xl text-slate-400">Watch your ads evolve and optimize in real-time</p>
          </div>

          <div className="flex items-center space-x-4">
            {/* Demo Mode Badge */}
            <Badge className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 border-purple-500/30 text-purple-300 px-4 py-2">
              <BarChart3 className="h-4 w-4 mr-2" />
              DEMO MODE
            </Badge>

            {/* Skip Controls */}
            <Button
              onClick={() => skipDays(7)}
              disabled={currentDay >= 28}
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 rounded-xl"
            >
              <FastForward className="h-4 w-4 mr-2" />
              Skip 7 Days
            </Button>
          </div>
        </div>

        {/* Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {[
            {
              title: "Current Day",
              value: `Day ${currentDay}`,
              change: currentDay > 0 ? `+${currentDay} days` : "Starting",
              icon: TrendingUp,
              color: "blue",
            },
            {
              title: "Total Engagement",
              value: Math.floor(getCurrentMetric()).toLocaleString(),
              change: currentDay > 0 ? "+85%" : "Baseline",
              icon: Heart,
              color: "pink",
            },
            {
              title: "Active Mutations",
              value: mutations.filter((m) => m.day <= currentDay).length.toString(),
              change: "AI Optimizations",
              icon: Brain,
              color: "purple",
            },
            {
              title: "Selected Ads",
              value: selectedAds.length.toString(),
              change: "Running Live",
              icon: Users,
              color: "green",
            },
          ].map((metric, index) => (
            <Card
              key={index}
              className="bg-slate-900/40 backdrop-blur-2xl border-slate-700/30 shadow-xl rounded-2xl overflow-hidden"
            >
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-slate-400 mb-1">{metric.title}</p>
                    <p className="text-3xl font-bold text-white mb-2">{metric.value}</p>
                    <p className="text-sm text-slate-300">{metric.change}</p>
                  </div>
                  <metric.icon
                    className={`h-10 w-10 ${
                      metric.color === "blue"
                        ? "text-blue-400"
                        : metric.color === "pink"
                          ? "text-pink-400"
                          : metric.color === "purple"
                            ? "text-purple-400"
                            : "text-green-400"
                    }`}
                  />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Main Chart */}
        <Card className="bg-slate-900/40 backdrop-blur-2xl border-slate-700/30 shadow-xl rounded-3xl overflow-hidden mb-8">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-white text-2xl font-semibold flex items-center">
                  <TrendingUp className="h-6 w-6 mr-3 text-purple-400" />
                  Engagement Evolution
                </CardTitle>
                <p className="text-slate-400 mt-2">Track the engagement performance over time</p>
              </div>

              {/* Metric Tabs */}
              <div className="flex space-x-2">
                {[
                  { key: "engagement", label: "Engagement", icon: Heart },
                  { key: "views", label: "Views", icon: Eye },
                  { key: "conversions", label: "Conversions", icon: ShoppingCart },
                ].map((tab) => (
                  <Button
                    key={tab.key}
                    variant={selectedTab === tab.key ? "default" : "ghost"}
                    size="sm"
                    onClick={() => setSelectedTab(tab.key as any)}
                    className={`${
                      selectedTab === tab.key ? "bg-purple-600 text-white" : "text-slate-400 hover:text-white"
                    } rounded-xl`}
                  >
                    <tab.icon className="h-4 w-4 mr-2" />
                    {tab.label}
                  </Button>
                ))}
              </div>
            </div>
          </CardHeader>

          <CardContent>
            <div className="h-96 relative">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={getCurrentData()} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
                  <XAxis dataKey="dayLabel" stroke="#94a3b8" tick={{ fontSize: 12 }} />
                  <YAxis
                    stroke="#94a3b8"
                    tick={{ fontSize: 12 }}
                    label={{
                      value: `${selectedTab.charAt(0).toUpperCase() + selectedTab.slice(1)} Score`,
                      angle: -90,
                      position: "insideLeft",
                      style: { textAnchor: "middle", fill: "#94a3b8" },
                    }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#0f172a",
                      border: "1px solid #475569",
                      borderRadius: "12px",
                      color: "#ffffff",
                      backdropFilter: "blur(20px)",
                    }}
                    content={({ active, payload, label }) => {
                      if (active && payload && payload.length) {
                        const data = payload[0].payload
                        return (
                          <div className="bg-slate-900/95 backdrop-blur-xl border border-purple-500/30 rounded-2xl p-4 shadow-2xl">
                            <p className="text-purple-300 font-medium mb-2">{label}</p>
                            <p className="text-white text-lg font-bold">
                              {selectedTab.charAt(0).toUpperCase() + selectedTab.slice(1)}:{" "}
                              {Math.floor(payload[0].value as number)}
                            </p>
                            {data.mutation && (
                              <div className="mt-3 pt-3 border-t border-slate-600">
                                <p className="text-yellow-400 font-medium text-sm">{data.mutation.type}</p>
                                <p className="text-slate-300 text-xs">{data.mutation.description}</p>
                              </div>
                            )}
                          </div>
                        )
                      }
                      return null
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey={selectedTab}
                    stroke="#a855f7"
                    strokeWidth={3}
                    dot={(props) => {
                      const { cx, cy, payload } = props
                      return (
                        <g>
                          <circle
                            cx={cx}
                            cy={cy}
                            r={payload.mutation ? 8 : 4}
                            fill={payload.mutation ? "#fbbf24" : "#a855f7"}
                            stroke={payload.mutation ? "#f59e0b" : "#a855f7"}
                            strokeWidth={2}
                            className={payload.mutation ? "animate-pulse cursor-pointer" : ""}
                            onMouseEnter={() => {
                              if (payload.mutation) {
                                setHoveredMutation({
                                  id: payload.mutation.id,
                                  day: payload.day,
                                  type: payload.mutation.type,
                                  engagement: payload.mutation.engagement,
                                  description: payload.mutation.description,
                                  imageUrl: payload.mutation.imageUrl,
                                  impact: `+${Math.floor(((payload.mutation.engagement - 280) / 280) * 100)}% engagement`,
                                })
                              }
                            }}
                            onMouseLeave={() => setHoveredMutation(null)}
                          />
                          {payload.mutation && (
                            <circle
                              cx={cx}
                              cy={cy}
                              r={12}
                              fill="none"
                              stroke="#fbbf24"
                              strokeWidth={1}
                              className="animate-ping opacity-75"
                            />
                          )}
                        </g>
                      )
                    }}
                    activeDot={{ r: 6, stroke: "#a855f7", strokeWidth: 2 }}
                  />
                </LineChart>
              </ResponsiveContainer>

              {/* Mutation Popup */}
              {hoveredMutation && (
                <div className="absolute top-4 right-4 bg-slate-900/95 backdrop-blur-xl border border-purple-500/30 rounded-2xl p-4 shadow-2xl max-w-xs">
                  <div className="flex items-start space-x-3">
                    <img
                      src={hoveredMutation.imageUrl || "/placeholder.svg"}
                      alt={hoveredMutation.type}
                      className="w-16 h-12 object-cover rounded-lg border border-slate-600/50"
                    />
                    <div>
                      <h4 className="text-white font-semibold text-sm">{hoveredMutation.type}</h4>
                      <p className="text-yellow-400 text-xs font-medium">engagement: {hoveredMutation.engagement}</p>
                      <p className="text-slate-300 text-xs mt-1">{hoveredMutation.description}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Playback Controls */}
        <div className="flex items-center justify-center space-x-6 mb-8">
          <Button
            onClick={() => setIsPlaying(!isPlaying)}
            disabled={currentDay >= 28}
            size="lg"
            className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 rounded-2xl px-8 py-4"
          >
            {isPlaying ? (
              <>
                <Pause className="h-5 w-5 mr-2" />
                Pause Simulation
              </>
            ) : (
              <>
                <Play className="h-5 w-5 mr-2" />
                {currentDay === 0 ? "Start Simulation" : "Resume Simulation"}
              </>
            )}
          </Button>

          <div className="text-center">
            <p className="text-slate-400 text-sm">Campaign Progress</p>
            <div className="w-64 h-2 bg-slate-800 rounded-full mt-2">
              <div
                className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full transition-all duration-500"
                style={{ width: `${(currentDay / 28) * 100}%` }}
              />
            </div>
            <p className="text-slate-300 text-xs mt-1">{Math.floor((currentDay / 28) * 100)}% Complete</p>
          </div>
        </div>

        {/* AI Analyst */}
        <Card className="bg-gradient-to-r from-slate-900/50 via-purple-900/30 to-pink-900/30 backdrop-blur-2xl border border-purple-500/20 rounded-3xl shadow-2xl overflow-hidden mb-8">
          <CardContent className="p-8">
            <div className="flex items-start space-x-6">
              <div className="relative">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-500 via-pink-500 to-blue-500 rounded-2xl flex items-center justify-center shadow-2xl">
                  <Brain className="h-8 w-8 text-white" />
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-slate-950 animate-pulse" />
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-2xl font-bold text-white flex items-center">
                    AI Campaign Analyst
                    <Badge className="ml-3 bg-blue-500/20 text-blue-400 border-blue-500/30 rounded-full px-3 py-1">
                      Evolution {mutations.filter((m) => m.day <= currentDay).length}
                    </Badge>
                  </h3>
                  <MessageSquare className="h-5 w-5 text-purple-400" />
                </div>
                <p className="text-slate-200 leading-relaxed text-lg">
                  {currentDay === 0 &&
                    "Ready to track your campaign performance! The simulation will show how AI optimizations improve engagement over time."}
                  {currentDay > 0 &&
                    currentDay < 7 &&
                    "Campaign is starting strong! Initial performance looks promising with steady engagement growth."}
                  {currentDay >= 7 &&
                    currentDay < 14 &&
                    "First optimization applied! Color adjustments are showing positive impact on user engagement."}
                  {currentDay >= 14 &&
                    currentDay < 21 &&
                    "Major breakthrough! Gaming integration has significantly boosted engagement. Let's continue the same strategy!"}
                  {currentDay >= 21 &&
                    currentDay < 28 &&
                    "Fine-tuning audience targeting based on performance data. Engagement remains strong and stable."}
                  {currentDay >= 28 &&
                    "Campaign complete! Your ads have evolved through multiple AI optimizations, achieving excellent engagement growth."}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Complete Button */}
        {currentDay >= 28 && (
          <div className="text-center">
            <Button
              onClick={() => {
                // You can pass additional data here if needed
                onComplete()
              }}
              size="lg"
              className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white rounded-2xl px-12 py-4 text-lg font-bold shadow-xl transition-all duration-300 hover:scale-105"
            >
              <TrendingUp className="h-5 w-5 mr-2" />
              Complete Campaign Analysis
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}
