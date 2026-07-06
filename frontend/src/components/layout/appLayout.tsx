import { Outlet } from 'react-router'
import { PriceDisplay } from '@/features/price/display/priceDisplay'

export function AppLayout() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="border-b">
        <div className="mx-auto flex max-w-5xl items-center justify-between gap-4 px-4 py-4">
          <h1 className="text-lg font-semibold">Agent Trade</h1>
          <PriceDisplay />
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-4 py-6">
        <Outlet />
      </main>
    </div>
  )
}
