"""
API Endpoint'leri
"""
import logging
from typing import List, Optional

from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel, Field

from ..models import (
    Summarizer,
    SentimentAnalyzer,
    EntitySentimentAnalyzer,
    TranslationService,
    TextClassifier,
    QuestionAnswerer,
    KeywordExtractor,
    NamedEntityRecognizer
)
from ..services import PDFService, FileService

logger = logging.getLogger(__name__)
router = APIRouter()

# Model instance'lari (lazy loading ile)
_summarizer = None
_sentiment_analyzer = None
_entity_sentiment = None
_translator = None
_classifier = None
_qa = None
_keyword_extractor = None
_ner = None
_pdf_service = None
_file_service = None


def get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = Summarizer()
    return _summarizer


def get_sentiment_analyzer():
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = SentimentAnalyzer()
    return _sentiment_analyzer


def get_entity_sentiment():
    global _entity_sentiment
    if _entity_sentiment is None:
        _entity_sentiment = EntitySentimentAnalyzer()
    return _entity_sentiment


def get_translator():
    global _translator
    if _translator is None:
        _translator = TranslationService()
    return _translator


def get_classifier():
    global _classifier
    if _classifier is None:
        _classifier = TextClassifier()
    return _classifier


def get_qa():
    global _qa
    if _qa is None:
        _qa = QuestionAnswerer()
    return _qa


def get_keyword_extractor():
    global _keyword_extractor
    if _keyword_extractor is None:
        _keyword_extractor = KeywordExtractor()
    return _keyword_extractor


def get_ner():
    global _ner
    if _ner is None:
        _ner = NamedEntityRecognizer()
    return _ner


def get_pdf_service():
    global _pdf_service
    if _pdf_service is None:
        _pdf_service = PDFService()
    return _pdf_service


def get_file_service():
    global _file_service
    if _file_service is None:
        _file_service = FileService()
    return _file_service


# ===================== Request/Response Modelleri =====================

class TextInput(BaseModel):
    text: str = Field(..., min_length=1, description="Islenecek metin")


class SummarizeInput(BaseModel):
    text: str = Field(..., min_length=10)
    max_length: int = Field(default=150, ge=50, le=500)
    min_length: int = Field(default=50, ge=20, le=200)


class TranslationInput(BaseModel):
    text: str = Field(..., min_length=1)
    source_language: Optional[str] = Field(default=None, description="Kaynak dil (otomatik tespit icin bos birakin)")
    target_language: str = Field(..., description="Hedef dil kodu (tr, en, de, fr, ...)")


class MultiTranslationInput(BaseModel):
    text: str = Field(..., min_length=1)
    source_language: Optional[str] = None
    target_languages: List[str] = Field(..., min_items=1)


class QAInput(BaseModel):
    context: str = Field(..., min_length=10, description="Cevabi iceren metin")
    question: str = Field(..., min_length=3, description="Soru")


class KeywordInput(BaseModel):
    text: str = Field(..., min_length=10)
    num_keywords: int = Field(default=10, ge=1, le=50)
    method: str = Field(default="tfidf", description="tfidf, frequency, textrank")


# ===================== PDF & Dosya Endpoint'leri =====================

@router.post("/upload-pdf", tags=["Dosya Isleme"])
async def upload_pdf(file: UploadFile = File(...)):
    """PDF dosyasindan metin ve tablo cikarir"""
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Sadece PDF dosyalari kabul edilir")

    try:
        contents = await file.read()
        result = get_pdf_service().extract_text(contents)
        return result
    except Exception as e:
        logger.error(f"PDF isleme hatasi: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-file", tags=["Dosya Isleme"])
async def upload_file(file: UploadFile = File(...)):
    """Cesitli dosya formatlarini isler (PDF, CSV, Excel, Word, TXT)"""
    try:
        extension = file.filename.split('.')[-1] if '.' in file.filename else ''
        contents = await file.read()
        result = get_file_service().process(contents, extension)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Dosya isleme hatasi: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===================== NLP Endpoint'leri =====================

@router.post("/summarize", tags=["NLP"])
async def summarize(input: SummarizeInput):
    """Metni ozetler"""
    try:
        summary = get_summarizer().summarize(
            input.text,
            max_length=input.max_length,
            min_length=input.min_length
        )
        return {"summary": summary, "original_length": len(input.text), "summary_length": len(summary)}
    except Exception as e:
        logger.error(f"Ozetleme hatasi: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-sentiment", tags=["NLP"])
async def analyze_sentiment(input: TextInput):
    """Metnin duygusunu analiz eder"""
    try:
        result = get_sentiment_analyzer().analyze(input.text)
        return result
    except Exception as e:
        logger.error(f"Duygu analizi hatasi: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-entity-sentiment", tags=["NLP"])
async def analyze_entity_sentiment(input: TextInput):
    """Metindeki varliklarin duygusunu analiz eder"""
    try:
        result = get_entity_sentiment().analyze(input.text)
        return result
    except Exception as e:
        logger.error(f"Varlik duygu analizi hatasi: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-keywords", tags=["NLP"])
async def extract_keywords(input: KeywordInput):
    """Metinden anahtar kelimeleri cikarir"""
    try:
        keywords = get_keyword_extractor().extract(
            input.text,
            num_keywords=input.num_keywords,
            method=input.method
        )
        return {"keywords": keywords}
    except Exception as e:
        logger.error(f"Anahtar kelime cikarma hatasi: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/classify-text", tags=["NLP"])
async def classify_text(input: TextInput):
    """Metni kategorilere siniflandirir"""
    try:
        result = get_classifier().classify(input.text)
        return result
    except Exception as e:
        logger.error(f"Siniflandirma hatasi: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recognize-entities", tags=["NLP"])
async def recognize_entities(input: TextInput):
    """Metindeki varliklari (kisi, yer, organizasyon) tanir"""
    try:
        result = get_ner().recognize(input.text)
        return result
    except Exception as e:
        logger.error(f"NER hatasi: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/answer-question", tags=["NLP"])
async def answer_question(input: QAInput):
    """Verilen baglam icerisinde soruyu cevaplar"""
    try:
        result = get_qa().answer(input.context, input.question)
        return result
    except Exception as e:
        logger.error(f"Soru-cevap hatasi: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===================== Ceviri Endpoint'leri =====================

@router.post("/translate", tags=["Ceviri"])
async def translate(input: TranslationInput):
    """Metni hedef dile cevirir"""
    try:
        translator = get_translator()

        source_lang = input.source_language
        if source_lang is None:
            source_lang = translator.detect_language(input.text)

        translated = translator.translate(input.text, source_lang, input.target_language)

        return {
            "translated_text": translated,
            "source_language": source_lang,
            "target_language": input.target_language
        }
    except Exception as e:
        logger.error(f"Ceviri hatasi: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate-multiple", tags=["Ceviri"])
async def translate_multiple(input: MultiTranslationInput):
    """Metni birden fazla dile cevirir"""
    try:
        translator = get_translator()

        source_lang = input.source_language
        if source_lang is None:
            source_lang = translator.detect_language(input.text)

        translations = {}
        for target_lang in input.target_languages:
            translations[target_lang] = translator.translate(input.text, source_lang, target_lang)

        return {
            "translations": translations,
            "source_language": source_lang
        }
    except Exception as e:
        logger.error(f"Coklu ceviri hatasi: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/supported-languages", tags=["Ceviri"])
async def get_supported_languages():
    """Desteklenen dilleri listeler"""
    return {"languages": get_translator().get_supported_languages()}


@router.post("/detect-language", tags=["Ceviri"])
async def detect_language(input: TextInput):
    """Metnin dilini tespit eder"""
    try:
        detected = get_translator().detect_language(input.text)
        return {"detected_language": detected}
    except Exception as e:
        logger.error(f"Dil tespiti hatasi: {e}")
        raise HTTPException(status_code=500, detail=str(e))
