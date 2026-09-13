# Extração de Dados de PDF — Estudo

## O que é

Extração de dados de PDF é o processo de ler um arquivo PDF e transformar seu conteúdo em dados estruturados que um sistema consegue processar (texto, tabelas, valores específicos), em vez de um documento pensado apenas para leitura humana. É um problema comum quando a única fonte de dados disponível é uma publicação em PDF, sem API — exatamente o caso do cardápio do RU/UnB.

O PDF não foi criado como formato de dados: ele descreve **onde** desenhar cada caractere na página (posição x/y, fonte, tamanho), não a estrutura lógica do conteúdo (o que é um título, uma tabela, uma célula). Por isso, "ler um PDF" é sempre, em algum grau, reconstruir estrutura a partir de posições de texto — e é isso que torna a extração sensível a qualquer mudança no layout do documento original.

## Dois tipos de PDF

### PDF com texto selecionável (PDF nativo/digital)
Gerado diretamente por um programa (Word, LaTeX, um sistema que exporta relatórios), o texto já existe como caracteres codificados dentro do arquivo — dá para selecionar e copiar o texto normalmente.

- Extração feita por **parsing**: bibliotecas leem a estrutura interna do PDF e recuperam o texto e sua posição na página.
- Mais confiável e muito mais rápido que OCR, porque não há necessidade de "adivinhar" o que está escrito.

### PDF escaneado/imagem
O conteúdo é, na prática, uma foto ou scan de um documento — o "texto" é só pixels, não existe camada de caracteres selecionáveis.

- Extração exige **OCR** (Optical Character Recognition): um modelo que reconhece formas de caracteres na imagem e as converte em texto.
- Mais lento, mais custoso computacionalmente e sujeito a erros de reconhecimento (uma letra confundida com outra, acentuação perdida), especialmente em imagens de baixa qualidade ou fontes incomuns.

O primeiro passo prático de qualquer extração de PDF é justamente checar qual dos dois casos se aplica — o cardápio do RU pode publicar em qualquer um dos formatos, ou até alternar entre eles, dependendo de como cada campus gera o arquivo.

## Parsing de PDF nativo

Bibliotecas de parsing (ex: `pdfplumber`, `PyMuPDF`/`fitz`, `pypdf` em Python) expõem o conteúdo do PDF em diferentes níveis:

- **Texto bruto** — todo o texto da página, geralmente na ordem em que os caracteres foram desenhados (nem sempre a ordem de leitura lógica, principalmente em layouts de múltiplas colunas).
- **Texto com posição (bounding box)** — cada palavra/linha vem acompanhada de coordenadas na página, o que permite reconstruir colunas, células de tabela ou blocos de texto.
- **Detecção de tabelas** — algumas bibliotecas (ex: `pdfplumber`, `camelot`, `tabula-py`) tentam identificar linhas/colunas de uma tabela a partir de bordas desenhadas ou do alinhamento do texto, e devolver algo próximo de uma planilha.

Cardápios como o do RU tendem a ser tabelas (dia da semana x tipo de refeição x prato), então a extração provavelmente depende mais da detecção de tabela ou do agrupamento de texto por posição do que de texto corrido.

## OCR (quando o PDF é imagem)

- **Tesseract OCR** é a engine open-source mais usada (via `pytesseract` em Python); suporta português, mas a qualidade depende diretamente da resolução e nitidez da imagem de origem.
- Fluxo típico: converter cada página do PDF em imagem (ex: com `pdf2image`) → pré-processar a imagem (ajustar contraste, remover ruído, endireitar se estiver torta) → rodar OCR → tratar o texto resultante (ele sai sem estrutura de tabela, geralmente precisa de heurísticas próprias para separar colunas).
- **Pré-processamento de imagem** costuma ser o que mais afeta a qualidade do resultado: mais importante, às vezes, que trocar de engine de OCR.
- OCR não garante 100% de acerto — projetos que dependem dele geralmente prevêem alguma validação humana ou heurísticas de sanidade (ex: um prato que não bate com nenhuma palavra conhecida é sinalizado para revisão).

## Da tabela ao dado estruturado

Depois de extrair texto/tabela do PDF, ainda falta transformar isso em algo que o sistema possa usar (essa etapa é, na prática, a parte de "transform" de um pipeline ETL — ver o estudo de [arquitetura de software](arquitetura_software.md)):

- **Parsing com regras/regex** — usar padrões de texto conhecidos do documento (ex: nome do prato seguido de um marcador de restrição alimentar entre parênteses) para separar os campos.
- **Normalização** — padronizar valores (ex: "Vegetariano", "vegetariano", "VEG" devem virar um único valor no sistema), remover espaços/quebras de linha indevidas, corrigir acentuação.
- **Validação** — checar se o resultado faz sentido antes de gravar no banco (ex: um dia da semana sem nenhum prato associado provavelmente indica falha de extração, não que o RU não serviu nada naquele dia).

## Por que esse processo é frágil

- O parsing (e ainda mais o OCR) depende diretamente do **layout visual** do documento — qualquer mudança de fonte, alinhamento, ordem das colunas ou template usado pelo RU pode quebrar as regras de extração, mesmo que o conteúdo em si (os pratos do cardápio) não tenha nada de anormal.
- Diferente de uma API, não há contrato/versionamento: o RU pode publicar um PDF em formato ligeiramente diferente sem aviso, e o sistema só descobre isso quando a extração falha ou produz dados incorretos.
- É por isso que esse componente deve ser isolado do resto do sistema (como já registrado no `CLAUDE.md` do projeto): um ajuste no parsing não deve exigir mudanças em backend, banco ou frontend.

## Boas práticas para tornar a extração mais robusta

- **Falhar de forma visível, não silenciosa** — se a extração não conseguir identificar um campo esperado (ex: nenhum prato para um campus), é melhor logar/alertar do que gravar dado incompleto ou incorreto sem avisar.
- **Isolar a lógica específica de cada campus/formato** — se cada campus do RU publica em um template ligeiramente diferente, vale a pena ter um parser dedicado por formato, em vez de uma função genérica cheia de casos especiais.
- **Guardar o PDF original processado** — manter o arquivo (ou pelo menos uma referência a ele) facilita depurar quando o resultado da extração parecer errado.
- **Testes com PDFs reais salvos** — como o RU pode trocar o link/formato a qualquer momento, ter cópias de PDFs já publicados como fixture de teste garante que mudanças no código de parsing não quebrem casos que já funcionavam.
- **Ambiente de execução consistente** — versões diferentes de bibliotecas de parsing/OCR podem produzir resultados ligeiramente diferentes para o mesmo arquivo; fixar versões (`requirements.txt`) evita esse tipo de inconsistência entre máquinas do time.

## Relação com o projeto Bandejão

- A camada `/extracao` do Bandejão depende de acessar `https://ru.unb.br/cardapio-refeitorio/`, identificar o link do PDF de cada campus (que muda toda semana) e então aplicar parsing (ou OCR, se o PDF publicado vier como imagem) para estruturar o cardápio.
- O RNF03 do documento de requisitos ("o processo de extração deve ser resiliente a pequenas variações no formato... e deve ser possível ajustá-lo rapidamente caso o formato mude") é, na prática, uma consequência direta da fragilidade inerente ao parsing de PDF descrita acima.
- A stack técnica já definida para essa camada (`requests` + `BeautifulSoup` para navegar a página HTML do RU, `pdfplumber` para extrair o conteúdo do PDF) cobre o caso de PDF nativo; se algum campus publicar o cardápio como imagem escaneada, será necessário adicionar OCR (ex: Tesseract) especificamente para esse caso.
- As restrições alimentares que o RU já sinaliza no cardápio (leite, ovos, glúten, cogumelo, mel, soja, pimenta, oleaginosas, carne suína, frutos do mar, opções vegetarianas) provavelmente aparecem como símbolos, siglas ou marcações entre parênteses no PDF — mapear esses marcadores corretamente durante o parsing é o que viabiliza os filtros alimentares (RF03) do sistema.

## Dúvidas em aberto

*(preencher assim que o grupo tiver acesso a um PDF real do RU para inspecionar: se é nativo ou escaneado, como as restrições alimentares são representadas visualmente, se o layout é consistente entre os diferentes campi)*

## Fontes

- [pdfplumber — documentação](https://github.com/jsvine/pdfplumber)
- [Tesseract OCR — documentação](https://tesseract-ocr.github.io/tessdoc/)
- [Extracting data from PDFs — Real Python](https://realpython.com/pdf-python/)
