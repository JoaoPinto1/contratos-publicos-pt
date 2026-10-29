"""Converte linhas do dump IMPIC para o esquema de saída (docs/esquema-de-saida.md)."""

import re
import unicodedata
from datetime import datetime

BASE_DETAIL_URL = "https://www.base.gov.pt/Base4/pt/detalhe/?type=contratos&id={}"

# Formas jurídicas que não se confundem com nomes de pessoas: comparadas sem acentos nem pontos.
LEGAL_WORDS = {
    "lda", "limitada", "unipessoal", "slu", "srl", "spa", "sarl", "sas", "gmbh", "ltd", "limited", "inc", "llc",
    "plc", "corp", "bv", "crl", "ace", "epe", "eem", "ipss", "associacao", "cooperativa", "fundacao", "instituto",
    "universidade", "municipio", "camara", "freguesia", "sociedade", "companhia", "agrupamento", "hospital",
    "escola", "misericordia", "federacao", "sindicato", "clube", "centro",
}
# Formas curtas ("SA", "SL") também são apelidos ("Sá"); só contam escritas com pontos ou depois de vírgula.
SHORT_FORM = re.compile(r"\bS\.\s?[AL]\.?(?=\W|$)|,\s*S\.?\s?[AL]\.?\s*$", re.IGNORECASE)
BIDDER = re.compile(r"^\s*(\d{9})?\s*(?:-\s*\d(?!\d))?[\s-]*(.*?)\s*$", re.DOTALL)


def fold(text):
    """Minúsculas e sem acentos, para comparar texto em português."""
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()


def is_likely_person(nif, name):
    if nif:
        return nif[0] in "123" or nif.startswith("45")
    if not name:
        return False
    words = set(re.findall(r"[a-z0-9]+", fold(name).replace(".", "")))
    return not (words & LEGAL_WORDS or SHORT_FORM.search(name))


def party(nif, name, smes=None):
    nif = nif if nif and nif.isdigit() else None
    name = (name or "").strip() or None
    person = is_likely_person(nif, name)
    return {
        "nif": nif,
        "name": None if person else name,
        "isSme": (nif in smes) if smes is not None and nif else None,
        "isLikelyPerson": person,
    }


def parse_party(raw, smes=None):
    """`"NIF - Nome"`; o NIF pode vir como `-`."""
    nif, _, name = raw.partition(" - ")
    return party(nif.strip(), name, smes)


def parse_bidder(raw):
    """`concorrentes` vem em vários formatos; o que não for NIF fica como nome."""
    m = BIDDER.match(raw)
    return party(m.group(1), m.group(2))


def iso_date(value):
    return datetime.strptime(value, "%d/%m/%Y").date().isoformat() if value else None


def _pairs(values):
    out = []
    for v in values or []:
        code, _, desc = v.partition(" - ")
        out.append((code.strip(), desc.strip() or None))
    return out


def _place(value):
    parts = [p.strip() or None for p in value.split(",")] + [None, None, None]
    return {"country": parts[0], "district": parts[1], "municipality": parts[2]}


def normalize(row):
    smes = set(row.get("adjudicatarioPMEs") or [])
    fa_id, fa_desc = row.get("numAcordoQuadro") or None, row.get("DescrAcordoQuadro") or None
    criteria = row.get("TipoCriterioAdjudicacao")
    return {
        "id": str(row["idcontrato"]),
        "url": BASE_DETAIL_URL.format(row["idcontrato"]),
        "description": (row.get("descContrato") or row.get("objectoContrato") or "").strip(),
        "contractTypes": row.get("tipoContrato") or [],
        "procedureType": row.get("tipoprocedimento"),
        "contractingEntities": [parse_party(p) for p in row.get("adjudicante") or []],
        "contractors": [parse_party(p, smes) for p in row.get("adjudicatarios") or []],
        "bidders": [parse_bidder(p) for p in row.get("concorrentes") or []],
        "priceEur": row.get("precoContratual"),
        "basePriceEur": row.get("precoBaseProcedimento") or None,
        "effectivePriceEur": row.get("PrecoTotalEfetivo") or None,
        "publicationDate": iso_date(row.get("dataPublicacao")),
        "signingDate": iso_date(row.get("dataCelebracaoContrato")),
        "awardDecisionDate": iso_date(row.get("dataDecisaoAdjudicacao")),
        "closeDate": iso_date(row.get("dataFechoContrato")),
        "executionDays": row.get("prazoExecucao"),
        "executionPlaces": [_place(p) for p in row.get("localExecucao") or []],
        "nuts": [{"code": c, "name": d} for c, d in _pairs(row.get("NUTs"))],
        "cpv": [{"code": c, "description": d} for c, d in _pairs(row.get("cpv"))],
        "frameworkAgreement": {"id": fa_id, "description": fa_desc} if fa_id or fa_desc else None,
        "announcementNumber": row.get("nAnuncio") or None,
        "legalBasis": row.get("fundamentacao") or None,
        "awardCriteriaTypes": [criteria] if criteria else [],
        "isGreen": row.get("ContratEcologico") == "Sim",
        "isCentralized": row.get("ProcedimentoCentralizado") == "Sim",
        "lots": row.get("Lotes") or [],
        "procedureDocumentsUrl": row.get("linkPecasProc") or None,
    }


MERGED_FIELDS = ("isGreen", "awardCriteriaTypes")


def merge_duplicate(kept, other):
    """Junta uma cópia repetida (mesmo id). Devolve False se diferir noutro campo além dos esperados."""
    kept["isGreen"] = kept["isGreen"] or other["isGreen"]
    kept["awardCriteriaTypes"] += [c for c in other["awardCriteriaTypes"] if c not in kept["awardCriteriaTypes"]]
    return all(kept[k] == other[k] for k in kept if k not in MERGED_FIELDS)
