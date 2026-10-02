import { AlergDots, SectionLabel } from '@/components/ui'
import { alergenosDoItem, CATEGORIAS, DIETAS } from '@/cardapios'
import type { FiltrosAlimentares, Refeicao, RefeicaoData } from '@/types'

export interface MealContentProps {
  data: RefeicaoData
  dia?: number
  refeicao: Refeicao
  filtros?: FiltrosAlimentares
}

export default function MealContent({ data, filtros }: MealContentProps) {
  const itens = data.itensApi ?? []
  const visiveis = itens.filter(item => {
    if (filtros?.alergenos.some(alergeno => alergenosDoItem(item).includes(alergeno))) return false
    if (filtros?.vegetariano || filtros?.vegetarianoEstrito) {
      return (filtros.vegetariano && item.tipo_dieta === 'ovolactovegetariano')
        || (filtros.vegetarianoEstrito && item.tipo_dieta === 'vegetariano_estrito')
    }
    return true
  })
  const categorias = [...new Set(visiveis.map(item => item.categoria))]

  return (
    <div className="space-y-3">
      <p className="text-sm text-muted-foreground">{data.label} · {data.data && new Date(`${data.data}T12:00:00`).toLocaleDateString('pt-BR')}</p>
      {itens.length === 0 ? (
        <p role="status" className="rounded-2xl border border-border bg-card p-5 text-sm">
          {data.id ? 'Esta refeição foi publicada sem itens.' : 'Nenhum cardápio publicado para esta refeição.'} Consulte a fonte oficial para confirmar o funcionamento do RU.
        </p>
      ) : (
        <>
          {visiveis.length === 0 && <p role="status" className="rounded-2xl border border-border bg-card p-5 text-sm">Nenhum item corresponde aos filtros selecionados.</p>}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {categorias.map(categoria => (
              <section key={categoria} className={`rounded-2xl border border-border bg-card p-5 ${categoria === 'prato_principal' ? 'sm:col-span-2' : ''}`}>
                <SectionLabel>{CATEGORIAS[categoria] ?? categoria.replaceAll('_', ' ')}</SectionLabel>
                <ul className="mt-3 space-y-3">
                  {visiveis.filter(item => item.categoria === categoria).map(item => (
                    <li key={item.id}>
                      <p className="text-sm font-semibold text-foreground">
                        {item.nome}<AlergDots item={{ nome: item.nome, alergenos: alergenosDoItem(item) }} />
                      </p>
                      <span className="inline-block mt-1 rounded-full bg-secondary px-2 py-0.5 text-xs text-secondary-foreground">{DIETAS[item.tipo_dieta] ?? item.tipo_dieta}</span>
                    </li>
                  ))}
                </ul>
              </section>
            ))}
          </div>
          <p className="text-xs text-muted-foreground">Os filtros usam as marcações publicadas. A ausência de uma marcação não garante ausência do ingrediente. A legenda validada não informa frutos do mar; confira a fonte oficial.</p>
        </>
      )}
      {data.fontePdfUrl && <a className="inline-block text-sm font-semibold text-primary underline" href={data.fontePdfUrl} target="_blank" rel="noreferrer">Ver PDF da fonte ↗</a>}
    </div>
  )
}
