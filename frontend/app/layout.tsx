import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";


const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "StayDesk - AI-Powered Hotel Email Management",
  description: "Automate your hotel email responses with AI. Get instant availability, pricing, and booking links sent to your guests.",
  keywords: ["hotel management", "AI", "email automation", "booking system", "hospitality"],
  authors: [{ name: "StayDesk Team" }],
  openGraph: {
    title: "StayDesk - AI-Powered Hotel Email Management",
    description: "Automate your hotel email responses with AI. Get instant availability, pricing, and booking links sent to your guests.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-gray-50 dark:bg-gray-900`}
      >
        {children}
      </body>
    </html>
  );
}
