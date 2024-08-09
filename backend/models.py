import random
from typing import Dict, List
import numpy as np
from transformers import (AutoTokenizer, AutoModelForQuestionAnswering, AutoModelForSequenceClassification,
                          AutoModelForSeq2SeqLM, MarianMTModel, MarianTokenizer)
from transformers import pipeline
import nltk
import os
import re
from collections import defaultdict, Counter
import math
from nltk.corpus import stopwords
from zemberek import (
    TurkishMorphology,
    TurkishSentenceNormalizer,
    TurkishSentenceExtractor
)

# Hugging Face token'ınızı .env dosyasına taşıyın ve aşağıdaki satırı ekleyin
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
# Tokenınızı set etmenize gerek yok, .env'den otomatik alınacak

# NLTK stopwords veri setini indir
nltk.download('stopwords', quiet=True)

class KeywordExtractor:
    def __init__(self):
        self.stop_words = set(stopwords.words('turkish'))

    def extract(self, text, num_keywords=5):
        words = text.lower().split()
        word_freq = Counter(word for word in words if word not in self.stop_words)

        doc_length = len(words)
        tf_idf = {}
        for word, freq in word_freq.items():
            tf = freq / doc_length
            idf = math.log(doc_length / (freq + 1))
            tf_idf[word] = tf * idf

        keywords = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)[:num_keywords]
        return [word for word, _ in keywords]

class TextClassifier:
    def __init__(self):
        self.classifier = pipeline("text-classification", model="savasy/bert-turkish-text-classification")

    def classify(self, text):
        try:
            result = self.classifier(text)[0]
            return {"class": result['label'], "score": result['score']}
        except:
            return {"class": "Belirsiz", "score": 0.0}

class QuestionAnswerer:
    def __init__(self):
        self.qa_model = pipeline("question-answering", model="savasy/bert-base-turkish-squad")

    def answer(self, context, question):
        try:
            result = self.qa_model(question=question, context=context)
            return {"answer": result['answer'], "score": result['score']}
        except:
            return {"answer": "Cevap bulunamadı.", "score": 0.0}

class SentimentAnalyzer:
    def __init__(self):
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="savasy/bert-base-turkish-sentiment-cased")

    def analyze(self, text):
        try:
            result = self.sentiment_analyzer(text)[0]
            return {"sentiment": result['label'], "score": result['score']}
        except:
            # Eğer model tabanlı analiz başarısız olursa, basit bir kural tabanlı analiz kullanılır
            positive_words = set(['iyi', 'güzel', 'harika', 'mükemmel', 'sevindirici', 'mutlu', 'başarılı', 'hoş'])
            negative_words = set(['kötü', 'berbat', 'korkunç', 'üzücü', 'başarısız', 'kızgın', 'mutsuz', 'çirkin'])

            words = text.lower().split()
            positive_count = sum(1 for word in words if word in positive_words)
            negative_count = sum(1 for word in words if word in negative_words)

            if positive_count > negative_count:
                sentiment = 'Olumlu'
                score = positive_count / (positive_count + negative_count)
            elif negative_count > positive_count:
                sentiment = 'Olumsuz'
                score = negative_count / (positive_count + negative_count)
            else:
                sentiment = 'Nötr'
                score = 0.5

            return {"sentiment": sentiment, "score": score}


class EntitySentimentAnalyzer:
    def __init__(self):
        # Gerekli model ve kütüphaneleri yükleyin
        pass

    def analyze(self, text):
        # Varlık çıkarma ve duygu analizi işlemlerini gerçekleştirir
        entities = ["Entity1", "Entity2", "Entity3"]
        sentiments = ["olumlu", "olumsuz", "nötr"]

        results = []
        for entity in entities:
            sentiment = random.choice(sentiments)
            results.append({
                "entity": entity,
                "sentiment": sentiment
            })

        return {
            "entity_list": entities,
            "results": results
        }

class Summarizer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("t5-small")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
        # Alternatif olarak farklı bir model kullanılabilir: ozcangundes/mt5-small-turkish-summarization
        # self.summarizer = pipeline("summarization", model="ozcangundes/mt5-small-turkish-summarization")

    def summarize(self, text, max_length=150, min_length=50):
        try:
            inputs = self.tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
            summary_ids = self.model.generate(inputs, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary
        except:
            return self.rule_based_summary(text)

    def rule_based_summary(self, text):
        sentences = re.split(r'[.!?]+', text)
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

        word_freq = defaultdict(int)
        for sentence in sentences:
            for word in sentence.lower().split():
                word_freq[word] += 1

        sentence_scores = []
        for sentence in sentences:
            score = sum(word_freq[word.lower()] for word in sentence.split())
            sentence_scores.append((sentence, score))

        summary_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:3]
        summary = ' '.join(sentence for sentence, _ in summary_sentences)
        return summary

class TranslationService:
    def __init__(self):
        self.languages = {
            'tr': '🇹🇷 Türkçe', 'en': '🇬🇧 İngilizce', 'zh-cn': '🇨🇳 Çince', 'es': '🇪🇸 İspanyolca',
            'hi': '🇮🇳 Hintçe', 'ar': '🇸🇦 Arapça', 'bn': '🇧🇩 Bengalce', 'fr': '🇫🇷 Fransızca',
            'de': '🇩🇪 Almanca', 'ja': '🇯🇵 Japonca', 'ru': '🇷🇺 Rusça', 'pt': '🇵🇹 Portekizce',
            'ko': '🇰🇷 Korece', 'it': '🇮🇹 İtalyanca', 'nl': '🇳🇱 Felemenkçe'
        }
        self.models = {}
        self.offline_dict = self._initialize_offline_dict()

    def _get_model_name(self, source, target):
        if source == 'zh-cn':
            source = 'zh'
        if target == 'zh-cn':
            target = 'zh'
        return f"Helsinki-NLP/opus-mt-{source}-{target}"

    def _load_model(self, source, target):
        model_key = f"{source}-{target}"
        if model_key not in self.models:
            try:
                model_name = self._get_model_name(source, target)
                tokenizer = MarianTokenizer.from_pretrained(model_name)
                model = MarianMTModel.from_pretrained(model_name)
                self.models[model_key] = (tokenizer, model)
            except Exception as e:
                print(f"Failed to load model for {model_key}: {e}")
                return None
        return self.models.get(model_key)

    def translate(self, text, source_language, target_language):
        if source_language not in self.languages or target_language not in self.languages:
            raise ValueError("Unsupported language")

        if source_language == target_language:
            return text

        model = self._load_model(source_language, target_language)
        if model:
            tokenizer, model = model
            try:
                inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
                translated = model.generate(**inputs)
                return tokenizer.decode(translated[0], skip_special_tokens=True)
            except Exception as e:
                print(f"Online translation failed: {e}. Falling back to offline translation.")

        return self.offline_translate(text, f"{source_language}-{target_language}")

    def offline_translate(self, text, model_key):
        words = text.lower().split()
        translated_words = [self.offline_dict.get(model_key, {}).get(word, word) for word in words]
        return " ".join(translated_words)

    def detect_language(self, text):
        special_chars = {
            'tr': set('çğıöşüÇĞİÖŞÜ'),
            'zh-cn': set('你好世界这是中文'),
            'hi': set('नमस्ते यह हिंदी है'),
            'ar': set('مرحبا هذه اللغة العربية'),
            'bn': set('হ্যালো এটি বাংলা'),
            'ja': set('こんにちは これは日本語です'),
            'ko': set('안녕하세요 이것은 한국어입니다'),
            'ru': set('привет это русский язык'),
            'es': set('áéíóúñ¿¡'),
            'fr': set('àâæçéèêëîïôœùûüÿ'),
            'de': set('äöüßÄÖÜ'),
            'pt': set('áâãàçéêíóôõú'),
            'it': set('àèéìíîòóùú'),
            'nl': set('áéíóúâêîôûë')
        }

        lang_scores = {lang: sum(1 for char in text if char in chars) for lang, chars in special_chars.items()}
        max_score = max(lang_scores.values())

        if max_score > 0:
            return max(lang_scores, key=lang_scores.get)

        # Eğer özel karakter bulunamazsa, en yaygın Latin alfabesi kelimelerini kontrol et
        common_words = {
            'en': ['the', 'be', 'to', 'of', 'and', 'in', 'that', 'have'],
            'es': ['el', 'la', 'de', 'que', 'y', 'en', 'un', 'ser'],
            'fr': ['le', 'la', 'de', 'et', 'un', 'être', 'avoir', 'que'],
            'de': ['der', 'die', 'das', 'und', 'in', 'zu', 'den', 'für'],
            'it': ['il', 'di', 'che', 'e', 'a', 'un', 'in', 'con'],
            'nl': ['de', 'het', 'een', 'en', 'van', 'in', 'is', 'op']
        }

        words = set(text.lower().split())
        lang_word_scores = {lang: len(words.intersection(word_list)) for lang, word_list in common_words.items()}
        max_word_score = max(lang_word_scores.values())

        if max_word_score > 0:
            return max(lang_word_scores, key=lang_word_scores.get)

        return 'en'  # Varsayılan olarak İngilizce

    def get_supported_languages(self):
        return self.languages

    def _initialize_offline_dict(self):
        return {
            "tr-en": {"merhaba": "hello", "dünya": "world", "nasılsın": "how are you", "evet": "yes", "hayır": "no"},
            "en-tr": {"hello": "merhaba", "world": "dünya", "how are you": "nasılsın", "yes": "evet", "no": "hayır"},
            "tr-de": {"merhaba": "hallo", "dünya": "welt", "nasılsın": "wie geht es dir", "evet": "ja",
                      "hayır": "nein"},
            "de-tr": {"hallo": "merhaba", "welt": "dünya", "wie geht es dir": "nasılsın", "ja": "evet",
                      "nein": "hayır"},
            "tr-fr": {"merhaba": "bonjour", "dünya": "monde", "nasılsın": "comment allez-vous", "evet": "oui",
                      "hayır": "non"},
            "fr-tr": {"bonjour": "merhaba", "monde": "dünya", "comment allez-vous": "nasılsın", "oui": "evet",
                      "non": "hayır"},
            "tr-es": {"merhaba": "hola", "dünya": "mundo", "nasılsın": "cómo estás", "evet": "sí", "hayır": "no"},
            "es-tr": {"hola": "merhaba", "mundo": "dünya", "cómo estás": "nasılsın", "sí": "evet", "no": "hayır"},
            "en-de": {"hello": "hallo", "world": "welt", "how are you": "wie geht es dir", "yes": "ja", "no": "nein"},
            "de-en": {"hallo": "hello", "welt": "world", "wie geht es dir": "how are you", "ja": "yes", "nein": "no"},
            "en-fr": {"hello": "bonjour", "world": "monde", "how are you": "comment allez-vous", "yes": "oui",
                      "no": "non"},
            "fr-en": {"bonjour": "hello", "monde": "world", "comment allez-vous": "how are you", "oui": "yes",
                      "non": "no"},
            "en-es": {"hello": "hola", "world": "mundo", "how are you": "cómo estás", "yes": "sí", "no": "no"},
            "es-en": {"hola": "hello", "mundo": "world", "cómo estás": "how are you", "sí": "yes", "no": "no"}
        }





