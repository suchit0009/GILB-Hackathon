import './globals.css'
import { Inter, JetBrains_Mono } from 'next/font/google'

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' })
const mono = JetBrains_Mono({ subsets: ['latin'], variable: '--font-mono' })

export const metadata = {
    title: 'SENTINEL FORTRESS | SOC',
    description: 'Active Defense Fraud Detection System',
}

export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <body className={`${inter.variable} ${mono.variable} font-sans antialiased`}>{children}</body>
        </html>
    )
}
