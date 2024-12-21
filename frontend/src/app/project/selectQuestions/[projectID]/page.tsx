"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useToast } from "@/hooks/use-toast"

export default function QuestionSelector() {
  const [selectedItems, setSelectedItems] = useState<string[]>([])
  const [customQuestions, setCustomQuestions] = useState<string[]>(["", "", ""])
  const { toast } = useToast()

  const placeholderQuestions = [
    "What is your favorite color and why?",
    "Describe your ideal vacation destination.",
    "If you could have dinner with any historical figure, who would it be?",
    "What's the most interesting book you've read recently?",
    "What's a skill you'd like to learn in the next year?",
  ]

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

  const handleSubmit = () => {
    if (selectedItems.length === 0) {
      toast({
        title: "Error",
        description: "Please select at least one question before submitting.",
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
    console.log("Selected questions:", selectedQuestions)
    toast({
      title: "Success",
      description: "Your questions have been submitted successfully!",
    })
  }

  return (
    <div className="min-h-screen bg-black text-white p-8 flex flex-col justify-center items-center">
      <div className="rounded-2xl w-3/5 h-auto bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px] shadow-lg">
        <div className="bg-black rounded-2xl flex justify-center items-center py-4 px-4">
          <div className="w-full max-w-3xl py-4">
            <h1 className="text-6xl mb-5 text-center">
              Select Questions
            </h1>
            <p className="text-2xl mb-8 text-center">
              Choose 1-3 questions from the options below or create your own.
              The order of selection matters. Once 3 are selected, the rest will
              be disabled.
            </p>
            <div className="flex flex-col space-y-4">
              {placeholderQuestions.map((question, index) => (
                <button
                  key={`preset-${index}`}
                  onClick={() => handleToggle(`preset-${index}`)}
                  disabled={isDisabled(`preset-${index}`)}
                  className={`w-full p-6 pr-12 text-left border border-gray-700 rounded-md text-2xl relative ${selectedItems.includes(`preset-${index}`)
                    ? "bg-gray-800"
                    : "bg-black hover:bg-gray-900"
                    } ${isDisabled(`preset-${index}`) ? "opacity-50 cursor-not-allowed" : ""}`}
                >
                  {question}
                  {selectedItems.includes(`preset-${index}`) && (
                    <span className="absolute top-2 right-2 w-8 h-8 bg-white text-black rounded-full flex items-center justify-center text-lg font-bold">
                      {getSelectionOrder(`preset-${index}`)}
                    </span>
                  )}
                </button>
              ))}
              {customQuestions.map((question, index) => (
                <div
                  key={`custom-${index}`}
                  className={`w-full px-6 pr-12 text-left border border-gray-700 rounded-md text-2xl relative ${selectedItems.includes(`custom-${index}`)
                    ? "bg-gray-800"
                    : "bg-black hover:bg-gray-900"
                    } ${isDisabled(`custom-${index}`) ? "opacity-50 cursor-not-allowed" : ""}`}
                >
                  <Input
                    type="text"
                    placeholder="Enter your custom question"
                    value={question}
                    onChange={(e) => handleCustomQuestionChange(index, e.target.value)}
                    disabled={isDisabled(`custom-${index}`)}
                    className="w-full bg-transparent border-r-2 border-none focus:ring-0 p-0 text-2xl"
                    maxLength={400}
                  />
                  {selectedItems.includes(`custom-${index}`) && (
                    <span className="absolute top-2 right-2 w-8 h-8 bg-white text-black rounded-full flex items-center justify-center text-lg font-bold">
                      {getSelectionOrder(`custom-${index}`)}
                    </span>
                  )}
                </div>
              ))}
            </div>
            <p className="text-xl mt-4 text-gray-400 text-center">
              Custom questions are automatically selected when you start typing.
            </p>
            <div className="my-8 relative group flex w-[600px] justify-center mx-auto">
              <div className="absolute inset-0 blur-xl rounded-full w-auto h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradientbg ease-out p-[3px] opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative flex rounded-full w-full h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[3px]">
                <Button
                  onClick={handleSubmit}
                  variant="gradient"
                  className="h-auto pb-[10px] text-3xl font-medium"
                >
                  Submit
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}