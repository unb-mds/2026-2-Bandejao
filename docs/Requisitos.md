# Documento de Requisitos — Bandejão

**Projeto:** Bandejão — Cardápio e Fila dos RUs da UnB
**Equipe:** 7 integrantes
**Versão:** 1.0

---

## 1. Requisitos Funcionais (RF)

### Release 1

| ID | Descrição |
|---|---|
| RF01 | O sistema deve exibir o cardápio da semana de cada Restaurante Universitário (RU) da UnB (Darcy Ribeiro, Ceilândia, Gama, Planaltina, Fazenda Água Limpa). |
| RF02 | O usuário deve poder selecionar/filtrar o cardápio por campus. |
| RF03 | O sistema deve permitir filtrar as refeições exibidas por restrição alimentar (ex: vegetariano, alergias/itens como leite, ovos, glúten, soja, oleaginosas, carne suína, frutos do mar). |
| RF04 | O usuário deve poder avaliar uma refeição já servida. |
| RF05 | O sistema deve armazenar e exibir o histórico de avaliações de uma refeição. |

### Release 2

| ID | Descrição |
|---|---|
| RF06 | O sistema deve registrar check-ins de usuários no RU (para compor o histórico usado na previsão de fila). |
| RF07 | O sistema deve estimar e exibir o horário de maior movimento (pico de fila) com base no histórico de check-ins. |

## 2. Requisitos Não Funcionais (RNF)

| ID | Descrição |
|---|---|
| RNF01 | O sistema deve responder às consultas de cardápio em tempo aceitável para uso em horário de pico (ex: horário de almoço). |
| RNF02 | O processo de extração do cardápio deve ser atualizado semanalmente, acompanhando a publicação do RU. |
| RNF03 | O processo de extração deve ser resiliente a pequenas variações no formato de publicação do PDF, e deve ser possível ajustá-lo rapidamente caso o formato mude. |
| RNF04 | O sistema deve estar disponível e implantado (deploy) de forma acessível para avaliação, conforme exigido pela disciplina. |
| RNF05 | O sistema não deve apresentar vulnerabilidades críticas ou altas em aberto na varredura de segurança estática (SAST). |

## 3. Restrições

- O cardápio não possui API oficial; a extração depende do PDF publicado em `ru.unb.br/cardapio-refeitorio`, cujo link muda semanalmente e é sujeito a alterações sem aviso prévio.
- A previsão de fila (RF07) depende de volume suficiente de check-ins (RF06) registrados; nas fases iniciais os dados podem ser insuficientes para gerar estimativas confiáveis.

## 4. Rastreabilidade

Cada requisito deste documento deve ser referenciado nas issues que o implementam (ex: "Implementa RF03"), de forma que seja possível rastrear issue → PR → teste.

---

*Documento sujeito a revisão pela equipe conforme o projeto evolui.*
