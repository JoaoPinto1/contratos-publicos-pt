# Contratos Públicos PT

Um actor do Apify que pesquisa os contratos públicos portugueses do Portal BASE e devolve dados limpos.
Mais tarde vai também gerar resumos por LLM e funcionar como MCP server.

Estado: MVP publicado na Apify Store em [apify.com/joaopinto/contratos-publicos-pt](https://apify.com/joaopinto/contratos-publicos-pt),
com pay-per-event: $0.003 por contrato e $0.02 por GB no arranque.
O arranque cobre o custo de plataforma de uma execução (~$0.014 a ler 3 ficheiros), para não perder dinheiro em execuções com poucos resultados. Publicar uma versão nova: `apify push`.

## Como funciona
Em cada execução, o actor:
1. Descarrega os dumps semanais do IMPIC (dados.gov.pt): o ano da pesquisa e os 2 anteriores, porque muitos contratos são publicados anos depois.
2. Lê o ficheiro em streaming, normaliza e filtra cada contrato.
3. Deduplica e guarda os resultados no dataset.

Com `onlyNew`, guarda o último `id` devolvido num key-value store com nome, um marcador para cada combinação de filtros.
Uma execução que lê 3 ficheiros demora ~1 min localmente e ~4–5 min no Apify com 1 GB, e usa ~75 MB de memória.
Erros de rede são repetidos com backoff, e as linhas mal formadas do dump são ignoradas e contadas no log.
Os dados chegam com até ~7 dias de atraso.

## Comandos
```bash
uv venv .venv && uv pip install --python .venv -r requirements.txt pytest
.venv/Scripts/python -m pytest          # testes
.venv/Scripts/python -m src             # execução local; o input vai em storage/key_value_stores/default/INPUT.json
```

## Documentação
- [Fontes de dados](docs/fontes-de-dados.md): os dumps do IMPIC e o endpoint interno do BASE
- [ADR-001](docs/decisions/ADR-001-fonte-de-dados-do-mvp.md): a fonte do MVP
- [ADR-002](docs/decisions/ADR-002-cache-semanal-partilhada.md): proposta de cache semanal partilhada
- [Esquema de saída](docs/esquema-de-saida.md): os campos de cada contrato e as regras de normalização
- [Eval dos resumos por LLM](docs/evals-resumos.md): Haiku vs Opus em 50 contratos, juiz, calibração e próximos passos
