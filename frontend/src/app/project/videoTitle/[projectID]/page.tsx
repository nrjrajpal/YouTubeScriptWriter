'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { useUser } from '@clerk/nextjs'
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Loader2 } from 'lucide-react'
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Skeleton } from "@/components/ui/skeleton"

export default function VideoTitleSelector() {
    const [titles, setTitles] = useState<string[]>([])
    const [selectedTitle, setSelectedTitle] = useState('')
    const [customTitle, setCustomTitle] = useState('')
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [successMessage, setSuccessMessage] = useState<string | null>(null)

    const params = useParams()
    const router = useRouter()
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
                setSelectedTitle(data.titles[0]) // Select the first title by default
            } else {
                setError(data.error || 'Failed to fetch video titles')
            }
        } catch (error) {
            setError('An error occurred while fetching video titles')
        } finally {
            setIsLoading(false)
        }
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!user?.primaryEmailAddress?.emailAddress) return

        const finalTitle = selectedTitle === 'custom' ? customTitle : selectedTitle

        setIsLoading(true)
        setError(null)
        setSuccessMessage(null)

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/setVideoTitle`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    userEmail: user.primaryEmailAddress.emailAddress,
                    projectID: projectID,
                    videoTitle: finalTitle
                }),
            })

            const data = await response.json()

            if (data.success) {
                setSuccessMessage(data.message)
                // Redirect to the selectQuestions page
                router.push(`/project/selectQuestions/${projectID}`)
            } else {
                setError(data.error || 'Failed to set video title')
            }
        } catch (error) {
            setError('An error occurred while setting the video title')
        } finally {
            setIsLoading(false)
        }
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
            <h1 className="text-4xl font-bold mb-8">Select Video Title</h1>
            <div className="bg-gray-800 p-8 rounded-lg shadow-md w-[32rem]">
                <form onSubmit={handleSubmit} className="text-lg">
                    <RadioGroup value={selectedTitle} onValueChange={setSelectedTitle} className="space-y-4">
                        {isLoading ? (
                            <>
                                <Skeleton className="h-6 w-full" />
                                <Skeleton className="h-6 w-full" />
                                <Skeleton className="h-6 w-full" />
                            </>
                        ) : (
                            titles.map((title, index) => (
                                <div key={index} className="flex items-center space-x-2">
                                    <RadioGroupItem value={title} id={`title-${index}`} />
                                    <Label htmlFor={`title-${index}`} className="text-white">{title}</Label>
                                </div>
                            ))
                        )}
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
                    <div className="flex space-x-4 mt-6">
                        <Button type="submit" className="flex-1 bg-blue-600 hover:bg-blue-700 text-white">
                            Submit
                        </Button>
                        <Button type="button" onClick={fetchVideoTitles} className="flex-1 bg-green-600 hover:bg-green-700 text-white">
                            Regenerate Titles
                        </Button>
                    </div>
                </form>
                {successMessage && (
                    <Alert className="mt-4 bg-green-700 text-white">
                        <AlertTitle>Success</AlertTitle>
                        <AlertDescription>{successMessage}</AlertDescription>
                    </Alert>
                )}
                {error && (
                    <Alert className="mt-4 bg-red-700 text-white">
                        <AlertTitle>Error</AlertTitle>
                        <AlertDescription>{error}</AlertDescription>
                    </Alert>
                )}
            </div>
        </div>
    )
}

