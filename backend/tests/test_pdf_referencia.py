"""#82: um PDF corrompido não chega à importação nem apaga o último cardápio."""

from datetime import date
from pathlib import Path

from tests.test_cardapio_api import criar_cardapio_de_teste


def test_sincronizacao_com_pdf_invalido_preserva_banco(
    db_session, client, monkeypatch,
):
    raiz = Path(__file__).resolve().parents[2]
    monkeypatch.syspath_prepend(str(raiz / "extracao"))
    from extracao import main, sincronizar

    cardapio = criar_cardapio_de_teste(db_session)
    antes = client.get(f"/cardapios/{cardapio.id}").json()
    conteudo = (
        raiz / "extracao/tests/fixtures/publicacao-2026-10-27/invalido.pdf"
    ).read_bytes()

    class Resposta:
        text = (
            '<a href="https://ru.unb.br/uploads/2026/'
            'Gama-Semana-02-26-10-a-01-11.pdf">Gama</a>'
        )

        def raise_for_status(self):
            pass

    def nao_importar(*args, **kwargs):
        raise AssertionError("PDF inválido não deve provocar escrita na API")

    monkeypatch.setenv("IMPORTACAO_TOKEN", "segredo-teste")
    monkeypatch.setattr(main.requests, "get", lambda *args, **kwargs: Resposta())
    monkeypatch.setattr(main, "baixar_pdf", lambda url: conteudo)
    executar_extracao = main.run
    monkeypatch.setattr(sincronizar, "run", lambda: executar_extracao(date(2026, 10, 27)))
    monkeypatch.setattr(sincronizar, "enviar_ao_backend", nao_importar)

    resumo = sincronizar.sincronizar("http://api.test")
    assert resumo["Gama"] == "falha na extração (ErroExtracao)"
    assert client.get(f"/cardapios/{cardapio.id}").json() == antes
