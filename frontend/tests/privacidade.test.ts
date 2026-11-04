import assert from 'node:assert/strict'
import { test } from 'node:test'

import { CHAVE_AVISO_PRIVACIDADE, criarRegistroAvisoPrivacidade } from '../src/privacidade.ts'

test('primeira visita exige leitura sem gravar nada automaticamente', () => {
  const registro = criarRegistroAvisoPrivacidade(() => ({
    getItem: chave => { assert.equal(chave, CHAVE_AVISO_PRIVACIDADE); return null },
    setItem: () => assert.fail('a leitura não pode registrar ciência'),
  }))
  assert.equal(registro.foiLido(), false)
  assert.equal(registro.foiLido(), false)
})

test('Entendi persiste somente o aviso da versão atual e dispensa nova exibição', () => {
  const valores = new Map<string, string>()
  const armazenamento = {
    getItem: (chave: string) => valores.get(chave) ?? null,
    setItem: (chave: string, valor: string) => { valores.set(chave, valor) },
  }
  const registro = criarRegistroAvisoPrivacidade(() => armazenamento)
  registro.registrarLeitura()
  assert.equal(registro.foiLido(), true)
  assert.deepEqual([...valores.entries()], [[CHAVE_AVISO_PRIVACIDADE, 'lido']])
  assert.equal(criarRegistroAvisoPrivacidade(() => armazenamento).foiLido(), true)
  valores.clear()
  assert.equal(criarRegistroAvisoPrivacidade(() => armazenamento).foiLido(), false)
})

test('versões antigas ou valores inválidos não dispensam o aviso atual', () => {
  const valores = new Map([['bandejao.privacidade.v0', 'lido'], [CHAVE_AVISO_PRIVACIDADE, 'true']])
  const registro = criarRegistroAvisoPrivacidade(() => ({
    getItem: chave => valores.get(chave) ?? null,
    setItem: () => undefined,
  }))
  assert.equal(registro.foiLido(), false)
})

test('acesso bloqueado ao armazenamento permite registrar leitura durante esta página', () => {
  const registro = criarRegistroAvisoPrivacidade(() => { throw new Error('bloqueado') })
  assert.equal(registro.foiLido(), false)
  assert.doesNotThrow(() => registro.registrarLeitura())
  assert.equal(registro.foiLido(), true)
  assert.equal(criarRegistroAvisoPrivacidade(() => { throw new Error('bloqueado') }).foiLido(), false)
})

test('falhas de leitura e de escrita não bloqueiam a confirmação em memória', () => {
  const registro = criarRegistroAvisoPrivacidade(() => ({
    getItem: () => { throw new Error('leitura bloqueada') },
    setItem: () => { throw new Error('quota excedida') },
  }))
  assert.equal(registro.foiLido(), false)
  registro.registrarLeitura()
  assert.equal(registro.foiLido(), true)
})
