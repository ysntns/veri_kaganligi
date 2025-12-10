"""
Veri Kaganligi - Turkce NLP API
Teknofest 2024 NLP Yarismasi Finalist Projesi

Ana FastAPI uygulamasi
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .config import get_settings
from .api import router

# Logging ayarlari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama yasam dongusu"""
    logger.info("Veri Kaganligi API baslatiliyor...")
    yield
    logger.info("Veri Kaganligi API kapatiliyor...")


# FastAPI uygulamasi
settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## Turkce Dogal Dil Isleme API'si

    Bu API, Turkce metinler uzerinde cesitli NLP islemlerini gerceklestirmek icin tasarlanmistir.

    ### Ozellikler:
    - **Metin Ozetleme**: Uzun metinleri otomatik ozetler
    - **Duygu Analizi**: Metinlerin duygusal tonunu analiz eder
    - **Metin Siniflandirma**: Metinleri kategorilere ayirir
    - **Soru-Cevap**: Baglam icerisinde sorulari cevaplar
    - **Anahtar Kelime Cikarma**: Onemli kelimeleri tespit eder
    - **Varlik Tanima (NER)**: Kisi, yer ve organizasyonlari bulur
    - **Ceviri**: Turkce'den diger dillere ve tersine ceviri
    - **PDF Isleme**: PDF'lerden metin ve tablo cikarma

    ### Teknofest 2024 NLP Yarismasi Finalist Projesi
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS ayarlari
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API router'ini ekle
app.include_router(router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
async def root():
    """Ana sayfa - API dokumantasyonuna yonlendir"""
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["Sistem"])
async def health_check():
    """Sistem saglik kontrolu"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "service": settings.APP_NAME
    }


@app.get("/api/v1", tags=["Sistem"])
async def api_info():
    """API bilgileri"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "endpoints": {
            "nlp": [
                "/api/v1/summarize",
                "/api/v1/analyze-sentiment",
                "/api/v1/analyze-entity-sentiment",
                "/api/v1/extract-keywords",
                "/api/v1/classify-text",
                "/api/v1/recognize-entities",
                "/api/v1/answer-question"
            ],
            "translation": [
                "/api/v1/translate",
                "/api/v1/translate-multiple",
                "/api/v1/detect-language",
                "/api/v1/supported-languages"
            ],
            "file_processing": [
                "/api/v1/upload-pdf",
                "/api/v1/upload-file"
            ]
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
