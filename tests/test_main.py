from src.main import years_to_read


def test_years_include_next_file():
    # O ficheiro de 2026 traz contratos publicados desde dezembro de 2025.
    assert years_to_read("2025-12-10", "2025-12-20", [2024, 2025, 2026]) == [2025, 2026]


def test_years_ignore_missing_future_file():
    assert years_to_read("2026-10-01", "2026-10-29", [2025, 2026]) == [2026]


def test_years_outside_available():
    assert years_to_read("2030-01-01", "2030-02-01", [2025, 2026]) == []
