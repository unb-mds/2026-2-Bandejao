import assert from 'node:assert/strict'
import { test } from 'node:test'

import { adaptarHistoricoAvaliacoes } from '../src/avaliacoes.ts'

test('adapta e ordena o histórico persistido do mais recente ao mais antigo', () => {
  const resultado = adaptarHistoricoAvaliacoes(
    [
      {
        id: 1,
        cardapio_id: 42,
        nota: 3,
        comentario: null,
        criado_em: '2026-10-24T12:00:00-03:00',
      },
      {
        id: 2,
        cardapio_id: 42,
        nota: 5,
        comentario: 'Muito bom',
        criado_em: '2026-10-24T14:30:00-03:00',
      },
    ],
    { refeicao: 'Almoço', campus: 'Darcy Ribeiro' },
  )

  assert.deepEqual(resultado.map(avaliacao => avaliacao.id), [2, 1])
  assert.deepEqual(resultado[0], {
    id: 2,
    autor: 'Anônimo',
    refeicao: 'Almoço',
    campus: 'Darcy Ribeiro',
    geral: 5,
    comentario: 'Muito bom',
    data: '24/10/2026',
    horario: '14:30',
  })
  assert.equal(resultado[1].comentario, '')
})
