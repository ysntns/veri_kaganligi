# Veri Kaganligi - Turkce NLP Platformu

> **Teknofest 2024 Turkce Dogal Dil Isleme Yarismasi Finalist Projesi**

Turkce metinler uzerinde kapsamli dogal dil isleme (NLP) islemleri gerceklestiren modern bir web uygulamasi.

## Ozellikler

| Ozellik | Aciklama | Model |
|---------|----------|-------|
| **Metin Ozetleme** | Uzun metinleri otomatik ozetler | mT5-Turkish |
| **Duygu Analizi** | Pozitif/Negatif/Notr siniflandirma | BERT-Turkish-Sentiment |
| **Metin Siniflandirma** | Kategori tahmini (ekonomi, spor, politika, teknoloji) | BERT-Turkish-Classification |
| **Soru-Cevap** | Baglam icinde soru cevaplama | BERT-Turkish-SQuAD |
| **Anahtar Kelime** | TF-IDF, TextRank tabanli cikarma | Custom |
| **Varlik Tanima (NER)** | Kisi, yer, organizasyon tespiti | BERT-Turkish-NER |
| **Ceviri** | 15+ dil destegi | Helsinki-NLP/OPUS |
| **PDF Isleme** | Metin ve tablo cikarma, OCR destegi | PyMuPDF + pdfplumber |

## Proje Yapisi

```
veri_kaganligi/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoint'leri
│   │   ├── models/        # NLP modelleri
│   │   ├── services/      # PDF ve dosya servisleri
│   │   ├── config.py      # Konfigürasyon
│   │   └── main.py        # FastAPI uygulamasi
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # React componentleri
│   │   ├── utils/         # API fonksiyonlari
│   │   └── styles/        # CSS/Styled Components
│   └── package.json
├── data/                  # Ornek veriler
└── tests/                 # Test dosyalari
```

## Kurulum

### Backend

```bash
# Sanal ortam olustur
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bagimliliklari yukle
cd backend
pip install -r requirements.txt

# Uygulamayi baslat
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Bagimliliklari yukle
yarn install  # veya npm install

# Uygulamayi baslat
yarn start    # veya npm start
```

## API Kullanimi

API dokumantasyonuna `http://localhost:8000/docs` adresinden erisebilirsiniz.

### Ornek Istekler

**Metin Ozetleme:**
```bash
curl -X POST "http://localhost:8000/api/v1/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Ozetlenecek uzun metin...", "max_length": 150}'
```

**Duygu Analizi:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze-sentiment" \
  -H "Content-Type: application/json" \
  -d '{"text": "Bu urun cok guzel!"}'
```

**Soru-Cevap:**
```bash
curl -X POST "http://localhost:8000/api/v1/answer-question" \
  -H "Content-Type: application/json" \
  -d '{"context": "Ankara Turkiyenin baskentidir.", "question": "Turkiyenin baskenti neresidir?"}'
```

## API Endpoint'leri

### NLP
- `POST /api/v1/summarize` - Metin ozetleme
- `POST /api/v1/analyze-sentiment` - Duygu analizi
- `POST /api/v1/analyze-entity-sentiment` - Varlik bazli duygu analizi
- `POST /api/v1/extract-keywords` - Anahtar kelime cikarma
- `POST /api/v1/classify-text` - Metin siniflandirma
- `POST /api/v1/recognize-entities` - Varlik tanima (NER)
- `POST /api/v1/answer-question` - Soru-cevap

### Ceviri
- `POST /api/v1/translate` - Tekli ceviri
- `POST /api/v1/translate-multiple` - Coklu dil cevirisi
- `POST /api/v1/detect-language` - Dil tespiti
- `GET /api/v1/supported-languages` - Desteklenen diller

### Dosya Isleme
- `POST /api/v1/upload-pdf` - PDF yukleme ve isleme
- `POST /api/v1/upload-file` - Genel dosya yukleme (PDF, CSV, Excel, Word)

## Teknolojiler

### Backend
- **FastAPI** - Modern, yuksek performansli web framework
- **Transformers** - HuggingFace NLP modelleri
- **PyTorch** - Derin ogrenme kutuphanesi
- **PyMuPDF & pdfplumber** - PDF isleme

### Frontend
- **React 18** - UI kutuphanesi
- **Material-UI** - Component kutuphanesi
- **Styled Components** - CSS-in-JS
- **Axios** - HTTP istemcisi

### NLP Modelleri
- `savasy/bert-base-turkish-sentiment-cased`
- `savasy/bert-turkish-text-classification`
- `savasy/bert-base-turkish-squad`
- `savasy/bert-base-turkish-ner-cased`
- `ozcangundes/mt5-small-turkish-summarization`
- `Helsinki-NLP/opus-mt-*`

## Gelistirici

**Yasin Tanis** - [@ysntns](https://github.com/ysntns)

## Lisans

Bu proje Apache License 2.0 altinda lisanslanmistir. Detaylar icin [LICENSE](LICENSE) dosyasina bakiniz.

---

*Teknofest 2024 Turkce Dogal Dil Isleme Yarismasi icin gelistirilmistir.*
