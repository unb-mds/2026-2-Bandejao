# Documento de Visão — Bandejão

**Projeto:** Bandejão — Cardápio e Fila dos RUs da UnB
**Instituição:** Universidade de Brasília (UnB) — todos os campi
**Equipe:** 7 integrantes
**Versão:** 1.0

---

## 1. Introdução / Problema

Os Restaurantes Universitários (RU) da UnB, em seus diferentes campi (Darcy Ribeiro, Ceilândia, Gama, Planaltina e Fazenda Água Limpa), publicam seus cardápios semanais em formato de PDF, o que dificulta o acesso rápido e organizado a essa informação. Alunos não têm uma forma prática de:

- Consultar o cardápio de forma estruturada e com antecedência;
- Filtrar refeições de acordo com restrições alimentares (vegetariano, alergias);
- Avaliar as refeições servidas, gerando feedback útil para a comunidade;
- Registrar reclamações sobre qualidade, higiene ou atendimento separadamente das avaliações por nota;
- Saber com antecedência os horários de maior movimento no RU, o que causa filas longas e imprevisíveis.

## 2. Objetivo do Projeto

Criar uma aplicação que centralize o cardápio semanal dos RUs da UnB, abrangendo todos os campi, permita a avaliação das refeições e o registro independente de reclamações e, em uma etapa posterior, forneça uma estimativa de movimento com base no planejamento semanal dos usuários. A estimativa de horários dentro de uma refeição depende da coleta de faixas de chegada e da decisão D05 do [Documento de Requisitos](Requisitos.md).

## 3. Escopo

A Release 1 acadêmica avalia a definição e a organização da solução; a Release 2 avalia sua implementação. Os grupos abaixo indicam prioridade do produto, não funcionalidades já entregues. Critérios, regras e decisões pendentes estão no [Documento de Requisitos](Requisitos.md).

### Núcleo do produto
- Exibição do cardápio da semana dos RUs, com seleção por campus;
- Filtros alimentares (vegetariano, alergias);
- Sistema de avaliação de refeições pelos usuários.
- Seção independente para registro de reclamações sobre qualidade, higiene e atendimento.

### Evolução do produto
- Planejamento antecipado dos dias e refeições em que o usuário pretende comer no RU;
- Estimativa de movimento a partir dos planejamentos por dia, refeição e campus. Estimar horários dentro de uma refeição depende de coletar faixas de chegada; essa decisão está pendente em D05 do Documento de Requisitos.

## 4. Público-alvo / Stakeholders

- **Usuários finais:** alunos e servidores da UnB que utilizam os RUs de qualquer um dos campi.
- **Stakeholder indireto:** administração do RU, que pode se beneficiar dos dados de avaliação e uso agregados pela ferramenta.

## 5. Visão Geral da Solução

O Bandejão é uma aplicação que consome o cardápio semanal publicado pelos RUs de todos os campi da UnB (atualmente em PDF), estrutura essa informação e a disponibiliza de forma organizada e filtrável para o usuário, por campus. Além de consultar o cardápio, o usuário pode avaliar as refeições que experimentou e registrar reclamações de forma independente. Em uma segunda etapa, o usuário poderá planejar antecipadamente os dias e refeições em que pretende comer no RU, e o sistema utilizará o volume desses planejamentos para estimar o movimento por refeição. A apresentação de horários depende dos dados adicionais e da definição de escopo registrados em D05.

O sistema é dividido em quatro camadas: extração de dados (Python), backend/API (FastAPI), banco de dados (PostgreSQL) e frontend (React).

## 6. Restrições e Riscos

- **Coleta de dados:** o cardápio é publicado no site oficial do RU (`ru.unb.br/cardapio-refeitorio`), sem API oficial. O link de cada PDF muda semanalmente, e a extração precisa localizar e processar o PDF de cada um dos 5 campi. O site alerta que o cardápio "está sujeito a alterações sem aviso prévio".
- **Qualidade da estimativa de movimento (evolução):** depende de haver volume suficiente de planejamentos registrados pelos usuários por dia, refeição e campus; no início, os dados podem ser insuficientes para gerar previsões confiáveis.
- **Equipe:** o projeto é conduzido por um grupo de 7 integrantes com diferentes níveis de experiência e engajamento, o que exige alinhamento constante de processo e fluxo de trabalho.

## 7. Critérios de Sucesso

- O cardápio da semana está visível e atualizado na aplicação, para todos os campi;
- O usuário consegue filtrar refeições por restrição alimentar (vegetariano, alergias);
- O usuário consegue avaliar uma refeição já servida;
- O usuário consegue registrar reclamações sobre uma refeição de forma independente da avaliação por nota;
- (Evolução) O usuário consegue planejar refeições e consultar uma estimativa de movimento, no nível de detalhe permitido pelos dados coletados e pela decisão D05;
- O progresso do desenvolvimento está rastreável através das issues e milestones no GitHub, conforme acompanhamento da professora.

---

*Documento sujeito a revisão pela equipe conforme o projeto evolui.*
