import { listarEstimativas } from './api'
import type { EstimativaApi } from './api'

export async function carregarEstimativas(
  filtros: { campus_id: string; data_inicio: string; data_fim: string },
  signal: AbortSignal,
  consultar = listarEstimativas,
): Promise<Map<number, EstimativaApi>> {
  const [reais, simuladas] = await Promise.all([
    consultar(filtros, { signal }),
    consultar({ ...filtros, dados_simulados: true }, { signal }),
  ])
  const demonstracao = new Map(simuladas.map(e => [e.cardapio_id, e]))
  return new Map(reais.map(real => {
    const simulada = demonstracao.get(real.cardapio_id)
    return [real.cardapio_id, real.status === 'disponivel' ? real
      : simulada?.status === 'disponivel' ? simulada : real]
  }))
}
