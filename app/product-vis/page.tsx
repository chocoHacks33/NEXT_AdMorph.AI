"use client"

import ProductVisAgent from "@/components/product-vis-agent-base"

export default function ProductVisualizationPage() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-indigo-50 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-6 text-indigo-800">
          Product Visualization Assistant
        </h1>
        
        <ProductVisAgent />
        
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>This agent will help understand your product to create accurate visual representations</p>
        </div>
      </div>
    </main>
  )
}
