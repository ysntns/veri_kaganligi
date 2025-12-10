"""
NLP Model Testleri
"""
import pytest


class TestKeywordExtractor:
    """Anahtar kelime cikarici testleri"""

    def test_extract_keywords(self):
        """Basit anahtar kelime cikarma"""
        from app.models.keywords import KeywordExtractor

        extractor = KeywordExtractor()
        text = "Python programlama dili yapay zeka ve makine ogrenimi icin cok populer."
        keywords = extractor.extract(text, num_keywords=3)

        assert len(keywords) <= 3
        assert all("keyword" in kw and "score" in kw for kw in keywords)

    def test_empty_text(self):
        """Bos metin icin bos liste donmeli"""
        from app.models.keywords import KeywordExtractor

        extractor = KeywordExtractor()
        keywords = extractor.extract("", num_keywords=5)
        assert keywords == []


class TestSentimentAnalyzer:
    """Duygu analizci testleri"""

    def test_analyze_returns_valid_structure(self):
        """Duygu analizi dogru yapi dondurmeli"""
        from app.models.sentiment import SentimentAnalyzer

        analyzer = SentimentAnalyzer()
        # Fallback mekanizmasi test edilir
        result = analyzer._rule_based_analysis("Bu cok guzel bir urun")

        assert "sentiment" in result
        assert "score" in result
        assert result["sentiment"] in ["positive", "negative", "neutral"]


class TestTranslationService:
    """Ceviri servisi testleri"""

    def test_language_detection_turkish(self):
        """Turkce tespit edilmeli"""
        from app.models.translator import TranslationService

        translator = TranslationService()
        detected = translator.detect_language("Merhaba, nasilsiniz?")
        assert detected == "tr"

    def test_supported_languages(self):
        """Desteklenen diller listesi bos olmamali"""
        from app.models.translator import TranslationService

        translator = TranslationService()
        languages = translator.get_supported_languages()

        assert len(languages) > 0
        assert "tr" in languages
        assert "en" in languages


class TestSummarizer:
    """Ozetleyici testleri"""

    def test_extractive_summary(self):
        """Extractive ozetleme calismali"""
        from app.models.summarizer import Summarizer

        summarizer = Summarizer()
        text = "Bu birinci cumle. Bu ikinci cumle. Bu ucuncu cumle. Bu dorduncu cumle."
        summary = summarizer._extractive_summary(text, num_sentences=2)

        assert len(summary) > 0
        assert len(summary) < len(text)
