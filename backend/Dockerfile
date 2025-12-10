FROM python:3.11-slim

# Sistem bagimliliklari
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-tur \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Calisma dizini
WORKDIR /app

# Python bagimliliklari
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# NLTK verileri
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Uygulama kodlari
COPY . .

# Port
EXPOSE 8000

# Baslat
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
