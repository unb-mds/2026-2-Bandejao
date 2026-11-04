from datetime import date
from io import BytesIO
import json
from pathlib import Path

import pytest
from PIL import Image

from extracao import main


@pytest.mark.parametrize("campus", list(main.CAMPI.values()))
def test_publicacao_oficial_versionada_mantem_resultado_esperado(campus):
    pasta = Path(__file__).parent / "fixtures" / "publicacao-2026-10-27"
    pdfs = main.descobrir_pdfs((pasta / "links.html").read_text(encoding="utf-8"), date(2026, 10, 27))
    assert len(pdfs) == 5
    pdf = pdfs[campus]
    nome = pdf.url.rsplit("/", 1)[-1]
    esperado = json.loads((pasta / f"{nome}.json").read_text(encoding="utf-8"))
    resultado = main.extrair_cardapio(pdf, (pasta / nome).read_bytes())
    assert main.para_payload_importacao(resultado) == esperado


@pytest.mark.parametrize("sufixo", ["", "-", "-1", "-2", "-12"])
def test_descoberta_aceita_revisoes_numericas_dos_cinco_campi(sufixo):
    html = "".join(
        f'<a href="/wp-content/uploads/2026/10/{slug}-Semana-02-26-10-a-01-11{sufixo}.pdf">'
        f"{nome}</a>"
        for slug, nome in main.CAMPI.items()
    )
    encontrados = main.descobrir_pdfs(html, hoje=date(2026, 10, 27))
    assert set(encontrados) == set(main.CAMPI.values())
    assert all(pdf.inicio == date(2026, 10, 26) for pdf in encontrados.values())
    assert all(pdf.fim == date(2026, 11, 1) for pdf in encontrados.values())


def test_decodifica_stream_jpeg_de_icone_em_vez_de_tratar_como_rgb_cru():
    buffer = BytesIO()
    Image.new("RGB", (32, 32), (20, 150, 70)).save(buffer, format="JPEG")

    class Stream:
        attrs = {"Width": 32, "Height": 32, "Filter": "DCTDecode"}

        def get_data(self):
            return buffer.getvalue()

    imagem = main._imagem_do_stream(Stream())
    assert imagem.mode == "RGB"
    assert imagem.size == (32, 32)
    pixel = imagem.getpixel((16, 16))
    assert all(abs(real - esperado) < 5 for real, esperado in zip(pixel, (20, 150, 70)))


def test_erro_inesperado_em_um_pdf_nao_interrompe_outros_campi(monkeypatch):
    class Resposta:
        text = "".join(
            f'<a href="/uploads/2026/{slug}-Semana-02-26-10-a-01-11.pdf">PDF</a>'
            for slug in main.CAMPI
        )

        def raise_for_status(self):
            pass

    processados = []

    def extrair(pdf, conteudo):
        processados.append(pdf.campus)
        if pdf.campus == "Darcy Ribeiro":
            raise ValueError("falha inesperada do decoder")
        return main.ResultadoExtracao(pdf.campus, pdf.url, [])

    monkeypatch.setattr(main.requests, "get", lambda *args, **kwargs: Resposta())
    monkeypatch.setattr(main, "baixar_pdf", lambda url: b"%PDF")
    monkeypatch.setattr(main, "extrair_cardapio", extrair)
    resultado = main.run(hoje=date(2026, 10, 27))
    assert set(processados) == set(main.CAMPI.values())
    assert isinstance(resultado["Darcy Ribeiro"], main.ErroExtracao)
    assert all(
        isinstance(valor, main.ResultadoExtracao)
        for campus, valor in resultado.items() if campus != "Darcy Ribeiro"
    )
