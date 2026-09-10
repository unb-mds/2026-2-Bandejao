# Arquitetura de Software — Estudo

## O que é

Arquitetura de software é o conjunto de decisões estruturais de alto nível sobre como um sistema é organizado: em que componentes/camadas ele se divide, como esses componentes se comunicam, onde os dados ficam armazenados e quais tecnologias sustentam cada parte. É a "planta" do sistema — decisões tomadas cedo, difíceis e caras de reverter depois, e que moldam a capacidade do time de evoluir o software com o tempo.

Diferente de um detalhe de implementação (ex: nome de uma função), uma decisão arquitetural afeta múltiplos componentes, é difícil de mudar isoladamente e tem impacto direto em qualidades como manutenibilidade, escalabilidade e resiliência a falhas.

## Por que importa

Um sistema com boa arquitetura facilita:

- **Isolar mudanças** — alterar uma parte do sistema sem quebrar as demais.
- **Trabalhar em paralelo** — times/pessoas diferentes cuidam de camadas diferentes sem pisar no trabalho um do outro.
- **Testar** — componentes bem separados são mais fáceis de testar isoladamente (testes unitários) e em conjunto (testes de integração).
- **Escalar e evoluir** — trocar uma tecnologia (ex: banco de dados) ou adicionar uma funcionalidade nova sem reescrever o sistema inteiro.

O custo de uma decisão arquitetural ruim geralmente não aparece de imediato — aparece meses depois, quando o sistema já cresceu e mudar a estrutura se torna caro e arriscado.

## Atributos de qualidade (requisitos não funcionais que a arquitetura precisa suportar)

- **Manutenibilidade** — facilidade de entender, corrigir e estender o código.
- **Escalabilidade** — capacidade de suportar mais uso (mais usuários, mais dados) sem degradar.
- **Disponibilidade / resiliência** — o sistema continua funcionando (ou falha de forma controlada) mesmo quando uma parte falha.
- **Desempenho** — tempo de resposta e uso eficiente de recursos.
- **Segurança** — proteção de dados e controle de acesso.
- **Testabilidade** — o quanto é fácil escrever testes automatizados para o sistema.

Arquitetura é, em essência, o conjunto de decisões que tenta equilibrar esses atributos — normalmente há tensão entre eles (ex: mais camadas de abstração ajudam manutenibilidade, mas podem custar desempenho).

## Camadas (layers) e separação de responsabilidades

Um padrão comum é dividir o sistema em camadas, cada uma com uma responsabilidade clara e comunicando-se apenas com a camada vizinha:

- **Camada de dados/extração** — obtém e estrutura os dados brutos.
- **Camada de negócio (backend/API)** — aplica regras, valida, expõe funcionalidades.
- **Camada de persistência (banco de dados)** — armazena o estado do sistema.
- **Camada de apresentação (frontend)** — interface com o usuário final.

O princípio por trás disso é a **separação de responsabilidades (separation of concerns)**: cada camada muda por um motivo diferente, então isolá-las reduz o efeito cascata de mudanças. Um exemplo clássico é o RU mudar o formato do PDF do cardápio — se a extração estiver isolada, só ela precisa ser ajustada; backend, banco e frontend continuam intactos.

## Estilos arquiteturais comuns

- **Monolito** — todo o sistema (ou todo o backend) roda como uma única aplicação/processo. Mais simples de desenvolver e implantar no início; pode ficar difícil de manter conforme o sistema cresce.
- **Arquitetura em camadas (layered/N-tier)** — divisão explícita entre apresentação, negócio e dados, como descrito acima. É o estilo mais comum em projetos de porte pequeno/médio, incluindo projetos acadêmicos.
- **Microsserviços** — cada funcionalidade roda como um serviço independente, com seu próprio deploy e, às vezes, seu próprio banco. Ganha-se escalabilidade e isolamento de falha, mas paga-se em complexidade operacional (comunicação entre serviços, consistência de dados). Geralmente só compensa em sistemas grandes com times grandes.
- **Cliente-servidor** — separação entre quem consome (cliente/frontend) e quem serve dados/lógica (servidor/backend), comunicando-se via rede (tipicamente uma API HTTP/REST).
- **Pipeline/ETL (Extract-Transform-Load)** — comum quando o sistema depende de processar dados de uma fonte externa em etapas: extrair o dado bruto, transformá-lo em um formato estruturado, carregá-lo no destino final (banco de dados). É o padrão que mais se aproxima do que a camada de extração do cardápio do RU precisa fazer.

## Comunicação entre componentes

- **API REST** — padrão mais comum para comunicação entre frontend e backend: endpoints HTTP que representam recursos (ex: `GET /cardapio/semana`), usando verbos HTTP (GET, POST, PUT, DELETE) e formato JSON.
- **Acoplamento forte x fraco** — componentes fortemente acoplados dependem de detalhes internos um do outro e quebram fácil quando um muda; componentes fracamente acoplados se comunicam por contratos bem definidos (ex: uma API com schema estável), o que permite evoluir cada lado de forma mais independente.
- **Contrato de API** — definir com clareza o formato de entrada/saída de cada endpoint (ex: o que exatamente vem em um item do cardápio: nome do prato, campus, dia, restrições alimentares) evita que frontend e backend fiquem "adivinhando" o formato um do outro.

## Persistência de dados

Decisões arquiteturais também envolvem como e onde os dados são armazenados:

- **Banco relacional (SQL)** — bom quando os dados têm estrutura bem definida e relações claras entre entidades (ex: cardápio, prato, restrição alimentar, avaliação, usuário, check-in) e quando há necessidade de consultas relacionais e integridade referencial.
- **Banco não relacional (NoSQL)** — mais flexível para dados semiestruturados ou que mudam de formato com frequência; costuma trocar consistência forte e relações por flexibilidade de esquema.
- Para o Bandejão, o cardápio semanal, as avaliações e (na Release 2) o histórico de check-ins têm relações naturais entre si (um prato pertence a um cardápio de um campus/dia; uma avaliação se refere a uma refeição e a um usuário), o que favorece um modelo relacional.

## Resiliência a fontes externas instáveis

Um ponto de atenção arquitetural específico do Bandejão: o sistema depende de uma fonte de dados externa (PDFs do RU) que muda de formato e de URL sem aviso e sem API oficial. Isso é tratado arquiteturalmente isolando essa dependência em um componente próprio (a camada de extração), de forma que:

- Uma falha na extração de um campus não deveria derrubar o sistema inteiro (ex: se o PDF de um campus mudar de formato, os demais campi continuam funcionando).
- O restante do sistema (backend, frontend) depende dos dados já estruturados, não do PDF em si — então uma mudança no formato do PDF exige ajuste apenas na extração, não em cascata pelo sistema todo.

Esse é um exemplo prático do princípio de isolar a parte mais frágil/instável de um sistema atrás de uma interface estável.

## Documentando decisões arquiteturais

- **Diagramas** (ex: diagrama de componentes, diagrama de arquitetura em camadas) ajudam a comunicar a estrutura do sistema para o time e para quem chega depois.
- **ADR (Architecture Decision Record)** — documento curto que registra uma decisão arquitetural: o contexto, as opções consideradas, a decisão tomada e as consequências. Útil para não perder o "porquê" de uma escolha ao longo do tempo, especialmente relevante em projeto em grupo, onde nem todo mundo participa de toda decisão.

## Relação com o projeto Bandejão

- A arquitetura em 4 camadas descrita no [CLAUDE.md](../../CLAUDE.md) (extração → backend/API → banco de dados → frontend) é um exemplo direto de arquitetura em camadas com separação de responsabilidades: cada camada existe para isolar um tipo de mudança (formato do PDF, regras de negócio, modelo de dados, interface).
- A camada de extração funciona como um pipeline ETL: extrai o PDF/imagem do RU, transforma em dados estruturados (pratos, restrições alimentares, campus, dia) e carrega no banco.
- A divisão em Release 1 (cardápio, filtros, avaliação) e Release 2 (previsão de fila a partir de check-ins) também é uma decisão arquitetural, além de ser priorização de requisitos: a Release 2 depende de uma funcionalidade nova (registro de check-in) e de volume histórico de dados, então faz sentido que o modelo de dados já prevja isso desde a Release 1, mesmo que a previsão em si só seja construída depois.

## Dúvidas em aberto

*(preencher conforme o grupo definir a stack técnica de cada camada e conforme decisões arquiteturais forem tomadas, ex: banco de dados escolhido, se a extração roda como job agendado ou sob demanda, como lidar com falha de extração de um campus específico)*

## Fontes

- [Cap. 2: Arquitetura – Engenharia de Software Moderna](https://engsoftmoderna.info/cap2.html)
- [Software Architecture Patterns — Mark Richards, O'Reilly (resumo)](https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/)
- [Architecture Decision Records (ADR) — GitHub adr collection](https://adr.github.io/)
