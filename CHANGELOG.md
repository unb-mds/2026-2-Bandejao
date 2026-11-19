# Changelog do produto

## 2.0.0 — Release 2 (preparada em 19/11/2026)

Conteúdo da versão fonte; a data de publicação e o commit implantado devem
ser conferidos na [nota da release](docs/release-2.md). Preparação não é
comprovação de deploy ou aceite de todos os requisitos.

### Integrado

- Consulta de cardápios por campus e semana, origem PDF, última importação,
  filtros por dieta e marcações de alérgenos.
- Avaliações por refeição com identidade anônima, janela em Brasília,
  atualização de nota e histórico persistido.
- Reclamações com confirmação, sem lista pública, e leitura interna por token.
- Planejamento semanal persistido e estimativa de intenções, com amostra
  mínima de 10 e separação entre registros reais e simulados.
- Importação autenticada, sincronização com isolamento de falhas por campus
  e preservação de avaliações e reclamações na reimportação.
- Testes em SQLite/PostgreSQL 16, concorrência, privacidade, PDFs reais,
  falhas de sincronização e análise estática no CI.

### Corrigido na verificação final

- Semana de segunda a domingo, índices e rótulos coerentes (#112).
- Datas, refeição corrente e prazo de intenção em Brasília, independentemente
  do fuso do dispositivo (#113).
- Atualização de estimativas após marcar/desmarcar, erro visível e remoção de
  contagens antigas ao trocar consulta ou após falha (#114).

### Demonstração

- Gerador explícito de intenções simuladas e remoção seletiva, sem geração
  automática em produção. A amostra simulada é identificada na interface.
- Aba Lotação com exemplos e relatos da sessão, sem medição da fila real.
- Protótipo Vercel externo como referência visual separada.

### Fora do escopo e limites

- Sem login, horário de chegada, tempo de espera, medição de fila,
  cancelamento formal de serviço ou encaminhamento automático de reclamação
  ao RU. Consulta posterior de reclamação pelo autor não implementada.
- Sem relatório k6 que comprove RNF01; sem evidência completa do roteiro em
  celular físico; sem comprovação de RNF04 na janela inteira prevista.
- Dependência do formato/disponibilidade dos PDFs e da configuração externa
  da hospedagem e da sincronização. Ausência de marcação não significa
  ausência do alérgeno.
- Em 19/11, `/version` público ainda informou `b5b345d`, anterior à base
  `17397be` usada nesta preparação. Nenhuma correção foi declarada implantada.

Histórico da documentação em [docs/changelog.md](docs/changelog.md).
