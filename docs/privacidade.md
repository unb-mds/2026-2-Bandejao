# Aviso de privacidade

O Bandejão exibe o aviso abaixo na primeira visita ao frontend. O botão **Privacidade**, no rodapé, permite reler o mesmo conteúdo a qualquer momento.

## Texto apresentado na interface

**Sua privacidade no Bandejão**

Para avaliar ou reclamar, não pedimos nome nem e-mail. Um código anônimo aleatório vincula seus envios e fica salvo neste navegador. Se o armazenamento estiver bloqueado, o código vale só enquanto a página estiver aberta.

Ao limpar os dados do site e abrir novamente, outro código será gerado no próximo envio. Isso não apaga os registros já enviados.

Notas, comentários e reclamações são salvos na API. Comentários das avaliações aparecem no histórico público. Reclamações não têm lista pública nem encaminhamento automático ao RU. Evite informar dados pessoais nos textos.

“Entendi” registra apenas que você leu este aviso neste navegador. Você pode reler em **Privacidade**, no rodapé.

## Funcionamento e limites

- O código é um UUID v4 aleatório criado ao enviar uma avaliação ou reclamação e armazenado em `localStorage`, na chave `bandejao.identidade`. O frontend não exige cadastro, nome ou e-mail nesses envios. Os campos de texto livre podem conter dados pessoais inseridos pelo próprio usuário; o código não torna esse conteúdo anônimo por si só.
- Notas, comentários, categorias e descrições de reclamações são persistidos no backend e vinculados ao código. O histórico público de avaliações inclui comentários. Não há lista pública de reclamações nem envio automático ao restaurante.
- Limpar os dados do navegador remove a cópia local do código e a confirmação de leitura. Após reabrir a página, o próximo envio gera outro código; registros já persistidos no backend não são excluídos por essa ação. Enquanto a página está aberta, o código já carregado pode continuar em memória.
- **Entendi** grava `lido` em `bandejao.privacidade.v1`. É uma confirmação de leitura, sem representar consentimento para coleta nem uma declaração de conformidade legal. Mudanças que exijam nova leitura devem incrementar a versão da chave.
- Se o armazenamento estiver indisponível ou a gravação falhar, a confirmação vale em memória enquanto a página permanecer aberta. É possível fechar o aviso e usar a aplicação; recarregar pode exibi-lo novamente. O código de identidade também tem alternativa em memória.
- O diálogo nativo permite navegação por teclado, mantém o foco dentro do aviso enquanto está aberto e devolve o foco ao botão do rodapé ao fechar uma releitura. Na primeira exibição, o foco segue para o conteúdo principal após fechar. **Escape** fecha sem registrar a leitura; a próxima visita volta a exibir o aviso se não houver confirmação salva.

Os testes unitários do frontend cobrem a primeira visita, a confirmação da versão atual, valores antigos ou inválidos, a remoção dos dados locais e falhas de armazenamento. O comportamento de foco e teclado deve ser verificado em navegador real.

## Verificação da entrega da issue 53

Em 27/10/2026, os 27 testes do frontend, o lint, TypeScript e o build Vite passaram. A revisão do código não encontrou defeitos bloqueantes. No Chrome foram conferidos primeira visita, teclado/foco no diálogo, confirmação persistida, recarga sem repetição, releitura pelo rodapé, Escape com retorno de foco, limpeza dos dados e armazenamento bloqueado. O aviso foi visto em desktop e em tela de 390 pixels, sem overflow horizontal e sem erros JavaScript observados.

A API foi simulada com listas vazias durante essa verificação do aviso; não houve envio de avaliações ou reclamações. A evidência não comprova a operação do backend publicado.

- [Registro dos cenários](evidencias/dados/privacidade-2026-10-27.json).
- [Captura desktop](evidencias/capturas/privacidade-desktop.png).
- [Captura mobile](evidencias/capturas/privacidade-mobile.png).
