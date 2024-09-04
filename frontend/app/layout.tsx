/** @format */
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"], display: 'swap', adjustFontFallback: false });

export const metadata: Metadata = {
  title: "App intranet",
  description: "App intrane"
};

export default function RootLayout({children}: {children: React.ReactNode;}) {

  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/Logo-Blocos-Coloridos.ico" />
      </head>
      <body
        className={cn(
          "min-h-screen w-full bg-white text-black flex ",
          inter.className,
          {
            "debug-screens": process.env.NODE_ENV === "development"
          }
        )}
      >
        {/* sidebar */}
        {/* <p className="border">Sidebar</p> */}
        {/* main page */}
        {children}
      </body>
    </html>
  );
}
