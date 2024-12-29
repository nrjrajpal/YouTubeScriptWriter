import * as React from "react"
import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogFooter,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { useParams, useRouter } from "next/navigation"

interface CreateProjectDialogProps {
    onProjectCreated: (projectID: string) => void
    userEmail: string
}

export function CreateProjectDialog({ onProjectCreated, userEmail }: CreateProjectDialogProps) {
    const [open, setOpen] = React.useState(false)
    const [ideaTitle, setIdeaTitle] = React.useState("")
    const [ideaDescription, setIdeaDescription] = React.useState("")
    const [isCreating, setIsCreating] = React.useState(false)
    const [message, setMessage] = React.useState<string | null>(null)
    const router = useRouter()

    const handleCreate = async () => {
        setIsCreating(true)
        setMessage(null)

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/createProject`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ ideaTitle, ideaDescription, userEmail }),
            })
            const result = await response.json()
            if (result.success) {
                setMessage("Project created successfully!")
                onProjectCreated(result.project.projectID)
                setTimeout(() => {
                    setOpen(false)
                    setIdeaTitle("")
                    setIdeaDescription("")
                    setMessage(null)
                }, 2000)

                router.push(`/project/selectSources/${result.project.projectID}`)

            } else {
                setMessage(result.error || "Failed to create project")
            }
        } catch (err) {
            setMessage("An error occurred while creating the project")
        } finally {
            setIsCreating(false)
        }
    }

    return (

        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
                <Button className="font-script border border-gray-600 text-sm h-10 w-auto px-6 rounded-xl bg-gray-900 text-white hover:bg-gray-800 font-medium">Create Project</Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px] bg-black text-gray-100">

                <DialogHeader>
                    <DialogTitle className="text-xl font-script">Create Project</DialogTitle>
                    <DialogDescription className="font-script text-gray-400">
                        Enter the details for your new project idea.
                    </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                    <Input
                        id="ideaTitle"
                        value={ideaTitle}
                        onChange={(e) => setIdeaTitle(e.target.value.slice(0, 200))}
                        className="font-script text-sm col-span-3 bg-gray-700 text-gray-100 border-gray-600 w-full h-fit rounded-lg"
                        maxLength={200}
                        required
                        placeholder="Enter idea title (max 200 characters)"
                    />
                    <Textarea
                        id="ideaDescription"
                        value={ideaDescription}
                        onChange={(e) => setIdeaDescription(e.target.value.slice(0, 2000))}
                        className="font-script text-sm col-span-3 bg-gray-700 text-gray-100 border-gray-600 w-full h-[40vh] rounded-lg"
                        maxLength={2000}
                        required
                        placeholder="Enter idea description (max 2000 characters)"
                    />
                </div>
                <DialogFooter>
                <div className="my-8 relative group flex w-full justify-center mx-auto">
                    <div className="absolute inset-0 blur-xl rounded-2xl w-auto h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradientbg ease-out p-[2px] opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    <div className="relative flex rounded-2xl w-full h-full bg-[linear-gradient(45deg,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF,#2998ff,#FB923C,#8F00FF)] bg-[length:800%_auto] animate-gradient p-[2px] hover:bg-transparent">
                        <Button
                            type="submit"
                            onClick={handleCreate}
                            variant={"gradient"}
                            disabled={!ideaTitle || !ideaDescription || isCreating}
                            className="font-script w-full rounded-2xl bg-black h-full text-lg font-bold text-white"
                            >
                            {isCreating ? "Creating..." : "Create"}
                        </Button>
                    </div>
                            </div>
                </DialogFooter>
                {message && (
                    <div className={`mt-2 text-center ${message.includes("success") ? "text-green-500" : "text-red-500"}`}>
                        {message}
                    </div>
                )}
            </DialogContent>
        </Dialog>
    )
}

