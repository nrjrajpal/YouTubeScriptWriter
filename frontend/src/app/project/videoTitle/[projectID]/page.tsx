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
            <div className="min-h-screen flex items-center justify-center bg-black text-white">
                <Loader2 className="h-8 w-8 animate-spin" />
            </div>
        )
    }

    if (error) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-black text-white">
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
        // <div className="min-h-screen flex flex-col items-center justify-center bg-black text-white">
        <div className="h-svh flex flex-row items-center justify-center bg-black ">
            <div className="-mt-12 rounded-2xl h-fit w-1/2 bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px] shadow-lg">
                <div className="bg-black w-full h-full rounded-2xl flex flex-col justify-center items-center">
                    <h1 className="text-3xl font-script font-bold mt-8">Select Video Title</h1>
                    <div className="p-8 rounded-lg shadow-md w-[32rem]">
                        <form onSubmit={handleSubmit} className="text-lg">
                            <RadioGroup value={selectedTitle} onValueChange={setSelectedTitle} className="font-script space-y-4">
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
                                            <Label htmlFor={`title-${index}`} className="text-white font-medium text-sm">{title}</Label>
                                        </div>
                                    ))
                                )}
                                <div className="flex items-center space-x-2">
                                    <RadioGroupItem value="custom" id="custom-title" />
                                    <Label htmlFor="custom-title" className="text-white text-sm">Custom Video Title</Label>
                                </div>
                            </RadioGroup>
                            <Input
                                type="text"
                                placeholder="Enter custom title"
                                value={customTitle}
                                onChange={(e) => setCustomTitle(e.target.value)}
                                disabled={selectedTitle !== 'custom'}
                                className="font-script rounded-xl my-4 mb-6 bg-gray-700 text-white text-sm placeholder-gray-400 border-gray-600 focus:border-blue-500 w-full h-fit"
                            />
                            <div className="flex flex-col gap-4">
                                <div className="h-fit relative group flex w-full justify-center mx-auto">
                                    <div className="absolute inset-0 blur-lg rounded-2xl w-auto h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradientbg ease-out p-[2px] opacity-0 group-hover:opacity-100 transition-opacity"></div>
                                    <div className="relative flex rounded-2xl w-full h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px]">
                                        <Button type="button" onClick={fetchVideoTitles} variant={"gradient"} className="font-script flex-1 h-full w-full rounded-2xl pb-[10px] text-xl font-medium">
                                            Regenerate Titles
                                        </Button>
                                    </div>
                                </div>
                                <div className="h-fit relative group flex w-full justify-center mx-auto">
                                    <div className="absolute inset-0 blur-lg rounded-2xl w-auto h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradientbg ease-out p-[2px] opacity-0 group-hover:opacity-100 transition-opacity"></div>
                                    <div className="relative flex rounded-2xl w-full h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px]">
                                        <Button type="submit" variant={"gradient"} className="font-script flex-1 h-full w-full rounded-2xl pb-[10px] text-xl font-medium">
                                            Submit
                                        </Button>
                                    </div>
                                </div>
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
            </div>
        </div>
    )
}

