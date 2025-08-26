# fetch.py
# Módulo para obtener el CIK y buscar filings desde la EDGAR API alternativa (data.sec.gov)

import requests
from datetime import datetime
from typing import List

EDGAR_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
TICKER_TO_CIK_LOOKUP = "https://www.sec.gov/files/company_tickers.json"
HEADERS = {
    "User-Agent": "secget/0.1 (crls@reflejo.capital)"
}

def get_cik_from_ticker(ticker: str) -> str:
    """
    Convierte un ticker (ej. AAPL) a su código CIK (Central Index Key).
    """
    r = requests.get(TICKER_TO_CIK_LOOKUP, headers=HEADERS)
    r.raise_for_status()
    data = r.json()
    for item in data.values():
        if item['ticker'].lower() == ticker.lower():
            return str(item['cik_str']).zfill(10)
    raise ValueError(f"CIK no encontrado para ticker: {ticker}")

def search_sec_filings(cik: str, form_types: List[str], start_date: str, end_date: str, max_results: int = 20):
    """
    Obtiene la lista de filings para un CIK desde data.sec.gov, filtrando por tipo de formulario y rango de fechas.

    Si `form_types` está vacío, no se filtra por tipo de formulario.
    """
    url = EDGAR_SUBMISSIONS_URL.format(cik=cik)
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    data = res.json()

    results = []
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    for acc_no, filing_type, filed_date in zip(
        data["filings"]["recent"]["accessionNumber"],
        data["filings"]["recent"]["form"],
        data["filings"]["recent"]["filingDate"]
    ):
        fdt = datetime.strptime(filed_date, "%Y-%m-%d")
        if start_dt <= fdt <= end_dt:
            if not form_types or filing_type in form_types:
                acc_no_dash = acc_no.replace("-", "")
                results.append({
                    "_source": {
                        "linkToHtml": f"/Archives/edgar/data/{int(cik)}/{acc_no_dash}/{acc_no}-index.html",
                        "form": filing_type,
                        "filed": filed_date
                    }
                })
        if len(results) >= max_results:
            break

    return results
