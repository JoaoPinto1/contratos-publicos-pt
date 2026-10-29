# Fontes de dados

Investigado a 29 out 2026. A decisão sobre a fonte está em [ADR-001](decisions/ADR-001-fonte-de-dados-do-mvp.md).

## 1. Dumps IMPIC no dados.gov.pt

Dataset: "Contratos Públicos – Portal Base – IMPIC – Contratos de 2012 a 2026"
- Atualização semanal. Licença `other-pd`. Um ficheiro por ano: `contratos{ano}.zip` (com um JSON lá dentro) ou `.xlsx`.
- Metadados e URLs: `GET https://dados.gov.pt/api/1/datasets/contratos-publicos-portal-base-impic-contratos-de-2012-a-2026/`
  → `resources[].url` e `last_modified`. O URL de cada ficheiro muda a cada publicação, por isso nunca deve estar fixo no código.
- Datasets irmãos com o mesmo formato: Anúncios, Modificações contratuais, Entidades.
- O dataset "OCDS – Portal BASE" está morto: 0 ficheiros e última atualização em 2022.

### `contratos2026.zip` (versão de 25 out 2026)
- O zip tem 47 MB e o `Contratos2026.json` lá dentro tem 356 MB: uma lista de **199 701** objetos, em UTF-8.
- O `dataPublicacao` vai de 2025-12-04 a 2026-10-24, ou seja, o dump está atrasado ~5 dias. São ~20–25 mil contratos por mês.
- `idcontrato` é o mesmo ID do Portal BASE (crescente).
- Há **1 033 linhas extra**, de 1 021 IDs repetidos com até 4 cópias cada. Parecem vir de um join no export: as cópias só diferem em
  `ContratEcologico` (710) e em `TipoCriterioAdjudicacao` (311). Ao deduplicar, os valores destes dois campos juntam-se em vez de se escolher um.

| Campo | Preenchido | Formato / nota |
|---|---|---|
| idcontrato | 100% | string numérica |
| objectoContrato, descContrato | 100% | descrição completa (máx. 2000 chars, média 97) |
| tipoContrato | 100% | lista |
| tipoprocedimento | 100% | top: Ajuste Direto (42%), Concurso público, Consulta Prévia, acordo-quadro |
| adjudicante | 100% | lista de `"NIF - Nome"` |
| adjudicatarios | ~100% | lista de `"NIF - Nome"`; 17 registos têm `null` |
| precoContratual | 100% | número (EUR) |
| dataPublicacao, dataCelebracaoContrato, dataDecisaoAdjudicacao | 100% | `dd/mm/aaaa` |
| cpv | 100% | lista de `"código - descrição"` |
| localExecucao | 100% | lista de `"País, Distrito, Concelho"` |
| prazoExecucao | 99% | dias |
| precoBaseProcedimento | 98% | número |
| adjudicatarioPMEs | 89% | lista de NIFs |
| NUTs | 64% | lista de `"código - nome"` |
| linkPecasProc | 53% | URL da plataforma eletrónica (peças do procedimento) |
| concorrentes | 42% | lista, **formato inconsistente** (ver abaixo) |
| Lotes | 26% | lista |
| nAnuncio, TipoAnuncio, idINCM | 16% | ligação ao anúncio em Diário da República |
| numAcordoQuadro, DescrAcordoQuadro | 17% | |
| dataFechoContrato, PrecoTotalEfetivo, tipoFimContrato | 7% | só para contratos já fechados |

### Dados sujos a tratar
- **NIF ocultado:** em ~12% dos adjudicatários o NIF vem como `-` (`"- - Nome"`), mas **o nome mantém-se**.
  Isto inclui pessoas singulares (médicos, advogados, formadores) e empresas estrangeiras (`EBSCO Information Services S.L.U.`).
- **`concorrentes`** aparece em pelo menos 6 formatos diferentes, por exemplo `"504615947-1 - MEO - ..."`, `"514181435-GROWSKILLS ..."`,
  `"-- Nome"`, `"999999999- Nome"`, `"999999999-999999999"`. Vai ser preciso um parser tolerante e testes com casos reais.
- As datas vêm em `dd/mm/aaaa` e os preços já em número. No endpoint live, pelo contrário, os preços vêm como `"31.804,00 €"` e as datas como `dd-mm-aaaa`.

## 2. Endpoint interno do Portal BASE (live)

`POST https://www.base.gov.pt/Base4/pt/resultados/`, com `Content-Type: application/x-www-form-urlencoded; charset=UTF-8`.

**Pesquisa:** `type=search_contratos`, `version=155.0`, `sort=-publicationDate`, `page=0..`, `size=25`, e `query` com
os campos do formulário url-encoded:
`texto`, `adjudicante`, `adjudicataria` (nome ou NIF), `tipo`, `tipocontrato`, `cpv`,
`desdeprecocontrato`/`ateprecocontrato`, `desdedatacontrato`/`atedatacontrato`,
`desdedatapublicacao`/`atedatapublicacao` (`aaaa-mm-dd`), `pais`, `distrito`, `concelho`.
A resposta é `{"total": N, "items": [...]}` e o `objectBriefDescription` vem truncado a ~200 chars.
Com `size=500` vieram só 20 resultados; o máximo real está por confirmar.

**Detalhe:** `type=detail_contratos`, `version=155.0`, `id=<idcontrato>`. Traz NIFs, `contestants`, CPV,
`documents: [{id, description}]` e `contractingProcedureUrl`.

**Firewall:** depois de ~10 pedidos em poucos minutos, o WebKnight começa a devolver **HTTP 999** com uma página HTML.
- Não existe `robots.txt` e não encontrei uma página de termos de uso. Existe uma política de privacidade.
- O `version` provavelmente muda com cada deploy do site.

## 3. Por confirmar
- O máximo do `size` na pesquisa.
- Quanto tempo dura o bloqueio da firewall: são pelo menos 40 minutos, porque o IP bloqueado por volta das 17:50 ainda estava bloqueado às 18:30, até na página de detalhe.
- O formato do URL de detalhe `/Base4/pt/detalhe/?type=contratos&id=…` (não deu para confirmar por causa do bloqueio).
- Se a firewall bloqueia IPs de datacenter, como os do Apify, logo à primeira.
- O cliente não oficial do GitHub (provavelmente usa o mesmo endpoint).
