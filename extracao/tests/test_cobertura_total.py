from datetime import date
import runpy
import sys

import pytest
import requests

from extracao import main, sincronizar
from extracao.main import ErroExtracao, PdfCardapio, ResultadoExtracao


def test_periodo_e_descoberta_usam_ultima_semana_quando_nao_ha_publicacao_atual():
    assert main._periodo_do_link("https://exemplo.test/arquivo.pdf") is None
    assert main._periodo_do_link("https://exemplo.test/uploads/2026/Gama-Semana-01-31-2-a-2-3.pdf") is None

    html = '<a href="/uploads/2026/Gama-Semana-01-1-9-a-7-9.pdf">Gama</a>'
    encontrados = main.descobrir_pdfs(html, hoje=date(2026, 9, 22))

    assert encontrados["Gama"].fim == date(2026, 9, 7)


def test_helpers_visuais_comparam_stream_e_assinaturas():
    class Stream:
        attrs = {"Width": 2, "Height": 2}

        @staticmethod
        def get_data():
            return b"\x00\x00\x00" * 4

    imagem = main._imagem_do_stream(Stream())
    assinatura = main._assinatura_visual(imagem)

    assert imagem.size == (2, 2)
    assert len(assinatura) == 256
    assert main._distancia_assinaturas([True, False], [False, False]) == 1


def test_alergenos_por_celula_reconhece_icone_e_ignora_imagens_fora_da_tabela(monkeypatch):
    class Linha:
        cells = [(0, 0, 20, 20)]

    class Tabela:
        rows = [Linha()]

    class Pagina:
        height = 100
        images = []

    referencias = [
        {"top": 90, "width": 30, "x0": indice, "stream": [indice]}
        for indice in range(len(main.ALERGENOS_LEGENDA))
    ]
    Pagina.images = referencias + [
        {"top": 10, "width": 10, "x0": 5, "x1": 6, "bottom": 11, "stream": [0]},
        {"top": 10, "width": 30, "x0": 5, "x1": 6, "bottom": 11, "stream": [0]},
        {"top": 10, "width": 10, "x0": 50, "x1": 51, "bottom": 51, "stream": [99]},
    ]
    monkeypatch.setattr(main, "_imagem_do_stream", lambda stream: stream)
    monkeypatch.setattr(main, "_assinatura_visual", lambda imagem: imagem)
    monkeypatch.setattr(
        main,
        "_distancia_assinaturas",
        lambda esquerda, direita: 0 if esquerda == direita else 30,
    )

    assert main._alergenos_por_celula(Pagina(), Tabela()) == {(0, 0): frozenset({"cogumelo"})}


def test_alergenos_por_celula_retorna_vazio_sem_uma_legenda_completa():
    pagina = type("Pagina", (), {"height": 100, "images": []})()

    assert main._alergenos_por_celula(pagina, object()) == {}


def test_extrair_tabelas_escolhe_maior_tabela_e_falha_sem_tabelas(monkeypatch):
    class Tabela:
        def __init__(self, linhas):
            self.rows = [object()] * linhas

        def extract(self):
            return [[str(len(self.rows))]]

    class Pagina:
        def __init__(self, tabelas):
            self._tabelas = tabelas

        def find_tables(self):
            return self._tabelas

    class Documento:
        def __init__(self, paginas):
            self.pages = paginas

        def __enter__(self):
            return self

        def __exit__(self, *_):
            return None

    documentos = iter(
        [
            Documento([Pagina([Tabela(1), Tabela(2)])]),
            Documento([Pagina([])]),
        ]
    )
    monkeypatch.setattr(main.pdfplumber, "open", lambda _: next(documentos))
    monkeypatch.setattr(main, "_alergenos_por_celula", lambda *_: {"celula": frozenset()})

    assert main.extrair_tabelas(b"%PDF") == [[["2"]]]
    with pytest.raises(ErroExtracao, match="Nenhuma tabela"):
        main.extrair_tabelas(b"%PDF")


@pytest.mark.parametrize(
    ("rotulo", "esperado"),
    [
        ("SALADA 2 OVOLACTO", ("salada_2", "ovolactovegetariano")),
        ("MOLHO VEGETARIANO ESTRITO", ("molho_salada", "vegetariano_estrito")),
        ("BEBIDA PADRAO", ("bebida", "padrao")),
        ("FRUTA", ("fruta", "comum")),
        ("DESCONHECIDO", None),
    ],
)
def test_categoria_e_dieta_cobrem_classificacoes(rotulo, esperado):
    assert main._categoria_e_dieta(rotulo) == esperado


def test_estruturar_tabela_registra_caractere_ilegivel_e_ignora_celula_ausente():
    tabela = [
        ["COMPOSIÇÃO", "21/9/2026"],
        ["SOPA", "Caldo�"],
        ["SOBREMESA", None],
    ]

    refeicoes, avisos = main.estruturar_tabela(tabela, "jantar")

    assert [item.nome for item in refeicoes[0].itens] == ["Caldo�"]
    assert avisos == ["Caracteres ilegíveis encontrados no PDF; considere OCR."]


def test_extrair_cardapio_ignora_pagina_sem_tipo_e_remove_avisos_duplicados(monkeypatch):
    tabela = [["COMPOSIÇÃO", "21/9/2026"], ["SOPA", "Caldo�"]]
    pdf = PdfCardapio("Gama", "https://exemplo.test/gama.pdf", date(2026, 9, 21), date(2026, 9, 27))
    monkeypatch.setattr(
        main,
        "_extrair_tabelas_com_alergenos",
        lambda _: [(tabela, {}), (tabela, {}), (tabela, {}), (tabela, {})],
    )

    resultado = main.extrair_cardapio(pdf, b"%PDF")

    assert resultado.avisos == [
        "Caracteres ilegíveis encontrados no PDF; considere OCR.",
        "Página 4 ignorada: tipo de refeição desconhecido.",
    ]


def test_baixar_e_enviar_usam_sessao_padrao_e_run_isola_falha(monkeypatch):
    class RespostaPdf:
        content = b"%PDF-teste"
        text = ""

        @staticmethod
        def raise_for_status():
            return None

    class RespostaApi:
        @staticmethod
        def raise_for_status():
            return None

        @staticmethod
        def json():
            return {"itens_processados": 0}

    class Sessao:
        def get(self, *_args, **_kwargs):
            return RespostaPdf()

        def post(self, *_args, **_kwargs):
            return RespostaApi()

    resultado = ResultadoExtracao("Gama", "https://exemplo.test/gama.pdf", [])
    monkeypatch.setattr(main.requests, "Session", Sessao)
    assert main.baixar_pdf("https://exemplo.test/gama.pdf") == b"%PDF-teste"
    assert main.enviar_ao_backend(resultado) == {"itens_processados": 0}

    pdf = PdfCardapio("Gama", "https://exemplo.test/gama.pdf", date.today(), date.today())
    monkeypatch.setattr(main.requests, "get", lambda *_args, **_kwargs: RespostaPdf())
    monkeypatch.setattr(main, "descobrir_pdfs", lambda *_: {"Gama": pdf})
    monkeypatch.setattr(
        main,
        "baixar_pdf",
        lambda *_: (_ for _ in ()).throw(requests.RequestException("falha de rede")),
    )

    assert isinstance(main.run()["Gama"], ErroExtracao)


def test_modulo_main_executa_saida_de_linha_de_comando(monkeypatch, capsys):
    class Resposta:
        text = ""

        @staticmethod
        def raise_for_status():
            return None

    monkeypatch.setattr(main.requests, "get", lambda *_args, **_kwargs: Resposta())

    runpy.run_module("extracao.main", run_name="__main__")

    saida = capsys.readouterr().out
    assert "Darcy Ribeiro: falha" in saida
    assert "Fazenda Água Limpa: falha" in saida


def test_main_exibe_resumo_de_resultado(monkeypatch, capsys):
    resultado = ResultadoExtracao("Gama", "https://exemplo.test/gama.pdf", [])
    monkeypatch.setattr(main, "run", lambda: {"Gama": resultado})

    main.main()

    assert "Gama: 0 refeições extraídas" in capsys.readouterr().out


def test_comando_sincronizar_cobre_execucao_unica_negativa_e_continua(monkeypatch, capsys):
    monkeypatch.setattr(sincronizar, "sincronizar", lambda _: {"Gama": "importado (1 itens)"})
    monkeypatch.setattr(sys, "argv", ["sincronizar"])
    sincronizar.main()
    assert "Gama: importado" in capsys.readouterr().out

    monkeypatch.setattr(sys, "argv", ["sincronizar", "--intervalo-segundos", "-1"])
    with pytest.raises(SystemExit):
        sincronizar.main()

    monkeypatch.setattr(sys, "argv", ["sincronizar", "--intervalo-segundos", "1"])
    monkeypatch.setattr(sincronizar, "sleep", lambda _: (_ for _ in ()).throw(KeyboardInterrupt))
    with pytest.raises(KeyboardInterrupt):
        sincronizar.main()


def test_modulo_sincronizar_executa_comando(monkeypatch, capsys):
    resultado = ResultadoExtracao("Gama", "https://exemplo.test/gama.pdf", [])
    monkeypatch.setattr(main, "run", lambda: {"Gama": resultado})
    monkeypatch.setattr(main, "enviar_ao_backend", lambda *_: {"itens_processados": 0})
    monkeypatch.setattr(sys, "argv", ["sincronizar"])

    runpy.run_module("extracao.sincronizar", run_name="__main__")

    assert "Gama: importado (0 itens)" in capsys.readouterr().out
