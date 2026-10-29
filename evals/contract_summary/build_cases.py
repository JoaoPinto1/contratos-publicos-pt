"""Escolhe os 50 contratos do eval de resumos, a partir dos dumps reais (determinístico: seed fixa).

Uso: .venv/Scripts/python -m evals.contract_summary.build_cases
Escreve cases.jsonl (entrada do runner) e cases.md (para rever os casos).
"""

import json
import random
from pathlib import Path

from src.normalize import normalize
from src.source import dump_urls, iter_rows

HERE = Path(__file__).parent
SEED = 20261029
PUBLISHED_FROM = "2026-07-01"
# Quotas por tipo de procedimento (tags[0]).
QUOTAS = {"ajuste_direto": 12, "concurso_publico": 12, "consulta_previa": 8, "acordo_quadro": 8, "outros": 10}


def group(procedure):
    p = (procedure or "").lower()
    if "acordo-quadro" in p:
        return "acordo_quadro"
    if "ajuste direto" in p:
        return "ajuste_direto"
    if "concurso público" in p:
        return "concurso_publico"
    if "consulta prévia" in p:
        return "consulta_previa"
    return "outros"


def features(c):
    """Características que tornam um resumo difícil; cada uma vira uma tag."""
    price, base = c["priceEur"] or 0, c["basePriceEur"]
    f = {
        "preco<5k": price < 5_000,
        "preco>1M": price > 1_000_000,
        "1_concorrente": len(c["bidders"]) == 1,
        "varios_concorrentes": len(c["bidders"]) >= 3,
        "pessoa_singular": any(p["isLikelyPerson"] for p in c["contractors"]),
        "consorcio": len(c["contractors"]) > 1,
        "acima_do_base": bool(base) and price > base * 1.001,
        "descricao_longa": len(c["description"]) > 400,
        "maiusculas": c["description"].isupper(),
        "lotes": bool(c["lots"]),
        "acordo_quadro": c["frameworkAgreement"] is not None,
        "fechado": c["closeDate"] is not None,
        "estrangeiro": any((p["country"] or "") != "Portugal" for p in c["executionPlaces"]),
    }
    return {k for k, v in f.items() if v}


def main():
    urls = dump_urls()
    pool = {g: [] for g in QUOTAS}
    seen_desc = set()
    for year in (2024, 2025, 2026):
        for row in iter_rows(urls[year]):
            try:
                c = normalize(row)
            except (KeyError, ValueError, TypeError, AttributeError):
                continue
            if c["publicationDate"] < PUBLISHED_FROM or c["description"] in seen_desc:
                continue
            seen_desc.add(c["description"])
            pool[group(c["procedureType"])].append(c)

    rng = random.Random(SEED)
    cases = []
    for g, quota in QUOTAS.items():
        candidates = sorted(pool[g], key=lambda c: c["id"])
        rng.shuffle(candidates)
        candidates = candidates[:5000]
        covered = set()
        for _ in range(quota):
            # Escolha gulosa: o candidato que acrescenta mais características ainda não cobertas neste grupo.
            best = max(candidates, key=lambda c: len(features(c) - covered))
            candidates.remove(best)
            covered |= features(best)
            cases.append((g, best))

    rows = []
    for i, (g, c) in enumerate(cases):
        language = "en" if i % 4 == 3 else "pt"
        rows.append({
            "prompt_id": f"c{i + 1:02d}",
            "tags": [g, language, *sorted(features(c))],
            "language": language,
            "contract": c,
        })

    with open(HERE / "cases.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    write_review(rows)
    print(f"{len(rows)} casos; por grupo: {dict((g, q) for g, q in QUOTAS.items())}")


def write_review(rows):
    lines = ["# Casos do eval de resumos", "",
             f"{len(rows)} contratos publicados desde {PUBLISHED_FROM}, escolhidos por `build_cases.py` (seed {SEED}).", "",
             "| id | grupo | língua | características | preço | descrição |", "|---|---|---|---|---|---|"]
    for r in rows:
        c = r["contract"]
        desc = c["description"][:70].replace("|", "/").replace("\n", " ")
        lines.append(f"| {r['prompt_id']} | {r['tags'][0]} | {r['language']} | {', '.join(r['tags'][2:]) or '—'} "
                     f"| {c['priceEur']:,.2f} € | {desc} |")
    lines.append("")
    for r in rows:
        body = json.dumps(r["contract"], ensure_ascii=False, indent=2)
        fence = "````" if "```" in body else "```"
        lines += [f"## {r['prompt_id']} · {r['tags'][0]} · {r['language']}", "", f"{fence}json", body, fence, ""]
    (HERE / "cases.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
