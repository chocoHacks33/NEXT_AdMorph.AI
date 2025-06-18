"use client"

import React, { useState, useEffect, useRef } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { motion, AnimatePresence } from "framer-motion"
import {
  BarChart3,
  TrendingUp,
  TrendingDown,
  Eye,
  MousePointer,
  DollarSign,
  Users,
  Target,
  Zap,
  Activity,
  Clock,
  Award,
  Sparkles,
  ArrowUp,
  ArrowDown,
  RefreshCw,
  Download,
  Filter,
  Calendar,
  Globe,
  Smartphone,
  Monitor,
  ShoppingCart,
  Heart,
  Share2
} from "lucide-react"
import { useAnalytics, usePerformanceMetrics } from "@/lib/websocket-client"
import { toast } from "sonner"

interface AnalyticsData {
  overview: {
    totalImpressions: number
    totalClicks: number
    totalConversions: number
    totalSpend: number
    totalRevenue: number
    averageCTR: number
    averageConversionRate: number
    roi: number
  }
  campaigns: Array<{
    id: string
    name: string
    status: 'active' | 'paused' | 'completed'
    impressions: number
    clicks: number
    conversions: number
    spend: number
    revenue: number
    ctr: number
    conversionRate: number
    roi: number
  }>
  demographics: Array<{
    segment: string
    impressions: number
    clicks: number
    conversions: number
    ctr: number
    conversionRate: number
    revenue: number
  }>
  realTimeActivity: Array<{
    timestamp: string
    event: 'impression' | 'click' | 'conversion'
    campaign: string
    demographic: string
    value?: number
  }>
  trends: {
    impressions: number[]
    clicks: number[]
    conversions: number[]
    revenue: number[]
    labels: string[]
  }
}

interface AnalyticsDashboardProps {
  businessId?: string
}

export default function AnalyticsDashboard({ businessId }: AnalyticsDashboardProps) {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null)
  const [selectedTimeRange, setSelectedTimeRange] = useState<'1h' | '24h' | '7d' | '30d'>('24h')
  const [isLoading, setIsLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date())
  const [realTimeEvents, setRealTimeEvents] = useState<any[]>([])
  
  // WebSocket connections
  const { isConnected: analyticsConnected, lastMessage: analyticsMessage } = useAnalytics()
  const { isConnected: metricsConnected, lastMessage: metricsMessage } = usePerformanceMetrics()
  
  // Refs for animations
  const eventListRef = useRef<HTMLDivElement>(null)

  // Mock data for demonstration
  const mockAnalyticsData: AnalyticsData = {
    overview: {
      totalImpressions: 125430,
      totalClicks: 3876,
      totalConversions: 234,
      totalSpend: 2450.75,
      totalRevenue: 8920.50,
      averageCTR: 3.09,
      averageConversionRate: 6.04,
      roi: 264.2
    },
    campaigns: [
      {
        id: 'camp-1',
        name: 'Tech Enthusiasts Campaign',
        status: 'active',
        impressions: 45230,
        clicks: 1456,
        conversions: 89,
        spend: 890.25,
        revenue: 3240.80,
        ctr: 3.22,
        conversionRate: 6.11,
        roi: 264.0
      },
      {
        id: 'camp-2', 
        name: 'Business Professionals',
        status: 'active',
        impressions: 38920,
        clicks: 1234,
        conversions: 76,
        spend: 720.50,
        revenue: 2890.30,
        ctr: 3.17,
        conversionRate: 6.16,
        roi: 301.2
      },
      {
        id: 'camp-3',
        name: 'Fitness Enthusiasts',
        status: 'active',
        impressions: 41280,
        clicks: 1186,
        conversions: 69,
        spend: 840.00,
        revenue: 2789.40,
        ctr: 2.87,
        conversionRate: 5.82,
        roi: 232.1
      }
    ],
    demographics: [
      {
        segment: 'Tech Early Adopters',
        impressions: 45230,
        clicks: 1456,
        conversions: 89,
        ctr: 3.22,
        conversionRate: 6.11,
        revenue: 3240.80
      },
      {
        segment: 'Business Professionals',
        impressions: 38920,
        clicks: 1234,
        conversions: 76,
        ctr: 3.17,
        conversionRate: 6.16,
        revenue: 2890.30
      },
      {
        segment: 'Fitness Enthusiasts',
        impressions: 41280,
        clicks: 1186,
        conversions: 69,
        ctr: 2.87,
        conversionRate: 5.82,
        revenue: 2789.40
      }
    ],
    realTimeActivity: [],
    trends: {
      impressions: [12000, 15000, 18000, 22000, 25000, 28000, 32000],
      clicks: [380, 450, 520, 680, 750, 840, 980],
      conversions: [23, 28, 31, 41, 45, 52, 61],
      revenue: [890, 1120, 1340, 1680, 1890, 2140, 2450],
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    }
  }

  // Initialize with mock data
  useEffect(() => {
    setAnalyticsData(mockAnalyticsData)
    setIsLoading(false)
  }, [])

  // Handle real-time analytics updates
  useEffect(() => {
    if (analyticsMessage) {
      const message = analyticsMessage as any
      
      if (message.type === 'analytics_update') {
        const { data } = message
        
        // Update overview metrics
        if (data && analyticsData) {
          setAnalyticsData(prev => ({
            ...prev!,
            overview: {
              ...prev!.overview,
              totalImpressions: data.total_impressions || prev!.overview.totalImpressions,
              totalClicks: data.total_clicks || prev!.overview.totalClicks,
              totalConversions: data.total_conversions || prev!.overview.totalConversions,
              totalSpend: data.total_spend || prev!.overview.totalSpend,
              totalRevenue: data.total_revenue || prev!.overview.totalRevenue,
              roi: data.roi || prev!.overview.roi
            }
          }))
        }
        
        setLastUpdate(new Date())
      } else if (message.type === 'real_time_event') {
        // Add new real-time event
        const newEvent = {
          timestamp: new Date().toISOString(),
          event: message.event_type,
          campaign: message.campaign_name || 'Unknown Campaign',
          demographic: message.demographic || 'Unknown Segment',
          value: message.value
        }
        
        setRealTimeEvents(prev => [newEvent, ...prev.slice(0, 49)]) // Keep last 50 events
      }
    }
  }, [analyticsMessage, analyticsData])

  // Handle performance metrics updates
  useEffect(() => {
    if (metricsMessage) {
      const message = metricsMessage as any
      
      if (message.type === 'performance_update') {
        // Update campaign performance
        const { campaign_id, metrics } = message
        
        if (campaign_id && metrics && analyticsData) {
          setAnalyticsData(prev => ({
            ...prev!,
            campaigns: prev!.campaigns.map(campaign => 
              campaign.id === campaign_id 
                ? { ...campaign, ...metrics }
                : campaign
            )
          }))
        }
      }
    }
  }, [metricsMessage, analyticsData])

  // Simulate real-time events for demo
  useEffect(() => {
    const interval = setInterval(() => {
      const eventTypes = ['impression', 'click', 'conversion']
      const campaigns = ['Tech Enthusiasts Campaign', 'Business Professionals', 'Fitness Enthusiasts']
      const demographics = ['Tech Early Adopters', 'Business Professionals', 'Fitness Enthusiasts']
      
      const newEvent = {
        timestamp: new Date().toISOString(),
        event: eventTypes[Math.floor(Math.random() * eventTypes.length)] as 'impression' | 'click' | 'conversion',
        campaign: campaigns[Math.floor(Math.random() * campaigns.length)],
        demographic: demographics[Math.floor(Math.random() * demographics.length)],
        value: Math.random() * 100 + 10
      }
      
      setRealTimeEvents(prev => [newEvent, ...prev.slice(0, 49)])
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US').format(num)
  }

  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'impression': return <Eye className="h-4 w-4 text-blue-400" />
      case 'click': return <MousePointer className="h-4 w-4 text-green-400" />
      case 'conversion': return <ShoppingCart className="h-4 w-4 text-purple-400" />
      default: return <Activity className="h-4 w-4 text-gray-400" />
    }
  }

  const getEventColor = (eventType: string) => {
    switch (eventType) {
      case 'impression': return 'bg-blue-500/20 border-blue-500/30'
      case 'click': return 'bg-green-500/20 border-green-500/30'
      case 'conversion': return 'bg-purple-500/20 border-purple-500/30'
      default: return 'bg-gray-500/20 border-gray-500/30'
    }
  }

  if (isLoading || !analyticsData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 flex items-center justify-center">
        <Card className="bg-slate-900/50 backdrop-blur-xl border-purple-500/20 shadow-2xl p-16">
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl mx-auto mb-6 flex items-center justify-center">
              <BarChart3 className="h-8 w-8 text-white animate-pulse" />
            </div>
            <h2 className="text-2xl font-bold text-white mb-4">Loading Analytics...</h2>
            <div className="w-64 h-2 bg-slate-800 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full animate-pulse" />
            </div>
          </div>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-slate-900/10 to-pink-900/20" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-pink-500/10 rounded-full blur-3xl animate-pulse delay-1000" />

      <div className="max-w-7xl mx-auto px-6 py-12 relative z-10">
        {/* Header */}
        <div className="flex items-center justify-between mb-12">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent mb-2">
              Analytics Dashboard
            </h1>
            <p className="text-purple-300 flex items-center">
              <div className={`w-2 h-2 rounded-full mr-2 ${analyticsConnected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
              Last updated: {lastUpdate.toLocaleTimeString()}
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            <Button variant="outline" size="sm" className="bg-slate-800/50 border-slate-600">
              <Download className="h-4 w-4 mr-2" />
              Export
            </Button>
            <Button variant="outline" size="sm" className="bg-slate-800/50 border-slate-600">
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh
            </Button>
          </div>
        </div>

        {/* Overview Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card className="bg-slate-900/50 backdrop-blur-xl border-slate-700/30 shadow-xl rounded-2xl overflow-hidden">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center">
                    <Eye className="h-6 w-6 text-blue-400" />
                  </div>
                  <Badge className="bg-blue-500/20 text-blue-300 border-blue-500/30">
                    +12.5%
                  </Badge>
                </div>
                <div className="text-2xl font-bold text-white mb-1">
                  {formatNumber(analyticsData.overview.totalImpressions)}
                </div>
                <div className="text-sm text-slate-400">Total Impressions</div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card className="bg-slate-900/50 backdrop-blur-xl border-slate-700/30 shadow-xl rounded-2xl overflow-hidden">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-green-500/20 rounded-xl flex items-center justify-center">
                    <MousePointer className="h-6 w-6 text-green-400" />
                  </div>
                  <Badge className="bg-green-500/20 text-green-300 border-green-500/30">
                    +8.3%
                  </Badge>
                </div>
                <div className="text-2xl font-bold text-white mb-1">
                  {formatNumber(analyticsData.overview.totalClicks)}
                </div>
                <div className="text-sm text-slate-400">Total Clicks</div>
                <div className="text-xs text-green-400 mt-1">
                  {analyticsData.overview.averageCTR.toFixed(2)}% CTR
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card className="bg-slate-900/50 backdrop-blur-xl border-slate-700/30 shadow-xl rounded-2xl overflow-hidden">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center">
                    <ShoppingCart className="h-6 w-6 text-purple-400" />
                  </div>
                  <Badge className="bg-purple-500/20 text-purple-300 border-purple-500/30">
                    +15.7%
                  </Badge>
                </div>
                <div className="text-2xl font-bold text-white mb-1">
                  {formatNumber(analyticsData.overview.totalConversions)}
                </div>
                <div className="text-sm text-slate-400">Conversions</div>
                <div className="text-xs text-purple-400 mt-1">
                  {analyticsData.overview.averageConversionRate.toFixed(2)}% CVR
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card className="bg-slate-900/50 backdrop-blur-xl border-slate-700/30 shadow-xl rounded-2xl overflow-hidden">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-yellow-500/20 rounded-xl flex items-center justify-center">
                    <DollarSign className="h-6 w-6 text-yellow-400" />
                  </div>
                  <Badge className="bg-yellow-500/20 text-yellow-300 border-yellow-500/30">
                    +24.1%
                  </Badge>
                </div>
                <div className="text-2xl font-bold text-white mb-1">
                  {formatCurrency(analyticsData.overview.totalRevenue)}
                </div>
                <div className="text-sm text-slate-400">Revenue</div>
                <div className="text-xs text-yellow-400 mt-1">
                  {analyticsData.overview.roi.toFixed(1)}% ROI
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Real-time Activity Summary */}
        <Card className="bg-slate-900/50 backdrop-blur-xl border-slate-700/30 shadow-xl rounded-3xl overflow-hidden mb-12">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <Activity className="h-5 w-5 mr-2 text-green-400 animate-pulse" />
              Live Activity Summary
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-400 mb-2">
                  {realTimeEvents.filter(e => e.event === 'impression').length}
                </div>
                <div className="text-sm text-slate-400">Recent Impressions</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-400 mb-2">
                  {realTimeEvents.filter(e => e.event === 'click').length}
                </div>
                <div className="text-sm text-slate-400">Recent Clicks</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-400 mb-2">
                  {realTimeEvents.filter(e => e.event === 'conversion').length}
                </div>
                <div className="text-sm text-slate-400">Recent Conversions</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Campaign Performance */}
        <Card className="bg-slate-900/50 backdrop-blur-xl border-slate-700/30 shadow-xl rounded-3xl overflow-hidden">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <Target className="h-5 w-5 mr-2 text-purple-400" />
              Campaign Performance
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {analyticsData.campaigns.map((campaign, index) => (
                <motion.div
                  key={campaign.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-center justify-between p-4 bg-slate-800/30 rounded-xl border border-slate-700/50"
                >
                  <div className="flex items-center space-x-4">
                    <div className={`w-3 h-3 rounded-full ${
                      campaign.status === 'active' ? 'bg-green-400 animate-pulse' :
                      campaign.status === 'paused' ? 'bg-yellow-400' : 'bg-gray-400'
                    }`} />
                    <div>
                      <div className="text-white font-medium">{campaign.name}</div>
                      <div className="text-xs text-slate-400 capitalize">{campaign.status}</div>
                    </div>
                  </div>

                  <div className="grid grid-cols-4 gap-8 text-center">
                    <div>
                      <div className="text-white font-bold">{formatNumber(campaign.impressions)}</div>
                      <div className="text-xs text-slate-400">Impressions</div>
                    </div>
                    <div>
                      <div className="text-white font-bold">{campaign.clicks}</div>
                      <div className="text-xs text-slate-400">Clicks</div>
                    </div>
                    <div>
                      <div className="text-white font-bold">{campaign.conversions}</div>
                      <div className="text-xs text-slate-400">Conversions</div>
                    </div>
                    <div>
                      <div className="text-green-400 font-bold">{formatCurrency(campaign.revenue)}</div>
                      <div className="text-xs text-slate-400">{campaign.roi.toFixed(1)}% ROI</div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
