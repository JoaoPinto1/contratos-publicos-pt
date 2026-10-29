# ADR-002: Cache semanal partilhada das publicações recentes

## Status
Proposed

## Date
2026-10-29

## Context
O ano de cada ficheiro do IMPIC é o ano do contrato, não o da publicação (ver [fontes-de-dados.md](../fontes-de-dados.md)).
Para apanhar os contratos publicados num dado mês, é preciso ler vários ficheiros anuais.

Hoje o actor lê o ano da pesquisa e os 2 anteriores:
- cobre ~99,3% das publicações; as ~0,7% em falta estão em ficheiros com 3 ou mais anos de atraso;
- cada execução descarrega ~150 MB e analisa ~1 GB de JSON, o que demora ~4,5 min com 1 GB de memória no Apify;
- custa ~$0,015 em plataforma, valor que sai da receita quando o utilizador paga.

Os dumps só mudam uma vez por semana, mas cada execução de cada utilizador repete o mesmo trabalho.

## Decision (proposta)
1. Uma tarefa agendada na conta do autor corre uma vez por semana, depois da atualização do IMPIC (o `last_modified` dos recursos).
2. Essa tarefa lê **todos** os ficheiros anuais.
3. Guarda as publicações dos últimos ~24 meses, já normalizadas, num key-value store com nome e de leitura pública: JSONL comprimido, mais um índice por mês.
4. O actor lê esse ficheiro em vez dos dumps. Se a cache não existir ou estiver desatualizada, volta à leitura direta dos dumps.

## Alternatives Considered

### Manter a leitura direta dos dumps (situação atual)
- Prós: zero infraestrutura e nenhum estado partilhado.
- Contras: execuções de minutos, custo por execução maior que a taxa de arranque, e ~0,7% de publicações em falta.

### Ler todos os ficheiros em cada execução
- Rejeitado: ~15 ficheiros por execução, ~20 min e ~$0,07, só para apanhar 0,7% de publicações.

### Cache por utilizador (key-value store na conta de quem corre o actor)
- Rejeitado: a primeira execução de cada semana pagaria a leitura completa, e o custo multiplica-se pelo número de utilizadores.

## Consequences
- As execuções passam de minutos para segundos e a cobertura chega a ~100% dos últimos 24 meses.
- Passa a haver um custo fixo de ~$0,30/mês na conta do autor (uma leitura completa por semana) e estado partilhado para manter.
- É preciso monitorizar a tarefa semanal: se falhar, o actor tem de voltar sozinho à leitura direta, para nunca devolver dados velhos sem avisar.
- Pesquisas com mais de 24 meses continuam a ler os dumps diretamente.
