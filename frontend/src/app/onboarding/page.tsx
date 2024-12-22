'use client'

import * as React from 'react'
import { useUser } from '@clerk/nextjs'
import { useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ExclamationTriangleIcon } from '@radix-ui/react-icons'
import { completeOnboarding } from './_actions'

export default function OnboardingComponent() {
    const [error, setError] = React.useState('')
    const [groqKey, setGroqKey] = React.useState('')
    const [tavilyKey, setTavilyKey] = React.useState('')
    const [serperKey, setSerperKey] = React.useState('')
    const { isLoaded, isSignedIn, user } = useUser()
    const router = useRouter()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')

        if (!isLoaded || !isSignedIn || !user?.primaryEmailAddress?.emailAddress) {
            setError('User information is not available. Please try again.')
            return
        }
        const formData = new FormData(e.target as HTMLFormElement)
        const res = await completeOnboarding(formData)
        if (res?.message) {
            // Reloads the user's data from the Clerk API
            await user?.reload()
            router.push('/')
        }
        if (res?.error) {
            setError(res?.error)
        }

        const apiKeys = {
            userEmail: user.primaryEmailAddress.emailAddress,
            userID: user.id,
            groqAPIKey: groqKey,
            serperAPIKey: serperKey,
            tavilyAPIKey: tavilyKey
        }

        try {
            // First, set the API keys
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/setAPIKeys`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(apiKeys),
            })

            const result = await response.json()

            if (result.success) {
                // If API keys are set successfully, complete the onboarding
                const formData = new FormData()
                formData.append('applicationName', 'DefaultApp') // You might want to adjust these values
                formData.append('applicationType', 'DefaultType')

                const onboardingResult = await completeOnboarding(formData)

                if (onboardingResult.message) {
                    router.push('/dashboard')
                } else if (onboardingResult.error) {
                    setError(onboardingResult.error)
                }
            } else {
                setError(result.error || 'Failed to set API keys')
            }
        } catch (err) {
            setError('An error occurred while setting API keys')
        }
    }

    const isFormValid = groqKey && tavilyKey && serperKey

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-950 p-4">
            <div className="rounded-2xl w-1/2 h-auto bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px] shadow-lg">
                <div className="bg-black rounded-2xl flex justify-center items-center py-4 px-4">

                    <Card className="w-full border-none bg-transparent text-gray-100">
                        <CardHeader>
                            <CardTitle className="text-4xl font-bold text-center mb-6">One last step...</CardTitle>
                            <CardDescription className="text-center text-gray-400 px-12">
                                Please provide your API keys to enable communication with the LLM and web information retrieval.
                                These keys are free to use up to certain limits.
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={handleSubmit} className="space-y-4">
                                <div className="space-y-2 py-2">
                                    {/* <Label htmlFor="groqKey">Groq API Key</Label> */}
                                    <Input
                                        id="groqKey"
                                        type="password"
                                        value={groqKey}
                                        onChange={(e) => setGroqKey(e.target.value)}
                                        required
                                        className="bg-gray-800 border-gray-700 text-white placeholder-gray-400 h-fit w-full"
                                        placeholder="Enter your Groq API key"
                                    />
                                </div>
                                <div className="space-y-2 py-2">
                                    {/* <Label htmlFor="tavilyKey">Tavily API Key</Label> */}
                                    <Input
                                        id="tavilyKey"
                                        type="password"
                                        value={tavilyKey}
                                        onChange={(e) => setTavilyKey(e.target.value)}
                                        required
                                        className="bg-gray-800 border-gray-700 text-white placeholder-gray-400 h-fit w-full"
                                        placeholder="Enter your Tavily API key"
                                    />
                                </div>
                                <div className="space-y-2 py-2">
                                    {/* <Label htmlFor="serperKey">Serper API Key</Label> */}
                                    <Input
                                        id="serperKey"
                                        type="password"
                                        value={serperKey}
                                        onChange={(e) => setSerperKey(e.target.value)}
                                        required
                                        className="bg-gray-800 border-gray-700 text-white placeholder-gray-400 h-fit w-full disabled:pointer-events-auto"
                                        placeholder="Enter your Serper API key"
                                    />
                                </div>
                                {error && (
                                    <Alert variant="destructive" className="mt-4 bg-red-900/50 border border-red-600 text-red-100">
                                        <ExclamationTriangleIcon className="h-4 w-4 mr-2" />
                                        <AlertDescription>{error}</AlertDescription>
                                    </Alert>
                                )}

                                {(isFormValid && isLoaded && isSignedIn) && (
                                    <>
                                        <div className="absolute inset-0 blur-xl rounded-full w-auto h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradientbg ease-out p-[3px] opacity-0 group-hover:border-none transition-opacity"></div>
                                        <div className="relative flex rounded-full w-full h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[3px]">
                                            <Button
                                                type="submit"
                                                variant={"gradient"}
                                                className="h-full w-full rounded-full pb-[10px] text-3xl font-medium disabled: bg-black">
                                                Complete Onboarding
                                            </Button>
                                        </div>
                                    </>
                                )}
                                {(!isFormValid || !isLoaded || !isSignedIn) && (
                                    <div>
                                        <div className="relative flex rounded-full w-full h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[3px] group-disabled:bg-black">
                                        <Button
                                            type="submit"
                                            variant={"gradient"}
                                            disabled={!isFormValid || !isLoaded || !isSignedIn}
                                            className="h-full w-full rounded-full pb-[10px] text-3xl font-medium bg-gray-700">
                                            Complete Onboarding
                                        </Button>
                                        </div>
                                    </div>
                                )}
                            </form>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div >
    )
}

