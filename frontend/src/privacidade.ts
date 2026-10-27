// Uma alteração no aviso que exija nova leitura deve incrementar a versão da chave.
export const CHAVE_AVISO_PRIVACIDADE = 'bandejao.privacidade.v1'

type Armazenamento = Pick<Storage, 'getItem' | 'setItem'>

export function criarRegistroAvisoPrivacidade(
  obterArmazenamento: () => Armazenamento = () => globalThis.localStorage,
) {
  let lidoNestaPagina = false

  return {
    foiLido(): boolean {
      if (lidoNestaPagina) return true
      try {
        return obterArmazenamento().getItem(CHAVE_AVISO_PRIVACIDADE) === 'lido'
      } catch {
        return false
      }
    },
    registrarLeitura(): void {
      lidoNestaPagina = true
      try {
        obterArmazenamento().setItem(CHAVE_AVISO_PRIVACIDADE, 'lido')
      } catch {
        // Sem persistência, a confirmação vale nesta página; recarregar exibe o aviso.
      }
    },
  }
}

export const registroAvisoPrivacidade = criarRegistroAvisoPrivacidade()
