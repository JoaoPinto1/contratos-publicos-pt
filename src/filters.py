"""Filtros do input aplicados a contratos já normalizados."""

from .normalize import fold


def _party_matches(parties, query):
    q = query.strip()
    if q.isdigit():
        return any(p["nif"] == q for p in parties)
    q = fold(q)
    return any(p["name"] and q in fold(p["name"]) for p in parties)


def build_filter(inp):
    """Devolve uma função contrato -> bool. Todos os critérios preenchidos têm de se verificar."""
    terms = fold(inp.get("keywords") or "").split()
    entity = inp.get("contractingEntity")
    contractor = inp.get("contractor")
    cpvs = [c.split("-")[0].strip() for c in inp.get("cpvPrefixes") or [] if c.strip()]
    procedures = [fold(p) for p in inp.get("procedureTypes") or [] if p.strip()]
    date_from, date_to = inp.get("dateFrom"), inp.get("dateTo")
    min_price, max_price = inp.get("minPrice"), inp.get("maxPrice")

    def matches(c):
        if date_from and c["publicationDate"] < date_from:
            return False
        if date_to and c["publicationDate"] > date_to:
            return False
        if min_price is not None and (c["priceEur"] or 0) < min_price:
            return False
        if max_price is not None and (c["priceEur"] or 0) > max_price:
            return False
        if terms:
            text = fold(c["description"])
            if not all(t in text for t in terms):
                return False
        if entity and not _party_matches(c["contractingEntities"], entity):
            return False
        if contractor and not _party_matches(c["contractors"], contractor):
            return False
        if cpvs and not any(x["code"].startswith(p) for x in c["cpv"] for p in cpvs):
            return False
        if procedures and not any(p in fold(c["procedureType"] or "") for p in procedures):
            return False
        return True

    return matches
