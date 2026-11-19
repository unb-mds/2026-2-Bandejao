import assert from 'node:assert/strict'
import { test } from 'node:test'
import { carregarEstimativas } from '../src/estimativas.ts'
import type { EstimativaApi, listarEstimativas } from '../src/api.ts'

const filtros = { campus_id: '1', data_inicio: '2026-11-16', data_fim: '2026-11-22' }
const real: EstimativaApi = {
  cardapio_id: 7, campus_id: 1, data: '2026-11-19', tipo_refeicao: 'almoco',
  data_inicio: filtros.data_inicio, data_fim: filtros.data_fim,
  calculado_em: '2026-11-19T10:00:00Z', dados_simulados: false,
  amostra_minima: 10, status: 'disponivel', mensagem: 'Intenções', contagem: 10,
}

test('atualiza contagem e preserva preferência pelos dados reais após nova consulta', async () => {
  let contagem = 10
  const consultar: typeof listarEstimativas = async params => params.dados_simulados
    ? [{ ...real, dados_simulados: true, contagem: 50 }]
    : [{ ...real, contagem }]
  const signal = new AbortController().signal
  assert.equal((await carregarEstimativas(filtros, signal, consultar)).get(7)?.contagem, 10)
  contagem = 11
  assert.equal((await carregarEstimativas(filtros, signal, consultar)).get(7)?.contagem, 11)
})

test('simulação só substitui amostra real insuficiente e mantém seu rótulo', async () => {
  const consultar: typeof listarEstimativas = async params => params.dados_simulados
    ? [{ ...real, dados_simulados: true, contagem: 20 }]
    : [{ ...real, status: 'dados_insuficientes', contagem: undefined }]
  const valor = (await carregarEstimativas(filtros, new AbortController().signal, consultar)).get(7)
  assert.equal(valor?.contagem, 20)
  assert.equal(valor?.dados_simulados, true)
})

test('falha em qualquer consulta é propagada em vez de produzir contagem antiga', async () => {
  for (const falhaSimulada of [false, true]) {
    const consultar: typeof listarEstimativas = async params => {
      if (!!params.dados_simulados === falhaSimulada) throw new Error('API indisponível')
      return [real]
    }
    await assert.rejects(carregarEstimativas(filtros, new AbortController().signal, consultar), /API indisponível/)
  }
})

test('envia mesmo campus, semana e sinal de cancelamento a ambas as consultas', async () => {
  const controller = new AbortController()
  const chamadas: unknown[] = []
  const consultar: typeof listarEstimativas = async (params, opcoes) => {
    assert.equal(opcoes?.signal, controller.signal)
    chamadas.push(params)
    return []
  }
  assert.equal((await carregarEstimativas(filtros, controller.signal, consultar)).size, 0)
  assert.deepEqual(chamadas, [filtros, { ...filtros, dados_simulados: true }])
})
