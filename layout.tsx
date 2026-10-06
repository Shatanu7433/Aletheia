import "./globals.css";
import type { Metadata } from "next";
import Link from "next/link";
import { Inter, Instrument_Serif } from "next/font/google";
import Sky from "@/components/Sky";

const sans = Inter({ subsets: ["latin"], variable: "--font-sans" });
const serif = Instrument_Serif({ subsets: ["latin"], weight: "400", variable: "--font-serif" });

export const metadata: Metadata = { title: "Aletheia — research, cited", description: "Ask anything. Get a report with its sources." };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${sans.variable} ${serif.variable}`}>
      <body>
        <Sky />
        <header className="absolute inset-x-0 top-0 z-10">
          <nav className="mx-auto flex h-24 max-w-6xl items-center justify-between px-6">
            <Link href="/" className="font-serif text-3xl tracking-tight">Aletheia<sup className="text-xs">®</sup></Link>
            <div className="hidden gap-9 text-[15px] text-white/90 md:flex">
              <Link href="/" className="hover:text-white">Home</Link>
              <Link href="/#recent" className="hover:text-white">Recent</Link>
              <Link href="/#how" className="hover:text-white">How it works</Link>
            </div>
            <Link href="/" className="glass rounded-full px-6 py-3 text-[15px] transition hover:bg-white hover:text-night">New research</Link>
          </nav>
        </header>
        {children}
      </body>
    </html>
  );
}
