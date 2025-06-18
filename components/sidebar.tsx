"use client"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Plus, ChevronLeft, ChevronRight, Sparkles, Calendar, TrendingUp, Eye } from "lucide-react"

interface LaunchedCampaign {
  id: string
  name: string
  thumbnail: string
  status: "active" | "completed"
  launchDate: Date
  selectedAds: string[]
  businessData: {
    targetEngagement: string
    budget: string
    audience: string
    themes: string[]
  }
}

interface SidebarProps {
  isCollapsed: boolean
  onToggle: () => void
  launchedCampaigns?: LaunchedCampaign[]
  onCampaignSelect?: (campaignId: string) => void
}

export default function Sidebar({ isCollapsed, onToggle, launchedCampaigns = [], onCampaignSelect }: SidebarProps) {
  const formatDate = (date: Date) => {
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
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

      {/* New Campaign Button */}
      <div className="relative p-6 border-b border-purple-500/20">
        <Button
          size={isCollapsed ? "icon" : "lg"}
          className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 rounded-2xl shadow-lg shadow-purple-500/25 transition-all duration-300 hover:scale-105 w-full"
        >
          <Plus className="h-5 w-5" />
          {!isCollapsed && <span className="ml-3 text-lg font-medium">New Campaign</span>}
        </Button>
      </div>

      {/* Campaigns List */}
      <div className="flex-1 relative">
        {!isCollapsed && (
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-white font-semibold text-lg">Campaigns</h3>
              <Badge className="bg-purple-500/20 text-purple-300 border-purple-500/30 rounded-full px-2 py-1 text-xs">
                {launchedCampaigns.length}
              </Badge>
            </div>

            <ScrollArea className="h-96">
              <div className="space-y-4">
                {launchedCampaigns.length === 0 ? (
                  <div className="text-center py-8">
                    <div className="w-16 h-16 bg-slate-800/50 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-slate-700/50">
                      <TrendingUp className="h-8 w-8 text-slate-500" />
                    </div>
                    <p className="text-slate-400 text-sm">No campaigns yet</p>
                    <p className="text-slate-500 text-xs mt-1">Launch your first campaign to see it here</p>
                  </div>
                ) : (
                  launchedCampaigns.map((campaign) => (
                    <div
                      key={campaign.id}
                      onClick={() => onCampaignSelect?.(campaign.id)}
                      className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-4 border border-slate-700/30 hover:border-purple-500/30 transition-all duration-300 cursor-pointer hover:bg-slate-700/50 group"
                    >
                      <div className="flex items-start space-x-4">
                        {/* Campaign Thumbnail */}
                        <div className="relative">
                          <img
                            src={campaign.thumbnail || "/placeholder.svg"}
                            alt={campaign.name}
                            className="w-12 h-12 object-cover rounded-xl border border-slate-600/50 group-hover:border-purple-500/30 transition-all duration-300"
                          />
                          <div
                            className={`absolute -top-1 -right-1 w-3 h-3 rounded-full border border-slate-950 ${
                              campaign.status === "active" ? "bg-green-400 animate-pulse" : "bg-blue-400"
                            }`}
                          />
                        </div>

                        {/* Campaign Info */}
                        <div className="flex-1 min-w-0">
                          <h4 className="text-white font-medium text-sm truncate group-hover:text-purple-300 transition-colors">
                            {campaign.name}
                          </h4>
                          <div className="flex items-center space-x-2 mt-1">
                            <Badge
                              className={`text-xs px-2 py-0.5 rounded-full ${
                                campaign.status === "active"
                                  ? "bg-green-500/20 text-green-400 border-green-500/30"
                                  : "bg-blue-500/20 text-blue-400 border-blue-500/30"
                              }`}
                            >
                              {campaign.status}
                            </Badge>
                            <span className="text-slate-500 text-xs">{campaign.selectedAds.length} ads</span>
                          </div>

                          {/* Launch Date */}
                          <div className="flex items-center space-x-1 mt-2">
                            <Calendar className="h-3 w-3 text-slate-500" />
                            <span className="text-slate-500 text-xs">{formatDate(campaign.launchDate)}</span>
                          </div>

                          {/* Quick Stats */}
                          <div className="flex items-center space-x-3 mt-2">
                            <div className="flex items-center space-x-1">
                              <Eye className="h-3 w-3 text-slate-500" />
                              <span className="text-slate-500 text-xs">2.4K</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <TrendingUp className="h-3 w-3 text-green-400" />
                              <span className="text-green-400 text-xs">+12%</span>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Campaign Preview on Hover */}
                      <div className="mt-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                        <div className="text-xs text-slate-400 truncate">{campaign.businessData.audience}</div>
                        <div className="text-xs text-slate-500 mt-1">Budget: {campaign.businessData.budget}</div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </ScrollArea>
          </div>
        )}

        {/* Collapsed View - Show Campaign Count */}
        {isCollapsed && launchedCampaigns.length > 0 && (
          <div className="p-4">
            <div className="bg-slate-800/50 rounded-2xl p-3 border border-slate-700/30 text-center">
              <TrendingUp className="h-6 w-6 text-purple-400 mx-auto mb-2" />
              <Badge className="bg-purple-500/20 text-purple-300 border-purple-500/30 rounded-full text-xs">
                {launchedCampaigns.length}
              </Badge>
            </div>
          </div>
        )}
      </div>

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
