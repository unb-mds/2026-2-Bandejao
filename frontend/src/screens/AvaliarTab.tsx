import AvaliacaoForm from '@/screens/AvaliacaoForm'
import AvaliacaoHistorico from '@/screens/AvaliacaoHistorico'
import Reclamacoes from '@/screens/Reclamacoes'

import type { AvaliacaoFormProps } from '@/screens/AvaliacaoForm'
import type {
  AvaliacaoHistoricoProps
} from '@/screens/AvaliacaoHistorico'
import type { ReclamacoesProps } from '@/screens/Reclamacoes'

import type { TabAvaliar } from '@/types'

export interface AvaliarTabProps {
  tabAvaliar: TabAvaliar
  setTabAvaliar: (t: TabAvaliar) => void
  formProps: AvaliacaoFormProps
  historicoProps: AvaliacaoHistoricoProps
  reclamacoesProps: ReclamacoesProps
}

export default function AvaliarTab({ tabAvaliar, setTabAvaliar, formProps, historicoProps, reclamacoesProps }: AvaliarTabProps) {
  return (
          <div id="panel-avaliar" role="tabpanel" aria-labelledby="tab-avaliar" className="max-w-2xl mx-auto px-4 pt-5 pb-8">
            {/* Sub-nav */}
            <div className="flex rounded-xl overflow-hidden mb-5" style={{ background: '#F5F2ED', padding: '4px' }}>
              {([
                { id: 'form' as const, label: 'Avaliar' },
                { id: 'historico' as const, label: 'Histórico' },
                { id: 'reclamacao' as const, label: 'Reclamações' },
              ]).map(({ id, label }) => (
                <button key={id} onClick={() => setTabAvaliar(id)}
                  className="flex-1 py-2 rounded-lg text-sm font-semibold transition-all"
                  style={{
                    background: tabAvaliar === id ? '#fff' : 'transparent',
                    color: tabAvaliar === id ? '#1E5631' : 'var(--muted-foreground)',
                    boxShadow: tabAvaliar === id ? '0 1px 4px rgba(0,0,0,0.08)' : 'none',
                  }}>
                  {label}
                </button>
              ))}
            </div>
      {tabAvaliar === 'form' && (<AvaliacaoForm {...formProps} />)}
      {tabAvaliar === 'historico' && (<AvaliacaoHistorico {...historicoProps} />)}
      {tabAvaliar === 'reclamacao' && (<Reclamacoes {...reclamacoesProps} />)}
    </div>
  )
}
