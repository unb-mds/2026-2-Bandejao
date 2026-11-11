# Publicação oficial conferida em 27 de outubro de 2026

Cinco PDFs do Restaurante Universitário da UnB, período 26/10 a 01/11/2026, coletados da página https://ru.unb.br/cardapio-refeitorio/ para regressão offline. A origem e os hashes estão em docs/evidencias/dados/sincronizacao-2026-10-27.json. links.html preserva os cinco destinos observados, incluindo revisões numéricas.

Cada PDF tem um JSON de saída esperada, registrado após a correção JPEG. A regressão detecta mudança de datas, refeições, categorias, dietas, nomes e marcadores em relação a esta linha de base. O arquivo esperado não constitui homologação nutricional ou auditoria manual de todos os ingredientes. Alterações no extrator devem comparar a saída com o PDF antes de atualizar o esperado.

## Caso de falha — issue 82

O sexto arquivo, `invalido.pdf`, é uma fixture sintética intencionalmente truncada,
sem catálogo, páginas ou tabela xref. Não veio do RU. Seu JSON guarda a mensagem
esperada de `ErroExtracao`. O teste usa o parser real, sem rede. A integração em
`backend/tests/test_pdf_referencia.py` percorre descoberta, extração e sincronização
com esse conteúdo e comprova que a importação não é chamada e que o cardápio
anterior permanece igual. Os testes rodam no workflow `ci.yml` já existente.

## Revisão humana dos resultados

A comparação automática não substitui a revisão por uma pessoa exigida na #82.
Não há confirmação dessa revisão até o momento; o critério segue pendente.

| PDF / campus | Resultado esperado | Revisão por pessoa |
| --- | --- | --- |
| Ceilândia | JSON ao lado do PDF | Pendente |
| Darcy Ribeiro | JSON ao lado do PDF | Pendente |
| Fazenda Água Limpa | JSON ao lado do PDF | Pendente |
| Gama | JSON ao lado do PDF | Pendente |
| Planaltina | JSON ao lado do PDF | Pendente |
| `invalido.pdf` | Erro descrito no JSON | Pendente |

Para cada arquivo, abra o PDF e o JSON lado a lado e confira todas as datas,
refeições, nomes, categorias, dietas e ícones de alérgenos. Registre divergências
com página e célula, corrigindo o extrator quando necessário. Ao terminar,
substitua a pendência pelo nome do revisor, data e referência do commit revisado.
No arquivo inválido, confira a mensagem de falha e o teste de preservação.
Só marque a #82 como concluída após registrar essa revisão.

## Como adicionar ou substituir uma referência

1. Descubra a publicação pela página oficial do RU e guarde os links observados
   em `links.html`; mantenha o conjunto entre quatro e seis PDFs, com mais de um
   campus e pelo menos uma falha. Ao incluir outro, substitua um válido existente.
2. Salve o PDF sem alterar seus bytes e registre origem, período e hash SHA-256
   no documento de evidências correspondente. Não fixe a URL semanal no extrator.
3. Monte o JSON esperado no contrato de `para_payload_importacao` e revise cada
   valor diretamente no PDF. A saída do extrator pode ajudar como rascunho, mas
   não deve ser aprovada automaticamente como resultado esperado.
4. Salve o JSON como `<nome-do-pdf>.json`. Para a falha, use `{"erro": "mensagem"}`.
   Atualize a descoberta offline e os casos parametrizados se substituir campus
   ou período; adicione um caso explícito quando a falha esperada for diferente.
5. Registre a revisão humana na tabela acima e execute, da pasta `extracao`,
   `python -m pytest`. Execute também os testes do backend com as dependências
   de ambos os componentes instaladas para validar a preservação do banco.
6. Revise o diff antes de commitar. Não atualize os JSONs apenas para fazer a
   regressão passar; documente o motivo da mudança e a conferência no PDF.
