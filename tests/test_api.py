from fastapi.testclient import TestClient
from backend.app import app
import os
from backend.app.services import json_safe

client = TestClient(app)

def test_upload_pdf():
    test_pdf_path = os.path.join(os.path.dirname(__file__), "test.pdf")
    with open(test_pdf_path, "rb") as f:
        response = client.post("/upload-pdf/", files={"file": ("test.pdf", f, "application/pdf")})
    assert response.status_code == 200
    result = json_safe(response.json())
    assert "text" in result
    assert "tables" in result

def test_summarize():
    response = client.post("/summarize/", json={"text": "This is a test text that needs to be summarized."})
    assert response.status_code == 200
    assert "summary" in response.json()

def test_translate():
    response = client.post("/translate/", json={"text": "Hello, world!", "target_language": "tr"})
    assert response.status_code == 200
    assert "translated" in response.json()

def test_get_supported_languages():
    response = client.get("/supported-languages/")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_detect_language():
    response = client.post("/detect-language/", json={"text": "Merhaba dünya"})
    assert response.status_code == 200
    assert "detected_language" in response.json()

def test_analyze_sentiment():
    response = client.post("/analyze-sentiment/", json={"text": "Bu harika bir ürün!"})
    assert response.status_code == 200
    assert "label" in response.json()
    assert "score" in response.json()

def test_extract_keywords():
    response = client.post("/extract-keywords/", json={"text": "Yapay zeka ve makine öğrenimi günümüzde çok önemli konular."})
    assert response.status_code == 200
    assert "keywords" in response.json()

def test_classify_text():
    response = client.post("/classify-text/", json={"text": "Bu bir teknoloji haberidir."})
    assert response.status_code == 200
    assert "label" in response.json()
    assert "score" in response.json()

def test_answer_question():
    context = "Ankara Türkiye'nin başkentidir. İstanbul ise en kalabalık şehridir."
    question = "Türkiye'nin başkenti neresidir?"
    response = client.post("/answer-question/", json={"context": context, "question": question})
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "score" in response.json()



def test_analyze_text():
    response = client.post("/analyze/", json={"text": "X marka telefonun kamerası harika ama bataryası çok çabuk bitiyor."})
    assert response.status_code == 200
    result = response.json()
    assert "entities" in result
    assert "sentiments" in result