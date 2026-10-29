# Esquema de saída (MVP)

O dataset do Apify tem um registo por contrato. Os nomes dos campos estão em inglês e são sempre os mesmos.
Quando um valor falta, o campo vem a `null` (nunca `""` ou `0`). A fonte é o dump do IMPIC ([ADR-001](decisions/ADR-001-fonte-de-dados-do-mvp.md)).

## Campos

| Campo | Tipo | Origem no dump | Regra |
|---|---|---|---|
| `id` | string | `idcontrato` | chave única, ver "Deduplicação" |
| `url` | string | — | `https://www.base.gov.pt/Base4/pt/detalhe/?type=contratos&id={id}` (formato a confirmar) |
| `description` | string | `descContrato` | se vier vazio, usar `objectoContrato`; fazer trim |
| `contractTypes` | string[] | `tipoContrato` | |
| `procedureType` | string | `tipoprocedimento` | |
| `contractingEntities` | `Party[]` | `adjudicante` | ver "Partes" |
| `contractors` | `Party[]` | `adjudicatarios` | ver "Partes"; `null` na origem → `[]` |
| `bidders` | `Party[]` | `concorrentes` | parser tolerante, ver "Partes" |
| `priceEur` | number | `precoContratual` | |
| `basePriceEur` | number \| null | `precoBaseProcedimento` | |
| `effectivePriceEur` | number \| null | `PrecoTotalEfetivo` | `0.0` → `null` |
| `publicationDate` | date ISO | `dataPublicacao` | `dd/mm/aaaa` → `aaaa-mm-dd` |
| `signingDate` | date ISO \| null | `dataCelebracaoContrato` | idem |
| `awardDecisionDate` | date ISO \| null | `dataDecisaoAdjudicacao` | idem |
| `closeDate` | date ISO \| null | `dataFechoContrato` | idem |
| `executionDays` | integer \| null | `prazoExecucao` | |
| `executionPlaces` | `{country, district, municipality}[]` | `localExecucao` | dividir `"País, Distrito, Concelho"` por `", "` |
| `nuts` | `{code, name}[]` | `NUTs` | dividir no primeiro `" - "` |
| `cpv` | `{code, description}[]` | `cpv` | dividir no primeiro `" - "` |
| `frameworkAgreement` | `{id, description}` \| null | `numAcordoQuadro`, `DescrAcordoQuadro` | `null` se os dois vierem vazios |
| `announcementNumber` | string \| null | `nAnuncio` | |
| `legalBasis` | string | `fundamentacao` | |
| `awardCriteriaTypes` | string[] | `TipoCriterioAdjudicacao` | juntar os valores dos duplicados |
| `isGreen` | boolean | `ContratEcologico` | `"Sim"` em qualquer duplicado → `true` |
| `isCentralized` | boolean | `ProcedimentoCentralizado` | `"Sim"` → `true` |
| `lots` | string[] | `Lotes` | `null` → `[]` |
| `procedureDocumentsUrl` | string \| null | `linkPecasProc` | |

Campos do dump que ficam de fora no MVP: `idprocedimento`, `idINCM`, `TipoAnuncio`, `regime`, `justifNReducEscrContrato`,
`tipoFimContrato`, `CritMateriais`, `Observacoes`, `Ano` e `fundamentAjusteDireto`.

## Partes (`Party`)

```json
{ "nif": "515615021", "name": "XpertGo - Business Solutions Development, Lda", "isSme": true, "isLikelyPerson": false }
```

- Cada valor vem como `"NIF - Nome"` e divide-se no primeiro `" - "`. Quando o NIF vem como `-`, fica `nif: null`.
- `isSme`: só nos `contractors`; é `true` se o NIF aparece em `adjudicatarioPMEs`.
- **Pessoas singulares (RGPD).** `isLikelyPerson` é `true` quando:
  - o NIF começa por 1, 2, 3 ou 45, **ou**
  - o NIF é `null` e o nome não tem nenhuma forma jurídica (Lda, L.da, S.A., Unipessoal, S.L., S.L.U., GmbH, Ltd, Inc, B.V., S.R.L.,
    Associação, Cooperativa, Fundação, Instituto, Universidade, Município, etc.).

  Quando `isLikelyPerson` é `true`, o `name` passa a `null`. Esta heurística tem de ter testes com casos reais
  (por exemplo `"- - EBSCO Information Services S.L.U."` é uma empresa e `"- - José Teixeira Moreira"` é uma pessoa).
- **`bidders`:** a origem tem pelo menos 6 formatos (`"504615947-1 - MEO ..."`, `"514181435-GROWSKILLS ..."`,
  `"-- Nome"`, `"999999999- Nome"`, `"999999999-999999999"`, …). Os 9 primeiros dígitos são o NIF; um sufixo `-N` a seguir ao NIF deita-se fora; o resto é o nome.
  Se um valor não encaixar em nenhum formato, guarda-se `{nif: null, name: <texto original>}` e conta-se num log.
  Nunca se perde o valor.

## Deduplicação

Por `id`. Os duplicados só diferem em `ContratEcologico` e em `TipoCriterioAdjudicacao`
(ver [fontes-de-dados.md](fontes-de-dados.md)):
- `isGreen` é `true` se qualquer cópia diz `"Sim"`.
- `awardCriteriaTypes` é a lista, sem repetições, de todos os valores das cópias.
- Se algum **outro** campo for diferente entre cópias, fica a primeira cópia e regista-se um aviso no log. Assim percebemos se o export mudou.

## Exemplo

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
