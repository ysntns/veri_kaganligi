import axios from 'axios';

// API Base URL - development'ta proxy kullanilacak
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api/v1';

// Axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 saniye timeout
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Gerekirse auth token eklenebilir
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.detail || error.message || 'Bir hata olustu';
    console.error('API Hatasi:', message);
    return Promise.reject(new Error(message));
  }
);

// NLP API Fonksiyonlari
export const nlpApi = {
  // Metin Ozetleme
  summarize: (text, maxLength = 150, minLength = 50) =>
    api.post('/summarize', { text, max_length: maxLength, min_length: minLength }),

  // Duygu Analizi
  analyzeSentiment: (text) =>
    api.post('/analyze-sentiment', { text }),

  // Varlik Bazli Duygu Analizi
  analyzeEntitySentiment: (text) =>
    api.post('/analyze-entity-sentiment', { text }),

  // Anahtar Kelime Cikarma
  extractKeywords: (text, numKeywords = 10, method = 'tfidf') =>
    api.post('/extract-keywords', { text, num_keywords: numKeywords, method }),

  // Metin Siniflandirma
  classifyText: (text) =>
    api.post('/classify-text', { text }),

  // Varlik Tanima (NER)
  recognizeEntities: (text) =>
    api.post('/recognize-entities', { text }),

  // Soru-Cevap
  answerQuestion: (context, question) =>
    api.post('/answer-question', { context, question }),
};

// Ceviri API Fonksiyonlari
export const translationApi = {
  // Tekli Ceviri
  translate: (text, targetLanguage, sourceLanguage = null) =>
    api.post('/translate', {
      text,
      target_language: targetLanguage,
      source_language: sourceLanguage,
    }),

  // Coklu Ceviri
  translateMultiple: (text, targetLanguages, sourceLanguage = null) =>
    api.post('/translate-multiple', {
      text,
      target_languages: targetLanguages,
      source_language: sourceLanguage,
    }),

  // Dil Tespiti
  detectLanguage: (text) =>
    api.post('/detect-language', { text }),

  // Desteklenen Diller
  getSupportedLanguages: () =>
    api.get('/supported-languages'),
};

// Dosya Isleme API Fonksiyonlari
export const fileApi = {
  // PDF Yukleme
  uploadPdf: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/upload-pdf', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  // Genel Dosya Yukleme
  uploadFile: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/upload-file', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

// Eski API uyumlulugu icin
export const apiRequest = async (endpoint, method = 'GET', data = null) => {
  try {
    if (method === 'GET') {
      return await api.get(endpoint);
    }
    return await api.post(endpoint, data);
  } catch (error) {
    throw error;
  }
};

export default api;
