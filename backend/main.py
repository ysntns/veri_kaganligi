from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

import os
import logging
from pydantic import BaseModel
from typing import List, Optional
from services import pdf_service, process_file
from models import Summarizer, TranslationService, SentimentAnalyzer, KeywordExtractor, TextClassifier, QuestionAnswerer, EntitySentimentAnalyzer

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI uygulaması oluşturuluyor
app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend adresini buraya ekleyin
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metodlarına izin ver
    allow_headers=["*"],  # Tüm başlıklara izin ver
)

# Statik dosyaları servis etmek için
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "build")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    logger.warning(f"Statik dosya dizini bulunamadı: {static_dir}")

# NLTK verilerinin indirilmesi
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Dil modelleri ve hizmetler
summarizer = Summarizer()
translator = TranslationService()
sentiment_analyzer = SentimentAnalyzer()
keyword_extractor = KeywordExtractor()
text_classifier = TextClassifier()
question_answerer = QuestionAnswerer()
entity_sentiment_analyzer = EntitySentimentAnalyzer()

class TextInput(BaseModel):
    text: str

class TranslationInput(BaseModel):
    text: str
    target_languages: List[str]

class QAInput(BaseModel):
    context: str
    question: str

class TranslationRequest(BaseModel):
    text: str
    source_language: Optional[str] = None
    target_language: str

class MultiTranslationRequest(BaseModel):
    text: str
    source_language: Optional[str] = None
    target_languages: List[str]

# Yeni eklenen modeller
class EntitySentimentResult(BaseModel):
    entity: str
    sentiment: str

class EntitySentimentResponse(BaseModel):
    entity_list: List[str]
    results: List[EntitySentimentResult]

# Ekstra boşlukları kaldıran fonksiyon
def remove_extra_whitespace(text):
    import re
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([.!?])', r'\1', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

# API Endpoints

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = pdf_service(contents)
        result["text"] = remove_extra_whitespace(result["text"])
        return result
    except Exception as e:
        logger.error(f"PDF işleme hatası: {str(e)}")
        raise HTTPException(status_code=400, detail="PDF işlenirken bir hata oluştu.")

@app.post("/summarize/")
async def summarize(input: TextInput):
    try:
        summary = summarizer.summarize(input.text)
        return {"summary": remove_extra_whitespace(summary)}
    except Exception as e:
        logger.error(f"Özetleme hatası: {str(e)}")
        raise HTTPException(status_code=500, detail="Özetleme işlemi başarısız.")

@app.post("/analyze-sentiment/")
async def analyze_sentiment(data: TextInput):
    try:
        result = sentiment_analyzer.analyze(data.text)
        return result
    except Exception as e:
        logger.error(f"Duygu analizi hatası: {str(e)}")
        raise HTTPException(status_code=500, detail="Duygu analizi başarısız.")

@app.post("/analyze-entity-sentiment/", response_model=EntitySentimentResponse)
async def analyze_entity_sentiment(input: TextInput):
    try:
        logger.info(f"Analyzing text: {input.text[:50]}...")
        result = entity_sentiment_analyzer.analyze(input.text)
        logger.info(f"Extracted entities: {result['entity_list']}")
        logger.info(f"Analysis result: {result}")
        return EntitySentimentResponse(**result)
    except Exception as e:
        logger.error(f"Varlık bazlı duygu analizi hatası: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Varlık bazlı duygu analizi başarısız: {str(e)}")

@app.post("/extract-keywords/")
async def extract_keywords(input: TextInput):
    try:
        keywords = keyword_extractor.extract(input.text)
        return {"keywords": keywords}
    except Exception as e:
        logger.error(f"Anahtar kelime çıkarma hatası: {str(e)}")
        raise HTTPException(status_code=500, detail="Anahtar kelime çıkarma başarısız.")

@app.post("/classify-text/")
async def classify_text(input: TextInput):
    try:
        classification = text_classifier.classify(input.text)
        return classification
    except Exception as e:
        logger.error(f"Metin sınıflandırma hatası: {str(e)}")
        raise HTTPException(status_code=500, detail="Metin sınıflandırma başarısız.")

@app.post("/translate/")
async def translate(request: TranslationRequest):
    try:
        if request.source_language is None:
            request.source_language = translator.detect_language(request.text)
        translated_text = translator.translate(request.text, request.source_language, request.target_language)
        return {
            "translated_text": translated_text,
            "source_language": request.source_language,
            "target_language": request.target_language
        }
    except Exception as e:
        logger.error(f"Çeviri hatası: {str(e)}")
        raise HTTPException(status_code=500, detail="Çeviri başarısız.")

@app.post("/translate-multiple/")
async def translate_multiple(request: MultiTranslationRequest):
    try:
        if request.source_language is None:
            request.source_language = translator.detect_language(request.text)
        translations = {}
        for target_lang in request.target_languages:
            translated_text = translator.translate(request.text, request.source_language, target_lang)
            translations[target_lang] = translated_text
        return {
            "translations": translations,
            "source_language": request.source_language
        }
    except Exception as e:
        logger.error(f"Çoklu çeviri hatası: {str(e)}")
        raise HTTPException(status_code=500, detail="Çoklu çeviri başarısız.")

@app.get("/supported-languages/")
async def get_supported_languages():
    return {"supported_languages": translator.get_supported_languages()}

@app.post("/detect-language/")
async def detect_language(text: str):
    try:
        detected_lang = translator.detect_language(text)
        return {"detected_language": detected_lang}
    except Exception as e:
        logger.error(f"Dil tespiti hatası: {str(e)}")
        raise HTTPException(status_code=500, detail="Dil tespiti başarısız.")

@app.post("/answer-question/")
async def answer_question(input: QAInput):
    try:
        answer = question_answerer.answer(input.context, input.question)
        return {"answer": remove_extra_whitespace(answer["answer"]), "score": answer["score"]}
    except Exception as e:
        logger.error(f"Soru-cevap hatası: {str(e)}")
        raise HTTPException(status_code=500, detail="Soru-cevap işlemi başarısız.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6355)
