---
name: frontend-componente
description: Use esta skill sempre que for criar ou modificar uma tela ou componente do frontend. Aciona em pedidos como "criar tela de listagem do cardápio", "implementar o filtro alimentar na interface", "criar componente de avaliação de refeição".
---

# Frontend — Bandejão

## Stack

React + Vite, na pasta `/frontend`.

## Estrutura de pastas

```
frontend/src/
├── App.jsx        → componente raiz
├── main.jsx        → ponto de entrada
└── assets/          → imagens e ícones
```

À medida que novas telas forem criadas, organizar em `src/components/` (componentes reutilizáveis) e `src/pages/` (telas completas).

## Convenções do projeto

- Componentes funcionais com Hooks (`useState`, `useEffect`) — não usar componentes de classe.
- Um componente por arquivo, nomeado em PascalCase (ex: `CardapioLista.jsx`).
- Consumir a API do backend (rodando em `localhost:8000` em desenvolvimento, via `docker-compose`) usando `fetch` ou uma lib simples como `axios`.
- Toda tela que lista o cardápio deve permitir selecionar o campus e aplicar os filtros alimentares definidos nos requisitos (`docs/Requisitos.md`).

## Telas esperadas (Release 1)

1. Seleção de campus
2. Listagem do cardápio da semana, com filtros alimentares
3. Interface de avaliação de uma refeição

## Pontos de atenção

- Tratar estados de carregamento e erro ao consumir a API (ex: cardápio ainda não disponível, falha de conexão).
- Manter a interface simples e funcional — não é objetivo do projeto um design elaborado, e sim a usabilidade dos filtros e da avaliação.
