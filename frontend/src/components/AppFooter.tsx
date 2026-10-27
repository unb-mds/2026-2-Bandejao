import type { Campus } from '@/types'

export interface AppFooterProps {
  campus: Campus
  onAbrirPrivacidade: () => void
}

export default function AppFooter({ campus, onAbrirPrivacidade }: AppFooterProps) {
  return (
    <footer className="mt-16 border-t border-[var(--border)] py-6 text-center text-xs mono" style={{ color: 'var(--muted-foreground)' }}>
      Bandejão UnB · Sistema de avaliação estudantil · {campus.name}
      <div className="mt-3">
        <button type="button" className="underline underline-offset-4" onClick={onAbrirPrivacidade}>Privacidade</button>
      </div>
    </footer>
  )
}
