# Backend — planejamento de refeições e estimativa de intenções

## Intenções de refeição — RF06

Cada intenção pertence a um cardápio existente e a uma identidade anônima. Todas
as rotas abaixo exigem `X-Identidade: <UUID v4>`. A identidade é persistida, mas
nunca aparece nas respostas. Não há campo de horário de chegada nem exigência
de corpo nas operações de marcação ou cancelamento.

| Método e rota | Comportamento | Resposta de sucesso |
| --- | --- | --- |
| `PUT /cardapios/{cardapio_id}/intencao/` | Marca ou reativa a intenção real | `200 {"cardapio_id": 1, "ativa": true}` |
| `GET /cardapios/{cardapio_id}/intencao/` | Consulta a intenção real da identidade | `200 {"cardapio_id": 1, "ativa": false}` quando ausente ou cancelada |
| `DELETE /cardapios/{cardapio_id}/intencao/` | Cancela a intenção real, preservando a linha | `200 {"cardapio_id": 1, "ativa": false}` |
| `GET /intencoes/` | Lista somente as intenções reais ativas da identidade no intervalo | `200` com a lista descrita abaixo |

As operações são idempotentes: repetir a marcação dentro do prazo não duplica a
linha; repetir o cancelamento mantém a intenção inativa. Cancelar uma intenção
ausente não cria registro. Uma marcação feita no início do serviço ou depois
dele recebe `422`, inclusive quando a intenção já estava ativa. O prazo RF06
limita a **marcação**; o cancelamento permanece permitido após o início para
remover a contribuição da estimativa.

O prazo compara o relógio da aplicação com a data do cardápio e o início do
serviço em `America/Sao_Paulo`, usando `HORARIOS_INICIO_REFEICAO` de
`app/core/config.py`. É possível marcar em dias anteriores. Um serviço sem
horário configurado recusa a marcação com `422` explicativo.

## Consulta pessoal

`GET /intencoes/` aceita `campus_id` (inteiro positivo), `data_inicio` e `data_fim`.
Sem datas, usa a semana do instante atual em Brasília, de segunda-feira a
domingo. Com intervalo explícito, as duas datas devem ser informadas juntas, no
formato estrito `YYYY-MM-DD`, com início menor ou igual ao fim. Os dois extremos
são inclusivos. Datas inválidas, incompletas, timestamps e intervalos invertidos
recebem `422`. Um campus sem intenções retorna lista vazia.

```json
[
  {
    "cardapio_id": 1,
    "ativa": true,
    "campus_id": 1,
    "data": "2026-09-15",
    "tipo_refeicao": "almoco"
  }
]
```

A ordenação é crescente por data, campus, tipo de refeição e ID do cardápio.
As leituras individuais e a listagem pessoal retornam `Cache-Control: no-store`.
O cabeçalho de identidade define o recorte, sem consulta por UUID de terceiros.

## Erros e persistência

- `400`: `X-Identidade` ausente, inválido ou diferente de UUID v4.
- `404`: cardápio inexistente nas operações individuais.
- `422`: prazo encerrado, horário não configurado ou filtro inválido.
- `409`: colisão com identidade reservada a uma intenção simulada da refeição.

A tabela `intencao` possui `id`, `cardapio_id`, `identidade`, `ativa` (padrão
`true`) e `simulada` (padrão `false`), com unicidade no banco para
`(cardapio_id, identidade)` e relação com `cardapio`. A API cria e reativa apenas
intenções reais: dados extras no corpo não escolhem a flag de simulação. Registros
simulados ficam fora da consulta pessoal e não são alterados pelo cancelamento.
Em uma disputa por inserção, a API desfaz a transação que conflitou e recupera a
intenção persistida, mantendo uma só linha.

A reimportação substitui os itens do cardápio existente e preserva suas intenções
ativas e canceladas. A migração `7c8d9e0f1a2b`, após `6b7c8d9e0f1a`, cria apenas
a tabela de intenções; o downgrade remove essa tabela. Check-ins legados
permanecem no banco e sem novas rotas públicas.

## Verificação local

Na pasta `backend`, usando o ambiente virtual existente:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check app tests
```

Os testes usam bancos SQLite isolados, incluindo a disputa de duas sessões e o
upgrade/downgrade da nova migração. A revisão antiga de amendoim tem um `ALTER
COLUMN` específico de PostgreSQL; os testes seguem o contorno SQLite já adotado
no projeto antes de avançar pelas migrações seguintes. O DDL do novo modelo
também é compilado para PostgreSQL. Essas verificações não executam migrações em
um PostgreSQL real nem validam uma publicação em produção.

## Estimativas de intenções — RF07

`GET /estimativas/` é uma consulta pública, sem `X-Identidade`. Parâmetros:

| Parâmetro | Regra |
| --- | --- |
| `campus_id` | Inteiro positivo, obrigatório; campus inexistente recebe `404` |
| `data_inicio`, `data_fim` | Datas obrigatórias, com extremos inclusivos e início menor ou igual ao fim |
| `tipo_refeicao` | Opcional: `cafe_da_manha`, `almoco` ou `jantar` |
| `dados_simulados` | `false` por padrão; `true` consulta somente intenções simuladas |

Exemplo: `/estimativas/?campus_id=1&data_inicio=2026-11-02&data_fim=2026-11-08`.
Um intervalo invertido ou filtro inválido recebe `422`. A lista contém cada
refeição cadastrada no recorte, inclusive as que não receberam intenções; não
inventa refeições para dias sem publicação. A ordem é data, tipo de refeição e ID.
As respostas de sucesso usam `Cache-Control: no-store`. Nenhuma resposta contém
identidades.

```json
[
  {
    "cardapio_id": 1,
    "campus_id": 1,
    "data": "2026-11-04",
    "tipo_refeicao": "almoco",
    "data_inicio": "2026-11-02",
    "data_fim": "2026-11-08",
    "calculado_em": "2026-11-04T09:00:00-03:00",
    "dados_simulados": false,
    "amostra_minima": 10,
    "status": "disponivel",
    "mensagem": "Estimativa de intenções; não representa a fila real.",
    "contagem": 11
  }
]
```

A contagem considera somente intenções ativas do campus, data e refeição. A
unicidade da tabela evita repetir a mesma identidade/refeição. Cancelamentos
deixam de contribuir. Reais e simuladas são sempre contadas separadamente: nove
reais mais nove simuladas continuam insuficientes em ambas as consultas.

O limiar vem de `AMOSTRA_MINIMA_ESTIMATIVA`, em `app/core/config.py`. Abaixo dele,
inclusive sem nenhuma intenção, `status` é `dados_insuficientes`, a mensagem
informa a insuficiência e o campo `contagem` é **omitido**, sem outro campo com o
total oculto. Com dez ou mais, `status` é `disponivel` e a contagem é incluída.
O intervalo consultado e o instante do cálculo acompanham cada resultado; todas
as refeições empatadas continuam na lista. Isso representa intenções, sem
horário de chegada, medição da fila ou tempo de espera.

Para a demonstração, solicite explicitamente `dados_simulados=true` e preserve
essa identificação na interface. Não é uma estimativa dos usuários reais. O
contrato prepara a integração do frontend da issue 79, sem alterar suas telas.

Os testes incluem 0, 9, 10 e 11 intenções, separação de origens, cancelamento,
marcação repetida via API, recortes de campus/data/refeição e configuração única.
