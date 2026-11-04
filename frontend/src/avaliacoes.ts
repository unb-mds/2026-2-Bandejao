import type { AvaliacaoApi } from './api'
import type { Avaliacao } from './types'

const FORMATADOR_DATA = new Intl.DateTimeFormat('pt-BR', {
  timeZone: 'America/Sao_Paulo',
  day: '2-digit',
  month: '2-digit',
  year: 'numeric',
})

const FORMATADOR_HORA = new Intl.DateTimeFormat('pt-BR', {
  timeZone: 'America/Sao_Paulo',
  hour: '2-digit',
  minute: '2-digit',
  hour12: false,
})

export interface ContextoAvaliacao {
  refeicao: string
  campus: string
}

export function adaptarHistoricoAvaliacoes(
  avaliacoes: AvaliacaoApi[],
  contexto: ContextoAvaliacao,
): Avaliacao[] {
  return [...avaliacoes]
    .sort((a, b) => Date.parse(b.criado_em) - Date.parse(a.criado_em))
    .map(avaliacao => {
      const instante = new Date(avaliacao.criado_em)
      return {
        id: avaliacao.id,
        autor: 'Anônimo',
        refeicao: contexto.refeicao,
        campus: contexto.campus,
        geral: avaliacao.nota,
        comentario: avaliacao.comentario ?? '',
        data: FORMATADOR_DATA.format(instante),
        horario: FORMATADOR_HORA.format(instante),
      }
    })
}
