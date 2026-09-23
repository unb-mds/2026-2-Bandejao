"""Comando para extrair e importar os cardápios publicados pelo RU."""

from __future__ import annotations

import argparse
import os
from time import sleep

import requests

from extracao.main import ErroExtracao, enviar_ao_backend, run

INTERVALO_PADRAO_SEGUNDOS = 6 * 60 * 60


def sincronizar(url_base: str) -> dict[str, str]:
    """Processa todos os campi, mantendo o erro de um deles isolado dos demais."""
    resultados = run()
    resumo: dict[str, str] = {}
    for campus, resultado in resultados.items():
        if isinstance(resultado, ErroExtracao):
            resumo[campus] = f"falha na extração: {resultado}"
            continue
        try:
            resposta = enviar_ao_backend(resultado, url_base)
            resumo[campus] = f"importado ({resposta['itens_processados']} itens)"
        except (requests.RequestException, ValueError, KeyError) as erro:
            # Um campus indisponível não impede que os demais sejam enviados nesta execução.
            resumo[campus] = f"falha na importação: {erro}"
    return resumo


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

    while True:
        for campus, status in sincronizar(argumentos.backend_url).items():
            print(f"{campus}: {status}")
        if argumentos.intervalo_segundos == 0:
            break
        # O modo contínuo é opcional para também permitir uso por agendadores externos.
        sleep(argumentos.intervalo_segundos)


if __name__ == "__main__":
    main()
