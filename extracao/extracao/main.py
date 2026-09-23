"""Extração do cardápio semanal publicado pelo Restaurante Universitário da UnB.

Os links dos PDFs são descobertos a cada execução, pois a publicação do RU muda
semanalmente. A saída estruturada pode ser enviada explicitamente ao endpoint
interno do backend, sem acoplar a etapa padrão de extração à persistência.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from io import BytesIO
import re
import unicodedata
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import pdfplumber
from PIL import Image, ImageOps
import requests

URL_CARDAPIO = "https://ru.unb.br/cardapio-refeitorio/"
TIMEOUT_SEGUNDOS = 30

CAMPI = {
    "darcy-ribeiro": "Darcy Ribeiro",
    "ceilandia": "Ceilândia",
    "gama": "Gama",
    "planaltina": "Planaltina",
    "fazenda": "Fazenda Água Limpa",
}
TIPOS_REFEICAO = ("cafe_da_manha", "almoco", "jantar")
ALERGENOS_LEGENDA = (
    "cogumelo",
    "leite",
    "mel",
    "pimenta",
    "soja",
    "gluten",
    "amendoim",
    "oleaginosas",
    "ovo",
    "carne_suina",
)
LIMIAR_DISTANCIA_ICONE = 25
PADRAO_PERIODO = re.compile(
    r"semana-\d+-(?P<inicio_dia>\d{1,2})-(?P<inicio_mes>\d{1,2})-a-"
    r"(?P<fim_dia>\d{1,2})-(?P<fim_mes>\d{1,2})\.pdf$",
    re.IGNORECASE,
)
PADRAO_ANO = re.compile(r"/uploads/(?P<ano>\d{4})/")
PADRAO_DATA_TABELA = re.compile(r"\b(?P<dia>\d{1,2})/(?P<mes>\d{1,2})/(?P<ano>\d{4})\b")


class ErroExtracao(RuntimeError):
    """Indica que uma fonte externa não pôde ser lida no formato esperado."""


@dataclass(frozen=True)
class PdfCardapio:
    campus: str
    url: str
    inicio: date
    fim: date


@dataclass(frozen=True)
class ItemExtraido:
    categoria: str
    tipo_dieta: str
    nome: str
    alergenos: frozenset[str] = frozenset()


@dataclass
class RefeicaoExtraida:
    data: date
    tipo_refeicao: str
    itens: list[ItemExtraido] = field(default_factory=list)


@dataclass
class ResultadoExtracao:
    campus: str
    fonte_pdf_url: str
    refeicoes: list[RefeicaoExtraida]
    avisos: list[str] = field(default_factory=list)


def _normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(caractere for caractere in texto if not unicodedata.combining(caractere))
    return re.sub(r"\s+", " ", texto).strip().lower()


def _periodo_do_link(url: str) -> tuple[date, date] | None:
    nome = url.rsplit("/", maxsplit=1)[-1]
    periodo = PADRAO_PERIODO.search(nome)
    ano = PADRAO_ANO.search(url)
    if periodo is None or ano is None:
        return None

    ano_numero = int(ano["ano"])
    try:
        inicio = date(ano_numero, int(periodo["inicio_mes"]), int(periodo["inicio_dia"]))
        fim = date(ano_numero, int(periodo["fim_mes"]), int(periodo["fim_dia"]))
    except ValueError:
        return None
    return inicio, fim


def descobrir_pdfs(html: str, hoje: date | None = None) -> dict[str, PdfCardapio]:
    """Encontra o PDF da semana corrente (ou o próximo) para cada campus."""
    hoje = hoje or date.today()
    soup = BeautifulSoup(html, "html.parser")
    candidatos: dict[str, list[PdfCardapio]] = {campus: [] for campus in CAMPI.values()}

    for link in soup.select("a[href]"):
        url = urljoin(URL_CARDAPIO, link["href"])
        periodo = _periodo_do_link(url)
        if periodo is None:
            continue

        nome_normalizado = _normalizar(url.rsplit("/", maxsplit=1)[-1])
        campus = next(
            (nome for slug, nome in CAMPI.items() if slug in nome_normalizado),
            None,
        )
        if campus is not None:
            candidatos[campus].append(PdfCardapio(campus, url, *periodo))

    encontrados: dict[str, PdfCardapio] = {}
    for campus, opcoes in candidatos.items():
        if not opcoes:
            continue
        atual = [opcao for opcao in opcoes if opcao.inicio <= hoje <= opcao.fim]
        futuras = [opcao for opcao in opcoes if opcao.inicio > hoje]
        if atual or futuras:
            selecionado = min(atual or futuras, key=lambda opcao: opcao.inicio)
        else:
            selecionado = max(opcoes, key=lambda opcao: opcao.inicio)
        encontrados[campus] = selecionado

    return encontrados


def baixar_pdf(url: str, sessao: requests.Session | None = None) -> bytes:
    """Baixa um PDF e falha explicitamente quando a fonte não responde corretamente."""
    cliente = sessao or requests.Session()
    resposta = cliente.get(url, timeout=TIMEOUT_SEGUNDOS)
    resposta.raise_for_status()
    if not resposta.content.startswith(b"%PDF"):
        raise ErroExtracao(f"O endereço não retornou um PDF válido: {url}")
    return resposta.content


def _imagem_do_stream(stream: object) -> Image.Image:
    atributos = stream.attrs
    return Image.frombytes("RGB", (atributos["Width"], atributos["Height"]), stream.get_data())


def _assinatura_visual(imagem: Image.Image) -> list[bool]:
    cinza = ImageOps.grayscale(imagem).resize((16, 16), Image.Resampling.LANCZOS)
    pixels = list(cinza.get_flattened_data())
    media = sum(pixels) / len(pixels)
    return [pixel >= media for pixel in pixels]


def _distancia_assinaturas(esquerda: list[bool], direita: list[bool]) -> int:
    return sum(valor_esquerda != valor_direita for valor_esquerda, valor_direita in zip(esquerda, direita))


def _alergenos_por_celula(pagina: object, tabela: object) -> dict[tuple[int, int], frozenset[str]]:
    """Associa os ícones de alérgeno às células usando a legenda do próprio PDF."""
    imagens = pagina.images
    referencias = sorted(
        (
            imagem
            for imagem in imagens
            if imagem["top"] > pagina.height * 0.8 and imagem["width"] > 20
        ),
        key=lambda imagem: imagem["x0"],
    )
    if len(referencias) != len(ALERGENOS_LEGENDA):
        return {}

    assinaturas = [
        (alergeno, _assinatura_visual(_imagem_do_stream(imagem["stream"])))
        for alergeno, imagem in zip(ALERGENOS_LEGENDA, referencias)
    ]
    encontrados: dict[tuple[int, int], set[str]] = {}
    for imagem in imagens:
        if imagem["top"] > pagina.height * 0.8 or imagem["width"] > 20:
            continue
        assinatura = _assinatura_visual(_imagem_do_stream(imagem["stream"]))
        distancia, alergeno = min(
            (_distancia_assinaturas(assinatura, referencia), nome)
            for nome, referencia in assinaturas
        )
        if distancia > LIMIAR_DISTANCIA_ICONE:
            continue
        centro_x = (imagem["x0"] + imagem["x1"]) / 2
        centro_y = (imagem["top"] + imagem["bottom"]) / 2
        for indice_linha, linha in enumerate(tabela.rows):
            for indice_coluna, limites in enumerate(linha.cells):
                if limites and limites[0] <= centro_x <= limites[2] and limites[1] <= centro_y <= limites[3]:
                    encontrados.setdefault((indice_linha, indice_coluna), set()).add(alergeno)
                    break
    return {celula: frozenset(alergenos) for celula, alergenos in encontrados.items()}


def _extrair_tabelas_com_alergenos(
    pdf: bytes,
) -> list[tuple[list[list[str | None]], dict[tuple[int, int], frozenset[str]]]]:
    tabelas = []
    with pdfplumber.open(BytesIO(pdf)) as documento:
        for pagina in documento.pages:
            encontradas = pagina.find_tables()
            if encontradas:
                tabela = max(encontradas, key=lambda encontrada: len(encontrada.rows))
                tabelas.append((tabela.extract(), _alergenos_por_celula(pagina, tabela)))
    if not tabelas:
        raise ErroExtracao("Nenhuma tabela foi encontrada no PDF.")
    return tabelas


def extrair_tabelas(pdf: bytes) -> list[list[list[str | None]]]:
    """Extrai a maior tabela de cada página do PDF do RU."""
    return [tabela for tabela, _ in _extrair_tabelas_com_alergenos(pdf)]


def _categoria_e_dieta(rotulo: str) -> tuple[str, str] | None:
    texto = _normalizar(rotulo).replace("�", "")
    categoria = next(
        (
            valor
            for prefixo, valor in (
                ("salada 1", "salada_1"),
                ("salada 2", "salada_2"),
                ("molho", "molho_salada"),
                ("prato principal", "prato_principal"),
                ("guarni", "guarnicao"),
                ("acompanh", "acompanhamento"),
                ("sobremesa", "sobremesa"),
                ("bebida", "bebida"),
                ("panifica", "panificacao"),
                ("opcao extra", "opcao_extra"),
                ("gordura", "gordura"),
                ("complemento", "acompanhamento"),
                ("sopa", "sopa"),
                ("torrada", "torrada"),
                ("fruta", "fruta"),
            )
            if prefixo in texto
        ),
        None,
    )
    if categoria is None:
        return None

    if "ovolacto" in texto:
        dieta = "ovolactovegetariano"
    elif "vegetariano" in texto and "estrito" in texto:
        dieta = "vegetariano_estrito"
    elif "padrao" in texto:
        dieta = "padrao"
    else:
        dieta = "comum"
    return categoria, dieta


def _colunas_com_datas(tabela: list[list[str | None]]) -> dict[int, date]:
    colunas: dict[int, date] = {}
    for linha in tabela:
        for indice, celula in enumerate(linha):
            if not celula:
                continue
            encontrada = PADRAO_DATA_TABELA.search(celula)
            if encontrada:
                colunas[indice] = datetime.strptime(encontrada.group(), "%d/%m/%Y").date()
    return colunas


def estruturar_tabela(
    tabela: list[list[str | None]],
    tipo_refeicao: str,
    alergenos_por_celula: dict[tuple[int, int], frozenset[str]] | None = None,
) -> tuple[list[RefeicaoExtraida], list[str]]:
    """Transforma uma tabela semanal em refeições por data, preservando avisos de qualidade."""
    colunas = _colunas_com_datas(tabela)
    if not colunas:
        raise ErroExtracao("A tabela não contém datas reconhecíveis.")

    refeicoes = {data: RefeicaoExtraida(data, tipo_refeicao) for data in colunas.values()}
    avisos: list[str] = []
    primeira_coluna_data = min(colunas)

    alergenos_por_celula = alergenos_por_celula or {}
    for indice_linha, linha in enumerate(tabela):
        rotulos = [celula for celula in linha[:primeira_coluna_data] if celula]
        classificacao = _categoria_e_dieta(" ".join(rotulos))
        if classificacao is None:
            continue
        categoria, dieta = classificacao

        for coluna, data_cardapio in colunas.items():
            coluna_valor = coluna
            if coluna >= len(linha) or not linha[coluna]:
                # Almoço e jantar usam uma subcoluna à direita para o cabeçalho da data.
                coluna_valor = coluna - 1
            if coluna_valor < 0 or coluna_valor >= len(linha) or not linha[coluna_valor]:
                continue
            nome = re.sub(r"\s+", " ", linha[coluna_valor]).strip()
            if "�" in nome and "Caracteres ilegíveis encontrados no PDF; considere OCR." not in avisos:
                avisos.append("Caracteres ilegíveis encontrados no PDF; considere OCR.")
            alergenos = alergenos_por_celula.get((indice_linha, coluna_valor), frozenset())
            refeicoes[data_cardapio].itens.append(ItemExtraido(categoria, dieta, nome, alergenos))

    return list(refeicoes.values()), avisos


def extrair_cardapio(pdf: PdfCardapio, conteudo_pdf: bytes) -> ResultadoExtracao:
    """Lê as páginas de café, almoço e jantar de um PDF já descoberto."""
    refeicoes: list[RefeicaoExtraida] = []
    avisos: list[str] = []
    for indice, (tabela, alergenos_por_celula) in enumerate(_extrair_tabelas_com_alergenos(conteudo_pdf)):
        if indice >= len(TIPOS_REFEICAO):
            avisos.append(f"Página {indice + 1} ignorada: tipo de refeição desconhecido.")
            continue
        resultado_tabela, avisos_tabela = estruturar_tabela(
            tabela, TIPOS_REFEICAO[indice], alergenos_por_celula
        )
        refeicoes.extend(resultado_tabela)
        avisos.extend(aviso for aviso in avisos_tabela if aviso not in avisos)
    return ResultadoExtracao(pdf.campus, pdf.url, refeicoes, avisos)


def para_payload_importacao(resultado: ResultadoExtracao) -> dict[str, object]:
    """Converte a saída da extração no contrato aceito pelo endpoint interno do backend."""
    return {
        "campus": resultado.campus,
        "fonte_pdf_url": resultado.fonte_pdf_url,
        "refeicoes": [
            {
                "data": refeicao.data.isoformat(),
                "tipo_refeicao": refeicao.tipo_refeicao,
                "itens": [
                    {
                        "categoria": item.categoria,
                        "tipo_dieta": item.tipo_dieta,
                        "nome": item.nome,
                        "alergenos": sorted(item.alergenos),
                    }
                    for item in refeicao.itens
                ],
            }
            for refeicao in resultado.refeicoes
        ],
    }


def enviar_ao_backend(
    resultado: ResultadoExtracao,
    url_base: str = "http://localhost:8000",
    sessao: requests.Session | None = None,
) -> dict[str, object]:
    """Envia explicitamente um campus extraído; a execução padrão continua sem gravar dados."""
    cliente = sessao or requests.Session()
    resposta = cliente.post(
        f"{url_base.rstrip('/')}/cardapios/importacao",
        json=para_payload_importacao(resultado),
        timeout=TIMEOUT_SEGUNDOS,
    )
    resposta.raise_for_status()
    return resposta.json()


def run(hoje: date | None = None) -> dict[str, ResultadoExtracao | ErroExtracao]:
    """Extrai cada campus separadamente para uma falha não interromper os demais."""
    resposta = requests.get(URL_CARDAPIO, timeout=TIMEOUT_SEGUNDOS)
    resposta.raise_for_status()
    pdfs = descobrir_pdfs(resposta.text, hoje)
    resultados: dict[str, ResultadoExtracao | ErroExtracao] = {
        campus: ErroExtracao("Nenhum PDF semanal foi encontrado na página do RU.")
        for campus in CAMPI.values()
        if campus not in pdfs
    }
    for campus, pdf in pdfs.items():
        try:
            resultados[campus] = extrair_cardapio(pdf, baixar_pdf(pdf.url))
        except (requests.RequestException, ErroExtracao) as erro:
            resultados[campus] = ErroExtracao(str(erro))
    return resultados


if __name__ == "__main__":
    for campus, resultado in run().items():
        if isinstance(resultado, ErroExtracao):
            print(f"{campus}: falha - {resultado}")
        else:
            print(f"{campus}: {len(resultado.refeicoes)} refeições extraídas")
