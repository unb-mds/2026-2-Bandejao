import type { Campus } from '@/types'
import { VERSAO_APP } from '@/versao'

export interface AppFooterProps {
  campus: Campus
  onAbrirPrivacidade: () => void
}

export default function AppFooter({ campus, onAbrirPrivacidade }: AppFooterProps) {
  return (
    <footer className="mt-16 border-t border-[var(--border)] py-6 text-center text-xs mono" style={{ color: 'var(--muted-foreground)' }}>
      <p>Bandejão UnB · Sistema de avaliação estudantil · {campus.name}</p>
      <p className="mt-1">Versão: {VERSAO_APP}</p>
      <div className="mt-3">
        <button type="button" className="underline underline-offset-4" onClick={onAbrirPrivacidade}>Privacidade</button>
      </div>

    </footer>
  )
}
