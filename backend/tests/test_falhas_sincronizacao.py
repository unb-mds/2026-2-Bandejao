"""Issue #97: falhas na sincronização não podem apagar nem duplicar dados.

Os testes rodam a sincronização de verdade (pasta extracao) e mandam os dados
para a API de teste. A página do RU e os PDFs vêm dos arquivos salvos em
extracao/tests/fixtures/publicacao-2026-10-27.
"""

from datetime import UTC, date, datetime
from pathlib import Path
from uuid import uuid4

import pytest
import requests
from pydantic import SecretStr

from app.core.config import settings
from app.models import Avaliacao, Campus, Cardapio, ItemCardapio, Reclamacao
from app.models.enums import CategoriaReclamacao, TipoRefeicao

RAIZ = Path(__file__).resolve().parents[2]
PASTA = RAIZ / "extracao/tests/fixtures/publicacao-2026-10-27"
TOKEN = "token-de-teste"


@pytest.fixture()
def sincronizacao(client, monkeypatch):
    """Faz a sincronização usar a página e os PDFs salvos e a API de teste."""
    monkeypatch.syspath_prepend(str(RAIZ / "extracao"))
    from extracao import main, sincronizar

    monkeypatch.setattr(settings, "importacao_token", SecretStr(TOKEN))

    class PaginaDoRu:
        text = (PASTA / "links.html").read_text(encoding="utf-8")

        def raise_for_status(self):
            pass

    def baixar_pdf_salvo(url):
        return (PASTA / url.split("/")[-1]).read_bytes()

    def enviar_para_api_de_teste(resultado, url, token):
        return main.enviar_ao_backend(resultado, "http://testserver", client, token=token)

    rodar_extracao = main.run
    monkeypatch.setattr(main.requests, "get", lambda *args, **kwargs: PaginaDoRu())
    monkeypatch.setattr(main, "baixar_pdf", baixar_pdf_salvo)
    monkeypatch.setattr(sincronizar, "run", lambda: rodar_extracao(date(2026, 10, 27)))
    monkeypatch.setattr(sincronizar, "enviar_ao_backend", enviar_para_api_de_teste)
    return main, sincronizar


def test_pdf_corrompido_em_um_campus_mantem_o_cardapio_anterior(
    db_session, sincronizacao, monkeypatch,
):
    main, sincronizar = sincronizacao

    # O Gama já tinha um cardápio importado antes.
    gama = Campus(nome="Gama", ultima_importacao_em=datetime(2026, 10, 20, 12, 0, tzinfo=UTC))
    db_session.add(gama)
    db_session.commit()
    cardapio = Cardapio(campus_id=gama.id, data=date(2026, 10, 26), tipo_refeicao=TipoRefeicao.ALMOCO)
    db_session.add(cardapio)
    db_session.commit()
    db_session.add(ItemCardapio(
        cardapio_id=cardapio.id, categoria="prato_principal", tipo_dieta="padrao", nome="Prato antigo",
    ))
    db_session.commit()

    # O PDF do Gama vem corrompido; os outros vêm normais.
    pdf_corrompido = (PASTA / "invalido.pdf").read_bytes()

    def baixar(url):
        if "Gama" in url:
            return pdf_corrompido
        return (PASTA / url.split("/")[-1]).read_bytes()

    monkeypatch.setattr(main, "baixar_pdf", baixar)

    resumo = sincronizar.sincronizar("http://api", token=TOKEN)

    assert resumo["Gama"] == "falha na extração (ErroExtracao)"
    for campus in ["Darcy Ribeiro", "Ceilândia", "Planaltina", "Fazenda Água Limpa"]:
        assert resumo[campus].startswith("importado")

    # O Gama continua igual: mesmo cardápio, mesmo item e mesma data da última importação.
    db_session.expire_all()
    assert db_session.query(Cardapio).filter_by(campus_id=gama.id).count() == 1
    assert [item.nome for item in cardapio.itens] == ["Prato antigo"]
    assert gama.ultima_importacao_em.replace(tzinfo=None) == datetime(2026, 10, 20, 12, 0)


def test_pagina_do_ru_fora_do_ar_nao_apaga_nada(db_session, sincronizacao, monkeypatch, capsys):
    main, sincronizar = sincronizacao
    sincronizar.sincronizar("http://api", token=TOKEN)
    cardapios_antes = db_session.query(Cardapio).count()
    itens_antes = db_session.query(ItemCardapio).count()

    def site_fora_do_ar(*args, **kwargs):
        raise requests.ConnectionError("ru.unb.br não respondeu")

    monkeypatch.setattr(main.requests, "get", site_fora_do_ar)

    deu_certo = sincronizar.executar("http://api", intervalo=0, token=TOKEN)

    assert deu_certo is False
    assert "campus=todos falha no ciclo (ConnectionError)" in capsys.readouterr().out
    assert db_session.query(Cardapio).count() == cardapios_antes
    assert db_session.query(ItemCardapio).count() == itens_antes


def test_token_invalido_e_recusado_e_nada_e_gravado(db_session, sincronizacao, capsys):
    _, sincronizar = sincronizacao

    resumo = sincronizar.sincronizar("http://api", token="token-errado")

    assert len(resumo) == 5
    for status in resumo.values():
        assert status.startswith("falha na importação")
    assert db_session.query(Campus).count() == 0
    assert db_session.query(Cardapio).count() == 0
    # O token não pode aparecer no log.
    saida = capsys.readouterr()
    assert "token-errado" not in saida.out + saida.err


def test_mesma_publicacao_duas_vezes_nao_duplica_e_mantem_avaliacoes(db_session, sincronizacao):
    _, sincronizar = sincronizacao

    primeira = sincronizar.sincronizar("http://api", token=TOKEN)
    cardapios = db_session.query(Cardapio).count()
    itens = db_session.query(ItemCardapio).count()

    # Alguém avalia e reclama de uma refeição entre as duas sincronizações.
    cardapio = db_session.query(Cardapio).first()
    identidade = uuid4()
    db_session.add(Avaliacao(cardapio_id=cardapio.id, identidade=identidade, nota=4, comentario="Bom"))
    db_session.add(Reclamacao(
        cardapio_id=cardapio.id,
        identidade=identidade,
        categoria=CategoriaReclamacao.QUALIDADE,
        descricao="Comida fria",
        criado_em=datetime(2026, 10, 27, 13, 0, tzinfo=UTC),
    ))
    db_session.commit()

    segunda = sincronizar.sincronizar("http://api", token=TOKEN)

    assert segunda == primeira
    assert db_session.query(Campus).count() == 5
    assert db_session.query(Cardapio).count() == cardapios
    assert db_session.query(ItemCardapio).count() == itens
    assert db_session.query(Avaliacao).filter_by(cardapio_id=cardapio.id).count() == 1
    assert db_session.query(Reclamacao).filter_by(cardapio_id=cardapio.id).count() == 1
