from pypdf import PdfReader

def extract_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)

    page_count = len(reader.pages)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text, page_count