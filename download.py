import requests
import pdfkit
from bs4 import BeautifulSoup
from pathlib import Path
from weasyprint import HTML

HEADERS = {
    "User-Agent": "secget/0.1 (crls@reflejo.capital)"
}

def get_filing_document_url(index_url: str) -> str:
    """
    Devuelve el enlace principal (.htm > .txt > .pdf) del filing.
    Solo busca dentro de la tabla de documentos reales del filing.
    """
    print(f"Analizando índice: {index_url}")
    res = requests.get(index_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    # Buscar tabla que contiene los documentos (evita navegación)
    doc_table = soup.find("table", class_="tableFile", summary="Document Format Files")
    if not doc_table:
        raise ValueError("No se encontró tabla de documentos en el índice.")

    links = doc_table.find_all("a", href=True)
    hrefs = [link["href"] for link in links]

    print("Enlaces encontrados en tabla de documentos:")
    for href in hrefs:
        print("  -", href)

    for ext in [".htm", ".txt", ".pdf"]:
        for href in hrefs:
            if ext in href and "-index.htm" not in href:
                if not href.startswith("http"):
                    href = "https://www.sec.gov" + href
                print(f"Documento detectado: {href}")
                return href

    raise ValueError("No se encontró documento visualizable en la tabla de documentos.")

def download_html_and_convert_to_pdf(document_url: str, output_path: str):
    try:
        html_path = Path(output_path).with_suffix(".htm")
        print(f"📥 Guardando HTML en: {html_path.name}")
        response = requests.get(document_url, headers=HEADERS)
        response.raise_for_status()
        html_path.write_text(response.text, encoding="utf-8")

        print(f"🧾 Convirtiendo a PDF desde archivo local con WeasyPrint...")
        HTML(filename=str(html_path)).write_pdf(output_path)
        print(f"✅ PDF generado en: {output_path}")

    except Exception as e:
        print(f"⚠️ Error al convertir {document_url} a PDF: {e}")
        print(f"📝 HTML guardado en: {html_path}")


