"""Runner do eval de resumos. Chama o mesmo `summarize` que o actor usa e grava no formato do relatório.

Uso (a partir da raiz do projeto, com ANTHROPIC_API_KEY definida):
  .venv/Scripts/python -m evals.contract_summary.run --variant baseline --model claude-haiku-5-5 --limit 5
  .venv/Scripts/python -m evals.contract_summary.run --variant v1 --model claude-opus-5-5
Na primeira execução, ou depois de mudar o runner/graders/prompt, é preciso aprovar com --approve-harness.
"""

import argparse
import hashlib
import json
import math
import random
import re
import shutil
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace

import anthropic

from evals.contract_summary.claude_code_client import ClaudeCodeClient, ClaudeCodeRateLimit
from evals.contract_summary.graders import JUDGE_MODEL, check_facts, judge, judge_prompt, JUDGE_SYSTEM
from src.summarize import SYSTEM, SummaryError, build_user_message, notable_points, summarize

ROOT = Path(__file__).resolve().parents[2]
FLOW = ROOT / ".claude" / "hillclimb" / "contract_summary"
# Resultados via subscrição (claude -p) ficam noutra pasta: nunca se misturam com os números da API.
FLOW_CC = FLOW.parent / "contract_summary_cc"
CASES = Path(__file__).parent / "cases.jsonl"
# $/1M tokens (input, output), da tabela de preços da API (out 2026); cache: escrita 1.25x, leitura 0.1x do input.
PRICES = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.00, 10.00), "claude-opus-5-5": (4.00, 20.00)}
RETRIABLE = (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APIConnectionError,
             anthropic.APITimeoutError, ClaudeCodeRateLimit)
lock = threading.Lock()


def harness_sha():
    state = json.loads((FLOW / "_state.json").read_text(encoding="utf-8"))
    h = hashlib.sha256()
    for rel in state["harness_paths"]:
        h.update(rel.encode())
        h.update((ROOT / rel).read_bytes())
    return h.hexdigest()


def usage_dict(u):
    return {"input_tokens": u.input_tokens, "output_tokens": u.output_tokens,
            "cache_read_input_tokens": u.cache_read_input_tokens or 0,
            "cache_creation_input_tokens": u.cache_creation_input_tokens or 0}


def cost(model, u):
    pin, pout = next(p for m, p in PRICES.items() if model.startswith(m))
    return (u["input_tokens"] * pin + u["output_tokens"] * pout + u["cache_read_input_tokens"] * pin * 0.1
            + u["cache_creation_input_tokens"] * pin * 1.25) / 1e6


def with_retries(fn, deadline):
    """Repete erros transitórios com backoff e jitter até ao prazo do caso; devolve (resultado, tentativas)."""
    attempt = 0
    while True:
        try:
            return fn(), attempt
        except RETRIABLE:
            attempt += 1
            delay = min(30, 2 ** attempt) * random.uniform(0.5, 1.5)
            if attempt >= 5 or time.monotonic() + delay > deadline:
                raise
            time.sleep(delay)


def append(path, row):
    with lock, open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def reused(reuse_dir, prompt_id, rep):
    """Resumo já gerado noutra corrida, para re-avaliar só com um juiz novo (o resumo fica igual)."""
    old = next(r for r in map(json.loads, open(reuse_dir / "results.jsonl", encoding="utf-8"))
               if r["prompt_id"] == prompt_id and r["rep"] == rep)
    trace = json.load(open(reuse_dir / "traces" / f"{prompt_id}_rep{rep}.json", encoding="utf-8"))
    resp = SimpleNamespace(model=old["model"], stop_reason=old["stop_reason"],
                           usage=SimpleNamespace(**old["usage"]))
    return old, (trace[2]["content"] if old["status"] == "ok" else ""), resp, trace[:3]


def run_case(client, case, rep, model, variant_dir, timeout_s, reuse_dir=None):
    c, language = case["contract"], case["language"]
    key = {"prompt_id": case["prompt_id"], "rep": rep}
    deadline = time.monotonic() + timeout_s
    t0 = time.monotonic()
    old_trace = None
    if reuse_dir:
        old, summary, resp, old_trace = reused(reuse_dir, case["prompt_id"], rep)
        status, stop, retries, latency = old["status"], old["stop_reason"], old["retries"], old["latency_s"]
    else:
        try:
            (summary, resp), retries = with_retries(lambda: summarize(client, c, language, model), deadline)
            latency = time.monotonic() - t0
            if not resp.model.startswith(model):
                raise RuntimeError(f"served model {resp.model} != requested {model}")
            status, stop = "ok", resp.stop_reason
        except SummaryError as e:
            # Recusa ou corte: resultado graduável, não erro de infraestrutura.
            resp, summary, retries, latency = e.response, "", 0, time.monotonic() - t0
            status, stop = ("truncated" if e.response.stop_reason == "max_tokens" else "refused"), e.response.stop_reason
        except Exception as e:  # infra: vai para errors.jsonl, nunca para results.jsonl
            append(variant_dir / "errors.jsonl", {**key, "failure_class": type(e).__name__, "error": str(e)[:500]})
            return

    notable = notable_points(c)
    facts_ok, facts_problems = check_facts(summary, c, language)
    if status == "ok":
        try:
            (crit, reasons, jresp), _ = with_retries(lambda: judge(client, c, notable, language, summary), deadline)
        except Exception as e:
            append(variant_dir / "errors.jsonl", {**key, "failure_class": "grader_" + type(e).__name__,
                                                   "error": str(e)[:500], "model": resp.model,
                                                   "usage": usage_dict(resp.usage)})
            return
        judge_usage = usage_dict(jresp.usage)
    else:
        crit = {k: False for k in ("faithful", "core", "notable", "clear")}
        reasons, judge_usage = {k: status for k in crit}, None

    grade = {"pass": float(facts_ok and crit["faithful"] and crit["core"]), "facts": float(facts_ok),
             **{k: float(v) for k, v in crit.items()}, "refused": float(status == "refused")}
    reasons["facts"] = "; ".join(facts_problems) or "ok"
    # Ao re-avaliar, o trace mantém o prompt que gerou o resumo, não o atual.
    user_msg = old_trace[1]["content"] if old_trace else build_user_message(c, language)
    row = {**key, "prompt": user_msg, "tags": case["tags"], "status": status, "stop_reason": stop,
           "grade": grade, "explanation": reasons, "model": resp.model, "usage": usage_dict(resp.usage),
           "judge_model": JUDGE_MODEL if judge_usage else None, "judge_usage": judge_usage,
           "latency_s": round(latency, 2), "words": len(summary.split()), "retries": retries,
           "meta": {"language": language, "contract_id": c["id"]}}
    trace = old_trace or [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user_msg},
                          {"role": "assistant", "content": summary or f"({status})"}]
    if judge_usage:
        trace += [{"role": "system", "content": "[judge] " + JUDGE_SYSTEM},
                  {"role": "user", "content": "[judge] " + judge_prompt(c, notable, language, summary)},
                  {"role": "assistant", "content": "[judge] " + json.dumps(reasons, ensure_ascii=False, indent=1)}]
    (variant_dir / "traces").mkdir(parents=True, exist_ok=True)
    (variant_dir / "traces" / f"{case['prompt_id']}_rep{rep}.json").write_text(
        json.dumps(trace, ensure_ascii=False, indent=1), encoding="utf-8")
    append(variant_dir / "results.jsonl", row)


def summary_line(variant_dir, backend):
    rows = [json.loads(l) for l in open(variant_dir / "results.jsonl", encoding="utf-8")]
    n = len(rows)
    print(f"\n{variant_dir.name}: {n} casos")
    for m in ("pass", "facts", "faithful", "core", "notable", "clear", "refused"):
        p = sum(r["grade"][m] for r in rows) / n
        half = 1.96 * math.sqrt(max(p * (1 - p), 1e-9) / n)
        print(f"  {m:9s} {100 * p:5.1f}%  (±{100 * half:.0f} pp)")
    app = sum(cost(r["model"], r["usage"]) for r in rows)
    jud = sum(cost(r["judge_model"], r["judge_usage"]) for r in rows if r["judge_usage"])
    lat = sorted(r["latency_s"] for r in rows)
    if backend == "claude-code":
        print("  (subscrição: o custo abaixo é uma estimativa a preços de API, não um valor pago)")
    print(f"  custo resumos ${app:.4f} (${app / n:.5f}/resumo) | juiz ${jud:.4f} | latência mediana {lat[n // 2]:.1f}s"
          f" | palavras mediana {sorted(r['words'] for r in rows)[n // 2]}")
    errors = variant_dir / "errors.jsonl"
    if errors.exists():
        print(f"  erros de infraestrutura: {sum(1 for _ in open(errors, encoding='utf-8'))} (ver errors.jsonl)")


def judge_selftest(client, cases):
    """O juiz tem de reprovar três resumos maus conhecidos; se não reprovar, é demasiado brando."""
    c, other = cases[1]["contract"], cases[2]["contract"]
    wrong = (f"{other['contractingEntities'][0]['name']} contratou {other['description'][:80]} "
             f"por {other['priceEur']:,.2f} € através de {other['procedureType']}.")
    ok = True
    for label, s in (("vazio", ""), ("não sei", "Não sei."), ("contrato errado", wrong)):
        crit, reasons, _ = judge(client, c, notable_points(c), "pt", s)
        failed = not (crit["faithful"] and crit["core"])
        ok &= failed
        print(f"  {label:16s} {'reprovado (bom)' if failed else 'APROVADO (mau)'} — {reasons['core']}")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", required=True)
    ap.add_argument("--model", required=True, choices=sorted(PRICES))
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--limit", type=int, help="só os primeiros N casos (piloto)")
    ap.add_argument("--timeout-s", type=float, default=180)
    ap.add_argument("--concurrency", type=int, default=5)
    ap.add_argument("--approve-harness", action="store_true")
    ap.add_argument("--judge-selftest", action="store_true", help="testa o juiz com 3 resumos maus e sai")
    ap.add_argument("--backend", choices=["api", "claude-code"], default="api",
                    help="claude-code usa a subscrição via 'claude -p' (grátis, números indicativos)")
    ap.add_argument("--reuse-from", type=Path,
                    help="pasta de uma variante já corrida: reutiliza os resumos e só volta a correr o juiz")
    args = ap.parse_args()
    if not re.fullmatch(r"baseline|v\d+", args.variant):
        sys.exit("--variant tem de ser 'baseline' ou 'vN' (o relatório ignora outros nomes)")

    out = FLOW_CC if args.backend == "claude-code" else FLOW
    out.mkdir(parents=True, exist_ok=True)
    if out != FLOW:
        shutil.copyfile(FLOW / "_state.json", out / "_state.json")
    approved = out / ".harness_sha"
    sha = harness_sha()
    if args.approve_harness:
        approved.write_text(sha)
    elif not approved.exists() or approved.read_text().strip() != sha:
        sys.exit("O runner, os graders ou o prompt mudaram desde a última aprovação. Revê-os e corre com --approve-harness.")

    variant_dir = out / args.variant
    variant_dir.mkdir(parents=True, exist_ok=True)
    done = set()
    if (variant_dir / "results.jsonl").exists():
        done = {(r["prompt_id"], r["rep"]) for r in map(json.loads, open(variant_dir / "results.jsonl", encoding="utf-8"))}
    cases = [json.loads(l) for l in open(CASES, encoding="utf-8")][:args.limit]
    todo = [(c, rep) for c in cases for rep in range(args.reps) if (c["prompt_id"], rep) not in done]
    print(f"{len(todo)} execuções a fazer ({len(done)} já feitas) com {args.model}")

    if args.backend == "claude-code":
        client = ClaudeCodeClient(timeout=args.timeout_s)
    else:
        client = anthropic.Anthropic(max_retries=0, timeout=args.timeout_s)  # as repetições são feitas aqui, com registo
    if args.judge_selftest:
        judge_selftest(client, cases)
    with ThreadPoolExecutor(args.concurrency) as pool:
        list(pool.map(lambda t: run_case(client, t[0], t[1], args.model, variant_dir, args.timeout_s,
                                         args.reuse_from), todo))
    summary_line(variant_dir, args.backend)


if __name__ == "__main__":
    main()
