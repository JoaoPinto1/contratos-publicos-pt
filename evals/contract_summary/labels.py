"""Calibração do juiz contra etiquetas humanas.

  .venv/Scripts/python -m evals.contract_summary.labels make  [--flow contract_summary_cc] [--n 20]
      escreve labels.md: N resumos às cegas (sem modelo nem nota do juiz), para preencher com s/n
  .venv/Scripts/python -m evals.contract_summary.labels score [--flow contract_summary_cc]
      compara as tuas etiquetas com as do juiz e mostra a concordância por critério
"""

import argparse
import json
import random
import re
from pathlib import Path

from evals.contract_summary.graders import CRITERIA
from src.summarize import notable_points

HILL = Path(__file__).resolve().parents[2] / ".claude" / "hillclimb"
CASES = {c["prompt_id"]: c for c in map(json.loads, open(Path(__file__).parent / "cases.jsonl", encoding="utf-8"))}
SEED = 7


def load_rows(flow):
    rows = []
    for variant in sorted(p.name for p in (HILL / flow).iterdir() if re.fullmatch(r"baseline|v\d+", p.name)):
        for r in map(json.loads, open(HILL / flow / variant / "results.jsonl", encoding="utf-8")):
            if r["status"] == "ok":
                trace = json.load(open(HILL / flow / variant / "traces" / f"{r['prompt_id']}_rep{r['rep']}.json",
                                       encoding="utf-8"))
                rows.append({**r, "variant": variant, "summary": trace[2]["content"]})
    return rows


def make(flow, n):
    rows = load_rows(flow)
    rng = random.Random(SEED)
    failed = [r for r in rows if not all(r["grade"][k] for k in CRITERIA)]
    passed = [r for r in rows if r not in failed]
    rng.shuffle(failed)
    rng.shuffle(passed)
    picked = failed[: n // 2] + passed[: n - min(len(failed), n // 2)]
    rng.shuffle(picked)  # a ordem não revela quais o juiz reprovou

    key, out = [], ["# Etiquetas humanas para calibrar o juiz", "",
                    "Para cada resumo, substitui cada `?` por `s` (cumpre) ou `n` (não cumpre). Critérios:", ""]
    out += [f"- **{k}**: {v}" for k, v in CRITERIA.items()]
    out.append("")
    for i, r in enumerate(picked, 1):
        c = CASES[r["prompt_id"]]["contract"]
        key.append({"label_id": i, "variant": r["variant"], "prompt_id": r["prompt_id"]})
        parties = lambda ps: "; ".join(f"{p['name'] or '(particular)'} [{p['nif'] or '-'}]" for p in ps) or "—"
        out += [f"## L{i:02d} · caso {r['prompt_id']} · língua {r['meta']['language']}", "",
                f"- **Descrição:** {c['description']}",
                f"- **Adjudicante:** {parties(c['contractingEntities'])}",
                f"- **Adjudicatário(s):** {parties(c['contractors'])}",
                f"- **Preço:** {c['priceEur']} € (base: {c['basePriceEur']}) · **Procedimento:** {c['procedureType']}",
                f"- **Destaques calculados:** {'; '.join(notable_points(c)) or 'nenhum'}",
                f"- Dados completos: `cases.md`, secção {r['prompt_id']}", "",
                "**Resumo:**", "", "> " + r["summary"].replace("\n", "\n> "), "",
                " ".join(f"{k}: ?" for k in CRITERIA), ""]
    (HILL / flow / "labels.md").write_text("\n".join(out), encoding="utf-8")
    (HILL / flow / "labels_key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    print(f"{len(picked)} resumos em {HILL / flow / 'labels.md'} ({min(len(failed), n // 2)} reprovados pelo juiz)")


def score(flow):
    text = (HILL / flow / "labels.md").read_text(encoding="utf-8")
    key = {k["label_id"]: k for k in json.load(open(HILL / flow / "labels_key.json", encoding="utf-8"))}
    judged = {(r["variant"], r["prompt_id"]): r for r in load_rows(flow)}
    agree = {k: [0, 0] for k in CRITERIA}
    disagreements = []
    for block in re.split(r"^## L", text, flags=re.M)[1:]:
        i = int(block[:2])
        r = judged[(key[i]["variant"], key[i]["prompt_id"])]
        for k in CRITERIA:
            m = re.search(rf"\b{k}:\s*([sSnN?])", block)
            if not m or m.group(1) == "?":
                continue
            human = m.group(1).lower() == "s"
            agree[k][1] += 1
            if human == bool(r["grade"][k]):
                agree[k][0] += 1
            else:
                disagreements.append(f"L{i:02d} {k}: tu={'s' if human else 'n'}, juiz={'s' if r['grade'][k] else 'n'}"
                                     f" — {r['explanation'][k]}")
    for k, (a, t) in agree.items():
        print(f"  {k:9s} {a}/{t} concordância" + (f" ({100 * a / t:.0f}%)" if t else ""))
    for d in disagreements:
        print("  ", d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["make", "score"])
    ap.add_argument("--flow", default="contract_summary_cc")
    ap.add_argument("--n", type=int, default=20)
    args = ap.parse_args()
    make(args.flow, args.n) if args.cmd == "make" else score(args.flow)


if __name__ == "__main__":
    main()
