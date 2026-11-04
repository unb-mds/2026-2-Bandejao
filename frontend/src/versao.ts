export function formatarVersao(valor: string | undefined): string {
  const versao = valor?.trim()
  if (!versao) return 'desenvolvimento'
  return /^[0-9a-f]{40}$/i.test(versao) ? versao.slice(0, 12) : versao
}

export const VERSAO_APP = formatarVersao(import.meta.env?.VITE_APP_VERSION)
