import pytest

from src.normalize import is_likely_person, merge_duplicate, normalize, parse_bidder, parse_party

# Linha real do dump contratos2026 (versão de 25 out 2026), encurtada.
ROW = {
    "idcontrato": "12014814", "tipoContrato": ["Aquisição de serviços"], "tipoprocedimento": "Ajuste Direto Regime Geral",
    "objectoContrato": "Selo de Usabilidade ", "descContrato": "Aquisição de serviços para obtenção de Selo de Usabilidade ",
    "adjudicante": ["600052737 - Serviços de Ação Social do Instituto Politécnico de Coimbra"],
    "adjudicatarios": ["515615021 - XpertGo - Business Solutions Development, Lda"],
    "dataPublicacao": "04/12/2025", "dataCelebracaoContrato": "23/02/2026", "precoContratual": 9000.0,
    "cpv": ["72210000-0 - Serviços de programação de pacotes de software"], "prazoExecucao": 81,
    "localExecucao": ["Portugal, Coimbra, Coimbra"], "fundamentacao": "Artigo 20.º", "ProcedimentoCentralizado": "Não",
    "numAcordoQuadro": "", "DescrAcordoQuadro": "", "precoBaseProcedimento": 9000.0, "dataDecisaoAdjudicacao": "13/11/2025",
    "dataFechoContrato": "", "PrecoTotalEfetivo": 0.0, "concorrentes": None, "linkPecasProc": "", "ContratEcologico": "Não",
    "adjudicatarioPMEs": ["515615021"], "NUTs": None, "Lotes": None, "TipoCriterioAdjudicacao": "Monofator", "nAnuncio": "",
}


def test_normalize_real_row():
    r = normalize(ROW)
    assert r["id"] == "12014814"
    assert r["description"] == "Aquisição de serviços para obtenção de Selo de Usabilidade"
    assert r["contractors"] == [{"nif": "515615021", "name": "XpertGo - Business Solutions Development, Lda",
                                 "isSme": True, "isLikelyPerson": False}]
    assert r["contractingEntities"][0]["isSme"] is None
    assert r["publicationDate"] == "2025-12-04"
    assert r["closeDate"] is None
    assert r["effectivePriceEur"] is None
    assert r["executionPlaces"] == [{"country": "Portugal", "district": "Coimbra", "municipality": "Coimbra"}]
    assert r["cpv"] == [{"code": "72210000-0", "description": "Serviços de programação de pacotes de software"}]
    assert r["frameworkAgreement"] is None and r["announcementNumber"] is None and r["procedureDocumentsUrl"] is None
    assert r["bidders"] == [] and r["nuts"] == [] and r["lots"] == []
    assert r["isGreen"] is False and r["awardCriteriaTypes"] == ["Monofator"]


def test_null_contractors_become_empty_list():
    assert normalize({**ROW, "adjudicatarios": None})["contractors"] == []


@pytest.mark.parametrize("raw, nif, name, person", [
    # NIF ocultado no dump: decide-se pelo nome
    ("- - EBSCO Information Services S.L.U.", None, "EBSCO Information Services S.L.U.", False),
    ("- - José Teixeira Moreira", None, None, True),
    ("- - Elsa Marisa Melo de Sousa Rocha", None, None, True),
    ("- - Acme Iberia, SA", None, "Acme Iberia, SA", False),
    ("- - Maria de Sá", None, None, True),  # apelido "Sá" não é "S.A."
    ("- - Fundação Calouste Gulbenkian", None, "Fundação Calouste Gulbenkian", False),
    # NIF visível: decide-se pelo prefixo
    ("234567890 - Ana Silva", "234567890", None, True),
    ("452000000 - John Smith", "452000000", None, True),
    ("504615947 - MEO - SERVIÇOS DE COMUNICAÇÕES E MULTIMÉDIA, S.A.", "504615947",
     "MEO - SERVIÇOS DE COMUNICAÇÕES E MULTIMÉDIA, S.A.", False),
])
def test_parse_party(raw, nif, name, person):
    p = parse_party(raw)
    assert (p["nif"], p["name"], p["isLikelyPerson"]) == (nif, name, person)


@pytest.mark.parametrize("raw, nif, name", [
    # formatos reais de `concorrentes`
    ("504615947-1 - MEO - SERVIÇOS DE COMUNICAÇÕES E MULTIMÉDIA, S.A.", "504615947",
     "MEO - SERVIÇOS DE COMUNICAÇÕES E MULTIMÉDIA, S.A."),
    ("514181435-GROWSKILLS UNIPESSOAL, LDA", "514181435", "GROWSKILLS UNIPESSOAL, LDA"),
    ("514181435- GROWSKILLS UNIPESSOAL, LDA", "514181435", "GROWSKILLS UNIPESSOAL, LDA"),
    ("504615947-1 MEO, S.A.", "504615947", "MEO, S.A."),
    ("504615947-1MEO, S.A.", "504615947", "MEO, S.A."),
    ("-- Empresa Exemplo, Lda", None, "Empresa Exemplo, Lda"),
    ("-- José Teixeira Moreira", None, None),
])
def test_parse_bidder(raw, nif, name):
    b = parse_bidder(raw)
    assert (b["nif"], b["name"]) == (nif, name)


def test_unknown_bidder_format_keeps_text_unless_person():
    assert parse_bidder("Consórcio X, Lda / Y, S.A.")["name"] == "Consórcio X, Lda / Y, S.A."
    assert parse_bidder("???")["name"] is None  # sem forma jurídica: na dúvida, tratado como pessoa


def test_is_likely_person_without_name():
    assert is_likely_person(None, None) is False


def test_merge_duplicate_joins_expected_fields():
    a = normalize(ROW)
    b = normalize({**ROW, "ContratEcologico": "Sim", "TipoCriterioAdjudicacao": "Multifator"})
    assert merge_duplicate(a, b) is True
    assert a["isGreen"] is True and a["awardCriteriaTypes"] == ["Monofator", "Multifator"]


def test_merge_duplicate_flags_other_differences():
    assert merge_duplicate(normalize(ROW), normalize({**ROW, "precoContratual": 1.0})) is False
