import io
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

def extract_text_and_tables_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file, filetype="pdf")
    text_content = ""
    tables = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Extract text
        text_content += page.get_text()

        # Placeholder for table extraction (as PyMuPDF does not have built-in table extraction)
        # You may want to use a library like camelot or pdfplumber for more accurate table extraction
        # For now, this part is omitted due to lack of built-in support in PyMuPDF
        # tables_on_page = page.find_tables()
        # for table in tables_on_page:
        #     tables.append(table.extract())

        # Extract text from images (if any)
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Use PIL to open the image
            image = Image.open(io.BytesIO(image_bytes))

            # Use pytesseract to do OCR on the image
            text_content += pytesseract.image_to_string(image)

    return {"text": text_content, "tables": tables}
