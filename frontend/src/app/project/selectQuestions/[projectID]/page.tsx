"use client"

import { useState, useEffect } from "react"
import { useParams, useRouter } from "next/navigation"
import { useUser } from '@clerk/nextjs'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useToast } from "@/hooks/use-toast"
import { Skeleton } from "@/components/ui/skeleton"

export default function QuestionSelector() {
  const [selectedItems, setSelectedItems] = useState<string[]>([])
  const [customQuestions, setCustomQuestions] = useState<string[]>(["", "", ""])
  const [placeholderQuestions, setPlaceholderQuestions] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isRegenerating, setIsRegenerating] = useState(false)
  const { toast } = useToast()
  const params = useParams()
  const router = useRouter()
  const { isLoaded, isSignedIn, user } = useUser()

  useEffect(() => {
    if (isLoaded && isSignedIn) {
      fetchQuestions()
    }
  }, [isLoaded, isSignedIn])

  const fetchQuestions = async () => {
    if (!user?.primaryEmailAddress?.emailAddress || !params.projectID) return

    try {
      setIsRegenerating(true)
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/generateQuestionsBasedOnTitle`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userEmail: user.primaryEmailAddress.emailAddress,
          projectID: params.projectID,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to fetch questions')
      }

      const data = await response.json()
      setPlaceholderQuestions(data.generated_questions)

      // Clear selections and custom questions
      setSelectedItems([])
      setCustomQuestions(["", "", ""])
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "An error occurred while fetching questions.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
      setIsRegenerating(false)
    }
  }

  const handleToggle = (id: string) => {
    setSelectedItems((prev) => {
      if (prev.includes(id)) {
        return prev.filter((item) => item !== id)
      } else if (prev.length < 3) {
        return [...prev, id]
      }
      return prev
    })
  }

  const handleCustomQuestionChange = (index: number, value: string) => {
    const newCustomQuestions = [...customQuestions]
    newCustomQuestions[index] = value
    setCustomQuestions(newCustomQuestions)

    if (value && !selectedItems.includes(`custom-${index}`)) {
      handleToggle(`custom-${index}`)
    } else if (!value && selectedItems.includes(`custom-${index}`)) {
      handleToggle(`custom-${index}`)
    }
  }

  const isDisabled = (id: string) => {
    return selectedItems.length >= 3 && !selectedItems.includes(id)
  }

  const getSelectionOrder = (id: string) => {
    const index = selectedItems.indexOf(id)
    return index !== -1 ? index + 1 : null
  }

  const handleSubmit = async () => {
    if (selectedItems.length !== 3) {
      toast({
        title: "Error",
        description: "Please select exactly 3 questions before submitting.",
        variant: "destructive",
      })
      return
    }

    if (!user?.primaryEmailAddress?.emailAddress || !params.projectID) {
      toast({
        title: "Error",
        description: "User email or project ID is missing.",
        variant: "destructive",
      })
      return
    }

    const selectedQuestions = selectedItems.map(id => {
      if (id.startsWith('preset-')) {
        const index = parseInt(id.split('-')[1])
        return placeholderQuestions[index]
      } else {
        const index = parseInt(id.split('-')[1])
        return customQuestions[index]
      }
    })

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/setSelectedQuestions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userEmail: user.primaryEmailAddress.emailAddress,
          projectID: params.projectID,
          selectedQuestions: selectedQuestions,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to set selected questions')
      }

      const data = await response.json()
      toast({
        title: "Success",
        description: data.Message || "Your questions have been submitted successfully!",
      })

      // Redirect to the next page
      router.push(`/project/selectSources/${params.projectID}`)
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "An error occurred while submitting questions.",
        variant: "destructive",
      })
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <p className="text-2xl">Loading questions...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black text-white p-8 flex flex-col justify-center items-center">
      <div className="rounded-2xl w-3/5 h-auto bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px] shadow-lg">
        <div className="bg-black rounded-2xl flex justify-center items-center py-4 px-4">
          <div className="w-full max-w-3xl py-4 px-8">
            <h1 className="text-4xl mb-5 font-semibold text-center font-script">
              Select Questions
            </h1>
            <p className="text-md mb-8 text-center font-script">
              Choose exactly 3 questions from the options below or create your own.
              The order of selection matters.
            </p>
            <div className="flex flex-col space-y-4">
              {isRegenerating
                ? Array(5).fill(0).map((_, index) => (
                  <Skeleton key={index} className="w-full h-24 bg-gray-800" />
                ))
                : placeholderQuestions.map((question, index) => (
                  <button
                    key={`preset-${index}`}
                    onClick={() => handleToggle(`preset-${index}`)}
                    disabled={isDisabled(`preset-${index}`) || isRegenerating}
                    className={`w-full p-6 pr-12 text-left border border-gray-700 rounded-2xl text-md relative font-script ${selectedItems.includes(`preset-${index}`)
                      ? "bg-gray-800"
                      : "bg-black hover:bg-gray-900"
                      } ${isDisabled(`preset-${index}`) || isRegenerating ? "opacity-50 cursor-not-allowed" : ""}`}
                  >
                    {question}
                    {selectedItems.includes(`preset-${index}`) && (
                      <span className="absolute top-2 right-2 w-8 h-8 bg-white text-black rounded-2xl flex items-center justify-center text-lg font-bold">
                        {getSelectionOrder(`preset-${index}`)}
                      </span>
                    )}
                  </button>
                ))}
              {customQuestions.map((question, index) => (
                <div
                  key={`custom-${index}`}
                  className={`w-full px-6 pr-12 text-left border border-gray-700 rounded-2xl text-md relative ${selectedItems.includes(`custom-${index}`)
                    ? "bg-gray-800"
                    : "bg-black hover:bg-gray-900"
                    } ${isDisabled(`custom-${index}`) || isRegenerating ? "opacity-50 cursor-not-allowed" : ""}`}
                >
                  <Input
                    type="text"
                    placeholder="Enter your custom question"
                    value={question}
                    onChange={(e) => handleCustomQuestionChange(index, e.target.value)}
                    disabled={isDisabled(`custom-${index}`) || isRegenerating}
                    className="text-md w-full bg-transparent border-r-2 border-none focus:ring-0 p-0"
                    maxLength={400}
                  />
                  {selectedItems.includes(`custom-${index}`) && (
                    <span className="text-md absolute top-2 right-2 w-8 h-8 bg-white text-black rounded-2xl flex items-center justify-center text-lg font-bold">
                      {getSelectionOrder(`custom-${index}`)}
                    </span>
                  )}
                </div>
              ))}
            </div>
            <p className="text-sm mt-4 text-gray-400 text-center">
              Custom questions are automatically selected when you start typing.
            </p>
            <div className="my-8 flex flex-rows justify-center space-x-4">
              <div className="h-fit relative group flex w-full justify-center mx-auto">
                {(selectedItems.length == 3 && !isRegenerating) && (
                  <div className="h-fit relative group flex w-full justify-center mx-auto">
                    <div className="absolute inset-0 blur-lg rounded-2xl w-auto h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradientbg ease-out p-[2px] opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    <div className="relative flex rounded-2xl w-full h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px]">
                        <Button onClick={handleSubmit} disabled={selectedItems.length !== 3 || isRegenerating} type="submit" variant={"gradient"} className="font-script flex-1 h-full w-full rounded-2xl pb-[10px] text-xl font-medium">
                            Submit
                        </Button>
                    </div>
                  </div>
                )}
                {(selectedItems.length !== 3 || isRegenerating) && (
                  <>
                    <div className="relative flex rounded-2xl w-full h-full bg-gray-600 animate-gradient p-[2px]">
                      <div className="h-fit relative group flex w-full justify-center mx-auto">
                            <Button disabled={selectedItems.length !== 3 || isRegenerating} type="submit" variant={"gradient"} className="text-gray-500 font-script flex-1 h-full w-full rounded-2xl pb-[10px] text-xl font-medium">
                                Submit
                            </Button>
                      </div>
                    </div>
                  </>
                )}
              </div>
              <div className="h-fit relative group flex w-full justify-center mx-auto">
                {(!isRegenerating) && (
                  <>
                    <div className="h-fit relative group flex w-full justify-center mx-auto">
                      <div className="absolute inset-0 blur-lg rounded-2xl w-auto h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradientbg ease-out p-[2px] opacity-0 group-hover:opacity-100 transition-opacity"></div>
                      <div className="relative flex rounded-2xl w-full h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px]">
                          <Button onClick={fetchQuestions} disabled={isRegenerating} type="submit" variant={"gradient"} className={`font-script flex-1 h-full w-full rounded-2xl pb-[10px] text-xl font-medium ${isRegenerating ? "cursor-not-allowed bg-gray-800 text-gray-400" : ""}`}>
                            Regenerate
                          </Button>
                      </div>
                    </div>
                  </>
                )}
                {(isRegenerating) && (
                  <>
                    <div className="relative flex rounded-2xl w-full h-full bg-gray-600 animate-gradient p-[2px]">
                      <div className="h-fit relative group flex w-full justify-center mx-auto">
                            <Button disabled={isRegenerating} type="submit" variant={"gradient"} className="text-gray-500 font-script flex-1 h-full w-full rounded-2xl pb-[10px] text-xl font-medium">
                                Regenerate
                            </Button>
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}