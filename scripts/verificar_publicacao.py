"""Conferência somente leitura de um ambiente HTTPS do Bandejão.

Não cria serviços, não envia avaliações e não recebe tokens. A revisão em um
navegador externo continua necessária para aceitar a issue 55.
"""

import argparse
from datetime import datetime, timezone
from http.client import HTTPException
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


def url_https(valor: str) -> str:
    if any(caractere.isspace() or ord(caractere) < 32 for caractere in valor):
        raise ValueError("A URL HTTPS não pode conter espaços ou caracteres de controle.")
    url = urlsplit(valor)
    _ = url.port  # Valida portas não numéricas e valores fora do intervalo permitido.
    if (
        url.scheme != "https" or not url.hostname or url.username or url.password
        or url.query or url.fragment
    ):
        raise ValueError("Informe uma URL HTTPS sem credenciais, consulta ou fragmento.")
    return valor.rstrip("/")


class SomenteHttpsRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Verificar antes do acesso evita aceitar HTTPS -> HTTP -> HTTPS.
        url_https(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


abrir_https = build_opener(SomenteHttpsRedirectHandler()).open


def requisitar(url: str, metodo: str = "GET", headers: dict | None = None) -> dict:
    request = Request(url, method=metodo, headers=headers or {})
    try:
        with abrir_https(request, timeout=30) as resposta:
            if urlsplit(resposta.url).scheme != "https":
                raise ValueError("O destino redirecionou para uma URL sem HTTPS.")
            corpo = resposta.read(2_000_001)
            if len(corpo) > 2_000_000:
                raise ValueError("A resposta excedeu o limite de leitura.")
            return {
                "status": resposta.status,
                "headers": {chave.lower(): valor for chave, valor in resposta.headers.items()},
                "corpo": corpo.decode("utf-8"),
            }
    except HTTPError as erro:
        raise ValueError(f"HTTP {erro.code}") from erro
    except (URLError, OSError, HTTPException) as erro:
        # Não registrar dados da exceção: podem conter detalhes locais/proxy.
        raise ValueError("Falha de conexão ou de verificação do certificado TLS.") from erro


def verificar(frontend: str, api: str, sha: str, consultar=requisitar) -> dict:
    frontend, api = url_https(frontend), url_https(api)
    if not re.fullmatch(r"[0-9a-fA-F]{40}", sha):
        raise ValueError("Informe o SHA completo de 40 caracteres da versão esperada.")
    sha = sha.lower()
    origem = f"{urlsplit(frontend).scheme}://{urlsplit(frontend).netloc}"
    checks = []

    def executar(nome, funcao):
        try:
            detalhe = funcao()
            checks.append({"checagem": nome, "resultado": "aprovado", "detalhe": detalhe})
        except (ValueError, TypeError, KeyError, IndexError) as erro:
            checks.append({"checagem": nome, "resultado": "falhou", "detalhe": str(erro)})

    def interface():
        resposta = consultar(frontend)
        if resposta["status"] != 200 or 'id="root"' not in resposta["corpo"]:
            raise ValueError("A URL não entregou o HTML esperado da aplicação.")
        return "HTML da aplicação acessível por HTTPS; renderização requer navegador."

    def json_api(caminho):
        resposta = consultar(f"{api}/{caminho}")
        if resposta["status"] != 200:
            raise ValueError(f"HTTP {resposta['status']}")
        return json.loads(resposta["corpo"])

    def saude():
        corpo = json_api("health")
        if not isinstance(corpo, dict) or corpo.get("status") != "ok":
            raise ValueError("Healthcheck não confirmou status ok.")
        return "API respondeu ao healthcheck."

    def versao():
        corpo = json_api("version")
        versao_publicada = corpo.get("version") if isinstance(corpo, dict) else None
        if not isinstance(versao_publicada, str) or versao_publicada.lower() != sha:
            raise ValueError("O commit retornado pela API difere do esperado.")
        return sha

    def dados():
        campi = json_api("campi/")
        menus = json_api("cardapios/")
        if not isinstance(campi, list) or not campi or not isinstance(menus, list) or not menus:
            raise ValueError("Não há campi e cardápios disponíveis para conferir a integração.")
        ids = {campus["id"] for campus in campi}
        if any(menu["campus_id"] not in ids for menu in menus):
            raise ValueError("Há cardápio vinculado a campus ausente da listagem.")
        itens = sum(len(menu["itens"]) for menu in menus)
        if itens == 0:
            raise ValueError("Os cardápios não possuem itens publicados.")
        return {"campi": len(campi), "refeicoes": len(menus), "itens": itens}

    def cors():
        resposta = consultar(f"{api}/campi/", headers={"Origin": origem})
        if resposta["headers"].get("access-control-allow-origin") != origem:
            raise ValueError("A API não permite a origem do frontend no CORS.")
        preflight = consultar(f"{api}/cardapios/1/avaliacoes/", "OPTIONS", {
            "Origin": origem, "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,x-identidade",
        })
        cabecalhos = preflight["headers"]
        permitidos = {valor.strip().lower() for valor in cabecalhos.get(
            "access-control-allow-headers", "").split(",")}
        metodos = {valor.strip().upper() for valor in cabecalhos.get(
            "access-control-allow-methods", "").split(",")}
        if (
            preflight["status"] != 200
            or cabecalhos.get("access-control-allow-origin") != origem
            or not {"content-type", "x-identidade"}.issubset(permitidos)
            or "POST" not in metodos
        ):
            raise ValueError("Preflight não permite POST com Content-Type e X-Identidade.")
        return "GET e preflight de avaliação autorizam a origem; nenhum POST foi enviado."

    for nome, funcao in [
        ("frontend_https", interface), ("api_health", saude), ("versao", versao),
        ("dados_publicados", dados), ("cors", cors),
    ]:
        executar(nome, funcao)
    return {
        "instante_utc": datetime.now(timezone.utc).isoformat(),
        "frontend": frontend, "api": api, "commit_esperado": sha,
        "checagens": checks,
        "aprovado": all(check["resultado"] == "aprovado" for check in checks),
        "limite": "Não substitui navegação externa, conferência visual da versão e persistência real.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frontend", required=True)
    parser.add_argument("--api", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--saida", type=Path)
    args = parser.parse_args()
    try:
        relatorio = verificar(args.frontend, args.api, args.commit)
    except ValueError as erro:
        parser.error(str(erro))
    texto = json.dumps(relatorio, ensure_ascii=False, indent=2) + "\n"
    if args.saida:
        args.saida.parent.mkdir(parents=True, exist_ok=True)
        args.saida.write_text(texto, encoding="utf-8")
    print(texto, end="")
    raise SystemExit(0 if relatorio["aprovado"] else 1)


if __name__ == "__main__":
    main()
