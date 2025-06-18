"use client"

import type React from "react"

import { useEffect, useState } from "react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Sparkles, CheckCircle, Loader2, Brain, Users, Palette, Target, Zap } from "lucide-react"

interface BusinessData {
  targetEngagement: string
  budget: string
  audience: string
  themes: string[]
  originalAd?: File
}

interface ProcessingPanelProps {
  businessData: BusinessData
}

interface Agent {
  id: string
  name: string
  description: string
  icon: React.ReactNode
  status: "pending" | "active" | "completed"
}

export default function ProcessingPanel({ businessData }: ProcessingPanelProps) {
  const [currentAgentIndex, setCurrentAgentIndex] = useState(0)
  const [progress, setProgress] = useState(0)

  const agents: Agent[] = [
    {
      id: "psychographic",
      name: "PsychoGrapher",
      description: "Analyzing psychological profiles and behavioral patterns",
      icon: <Brain className="h-5 w-5" />,
      status: "pending",
    },
    {
      id: "demographic",
      name: "DemoDetective",
      description: "Identifying key demographic segments and interests",
      icon: <Users className="h-5 w-5" />,
      status: "pending",
    },
    {
      id: "creative",
      name: "VisualVirtuoso",
      description: "Crafting compelling creative variations",
      icon: <Palette className="h-5 w-5" />,
      status: "pending",
    },
    {
      id: "optimizer",
      name: "PerformanceProdigy",
      description: "Optimizing for maximum engagement and conversions",
      icon: <Target className="h-5 w-5" />,
      status: "pending",
    },
    {
      id: "deployer",
      name: "LaunchLord",
      description: "Finalizing variants and preparing deployment",
      icon: <Zap className="h-5 w-5" />,
      status: "pending",
    },
  ]

  const [agentStates, setAgentStates] = useState<Agent[]>(agents)

  useEffect(() => {
    const agentInterval = setInterval(() => {
      setCurrentAgentIndex((prev) => {
        const next = (prev + 1) % agents.length

        // Update agent states
        setAgentStates((currentAgents) =>
          currentAgents.map((agent, index) => ({
            ...agent,
            status: index < prev ? "completed" : index === prev ? "active" : "pending",
          })),
        )

        setProgress((prev) => Math.min(prev + 20, 100))
        return next
      })
    }, 1200)

    return () => clearInterval(agentInterval)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 relative overflow-hidden">
      {/* Enhanced Background Effects */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-slate-900/10 to-pink-900/20" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-pink-500/10 rounded-full blur-3xl animate-pulse delay-1000" />
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl animate-pulse delay-2000" />

      <div className="max-w-6xl mx-auto px-6 py-12 relative z-10">
        {/* Enhanced Header */}
        <div className="text-center mb-16">
          <div className="flex items-center justify-center mb-6">
            <div className="relative">
              <div className="w-20 h-20 bg-gradient-to-br from-pink-500 via-purple-500 to-blue-500 rounded-3xl flex items-center justify-center shadow-2xl shadow-purple-500/25">
                <Sparkles className="h-10 w-10 text-white animate-pulse" />
              </div>
              <div className="absolute -top-2 -right-2 w-6 h-6 bg-green-400 rounded-full border-2 border-slate-950 animate-pulse" />
            </div>
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-pink-400 via-purple-400 to-blue-400 bg-clip-text text-transparent mb-4">
            AI Agents At Work
          </h1>
          <p className="text-xl text-purple-300 font-medium">Multi-agent system creating your personalized campaigns</p>
          <div className="inline-flex items-center space-x-3 bg-gradient-to-r from-yellow-500/20 via-orange-500/20 to-red-500/20 border border-yellow-500/30 rounded-full px-6 py-3 mt-6 backdrop-blur-sm">
            <div className="relative">
              <div className="w-3 h-3 bg-yellow-400 rounded-full animate-pulse"></div>
              <div className="absolute inset-0 w-3 h-3 bg-yellow-400 rounded-full animate-ping opacity-75"></div>
            </div>
            <span className="text-yellow-400 text-sm font-bold">DEMO MODE</span>
          </div>
        </div>

        {/* Enhanced Agent Workflow Nodes */}
        <div className="mb-20">
          <div className="flex justify-center">
            <div className="flex items-center space-x-6 max-w-5xl overflow-x-auto pb-4">
              {agentStates.map((agent, i) => (
                <div key={agent.id} className="flex flex-col items-center min-w-0 relative">
                  {/* Enhanced Connection Line */}
                  {i > 0 && (
                    <div
                      className={`
                      w-16 h-1 mb-8 -ml-20 mt-8 rounded-full transition-all duration-500
                      ${
                        agentStates[i - 1].status === "completed"
                          ? "bg-gradient-to-r from-green-400 via-blue-500 to-purple-500 shadow-lg shadow-purple-500/25"
                          : "bg-slate-700"
                      }
                    `}
                    />
                  )}

                  {/* Enhanced Agent Node */}
                  <div
                    className={`
                    w-20 h-20 rounded-3xl flex items-center justify-center transition-all duration-500 mb-4 shadow-2xl
                    ${
                      agent.status === "completed"
                        ? "bg-gradient-to-r from-green-400 via-emerald-500 to-teal-500 text-white scale-110 shadow-green-500/25"
                        : agent.status === "active"
                          ? "bg-gradient-to-r from-pink-500 via-purple-600 to-blue-600 text-white animate-pulse scale-110 shadow-purple-500/25"
                          : "bg-slate-800/50 text-slate-500 backdrop-blur-sm border border-slate-700/50"
                    }
                  `}
                  >
                    {agent.status === "completed" ? (
                      <CheckCircle className="h-8 w-8" />
                    ) : agent.status === "active" ? (
                      <Loader2 className="h-8 w-8 animate-spin" />
                    ) : (
                      agent.icon
                    )}
                  </div>

                  {/* Enhanced Agent Info */}
                  <div className="text-center max-w-36">
                    <p
                      className={`text-base font-bold mb-2 ${
                        agent.status === "active"
                          ? "text-pink-400"
                          : agent.status === "completed"
                            ? "text-green-400"
                            : "text-slate-500"
                      }`}
                    >
                      {agent.name}
                    </p>
                    <p className="text-xs text-slate-400 leading-tight">{agent.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Enhanced Current Agent Activity */}
        <div className="flex justify-center mb-20">
          <Card className="bg-slate-900/50 backdrop-blur-xl border-purple-500/20 shadow-2xl shadow-purple-500/10 rounded-3xl p-16 max-w-3xl w-full relative overflow-hidden">
            {/* Enhanced Card Background Effects */}
            <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 via-pink-500/5 to-blue-500/5" />
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-pink-500 via-purple-500 to-blue-500" />

            <div className="text-center relative">
              {/* Enhanced Central Processing Icon */}
              <div className="w-32 h-32 bg-gradient-to-br from-pink-500 via-purple-600 to-blue-600 rounded-3xl mx-auto mb-10 flex items-center justify-center shadow-2xl shadow-purple-500/25 relative">
                <Sparkles className="h-16 w-16 text-white animate-pulse" />
                <div className="absolute -top-2 -right-2 w-8 h-8 bg-green-400 rounded-full border-2 border-slate-950 animate-pulse" />
              </div>

              <h2 className="text-3xl font-bold text-white mb-6">
                {agentStates[currentAgentIndex]?.name} is working...
              </h2>

              <p className="text-xl text-purple-300 mb-10 font-medium">{agentStates[currentAgentIndex]?.description}</p>

              {/* Enhanced Progress Bar */}
              <div className="mb-10">
                <div className="flex justify-between text-lg text-slate-300 mb-4 font-medium">
                  <span>Campaign Generation Progress</span>
                  <span>{progress}%</span>
                </div>
                <div className="w-full h-4 bg-slate-800/50 rounded-full overflow-hidden backdrop-blur-sm border border-slate-700/50">
                  <div
                    className="h-full bg-gradient-to-r from-pink-500 via-purple-600 to-blue-600 rounded-full transition-all duration-1000 shadow-lg shadow-purple-500/25"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>

              <div className="flex items-center justify-center space-x-3 text-purple-300">
                <div className="relative">
                  <div className="w-3 h-3 bg-pink-500 rounded-full animate-ping"></div>
                  <div className="absolute inset-0 w-3 h-3 bg-pink-500 rounded-full animate-pulse"></div>
                </div>
                <p className="text-lg font-medium">Analyzing {businessData.audience.toLowerCase()} segments...</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Enhanced Campaign Preview */}
        <div className="flex justify-center">
          <Card className="bg-slate-900/30 backdrop-blur-xl border-slate-700/50 shadow-xl rounded-3xl p-10 max-w-2xl w-full relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-slate-800/20 to-purple-900/20" />
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-slate-500 via-purple-500 to-pink-500" />

            <h3 className="text-2xl font-bold text-white mb-8 text-center relative">Campaign Preview</h3>

            <div className="space-y-6 relative">
              <div className="p-6 bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-600/50">
                <label className="text-sm font-bold text-purple-300 uppercase tracking-wider mb-2 block">
                  Target Goal
                </label>
                <p className="text-white text-lg">{businessData.targetEngagement}</p>
              </div>

              <div className="p-6 bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-600/50">
                <label className="text-sm font-bold text-pink-300 uppercase tracking-wider mb-2 block">Budget</label>
                <p className="text-white text-lg">{businessData.budget}</p>
              </div>

              <div className="p-6 bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-600/50">
                <label className="text-sm font-bold text-blue-300 uppercase tracking-wider mb-2 block">Audience</label>
                <p className="text-white text-lg">{businessData.audience}</p>
              </div>

              <div className="p-6 bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-600/50">
                <label className="text-sm font-bold text-green-300 uppercase tracking-wider mb-2 block">Themes</label>
                <div className="flex flex-wrap gap-3 mt-3">
                  {businessData.themes.map((theme, index) => (
                    <Badge
                      key={index}
                      variant="outline"
                      className="bg-slate-700/50 border-slate-500 text-slate-200 px-4 py-2 text-sm"
                    >
                      {theme}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
