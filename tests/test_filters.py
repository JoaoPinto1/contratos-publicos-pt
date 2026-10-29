import pytest

from src.filters import build_filter
from src.normalize import normalize
from tests.test_normalize import ROW

C = normalize(ROW)  # publicado 2025-12-04, 9000 €, CPV 72210000-0, adjudicante NIF 600052737


@pytest.mark.parametrize("inp, expected", [
    ({}, True),
    ({"keywords": "selo usabilidade"}, True),
    ({"keywords": "AQUISICAO servicos"}, True),  # sem acentos nem maiúsculas
    ({"keywords": "selo software"}, False),  # todos os termos têm de aparecer
    ({"contractingEntity": "600052737"}, True),
    ({"contractingEntity": "politecnico de coimbra"}, True),
    ({"contractingEntity": "lisboa"}, False),
    ({"contractor": "515615021"}, True),
    ({"contractor": "xpertgo"}, True),
    ({"cpvPrefixes": ["7221"]}, True),
    ({"cpvPrefixes": ["48", "72"]}, True),
    ({"cpvPrefixes": ["48"]}, False),
    ({"dateFrom": "2025-12-04", "dateTo": "2025-12-04"}, True),
    ({"dateFrom": "2025-12-05"}, False),
    ({"minPrice": 9000, "maxPrice": 9000}, True),
    ({"minPrice": 9001}, False),
    ({"procedureTypes": ["ajuste direto"]}, True),
    ({"procedureTypes": ["concurso publico"]}, False),
])
def test_filter(inp, expected):
    assert build_filter(inp)(C) is expected
