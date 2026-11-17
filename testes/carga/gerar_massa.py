"""Cria os dados falsos do teste de carga do RNF01 (issue #96).

Manda para a API, pela rota de importação, 4 semanas de cardápio para 5 campi,
com 3 refeições por dia e 10 itens por refeição. Os campi ganham o prefixo
"[carga]" para não se misturarem com os dados reais do RU.

Uso:
    IMPORTACAO_TOKEN=... python gerar_massa.py --api-url http://localhost:8000

No fim, salva o arquivo massa.json, que o script do k6 usa.
"""

import argparse
from datetime import date, timedelta
import json
import os
import urllib.request

CAMPI = ["Darcy Ribeiro", "Ceilândia", "Gama", "Planaltina", "Fazenda Água Limpa"]
REFEICOES = ["cafe_da_manha", "almoco", "jantar"]
SEMANAS = 4

# Os 10 itens de cada refeição: (categoria, dieta, alérgenos).
ITENS = [
    ("prato_principal", "padrao", ["leite", "gluten"]),
    ("guarnicao", "padrao", ["ovo"]),
    ("acompanhamento", "padrao", []),
    ("salada_1", "padrao", []),
    ("salada_2", "padrao", ["soja"]),
    ("molho_salada", "padrao", ["mel"]),
    ("sopa", "ovolactovegetariano", ["leite"]),
    ("sobremesa", "ovolactovegetariano", ["leite", "ovo", "gluten"]),
    ("fruta", "vegetariano_estrito", []),
    ("bebida", "vegetariano_estrito", ["amendoim"]),
]


def montar_cardapio(campus, primeira_segunda):
    refeicoes = []
    for dia in range(SEMANAS * 7):
        data = primeira_segunda + timedelta(days=dia)
        for refeicao in REFEICOES:
            itens = []
            for numero, (categoria, dieta, alergenos) in enumerate(ITENS, start=1):
                itens.append({
                    "categoria": categoria,
                    "tipo_dieta": dieta,
                    "nome": f"Item {numero} - {refeicao} {data}",
                    "alergenos": alergenos,
                })
            refeicoes.append({"data": str(data), "tipo_refeicao": refeicao, "itens": itens})
    return {"campus": "[carga] " + campus, "fonte_pdf_url": None, "refeicoes": refeicoes}


def importar(api_url, token, cardapio):
    pedido = urllib.request.Request(
        api_url + "/cardapios/importacao",
        data=json.dumps(cardapio).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + token},
    )
    # A URL é a da API informada por quem roda o script.
    with urllib.request.urlopen(pedido, timeout=60) as resposta:  # nosec B310
        return json.loads(resposta.read())


def main():
    parser = argparse.ArgumentParser(description="Cria os dados falsos do teste de carga.")
    parser.add_argument("--api-url", default="http://localhost:8000")
    parser.add_argument("--inicio", help="Segunda-feira da primeira semana (AAAA-MM-DD). Padrão: esta semana.")
    args = parser.parse_args()

    token = os.getenv("IMPORTACAO_TOKEN")
    if not token:
        parser.error("Defina IMPORTACAO_TOKEN com o mesmo valor configurado na API.")

    hoje = date.fromisoformat(args.inicio) if args.inicio else date.today()
    primeira_segunda = hoje - timedelta(days=hoje.weekday())
    api_url = args.api_url.rstrip("/")

    campi = []
    for campus in CAMPI:
        resultado = importar(api_url, token, montar_cardapio(campus, primeira_segunda))
        campi.append({"id": resultado["campus_id"], "nome": "[carga] " + campus})
        print(f"[carga] {campus}: {resultado['itens_processados']} itens importados")

    massa = {
        "api_url": api_url,
        "campi": campi,
        "semanas": [str(primeira_segunda + timedelta(weeks=s)) for s in range(SEMANAS)],
        "dietas": ["ovolactovegetariano", "vegetariano_estrito"],
        "exclusoes": ["leite", "gluten", "ovo"],
    }
    with open("massa.json", "w", encoding="utf-8") as arquivo:
        json.dump(massa, arquivo, ensure_ascii=False, indent=2)
    print("Pronto: massa.json criado.")


if __name__ == "__main__":
    main()
