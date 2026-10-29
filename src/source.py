"""Dumps semanais do IMPIC no dados.gov.pt (ADR-001)."""

import json
import re
import shutil
import tempfile
import urllib.request
import zipfile

import ijson

# shortcut: o slug inclui "2012-a-2026"; se o IMPIC criar um dataset novo em 2027, procurar pela API de pesquisa.
DATASET_API = "https://dados.gov.pt/api/1/datasets/contratos-publicos-portal-base-impic-contratos-de-2012-a-2026/"
HEADERS = {"User-Agent": "contratos-publicos-pt (Apify actor)"}


def _get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=120)


def dump_urls():
    """{ano: url do zip}. Os URLs mudam a cada publicação, por isso vêm sempre da API."""
    with _get(DATASET_API) as resp:
        resources = json.load(resp)["resources"]
    urls = {}
    for r in resources:
        m = re.fullmatch(r"contratos(\d{4})\.zip", r["title"].strip(), re.IGNORECASE)
        if m:
            urls[int(m.group(1))] = r["url"]
    return urls


def iter_rows(url):
    """Linhas do JSON dentro do zip, em streaming: o JSON de um ano tem ~360 MB."""
    with tempfile.TemporaryFile() as tmp:
        with _get(url) as resp:
            shutil.copyfileobj(resp, tmp)
        tmp.seek(0)
        with zipfile.ZipFile(tmp) as zf:
            name = next(n for n in zf.namelist() if n.lower().endswith(".json"))
            with zf.open(name) as f:
                yield from ijson.items(f, "item", use_float=True)
