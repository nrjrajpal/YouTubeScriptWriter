'use client'

import * as React from 'react'
import { useSignUp } from '@clerk/nextjs'
import { useRouter } from 'next/navigation'
import { isClerkAPIResponseError } from '@clerk/nextjs/errors'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { TriangleIcon as ExclamationTriangle, Eye, EyeOff } from 'lucide-react'
import Link from 'next/link'
import { OTPInput } from '@/components/OTPInput'

export default function SignUpForm() {
    const { isLoaded, signUp, setActive } = useSignUp()
    const [emailAddress, setEmailAddress] = React.useState('')
    const [password, setPassword] = React.useState('')
    const [verifying, setVerifying] = React.useState(false)
    const [code, setCode] = React.useState('')
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
            setIsEmailValid(validateEmail(emailAddress))
        }
    }, [emailAddress, isEmailTouched])

    const handleEmailBlur = () => {
        setIsEmailTouched(true)
        setIsEmailValid(validateEmail(emailAddress))
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError(null)

        if (!isLoaded) return

        try {
            await signUp.create({
                emailAddress,
                password,
            })

            await signUp.prepareEmailAddressVerification({
                strategy: 'email_code',
            })

            setVerifying(true)
        } catch (err) {
            if (isClerkAPIResponseError(err)) {
                setError(err.errors[0].longMessage || 'An error occurred during sign-up. Please try again.')
            } else {
                setError('An unexpected error occurred. Please try again later.')
            }
        }
    }

    const handleVerify = async (e: React.FormEvent) => {
        e.preventDefault()
        setError(null)

        if (!isLoaded) return

        try {
            const signUpAttempt = await signUp.attemptEmailAddressVerification({
                code,
            })

            if (signUpAttempt.status === 'complete') {
                await setActive({ session: signUpAttempt.createdSessionId })
                router.push('/')
            } else {
                setError('Verification incomplete. Please try again.')
            }
        } catch (err) {
            if (isClerkAPIResponseError(err)) {
                setError(err.errors[0].longMessage || 'An error occurred during verification. Please try again.')
            } else {
                setError('An unexpected error occurred. Please try again later.')
            }
        }
    }

    const renderForm = () => {
        if (verifying) {
            return (
                <form onSubmit={handleVerify} className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="code">Enter your verification code</Label>
                        <OTPInput
                            value={code}
                            valueLength={6}
                            onChange={(value) => setCode(value)}
                        />
                    </div>
                    <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white">Verify</Button>
                </form>
            )
        }

        return (
            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                    <Label htmlFor="email">Email address</Label>
                    <Input
                        id="email"
                        type="email"
                        value={emailAddress}
                        onChange={(e) => setEmailAddress(e.target.value)}
                        onBlur={handleEmailBlur}
                        placeholder="you@example.com"
                        className="bg-gray-800 border-gray-700 text-white placeholder-gray-400 h-fit w-full text-base"
                    />
                    {isEmailTouched && !isEmailValid && (
                        <p className="text-sm text-red-500">Please enter a valid email address.</p>
                    )}
                </div>
                <div className="space-y-2">
                    <Label htmlFor="password">Password</Label>
                    <div className="relative">
                        <Input
                            id="password"
                            type={showPassword ? "text" : "password"}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="bg-gray-800 border-gray-700 text-white placeholder-gray-400 pr-10 h-fit w-full text-base"
                            placeholder="Enter your password"
                        />
                        <Button
                            type="button"
                            variant="ghost"
                            size="icon"
                            className="absolute right-0 top-0 h-full text-gray-400 hover:text-white mr-2"
                            onClick={() => setShowPassword(!showPassword)}
                        >
                            {showPassword ? (
                                <EyeOff size={22} />
                            ) : (
                                <Eye size={22} />
                            )}
                        </Button>
                    </div>
                </div>
                <Button
                    type="submit"
                    disabled={!isEmailValid || !password}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                >
                    Sign up
                </Button>
                {/* <Button type="submit" className="w-full">Sign up</Button> */}
            </form>
        )
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-950 p-4">
            <Card className="w-full max-w-md bg-gray-900 text-gray-100">
                <CardHeader>
                    <CardTitle className="text-2xl font-bold text-center">
                        {verifying ? 'Verify your email' : 'Sign up'}
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    {renderForm()}
                    {error && (
                        <Alert variant="destructive" className="mt-4 bg-red-900/50 border border-red-600 text-red-100">
                            <ExclamationTriangle className="h-4 w-4 mr-2" />
                            <AlertDescription>{error}</AlertDescription>
                        </Alert>
                    )}
                </CardContent>
                <CardFooter className="flex justify-center">
                    <p className="text-sm text-gray-400">
                        {verifying ? (
                            // "Didn't receive the code? " 
                            ""
                        ) : (
                            <>
                                Already have an account?{' '}
                                <Link href="/sign-in" className="text-blue-400 hover:underline">
                                    Sign in
                                </Link>
                            </>
                        )}
                    </p>
                </CardFooter>
            </Card>
        </div>
    )
}

