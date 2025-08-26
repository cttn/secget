# merge.py

import os
from PyPDF2 import PdfMerger
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def create_cover_page(title: str, date: str, output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph(f"<b>Fecha:</b> {date}", styles["Title"]))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(f"<b>Formulario:</b> {title}", styles["Title"]))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Documento del filing a continuación.", styles["Normal"]))

    doc.build(story)

def merge_cover_and_document(cover_path: str, doc_path: str, output_path: str):
    merger = PdfMerger()
    merger.append(cover_path)
    merger.append(doc_path)
    merger.write(output_path)
    merger.close()

def merge_pdfs(pdf_paths: list, output_path: str):
    merger = PdfMerger()
    for pdf in pdf_paths:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()
