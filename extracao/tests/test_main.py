from datetime import date

import pytest

from extracao import main
from extracao.main import ErroExtracao, PdfCardapio, descobrir_pdfs, estruturar_tabela


HTML_CARDAPIOS = """
<a href="/wp-content/uploads/2026/09/Gama-Semana-04-14-9-a-20-9.pdf">Gama anterior</a>
<a href="/wp-content/uploads/2026/09/Gama-Semana-01-21-9-a-27-9.pdf">Gama atual</a>
<a href="/wp-content/uploads/2026/09/Ceilandia-Semana-01-21-9-a-27-9.pdf">Ceilândia</a>
<a href="/documentos/outro.pdf">Ignorar</a>
"""


def test_descobrir_pdfs_seleciona_semana_atual_por_campus():
    encontrados = descobrir_pdfs(HTML_CARDAPIOS, hoje=date(2026, 9, 22))

    assert encontrados["Gama"].url.endswith("Gama-Semana-01-21-9-a-27-9.pdf")
    assert encontrados["Gama"].inicio == date(2026, 9, 21)
    assert encontrados["Ceilândia"].fim == date(2026, 9, 27)


def test_estruturar_tabela_cria_itens_por_data_e_tipo_de_dieta():
    tabela = [
        ["COMPOSIÇÃO", "2ª FEIRA\n21/9/2026", "3ª FEIRA\n22/9/2026"],
        ["PRATO PRINCIPAL\nPADRÃO", "Frango grelhado", "Carne assada"],
        ["PRATO PRINCIPAL\nVEGETARIANO\nESTRITO", "Grão-de-bico", "Lentilha"],
        ["SOBREMESA", "Banana", "Maçã"],
    ]

    refeicoes, avisos = estruturar_tabela(tabela, "almoco")

    assert avisos == []
    assert [refeicao.data for refeicao in refeicoes] == [date(2026, 9, 21), date(2026, 9, 22)]
    assert refeicoes[0].tipo_refeicao == "almoco"
    assert [(item.categoria, item.tipo_dieta, item.nome) for item in refeicoes[0].itens] == [
        ("prato_principal", "padrao", "Frango grelhado"),
        ("prato_principal", "vegetariano_estrito", "Grão-de-bico"),
        ("sobremesa", "comum", "Banana"),
    ]


def test_estruturar_tabela_lida_com_rotulo_corrompido_do_pdf_atual():
    tabela = [
        ["COMPOSIÇÃO", "21/9/2026"],
        ["GUARNI��O", "Purê de batata"],
    ]

    refeicoes, avisos = estruturar_tabela(tabela, "almoco")

    assert refeicoes[0].itens[0].categoria == "guarnicao"
    assert avisos == []


def test_estruturar_tabela_rejeita_tabela_sem_datas():
    with pytest.raises(ErroExtracao, match="datas"):
        estruturar_tabela([["PRATO PRINCIPAL", "Frango"]], "almoco")


def test_extrair_cardapio_sinaliza_limitacao_dos_alergenos(monkeypatch):
    tabela = [["COMPOSIÇÃO", "21/9/2026"], ["SOBREMESA", "Banana"]]
    pdf = PdfCardapio("Gama", "https://exemplo.test/gama.pdf", date(2026, 9, 21), date(2026, 9, 27))
    monkeypatch.setattr(main, "extrair_tabelas", lambda _: [tabela])

    resultado = main.extrair_cardapio(pdf, b"%PDF")

    assert resultado.refeicoes[0].itens[0].nome == "Banana"
    assert "Marcadores de alérgenos" in resultado.avisos[0]


def test_run_registra_falha_para_campus_sem_pdf(monkeypatch):
    class Resposta:
        text = HTML_CARDAPIOS.split("Ceilandia")[0]

        def raise_for_status(self):
            return None

    monkeypatch.setattr(main.requests, "get", lambda *_, **__: Resposta())
    monkeypatch.setattr(main, "baixar_pdf", lambda _: b"%PDF")
    monkeypatch.setattr(
        main,
        "extrair_cardapio",
        lambda pdf, _: main.ResultadoExtracao(pdf.campus, pdf.url, []),
    )

    resultados = main.run(hoje=date(2026, 9, 22))

    assert isinstance(resultados["Gama"], main.ResultadoExtracao)
    assert isinstance(resultados["Ceilândia"], ErroExtracao)


def test_pdf_cardapio_eh_imutavel():
    pdf = PdfCardapio(
        "Gama", "https://exemplo.test/gama.pdf", date(2026, 9, 21), date(2026, 9, 27)
    )

    with pytest.raises(AttributeError):
        pdf.campus = "Ceilândia"
