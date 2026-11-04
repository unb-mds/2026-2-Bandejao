import assert from 'node:assert/strict'
import { test } from 'node:test'

import { refeicaoJaIniciada } from '../src/utils.ts'

// Comparado em horário local (sem offset explícito), igual à função: evita depender
// do fuso horário de quem roda o teste.
test('refeição ainda não iniciada antes do horário de início', () => {
  const antes = new Date('2026-11-03T10:59:00')
  assert.equal(refeicaoJaIniciada('2026-11-03', 'almoco', antes), false)
})

test('refeição considerada iniciada exatamente no horário de início', () => {
  const noInicio = new Date('2026-11-03T11:00:00')
  assert.equal(refeicaoJaIniciada('2026-11-03', 'almoco', noInicio), true)
})

test('refeição iniciada depois do horário de início', () => {
  const depois = new Date('2026-11-03T11:01:00')
  assert.equal(refeicaoJaIniciada('2026-11-03', 'almoco', depois), true)
})
