'use client'
import Hero from '@/components/Hero'
export const runtime = "edge";
export default function Home() {
  return (
    <div>
      <h1 className="text-2xl font-bold">
        <Hero />
      </h1>
    </div>
  );
}
