import type { Campus } from '@/types'

export interface AppFooterProps {
  campus: Campus
}

export default function AppFooter({ campus }: AppFooterProps) {
  return (
    <footer className="mt-16 border-t border-[var(--border)] py-6 text-center text-xs mono" style={{ color: 'var(--muted-foreground)' }}>
      Bandejão UnB · Sistema de avaliação estudantil · {campus.name}
    </footer>
  )
}