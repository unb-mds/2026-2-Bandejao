# Auditoria das marcações de dieta e alérgenos - issue 81

## Escopo

Esta auditoria compara os PDFs oficiais do Restaurante Universitário com a saída
do extrator para **Darcy Ribeiro** e **Ceilândia**, na semana de **26/10 a
01/11/2026**. A conferência foi refeita em 16/11/2026 para atender a D02, RN03 e
RN04.

Os arquivos foram obtidos da página oficial do RU e permanecem versionados em
`extracao/tests/fixtures/publicacao-2026-10-27/`. A origem dos cinco campi está
registrada em `docs/evidencias/dados/sincronizacao-2026-10-27.json`.

| Campus | Arquivo | SHA-256 |
| --- | --- | --- |
| Darcy Ribeiro | `Darcy-Ribeiro-Semana-02-26-10-a-01-11-2.pdf` | `048080a945826cf7b64281b195d3a3a3b0f48db9d1e1a04229374b8f7211eb83` |
| Ceilândia | `Ceilandia-Semana-02-26-10-a-01-11-1.pdf` | `2f431622e3dd30904354a1e6527ee2c859a6b24ae6a7b057e50046cc911b87ec` |

## Método de conferência

As três páginas de cada PDF - café da manhã, almoço e jantar - foram renderizadas
e comparadas com o JSON produzido pelo extrator. A revisão considerou:

1. o campus, a data, a refeição e o nome do item;
2. o tipo de dieta indicado pela linha da tabela;
3. cada ícone exibido junto ao item e sua correspondência com a legenda do próprio PDF;
4. a saída antes e depois da correção.

Não foram inferidos alérgenos pelo nome ou pelos ingredientes do prato. Uma
marcação só foi aceita quando estava presente no PDF.

## Divergências encontradas e resultado

O problema afetava itens com dois ou três ícones agrupados. A tabela registra
uma amostra representativa dos casos conferidos; os JSONs de regressão guardam a
saída completa dos dois campi.

| Campus | Data / refeição | Item | Esperado no PDF | Antes da correção | Depois da correção |
| --- | --- | --- | --- | --- | --- |
| Darcy Ribeiro | 27/10, café | Ovos mexidos | Ovo; leite | Sem marcação | Ovo; leite |
| Darcy Ribeiro | 28/10, almoço | Lasanha à bolonhesa | Leite; suíno; trigo/glúten | Sem marcação | Leite; suíno; trigo/glúten |
| Darcy Ribeiro | 31/10, almoço | Empadão de legumes com ervilha gratinado | Ovo; leite; trigo/glúten | Apenas trigo/glúten | Ovo; leite; trigo/glúten |
| Darcy Ribeiro | 29/10, jantar | Strogonoff de carne | Trigo/glúten; leite; cogumelo | Apenas cogumelo | Trigo/glúten; leite; cogumelo |
| Ceilândia | 28/10, almoço | Lasanha à bolonhesa | Leite; suíno; trigo/glúten | Sem marcação | Leite; suíno; trigo/glúten |
| Ceilândia | 29/10, jantar | Macarrão ao molho branco com PTS | Leite; trigo/glúten; soja | Sem marcação | Leite; trigo/glúten; soja |
| Ceilândia | 30/10, almoço | Peixe ao molho bechamel gratinado | Trigo/glúten; leite | Sem marcação | Trigo/glúten; leite |

Também foram conferidas as marcações de dieta. A linha "prato principal
ovolactovegetariano" continua sendo extraída como `ovolactovegetariano`, e a
linha "prato principal vegetariano estrito" como `vegetariano_estrito`. Não foi
encontrada divergência de dieta nos dois PDFs auditados.

## Causa e correção

O PDF armazena um ícone isolado como uma imagem quase quadrada. Quando dois ou
três ícones aparecem lado a lado, eles são compactados em uma única imagem larga.
O extrator descartava imagens com largura superior a 20 pontos para evitar os
logotipos da página e, com isso, descartava também todos os grupos de alérgenos.

A correção aplicada:

- reconhece faixas com até quatro ícones pela proporção entre largura e altura;
- divide a faixa em imagens individuais;
- compara a cor saturada da borda com a legenda do próprio PDF;
- mantém a assinatura visual anterior como alternativa quando a cor não for suficiente;
- associa o conjunto completo à célula e elimina repetições.

Foram adicionados testes unitários para a separação de ícones agrupados e testes
de regressão com os PDFs reais de Darcy Ribeiro e Ceilândia. As saídas esperadas
dos cinco campi foram atualizadas porque a mesma correção recuperou marcações que
estavam ausentes nas demais referências da semana.

## Limitações conhecidas

- A auditoria manual cobre esta publicação e os dois campi exigidos pela issue;
  mudanças futuras no modelo dos PDFs ainda podem exigir nova calibração.
- O extrator preserva somente as marcações publicadas pelo RU. Ausência de ícone
  significa "não marcado na fonte", e não garante que o item seja livre do alérgeno.
- Esta publicação tem dez símbolos e não apresenta um símbolo separado para
  frutos do mar. O sistema não cria essa informação por inferência.
- Textos ilegíveis na camada do PDF continuam sendo sinalizados para possível
  revisão por OCR; essa limitação não altera os ícones conferidos nesta auditoria.
