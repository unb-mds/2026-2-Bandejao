import json
from http.client import BadStatusLine, IncompleteRead
from urllib.request import Request

import pytest

import verificar_publicacao
from verificar_publicacao import requisitar, url_https, verificar

SHA = "a" * 40


def transporte(url, metodo="GET", headers=None):
    resposta = {"status": 200, "headers": {}, "corpo": ""}
    if metodo == "OPTIONS":
        resposta["headers"] = {
            "access-control-allow-origin": "https://front.test",
            "access-control-allow-headers": "content-type, X-Identidade",
            "access-control-allow-methods": "GET, POST, OPTIONS",
        }
    elif url == "https://front.test":
        resposta["corpo"] = '<html><div id="root"></div></html>'
    elif url.endswith("/health"):
        resposta["corpo"] = json.dumps({"status": "ok"})
    elif url.endswith("/version"):
        resposta["corpo"] = json.dumps({"version": SHA})
    elif url.endswith("/campi/"):
        resposta["corpo"] = json.dumps([{"id": 1, "nome": "Gama"}])
        resposta["headers"]["access-control-allow-origin"] = "https://front.test"
    elif url.endswith("/cardapios/"):
        resposta["corpo"] = json.dumps([{"campus_id": 1, "itens": [{"nome": "Exemplo"}]}])
    return resposta


def test_ambiente_valido_confere_contrato_real_sem_enviar_escrita():
    metodos = []

    def consultar(url, metodo="GET", headers=None):
        metodos.append(metodo)
        return transporte(url, metodo, headers)

    resultado = verificar("https://front.test", "https://api.test", SHA, consultar)
    assert resultado["aprovado"]
    assert len(resultado["checagens"]) == 5
    assert set(metodos) == {"GET", "OPTIONS"}


@pytest.mark.parametrize("url", [
    "http://front.test", "https://usuario:segredo@front.test", "https://front.test?token=x",
    "https://front.test#fragmento", "file:///etc/passwd",
])
def test_rejeita_url_insegura_ou_com_credenciais_antes_da_rede(url):
    with pytest.raises(ValueError, match="HTTPS"):
        url_https(url)


def test_sha_diferente_nao_aprova_versao_publicada():
    resultado = verificar("https://front.test", "https://api.test", "b" * 40, transporte)
    assert not resultado["aprovado"]
    assert resultado["checagens"][2]["resultado"] == "falhou"


@pytest.mark.parametrize("caminho", ["/health", "/version", "/campi/", "/cardapios/"])
def test_json_invalido_nao_interrompe_relatorio(caminho):
    def consultar(url, metodo="GET", headers=None):
        resposta = transporte(url, metodo, headers)
        if url.endswith(caminho):
            resposta["corpo"] = '"formato inesperado"'
        return resposta

    resultado = verificar("https://front.test", "https://api.test", SHA, consultar)
    assert not resultado["aprovado"]
    assert len(resultado["checagens"]) == 5


def test_falha_de_preflight_e_registrada_sem_post():
    def consultar(url, metodo="GET", headers=None):
        resposta = transporte(url, metodo, headers)
        if metodo == "OPTIONS":
            resposta["headers"]["access-control-allow-headers"] = "content-type"
        return resposta

    resultado = verificar("https://front.test", "https://api.test", SHA, consultar)
    assert not resultado["aprovado"]
    assert resultado["checagens"][-1]["resultado"] == "falhou"


def test_urls_indisponiveis_produzem_relatorio_reprovado():
    def consultar(*args, **kwargs):
        raise ValueError("HTTP 404")

    resultado = verificar("https://front.test", "https://api.test", SHA, consultar)
    assert not resultado["aprovado"]
    assert all(check["resultado"] == "falhou" for check in resultado["checagens"])


def test_timeout_de_leitura_vira_falha_segura_sem_detalhes_locais(monkeypatch):
    def timeout(*args, **kwargs):
        raise TimeoutError("detalhe privado do proxy")

    monkeypatch.setattr(verificar_publicacao, "abrir_https", timeout)
    with pytest.raises(ValueError, match="Falha de conexão") as erro:
        requisitar("https://api.test/health")
    assert "proxy" not in str(erro.value)


@pytest.mark.parametrize("erro_rede", [BadStatusLine("proxy privado"), IncompleteRead(b"privado")])
def test_protocolo_truncado_nao_aborta_relatorio(monkeypatch, erro_rede):
    def falhar(*args, **kwargs):
        raise erro_rede

    monkeypatch.setattr(verificar_publicacao, "abrir_https", falhar)
    resultado = verificar("https://front.test", "https://api.test", SHA)
    assert not resultado["aprovado"]
    assert len(resultado["checagens"]) == 5
    assert "privado" not in json.dumps(resultado)


@pytest.mark.parametrize("destino", ["http://api.test/", "http://api.test/voltar-para-https"])
def test_redirecionamento_http_e_recusado_antes_de_seguir(destino):
    handler = verificar_publicacao.SomenteHttpsRedirectHandler()
    with pytest.raises(ValueError, match="HTTPS"):
        handler.redirect_request(Request("https://api.test/"), None, 302, "Found", {}, destino)


@pytest.mark.parametrize("valor", ["https://api.test:abc", "https://api.test:99999", "https://api.test\n"])
def test_rejeita_porta_invalida_e_caracteres_de_controle(valor):
    with pytest.raises(ValueError):
        url_https(valor)
