from src.main import years_to_read

YEARS = list(range(2012, 2027))


def test_recent_window_reads_current_and_two_previous_files():
    # Publicações de out/2026 estão nos ficheiros de 2026, 2025 e 2024.
    assert years_to_read("2026-09-29", "2026-10-29", YEARS) == [2024, 2025, 2026]


def test_december_includes_next_year_file_when_it_exists():
    # O ficheiro de 2026 traz publicações desde dez/2025.
    assert years_to_read("2025-12-01", "2025-12-31", YEARS) == [2023, 2024, 2025, 2026]


def test_new_year_before_next_file_is_published():
    # Início de 2027 sem contratos2027.zip: tem de ler os anos anteriores, não falhar.
    assert years_to_read("2026-12-06", "2027-01-05", YEARS) == [2024, 2025, 2026]
    assert years_to_read("2027-01-01", "2027-01-05", YEARS) == [2025, 2026]


def test_years_outside_available():
    assert years_to_read("2035-01-01", "2035-02-01", YEARS) == []
