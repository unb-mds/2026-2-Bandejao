# Sprint 04 — Núcleo no backend, telas integradas e publicação

**Período:** 21/10/2026 a 04/11/2026

**Objetivo da sprint:** colocar em funcionamento, de ponta a ponta, o que o usuário faz na Release 1: avaliar uma refeição e registrar uma reclamação com dados gravados no banco, ver a data da última importação e acessar a aplicação publicada em HTTPS.

Os requisitos citados estão no [Documento de Requisitos](../Requisitos.md).

## O que a sprint entrega

| Área | Entrega | Requisitos |
|---|---|---|
| Backend | Avaliação aceita somente dentro da janela de horário da refeição | RF04; RN05 |
| Backend | Reclamações: modelo, migração, rotas e leitura pela equipe com token | RF08; RN10 |
| Backend | Data e hora da última importação bem-sucedida por campus | RF01 |
| Frontend | Avaliações e histórico ligados à API, com a identidade anônima do navegador | RF04; RF05 |
| Frontend | Tela de reclamações ligada à API | RF08 |
| Frontend | Aviso de privacidade sobre o código anônimo | D04 |
| Dados / DevOps | Sincronização automática a cada 6 horas, com registro por campus | RNF02 |
| DevOps | Aplicação publicada em HTTPS, com a versão visível | RNF04 |

## Issues da sprint

| # | Issue | Área |
|---|---|---|
| 1 | Avaliação só dentro da janela de horário | Back |
| 2 | Reclamações no backend | Back |
| 3 | Data da última importação bem-sucedida | Back + Front |
| 4 | Ligar avaliações à API | Front |
| 5 | Tela de reclamações | Front |
| 6 | Aviso de privacidade | Front |
| 7 | Sincronização automática a cada 6 horas | Dados + DevOps |
| 8 | Publicar em HTTPS | DevOps |

## Critérios de aceitação

1. **Janela de avaliação (RF04, RN05):** antes do início da refeição, a API recusa a avaliação com mensagem que explica o motivo; no início, aceita; um instante antes de 00h do dia seguinte, aceita; às 00h do dia seguinte, recusa; refeição inexistente é recusada. Uma nova nota da mesma identidade para a mesma refeição atualiza a anterior, sem criar outra. Os testes usam o fuso `America/Sao_Paulo`.
2. **Reclamações no backend (RF08, RN10):** categoria válida (qualidade, higiene, atendimento ou outros) e descrição de 1 a 1.000 caracteres gravam a reclamação com a refeição, a identidade e o instante do envio, sem exigir nota. Categoria inválida, descrição vazia ou acima do limite e refeição inexistente são recusadas com o motivo, sem gravar. Não existe rota pública de listagem, e outra identidade não consegue ver a reclamação. A leitura pela equipe exige token. Reimportar o cardápio não apaga as reclamações.
3. **Última importação (RF01):** a API devolve a data e a hora da última importação bem-sucedida de cada campus e o link da fonte; a tela do cardápio exibe essas informações. Uma falha de atualização não altera a data guardada.
4. **Avaliações na API (RF04, RF05):** a tela envia nota e comentário com a identidade do navegador; erros da API, como janela fechada ou campo inválido, aparecem com mensagem clara; o histórico mostra nota, comentário e data/hora, da mais recente para a mais antiga, somente da refeição escolhida; sem avaliações, a tela mostra "sem avaliações", sem notas fictícias; a avaliação permanece ao recarregar a página.
5. **Tela de reclamações (RF08):** somente as 4 categorias; sem campo de nome, sem foto e sem lista de reclamações de outras pessoas; limite de 1.000 caracteres visível e respeitado; a confirmação não afirma encaminhamento ao RU nem publicação; erros da API aparecem com mensagem clara.
6. **Aviso de privacidade (D04):** o aviso aparece na primeira visita e pode ser relido depois; informa que o app guarda um código anônimo no navegador, sem nome, e-mail ou outro dado pessoal, e que quem limpar os dados do navegador terá outro código.
7. **Sincronização (RNF02, D07b):** a rotina roda a cada 6 horas e usa o token por variável de ambiente; cada execução registra campus, URL e instante de sucesso; a falha em um campus é registrada por campus e não interrompe os demais; processar a mesma publicação duas vezes não duplica refeições nem apaga avaliações ou reclamações.
8. **Publicação (RNF04):** em um navegador limpo, fora da máquina de desenvolvimento, a URL abre em HTTPS sem erro de certificado; a versão (commit ou tag) aparece na interface ou em uma rota; segredos como token e senha do banco ficam em variáveis da plataforma, fora do repositório.