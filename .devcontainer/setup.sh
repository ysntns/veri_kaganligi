#!/bin/bash
set -e

echo "🚀 Veri Kaganligi - Kurulum Basliyor..."

# Backend kurulumu
echo "📦 Backend bagimliliklari yukleniyor..."
cd /workspace/backend
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# NLTK verilerini indir
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Frontend kurulumu
echo "📦 Frontend bagimliliklari yukleniyor..."
cd /workspace/frontend
npm install

echo "✅ Kurulum tamamlandi!"
echo ""
echo "🎯 Calistirmak icin:"
echo "   Backend:  cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "   Frontend: cd frontend && npm start"
