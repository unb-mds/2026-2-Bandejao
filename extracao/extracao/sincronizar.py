"""Comando para extrair e importar os cardápios publicados pelo RU."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from time import monotonic, sleep

from extracao.main import ErroExtracao, enviar_ao_backend, obter_token_importacao, run

INTERVALO_PADRAO_SEGUNDOS = 6 * 60 * 60


def sincronizar(url_base: str, token: str | None = None) -> dict[str, str]:
    """Processa os campi isoladamente, validando o segredo antes de acessar o RU."""
    token = obter_token_importacao(token)
    resultados = run()
    resumo: dict[str, str] = {}
    for campus, resultado in resultados.items():
        if isinstance(resultado, ErroExtracao):
            resumo[campus] = "falha na extração (ErroExtracao)"
            continue
        try:
            resposta = enviar_ao_backend(resultado, url_base, token=token)
            resumo[campus] = f"importado ({resposta['itens_processados']} itens)"
            print(json.dumps({
                "instante": datetime.now(timezone.utc).isoformat(),
                "campus": campus,
                "fonte_pdf_url": resultado.fonte_pdf_url,
                "status": "importado",
                "ultima_importacao_em": resposta.get("ultima_importacao_em"),
            }, ensure_ascii=False), flush=True)
        except Exception as erro:
            # Não imprimir exceções externas: podem conter headers ou segredos.
            resumo[campus] = f"falha na importação ({type(erro).__name__})"
    return resumo


def executar(url_base: str, intervalo: int, token: str | None = None) -> bool:
    """Executa imediatamente e repete a cada intervalo entre inícios de ciclos."""
    token = obter_token_importacao(token)
    while True:
        inicio = monotonic()
        instante = datetime.now(timezone.utc).isoformat()
        print(f"{instante} campus=todos início da sincronização", flush=True)
        try:
            resumo = sincronizar(url_base, token)
        except Exception as erro:
            # Falha na descoberta da fonte não encerra o serviço periódico.
            resumo = {"todos": f"falha no ciclo ({type(erro).__name__})"}
        for campus, status in resumo.items():
            instante = datetime.now(timezone.utc).isoformat()
            print(f"{instante} campus={campus} {status}", flush=True)
        houve_falha = any("falha" in status for status in resumo.values())
        if intervalo == 0:
            return not houve_falha
        # Ciclos nunca se sobrepõem; se um ciclo exceder o intervalo, o próximo
        # começa assim que o atual terminar.
        restante = intervalo - (monotonic() - inicio)
        sleep(max(0, restante))


def main() -> None:
    parser = argparse.ArgumentParser(description="Sincroniza os cardápios do RU com a API.")
    parser.add_argument(
        "--backend-url",
        default=os.getenv("BACKEND_URL", "http://localhost:8000"),
        help="URL base da API (padrão: BACKEND_URL ou http://localhost:8000).",
    )
    parser.add_argument(
        "--intervalo-segundos",
        type=int,
        default=0,
        help="Repete a sincronização nesse intervalo; 0 executa somente uma vez.",
    )
    argumentos = parser.parse_args()
    if argumentos.intervalo_segundos < 0:
        parser.error("--intervalo-segundos deve ser maior ou igual a zero.")
    try:
        token = obter_token_importacao()
    except ValueError as erro:
        parser.error(str(erro))
    sucesso = executar(argumentos.backend_url, argumentos.intervalo_segundos, token)
    if argumentos.intervalo_segundos == 0 and not sucesso:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
