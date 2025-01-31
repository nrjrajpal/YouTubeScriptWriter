'use client'

import { Anton, Maven_Pro, Montserrat } from 'next/font/google'
import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import ScrollTrigger from 'gsap/ScrollTrigger'

const anton = Anton({
  weight: '400',
  subsets: ['latin'],
})

const mavenPro = Maven_Pro({
  weight: '500',
  subsets: ['latin'],
})

const montserrat300 = Montserrat({
  weight: '300',
})
const montserrat600 = Montserrat({
  weight: '600',
})

// FAQ data as a constant object
const FAQs = [
  {
    question: 'How does the system collect data for scriptwriting?',
    answer: 'The system gathers content from reliable sources such as YouTube video transcripts, research papers, articles, blogs, and custom user content.',
  },
  {
    question: 'Can I use the system for any type of YouTube content',
    answer: 'Yes, the system is designed to cater to diverse YouTube content genres, allowing you to customize titles, viewer questions, and data sources for specific requirements.',
  },
  {
    question: 'Does the system help with audience retention strategies?',
    answer: 'The scripts incorporate audience retention strategies to keep viewers engaged throughout the video.',
  },
  {
    question: 'Can the system generate scripts in different languages?',
    answer: 'Currently, the system supports English scripts. We are working on adding support for other languages in the future.',
  },
]

export default function Hero() {
  const headingRef = useRef<HTMLDivElement>(null)
  const subTextRef = useRef<HTMLDivElement>(null)
  const faqTextRef = useRef<HTMLDivElement>(null)
  const faqContentRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger)

    // Animate heading and subtitle
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
        filter: 'blur(10px)',
      })

      // Animate subtitle lines
      tl.from(
        Array.from(subTextLines),
        {
          duration: 0.5,
          opacity: 0,
          y: 20,
          stagger: 0.2,
          ease: 'power3.out',
        },
        '-=0.5' // Start slightly before the heading animation ends
      )
    }

    // Animate the FAQs heading
    if (faqTextRef.current) {
      gsap.fromTo(
        faqTextRef.current,
        { opacity: 0, scaleY: '350%', y: 50, filter: 'blur(10px)'},
        {
          filter: 'blur(0px)',
          opacity: 1,
          scaleY: '100%',
          y: 0,
          ease: 'circ.inOut',
          duration: 1.5,
          scrollTrigger: {
            trigger: faqTextRef.current,
            start: 'top 90%',
            end: 'top 10%',
            toggleActions: 'restart none none reverse',
          },
        }
      )
    }

    // Animate individual FAQ pairs
    if (faqContentRef.current) {
      const faqPairs = Array.from(faqContentRef.current.children) as HTMLDivElement[]
      gsap.fromTo(
        faqPairs,
        { opacity: 0, y: 50, filter: 'blur(15px)' },
        {
          filter: 'blur(0px)',
          opacity: 1,
          y: 0,
          ease: 'circ.inOut',
          duration: 1.5,
          stagger: 0.3, // Add delay between animations
          scrollTrigger: {
            trigger: faqContentRef.current,
            start: 'top 70%',
            end: 'top 10%',
            toggleActions: 'restart none none reverse',
          },
        }
      )
    }
  }, [])

  return (
    <div>
      {/* Section 1: Heading and Subtext */}
      <section className="min-h-screen bg-black flex items-center justify-center px-4">
        <div className="max-w-6xl mx-auto text-center">
          <h1
            ref={headingRef}
            className={`${anton.className} text-white text-4xl sm:text-5xl md:text-6xl lg:text-7xl leading-tight mb-8`}
          >
            {['ELIMINATE','YOUR','SCRIPTWRITING','HASSLES,','GENERATE','ENGAGING','SCRIPTS'].map((word, index) => (
              <span key={index} className="inline-block mr-2">
                {word}
              </span>
            ))}
          </h1>
          <div
            ref={subTextRef}
            className={`${montserrat300.className} text-white text-sm sm:text-base md:text-lg lg:text-xl max-w-3xl mx-auto mb-12`}
          >
            <p>EFFORTLESSLY TRANSFORM YOUR YOUTUBE VIDEO IDEAS INTO</p>
            <p>CAPTIVATING, WELL-RESEARCHED SCRIPTS IN MINUTES</p>
          </div>
        </div>
      </section>


      <section className="bg-black py-16">
        <div
          ref={faqTextRef}
          className={`${anton.className} w-full flex justify-center items-center text-center text-white text-3xl sm:text-4xl md:text-5xl lg:text-6xl leading-snug`}
        >
          FAQs
        </div>
        <div
          ref={faqContentRef}
          className="w-full flex flex-col justify-center items-center text-center text-white text-sm leading-snug px-4"
        >
          {FAQs.map((faq, index) => (
            <div
              key={index}
              className="max-w-3xl" 
            >
              <br/><br/><br/>
              <p className={`${montserrat600.className} mb-4`}>{faq.question}</p>
              <p className={`${montserrat300.className}`}>{faq.answer}</p>
            </div>
          ))}
        </div>
      </section>


      <section className="bg-black py-16 mt-20">
        <div className="justify-center items-center text-center">Section</div>
      </section>
      <section className="bg-black py-16 mt-20">
        <div className="justify-center items-center text-center">Section</div>
      </section>
      <section className="bg-black py-16 mt-20">
        <div className="justify-center items-center text-center">Contact Us</div>
      </section>
    </div>
  )
}
