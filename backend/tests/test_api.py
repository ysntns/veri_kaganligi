"""
API Endpoint Testleri
"""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Test client fixture"""
    from app.main import app
    return TestClient(app)


class TestHealthCheck:
    """Saglik kontrolu testleri"""

    def test_health_endpoint(self, client):
        """Health endpoint'inin calistigini dogrula"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_root_redirects_to_docs(self, client):
        """Root path docs'a yonlendirmeli"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307


class TestNLPEndpoints:
    """NLP endpoint testleri"""

    def test_summarize_endpoint(self, client):
        """Ozetleme endpoint'i testi"""
        response = client.post(
            "/api/v1/summarize",
            json={"text": "Bu bir test metnidir. " * 20, "max_length": 50, "min_length": 20}
        )
        assert response.status_code == 200
        assert "summary" in response.json()

    def test_sentiment_endpoint(self, client):
        """Duygu analizi endpoint'i testi"""
        response = client.post(
            "/api/v1/analyze-sentiment",
            json={"text": "Bu urun cok guzel!"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "sentiment" in data
        assert "score" in data

    def test_keywords_endpoint(self, client):
        """Anahtar kelime endpoint'i testi"""
        response = client.post(
            "/api/v1/extract-keywords",
            json={"text": "Python programlama dili cok populer bir dildir.", "num_keywords": 3}
        )
        assert response.status_code == 200
        assert "keywords" in response.json()

    def test_classify_endpoint(self, client):
        """Siniflandirma endpoint'i testi"""
        response = client.post(
            "/api/v1/classify-text",
            json={"text": "Fenerbahce mac kazandi"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "category" in data


class TestTranslationEndpoints:
    """Ceviri endpoint testleri"""

    def test_supported_languages(self, client):
        """Desteklenen diller endpoint'i"""
        response = client.get("/api/v1/supported-languages")
        assert response.status_code == 200
        assert "languages" in response.json()


class TestValidation:
    """Input validasyon testleri"""

    def test_empty_text_validation(self, client):
        """Bos metin reddedilmeli"""
        response = client.post(
            "/api/v1/analyze-sentiment",
            json={"text": ""}
        )
        assert response.status_code == 422  # Validation error
