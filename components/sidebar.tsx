"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { LayoutDashboard, TrendingUp, Users, Settings, Plus, ChevronLeft, ChevronRight, Sparkles } from "lucide-react"

interface Campaign {
  id: string
  name: string
  status: "active" | "paused" | "completed"
  performance: number
  spend: string
}

interface SidebarProps {
  isCollapsed: boolean
  onToggle: () => void
  onCampaignSelect?: (id: string) => void
}

export default function Sidebar({ isCollapsed, onToggle, onCampaignSelect }: SidebarProps) {
  const [selectedCampaign, setSelectedCampaign] = useState<string>("1")

  const campaigns: Campaign[] = [
    { id: "1", name: "Q1 Brand Push", status: "active", performance: 94, spend: "$12.4K" },
    { id: "2", name: "Product Launch", status: "active", performance: 87, spend: "$8.7K" },
    { id: "3", name: "Holiday Sale", status: "completed", performance: 92, spend: "$15.2K" },
    { id: "4", name: "Retargeting", status: "paused", performance: 76, spend: "$5.1K" },
  ]

  const handleCampaignClick = (campaignId: string) => {
    setSelectedCampaign(campaignId)
    onCampaignSelect?.(campaignId)
  }

  return (
    <div
      className={`
      bg-gradient-to-b from-slate-950 via-purple-950 to-slate-950 border-r border-purple-500/20 
      transition-all duration-500 flex flex-col relative overflow-hidden
      ${isCollapsed ? "w-20" : "w-80"}
    `}
    >
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-600/5 via-pink-600/5 to-blue-600/5 animate-pulse" />
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-pink-500 via-purple-500 to-blue-500" />

      {/* Header */}
      <div className="relative p-6 border-b border-purple-500/20">
        <div className="flex items-center justify-between">
          {!isCollapsed && (
            <div className="flex items-center space-x-4">
              <div className="relative">
                <div className="w-12 h-12 bg-gradient-to-br from-pink-500 via-purple-500 to-blue-500 rounded-2xl flex items-center justify-center shadow-lg shadow-purple-500/25">
                  <Sparkles className="h-6 w-6 text-white animate-pulse" />
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-400 rounded-full border-2 border-slate-950 animate-pulse" />
              </div>
              <div>
                <h2 className="text-white font-bold text-lg bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent">
                  AdMorph.AI
                </h2>
                <p className="text-purple-300 text-sm font-medium">Campaign Hub</p>
              </div>
            </div>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={onToggle}
            className="text-purple-300 hover:text-white hover:bg-purple-500/20 rounded-xl transition-all duration-300"
          >
            {isCollapsed ? <ChevronRight className="h-5 w-5" /> : <ChevronLeft className="h-5 w-5" />}
          </Button>
        </div>
      </div>

      {/* Navigation */}
      <div className="relative p-6">
        <nav className="space-y-3">
          <Button
            variant="ghost"
            className={`w-full justify-start text-white hover:bg-gradient-to-r hover:from-pink-500/20 hover:to-purple-500/20 rounded-xl transition-all duration-300 ${isCollapsed ? "px-4" : ""} h-12`}
          >
            <LayoutDashboard className="h-5 w-5" />
            {!isCollapsed && <span className="ml-4 font-medium">Dashboard</span>}
          </Button>
          <Button
            variant="ghost"
            className={`w-full justify-start text-purple-300 hover:text-white hover:bg-gradient-to-r hover:from-pink-500/20 hover:to-purple-500/20 rounded-xl transition-all duration-300 ${isCollapsed ? "px-4" : ""} h-12`}
          >
            <TrendingUp className="h-5 w-5" />
            {!isCollapsed && <span className="ml-4 font-medium">Analytics</span>}
          </Button>
          <Button
            variant="ghost"
            className={`w-full justify-start text-purple-300 hover:text-white hover:bg-gradient-to-r hover:from-pink-500/20 hover:to-purple-500/20 rounded-xl transition-all duration-300 ${isCollapsed ? "px-4" : ""} h-12`}
          >
            <Users className="h-5 w-5" />
            {!isCollapsed && <span className="ml-4 font-medium">Audiences</span>}
          </Button>
          <Button
            variant="ghost"
            className={`w-full justify-start text-purple-300 hover:text-white hover:bg-gradient-to-r hover:from-pink-500/20 hover:to-purple-500/20 rounded-xl transition-all duration-300 ${isCollapsed ? "px-4" : ""} h-12`}
          >
            <Settings className="h-5 w-5" />
            {!isCollapsed && <span className="ml-4 font-medium">Settings</span>}
          </Button>
        </nav>
      </div>

      {/* Campaigns */}
      {!isCollapsed && (
        <div className="flex-1 relative p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-white font-bold text-lg">Active Campaigns</h3>
            <Button
              size="sm"
              className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 rounded-xl shadow-lg shadow-purple-500/25 transition-all duration-300 hover:scale-105"
            >
              <Plus className="h-4 w-4" />
            </Button>
          </div>

          <div className="space-y-4">
            {campaigns.map((campaign) => (
              <Card
                key={campaign.id}
                className={`p-4 cursor-pointer transition-all duration-300 border-purple-500/20 backdrop-blur-sm rounded-2xl hover:scale-105 ${
                  selectedCampaign === campaign.id
                    ? "bg-gradient-to-r from-pink-500/20 via-purple-500/20 to-blue-500/20 border-pink-500/50 shadow-lg shadow-purple-500/25"
                    : "bg-slate-800/30 hover:bg-slate-700/40"
                }`}
                onClick={() => handleCampaignClick(campaign.id)}
              >
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-white text-sm font-bold truncate">{campaign.name}</h4>
                  <Badge
                    variant="outline"
                    className={`text-xs font-medium rounded-full px-3 py-1 ${
                      campaign.status === "active"
                        ? "border-green-400/50 text-green-400 bg-green-400/10"
                        : campaign.status === "paused"
                          ? "border-yellow-400/50 text-yellow-400 bg-yellow-400/10"
                          : "border-slate-400/50 text-slate-400 bg-slate-400/10"
                    }`}
                  >
                    {campaign.status}
                  </Badge>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-purple-300 font-medium">Performance: {campaign.performance}%</span>
                  <span className="text-pink-300 font-bold">{campaign.spend}</span>
                </div>
                <div className="mt-2 w-full bg-slate-700/50 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-pink-500 to-purple-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${campaign.performance}%` }}
                  />
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Demo Mode Indicator */}
      <div className="relative p-6 border-t border-purple-500/20">
        <div className="bg-gradient-to-r from-yellow-500/20 via-orange-500/20 to-red-500/20 border border-yellow-500/30 rounded-2xl p-4 backdrop-blur-sm">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <div className="w-3 h-3 bg-yellow-400 rounded-full animate-pulse"></div>
              <div className="absolute inset-0 w-3 h-3 bg-yellow-400 rounded-full animate-ping opacity-75"></div>
            </div>
            {!isCollapsed && (
              <div>
                <span className="text-yellow-400 text-sm font-bold">DEMO MODE</span>
                <p className="text-yellow-300/80 text-xs">Simulated data</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
