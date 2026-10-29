# ADR-001: Dumps semanais do IMPIC como fonte do MVP

## Status
Accepted (29 out 2026). O MVP é sobre **contratos** celebrados; os anúncios ficam para depois.

## Date
2026-10-29

## Context
O actor tem de pesquisar contratos públicos portugueses por palavras-chave, entidades, NIF, CPV, datas, preço e tipo de procedimento.
Também tem de ter um modo incremental, para quem o agenda todos os dias.
As fontes possíveis estão descritas em [fontes-de-dados.md](../fontes-de-dados.md). Para esta decisão contam três coisas:
- O endpoint interno do BASE suporta todos os filtros, mas não é documentado, tem uma firewall que bloqueia ao fim de ~10 pedidos e não tem termos de uso publicados.
- Os dumps do IMPIC têm licença aberta, são semanais, chegam com ~5 dias de atraso e trazem campos mais ricos do que a listagem do endpoint (descrição completa, concorrentes, NUTs, PME).
- No Apify, o actor corre a partir de IPs de datacenter.

## Decision
O MVP lê o dump anual do IMPIC (`contratos{ano}.zip`), deduplica por `idcontrato`, aplica os filtros em memória
e, no modo incremental, emite só os contratos com `idcontrato` maior do que o último já visto.
O URL do dump é obtido em cada execução pela API de metadados do dados.gov.pt.

## Alternatives Considered

### Endpoint interno do BASE como fonte principal
- Prós: dados do próprio dia e filtros feitos no servidor.
- Contras: a firewall bloqueia ao fim de ~10 pedidos; precisaria de um proxy pago e de um ritmo de pedidos baixo. O endpoint não é documentado e o campo `version` muda com os deploys do site. A recolha automatizada pode não ser permitida.
- Rejeitado para o MVP. Pode voltar na v1.1, só para o detalhe de cada contrato (documentos), com poucos pedidos.

### Dataset OCDS no dados.gov.pt
- Rejeitado: não tem ficheiros e não é atualizado desde 2022.

## Consequences
- Resolve de uma vez os riscos de "termos de uso" e de "mudanças no site" do plano.
- O atraso de até ~7 dias tem de ser explicado no README do actor. Para contratos já celebrados, isso é aceitável.
- Cada execução descarrega ~50 MB e processa ~360 MB de JSON, o que custa memória e tempo no Apify. Ainda falta medir quanto.
- Os pedidos de anos anteriores precisam de mais do que um ficheiro, ou seja, várias descargas.
- Os anúncios têm um dump com o mesmo formato, por isso, quando entrarem no actor, esta decisão aplica-se também a eles.
