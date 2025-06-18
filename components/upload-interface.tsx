"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Upload, FileImage, FileVideo, ArrowRight, SkipBackIcon as Skip, CheckCircle, Sparkles } from "lucide-react"

interface BusinessData {
  targetEngagement: string
  budget: string
  audience: string
  themes: string[]
  originalAd?: File
}

interface UploadInterfaceProps {
  businessData: BusinessData
  onComplete: (file?: File) => void
}

export default function UploadInterface({ businessData, onComplete }: UploadInterfaceProps) {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [isDragging, setIsDragging] = useState(false)

  const handleFileUpload = (file: File) => {
    setUploadedFile(file)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    if (file && (file.type.startsWith("image/") || file.type.startsWith("video/"))) {
      handleFileUpload(file)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleContinue = () => {
    onComplete(uploadedFile || undefined)
  }

  const handleSkip = () => {
    onComplete()
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 relative overflow-hidden">
      {/* Elegant Background */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-purple-900/15 via-transparent to-pink-900/15" />
      <div className="absolute top-1/4 left-1/3 w-96 h-96 bg-purple-500/8 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 right-1/3 w-96 h-96 bg-pink-500/8 rounded-full blur-3xl animate-pulse delay-1000" />

      <div className="max-w-3xl mx-auto px-6 py-16 relative z-10">
        {/* Elegant Header */}
        <div className="text-center mb-16">
          <div className="flex items-center justify-center mb-6">
            <div className="w-16 h-16 bg-gradient-to-br from-orange-500 via-pink-500 to-purple-500 rounded-3xl flex items-center justify-center shadow-2xl shadow-purple-500/20">
              <Upload className="h-8 w-8 text-white" />
            </div>
          </div>
          <h1 className="text-4xl font-light bg-gradient-to-r from-white via-orange-200 to-pink-200 bg-clip-text text-transparent mb-4">
            Upload Your Current Ad
          </h1>
          <p className="text-xl text-slate-400">Help AI understand your brand style</p>
        </div>

        {/* Progress Steps */}
        <div className="mb-16">
          <div className="flex justify-center">
            <div className="flex items-center space-x-6">
              <div className="flex flex-col items-center">
                <div className="w-10 h-10 rounded-full bg-gradient-to-r from-green-400 to-emerald-500 text-white flex items-center justify-center shadow-lg">
                  <CheckCircle className="h-5 w-5" />
                </div>
                <p className="text-xs text-slate-400 mt-2 font-medium">Voice Setup</p>
              </div>
              <div className="w-12 h-0.5 bg-gradient-to-r from-green-400 to-orange-500"></div>
              <div className="flex flex-col items-center">
                <div className="w-10 h-10 rounded-full bg-gradient-to-r from-orange-500 to-pink-500 text-white flex items-center justify-center animate-pulse shadow-lg">
                  <Upload className="h-5 w-5" />
                </div>
                <p className="text-xs text-slate-400 mt-2 font-medium">Upload Ad</p>
              </div>
              <div className="w-12 h-0.5 bg-slate-600"></div>
              <div className="flex flex-col items-center">
                <div className="w-10 h-10 rounded-full bg-slate-700 text-slate-400 flex items-center justify-center">
                  <span className="text-sm font-medium">3</span>
                </div>
                <p className="text-xs text-slate-400 mt-2 font-medium">Processing</p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Upload Area */}
        <div className="flex justify-center mb-12">
          <Card className="bg-slate-900/40 backdrop-blur-2xl border-slate-700/30 shadow-2xl rounded-3xl p-12 max-w-2xl w-full relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-orange-500/5 via-pink-500/5 to-purple-500/5" />
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-orange-500 via-pink-500 to-purple-500" />

            <div className="text-center relative">
              {!uploadedFile ? (
                <>
                  {/* Upload Drop Zone */}
                  <div
                    className={`border-2 border-dashed rounded-3xl p-12 transition-all duration-500 ${
                      isDragging
                        ? "border-purple-400/50 bg-purple-500/10 scale-105"
                        : "border-slate-600/50 hover:border-slate-500/50"
                    }`}
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                  >
                    <div className="w-20 h-20 bg-gradient-to-br from-orange-500 via-pink-500 to-purple-500 rounded-3xl mx-auto mb-8 flex items-center justify-center shadow-xl">
                      <Upload className="h-10 w-10 text-white" />
                    </div>

                    <h3 className="text-2xl font-semibold text-white mb-3">Drop your ad here</h3>
                    <p className="text-slate-400 mb-8 text-lg">Or click to browse files</p>

                    <div className="relative">
                      <input
                        type="file"
                        accept="image/*,video/*"
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                        onChange={(e) => {
                          const file = e.target.files?.[0]
                          if (file) handleFileUpload(file)
                        }}
                      />
                      <Button className="bg-gradient-to-r from-orange-500 to-pink-500 hover:from-orange-600 hover:to-pink-600 text-white rounded-2xl px-10 py-4 text-lg font-medium shadow-xl transition-all duration-300 hover:scale-105">
                        Choose File
                      </Button>
                    </div>

                    <p className="text-sm text-slate-500 mt-6">Supports JPG, PNG, MP4, MOV up to 10MB</p>
                  </div>
                </>
              ) : (
                <>
                  {/* File Preview */}
                  <div className="p-8 bg-slate-800/50 backdrop-blur-sm rounded-3xl mb-8 border border-slate-600/30">
                    <div className="flex items-center justify-center space-x-6">
                      <div className="w-16 h-16 bg-gradient-to-r from-green-400 to-emerald-500 rounded-2xl flex items-center justify-center shadow-lg">
                        {uploadedFile.type.startsWith("image/") ? (
                          <FileImage className="h-8 w-8 text-white" />
                        ) : (
                          <FileVideo className="h-8 w-8 text-white" />
                        )}
                      </div>
                      <div className="text-left">
                        <p className="font-semibold text-white text-lg">{uploadedFile.name}</p>
                        <p className="text-slate-400">{(uploadedFile.size / 1024 / 1024).toFixed(1)} MB</p>
                      </div>
                      <CheckCircle className="h-8 w-8 text-green-400" />
                    </div>
                  </div>

                  <p className="text-slate-300 mb-8 text-lg">
                    Perfect! This will help AI understand your brand style and create better variants.
                  </p>

                  <Button
                    onClick={() => setUploadedFile(null)}
                    variant="outline"
                    className="bg-slate-800/50 backdrop-blur-sm border-slate-600/50 text-slate-300 hover:bg-slate-700/50 hover:text-white rounded-xl"
                  >
                    Upload Different File
                  </Button>
                </>
              )}
            </div>
          </Card>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center space-x-6 mb-16">
          <Button
            onClick={handleSkip}
            variant="outline"
            className="bg-slate-900/50 backdrop-blur-xl border-slate-600/30 text-slate-300 hover:text-white hover:bg-slate-800/50 rounded-2xl px-8 py-3 transition-all duration-300"
          >
            <Skip className="h-4 w-4 mr-2" />
            Skip This Step
          </Button>

          <Button
            onClick={handleContinue}
            className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-2xl px-10 py-3 font-medium shadow-xl transition-all duration-300 hover:scale-105"
          >
            Continue
            <ArrowRight className="h-4 w-4 ml-2" />
          </Button>
        </div>

        {/* Info Section */}
        <div className="flex justify-center">
          <Card className="bg-slate-900/30 backdrop-blur-xl border-slate-700/30 shadow-lg rounded-3xl p-8 max-w-lg">
            <h3 className="text-xl font-semibold text-white mb-6 text-center flex items-center justify-center">
              <Sparkles className="h-5 w-5 mr-2 text-purple-400" />
              Why Upload Your Ad?
            </h3>
            <div className="space-y-4 text-slate-300">
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                <p>AI learns your brand colors and style</p>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-pink-400 rounded-full"></div>
                <p>Better variant generation based on your current creative</p>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                <p>Maintains brand consistency across new ads</p>
              </div>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <p>Improves targeting accuracy</p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
