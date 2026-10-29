"""Dumps semanais do IMPIC no dados.gov.pt (ADR-001)."""

import json
import logging
import re
import shutil
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

import ijson

API = "https://dados.gov.pt/api/1/datasets/"
SEARCH_QUERY = "contratos publicos portal base impic contratos"
# O slug muda quando o IMPIC acrescenta um ano ("...-de-2012-a-2026" → "...-a-2027").
SLUG = re.compile(r"contratos-publicos-portal-base-impic-contratos-de-2012-a-(\d{4})")
FALLBACK_SLUG = "contratos-publicos-portal-base-impic-contratos-de-2012-a-2026"
HEADERS = {"User-Agent": "contratos-publicos-pt (Apify actor)"}
RETRIES = 4

log = logging.getLogger(__name__)


def _retry(fn, what):
    """Repete erros de rede e 5xx com backoff (2, 4, 8 s); erros 4xx falham logo."""
    for attempt in range(RETRIES):
        try:
            return fn()
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == RETRIES - 1:
                raise
            err = e
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if attempt == RETRIES - 1:
                raise
            err = e
        log.warning(f"{what}: {err}; nova tentativa em {2 ** (attempt + 1)} s")
        time.sleep(2 ** (attempt + 1))


def _get_json(url):
    def fetch():
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)
    return _retry(fetch, url)


def pick_dataset_slug(search_results):
    """O slug do dataset de contratos com o ano final mais alto, ou None."""
    found = [(int(m.group(1)), d["slug"]) for d in search_results
             if (m := SLUG.fullmatch(d.get("slug", "")))]
    return max(found)[1] if found else None


def dump_urls():
    """{ano: url do zip}. Os URLs mudam a cada publicação, por isso vêm sempre da API."""
    query = urllib.parse.urlencode({"q": SEARCH_QUERY, "page_size": 20})
    try:
        slug = pick_dataset_slug(_get_json(f"{API}?{query}")["data"]) or FALLBACK_SLUG
    except (urllib.error.URLError, KeyError, ValueError) as e:
        log.warning(f"Pesquisa de datasets falhou ({e}); a usar {FALLBACK_SLUG}")
        slug = FALLBACK_SLUG
    urls = {}
    for r in _get_json(f"{API}{slug}/")["resources"]:
        m = re.fullmatch(r"contratos(\d{4})\.zip", r["title"].strip(), re.IGNORECASE)
        if m:
            urls[int(m.group(1))] = r["url"]
    return urls


def _download(url, tmp):
    def fetch():
        tmp.seek(0)
        tmp.truncate()
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=120) as resp:
            shutil.copyfileobj(resp, tmp)
    _retry(fetch, url)


def iter_rows(url):
    """Linhas do JSON dentro do zip, em streaming: o JSON de um ano tem ~360 MB."""
    with tempfile.TemporaryFile() as tmp:
        _download(url, tmp)
        tmp.seek(0)
        with zipfile.ZipFile(tmp) as zf:
            names = [n for n in zf.namelist() if n.lower().endswith(".json")]
            if not names:
                raise ValueError(f"O zip {url} não tem nenhum ficheiro JSON: {zf.namelist()}")
            with zf.open(names[0]) as f:
                yield from ijson.items(f, "item", use_float=True)
