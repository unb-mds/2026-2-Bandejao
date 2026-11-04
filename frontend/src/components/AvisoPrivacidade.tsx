import { useEffect, useRef } from 'react'

interface AvisoPrivacidadeProps {
  aberto: boolean
  onConfirmar: () => void
  onFechar: () => void
}

export default function AvisoPrivacidade({ aberto, onConfirmar, onFechar }: AvisoPrivacidadeProps) {
  const dialogRef = useRef<HTMLDialogElement>(null)
  const origemFoco = useRef<HTMLElement | null>(null)

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return
    if (aberto && !dialog.open) {
      origemFoco.current = document.activeElement instanceof HTMLElement ? document.activeElement : null
      dialog.showModal()
    } else if (!aberto && dialog.open) {
      dialog.close()
    }
  }, [aberto])

  const fechar = () => {
    onFechar()
    const origem = origemFoco.current
    if (origem && origem !== document.body && origem.isConnected) origem.focus()
    else document.getElementById('main-content')?.focus()
  }

  return (
    <dialog
      ref={dialogRef}
      aria-labelledby="aviso-privacidade-titulo"
      aria-describedby="aviso-privacidade-resumo"
      onClose={fechar}
      className="m-auto max-h-[90dvh] w-[calc(100%-2rem)] max-w-lg overflow-y-auto rounded-2xl border border-border bg-background p-6 text-foreground shadow-xl backdrop:bg-black/50"
    >
      <h2 id="aviso-privacidade-titulo" className="text-xl font-bold">Sua privacidade no Bandejão</h2>
      <div className="mt-4 space-y-3 text-sm leading-relaxed">
        <p id="aviso-privacidade-resumo">Para avaliar ou reclamar, não pedimos nome nem e-mail. Um código anônimo aleatório vincula seus envios e fica salvo neste navegador. Se o armazenamento estiver bloqueado, o código vale só enquanto a página estiver aberta.</p>
        <p>Ao limpar os dados do site e abrir novamente, outro código será gerado no próximo envio. Isso não apaga os registros já enviados.</p>
        <p>Notas, comentários e reclamações são salvos na API. Comentários das avaliações aparecem no histórico público. Reclamações não têm lista pública nem encaminhamento automático ao RU. Evite informar dados pessoais nos textos.</p>
        <p>“Entendi” registra apenas que você leu este aviso neste navegador. Você pode reler em <strong>Privacidade</strong>, no rodapé.</p>
      </div>
      <button type="button" autoFocus onClick={onConfirmar} className="mt-5 rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground">Entendi</button>
    </dialog>
  )
}
