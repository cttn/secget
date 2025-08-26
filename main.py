# main.py
# Script principal: orquesta la descarga y combinación de filings por ticker

import os
import time
from typing import List, Optional
import json
from fetch import get_cik_from_ticker, search_sec_filings
from download import download_html_and_convert_to_pdf, get_filing_document_url
from merge import merge_pdfs, create_cover_page, merge_cover_and_document

def download_and_merge_sec_filings(
    ticker: str,
    start: str,
    end: str,
    forms: List[str] = [],
    output_dir: Optional[str] = None,
) -> str:
    cik = get_cik_from_ticker(ticker)
    print(f"========== Procesando {ticker} ==========")
    print(f"Buscando documentos para {ticker} (CIK: {cik}) entre {start} y {end}...")
    filings = search_sec_filings(cik, forms, start, end)

    if output_dir is None:
        output_dir = os.path.join("output", ticker)
    os.makedirs(output_dir, exist_ok=True)
    pdfs: List[str] = []

    for i, filing in enumerate(filings):
        print("DEBUG FILING:\n", json.dumps(filing, indent=2))
        index_url = "https://www.sec.gov" + filing["_source"]["linkToHtml"]
        form_type = filing["_source"].get("form", "Desconocido")
        filing_date = filing["_source"].get("filed", "Sin fecha")

        print(f"Descargando y convirtiendo: {index_url}")
        doc_url = get_filing_document_url(index_url)
        pdf_path = os.path.join(output_dir, f"{ticker}_{i}_document.pdf")
        final_pdf_path = os.path.join(output_dir, f"{ticker}_{i}.pdf")

        download_html_and_convert_to_pdf(doc_url, pdf_path)

        # Crear portada y combinar
        cover_path = os.path.join(output_dir, f"{ticker}_{i}_cover.pdf")
        create_cover_page(form_type, filing_date, cover_path)
        merge_cover_and_document(cover_path, pdf_path, final_pdf_path)

        pdfs.append(final_pdf_path)
        time.sleep(0.5)

    merged_path = os.path.join(output_dir, f"{ticker}_merged.pdf")
    merge_pdfs(pdfs, merged_path)
    print(f"📄 PDF combinado guardado en: {merged_path}")
    return merged_path

if __name__ == "__main__":
    download_and_merge_sec_filings("AAPL", "2023-01-01", "2023-12-31")
