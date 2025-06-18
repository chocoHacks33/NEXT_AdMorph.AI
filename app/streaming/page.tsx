"use client"

import { useState } from "react"
import StreamingChatInterface from "@/components/streaming-chat-interface"

export default function StreamingPage() {
  const [completed, setCompleted] = useState(false)
  const [businessData, setBusinessData] = useState<any>(null)
  
  const handleComplete = (data: any) => {
    setBusinessData(data)
    setCompleted(true)
  }
  
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-purple-50 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-6 text-purple-800">
          AdMorph.AI - Streaming Voice Interface
        </h1>
        
        {completed ? (
          <div className="bg-white rounded-xl p-6 shadow-lg">
            <h2 className="text-2xl font-semibold mb-4">Your Ad Campaign Details</h2>
            <div className="space-y-4">
              <div>
                <h3 className="font-medium text-gray-700">Target Engagement</h3>
                <p className="text-gray-900">{businessData.targetEngagement}</p>
              </div>
              
              <div>
                <h3 className="font-medium text-gray-700">Budget</h3>
                <p className="text-gray-900">{businessData.budget}</p>
              </div>
              
              <div>
                <h3 className="font-medium text-gray-700">Target Audience</h3>
                <p className="text-gray-900">{businessData.audience}</p>
              </div>
              
              <div>
                <h3 className="font-medium text-gray-700">Themes & Messaging</h3>
                <div className="flex flex-wrap gap-2">
                  {businessData.themes.map((theme: string, i: number) => (
                    <span key={i} className="bg-purple-100 text-purple-800 px-2 py-1 rounded-full text-sm">
                      {theme}
                    </span>
                  ))}
                </div>
              </div>
              
              <div>
                <h3 className="font-medium text-gray-700">Original Ad</h3>
                {businessData.originalAd ? (
                  <p className="text-gray-900">Uploaded: {businessData.originalAd.name}</p>
                ) : (
                  <p className="text-gray-500">No ad file uploaded</p>
                )}
              </div>
              
              <div className="pt-4">
                <button
                  onClick={() => setCompleted(false)}
                  className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors"
                >
                  Start New Campaign
                </button>
              </div>
            </div>
          </div>
        ) : (
          <StreamingChatInterface onComplete={handleComplete} />
        )}
      </div>
    </main>
  )
}
