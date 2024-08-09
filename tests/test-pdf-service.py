import os
from backend.app.services import extract_text_and_tables_from_pdf

def test_extract_text_and_tables_from_pdf():
    test_pdf_path = os.path.join(os.path.dirname(__file__), "test.pdf")
    with open(test_pdf_path, "rb") as f:
        pdf_content = f.read()
    
    result = extract_text_and_tables_from_pdf(pdf_content)
    
    assert "text" in result
    assert "tables" in result
    assert isinstance(result["text"], str)
    assert len(result["text"]) > 0
    assert isinstance(result["tables"], list)

def test_extract_text_and_tables_from_pdf_with_table():
    test_pdf_path = os.path.join(os.path.dirname(__file__), "test_with_table.pdf")
    with open(test_pdf_path, "rb") as f:
        pdf_content = f.read()
    
    result = extract_text_and_tables_from_pdf(pdf_content)
    
    assert "text" in result
    assert "tables" in result
    assert isinstance(result["text"], str)
    assert len(result["text"]) > 0
    assert isinstance(result["tables"], list)
    assert len(result["tables"]) > 0
