import type { Metadata } from 'next'
import './globals.css'
import NavBar from '@/components/nav-bar'

export const metadata: Metadata = {
  title: 'AdMorph.AI',
  description: 'AI-powered ad morphing and optimization platform',
  generator: 'AdMorph.AI',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>
        <NavBar />
        {children}
      </body>
    </html>
  )
}
