# Banco de Dados — Estudo

## O que é

Banco de dados é o componente responsável por armazenar, organizar e recuperar os dados de um sistema de forma persistente — ou seja, os dados continuam existindo mesmo depois que a aplicação é reiniciada. É gerenciado por um **SGBD** (Sistema Gerenciador de Banco de Dados), software que controla como os dados são armazenados, consultados, alterados e protegidos (ex: PostgreSQL, MySQL, MongoDB).

No Bandejão, é a camada que guarda o cardápio já estruturado, as avaliações dos usuários e, na Release 2, o histórico de check-ins.

## Banco relacional x não relacional

### Relacional (SQL)
Organiza os dados em **tabelas**, com colunas (atributos) e linhas (registros). As tabelas se relacionam entre si por meio de chaves.

- **Chave primária (PK)** — identifica de forma única cada linha de uma tabela.
- **Chave estrangeira (FK)** — referencia a chave primária de outra tabela, criando um relacionamento entre elas.
- Segue um **esquema fixo**: a estrutura das tabelas é definida antes de inserir dados, o que garante consistência.
- Consultado através de **SQL** (Structured Query Language).
- Exemplos: PostgreSQL, MySQL, SQLite.

> Exemplo (Bandejão): uma tabela `pratos` com FK para `cardapios`, e uma tabela `avaliacoes` com FK para `pratos` e para `usuarios`.

### Não relacional (NoSQL)
Não exige uma estrutura fixa de tabelas. Formatos comuns:

- **Documentos** (ex: MongoDB) — dados guardados como documentos tipo JSON, sem esquema rígido.
- **Chave-valor** (ex: Redis) — acesso muito rápido por chave, útil para cache.
- **Colunar / grafo** — formatos mais específicos, menos comuns em projetos de porte pequeno/médio.

Costuma ser escolhido quando os dados são pouco estruturados, mudam de formato com frequência, ou quando a prioridade é escala horizontal muito grande — trade-off geralmente é abrir mão de relações fortes e de algumas garantias de consistência.

### Qual escolher
Depende do formato e das relações entre os dados do sistema. Dados com relações claras e necessidade de integridade (como o Bandejão: prato pertence a um cardápio de um campus/dia, avaliação se refere a um prato e a um usuário) tendem a se beneficiar de um banco relacional. Dados muito variáveis em estrutura, ou que exigem escala massiva desde o início, tendem a se beneficiar de NoSQL.

## Modelagem de dados

### Modelo conceitual
Representação abstrata das entidades do domínio e como elas se relacionam, geralmente feita com um **diagrama entidade-relacionamento (DER)**, antes de pensar em tabelas ou tecnologia específica.

> Exemplo (Bandejão): entidades como `Campus`, `Cardápio`, `Prato`, `RestriçãoAlimentar`, `Usuário`, `Avaliação` e (Release 2) `CheckIn`, com relacionamentos como "um Cardápio tem vários Pratos" ou "um Prato pode ter várias RestriçõesAlimentares".

### Modelo lógico/físico
Tradução do modelo conceitual para tabelas, colunas, tipos de dados e chaves — já pensando no SGBD escolhido.

### Cardinalidade dos relacionamentos
- **1:1** — um registro de uma tabela se relaciona com no máximo um de outra.
- **1:N** — um registro se relaciona com vários de outra tabela (ex: um Cardápio tem vários Pratos).
- **N:N** — vários registros de uma tabela se relacionam com vários de outra, geralmente resolvido com uma tabela associativa (ex: Prato e RestriçãoAlimentar — um prato pode ter várias restrições, e uma restrição se aplica a vários pratos, então existe uma tabela intermediária `prato_restricao`).

## Normalização

Processo de organizar as tabelas para reduzir redundância e evitar inconsistências, seguindo formas normais (1FN, 2FN, 3FN):

- **1FN** — cada coluna guarda um valor atômico (não uma lista de valores).
- **2FN** — elimina dependências parciais (relevante quando a chave primária é composta).
- **3FN** — elimina dependências transitivas (um atributo não deve depender de outro atributo que não seja a chave).

Na prática: em vez de uma tabela `pratos` com uma coluna de texto tipo `"contém leite, contém glúten"`, normaliza-se em uma tabela `restricoes_alimentares` e uma tabela associativa `prato_restricao` — isso evita repetir texto e facilita filtrar (ex: "todos os pratos sem glúten").

Às vezes normalizar demais prejudica desempenho de leitura (exige mais `JOIN`s); **desnormalizar** propositalmente uma parte do modelo é uma troca válida quando a prioridade é velocidade de consulta sobre economia de espaço/consistência absoluta.

## SQL — operações básicas

- **DDL (Data Definition Language)** — define a estrutura: `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`.
- **DML (Data Manipulation Language)** — manipula os dados: `SELECT`, `INSERT`, `UPDATE`, `DELETE`.
- **JOIN** — combina dados de duas ou mais tabelas relacionadas (ex: buscar o nome do prato junto com suas restrições alimentares, que estão em tabelas diferentes).
- **Índices** — estrutura auxiliar que acelera buscas em colunas frequentemente consultadas (ex: um índice na coluna de data do cardápio, já que a consulta mais comum do sistema é "cardápio da semana atual").

## Transações e integridade

- **Transação** — conjunto de operações tratado como uma unidade: ou todas acontecem, ou nenhuma acontece (evita, por exemplo, salvar uma avaliação sem vínculo válido a um usuário por causa de uma falha no meio do processo).
- **Propriedades ACID**:
  - **Atomicidade** — a transação é tudo ou nada.
  - **Consistência** — a transação leva o banco de um estado válido a outro estado válido.
  - **Isolamento** — transações concorrentes não interferem uma na outra.
  - **Durabilidade** — uma vez confirmada, a transação persiste mesmo em caso de falha do sistema.
- **Integridade referencial** — o SGBD impede, por exemplo, que uma avaliação referencie um prato que não existe, através das chaves estrangeiras.

## Migrations

Scripts versionados que alteram a estrutura do banco de dados (criar tabela, adicionar coluna, etc.) de forma controlada e repetível, geralmente numa pasta do projeto e aplicados na ordem correta. Permitem que qualquer pessoa do time (ou o ambiente de produção) chegue à mesma estrutura de banco a partir do zero, e mantêm um histórico de como o esquema evoluiu — importante em projeto em grupo, onde o modelo de dados muda conforme o entendimento do domínio amadurece.

## Relação com o projeto Bandejão

- O modelo de dados do Bandejão tem relações claras entre as entidades (Campus, Cardápio, Prato, RestriçãoAlimentar, Usuário, Avaliação, CheckIn), o que favorece um banco relacional, como já indicado no estudo de [arquitetura de software](arquitetura_software.md).
- Os filtros alimentares (vegetariano, sem glúten, sem lactose etc., citados no [CLAUDE.md](../../CLAUDE.md)) dependem diretamente de uma boa modelagem: tratar cada restrição como uma entidade própria (em vez de texto solto no prato) é o que viabiliza a consulta "me mostre só os pratos sem glúten" com uma query simples.
- A Release 2 (previsão de horário de pico) depende de uma tabela de `CheckIn` acumulando histórico — é um bom exemplo de decisão de modelagem que vale antecipar desde a Release 1 (criar a tabela e já registrar os check-ins), mesmo que a funcionalidade de previsão em si só seja construída depois.
- Como o cardápio é reextraído periodicamente do PDF do RU, faz sentido pensar desde já em como evitar duplicar cardápios/pratos já existentes no banco (ex: chave única por campus + data + prato) ao rodar a extração toda semana.

## Dúvidas em aberto

*(preencher conforme o grupo escolher o SGBD e definir o modelo de dados final, ex: qual SGBD usar, como versionar as migrations, como tratar reextrações semanais sem duplicar dados)*

## Fontes

- [Cap. 5: Persistência – Engenharia de Software Moderna](https://engsoftmoderna.info/cap5.html)
- [SQL vs NoSQL — AWS](https://aws.amazon.com/pt/compare/the-difference-between-sql-and-nosql/)
- [Database Normalization — PostgreSQL Tutorial](https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-normalization/)
