
import os
from fpdf import FPDF


EXPORT_DIR = "static/exports"


def save_as_markdown(content: str, topic: str) -> str:
    os.makedirs(EXPORT_DIR, exist_ok=True)
    filename = f"{topic.replace(' ' , '_').lower()}.md"
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filename    

def save_as_pdf(content: str, topic: str) -> str:
    os.makedirs(EXPORT_DIR, exist_ok=True)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Fix for unicode characteres that fpdf (latin-1) can't encode
    cleaned_content = content.encode("latin-1", "replace").decode("latin-1")

    for line in cleaned_content.split("\n"):
        pdf.multi_cell(0, 10, line)

    filename = f"{topic.replace(' ','_').lower()}.pdf"
    filepath = os.path.join(EXPORT_DIR, filename)
    pdf.output(filepath)
    return filename