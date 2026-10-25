import assert from 'node:assert/strict'
import { test } from 'node:test'

import {
  listarAvaliacoes,
  listarCampi,
  listarCardapios,
  requisitarJson,
  salvarAvaliacao,
} from '../src/api.ts'

test('carrega campi pela rota da API', async () => {
  let urlRecebida

  const resultado = await listarCampi({
    baseUrl: 'https://api.exemplo.test',
    fetchImpl: async (url) => {
      urlRecebida = new URL(url)
      return { ok: true, json: async () => [{ id: 2, nome: 'Gama' }] }
    },
  })

  assert.deepEqual(resultado, [{ id: 2, nome: 'Gama' }])
  assert.equal(urlRecebida.pathname, '/campi/')
})

test('consulta cardápios envia filtros preenchidos e omite os vazios', async () => {
  let urlRecebida

  const resultado = await listarCardapios(
    {
      campus_id: 4,
      data_inicio: '2026-09-28',
      data_fim: '',
      tipo_refeicao: 'almoco',
    },
    {
      baseUrl: 'https://api.exemplo.test/',
      fetchImpl: async (url) => {
        urlRecebida = new URL(url)
        return { ok: true, json: async () => [{ id: 3 }] }
      },
    },
  )

  assert.deepEqual(resultado, [{ id: 3 }])
  assert.equal(urlRecebida.pathname, '/cardapios/')
  assert.equal(urlRecebida.searchParams.get('campus_id'), '4')
  assert.equal(urlRecebida.searchParams.get('data_inicio'), '2026-09-28')
  assert.equal(urlRecebida.searchParams.get('tipo_refeicao'), 'almoco')
  assert.equal(urlRecebida.searchParams.has('data_fim'), false)
})

test('usa o detalhe retornado pela API quando uma consulta falha', async () => {
  await assert.rejects(
    requisitarJson('campi/', {}, {
      baseUrl: 'https://api.exemplo.test',
      fetchImpl: async () => ({
        ok: false,
        status: 503,
        json: async () => ({ detail: 'Banco indisponível' }),
      }),
    }),
    { message: 'Banco indisponível' },
  )
})

test('informa o status HTTP se a resposta de erro não tiver JSON', async () => {
  await assert.rejects(
    requisitarJson('cardapios/', {}, {
      baseUrl: 'https://api.exemplo.test',
      fetchImpl: async () => ({
        ok: false,
        status: 502,
        json: async () => {
          throw new Error('resposta vazia')
        },
      }),
    }),
    { message: 'A API respondeu com HTTP 502.' },
  )
})

test('envia avaliação com a identidade anônima no cabeçalho', async () => {
  let urlRecebida
  let opcoesRecebidas
  const identidade = '123e4567-e89b-42d3-a456-426614174000'

  const resultado = await salvarAvaliacao(
    42,
    { nota: 5, comentario: 'Muito bom' },
    identidade,
    {
      baseUrl: 'https://api.exemplo.test',
      fetchImpl: async (url, opcoes) => {
        urlRecebida = new URL(url)
        opcoesRecebidas = opcoes
        return {
          ok: true,
          status: 201,
          json: async () => ({ id: 7, cardapio_id: 42, nota: 5 }),
        }
      },
    },
  )

  assert.equal(urlRecebida.pathname, '/cardapios/42/avaliacoes/')
  assert.equal(opcoesRecebidas.method, 'POST')
  assert.equal(opcoesRecebidas.headers['X-Identidade'], identidade)
  assert.equal(opcoesRecebidas.headers['Content-Type'], 'application/json')
  assert.deepEqual(JSON.parse(opcoesRecebidas.body), { nota: 5, comentario: 'Muito bom' })
  assert.equal(resultado.id, 7)
})

test('consulta somente o histórico da refeição informada', async () => {
  let urlRecebida

  const resultado = await listarAvaliacoes(42, {
    baseUrl: 'https://api.exemplo.test',
    fetchImpl: async (url, opcoes) => {
      urlRecebida = new URL(url)
      assert.equal(opcoes.method, 'GET')
      return {
        ok: true,
        status: 200,
        json: async () => [
          { id: 8, cardapio_id: 42, nota: 4, comentario: null, criado_em: '2026-10-24T14:00:00-03:00' },
        ],
      }
    },
  })

  assert.equal(urlRecebida.pathname, '/cardapios/42/avaliacoes/')
  assert.equal(resultado.length, 1)
  assert.equal(resultado[0].cardapio_id, 42)
})

test('traduz erro de campo inválido retornado pela API', async () => {
  await assert.rejects(
    salvarAvaliacao(
      42,
      { nota: 6, comentario: null },
      '123e4567-e89b-42d3-a456-426614174000',
      {
        baseUrl: 'https://api.exemplo.test',
        fetchImpl: async () => ({
          ok: false,
          status: 422,
          json: async () => ({
            detail: [{
              type: 'less_than_equal',
              loc: ['body', 'nota'],
              msg: 'Input should be less than or equal to 5',
              ctx: { le: 5 },
            }],
          }),
        }),
      },
    ),
    { message: 'Campo “nota”: deve ser menor ou igual a 5.' },
  )
})
