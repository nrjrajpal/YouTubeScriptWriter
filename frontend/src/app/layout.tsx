
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ClerkProvider, SignedIn, UserButton } from '@clerk/nextjs'
import { dark } from '@clerk/themes'
// import { Button } from "@/components/ui/button";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "YouTube Script Writer",
  description: "The AI Pseudo-Agent powered YouTube Script Writer",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider appearance={{
      baseTheme: dark,
      layout: {
        unsafe_disableDevelopmentModeWarnings: true,
      }
    }}>
      <html lang="en" className="dark">
        <body
          className={`${geistSans.variable} ${geistMono.variable} antialiased bg-black`}
        >
          {/* <header className="flex justify-end w-screen p-2"> */}
          <header className="absolute end-0 p-4">
            {/* <SignedOut>
              <SignInButton >
                <Button>Log In</Button>
                </SignInButton>
                </SignedOut> */}
            <SignedIn>
              <UserButton appearance={{
                elements: {
                  userButtonAvatarBox: {
                    height: 40,
                    width: 40,
                  },
                  userButtonAvatarImage: {
                    height: 40,
                    width: 40,
                  }
                }
              }} />
              {/* <p className="text-white pl-4">Profile</p> */}
            </SignedIn>
          </header>
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
