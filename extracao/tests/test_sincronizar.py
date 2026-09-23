from extracao import sincronizar
from extracao.main import ErroExtracao, ResultadoExtracao


def test_sincronizar_importa_campi_validos_e_isola_falhas(monkeypatch):
    resultado = ResultadoExtracao("Gama", "https://exemplo.test/gama.pdf", [])
    monkeypatch.setattr(
        sincronizar,
        "run",
        lambda: {"Gama": resultado, "Ceilândia": ErroExtracao("PDF indisponível")},
    )
    monkeypatch.setattr(
        sincronizar,
        "enviar_ao_backend",
        lambda recebido, url: {"itens_processados": 3}
        if recebido is resultado and url == "http://api.test"
        else None,
    )

    resumo = sincronizar.sincronizar("http://api.test")

    assert resumo == {
        "Gama": "importado (3 itens)",
        "Ceilândia": "falha na extração: PDF indisponível",
    }


def test_sincronizar_registra_falha_de_comunicacao_com_api(monkeypatch):
    resultado = ResultadoExtracao("Gama", "https://exemplo.test/gama.pdf", [])
    monkeypatch.setattr(sincronizar, "run", lambda: {"Gama": resultado})
    monkeypatch.setattr(
        sincronizar,
        "enviar_ao_backend",
        lambda *_: (_ for _ in ()).throw(ValueError("resposta inválida")),
    )

    assert sincronizar.sincronizar("http://api.test") == {
        "Gama": "falha na importação: resposta inválida"
    }
