---
name: extracao-cardapio
description: Use esta skill sempre que for implementar, corrigir ou expandir a extração do cardápio do RU (scraping da página, download do PDF, parsing dos dados). Aciona em pedidos como "implementar a extração do campus X", "o parsing do PDF quebrou", "adicionar novo campus na extração".
---

# Extração do Cardápio — Bandejão

## Contexto do projeto

O cardápio de cada campus da UnB é publicado em `https://ru.unb.br/cardapio-refeitorio/`, uma página HTML que lista todos os campi (Darcy Ribeiro, Ceilândia, Gama, Planaltina, Fazenda Água Limpa), cada um com um link para um PDF. **O link do PDF muda toda semana** — nunca fixar a URL do PDF diretamente no código.

## Fluxo esperado

1. Fazer requisição HTTP na página `ru.unb.br/cardapio-refeitorio/` (usar `requests`).
2. Usar `BeautifulSoup` para localizar, na página, o link do PDF correspondente ao campus desejado.
3. Baixar o PDF encontrado.
4. Usar `pdfplumber` para extrair o texto do PDF.
5. Estruturar o texto extraído em dados organizados: campus, dia da semana, tipo de refeição, itens, indicação de alérgenos (leite, ovos, glúten, cogumelo, mel, soja, pimenta, oleaginosas, carne suína, frutos do mar) e opção vegetariana/vegana.

## Convenções do projeto

- Código Python, na pasta `/extracao`.
- Cada campus deve ser tratável de forma independente — uma falha na extração de um campus não deve travar os demais.
- Sempre escrever um teste correspondente em `/extracao/tests/` para qualquer função nova.
- Não deixar credenciais, tokens ou URLs fixas de PDF hardcoded no código.

## Pontos de atenção

- O formato do PDF pode variar sutilmente entre campi ou de uma semana para outra — tratar exceções de parsing sem quebrar a extração inteira.
- Se o HTML da página mudar de estrutura, o seletor usado no `BeautifulSoup` pode parar de funcionar — sinalizar isso com um erro claro, não uma falha silenciosa.

