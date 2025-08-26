# test_fetch.py
# Tests para el módulo fetch.py

import pytest
from fetch import get_cik_from_ticker, search_sec_filings

# Test básico: ticker conocido → CIK
def test_get_cik_from_ticker():
    cik = get_cik_from_ticker("AAPL")
    assert cik.isdigit()
    assert len(cik) == 10

# Test de búsqueda real (requiere conexión a internet)
def test_search_sec_filings():
    cik = get_cik_from_ticker("MSFT")
    filings = search_sec_filings(cik, ["10-K"], "2023-01-01", "2023-12-31", max_results=5)
    assert isinstance(filings, list)
    assert len(filings) > 0
    assert "linkToHtml" in filings[0]["_source"]
