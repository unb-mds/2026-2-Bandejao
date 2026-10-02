import type { DiaPlanejado } from '@/types'

export interface PlanejamentoSemanaProps {
  diasPlanejados: DiaPlanejado[]
  planejadosCount: number
  onPlanejar: () => void
}

// NOTA: no HomeScreen original estas props eram recebidas mas nunca renderizadas
// (planejadosCount/onPlanejar/diasPlanejados não apareciam em nenhum JSX e o cálculo
// planejadosNaSemana era descartado). Para preservar comportamento e visual
// exatamente iguais, este componente recebe as props e intencionalmente não
// renderiza nada. Verificável em HomeScreen.orig: apenas declaração, sem uso.
export default function PlanejamentoSemana(_props: PlanejamentoSemanaProps) {
  return null
}
