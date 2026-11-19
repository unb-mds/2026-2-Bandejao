# Release 2 — 2.0.0

Preparação em **19/11/2026**. Esta nota descreve a versão fonte preparada
para revisão. A tag e o rascunho no GitHub identificam esse conteúdo; a
publicação final depende da integração e da conferência do commit implantado.

## O que está integrado

Consulta semanal dos cinco campi, filtros alimentares e origem dos PDFs;
avaliações e histórico persistidos; reclamações com acesso interno restrito;
planejamento de refeições por identidade anônima; estimativas por campus,
data e refeição com amostra mínima de 10 intenções. A importação usa token,
preserva feedback e isola falhas por campus.

Na verificação final foram corrigidos a semana que começava no domingo
([#112](https://github.com/unb-mds/2026-2-Bandejao/issues/112)), os cálculos
no fuso do dispositivo
([#113](https://github.com/unb-mds/2026-2-Bandejao/issues/113)) e as contagens
antigas após erro ou alteração do planejamento
([#114](https://github.com/unb-mds/2026-2-Bandejao/issues/114)). Nenhum
recurso novo foi adicionado após o congelamento.

## Demonstração e exclusões

Intenções simuladas são criadas apenas por comando explícito, separadas das
reais e identificadas na interface. A aba Lotação usa exemplos e relatos da
sessão; não mede fila nem tempo de espera. O protótipo Vercel é uma referência
visual separada da aplicação integrada.

Não fazem parte desta versão login, horários de chegada, medição da fila,
encaminhamento automático de reclamações, consulta posterior pelo autor ou
registro formal de serviço suspenso. A identidade por navegador pode ser
recriada ao apagar dados ou trocar de navegador. As marcações alimentares
reproduzem a fonte e não garantem ausência de ingredientes.

## Validação e limites

- 206 testes backend em SQLite, 3 exclusivos de PostgreSQL ignorados
  localmente; 59 da extração; cobertura 100% em ambos.
- 45 testes frontend em UTC e `Pacific/Auckland`; TypeScript, Oxlint e Vite
  aprovados. PostgreSQL 16 e SAST são executados no CI.
- Fluxos corrigidos verificados em Chrome 390 × 844 com API simulada,
  incluindo falha 503 sem contagem antiga. [Evidência](evidencias/verificacao-issue-101.md).
- Scripts k6 versionados, sem relatório medido de RNF01 disponível. Roteiro
  manual completo em celular físico e janela de disponibilidade de RNF04
  ainda sem comprovação. Isso não é aceite global dos requisitos.

## Fonte e hospedagem

Base de preparação: `17397beb184a708fdf5ab9991a6e51801ecf514b` e os commits
dos PRs de correção e documentação. A tag `v2.0.0` identifica a revisão fonte
preparada, enquanto a GitHub Release permanece como rascunho até a revisão.

Na consulta de 19/11, a interface estava acessível e a API respondeu 200 em
`/health` na repetição. `/version` informou
`b5b345d7690c8b543dac44f7929a315925da0911`, anterior à base de preparação.
O [registro bruto](evidencias/dados/publicacao-release2-2026-11-19.json)
preserva a falha transitória inicial de conexão/TLS. Não houve escrita em
produção, e as correções deste fechamento não são declaradas implantadas.

Para concluir a publicação:

1. Revisar por outro integrante e integrar o PR de correções preservando os
   commits; atualizar a base do PR desta documentação para `main` e integrá-lo.
2. Implantar a revisão integrada e conferir o SHA completo em `/version`, a
   versão do frontend e as verificações descritas em
   [verificação da publicação](verificacao-publicacao.md).
3. Atualizar a tag anotada `v2.0.0` e o rascunho para o **commit efetivamente
   publicado**, registrar aqui SHA/data e publicar a GitHub Release. Enquanto
   o rascunho não for publicado, a tag de preparação pode ser atualizada.
4. Repetir a validação da sincronização e registrar as pendências que
   permanecerem. Fechar #102 somente com documento integrado e release final.

Ver também a [Sprint 06](scrum/sprint06.md) e os
[requisitos e evidências](Requisitos.md).
