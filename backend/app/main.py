from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html

from services import pdf_service
from models import summarizer, translator, sentiment_analyzer, keyword_extractor, text_classifier, question_answerer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Docs",
        oauth2_redirect_url=None,
        swagger_js_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.37.2/swagger-ui-bundle.js",
        swagger_css_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.37.2/swagger-ui.css",
    )


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        content = await file.read()
        return pdf_service.extract_text_and_tables(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize/")
async def summarize(text: str):
    try:
        return {"summary": summarizer.summarize(text)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate/")
async def translate(text: str, target_language: str):
    try:
        return {"translated": translator.translate(text, target_language)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-sentiment/")
async def analyze_sentiment(text: str):
    try:
        return {"sentiment": sentiment_analyzer.analyze(text)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-keywords/")
async def extract_keywords(text: str):
    try:
        return {"keywords": keyword_extractor.extract(text)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/classify-text/")
async def classify_text(text: str):
    try:
        return {"classification": text_classifier.classify(text)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/answer-question/")
async def answer_question(context: str, question: str):
    try:
        return {"answer": question_answerer.answer(context, question)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
