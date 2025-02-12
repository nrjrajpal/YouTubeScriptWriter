"use client"

import * as React from "react"
import {
    ColumnDef,
    ColumnFiltersState,
    SortingState,
    VisibilityState,
    flexRender,
    getCoreRowModel,
    getFilteredRowModel,
    getPaginationRowModel,
    getSortedRowModel,
    useReactTable,
} from "@tanstack/react-table"
import { ArrowUpDown, Trash2 } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { useUser } from '@clerk/nextjs'

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from "@/components/ui/tooltip"
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { CreateProjectDialog } from "./create-project-dialog"

// Define the data structure
type Project = {
    projectID: string
    ideaTitle: string
    dateCreated: string
    ideaDescription: string
}

export default function DataTableDemo() {
    const [data, setData] = React.useState<Project[]>([])
    const [loading, setLoading] = React.useState(true)
    const [error, setError] = React.useState<string | null>(null)
    //const [projectToDelete, setProjectToDelete] = React.useState<string | null>(null) //Removed

    const [sorting, setSorting] = React.useState<SortingState>([])
    const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([])
    const [columnVisibility, setColumnVisibility] =
        React.useState<VisibilityState>({})

    const router = useRouter()
    const { isLoaded, isSignedIn, user } = useUser()

    React.useEffect(() => {
        if (isLoaded && isSignedIn) {
            fetchProjects()
        }
    }, [isLoaded, isSignedIn])

    const fetchProjects = async () => {
        if (!user?.primaryEmailAddress?.emailAddress) return

        try {
            setLoading(true)
            const response = await fetch('http://localhost:5000/getUserProjects', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ userEmail: user.primaryEmailAddress.emailAddress }),
            })
            const result = await response.json()
            if (response.status === 404) {
                // No projects found, but this is not an error state
                setData([])
                setError(null)
            } else if (result.success) {
                const sortedProjects = result.allUserProjects.sort((a: { dateCreated: string | number | Date }, b: { dateCreated: string | number | Date }) => 
                    new Date(b.dateCreated).getTime() - new Date(a.dateCreated).getTime()
                )
                setData(sortedProjects)
                setError(null)
            } else {
                setError(result.error || 'Failed to fetch projects')
            }
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
        } catch (err) {
            setError('An error occurred while fetching projects')
        } finally {
            setLoading(false)
        }
    }

    const deleteProject = async (projectID: string) => {
        if (!user?.primaryEmailAddress?.emailAddress) return

        try {
            const response = await fetch('http://localhost:5000/deleteProject', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ projectID, userEmail: user.primaryEmailAddress.emailAddress }),
            })
            const result = await response.json()
            if (result.success) {
                setData(prevData => prevData.filter(project => project.projectID !== projectID))
                setError(null) // Clear any previous errors
            } else {
                setError(result.error || 'Failed to delete project')
            }
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
        } catch (err) {
            setError('An error occurred while deleting the project')
        } finally {
            //setProjectToDelete(null) //Removed
        }
    }

    const handleRowClick = (event: React.MouseEvent, projectID: string) => {
        // Check if the click target is the delete button or its parent
        if (
            (event.target as HTMLElement).closest('[data-delete-button]') ||
            (event.target as HTMLElement).closest('[role="dialog"]')
        ) {
            return; // Do nothing if the delete button or dialog was clicked
        }
        router.push(`/project/script/${projectID}`)
    };

    const columns: ColumnDef<Project>[] = [
        {
            accessorKey: "ideaTitle",
            header: ({ column }) => {
                return (
                    <Button
                        variant="ghost"
                        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        className="text-lg font-bold"
                    >
                        Idea Title
                        <ArrowUpDown className="ml-2 h-5 w-5" />
                    </Button>
                )
            },
            cell: ({ row }) => <div className="text-lg">{row.getValue("ideaTitle")}</div>,
        },
        {
            accessorKey: "dateCreated",
            header: ({ column }) => {
                return (
                    <Button
                        variant="ghost"
                        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                        className="text-lg font-bold"
                    >
                        Date Created
                        <ArrowUpDown className="ml-2 h-5 w-5" />
                    </Button>
                )
            },
            cell: ({ row }) => <div className="text-lg">{row.getValue("dateCreated")}</div>,
        },
        {
            id: "actions",
            cell: ({ row }) => {
                const project = row.original

                return (
                    <AlertDialog>
                        <AlertDialogTrigger asChild>
                            <Button
                                variant="ghost"
                                className="h-10 w-10 p-0 float-right"
                                onClick={(e) => e.stopPropagation()}
                                data-delete-button
                            >
                                <span className="sr-only">Delete project</span>
                                <Trash2 className="h-5 w-5 text-red-500" />
                            </Button>
                        </AlertDialogTrigger>
                        <AlertDialogContent className="bg-gray-800 text-gray-100">
                            <AlertDialogHeader>
                                <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                                <AlertDialogDescription className="text-gray-400">
                                    This action cannot be undone. This will permanently delete the
                                    project &quot;{project.ideaTitle}&quot; and remove the data from our servers.
                                </AlertDialogDescription>
                            </AlertDialogHeader>
                            <AlertDialogFooter>
                                <AlertDialogCancel className="bg-gray-700 text-gray-100">Cancel</AlertDialogCancel>
                                <AlertDialogAction 
                                    onClick={() => deleteProject(project.projectID)} 
                                    className="bg-red-600 text-white"
                                >
                                    Delete
                                </AlertDialogAction>
                            </AlertDialogFooter>
                        </AlertDialogContent>
                    </AlertDialog>
                )
            },
        },
    ]

    const table = useReactTable({
        data,
        columns,
        onSortingChange: setSorting,
        onColumnFiltersChange: setColumnFilters,
        getCoreRowModel: getCoreRowModel(),
        getPaginationRowModel: getPaginationRowModel(),
        getSortedRowModel: getSortedRowModel(),
        getFilteredRowModel: getFilteredRowModel(),
        onColumnVisibilityChange: setColumnVisibility,
        initialState: {
            pagination: {
                pageSize: 5,
            },
            sorting: [
                { id: 'dateCreated', desc: true }
            ],
        },
        state: {
            sorting,
            columnFilters,
            columnVisibility,
        },
    })
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const handleProjectCreated = (projectId: string) => {
        fetchProjects()
    }

    if (!isLoaded || !isSignedIn) {
        return <div className="min-h-fit w-full bg-black text-gray-100 p-8 flex justify-center items-center">Loading...</div>
    }

    if (loading) {
        return <div className="min-h-fit w-full bg-black text-gray-100 p-8 flex justify-center items-center">Loading projects...</div>
    }

    return (
        <div className="max-h-fit w-full bg-black text-gray-100 p-8 flex justify-center items-start">
            <div className="w-full max-w-4xl max-h-fit">
                {data.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-fit">
                        <div className="text-center text-gray-400 mb-4">You don&apos;t have any projects yet. Create your first project to get started!</div>
                        <CreateProjectDialog onProjectCreated={handleProjectCreated} userEmail={user.primaryEmailAddress?.emailAddress || ''} />
                    </div>
                ) : (
                    <>
                        <div className="mb-4 flex justify-between items-center">
                            <Input
                                placeholder="Search ideas..."
                                value={(table.getColumn("ideaTitle")?.getFilterValue() as string) ?? ""}
                                onChange={(event) =>
                                    table.getColumn("ideaTitle")?.setFilterValue(event.target.value)
                                }
                                className="max-w-sm text-lg bg-gray-800 text-gray-100 border-gray-700"
                            />
                            <CreateProjectDialog onProjectCreated={handleProjectCreated} userEmail={user.primaryEmailAddress?.emailAddress || ''} />
                        </div>
                        {error ? (
                            <div className="text-center text-red-500 mb-4">{error}</div>
                        ) : (
                            <div className="rounded-md border border-gray-700 overflow-hidden">
                                <Table className="gap-96">
                                    <TableHeader className="bg-gray-800">
                                        {table.getHeaderGroups().map((headerGroup) => (
                                            <TableRow key={headerGroup.id}>
                                                {headerGroup.headers.map((header) => {
                                                    return (
                                                        <TableHead key={header.id} className="py-2 text-white text-left">
                                                            {header.isPlaceholder
                                                                ? null
                                                                : flexRender(
                                                                    header.column.columnDef.header,
                                                                    header.getContext()
                                                                )}
                                                        </TableHead>
                                                    )
                                                })}
                                            </TableRow>
                                        ))}
                                    </TableHeader>
                                    <TableBody>
                                        {table.getRowModel().rows?.length ? (
                                            table.getRowModel().rows.map((row) => (
                                                <TableRow
                                                    key={row.id}
                                                    data-state={row.getIsSelected() && "selected"}
                                                    onClick={(event) => handleRowClick(event, row.original.projectID)}
                                                    className="cursor-pointer hover:bg-gray-800"
                                                >
                                                    {row.getVisibleCells().map((cell) => (
                                                        <TableCell key={cell.id} className="pl-6 text-left">
                                                            {cell.column.id !== "actions" ? (
                                                                <TooltipProvider>
                                                                    <Tooltip>
                                                                        <TooltipTrigger asChild>
                                                                            <div>
                                                                                {flexRender(
                                                                                    cell.column.columnDef.cell,
                                                                                    cell.getContext()
                                                                                )}
                                                                            </div>
                                                                        </TooltipTrigger>
                                                                        <TooltipContent>
                                                                            <p className="text-lg">{row.original.ideaDescription}</p>
                                                                        </TooltipContent>
                                                                    </Tooltip>
                                                                </TooltipProvider>
                                                            ) : (
                                                                flexRender(
                                                                    cell.column.columnDef.cell,
                                                                    cell.getContext()
                                                                )
                                                            )}
                                                        </TableCell>
                                                    ))}
                                                </TableRow>
                                            ))
                                        ) : (
                                            <TableRow>
                                                <TableCell
                                                    colSpan={columns.length}
                                                    className="h-24 text-center"
                                                >
                                                    No results.
                                                </TableCell>
                                            </TableRow>
                                        )}
                                    </TableBody>
                                </Table>
                            </div>
                        )}
                        <div className="flex items-center justify-end space-x-2 py-4">
                            <div className="flex items-center space-x-2">
                                <p className="text-lg font-medium">Rows per page</p>
                                <select
                                    className="bg-gray-800 text-gray-100 border border-gray-700 rounded-md text-lg"
                                    value={table.getState().pagination.pageSize}
                                    onChange={(e) => {
                                        table.setPageSize(Number(e.target.value))
                                    }}
                                >
                                    {[5, 10, 20, 30, 40, 50].map((pageSize) => (
                                        <option key={pageSize} value={pageSize}>
                                            {pageSize}
                                        </option>
                                    ))}
                                </select>
                                <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={() => table.previousPage()}
                                    disabled={!table.getCanPreviousPage()}
                                    className="text-lg bg-gray-800"
                                >
                                    Previous
                                </Button>
                                <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={() => table.nextPage()}
                                    disabled={!table.getCanNextPage()}
                                    className="text-lg bg-gray-800"
                                >
                                    Next
                                </Button>
                            </div>
                        </div>
                    </>
                )}
            </div>
        </div>
    )
}

