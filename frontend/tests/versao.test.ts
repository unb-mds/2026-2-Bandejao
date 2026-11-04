import assert from 'node:assert/strict'
import test from 'node:test'

import { formatarVersao } from '../src/versao.ts'

test('encurta o SHA publicado para uma versão legível', () => {
  assert.equal(
    formatarVersao('299d9f4c3b2a190876543210fedcba9876543210'),
    '299d9f4c3b2a',
  )
})

test('preserva tags e informa desenvolvimento quando não há versão', () => {
  assert.equal(formatarVersao('v2.0.0'), 'v2.0.0')
  assert.equal(formatarVersao('  '), 'desenvolvimento')
  assert.equal(formatarVersao(undefined), 'desenvolvimento')
})
