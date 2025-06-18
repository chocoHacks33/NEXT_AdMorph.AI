"use client"

import React, { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { motion, AnimatePresence } from "framer-motion"
import {
  ShoppingBag,
  Sparkles,
  Target,
  TrendingUp,
  Users,
  Zap,
  Star,
  Heart,
  ShoppingCart,
  Eye,
  MousePointer,
  DollarSign,
  BarChart3,
  Loader2,
  CheckCircle,
  ArrowRight,
  Package,
  Palette,
  MessageSquare,
  Clock,
  Award
} from "lucide-react"
import { usePersonalizationUpdates, useAnalytics } from "@/lib/websocket-client"
import { toast } from "sonner"

interface Product {
  id: string
  name: string
  description: string
  price: number
  category: string
  features: string[]
  images: string[]
  platform: string
}

interface ProductVariant {
  id: string
  productId: string
  demographicSegment: string
  personalizedTitle: string
  personalizedDescription: string
  highlightedFeatures: string[]
  personalizedCta: string
  pricePositioning: string
  urgencyMessaging: string
  socialProof: string[]
  personalizationScore: number
  conversionLiftEstimate: number
  realTimeMetrics?: {
    views: number
    clicks: number
    purchases: number
    revenue: number
    conversionRate: number
  }
}

interface DemographicSegment {
  id: string
  name: string
  ageRange: [number, number]
  interests: string[]
  behaviors: string[]
  psychographics: Record<string, string>
}

interface EcommercePersonalizationProps {
  onComplete?: (variants: ProductVariant[]) => void
}

export default function EcommercePersonalization({ onComplete }: EcommercePersonalizationProps) {
  const [currentStep, setCurrentStep] = useState<"setup" | "processing" | "variants" | "testing">("setup")
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null)
  const [selectedSegments, setSelectedSegments] = useState<string[]>([])
  const [generatedVariants, setGeneratedVariants] = useState<ProductVariant[]>([])
  const [processingProgress, setProcessingProgress] = useState(0)
  const [currentProcessingStep, setCurrentProcessingStep] = useState("")
  const [isGenerating, setIsGenerating] = useState(false)
  
  // WebSocket connections
  const { isConnected: personalizationConnected, lastMessage: personalizationMessage } = usePersonalizationUpdates()
  const { isConnected: analyticsConnected, lastMessage: analyticsMessage } = useAnalytics()

  // Sample data
  const sampleProducts: Product[] = [
    {
      id: "prod-1",
      name: "Premium Wireless Headphones",
      description: "High-quality wireless headphones with noise cancellation",
      price: 299.99,
      category: "Electronics",
      features: ["Noise Cancellation", "30hr Battery", "Premium Sound", "Comfortable Fit"],
      images: ["/headphones-1.jpg", "/headphones-2.jpg"],
      platform: "shopify"
    },
    {
      id: "prod-2", 
      name: "Organic Skincare Set",
      description: "Complete organic skincare routine for healthy, glowing skin",
      price: 89.99,
      category: "Beauty",
      features: ["100% Organic", "Cruelty-Free", "Dermatologist Tested", "All Skin Types"],
      images: ["/skincare-1.jpg", "/skincare-2.jpg"],
      platform: "shopify"
    },
    {
      id: "prod-3",
      name: "Smart Fitness Tracker",
      description: "Advanced fitness tracker with health monitoring features",
      price: 199.99,
      category: "Fitness",
      features: ["Heart Rate Monitor", "Sleep Tracking", "GPS", "Waterproof"],
      images: ["/fitness-1.jpg", "/fitness-2.jpg"],
      platform: "amazon"
    }
  ]

  const demographicSegments: DemographicSegment[] = [
    {
      id: "fitness-enthusiasts",
      name: "Fitness Enthusiasts",
      ageRange: [22, 40],
      interests: ["fitness", "health", "wellness", "sports"],
      behaviors: ["gym_membership", "health_app_usage", "supplement_purchases"],
      psychographics: { lifestyle: "active", values: "health,performance" }
    },
    {
      id: "business-professionals",
      name: "Business Professionals", 
      ageRange: [28, 45],
      interests: ["business", "technology", "productivity", "networking"],
      behaviors: ["linkedin_usage", "business_travel", "premium_subscriptions"],
      psychographics: { lifestyle: "busy", values: "efficiency,success" }
    },
    {
      id: "tech-early-adopters",
      name: "Tech Early Adopters",
      ageRange: [25, 35],
      interests: ["technology", "gadgets", "innovation", "gaming"],
      behaviors: ["early_tech_adoption", "online_reviews", "social_sharing"],
      psychographics: { lifestyle: "digital", values: "innovation,convenience" }
    },
    {
      id: "conscious-consumers",
      name: "Conscious Consumers",
      ageRange: [25, 45],
      interests: ["sustainability", "organic", "ethical_brands", "wellness"],
      behaviors: ["eco_friendly_purchases", "brand_research", "social_causes"],
      psychographics: { lifestyle: "mindful", values: "sustainability,authenticity" }
    }
  ]

  // Handle personalization updates
  useEffect(() => {
    if (personalizationMessage) {
      const message = personalizationMessage as any
      
      if (message.type === 'personalization_update') {
        const { status, progress, result } = message
        
        if (progress !== undefined) {
          setProcessingProgress(progress)
        }
        
        if (status === 'completed' && result) {
          setGeneratedVariants(result.personalized_variants || [])
          setCurrentStep("variants")
          toast.success('Product personalization completed!')
        } else if (status === 'failed') {
          toast.error('Personalization failed. Please try again.')
          setCurrentStep("setup")
        }
        
        // Update processing step based on progress
        if (progress < 25) {
          setCurrentProcessingStep("Analyzing product features...")
        } else if (progress < 50) {
          setCurrentProcessingStep("Understanding demographic preferences...")
        } else if (progress < 75) {
          setCurrentProcessingStep("Generating personalized variants...")
        } else if (progress < 100) {
          setCurrentProcessingStep("Optimizing conversion potential...")
        } else {
          setCurrentProcessingStep("Personalization complete!")
        }
      }
    }
  }, [personalizationMessage])

  // Handle analytics updates for variant performance
  useEffect(() => {
    if (analyticsMessage) {
      const message = analyticsMessage as any
      
      if (message.type === 'analytics_update') {
        // Update variant metrics with real-time data
        setGeneratedVariants(prev => prev.map(variant => ({
          ...variant,
          realTimeMetrics: {
            views: Math.floor(Math.random() * 1000) + 100,
            clicks: Math.floor(Math.random() * 100) + 10,
            purchases: Math.floor(Math.random() * 20) + 1,
            revenue: Math.floor(Math.random() * 1000) + 100,
            conversionRate: Math.random() * 5 + 1
          }
        })))
      }
    }
  }, [analyticsMessage])

  const handleProductSelect = (product: Product) => {
    setSelectedProduct(product)
  }

  const handleSegmentToggle = (segmentId: string) => {
    setSelectedSegments(prev => 
      prev.includes(segmentId) 
        ? prev.filter(id => id !== segmentId)
        : [...prev, segmentId]
    )
  }

  const handleGenerateVariants = async () => {
    if (!selectedProduct || selectedSegments.length === 0) {
      toast.error('Please select a product and at least one demographic segment')
      return
    }

    setIsGenerating(true)
    setCurrentStep("processing")
    setProcessingProgress(0)
    setCurrentProcessingStep("Initializing personalization engine...")

    // Simulate processing with gradual progress
    const progressInterval = setInterval(() => {
      setProcessingProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval)
          return 100
        }
        return prev + Math.random() * 10
      })
    }, 500)

    // Simulate completion after 5 seconds
    setTimeout(() => {
      clearInterval(progressInterval)
      setProcessingProgress(100)
      
      // Generate mock variants
      const mockVariants: ProductVariant[] = selectedSegments.map((segmentId, index) => {
        const segment = demographicSegments.find(s => s.id === segmentId)!
        return {
          id: `variant-${index + 1}`,
          productId: selectedProduct.id,
          demographicSegment: segment.name,
          personalizedTitle: `${selectedProduct.name} - Perfect for ${segment.name}`,
          personalizedDescription: `Specially crafted for ${segment.name.toLowerCase()} who value ${segment.psychographics.values}`,
          highlightedFeatures: selectedProduct.features.slice(0, 3),
          personalizedCta: segment.id === 'business-professionals' ? 'Boost Your Productivity' : 
                           segment.id === 'fitness-enthusiasts' ? 'Enhance Your Performance' :
                           segment.id === 'tech-early-adopters' ? 'Get Cutting-Edge Tech' : 'Shop Consciously',
          pricePositioning: 'Premium quality at competitive price',
          urgencyMessaging: 'Limited time offer - 20% off',
          socialProof: ['Loved by thousands', '5-star rated', 'Recommended by experts'],
          personalizationScore: Math.random() * 0.3 + 0.7, // 70-100%
          conversionLiftEstimate: Math.random() * 25 + 15, // 15-40%
          realTimeMetrics: {
            views: Math.floor(Math.random() * 1000) + 100,
            clicks: Math.floor(Math.random() * 100) + 10,
            purchases: Math.floor(Math.random() * 20) + 1,
            revenue: Math.floor(Math.random() * 1000) + 100,
            conversionRate: Math.random() * 5 + 1
          }
        }
      })
      
      setGeneratedVariants(mockVariants)
      setCurrentStep("variants")
      setIsGenerating(false)
      toast.success('Product variants generated successfully!')
    }, 5000)
  }

  const handleStartABTest = () => {
    setCurrentStep("testing")
    toast.success('A/B test started for all variants!')
  }

  if (currentStep === "setup") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 relative overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-slate-900/10 to-pink-900/20" />
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-pink-500/10 rounded-full blur-3xl animate-pulse delay-1000" />

        <div className="max-w-6xl mx-auto px-6 py-12 relative z-10">
          {/* Header */}
          <div className="text-center mb-16">
            <div className="flex items-center justify-center mb-6">
              <div className="relative">
                <div className="w-20 h-20 bg-gradient-to-br from-pink-500 via-purple-500 to-blue-500 rounded-3xl flex items-center justify-center shadow-2xl shadow-purple-500/25">
                  <ShoppingBag className="h-10 w-10 text-white animate-pulse" />
                </div>
                <div className="absolute -top-2 -right-2 w-6 h-6 bg-green-400 rounded-full border-2 border-slate-950 animate-pulse" />
              </div>
            </div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-pink-400 via-purple-400 to-blue-400 bg-clip-text text-transparent mb-4">
              E-commerce Personalization
            </h1>
            <p className="text-xl text-purple-300 font-medium">Create personalized product experiences for every customer segment</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Product Selection */}
            <Card className="bg-slate-900/50 backdrop-blur-xl border-purple-500/20 shadow-2xl shadow-purple-500/10 rounded-3xl overflow-hidden">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Package className="h-6 w-6 mr-2 text-purple-400" />
                  Select Product
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {sampleProducts.map((product) => (
                  <motion.div
                    key={product.id}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <Card 
                      className={`cursor-pointer transition-all duration-300 ${
                        selectedProduct?.id === product.id 
                          ? 'bg-purple-500/20 border-purple-500/50' 
                          : 'bg-slate-800/50 border-slate-700/50 hover:bg-slate-700/50'
                      }`}
                      onClick={() => handleProductSelect(product)}
                    >
                      <CardContent className="p-4">
                        <div className="flex items-start justify-between mb-2">
                          <h3 className="font-semibold text-white">{product.name}</h3>
                          <Badge variant="outline" className="text-xs">
                            ${product.price}
                          </Badge>
                        </div>
                        <p className="text-sm text-slate-400 mb-3">{product.description}</p>
                        <div className="flex flex-wrap gap-2">
                          {product.features.slice(0, 3).map((feature, index) => (
                            <Badge key={index} variant="secondary" className="text-xs">
                              {feature}
                            </Badge>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </CardContent>
            </Card>

            {/* Demographic Segments */}
            <Card className="bg-slate-900/50 backdrop-blur-xl border-purple-500/20 shadow-2xl shadow-purple-500/10 rounded-3xl overflow-hidden">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Users className="h-6 w-6 mr-2 text-blue-400" />
                  Target Segments
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {demographicSegments.map((segment) => (
                  <motion.div
                    key={segment.id}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <Card 
                      className={`cursor-pointer transition-all duration-300 ${
                        selectedSegments.includes(segment.id)
                          ? 'bg-blue-500/20 border-blue-500/50' 
                          : 'bg-slate-800/50 border-slate-700/50 hover:bg-slate-700/50'
                      }`}
                      onClick={() => handleSegmentToggle(segment.id)}
                    >
                      <CardContent className="p-4">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="font-semibold text-white">{segment.name}</h3>
                          {selectedSegments.includes(segment.id) && (
                            <CheckCircle className="h-5 w-5 text-blue-400" />
                          )}
                        </div>
                        <p className="text-sm text-slate-400 mb-2">
                          Ages {segment.ageRange[0]}-{segment.ageRange[1]}
                        </p>
                        <div className="flex flex-wrap gap-1">
                          {segment.interests.slice(0, 3).map((interest, index) => (
                            <Badge key={index} variant="outline" className="text-xs">
                              {interest}
                            </Badge>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Generate Button */}
          <div className="text-center mt-12">
            <Button
              onClick={handleGenerateVariants}
              disabled={!selectedProduct || selectedSegments.length === 0 || isGenerating}
              size="lg"
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-2xl px-12 py-4 text-lg font-medium shadow-xl shadow-purple-500/25 transition-all duration-300 hover:scale-105 disabled:opacity-50 disabled:scale-100"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Sparkles className="h-5 w-5 mr-2" />
                  Generate Personalized Variants
                </>
              )}
            </Button>
            {selectedProduct && selectedSegments.length > 0 && (
              <p className="text-slate-400 mt-4">
                Will generate {selectedSegments.length} personalized variant{selectedSegments.length > 1 ? 's' : ''} for {selectedProduct.name}
              </p>
            )}
          </div>
        </div>
      </div>
    )
  }

  // Processing view
  if (currentStep === "processing") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 relative overflow-hidden flex items-center justify-center">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/20 via-slate-900/10 to-pink-900/20" />

        <Card className="bg-slate-900/50 backdrop-blur-xl border-purple-500/20 shadow-2xl shadow-purple-500/10 rounded-3xl p-16 max-w-2xl w-full mx-6">
          <div className="text-center">
            <div className="w-32 h-32 bg-gradient-to-br from-pink-500 via-purple-600 to-blue-600 rounded-3xl mx-auto mb-10 flex items-center justify-center shadow-2xl shadow-purple-500/25 relative">
              <Sparkles className="h-16 w-16 text-white animate-pulse" />
              <div className="absolute -top-2 -right-2 w-8 h-8 bg-green-400 rounded-full border-2 border-slate-950 animate-pulse" />
            </div>

            <h2 className="text-3xl font-bold text-white mb-6">AI Personalization Engine</h2>
            <p className="text-xl text-purple-300 mb-10 font-medium">{currentProcessingStep}</p>

            <div className="mb-10">
              <div className="flex justify-between text-lg text-slate-300 mb-4 font-medium">
                <span>Personalization Progress</span>
                <span>{Math.round(processingProgress)}%</span>
              </div>
              <Progress value={processingProgress} className="w-full h-4" />
            </div>

            <div className="flex items-center justify-center space-x-3 text-purple-300">
              <div className="relative">
                <div className="w-3 h-3 bg-pink-500 rounded-full animate-ping"></div>
                <div className="absolute inset-0 w-3 h-3 bg-pink-500 rounded-full animate-pulse"></div>
              </div>
              <p className="text-lg font-medium">Creating personalized experiences...</p>
            </div>
          </div>
        </Card>
      </div>
    )
  }

  return null
}
