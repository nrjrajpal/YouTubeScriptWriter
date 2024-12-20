'use client'

import * as React from 'react'
import { useSignIn } from '@clerk/nextjs'
import { useRouter } from 'next/navigation'
import { isClerkAPIResponseError } from '@clerk/nextjs/errors'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { TriangleIcon as ExclamationTriangle, Eye, EyeOff } from 'lucide-react'
import Link from 'next/link'

export default function SignInForm() {
    const { isLoaded, signIn, setActive } = useSignIn()
    const [email, setEmail] = React.useState('')
    const [password, setPassword] = React.useState('')
    const [error, setError] = React.useState<string | null>(null)
    const [isEmailValid, setIsEmailValid] = React.useState(true)
    const [isEmailTouched, setIsEmailTouched] = React.useState(false)
    const [showPassword, setShowPassword] = React.useState(false)

    const router = useRouter()

    const validateEmail = (email: string) => {
        const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
        return re.test(email)
    }

    React.useEffect(() => {
        if (isEmailTouched) {
            setIsEmailValid(validateEmail(email))
        }
    }, [email, isEmailTouched])

    const handleEmailBlur = () => {
        setIsEmailTouched(true)
        setIsEmailValid(validateEmail(email))
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError(null)

        if (!isLoaded) {
            return
        }

        try {
            const signInAttempt = await signIn.create({
                identifier: email,
                password,
            })

            if (signInAttempt.status === 'complete') {
                await setActive({ session: signInAttempt.createdSessionId })
                router.push('/')
            } else {
                setError('Sign-in process incomplete. Please try again.')
            }
        } catch (err) {
            if (isClerkAPIResponseError(err)) {
                const clerkError = err.errors[0]
                if (clerkError.code === 'form_identifier_not_found') {
                    setError("We couldn't find an account with that email. Please check your email or sign up if you don't have an account.")
                } else {
                    setError(clerkError.longMessage || 'An error occurred during sign-in. Please try again.')
                }
            } else {
                setError('An unexpected error occurred. Please try again later.')
            }
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-950 p-4">
            <Card className="w-full max-w-md bg-gray-900 text-gray-100">
                <CardHeader>
                    <CardTitle className="text-2xl font-bold text-center">Sign in</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="email" className="text-sm font-medium text-gray-300">
                                Email address
                            </Label>
                            <Input
                                onChange={(e) => setEmail(e.target.value)}
                                onBlur={handleEmailBlur}
                                id="email"
                                name="email"
                                type="email"
                                required
                                className="bg-gray-800 border-gray-700 text-white placeholder-gray-400"
                                placeholder="you@example.com"
                                value={email}
                            />
                            {isEmailTouched && !isEmailValid && (
                                <p className="text-sm text-red-500">Please enter a valid email address.</p>
                            )}
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="password" className="text-sm font-medium text-gray-300">
                                Password
                            </Label>
                            <div className="relative">
                                <Input
                                    onChange={(e) => setPassword(e.target.value)}
                                    id="password"
                                    name="password"
                                    type={showPassword ? "text" : "password"}
                                    required
                                    className="bg-gray-800 border-gray-700 text-white placeholder-gray-400 pr-10"
                                    placeholder="Enter your password"
                                    value={password}
                                />
                                <Button
                                    type="button"
                                    variant="ghost"
                                    size="icon"
                                    className="absolute right-0 top-0 h-full px-3 text-gray-400 hover:text-white"
                                    onClick={() => setShowPassword(!showPassword)}
                                >
                                    {showPassword ? (
                                        <EyeOff className="h-4 w-4" />
                                    ) : (
                                        <Eye className="h-4 w-4" />
                                    )}
                                </Button>
                            </div>
                        </div>
                        <Button
                            type="submit"
                            disabled={!isEmailValid || !password}
                            className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                        >
                            Sign in
                        </Button>
                    </form>

                    {error && (
                        <Alert variant="destructive" className="mt-4 bg-red-900/50 border border-red-600 text-red-100">
                            <ExclamationTriangle className="h-4 w-4 mr-2" />
                            <AlertDescription>{error}</AlertDescription>
                        </Alert>
                    )}
                </CardContent>
                <CardFooter className="flex justify-center">
                    <p className="text-sm text-gray-400">
                        <>
                            Don't have an account?{' '}
                            <Link href="/sign-up" className="text-blue-400 hover:underline">
                                Sign up
                            </Link>
                        </>
                    </p>
                </CardFooter>
            </Card>
        </div>
    )
}

