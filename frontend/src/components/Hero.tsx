'use client'

import { Anton, Maven_Pro } from 'next/font/google'
import { useEffect, useRef } from 'react'
import gsap from 'gsap'

const anton = Anton({
  weight: '400',
  subsets: ['latin'],
})

const mavenPro = Maven_Pro({
  weight: '500',
  subsets: ['latin'],
})

export default function Hero() {
  const headingRef = useRef<HTMLDivElement>(null)
  const subTextRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const headingWords = headingRef.current?.querySelectorAll('span')
    const subTextLines = subTextRef.current?.querySelectorAll('p')

    if (headingWords && subTextLines) {
      const tl = gsap.timeline()
      
      // Animate heading words
      tl.from(Array.from(headingWords), {
        duration: 1,
        opacity: 0,
        y: 30,
        stagger: 0.1,
        ease: 'power4.out',
        filter: 'blur(10px)'
      })

      // Animate subtitle lines
      tl.from(Array.from(subTextLines), {
        duration: 0.5,
        opacity: 0,
        y: 20,
        stagger: 0.2,
        ease: 'power3.out',
      }, '-=0.5s') // Start slightly before the heading animation ends
    }
  }, [])

  return (
    <section className="min-h-screen bg-black flex items-center justify-center px-4">
      <div className="max-w-6xl mx-auto text-center">
        <h1 
          ref={headingRef}
          className={`${anton.className} text-white text-4xl sm:text-5xl md:text-6xl lg:text-7xl leading-tight mb-8`}
        >
          {['ELIMINATE', 'YOUR', 'SCRIPTWRITING', 'HASSLES,', 'GENERATE', 'ENGAGING', 'SCRIPTS'].map((word, index) => (
            <span key={index} className="inline-block mr-2">{word}</span>
          ))}
        </h1>
        <div 
          ref={subTextRef}
          className={`${mavenPro.className} text-white text-sm sm:text-base md:text-lg lg:text-xl max-w-3xl mx-auto`}
        >
          <p>EFFORTLESSLY TRANSFORM YOUR YOUTUBE VIDEO IDEAS INTO</p>
          <p>CAPTIVATING, WELL-RESEARCHED SCRIPTS IN MINUTES</p>
        </div>
      </div>
    </section>
  )
}

