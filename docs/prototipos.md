# Protótipos e produto

## Materiais existentes

- [Board no Figma: personas, story map e protótipos](https://www.figma.com/board/61OYJuLeyE3m3jwzSzfZ1W/Bandejao-2026-2?t=kVJg4rR4m3kIYsj7-0).
- [Protótipo web informado pela equipe](https://frontend-react-tan-gamma.vercel.app).

A [Sprint 02](scrum/sprint02.md) registra a preparação dos materiais de produto. A disponibilidade e a integração do protótipo externo com a API não foram verificadas nesta atualização da GH Page.

## Incorporação à aplicação local

As telas da equipe em [marilluantunes/frontend-react](https://github.com/marilluantunes/frontend-react), revisão `c1833a3b7175765574e258c6574973b88a04c361`, foram incorporadas ao diretório `frontend/` em 01/10/2026. A aplicação usa React, Vite, TypeScript e Tailwind v4. A consulta de campi/cardápios usa a API do projeto; os demais fluxos continuam demonstrações locais identificadas. Consulte [Arquitetura](Arquitetura.md) e [Desenvolvimento](desenvolvimento.md).

Essa integração local não atualiza a publicação Vercel externa nem comprova aceite dos requisitos.

## Roteiro de revisão

| Fluxo a revisar no protótipo | Requisitos relacionados |
|---|---|
| Selecionar campus e consultar cardápio | RF01, RF02 |
| Filtrar por dieta e restrição alimentar | RF03 |
| Enviar e consultar avaliações | RF04, RF05 |
| Registrar reclamação independentemente da nota | RF08 |
| Planejar refeições e consultar estimativa de movimento | RF06, RF07; escopo futuro |

A tabela orienta a revisão; não afirma que todos os fluxos estejam prototipados. O responsável por produto deve acrescentar links diretos das telas e registrar lacunas e decisões. Consulte os [requisitos e critérios de aceitação](Requisitos.md) para avaliar cada fluxo.
