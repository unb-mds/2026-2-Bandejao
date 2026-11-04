# Ata de reunião — Planejamento da Sprint 03 e decisões D01 a D08

**Data:** 12/10/2026
**Formato:** Videochamada

## Pauta

1. Decisões pendentes do Documento de Requisitos (D01 a D08).
2. Escopo e responsáveis da Sprint 03.

## Decisões

| ID | Decisão |
|---|---|
| D01 | Semana de segunda a domingo, fuso `America/Sao_Paulo`. Não presumir que todas as refeições existem todos os dias em todos os campi. |
| D02 | Filtro de dieta inclusivo (ovolactovegetariano inclui vegetariano estrito). Manter as marcações do RU e avisar na tela que "sem marcação" significa "não marcado na fonte". Revisar as marcações com PDFs reais. |
| D03 | Horários fixos por refeição em tabela de configuração. Sem o recurso de "suspenso" por administração; fica como limitação conhecida. |
| D04 | Sem cadastro nem login. Identidade anônima por navegador (código aleatório). Avaliação sem login, com uma avaliação por identidade por refeição. |
| D05 | Estimativa de intenções por refeição, sem horário de chegada. Amostra mínima de 10. Dados simulados na demonstração, identificados como tal. |
| D06 | Reclamações com 4 categorias, até 1.000 caracteres, sem foto, sem nome e sem lista pública. Leitura pela equipe por rota com token ou direto no banco. |
| D07 | Teste de carga com k6 (50 usuários), sincronização a cada 6 horas, 4 a 6 PDFs de referência, SAST com bandit e CodeQL bloqueando achados altos e críticos, e checagem de 5 em 5 minutos em janela curta de 1 a 2 horas. |
| D08 | A importação do cardápio passa a exigir token secreto. |

## Encaminhamentos

- A Sprint 03 trata apenas das decisões acima (ver `docs/scrum/sprint03.md`).
- Reclamações, janela de avaliação nas rotas, deploy, planejamento e estimativa ficam para as Sprints 04 a 06.



## Próxima reunião

Data: ____/____/2026. Pauta: andamento da Sprint 03 e bloqueio
