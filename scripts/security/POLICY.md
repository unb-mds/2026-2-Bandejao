# Política de SAST — RNF05

O workflow `SAST` executa em todo pull request, push na `main` e acionamento
manual, sem filtros por caminho. Isso evita checks obrigatórios pendentes em
PRs de documentação. Não depende da execução da CI funcional.

## Ferramentas, cobertura e bloqueio

| Ferramenta | Cobertura | Regras | Bloqueio |
|---|---|---|---|
| Bandit 1.9.4, Python 3.12 | Todos os `.py` rastreados pelo Git, incluindo testes e scripts | Regras padrão da versão fixada, sem filtros de confiança | Qualquer achado `HIGH` |
| CodeQL Action v4 fixada por SHA, bundle `linked` | JavaScript/TypeScript, incluindo JSX/TSX, descobertos pelo extrator | `security-extended` | `security-severity` >= 7.0 |

No CodeQL, alto corresponde a 7.0–8.9 e crítico a 9.0–10.0. O nível SARIF
`warning`/`error` **não** substitui a severidade de segurança da regra. No
Bandit não há categoria crítica: a maior categoria é `HIGH`, toda bloqueante.
Baixos/médios permanecem nos relatórios para triagem, sem bloquear RNF05.

`check_reports.py` inspeciona os resultados, independentemente de o scanner
ter terminado com sucesso. Arquivo ausente, JSON inválido, execução com erro,
severidade inválida ou regra de segurança sem severidade fazem o check falhar.
O wrapper do Bandit distingue saída 1 por achados de erro real e também verifica
erros de análise no JSON. Análise vazia não conta como aprovação.

Não há exclusões configuradas de código próprio. Bibliotecas instaladas e
arquivos gerados não rastreados ficam fora da entrada do Bandit; CodeQL aplica
suas exclusões padrão de bibliotecas/arquivos gerados. O gate não aceita
supressões silenciosas: Bandit usa `--ignore-nosec`; uma supressão no SARIF não
remove achados bloqueantes. Para falso positivo, registrar justificativa e
revisão de outro integrante em issue/PR antes de propor mudança explícita na
política ou regra. Não há mecanismo de exceção automático nesta entrega.

## Evidências e configuração remota

Artefatos `bandit-<commit>` e `codeql-<commit>` são preservados por 30 dias,
mesmo após falha, quando os relatórios chegaram a ser produzidos. Bandit inclui
inventário de arquivos e versão; o artefato CodeQL inclui inventário das fontes
JS/TS rastreadas e commit, enquanto SARIF inclui ferramenta, regras e locais dos
achados. O inventário representa entradas candidatas, não certifica cobertura
de cada linha pelo extrator. Logs identificam bundle CodeQL e ambiente. A equipe
deve guardar os relatórios da versão aceita na issue antes de sua expiração.

O workflow usa somente `contents: read`, sem upload para a aba Security:
o resultado SARIF é guardado como artefato e validado localmente. Não é necessário
`security-events: write`. A execução não depende da habilitação do upload de
code scanning; o uso do CodeQL continua sujeito à licença do GitHub (repositório
público ou plano/licença aplicável a repositório privado).

O ruleset [SAST obrigatório na main](https://github.com/unb-mds/2026-2-Bandejao/rules/25208102)
foi ativado em 15/10/2026, sem atores com bypass. Ele exige a atualização da
branch e a aprovação destes dois checks antes de atualizar a `main`:

- `SAST Python (Bandit)`
- `SAST JavaScript (CodeQL)`

A [evidência da issue 60](../../docs/evidencias/sast-issue-60.md) registra a
execução real, os artefatos e a configuração efetiva. As ações são fixadas por
SHA; atualização de versão, bundle ou regras deve passar por revisão. A execução
real do CodeQL acontece no GitHub Actions; os testes locais do gate não equivalem
à análise do frontend.

## Verificação local

```text
python -m pip install -r requirements-security.txt
python -m unittest discover -s scripts/security -p "test_*.py" -v
python scripts/security/run_bandit.py <diretorio-de-relatorios>
python scripts/security/check_reports.py sarif <arquivo.sarif>
```

O wrapper usa os arquivos já rastreados. Arquivos novos precisam estar incluídos
no Git para entrar nessa análise local; no checkout do PR eles já estarão.
Código de saída: 0 aprovado; 1 achados bloqueantes; 2 erro de scanner/relatório.
SAST não substitui testes de autorização, configuração segura ou avaliação
dinâmica do produto.

## Referências oficiais consultadas

- [Bandit CLI](https://bandit.readthedocs.io/en/latest/man/bandit.html)
- [CodeQL Action](https://github.com/github/codeql-action)
- [Entradas da análise CodeQL](https://github.com/github/codeql-action/blob/v4/analyze/action.yml)
- [Severidade dos alertas](https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning-alerts)
- [Formato SARIF](https://docs.github.com/en/code-security/reference/code-scanning/sarif-files/sarif-support)
