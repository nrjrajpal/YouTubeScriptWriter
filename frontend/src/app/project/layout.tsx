import Link from 'next/link'
import { Button } from "@/components/ui/button"

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen flex flex-col">
            <header className="p-4 border-b">
                <Link href="/dashboard" passHref>
                <Button className="font-script border border-gray-600 text-sm h-10 w-auto px-6 rounded-xl bg-gray-900 text-white hover:bg-gray-800 font-medium">Dashboard</Button>
                    {/* <Button variant="outline" className="text-md border-[1px] border-white">
                        Dashboard
                    </Button> */}
                </Link>
            </header>
            <main className="flex-grow">
                {children}
            </main>
        </div>
    )
}

