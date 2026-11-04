# Publicação oficial conferida em 27 de outubro de 2026

Cinco PDFs do Restaurante Universitário da UnB, período 26/10 a 01/11/2026, coletados da página https://ru.unb.br/cardapio-refeitorio/ para regressão offline. A origem e os hashes estão em docs/evidencias/dados/sincronizacao-2026-10-27.json. links.html preserva os cinco destinos observados, incluindo revisões numéricas.

Cada PDF tem um JSON de saída esperada, registrado após a correção JPEG. A regressão detecta mudança de datas, refeições, categorias, dietas, nomes e marcadores em relação a esta linha de base. O arquivo esperado não constitui homologação nutricional ou auditoria manual de todos os ingredientes. Alterações no extrator devem comparar a saída com o PDF antes de atualizar o esperado.
