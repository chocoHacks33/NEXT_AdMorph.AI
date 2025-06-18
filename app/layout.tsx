import type { Metadata } from 'next'
import './globals.css'

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
      <body>{children}</body>
    </html>
  )
}
