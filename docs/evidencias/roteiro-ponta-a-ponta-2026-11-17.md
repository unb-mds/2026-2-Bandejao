# Registro de execução do roteiro ponta a ponta

**Data da tentativa:** 17/11/2026 (consulta às 03:14 UTC; tentativa anterior em 16/11/2026 com o mesmo resultado)  
**Commit esperado da aplicação:** [`326569c`](https://github.com/unb-mds/2026-2-Bandejao/commit/326569c) (`main` em 17/11/2026)  
**Aplicação integrada:** <https://bandejao-unb-g12.onrender.com>  
**API:** <https://bandejao-unb-g12-api.onrender.com>  
**Protótipo visual (referência separada):** <https://frontend-react-tan-gamma.vercel.app>  
**Ambiente:** consulta HTTPS somente leitura, em desktop; fluxos de interface não executados.  
**Roteiro:** [`testes/roteiros/roteiro-ponta-a-ponta.md`](https://github.com/unb-mds/2026-2-Bandejao/blob/main/testes/roteiros/roteiro-ponta-a-ponta.md)  
**Resultado geral:** bloqueado. A aplicação integrada e a API responderam HTTP 404, então os fluxos não puderam ser executados em aba anônima.

## Verificação de disponibilidade

| Alvo | 16/11/2026 | 17/11/2026 |
|---|---|---|
| Interface integrada `/` | HTTP 404 | HTTP 404 |
| API `/health` | HTTP 404 | HTTP 404 |
| API `/version` | HTTP 404 | HTTP 404 |
| Protótipo visual Vercel `/` | HTTP 200 | HTTP 200 |

O protótipo Vercel não consulta a API publicada e não substitui a aplicação integrada. Ele não foi usado como evidência dos fluxos.

## Fluxos

"Não executado" não significa aprovação nem reprovação funcional.

| Passo | Esperado | Obtido | Data | Commit esperado | Estado |
|---|---|---|---|---|---|
| 1. Cardápio semanal | Consultar refeições do campus e da semana escolhidos. | Não executado: a interface integrada retornou HTTP 404. | 17/11/2026 | `326569c` | Bloqueado |
| 2. Filtro por dieta | Exibir somente itens compatíveis com a dieta selecionada. | Não executado: interface indisponível. | 17/11/2026 | `326569c` | Bloqueado |
| 3. Filtro por alérgeno | Excluir itens com a marcação selecionada e exibir o aviso sobre marcações da fonte. | Não executado: interface indisponível. | 17/11/2026 | `326569c` | Bloqueado |
| 4. Avaliação | Registrar a nota permitida e confirmar o envio. | Não executado: interface indisponível. | 17/11/2026 | `326569c` | Bloqueado |
| 5. Histórico | Exibir a avaliação associada à refeição escolhida. | Não executado: interface indisponível. | 17/11/2026 | `326569c` | Bloqueado |
| 6. Reclamação | Confirmar o envio ou exibir o erro, sem lista pública. | Não executado: interface indisponível. | 17/11/2026 | `326569c` | Bloqueado |
| 7. Marcar e desmarcar intenção | Ativar e remover uma intenção futura. | Não executado: interface indisponível. | 17/11/2026 | `326569c` | Bloqueado |
| 8. Estimativa | Consultar o recorte solicitado e distinguir contagens reais e simuladas. | Não executado: interface indisponível. | 17/11/2026 | `326569c` | Bloqueado |

## Teste em celular

Em 16/11/2026, Arthur relatou ter testado a versão mobile e que estava funcionando. Não foram registrados aparelho, navegador, viewport, fluxos executados nem commit testado. Como a aplicação integrada estava indisponível, o relato pode se referir ao protótipo ou a uma execução local. Fica registrado como relato, sem verificação independente.

## Para concluir a verificação

1. Reativar a aplicação integrada e a API no Render. Se a publicação não for possível até o fim da sprint, executar o roteiro em ambiente local (Docker Compose) e registrar aqui que a execução foi local, com o commit testado.
2. Executar os 8 passos em uma janela anônima e preencher o resultado observado de cada um.
3. Repetir em um celular físico, registrando modelo, sistema, navegador e commit.
4. Abrir uma issue para cada falha encontrada e ligá-la à [#101](https://github.com/unb-mds/2026-2-Bandejao/issues/101).

Este documento comprova apenas as respostas HTTP registradas. Não comprova uso funcional da aplicação integrada, persistência nem navegação anônima.
