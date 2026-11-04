const CHAVE_IDENTIDADE = 'bandejao.identidade'
const UUID_V4 = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

type Armazenamento = Pick<Storage, 'getItem' | 'setItem'>

export function criarGerenciadorIdentidade(
  obterArmazenamento: () => Armazenamento = () => globalThis.localStorage,
  gerarUuid: () => string = () => globalThis.crypto.randomUUID(),
) {
  let identidadeEmMemoria: string | null = null

  return function obterIdentidade(): string {
    if (identidadeEmMemoria) return identidadeEmMemoria

    let armazenamento: Armazenamento | undefined
    try {
      armazenamento = obterArmazenamento()
      const identidadeSalva = armazenamento.getItem(CHAVE_IDENTIDADE)
      if (identidadeSalva && UUID_V4.test(identidadeSalva)) {
        identidadeEmMemoria = identidadeSalva
        return identidadeEmMemoria
      }
    } catch {
      // Alguns navegadores bloqueiam o localStorage; a memória mantém a sessão estável.
    }

    const novaIdentidade = gerarUuid()
    if (!UUID_V4.test(novaIdentidade)) {
      throw new Error('Não foi possível gerar uma identidade anônima válida.')
    }
    identidadeEmMemoria = novaIdentidade

    try {
      armazenamento ??= obterArmazenamento()
      armazenamento.setItem(CHAVE_IDENTIDADE, novaIdentidade)
    } catch {
      // O envio ainda funciona durante a sessão quando a persistência local falha.
    }

    return identidadeEmMemoria
  }
}

export const obterIdentidadeAnonima = criarGerenciadorIdentidade()
