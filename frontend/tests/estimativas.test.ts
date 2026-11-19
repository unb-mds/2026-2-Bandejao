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

test('falha da consulta real é propagada mesmo com simulação disponível', async () => {
  const consultar: typeof listarEstimativas = async params => {
    if (!params.dados_simulados) throw new Error('API indisponível')
    return [{ ...real, dados_simulados: true, contagem: 50 }]
  }
  await assert.rejects(carregarEstimativas(filtros, new AbortController().signal, consultar), /API indisponível/)
})

test('falha apenas da simulação preserva a contagem real válida e sua origem', async () => {
  const consultar: typeof listarEstimativas = async params => {
    if (params.dados_simulados) throw new Error('Simulação indisponível')
    return [real]
  }
  const resultado = await carregarEstimativas(filtros, new AbortController().signal, consultar)
  assert.deepEqual(resultado.get(7), real)
  assert.equal(resultado.get(7)?.contagem, 10)
  assert.equal(resultado.get(7)?.dados_simulados, false)
})

test('falha da simulação preserva dados insuficientes sem inventar contagem', async () => {
  const insuficiente = { ...real, cardapio_id: 8, status: 'dados_insuficientes' as const, contagem: undefined }
  const consultar: typeof listarEstimativas = async params => {
    if (params.dados_simulados) throw new Error('Simulação indisponível')
    return [real, insuficiente]
  }
  const resultado = await carregarEstimativas(filtros, new AbortController().signal, consultar)
  assert.deepEqual(resultado.get(7), real)
  assert.deepEqual(resultado.get(8), insuficiente)
})

test('cancelamento da consulta simulada não é tratado como falha opcional', async () => {
  const controller = new AbortController()
  const consultar: typeof listarEstimativas = async params => {
    if (params.dados_simulados) {
      controller.abort()
      throw new DOMException('Consulta cancelada', 'AbortError')
    }
    return [real]
  }
  await assert.rejects(carregarEstimativas(filtros, controller.signal, consultar), { name: 'AbortError' })
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
