# OCR e Extração de Imagem — Estudo

## O que é OCR

OCR (Optical Character Recognition — Reconhecimento Óptico de Caracteres) é a tecnologia que converte texto presente em uma imagem (uma foto, um scan, um PDF sem camada de texto) em texto digital editável e pesquisável. Diferente da extração de um PDF nativo (onde o texto já existe como dado), o OCR precisa "ler" os pixels da imagem e reconhecer quais formam letras e números.

## Quando o OCR é necessário

- O PDF é uma imagem escaneada (o documento foi fotografado ou digitalizado, sem camada de texto real por trás).
- O conteúdo está em formato de imagem pura (JPG, PNG) e não em PDF.
- Uma biblioteca de extração de PDF (como `pdfplumber`) retorna texto vazio ou incompreensível — sinal de que o PDF não tem texto nativo, só a aparência visual de texto.

## Como funciona, em linhas gerais

1. **Pré-processamento da imagem**: ajustes como conversão para escala de cinza, aumento de contraste, remoção de ruído — melhoram a taxa de acerto do reconhecimento.
2. **Detecção de regiones de texto**: o motor de OCR identifica onde, na imagem, existem blocos de texto.
3. **Reconhecimento de caracteres**: cada caractere é comparado a padrões conhecidos (hoje em dia, isso é feito majoritariamente com modelos de machine learning treinados em grandes volumes de texto).
4. **Pós-processamento**: correção de erros comuns (ex: confundir "0" com "O"), montagem do texto final.

## Ferramentas comuns

- **Tesseract OCR** — motor de OCR de código aberto, mantido pelo Google. É a opção mais usada em projetos Python (via biblioteca `pytesseract`), gratuita e roda localmente.
- **EasyOCR** — biblioteca Python mais recente, baseada em deep learning, geralmente com boa acurácia e fácil de usar, mas mais pesada computacionalmente que o Tesseract.
- **APIs de OCR na nuvem** (ex: Google Cloud Vision, AWS Textract) — tendem a ter maior precisão, mas são pagas (geralmente com uma cota gratuita limitada) e exigem enviar a imagem para um serviço externo.

## Limitações e desafios do OCR

- Qualidade da imagem de entrada afeta diretamente a precisão — imagens borradas, de baixa resolução ou com fundo complexo geram mais erros.
- Layouts complexos (tabelas, colunas múltiplas) são mais difíceis de interpretar corretamente do que texto corrido.
- Fontes estilizadas ou manuscritas reduzem bastante a precisão comparado a fontes padrão.
- Requer, em geral, mais poder de processamento do que a extração direta de texto de um PDF nativo.

## Relevância para o projeto

Essa abordagem seria necessária apenas se algum campus da UnB publicar o cardápio como uma imagem escaneada em vez de um PDF com texto nativo. Vale, na prática, primeiro testar a extração direta (`pdfplumber`) nos PDFs reais de cada campus — o OCR entra como alternativa apenas nos casos em que a extração direta falhar.

## Dúvidas em aberto

*(preencher conforme surgirem dúvidas durante o uso prático)*
