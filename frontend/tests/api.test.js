import assert from 'node:assert/strict'
import { test } from 'node:test'

import { listarCampi, listarCardapios, requisitarJson } from '../src/api.js'

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
