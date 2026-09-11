# Documento de Arquitetura — Bandejão

**Projeto:** Bandejão — Cardápio e Fila dos RUs da UnB
**Equipe:** 7 integrantes
**Versão:** 1.0

---

## 1. Visão geral da arquitetura

O sistema é dividido em quatro camadas, cada uma com uma responsabilidade isolada. Essa separação permite que cada dupla/pessoa do grupo trabalhe de forma independente, e limita o impacto de mudanças (principalmente na camada de extração, que é a mais sujeita a variações externas).

```
Cardápio (PDF)  →  Extração de dados  →  Backend / API  →  Banco de dados
                                              ↓
                                          Frontend
```

## 2. Camadas

### 2.1 Extração de dados

- **Responsabilidade:** localizar o link do PDF de cada campus na página `ru.unb.br/cardapio-refeitorio`, baixar o arquivo e extrair as informações do cardápio (dia, refeição, itens, alérgenos, opção vegetariana).
- **Por que isolada:** é o componente mais frágil do sistema — depende de uma fonte externa sem API oficial, cujo formato pode mudar sem aviso. Isolar essa camada significa que, se o formato do RU mudar, o ajuste fica restrito a essa parte, sem afetar backend ou frontend.
- **Saída esperada:** dados estruturados (ex: JSON) por campus, prontos para serem persistidos no banco de dados.

### 2.2 Backend / API

- **Responsabilidade:** receber os dados extraídos e persistir no banco; aplicar regras de negócio (filtros alimentares, cálculo de avaliação); expor endpoints para o frontend consumir.
- **Principais funcionalidades (Release 1):** listar cardápio por campus, filtrar por restrição alimentar, registrar e listar avaliações de refeições.
- **Principais funcionalidades (Release 2):** registrar check-ins, calcular e expor estimativa de horário de pico.

### 2.3 Banco de dados

- **Responsabilidade:** armazenar cardápio (por campus e semana), refeições, avaliações e, na Release 2, histórico de check-ins.
- **Entidades principais (a detalhar em ADR):** Campus, Cardápio/Semana, Refeição, Avaliação, Check-in.

### 2.4 Frontend

- **Responsabilidade:** consumir a API e apresentar ao usuário o cardápio, os filtros alimentares e a interface de avaliação.
- **Principais telas (Release 1):** seleção de campus, listagem do cardápio da semana com filtros, avaliação de refeição.
- **Principais telas (Release 2):** indicador de horário de pico da fila.

## 3. Fluxo de dados

1. A extração roda periodicamente (semanalmente, acompanhando a publicação do RU), buscando o PDF de cada campus.
2. Os dados extraídos são enviados ao backend, que os persiste no banco de dados.
3. O frontend consulta a API do backend para exibir o cardápio, aplicar filtros e enviar avaliações.
4. (Release 2) O backend registra check-ins enviados pelo frontend e calcula a estimativa de pico a partir do histórico armazenado.

## 4. Stack técnica

| Camada | Tecnologia |
|---|---|
| Extração de dados | *(a definir)* |
| Backend / API | *(a definir)* |
| Banco de dados | *(a definir)* |
| Frontend | *(a definir)* |

---

*Documento sujeito a revisão pela equipe conforme o projeto evolui.*
