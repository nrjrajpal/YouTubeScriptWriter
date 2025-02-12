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
            const response = await fetch('http://localhost:5000/setAPIKeys', {
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
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
        } catch (err) { 
            setError('An error occurred while setting API keys')
        }
    }

    const isFormValid = groqKey && tavilyKey && serperKey

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-950 p-4">
            <Card className="w-full max-w-md bg-gray-900 text-gray-100">
                <CardHeader>
                    <CardTitle className="text-2xl font-bold text-center">Welcome to the Onboarding Process</CardTitle>
                    <CardDescription className="text-center text-gray-400">
                        Please provide your API keys to enable communication with the LLM and web information retrieval.
                        These keys are free to use up to certain limits.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="groqKey">Groq API Key</Label>
                            <Input
                                id="groqKey"
                                type="password"
                                value={groqKey}
                                onChange={(e) => setGroqKey(e.target.value)}
                                required
                                className="bg-gray-800 border-gray-700 text-white placeholder-gray-400"
                                placeholder="Enter your Groq API key"
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="tavilyKey">Tavily API Key</Label>
                            <Input
                                id="tavilyKey"
                                type="password"
                                value={tavilyKey}
                                onChange={(e) => setTavilyKey(e.target.value)}
                                required
                                className="bg-gray-800 border-gray-700 text-white placeholder-gray-400"
                                placeholder="Enter your Tavily API key"
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="serperKey">Serper API Key</Label>
                            <Input
                                id="serperKey"
                                type="password"
                                value={serperKey}
                                onChange={(e) => setSerperKey(e.target.value)}
                                required
                                className="bg-gray-800 border-gray-700 text-white placeholder-gray-400"
                                placeholder="Enter your Serper API key"
                            />
                        </div>
                        {error && (
                            <Alert variant="destructive" className="mt-4 bg-red-900/50 border border-red-600 text-red-100">
                                <ExclamationTriangleIcon className="h-4 w-4 mr-2" />
                                <AlertDescription>{error}</AlertDescription>
                            </Alert>
                        )}
                        <Button
                            type="submit"
                            disabled={!isFormValid || !isLoaded || !isSignedIn}
                            className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                        >
                            Complete Onboarding
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}

