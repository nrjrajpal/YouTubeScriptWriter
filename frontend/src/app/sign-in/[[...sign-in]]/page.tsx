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
import { TriangleAlert  as ExclamationTriangle, Eye, EyeOff } from 'lucide-react'
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
                router.push('/dashboard')
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
        <div className="min-h-screen flex items-center justify-center bg-black p-4">
            <div className="rounded-2xl w-2/5 h-auto bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px] shadow-lg">
                <div className="bg-black rounded-2xl flex justify-center items-center">

                    <Card className="w-full rounded-2xl text-gray-100">
                        <CardHeader>
                            <CardTitle className="text-5xl font-bold text-center py-4">Sign In</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={handleSubmit} className="space-y-4">
                                <div className="space-y-2">
                                    {/* <Label htmlFor="email" className="text-base pl-2 font-medium">
                                        Email address
                                    </Label> */}
                                    <Input
                                        onChange={(e) => setEmail(e.target.value)}
                                        onBlur={handleEmailBlur}
                                        id="email"
                                        name="email"
                                        type="email"
                                        required
                                        className="font-script text-md bg-gray-800 border-gray-700 text-white placeholder-gray-400 h-fit w-full py-4"
                                        placeholder="Enter your email"
                                        value={email}
                                    />
                                    {isEmailTouched && !isEmailValid && (
                                        <p className="pl-2 text-base text-red-500">Please enter a valid email address.</p>
                                    )}
                                </div>
                                <div className="space-y-2 pb-4">
                                    {/* <Label htmlFor="password" className="text-base pl-2 font-medium">
                                        Password
                                    </Label> */}
                                    <div className="relative">
                                        <Input
                                            onChange={(e) => setPassword(e.target.value)}
                                            id="password"
                                            name="password"
                                            type={showPassword ? "text" : "password"}
                                            required
                                            className="font-script text-md bg-gray-800 border-gray-700 text-white placeholder-gray-400 pr-10 h-fit w-full py-4"
                                            placeholder="Enter your password"
                                            value={password}
                                        />
                                        <Button
                                            type="button"
                                            variant="ghost"
                                            size="icon"
                                            className="absolute right-0 top-0 h-full text-gray-400 hover:text-white hover:bg-transparent mr-2"
                                            onClick={() => setShowPassword(!showPassword)}
                                        >
                                            {showPassword ? (
                                                <EyeOff size={25} />
                                            ) : (
                                                <Eye size={25} />
                                            )}
                                        </Button>
                                    </div>
                                </div>
                                <div className="h-fit relative group flex w-full justify-center mx-auto">
                                    <div className="absolute inset-0 blur-lg rounded-2xl w-auto h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradientbg ease-out p-[3px] opacity-0 group-hover:opacity-100 transition-opacity"></div>
                                    <div className="relative flex rounded-2xl w-full h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[3px]">
                                        {/* <Button
                                        type="submit"
                                        variant={"gradient"}
                                        className="h-full w-full rounded-full pb-[10px] text-3xl font-medium disabled: bg-black">
                                        Complete Onboarding
                                    </Button> */}
                                        <Button
                                            type="submit"
                                            disabled={!isEmailValid || !password}
                                            variant={"gradient"}
                                            className="font-script h-full w-full rounded-2xl pb-[10px] text-2xl font-medium disabled: bg-black ">
                                            Sign in
                                        </Button>
                                    </div>
                                </div>
                            </form>
                            {error && (
                                <Alert variant="destructive" className="bg-red-900/50 border border-red-600 text-red-100 h-full flex justify-center mt-4">
                                    <div className=' flex items-center h-full'>
                                        <ExclamationTriangle className="h-5 w-5 mr-2" />
                                        <AlertDescription className='h-full'>{error}</AlertDescription>
                                    </div>
                                </Alert>
                            )}
                        </CardContent>
                        <CardFooter className="flex justify-center">
                            <p className="text-sm font-script text-gray-300">
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
            </div>
        </div>
    )
}

