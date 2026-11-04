import assert from 'node:assert/strict'
import { test } from 'node:test'

import { criarGerenciadorIdentidade } from '../src/identidade.ts'

const IDENTIDADE_SALVA = '123e4567-e89b-42d3-a456-426614174000'
const IDENTIDADE_NOVA = '123e4567-e89b-42d3-a456-426614174001'

test('reutiliza a identidade v4 salva no navegador', () => {
  const armazenamento = {
    getItem: () => IDENTIDADE_SALVA,
    setItem: () => assert.fail('não deveria substituir uma identidade válida'),
  }
  const obterIdentidade = criarGerenciadorIdentidade(
    () => armazenamento,
    () => assert.fail('não deveria gerar uma nova identidade'),
  )

  assert.equal(obterIdentidade(), IDENTIDADE_SALVA)
  assert.equal(obterIdentidade(), IDENTIDADE_SALVA)
})

test('gera e persiste uma identidade quando ainda não existe', () => {
  let valorSalvo = null
  const armazenamento = {
    getItem: () => null,
    setItem: (_chave: string, valor: string) => { valorSalvo = valor },
  }
  const obterIdentidade = criarGerenciadorIdentidade(
    () => armazenamento,
    () => IDENTIDADE_NOVA,
  )

  assert.equal(obterIdentidade(), IDENTIDADE_NOVA)
  assert.equal(valorSalvo, IDENTIDADE_NOVA)
})

test('mantém a identidade em memória quando o localStorage falha', () => {
  let geracoes = 0
  const armazenamento = {
    getItem: () => { throw new Error('bloqueado') },
    setItem: () => { throw new Error('bloqueado') },
  }
  const obterIdentidade = criarGerenciadorIdentidade(
    () => armazenamento,
    () => { geracoes += 1; return IDENTIDADE_NOVA },
  )

  assert.equal(obterIdentidade(), IDENTIDADE_NOVA)
  assert.equal(obterIdentidade(), IDENTIDADE_NOVA)
  assert.equal(geracoes, 1)
})

test('substitui valor inválido e rejeita UUID gerado fora da versão 4', () => {
  const armazenamento = { getItem: () => 'inválido', setItem: () => undefined }
  const obterIdentidade = criarGerenciadorIdentidade(
    () => armazenamento,
    () => '6ba7b810-9dad-11d1-80b4-00c04fd430c8',
  )

  assert.throws(obterIdentidade, /identidade anônima válida/)
})
