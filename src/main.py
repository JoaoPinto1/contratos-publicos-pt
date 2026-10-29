import hashlib
import json
from datetime import date, timedelta

from apify import Actor

from .filters import build_filter
from .normalize import merge_duplicate, normalize
from .source import dump_urls, iter_rows

STATE_STORE = "contratos-publicos-pt-state"
FILTER_KEYS = ("keywords", "contractingEntity", "contractor", "cpvPrefixes", "procedureTypes",
               "dateFrom", "dateTo", "minPrice", "maxPrice")
BATCH = 500


def years_to_read(date_from, date_to, available):
    """Ficheiros anuais a ler para um intervalo de datas de publicação.

    O ano do ficheiro é o do contrato, não o da publicação: o ficheiro de 2026 traz publicações desde dez/2025,
    e os de 2025 e 2024 trazem ~12% das publicações de 2026.
    shortcut: ficheiros com 3+ anos de atraso (~0.7% das publicações) ficam de fora; ver ADR-002.
    """
    first, last = int(date_from[:4]) - 2, int(date_to[:4]) + 1
    return [y for y in sorted(available) if first <= y <= last]


async def main():
    async with Actor:
        inp = await Actor.get_input() or {}
        today = date.today().isoformat()
        inp.setdefault("dateFrom", (date.today() - timedelta(days=30)).isoformat())
        inp["dateTo"] = inp.get("dateTo") or today
        max_items = inp.get("maxItems") or 1000
        only_new = bool(inp.get("onlyNew"))

        state_key = "last-id-" + hashlib.sha1(
            json.dumps({k: inp.get(k) for k in FILTER_KEYS}, sort_keys=True).encode()).hexdigest()[:16]
        store = await Actor.open_key_value_store(name=STATE_STORE)
        last_id = int(await store.get_value(state_key) or 0) if only_new else 0
        if only_new:
            Actor.log.info(f"Modo incremental: só contratos com id > {last_id}")

        matches = build_filter(inp)
        urls = dump_urls()
        years = years_to_read(inp["dateFrom"], inp["dateTo"], urls)
        if not years:
            await Actor.fail(status_message=f"Não há dumps para {inp['dateFrom']}..{inp['dateTo']}. Anos: {sorted(urls)}")
            return

        found = {}
        skipped = 0
        for year in years:
            Actor.log.info(f"A ler o dump de {year}")
            await Actor.set_status_message(f"A ler os contratos de {year}")
            for row in iter_rows(urls[year]):
                try:
                    if int(row["idcontrato"]) <= last_id:
                        continue
                    c = normalize(row)
                except (KeyError, ValueError, TypeError, AttributeError) as e:
                    # Uma linha mal formada no dump não pode estragar a execução inteira.
                    skipped += 1
                    if skipped <= 5:
                        Actor.log.warning(f"Linha ignorada ({type(e).__name__}: {e}): {str(row)[:200]}")
                    continue
                if not matches(c):
                    continue
                if c["id"] in found:
                    if not merge_duplicate(found[c["id"]], c):
                        Actor.log.warning(f"Contrato {c['id']} repetido com campos diferentes; fica a primeira cópia")
                else:
                    found[c["id"]] = c

        if skipped:
            Actor.log.warning(f"{skipped} linhas do dump ignoradas por estarem mal formadas")

        # Incremental: do mais antigo para o mais recente, para o marcador ficar certo se o maxItems cortar a lista.
        items = sorted(found.values(), key=lambda c: int(c["id"]), reverse=not only_new)[:max_items]
        charging = Actor.get_charging_manager()
        pushed = 0
        for i in range(0, len(items), BATCH):
            batch = items[i:i + BATCH]
            # Quantos cabem no limite de gasto do utilizador; o charged_count não serve porque é 0 sem pay-per-event.
            n = charging.compute_push_data_limit(len(batch), "contract", is_default_dataset=True)
            await Actor.push_data(batch[:n], charged_event_name="contract")
            pushed += n
            if n < len(batch):
                Actor.log.info("Limite de gasto atingido")
                break

        if only_new and pushed:
            await store.set_value(state_key, int(items[pushed - 1]["id"]))
        await Actor.set_status_message(f"{pushed} contratos ({len(found)} encontrados)", is_terminal=True)
