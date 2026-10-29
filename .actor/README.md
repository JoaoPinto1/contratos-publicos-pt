# Portugal Public Contracts (Portal BASE)

Search every public contract signed in Portugal and get clean, structured data: who bought what, from whom, for how much, and through which procedure.

The data covers all contracts that Portuguese public entities report to [Portal BASE](https://www.base.gov.pt) under the Public Contracts Code (Código dos Contratos Públicos). That's about 20–25 thousand new contracts a month.

*Em português: ver mais abaixo.*

## What you can do with it

- **Competitive intelligence:** see which contracts your competitors win, at what prices, and from which buyers.
- **Find buyers:** which municipalities, hospitals or universities buy what you sell, and how often.
- **Journalism and research:** follow how a public body spends money, or find repeated direct awards to the same supplier.
- **Daily monitoring:** schedule the actor with **Só contratos novos** (`onlyNew`) to get only the contracts published since the last run.
- **AI agents:** the output has fixed English field names and typed values, so you can use it directly in an LLM pipeline.

## Input

All filters are optional, and any filters you set must all match. The input form shows the field titles in Portuguese; the API name of each field is in brackets.

| Field | Example | Notes |
|---|---|---|
| Palavras-chave (`keywords`) | `software licenças` | Every word must appear in the contract description. Not case or accent sensitive. |
| Entidade adjudicante (`contractingEntity`) | `Reforma Tecnológica` or `508184509` | Part of the buyer's name, or its 9-digit NIF (tax number) |
| Adjudicatário (`contractor`) | `Claranet` or `510728189` | Part of the supplier's name, or its NIF |
| Códigos CPV (`cpvPrefixes`) | `48`, `72` | CPV code prefixes: `48` = software, `72` = IT services |
| Tipos de procedimento (`procedureTypes`) | `Concurso público` | For example `Ajuste direto` (direct award) or `Consulta prévia` |
| Publicado desde / até (`dateFrom`, `dateTo`) | `2026-01-01` | Publication date on BASE. By default, the last 30 days. |
| Preço mínimo / máximo (`minPrice`, `maxPrice`) | `10000` | Contract price in euros |
| Só contratos novos (`onlyNew`) | `true` | Returns only contracts not returned by a previous run with the same filters |
| Máximo de contratos (`maxItems`) | `1000` | Upper limit per run |

Example, IT contracts over €50,000 awarded by Lisbon entities this year:

```json
{
  "contractingEntity": "Lisboa",
  "cpvPrefixes": ["48", "72"],
  "minPrice": 50000,
  "dateFrom": "2026-01-01"
}
```

## Output

One item per contract. You can export it to JSON, CSV or Excel.

```json
{
  "id": "12014814",
  "url": "https://www.base.gov.pt/Base4/pt/detalhe/?type=contratos&id=12014814",
  "description": "Aquisição de serviços para obtenção de Selo de Usabilidade e Acessibilidade Digital Ouro na Página/Portal/App SASocial",
  "contractTypes": ["Aquisição de serviços"],
  "procedureType": "Ajuste Direto Regime Geral",
  "contractingEntities": [{ "nif": "600052737", "name": "Serviços de Ação Social do Instituto Politécnico de Coimbra", "isSme": null, "isLikelyPerson": false }],
  "contractors": [{ "nif": "515615021", "name": "XpertGo - Business Solutions Development, Lda", "isSme": true, "isLikelyPerson": false }],
  "bidders": [],
  "priceEur": 9000.0,
  "basePriceEur": 9000.0,
  "effectivePriceEur": null,
  "publicationDate": "2025-12-04",
  "signingDate": "2026-02-23",
  "awardDecisionDate": "2025-11-13",
  "closeDate": null,
  "executionDays": 81,
  "executionPlaces": [{ "country": "Portugal", "district": "Coimbra", "municipality": "Coimbra" }],
  "nuts": [],
  "cpv": [{ "code": "72210000-0", "description": "Serviços de programação de pacotes de software" }],
  "frameworkAgreement": null,
  "announcementNumber": null,
  "legalBasis": "Artigo 20.º, n.º 1, alínea d) do Código dos Contratos Públicos",
  "awardCriteriaTypes": ["Monofator"],
  "isGreen": false,
  "isCentralized": false,
  "lots": [],
  "procedureDocumentsUrl": null
}
```

- Dates use the ISO format (`YYYY-MM-DD`) and prices are numbers in euros.
- Missing values are always `null` or `[]`, never empty strings.
- `bidders` lists the companies that took part in the procedure, when the source includes them (about 40% of contracts).

## Data source and freshness

The actor reads the **open data that IMPIC publishes weekly** on [dados.gov.pt](https://dados.gov.pt/datasets/contratos-publicos-portal-base-impic-contratos-de-2012-a-2026). It does not scrape the BASE website. This makes it reliable, and polite to the public servers.

As a result, **the newest contracts arrive with a delay of up to about a week**. That delay comes from the source. For contracts that are already signed, it rarely matters.

This actor is not affiliated with IMPIC or Portal BASE.

## Privacy

Some contractors are private individuals, such as doctors, lawyers or trainers hired directly. The source already hides their NIF but still includes their name.

This actor goes further: when a contractor or bidder looks like a private individual, the actor **removes the name** and sets `isLikelyPerson: true`. The check uses the NIF prefix, or the absence of a legal form (Lda, S.A., etc.) in the name.

## Pricing

You pay per contract returned (see the **Pricing** tab). Use **Máximo de contratos** (`maxItems`) to cap the cost of each run.

A typical run takes 1–2 minutes and reads a full year of data.

## Limitations

- Contracts only. Open tenders (anúncios) are not included yet.
- Search works on the contract description, which is the text the public entity wrote. Search for the words they would use, in Portuguese.
- `isLikelyPerson` is a heuristic. In rare cases a company with an unusual name is hidden, or the reverse.

---

## Em português

Pesquise todos os contratos públicos celebrados em Portugal, publicados no Portal BASE, e receba dados limpos e estruturados: quem comprou o quê, a quem, por quanto e com que procedimento.

- **Filtros:** palavras-chave na descrição (sem distinguir maiúsculas nem acentos); entidade adjudicante e adjudicatário, por nome ou NIF; prefixos CPV; tipo de procedimento; datas de publicação; e preço.
- **Agendamento:** com **Só contratos novos**, cada execução devolve apenas os contratos publicados desde a anterior. Útil para alertas diários sobre concorrentes ou clientes.
- **Fonte:** os dados abertos que o IMPIC publica todas as semanas no dados.gov.pt. Por isso os contratos mais recentes chegam com até ~1 semana de atraso.
- **Privacidade:** o nome dos adjudicatários que são pessoas singulares é removido.
- **Preço:** paga por contrato devolvido. O campo **Máximo de contratos** limita o custo de cada execução.

Este actor não tem qualquer ligação ao IMPIC nem ao Portal BASE.
