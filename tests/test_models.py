from backend.app.models.summarizer import Summarizer
from backend.app import TranslationService
from backend.app.models.sentiment_analyzer import SentimentAnalyzer
from backend.app import KeywordExtractor
from backend.app import TextClassifier
from backend.app import QuestionAnswerer

def test_summarizer():
    summarizer = Summarizer()
    text = "Bu bir test metnidir. " * 20
    summary = summarizer.summarize(text)
    assert isinstance(summary, str)
    assert len(summary) < len(text)

def test_translator():
    translator = TranslationService()
    text = "Merhaba dünya"
    translated = translator.translate(text, "en")
    assert isinstance(translated, str)
    assert "Translated:" in translated
    assert "to en" in translated

def test_sentiment_analyzer():
    analyzer = SentimentAnalyzer()
    text = "Bu harika bir ürün!"
    result = analyzer.analyze(text)
    assert isinstance(result, dict)
    assert "label" in result
    assert "score" in result
    assert isinstance(result["label"], str)
    assert isinstance(result["score"], float)

def test_keyword_extractor():
    extractor = KeywordExtractor()
    text = "Yapay zeka ve makine öğrenimi günümüzde çok önemli konular."
    keywords = extractor.extract(text)
    assert isinstance(keywords, list)
    assert len(keywords) > 0

def test_text_classifier():
    classifier = TextClassifier()
    text = "Bu bir teknoloji haberidir."
    result = classifier.classify(text)
    assert isinstance(result, dict)
    assert "label" in result
    assert "score" in result

def test_question_answerer():
    answerer = QuestionAnswerer()
    context = "Ankara Türkiye'nin başkentidir. İstanbul ise en kalabalık şehridir."
    question = "Türkiye'nin başkenti neresidir?"
    result = answerer.answer(context, question)
    assert isinstance(result, dict)
    assert "answer" in result
    assert "score" in result
