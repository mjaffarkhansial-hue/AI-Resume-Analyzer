import fitz  # PyMuPDF


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract selectable text from an uploaded PDF file."""
    document = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    try:
        pages = [page.get_text("text") for page in document]
        return "\n".join(pages).strip()
    finally:
        document.close()
