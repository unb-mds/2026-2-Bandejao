# Validação da extração dos PDFs oficiais

**Data do acesso:** 30/09/2026

**Página de origem:** [Cardápio dos RUs da UnB](https://ru.unb.br/cardapio-refeitorio/)

**Período publicado nos arquivos:** 28/09/2026 a 04/10/2026

Esta verificação exercitou o descobrimento dos links, o download e a leitura dos PDFs atualmente publicados. Não enviou dados ao backend. Os totais descrevem somente o conteúdo encontrado nos arquivos; datas ou refeições não publicadas não foram interpretadas como confirmação de que o RU não funciona.

## Arquivos e resultado

| Campus | PDF da fonte | Datas encontradas | Refeições extraídas por tipo | Itens extraídos |
|---|---|---|---|---:|
| Darcy Ribeiro | [PDF](https://ru.unb.br/wp-content/uploads/2026/09/Darcy-Ribeiro-Semana-02-28-09-a-04-10.pdf) | 28/09 a 04/10 | Café 7; almoço 7; jantar 7 | 191 |
| Ceilândia | [PDF](https://ru.unb.br/wp-content/uploads/2026/09/Ceilandia-Semana-02-28-09-a-04-10.pdf) | 28/09 a 03/10 | Café 6; almoço 6; jantar 5 | 154 |
| Gama | [PDF](https://ru.unb.br/wp-content/uploads/2026/09/Gama-Semana-02-28-09-a-04-10.pdf) | 28/09 a 02/10 | Café 5; almoço 5; jantar 5 | 138 |
| Planaltina | [PDF](https://ru.unb.br/wp-content/uploads/2026/09/Planaltina-Semana-02-28-09-a-04-10-.pdf) | 28/09 a 04/10 | Café 7; almoço 7; jantar 7 | 191 |
| Fazenda Água Limpa | [PDF](https://ru.unb.br/wp-content/uploads/2026/09/Fazenda-Semana-02-28-09-a-04-10.pdf) | 28/09 a 02/10 | Café 5; almoço 5; jantar não consta | 83 |

Foram extraídas 84 refeições e 757 itens. As categorias presentes foram bebida, panificação, opção extra, gordura, acompanhamento, fruta, salada 1, salada 2, molho de salada, prato principal, guarnição, sobremesa, sopa e torrada. Os nomes dos itens foram lidos das células das tabelas e preservados; a conferência visual de amostras incluiu, por exemplo, as opções de bebida e pão do café, a preparação de cenoura à bolonhesa de soja e salsicha ao molho.

As classificações extraídas totalizaram 505 itens comuns e 84 em cada uma das classes padrão, ovolactovegetariana e vegetariana estrita. A contagem dos marcadores visuais foi: leite 167, glúten 108, soja 60, ovo 44, carne suína 15, pimenta 11, amendoim 10, cogumelo 9, mel 8 e oleaginosas 4. Os totais não demonstram segurança alimentar nem validam a semântica de dieta proposta em D02.

## Divergências encontradas e limites

- O link atual de Planaltina termina em `04-10-.pdf`, com hífen adicional antes da extensão. O descobridor não aceitava esse nome e deixava o campus de fora. O padrão agora aceita o hífen opcional e há teste de regressão com o link publicado.
- Os PDFs atuais apresentam dez ícones na legenda visual, embora o código anterior esperasse onze; por isso os alérgenos não eram associados a nenhuma célula. O mapeamento agora aceita as dez posições atuais e mantém a configuração de onze posições para arquivos anteriores.
- A legenda visível desses arquivos nomeia “Suíno”, mas não traz um símbolo separado para frutos do mar. Nenhum marcador `frutos_do_mar` foi extraído. Isso significa informação não disponível nessa legenda, não ausência confirmada desse ingrediente ou risco.
- Os PDFs cobrem quantidades diferentes de datas/refeições. A extração preserva apenas as tabelas publicadas, sem completar os dias ausentes.
- O rótulo HTML publicado para Gama apresenta datas inconsistentes com o nome do arquivo e com as datas internas das tabelas. A seleção usa o período do link e as datas extraídas do PDF; não usa o rótulo de texto da página.
- Os totais são uma fotografia da publicação acessada em 30/09/2026. A validação não garante compatibilidade com PDFs futuros nem substitui conferência humana antes de usar os dados para decisões alimentares. Os arquivos podem mudar sem aviso.

## Reprodutibilidade

Os hashes abaixo identificam exatamente os arquivos baixados nesta execução. Os PDFs não foram copiados para o repositório; os links acima apontam para a fonte oficial.

| Campus | SHA-256 |
|---|---|
| Darcy Ribeiro | `70c3df72203791a7e7f09e2ab3e37d8d087d6b1ed5d61359820c668fe2184c4f` |
| Ceilândia | `08eda65af384beb05a4dcd05a150a84360df456cddaf118788def6e7c346853c` |
| Gama | `06a166bd13639910eef0ab8d297971523500cb1d1cf957c30a0daea6a2583434` |
| Planaltina | `7e6ed77fe6282f58b1738a0bf3207b10a320693e70dc5eb3809fe936990cd872` |
| Fazenda Água Limpa | `7825c27075e7844bb5dc95754b33ef27e4a5082b9b2f13c411fb07cb4397ed7b` |

## Validação automatizada

Os testes da extração cobrem a seleção do PDF de Planaltina com hífen adicional, o reconhecimento da legenda atual de dez ícones e a legenda anterior de onze ícones. A execução local em 30/09/2026 passou com 33 testes; a validação dos arquivos acima foi uma execução manual separada, dependente da disponibilidade da página e dos PDFs oficiais.
