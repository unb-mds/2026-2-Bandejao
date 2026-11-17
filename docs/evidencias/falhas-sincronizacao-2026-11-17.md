# Falhas simuladas na sincronização (issue #97)

**Requisitos:** RNF02, RNF03, CA-RNF03-02  
**Data:** 17/11/2026  
**Commit testado:** [`c9df0af`](https://github.com/unb-mds/2026-2-Bandejao/commit/c9df0af) (a partir da `main` `326569c`)  
**Teste:** `backend/tests/test_falhas_sincronizacao.py`  
**Ambiente:** Windows 10, Python 3.14.4, banco SQLite em memória. No CI, os testes do backend também rodam em PostgreSQL (#94).  
**Como rodar:** `cd backend && pytest tests/test_falhas_sincronizacao.py -v`

## Como o teste funciona

Cada teste roda a sincronização de verdade (`extracao/sincronizar.py`) e manda os dados para a API de teste, com um banco separado. A página do RU e os cinco PDFs são os arquivos oficiais salvos em `extracao/tests/fixtures/publicacao-2026-10-27/`. Só a falha de cada cenário é simulada.

## Resultados

| Cenário | O que foi feito | Esperado | Obtido | Resultado |
|---|---|---|---|---|
| 1. PDF corrompido em um campus | O PDF do Gama foi trocado por `invalido.pdf`. O Gama já tinha um cardápio antigo. | Os outros 4 campi são importados e o Gama fica como estava. | Gama com `falha na extração (ErroExtracao)`; os outros 4 com `importado`. O Gama manteve o cardápio, o item e a data da última importação. | Passou |
| 2. Página do RU fora do ar | Depois de uma sincronização normal, a página do RU passa a dar erro de conexão. | Nada é apagado e a falha aparece no log. | Log com `campus=todos falha no ciclo (ConnectionError)` e retorno de falha. Mesma quantidade de cardápios e itens antes e depois. | Passou |
| 3. Token inválido | A sincronização usa um token diferente do configurado na API. | A API recusa e nada é gravado. | Os 5 campi com `falha na importação`; nenhum campus ou cardápio no banco; o token não aparece no log. | Passou |
| 4. Mesma publicação duas vezes | Sincroniza, registra uma avaliação e uma reclamação, e sincroniza de novo. | Nada duplicado; avaliação e reclamação continuam lá. | Mesmo resultado nas duas vezes; mesma quantidade de campi (5), cardápios e itens; a avaliação e a reclamação continuam no mesmo cardápio. | Passou |

Execução: `4 passed`. Suíte completa do backend: `206 passed, 3 skipped`, cobertura de 100%.

## Limites

- A página do RU e o envio para a API são simulados dentro do teste. Não houve acesso ao site real do RU nem à API publicada, que estava respondendo HTTP 404 nessa data.
