"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Mic, Workflow, Image as ImageIcon } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function NavBar() {
  const pathname = usePathname()

  return (
    <div className="bg-slate-900/80 backdrop-blur-xl border-b border-purple-500/20 relative">
      <div className="max-w-7xl mx-auto px-4 py-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="bg-gradient-to-r from-purple-500 to-pink-500 p-2 rounded-lg">
              <Mic className="h-5 w-5 text-white" />
            </div>
            <span className="font-bold text-white text-xl tracking-tight">AdMorph.AI</span>
          </div>

          <div className="flex space-x-2">
            <Link href="/" passHref>
              <Button
                variant={pathname === "/" ? "default" : "outline"} 
                size="sm"
                className="flex items-center space-x-1"
              >
                <Workflow className="h-4 w-4 mr-1" />
                <span>Original App</span>
              </Button>
            </Link>
            <Link href="/streaming" passHref>
              <Button
                variant={pathname === "/streaming" ? "default" : "outline"}
                size="sm" 
                className="flex items-center space-x-1"
              >
                <Mic className="h-4 w-4 mr-1" />
                <span>Streaming Voice</span>
              </Button>
            </Link>
            <Link href="/product-vis" passHref>
              <Button
                variant={pathname === "/product-vis" ? "default" : "outline"}
                size="sm" 
                className="flex items-center space-x-1"
              >
                <ImageIcon className="h-4 w-4 mr-1" />
                <span>Product Visualization</span>
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
