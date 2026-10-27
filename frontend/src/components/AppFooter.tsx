import type { Campus } from '@/types'
import { VERSAO_APP } from '@/versao'

export interface AppFooterProps {
  campus: Campus
}

export default function AppFooter({ campus }: AppFooterProps) {
  return (
    <footer className="mt-16 border-t border-[var(--border)] py-6 text-center text-xs mono" style={{ color: 'var(--muted-foreground)' }}>
      <p>Bandejão UnB · Sistema de avaliação estudantil · {campus.name}</p>
      <p className="mt-1">Versão: {VERSAO_APP}</p>
    </footer>
  )
}
