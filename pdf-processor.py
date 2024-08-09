import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with fitz.open(stream=pdf_file, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text
