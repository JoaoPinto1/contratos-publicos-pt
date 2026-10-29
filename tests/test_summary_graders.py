import pytest

from evals.contract_summary.graders import check_facts, money_amounts
from src.normalize import normalize
from src.summarize import build_user_message, notable_points
from tests.test_normalize import ROW

C = normalize(ROW)  # 9000 €, base 9000 €, adjudicante 600052737, adjudicatário 515615021


@pytest.mark.parametrize("text, language, expected", [
    ("O contrato custa 9.000,00 €.", "pt", [9000.0]),
    ("O contrato custa 9 000 euros.", "pt", [9000.0]),
    ("por 19,98 milhões de euros", "pt", [19_980_000.0]),
    ("The contract is worth €9,000.", "en", [9000.0]),
    ("worth 19.98 million euros", "en", [19_980_000.0]),
    ("priced at 19.977.035,78 €", "en", [19_977_035.78]),
    ("assinado em 2026, por 9.000 €", "pt", [9000.0]),  # o ano não se cola ao valor
    ("Lote 3 de 2026, sem valor em euros mencionado", "pt", []),
])
def test_money_amounts(text, language, expected):
    assert money_amounts(text, language) == pytest.approx(expected)


def test_facts_pass_on_correct_summary():
    s = ("Os Serviços de Ação Social do Instituto Politécnico de Coimbra adjudicaram por ajuste direto à "
         "XpertGo (NIF 515615021) a obtenção de um selo de usabilidade, por 9.000,00 €.")
    assert check_facts(s, C, "pt") == (True, [])


def test_facts_fail_on_wrong_amount_and_nif():
    ok, problems = check_facts("Contrato de 90.000 € com a empresa 123456789.", C, "pt")
    assert not ok and len(problems) == 2


def test_facts_null_output_has_nothing_to_check():
    # Um resumo vazio passa nos factos; é a rubrica que o reprova (critério core).
    assert check_facts("", C, "pt") == (True, [])


def test_notable_points_from_code():
    c = normalize({**ROW, "precoContratual": 9900.0, "concorrentes": ["504615947-1 - MEO, S.A."]})
    points = notable_points(c)
    assert "only one bidder took part in the procedure" in points
    assert any("10.0% above" in p for p in points)


def test_user_message_has_no_url_and_lists_points():
    msg = build_user_message(C, "pt")
    assert "base.gov.pt" not in msg and "Notable points:\n- none" in msg and "português" in msg
