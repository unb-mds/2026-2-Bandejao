# Handoff — banco de dados e importação de cardápios

Este documento registra o que a infraestrutura de banco precisa aplicar e o
contrato que será usado pela rotina de extração dos cardápios do RU.

## Migração pendente

A revisão `cb27a92c83d1` adiciona a coluna abaixo à tabela `item_cardapio`:

| Coluna | Tipo | Nulo | Padrão para registros existentes |
| --- | --- | --- | --- |
| `contem_amendoim` | `BOOLEAN` | não | `false` |

A coluna permite que o filtro de alérgenos e a importação representem o ícone
de amendoim presente nos PDFs do RU. Ela é aplicada após a revisão inicial
`3e9ed9bb9055`.

No ambiente do backend, executar:

```bash
cd backend
alembic upgrade head
```

Para reverter somente essa alteração, caso necessário:

```bash
alembic downgrade 3e9ed9bb9055
```

Não é necessário alterar dados já cadastrados: a migração preenche os registros
anteriores com `false` e então remove o valor padrão do banco para que o modelo
da aplicação continue sendo a fonte da regra.

## Contrato de importação

### Endpoint

`POST /cardapios/importacao`

O endpoint é interno e recebe a saída normalizada da extração. A documentação
interativa também fica disponível em `/docs` quando a API está em execução.

### Autenticação (D08)

A importação exige `Authorization: Bearer <IMPORTACAO_TOKEN>`. Configure o mesmo segredo na API e na rotina de sincronização, por variável de ambiente; não o coloque no payload, na URL, no frontend ou no repositório. O arquivo de exemplo contém apenas a chave sem um token real.

Sem token ou com token inválido, a API recusa com 401/403 antes de gravar. Sem segredo configurado no servidor, a importação também permanece bloqueada. As consultas de campus e cardápio continuam públicas. As rotas HTTP de check-in legado foram retiradas; suas tabelas e registros não foram apagados.

### Payload

```json
{
  "campus": "Gama",
  "fonte_pdf_url": "https://ru.unb.br/wp-content/uploads/2026/09/Gama-Semana-01-21-9-a-27-9.pdf",
  "refeicoes": [
    {
      "data": "2026-09-21",
      "tipo_refeicao": "almoco",
      "itens": [
        {
          "categoria": "prato_principal",
          "tipo_dieta": "padrao",
          "nome": "Frango grelhado",
          "alergenos": ["soja"]
        }
      ]
    }
  ]
}
```

| Campo | Obrigatório | Regras |
| --- | --- | --- |
| `campus` | sim | Texto não vazio, com até 100 caracteres. |
| `fonte_pdf_url` | não | URL do PDF de origem ou `null`; até 500 caracteres. |
| `refeicoes` | não | Lista de refeições; vazia é aceita, mas não cria cardápios. |
| `refeicoes[].data` | sim | Data no formato ISO `YYYY-MM-DD`. |
| `refeicoes[].tipo_refeicao` | sim | `cafe_da_manha`, `almoco` ou `jantar`. |
| `refeicoes[].itens` | não | Lista de itens; vazia é aceita. |
| `itens[].categoria` | sim | Categoria reconhecida pelo domínio da API. |
| `itens[].tipo_dieta` | sim | `comum`, `padrao`, `ovolactovegetariano` ou `vegetariano_estrito`. |
| `itens[].nome` | sim | Texto não vazio, com até 200 caracteres. |
| `itens[].alergenos` | não | Lista sem repetição dos alérgenos aceitos. |

Categorias aceitas: `bebida`, `panificacao`, `opcao_extra`, `gordura`,
`salada_1`, `salada_2`, `molho_salada`, `prato_principal`, `guarnicao`,
`sopa`, `torrada`, `acompanhamento`, `sobremesa` e `fruta`.

Alérgenos aceitos: `leite`, `ovo`, `gluten`, `cogumelo`, `amendoim`, `mel`,
`soja`, `pimenta`, `oleaginosas`, `carne_suina` e `frutos_do_mar`. Um valor
fora dessa lista retorna `422 Unprocessable Entity` antes de qualquer gravação.

### Resposta de sucesso

O endpoint responde `200 OK`:

```json
{
  "campus_id": 1,
  "cardapios_processados": 1,
  "itens_processados": 1,
  "ultima_importacao_em": "2026-10-24T18:45:00Z",
  "fonte_pdf_url": "https://ru.unb.br/wp-content/uploads/2026/10/Gama-Semana-04.pdf"
}
```

## Regra de reprocessamento

A chave lógica de uma refeição é `(campus, data, tipo_refeicao)`.

- Se o campus ainda não existir, ele é criado.
- Se não existir um cardápio com essa chave, ele e seus itens são inseridos.
- Se já existir, a `fonte_pdf_url` é atualizada, os itens anteriores daquela
  refeição são removidos e os novos itens são inseridos.
- Quando toda a operação é confirmada, o campus recebe `ultima_importacao_em`
  em UTC e `ultima_fonte_pdf_url`. Validação, autenticação, extração ou gravação
  com falha não alteram o último sucesso armazenado.

Assim, reenviar um PDF corrigido ou executar a sincronização novamente não cria
duplicatas. As avaliações já vinculadas ao cardápio são preservadas, porque o
registro de `cardapio` é mantido; somente os respectivos itens são substituídos.

## Dependência da rotina de extração

Depois de aplicar a migração e iniciar a API, exporte `IMPORTACAO_TOKEN` com o mesmo valor usado pelo backend. A sincronização pode ser rodada com:

```bash
cd extracao
python -m extracao.sincronizar --backend-url http://localhost:8000
```

O processo trata cada campus de forma independente: uma falha de PDF ou de
importação em um campus não impede os demais de serem processados.

O perfil `sincronizacao` do Compose agenda a execução a cada seis horas; consulte o [roteiro de operação](desenvolvimento.md). A rotina não aplica migrações nem lê o `.env` automaticamente fora do Docker.
