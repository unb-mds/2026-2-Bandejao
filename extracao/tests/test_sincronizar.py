import pytest
import requests

from extracao import sincronizar
from extracao.main import ErroExtracao, ResultadoExtracao, enviar_ao_backend


@pytest.fixture(autouse=True)
def token(monkeypatch):
    monkeypatch.setenv("IMPORTACAO_TOKEN", "segredo-teste")


def test_sincronizar_importa_campi_validos_e_isola_falhas(monkeypatch):
    resultado = ResultadoExtracao("Gama", "https://exemplo.test/gama.pdf", [])
    monkeypatch.setattr(sincronizar, "run", lambda: {
        "Gama": resultado, "Ceilândia": ErroExtracao("PDF indisponível"),
    })

    def enviar(recebido, url, *, token):
        assert recebido is resultado
        assert url == "http://api.test"
        assert token == "segredo-teste"
        return {"itens_processados": 3}

    monkeypatch.setattr(sincronizar, "enviar_ao_backend", enviar)
    assert sincronizar.sincronizar("http://api.test") == {
        "Gama": "importado (3 itens)",
        "Ceilândia": "falha na extração (ErroExtracao)",
    }


def test_falha_api_nao_impede_proximo_campus_nem_expoe_segredo(monkeypatch):
    monkeypatch.setattr(sincronizar, "run", lambda: {
        nome: ResultadoExtracao(nome, "https://exemplo.test/menu.pdf", [])
        for nome in ["Gama", "Ceilândia"]
    })

    def enviar(resultado, *args, **kwargs):
        if resultado.campus == "Gama":
            raise requests.HTTPError("Authorization: Bearer segredo-teste")
        return {"itens_processados": 2}

    monkeypatch.setattr(sincronizar, "enviar_ao_backend", enviar)
    resumo = sincronizar.sincronizar("http://api.test")
    assert resumo["Gama"] == "falha na importação (HTTPError)"
    assert resumo["Ceilândia"] == "importado (2 itens)"
    assert "segredo-teste" not in str(resumo)


@pytest.mark.parametrize("valor", [None, "", "   ", "segredo\nerrado"])
def test_sem_token_valido_nao_acessa_rede(monkeypatch, valor):
    if valor is None:
        monkeypatch.delenv("IMPORTACAO_TOKEN", raising=False)
    else:
        monkeypatch.setenv("IMPORTACAO_TOKEN", valor)

    def proibido(*args, **kwargs):
        pytest.fail("não deveria acessar rede")

    monkeypatch.setattr(sincronizar, "run", proibido)
    monkeypatch.setattr(requests.Session, "post", proibido)
    with pytest.raises(ValueError, match="IMPORTACAO_TOKEN"):
        sincronizar.sincronizar("http://api.test")
    with pytest.raises(ValueError, match="IMPORTACAO_TOKEN"):
        enviar_ao_backend(ResultadoExtracao("Gama", "https://exemplo.test/menu.pdf", []))


def test_ciclo_imediato_repete_em_seis_horas_apos_falha(monkeypatch, capsys):
    eventos = []
    tempos = iter([100, 110, 21700, 21705])
    monkeypatch.setattr(sincronizar, "monotonic", lambda: next(tempos))

    def ciclo(url, token):
        eventos.append("ciclo")
        if eventos.count("ciclo") == 1:
            raise requests.ConnectionError("segredo-teste")
        return {"Gama": "importado (2 itens)"}

    def esperar(segundos):
        eventos.append(segundos)
        if eventos.count("ciclo") == 2:
            raise KeyboardInterrupt

    monkeypatch.setattr(sincronizar, "sincronizar", ciclo)
    monkeypatch.setattr(sincronizar, "sleep", esperar)
    assert sincronizar.INTERVALO_PADRAO_SEGUNDOS == 21600
    with pytest.raises(KeyboardInterrupt):
        sincronizar.executar("http://api.test", 21600)
    assert eventos == ["ciclo", 21590, "ciclo", 21595]
    logs = capsys.readouterr().out
    assert "campus=todos falha no ciclo (ConnectionError)" in logs
    assert "campus=Gama importado" in logs
    assert "+00:00" in logs
    assert "segredo-teste" not in logs


def test_execucao_unica_nao_aguarda(monkeypatch):
    monkeypatch.setattr(sincronizar, "sincronizar", lambda *args: {})
    monkeypatch.setattr(sincronizar, "sleep", lambda *_: pytest.fail("não deve aguardar"))
    assert sincronizar.executar("http://api.test", 0)


def test_execucao_unica_retorna_falha_para_automacao(monkeypatch):
    monkeypatch.setattr(
        sincronizar,
        "sincronizar",
        lambda *args: {"Gama": "falha na importação (ConnectionError)"},
    )
    assert not sincronizar.executar("http://api.test", 0)


def test_ciclo_que_excede_intervalo_reinicia_sem_sobreposicao(monkeypatch):
    eventos = []
    tempos = iter([100, 21701, 21701, 21702])
    monkeypatch.setattr(sincronizar, "monotonic", lambda: next(tempos))
    monkeypatch.setattr(
        sincronizar,
        "sincronizar",
        lambda *args: eventos.append("ciclo") or {"Gama": "importado (1 itens)"},
    )

    def esperar(segundos):
        eventos.append(segundos)
        if eventos.count("ciclo") == 2:
            raise KeyboardInterrupt

    monkeypatch.setattr(sincronizar, "sleep", esperar)
    with pytest.raises(KeyboardInterrupt):
        sincronizar.executar("http://api.test", 21600)
    assert eventos == ["ciclo", 0, "ciclo", 21599]
