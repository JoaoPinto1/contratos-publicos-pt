import urllib.error

import pytest

from src import source
from src.source import pick_dataset_slug

# Resultados reais da pesquisa no dados.gov.pt (29 out 2026), mais um de 2027 hipotético.
RESULTS = [
    {"slug": "contratos-publicos-portal-base-impic-contratos-de-2012-a-2026"},
    {"slug": "contratos-publicos-portal-base-impic-entidades"},
    {"slug": "contratos-publicos-portal-base-impic-anuncios-de-2012-a-2026"},
    {"slug": "contratos-publicos-portal-base-impic-modificacoes-contratuais-de-2012-a-2026"},
]


def test_pick_current_dataset():
    assert pick_dataset_slug(RESULTS) == "contratos-publicos-portal-base-impic-contratos-de-2012-a-2026"


def test_pick_newest_when_new_year_appears():
    new = {"slug": "contratos-publicos-portal-base-impic-contratos-de-2012-a-2027"}
    assert pick_dataset_slug(RESULTS + [new]) == new["slug"]


def test_pick_none_when_missing():
    assert pick_dataset_slug(RESULTS[1:]) is None


@pytest.fixture
def no_sleep(monkeypatch):
    monkeypatch.setattr(source.time, "sleep", lambda s: None)


def test_retry_recovers_from_network_error(no_sleep):
    calls = []

    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise urllib.error.URLError("reset")
        return "ok"

    assert source._retry(flaky, "x") == "ok" and len(calls) == 3


def test_retry_gives_up(no_sleep):
    def down():
        raise urllib.error.HTTPError("u", 503, "down", {}, None)

    with pytest.raises(urllib.error.HTTPError):
        source._retry(down, "x")


def test_retry_does_not_repeat_client_errors(no_sleep):
    calls = []

    def missing():
        calls.append(1)
        raise urllib.error.HTTPError("u", 404, "not found", {}, None)

    with pytest.raises(urllib.error.HTTPError):
        source._retry(missing, "x")
    assert len(calls) == 1
