import Link from 'next/link'
import { Button } from "@/components/ui/button"

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen flex flex-col">
            <header className="p-4 border-b">
                <Link href="/dashboard" passHref>
                    <Button variant="outline" className="text-xl border-[1px] border-white">
                        Dashboard
                    </Button>
                </Link>
            </header>
            <main className="flex-grow">
                {children}
            </main>
        </div>
    )
}

