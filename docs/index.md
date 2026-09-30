# Bandejão

**Cardápio semanal, filtros alimentares e avaliação das refeições dos Restaurantes Universitários da UnB.**

[🎨 Protótipo no Figma](https://www.figma.com/board/61OYJuLeyE3m3jwzSzfZ1W/Bandejao-2026-2?t=kVJg4rR4m3kIYsj7-0){ .md-button .md-button--primary }
[💻 Repositório no GitHub](https://github.com/unb-mds/2026-2-Bandejao){ .md-button }

!!! info "Projeto em andamento"
    Esta documentação acompanha o projeto sprint a sprint: requisitos, produto e decisões são atualizados conforme o grupo avança.

## Avaliação da Release 1

Esta entrega acadêmica apresenta a ideia e a organização da implementação. As funcionalidades descritas abaixo representam o escopo do produto; seu estado e as pendências estão registrados na arquitetura e nos requisitos.

| Material para avaliação | Onde consultar |
|---|---|
| Problema, público e escopo | [Visão do produto](documento_de_visao.md) |
| RFs, RNFs, regras e critérios de aceitação | [Requisitos e decisões pendentes](Requisitos.md) |
| Contexto e containers C4, relações entre dados | [Arquitetura](Arquitetura.md) |
| Fonte dos dados e contrato de importação | [Banco e importação](handoff_banco_e_importacao.md) |
| Figma e protótipo web | [Protótipos](prototipos.md) |
| Evolução do projeto | [Sprint 00](scrum/sprint00.md), [Sprint 01](scrum/sprint01.md), [Sprint 02](scrum/sprint02.md) |
| Passo a passo para rodar | [Desenvolvimento](desenvolvimento.md) |
| Manutenção e rastreabilidade desta página | [Publicação](github-pages.md) e [histórico](changelog.md) |

## 🎯 Objetivo

Os Restaurantes Universitários da UnB publicam o cardápio da semana apenas em **PDF**, separado por campus e sem nenhum filtro. Quem tem restrição alimentar não encontra rápido uma opção adequada, não há como avaliar as refeições e a fila é imprevisível.

O **Bandejão** centraliza o cardápio dos **5 campi** (Darcy Ribeiro, Ceilândia, Gama, Planaltina e Fazenda Água Limpa), permite filtrar por dieta e alérgenos, avaliar refeições e registrar reclamações, e, em uma segunda etapa, ajuda a escolher o melhor horário para ir ao RU.

## 🧩 Épicos do produto

<div class="grid cards" markdown>

-   :material-food: **Consulta ao cardápio**

    ---

    Cardápio da semana por campus, organizado por dia e refeição (café da manhã, almoço e jantar).

-   :material-filter: **Filtros alimentares**

    ---

    Filtro por dieta (vegetariano, vegetariano estrito) e exclusão de alérgenos, como glúten, leite, soja e amendoim.

-   :material-star: **Avaliação e reclamações**

    ---

    Nota de 1 a 5 para cada refeição e registro de reclamações, de forma independente da nota.

-   :material-calendar-check: **Planejamento e fila** *(Release 2)*

    ---

    O usuário marca os dias em que pretende ir ao RU, e o sistema estima o horário de maior movimento.

</div>

## 🏗️ Como funciona

```
Site do RU (PDFs) → Extração (Python) → Backend (FastAPI) ↔ Banco (PostgreSQL)
                                              ↑
                                       Frontend (React)
```

A extração localiza o PDF de cada campus na página do RU, lê a tabela (inclusive os ícones de alérgenos) e envia os dados para a API. Veja os detalhes em [Arquitetura](Arquitetura.md).

## 🗺️ Navegue pela documentação

<div class="grid cards" markdown>

-   :material-account-group: **Produto**

    ---

    Problema, objetivo, escopo e critérios de sucesso do projeto.

    [:octicons-arrow-right-24: Ver visão do produto](documento_de_visao.md)

-   :material-clipboard-list: **Requisitos**

    ---

    Requisitos funcionais e não funcionais das Releases 1 e 2.

    [:octicons-arrow-right-24: Ver requisitos](Requisitos.md)

-   :material-sitemap: **Arquitetura**

    ---

    Camadas do sistema, fluxo de dados e modelo do banco.

    [:octicons-arrow-right-24: Ver arquitetura](Arquitetura.md)

-   :material-book-open-variant: **Estudos**

    ---

    Conteúdos técnicos estudados pelo grupo na Sprint 00.

    [:octicons-arrow-right-24: Ver estudos](estudos/README.md)

-   :material-run-fast: **Sprints**

    ---

    O que foi feito em cada sprint.

    [:octicons-arrow-right-24: Ver sprint atual](scrum/sprint02.md)

</div>

---

Projeto acadêmico do grupo **G12**, disciplina de Métodos de Desenvolvimento de Software, UnB 2026/2.

## 👥 Equipe

Arthur Pitanga Lopes Costa e Lima · Gabriel Sousa Silva · João Victor Tavares de Souza · Gustavo Alves Bonfim · Fábio Abelha Castro Gomes · Maria Luiza Antunes de Oliveira · João Pedro da Motta Laude
