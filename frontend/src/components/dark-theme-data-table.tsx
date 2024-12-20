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
    id: string
    ideaTitle: string
    dateCreated: string
    ideaDescription: string
}

export default function DataTableDemo() {
    const [data, setData] = React.useState<Project[]>([])
    const [loading, setLoading] = React.useState(true)
    const [error, setError] = React.useState<string | null>(null)
    const [projectToDelete, setProjectToDelete] = React.useState<string | null>(null)

    const [sorting, setSorting] = React.useState<SortingState>([])
    const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([])
    const [columnVisibility, setColumnVisibility] =
        React.useState<VisibilityState>({})

    const router = useRouter()

    React.useEffect(() => {
        fetchProjects()
    }, [])

    const fetchProjects = async () => {
        try {
            setLoading(true)
            const response = await fetch('http://localhost:5000/getUserProjects', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            const result = await response.json()
            if (result.success) {
                setData(result.allUserProjects)
            } else {
                setError(result.error || 'Failed to fetch projects')
            }
        } catch (err) {
            setError('An error occurred while fetching projects')
        } finally {
            setLoading(false)
        }
    }

    const deleteProject = async (id: string) => {
        try {
            const response = await fetch('http://localhost:5000/deleteProject', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id }),
            })
            const result = await response.json()
            if (result.success) {
                setData(prevData => prevData.filter(project => project.id !== id))
            } else {
                setError(result.error || 'Failed to delete project')
            }
        } catch (err) {
            setError('An error occurred while deleting the project')
        } finally {
            setProjectToDelete(null)
        }
    }

    const handleRowClick = (projectId: string) => {
        router.push(`/project/script/${projectId}`)
    }

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
                                className="h-10 w-10 p-0"
                                onClick={(e) => e.stopPropagation()}
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
                                    project "{project.ideaTitle}" and remove the data from our servers.
                                </AlertDialogDescription>
                            </AlertDialogHeader>
                            <AlertDialogFooter>
                                <AlertDialogCancel className="bg-gray-700 text-gray-100">Cancel</AlertDialogCancel>
                                <AlertDialogAction onClick={() => deleteProject(project.id)} className="bg-red-600 text-white">Delete</AlertDialogAction>
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
        },
        state: {
            sorting,
            columnFilters,
            columnVisibility,
        },
    })

    const handleProjectCreated = (projectId: string) => {
        router.push(`/project/script/${projectId}`)
    }

    if (loading) {
        return <div className="min-h-screen w-full bg-gray-900 text-gray-100 p-8 flex justify-center items-center">Loading...</div>
    }

    if (error) {
        return <div className="min-h-screen w-full bg-gray-900 text-gray-100 p-8 flex justify-center items-center">Error: {error}</div>
    }

    return (
        <div className="min-h-screen w-full bg-gray-900 text-gray-100 p-8 flex justify-center items-start">
            <div className="w-full max-w-4xl">
                <div className="mb-4 flex justify-between items-center">
                    <Input
                        placeholder="Search ideas..."
                        value={(table.getColumn("ideaTitle")?.getFilterValue() as string) ?? ""}
                        onChange={(event) =>
                            table.getColumn("ideaTitle")?.setFilterValue(event.target.value)
                        }
                        className="max-w-sm text-lg bg-gray-800 text-gray-100 border-gray-700"
                    />
                    <CreateProjectDialog onProjectCreated={handleProjectCreated} />
                </div>
                <div className="rounded-md border border-gray-700 overflow-hidden">
                    <Table>
                        <TableHeader className="bg-gray-800">
                            {table.getHeaderGroups().map((headerGroup) => (
                                <TableRow key={headerGroup.id}>
                                    {headerGroup.headers.map((header) => {
                                        return (
                                            <TableHead key={header.id} className="text-left">
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
                                        onClick={() => handleRowClick(row.original.id)}
                                        className="cursor-pointer hover:bg-gray-800"
                                    >
                                        {row.getVisibleCells().map((cell) => (
                                            <TableCell key={cell.id} className="text-left">
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
                            className="text-lg"
                        >
                            Previous
                        </Button>
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={() => table.nextPage()}
                            disabled={!table.getCanNextPage()}
                            className="text-lg"
                        >
                            Next
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    )
}

