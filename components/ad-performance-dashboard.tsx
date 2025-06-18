"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { TrendingUp, Eye, MousePointer, ShoppingCart, Zap, Brain, MessageSquare } from "lucide-react"

interface AdPerformanceProps {
  adId: string
  onBack: () => void
}

interface Mutation {
  id: string
  timestamp: string
  type: string
  description: string
  impact: string
  status: "active" | "completed"
  explanation: string
}

export default function AdPerformanceDashboard({ adId, onBack }: AdPerformanceProps) {
  const [performanceData, setPerformanceData] = useState([
    { time: "00:00", ctr: 2.1, conversions: 0.8, impressions: 1200 },
    { time: "04:00", ctr: 2.3, conversions: 1.1, impressions: 1450 },
    { time: "08:00", ctr: 2.8, conversions: 1.4, impressions: 1800 },
    { time: "12:00", ctr: 3.2, conversions: 1.8, impressions: 2100 },
    { time: "16:00", ctr: 3.5, conversions: 2.1, impressions: 2400 },
    { time: "20:00", ctr: 3.1, conversions: 1.9, impressions: 2200 },
  ])

  const [mutations, setMutations] = useState<Mutation[]>([
    {
      id: "1",
      timestamp: "2 hours ago",
      type: "Gaming Integration",
      description: "Incorporated Minecraft elements into ad creative",
      impact: "+12% Engagement",
      status: "active",
      explanation:
        "Detected rising trend in sandbox gaming among target demographic. Integrated Minecraft-style visuals to align with current gaming preferences, resulting in improved engagement rates.",
    },
    {
      id: "2",
      timestamp: "4 hours ago",
      type: "Color Psychology",
      description: "Adjusted color scheme based on A/B test results",
      impact: "+8% Conversion",
      status: "completed",
      explanation:
        "Visual analysis showed purple-blue gradients perform 23% better with our target age group. Updated creative assets to leverage this psychological preference.",
    },
    {
      id: "3",
      timestamp: "6 hours ago",
      type: "Demographic Refinement",
      description: "Narrowed targeting to high-intent segments",
      impact: "+15% ROI",
      status: "completed",
      explanation:
        "Machine learning identified micro-segments with 3x higher conversion probability. Reallocated budget to focus on these high-value audience clusters.",
    },
  ])

  const [currentExplanation, setCurrentExplanation] = useState(mutations[0]?.explanation || "")
  const [isExplaining, setIsExplaining] = useState(false)

  useEffect(() => {
    // Simulate real-time explanations
    const explanationInterval = setInterval(() => {
      const randomMutation = mutations[Math.floor(Math.random() * mutations.length)]
      setCurrentExplanation(randomMutation.explanation)
      setIsExplaining(true)

      setTimeout(() => setIsExplaining(false), 4000)
    }, 8000)

    return () => clearInterval(explanationInterval)
  }, [mutations])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 relative overflow-hidden">
      {/* Sophisticated Background */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/15 via-transparent to-pink-900/15" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/8 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-pink-500/8 rounded-full blur-3xl animate-pulse delay-1000" />

      <div className="max-w-7xl mx-auto p-6 relative z-10">
        {/* Elegant Header */}
        <div className="flex items-center justify-between mb-12">
          <div>
            <Button
              variant="ghost"
              onClick={onBack}
              className="mb-6 text-slate-400 hover:text-white hover:bg-slate-800/50 rounded-xl transition-all duration-300"
            >
              ← Back to Gallery
            </Button>
            <h1 className="text-4xl font-light bg-gradient-to-r from-white via-purple-200 to-pink-200 bg-clip-text text-transparent mb-2">
              Live Performance Dashboard
            </h1>
            <p className="text-xl text-slate-400">Real-time AI optimization in action</p>
          </div>
          <div className="flex items-center space-x-6">
            <div className="bg-gradient-to-r from-yellow-500/20 via-orange-500/20 to-red-500/20 border border-yellow-500/30 rounded-2xl px-6 py-3 backdrop-blur-xl">
              <div className="flex items-center space-x-3">
                <div className="relative">
                  <div className="w-3 h-3 bg-yellow-400 rounded-full animate-pulse"></div>
                  <div className="absolute inset-0 w-3 h-3 bg-yellow-400 rounded-full animate-ping opacity-75"></div>
                </div>
                <span className="text-yellow-400 font-bold">DEMO MODE</span>
              </div>
            </div>
            <div className="flex items-center space-x-3 bg-slate-900/50 backdrop-blur-xl rounded-2xl px-4 py-3">
              <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse" />
              <span className="text-slate-300 font-medium">Live Optimization Active</span>
            </div>
          </div>
        </div>

        {/* Elegant Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          {[
            {
              title: "Click-Through Rate",
              value: "3.5%",
              change: "+0.7%",
              icon: MousePointer,
              color: "blue",
            },
            {
              title: "Conversion Rate",
              value: "2.1%",
              change: "+0.3%",
              icon: ShoppingCart,
              color: "green",
            },
            {
              title: "Impressions",
              value: "24.2K",
              change: "+12%",
              icon: Eye,
              color: "purple",
            },
            {
              title: "AI Evolutions",
              value: "7",
              change: "3 active",
              icon: Brain,
              color: "yellow",
            },
          ].map((metric, index) => (
            <Card
              key={index}
              className="bg-slate-900/40 backdrop-blur-2xl border-slate-700/30 shadow-xl rounded-2xl overflow-hidden group hover:scale-105 transition-all duration-300"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-slate-800/20 to-purple-900/20" />
              <CardContent className="p-6 relative">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-slate-400 mb-1">{metric.title}</p>
                    <p className="text-3xl font-bold text-white mb-2">{metric.value}</p>
                    <div className="flex items-center">
                      <TrendingUp className="h-4 w-4 text-green-400 mr-1" />
                      <span className="text-sm text-green-400 font-medium">{metric.change} from yesterday</span>
                    </div>
                  </div>
                  <metric.icon
                    className={`h-10 w-10 ${
                      metric.color === "blue"
                        ? "text-blue-400"
                        : metric.color === "green"
                          ? "text-green-400"
                          : metric.color === "purple"
                            ? "text-purple-400"
                            : "text-yellow-400"
                    }`}
                  />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Elegant Performance Chart */}
          <Card className="bg-slate-900/40 backdrop-blur-2xl border-slate-700/30 shadow-xl rounded-3xl overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-slate-800/20 to-purple-900/20" />
            <CardHeader className="relative">
              <CardTitle className="text-white text-xl font-semibold flex items-center">
                <TrendingUp className="h-5 w-5 mr-2 text-purple-400" />
                Performance Evolution
              </CardTitle>
            </CardHeader>
            <CardContent className="relative">
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={performanceData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
                  <XAxis dataKey="time" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#0f172a",
                      border: "1px solid #475569",
                      borderRadius: "12px",
                      color: "#ffffff",
                      backdropFilter: "blur(20px)",
                    }}
                  />
                  <Line type="monotone" dataKey="ctr" stroke="#a855f7" name="CTR %" strokeWidth={3} />
                  <Line type="monotone" dataKey="conversions" stroke="#10b981" name="Conversion %" strokeWidth={3} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Elegant Mutation Tracker */}
          <Card className="bg-slate-900/40 backdrop-blur-2xl border-slate-700/30 shadow-xl rounded-3xl overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-slate-800/20 to-purple-900/20" />
            <CardHeader className="relative">
              <CardTitle className="text-white text-xl font-semibold flex items-center">
                <Zap className="h-5 w-5 mr-2 text-yellow-400" />
                Live Mutation Tracker
              </CardTitle>
            </CardHeader>
            <CardContent className="relative">
              <div className="space-y-4">
                {mutations.map((mutation, index) => (
                  <div
                    key={mutation.id}
                    className="p-4 bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-600/30 transition-all duration-300 hover:bg-slate-700/50"
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <div
                          className={`w-3 h-3 rounded-full ${
                            mutation.status === "active" ? "bg-green-400 animate-pulse" : "bg-slate-500"
                          }`}
                        />
                        <div>
                          <p className="font-semibold text-white">{mutation.type}</p>
                          <p className="text-sm text-slate-400">{mutation.description}</p>
                          <p className="text-xs text-slate-500 mt-1">{mutation.timestamp}</p>
                        </div>
                      </div>
                      <Badge
                        className={`${
                          mutation.status === "active"
                            ? "bg-green-500/20 text-green-400 border-green-500/30"
                            : "bg-slate-600/20 text-slate-300 border-slate-600/30"
                        } rounded-full px-3 py-1`}
                      >
                        {mutation.impact}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Elegant AI Campaign Analyst */}
        <Card className="bg-gradient-to-r from-slate-900/50 via-purple-900/30 to-pink-900/30 backdrop-blur-2xl border border-purple-500/20 rounded-3xl shadow-2xl overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 via-pink-500/5 to-blue-500/5" />
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500" />
          <CardContent className="p-8 relative">
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
                      Evolution 1
                    </Badge>
                  </h3>
                  <div className={`flex items-center space-x-3 ${isExplaining ? "animate-pulse" : ""}`}>
                    <MessageSquare className="h-5 w-5 text-purple-400" />
                    <span className="text-sm text-purple-400 font-medium">EXPLAINING</span>
                  </div>
                </div>
                <p className="text-slate-200 leading-relaxed text-lg">{currentExplanation}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
