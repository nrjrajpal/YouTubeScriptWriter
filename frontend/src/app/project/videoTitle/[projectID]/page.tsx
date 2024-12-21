'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { useUser } from '@clerk/nextjs'
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Loader2 } from 'lucide-react'

export default function VideoTitleSelector() {
    const [titles, setTitles] = useState<string[]>([])
    const [selectedTitle, setSelectedTitle] = useState('')
    const [customTitle, setCustomTitle] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const params = useParams()
    const projectID = params.projectID as string
    const { isLoaded, isSignedIn, user } = useUser()

    useEffect(() => {
        if (isLoaded && isSignedIn && projectID) {
            fetchVideoTitles()
        }
    }, [isLoaded, isSignedIn, projectID])

    const fetchVideoTitles = async () => {
        if (!user?.primaryEmailAddress?.emailAddress) return

        setIsLoading(true)
        setError(null)

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/generateVideoTitles`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    userEmail: user.primaryEmailAddress.emailAddress,
                    projectID: projectID
                }),
            })

            const data = await response.json()

            if (data.success) {
                setTitles(data.titles)
            } else {
                setError(data.error || 'Failed to fetch video titles')
            }
        } catch (error) {
            setError('An error occurred while fetching video titles')
        } finally {
            setIsLoading(false)
        }
    }

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        const finalTitle = selectedTitle === 'custom' ? customTitle : selectedTitle
        console.log('Selected title:', finalTitle)
        // Here you would typically send the selected title back to your backend
    }

    if (isLoading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
                <Loader2 className="h-8 w-8 animate-spin" />
            </div>
        )
    }

    if (error) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
                <div className="text-center">
                    <h1 className="text-2xl font-bold mb-4">Error</h1>
                    <p>{error}</p>
                    <Button onClick={fetchVideoTitles} className="mt-4">
                        Try Again
                    </Button>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white">
            <h1 className="text-3xl font-bold mb-8">Select Video Title</h1>
            <div className="bg-gray-800 p-8 rounded-lg shadow-md w-96">
                <form onSubmit={handleSubmit}>
                    <RadioGroup value={selectedTitle} onValueChange={setSelectedTitle} className="space-y-4">
                        {titles.map((title, index) => (
                            <div key={index} className="flex items-center space-x-2">
                                <RadioGroupItem value={title} id={`title-${index}`} />
                                <Label htmlFor={`title-${index}`} className="text-white">{title}</Label>
                            </div>
                        ))}
                        <div className="flex items-center space-x-2">
                            <RadioGroupItem value="custom" id="custom-title" />
                            <Label htmlFor="custom-title" className="text-white">Custom Video Title</Label>
                        </div>
                    </RadioGroup>
                    <Input
                        type="text"
                        placeholder="Enter custom title"
                        value={customTitle}
                        onChange={(e) => setCustomTitle(e.target.value)}
                        disabled={selectedTitle !== 'custom'}
                        className="mt-4 bg-gray-700 text-white placeholder-gray-400 border-gray-600 focus:border-blue-500"
                    />
                    <Button type="submit" className="mt-6 w-full bg-blue-600 hover:bg-blue-700 text-white">
                        Submit
                    </Button>
                </form>
            </div>
        </div>
    )
}

