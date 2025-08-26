# test_merge.py
# Tests para el módulo merge.py

import os
from merge import merge_pdfs
from PyPDF2 import PdfReader

def test_merge_pdfs(tmp_path):
    # Crear archivos PDF de prueba
    from fpdf import FPDF
    pdf_paths = []
    for i in range(2):
        path = tmp_path / f"test_{i}.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Documento {i+1}", ln=True)
        pdf.output(str(path))
        pdf_paths.append(str(path))

    output_path = tmp_path / "merged.pdf"
    merge_pdfs(pdf_paths, str(output_path))

    assert os.path.exists(output_path)
    reader = PdfReader(str(output_path))
    assert len(reader.pages) == 2
