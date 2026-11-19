import assert from 'node:assert/strict'
import { test } from 'node:test'

import { getCurrentMealInfo, refeicaoJaIniciada } from '../src/utils.ts'

test('prazo do almoço usa 14h UTC, equivalente a 11h de Brasília', () => {
  assert.equal(refeicaoJaIniciada('2026-11-03', 'almoco', new Date('2026-11-03T13:59:59Z')), false)
  assert.equal(refeicaoJaIniciada('2026-11-03', 'almoco', new Date('2026-11-03T14:00:00Z')), true)
  assert.equal(refeicaoJaIniciada('2026-11-03', 'cafe', new Date('2026-11-03T10:00:00Z')), true)
  assert.equal(refeicaoJaIniciada('2026-11-03', 'jantar', new Date('2026-11-03T19:59:59Z')), false)
})

test('refeição corrente segue Brasília mesmo quando o instante está em UTC', () => {
  assert.deepEqual(getCurrentMealInfo(new Date('2026-11-03T13:30:00Z')), { tipo: 'almoco', status: 'proxima' })
  assert.deepEqual(getCurrentMealInfo(new Date('2026-11-03T14:00:00Z')), { tipo: 'almoco', status: 'agora' })
})

// Instantes explícitos de Brasília: o resultado independe do fuso do computador.
test('refeição ainda não iniciada antes do horário de início', () => {
  const antes = new Date('2026-11-03T10:59:00-03:00')
  assert.equal(refeicaoJaIniciada('2026-11-03', 'almoco', antes), false)
})

test('refeição considerada iniciada exatamente no horário de início', () => {
  const noInicio = new Date('2026-11-03T11:00:00-03:00')
  assert.equal(refeicaoJaIniciada('2026-11-03', 'almoco', noInicio), true)
})

test('refeição iniciada depois do horário de início', () => {
  const depois = new Date('2026-11-03T11:01:00-03:00')
  assert.equal(refeicaoJaIniciada('2026-11-03', 'almoco', depois), true)
})
