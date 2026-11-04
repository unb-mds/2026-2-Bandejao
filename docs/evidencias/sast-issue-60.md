# Evidência de ativação do SAST — issue 60

**Data da verificação:** 15/10/2026

**Requisito:** RNF05 / D07d

**Repositório:** `unb-mds/2026-2-Bandejao`

## Execução em Pull Request

O workflow foi confirmado em um Pull Request real na [execução 38827385419](https://github.com/unb-mds/2026-2-Bandejao/actions/runs/38827385419), disparada pelo PR [#63](https://github.com/unb-mds/2026-2-Bandejao/pull/63).

| Job | Resultado | Evidência |
|---|---|---|
| SAST Python (Bandit) | Aprovado | [Job 116737910897](https://github.com/unb-mds/2026-2-Bandejao/actions/runs/38827385419/job/116737910897) |
| SAST JavaScript (CodeQL) | Aprovado | [Job 116737911224](https://github.com/unb-mds/2026-2-Bandejao/actions/runs/38827385419/job/116737911224) |

O commit da branch era `645d6c6078304566e7f374ff474544d1f2ebc34e`. Como o evento era `pull_request`, os artefatos registraram o commit de merge de teste `c6bf33f8d583b7d89f903daaaaa7eb2ca73c117f` usado pelo GitHub Actions.

Os artefatos foram baixados e inspecionados:

- `bandit-c6bf33f8d583b7d89f903daaaaa7eb2ca73c117f`: relatório JSON válido, sem erros de análise, 148 achados baixos e nenhum achado alto;
- `codeql-c6bf33f8d583b7d89f903daaaaa7eb2ca73c117f`: SARIF válido, uma execução e nenhum achado.

Não houve achado alto ou crítico que exigisse correção ou justificativa. Os achados baixos do Bandit permanecem no relatório conforme a política e não bloqueiam RNF05.

## Proteção da `main`

O ruleset [SAST obrigatório na main](https://github.com/unb-mds/2026-2-Bandejao/rules/25208102) foi ativado no repositório com esta configuração:

| Campo | Valor verificado |
|---|---|
| Estado | `active` |
| Branch alvo | `main` |
| Checks obrigatórios | `SAST Python (Bandit)` e `SAST JavaScript (CodeQL)` |
| Branch atualizada antes do merge | obrigatório |
| Bypass | nenhum ator; `current_user_can_bypass: never` |

A página pública do ruleset apresenta a configuração visual usada como captura de verificação. A resposta da API do GitHub também confirmou `strict_required_status_checks_policy: true`, `bypass_actors: []` e os dois contextos obrigatórios.

De acordo com a [documentação do GitHub sobre checks obrigatórios](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#require-status-checks-to-pass-before-merging), uma atualização da branch protegida só é permitida quando todos os contextos exigidos estão aprovados. Portanto, um PR cujo Bandit ou CodeQL falhe fica impedido de entrar na `main`.

## Reprodução da verificação

```powershell
gh run view 38827385419 --repo unb-mds/2026-2-Bandejao
gh run download 38827385419 --repo unb-mds/2026-2-Bandejao
gh api repos/unb-mds/2026-2-Bandejao/rulesets/25208102
```
