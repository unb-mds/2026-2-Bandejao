# Relatório de Auditoria e Divergências — Extração de Cardápios e Alérgenos (RU/UnB)

**Issue Relacionada:** #81  
**Data da Auditoria:** Terça-feira, 10/11/2026  
**Campi Auditados:** Darcy Ribeiro / Ceilândia  
**Módulo Analisado:** `extracao/extracao/main.py`  
**Interface Validada:** Frontend Web (http://localhost:5173) vs. PDFs Oficiais do RU/UnB

---

## 1. Contexto e Objetivo

Este documento registra os resultados da auditoria técnica realizada sobre o sistema de extração automática dos cardápios semanais do Restaurante Universitário (RU) da Universidade de Brasília (UnB). O objetivo é identificar, classificar e documentar as divergências entre as informações nutricionais e de alérgenos publicadas nos documentos PDF oficiais e os dados efetivamente processados e exibidos na aplicação web em **Darcy Ribeiro / Ceilândia**.

---

## 2. Quadro Comparativo: Esperado (PDF Oficial) vs. Exibido no Sistema

A tabela abaixo consolida as inconsistências observadas na grade de terça-feira (10/11/2026) em **Darcy Ribeiro / Ceilândia**, demonstrando que o impacto estrutural é o mesmo nos dois campi:

| Campus | Refeição | Categoria / Dieta | Item / Preparação | Esperado (PDF Oficial) | Exibido no Sistema | Status / Severidade | Diagnóstico da Divergência |
|---|---|---|---|---|---|---|---|
| Darcy Ribeiro / Ceilândia | Café da Manhã | Bebida (Comum) | Leite integral OU Bebida de soja | Leite e derivados, Soja | Leite e derivados, Soja | OK | Extração correta para itens com ícones bem espaçados horizontalmente. |
| Darcy Ribeiro / Ceilândia | Café da Manhã | Panificação (Comum) | Pão francês / careca / integral | Trigo/Glúten (3 ícones repetidos) | Trigo/Glúten (1 ícone consolidado) | OK | Deduplicação correta via `frozenset`. |
| Darcy Ribeiro / Ceilândia | Café da Manhã | Complemento (Ovolacto) | Queijo muçarela | Leite e derivados | Leite + tag Ovolactovegetariano | OK | Tolerância ajustada capturou a célula corretamente. |
| Darcy Ribeiro / Ceilândia | Jantar | Prato Principal (Ovolacto) | Bife de soja ao sugo gratinado | Soja, Leite e derivados | Apenas tag Ovolacto (sem alérgenos) | **Crítico** | Célula densa com múltiplos ícones agrupados; supressão total dos alérgenos. |
| Darcy Ribeiro / Ceilândia | Almoço | Prato Principal (Padrão) | Lasanha à bolonhesa / Gratinados | Trigo/Glúten, Leite e derivados | Apenas o 1º alérgeno ou vazio | **Crítico** | Gargalo na seleção única (`min()`) e falha na leitura de subcolunas complexas do Almoço. |
| Darcy Ribeiro / Ceilândia | Almoço | Guarnição (Comum) | Purê de batata com manteiga | Leite e derivados | Ausente (sem ícone) | **Crítico** | Ícones posicionados na divisória da subcoluna de guarnições descartados pelo parser. |
| Darcy Ribeiro / Ceilândia | Jantar | Sopa / Caldo (Comum) | Sopa de macarrão com legumes | Trigo/Glúten, Soja (tempero) | Ausente na interface | **Crítico** | Páginas de jantar de Darcy Ribeiro / Ceilândia sofrem do mesmo desalinhamento vertical nas linhas finais. |
| Darcy Ribeiro / Ceilândia | Almoço / Jantar | Geral (Múltiplas categorias) | Pratos compostos diversos | Todos os ícones da legenda | Alérgenos ausentes na interface | **Crítico** | Diferença estrutural sistêmica entre a grade da Página 1 (Café) e das Páginas 2/3 (Almoço/Jantar). |

---

## 3. Análise Técnica das Causas Raiz (`extracao/extracao/main.py`)

A investigação do pipeline de extração (pdfplumber + Pillow) revelou quatro causas principais que afetam identicamente **Darcy Ribeiro / Ceilândia**:

### 3.1. Desalinhamento de Subcolunas no Almoço e Jantar (`estruturar_tabela`)

- **O Problema:** Nas páginas de almoço e jantar de **Darcy Ribeiro / Ceilândia**, o layout do PDF utiliza estruturas de colunas e subcolunas mais densas que o café da manhã. A lógica de fallback (`coluna_valor = coluna - 1`) falha na correspondência exata.
- **Consequência:** O dicionário `alergenos_por_celula` indexa os ícones usando coordenadas que divergem da consulta em `estruturar_tabela`, retornando conjuntos vazios (`frozenset()`).

### 3.2. Rigidez na Detecção Geográfica de Ícones (`_alergenos_por_celula`)

- **O Problema:** A associação entre imagem e célula verifica estritamente se o centro geométrico do ícone (`centro_x`, `centro_y`) está dentro dos limites exatos da caixa.
- **Consequência:** Ícones nas margens (comum em pratos compostos de **Darcy Ribeiro / Ceilândia**) são ignorados.

### 3.3. Gargalo da Seleção Única (`min()`)

- **O Problema:** O algoritmo selecionava apenas a assinatura visual com a menor distância de Hamming por imagem, com corte rígido (`LIMIAR_DISTANCIA_ICONE = 25`).
- **Consequência:** Variações de renderização nos PDFs de **Darcy Ribeiro / Ceilândia** elevam a distância acima de 25, descartando ícones válidos.

### 3.4. Células Mescladas e Densidade Gráfica

- **O Problema:** Pratos principais elaborados em **Darcy Ribeiro / Ceilândia** geram aglomeração de ícones de alérgenos, confundindo o isolamento de bounding boxes.

---

## 4. Recomendações e Próximos Passos

1. **Alinhamento de Coordenadas:** Mapear ícones por interseção de área (bounding box) com a coluna da data correspondente em **Darcy Ribeiro / Ceilândia**.
2. **Margem de Tolerância (`MARGEM_TOLERANCIA`):** Expandir os limites em 6px a 8px para capturar ícones nas bordas.
3. **Calibração Visual:** Ajustar o limiar para lidar com variações de compressão nos PDFs de **Darcy Ribeiro / Ceilândia**.
4. **Testes Automatizados:** Adicionar fixtures de regressão para validar que o processamento em **Darcy Ribeiro / Ceilândia** retorna os conjuntos completos.