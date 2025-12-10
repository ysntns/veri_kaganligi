"""
Turkce Anahtar Kelime Cikarma Modulu
"""
import logging
import re
import math
from collections import Counter
from typing import Optional

import nltk
from nltk.corpus import stopwords

logger = logging.getLogger(__name__)

# NLTK verilerini indir
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class KeywordExtractor:
    """Turkce anahtar kelime cikarma sinifi"""

    # Turkce stopwords (genisletilmis)
    TURKISH_STOPWORDS = {
        've', 'ile', 'bir', 'bu', 'da', 'de', 'mi', 'mu', 'ne', 'o',
        'su', 'icin', 'gibi', 'daha', 'en', 'cok', 'kadar', 'sonra',
        'once', 'ama', 'fakat', 'ancak', 'eger', 'ki', 'hem', 'ya',
        'veya', 'ise', 'olan', 'olarak', 'uzerine', 'gore', 'tarafindan',
        'her', 'herkes', 'hep', 'bazi', 'tum', 'butun', 'sadece', 'yalniz',
        'ben', 'sen', 'biz', 'siz', 'onlar', 'bunlar', 'sunlar', 'kendi',
        'var', 'yok', 'oldu', 'olmus', 'olan', 'olmak', 'etmek', 'yapmak'
    }

    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('turkish')) | self.TURKISH_STOPWORDS
        except Exception:
            self.stop_words = self.TURKISH_STOPWORDS

    def extract(
        self,
        text: str,
        num_keywords: int = 10,
        min_word_length: int = 3,
        method: str = "tfidf"
    ) -> list[dict]:
        """
        Metinden anahtar kelimeleri cikarir.

        Args:
            text: Analiz edilecek metin
            num_keywords: Cikarilacak anahtar kelime sayisi
            min_word_length: Minimum kelime uzunlugu
            method: Cikarma yontemi ("tfidf", "frequency", "textrank")

        Returns:
            [{"keyword": str, "score": float}, ...]
        """
        # Metni temizle
        text = self._clean_text(text)
        words = text.lower().split()

        # Stopwords ve kisa kelimeleri filtrele
        filtered_words = [
            w for w in words
            if w not in self.stop_words
            and len(w) >= min_word_length
            and not w.isdigit()
        ]

        if method == "tfidf":
            keywords = self._tfidf_extract(filtered_words, num_keywords)
        elif method == "textrank":
            keywords = self._textrank_extract(text, num_keywords)
        else:
            keywords = self._frequency_extract(filtered_words, num_keywords)

        return keywords

    def _clean_text(self, text: str) -> str:
        """Metni temizler"""
        # Noktalama isaretlerini kaldir
        text = re.sub(r'[^\w\s]', ' ', text)
        # Fazla bosluklari kaldir
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _tfidf_extract(self, words: list[str], num_keywords: int) -> list[dict]:
        """TF-IDF tabanli anahtar kelime cikarma"""
        word_freq = Counter(words)
        doc_length = len(words)

        tfidf_scores = {}
        for word, freq in word_freq.items():
            tf = freq / doc_length
            # IDF yaklasimi (tek dokuman icin)
            idf = math.log(doc_length / (freq + 1)) + 1
            tfidf_scores[word] = tf * idf

        sorted_keywords = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)

        return [
            {"keyword": word, "score": round(score, 4)}
            for word, score in sorted_keywords[:num_keywords]
        ]

    def _frequency_extract(self, words: list[str], num_keywords: int) -> list[dict]:
        """Frekans tabanli anahtar kelime cikarma"""
        word_freq = Counter(words)
        total = sum(word_freq.values())

        return [
            {"keyword": word, "score": round(count / total, 4)}
            for word, count in word_freq.most_common(num_keywords)
        ]

    def _textrank_extract(self, text: str, num_keywords: int) -> list[dict]:
        """TextRank tabanli anahtar kelime cikarma (basit versiyon)"""
        sentences = re.split(r'[.!?]+', text)
        word_scores = Counter()

        for sent in sentences:
            words = [
                w.lower() for w in sent.split()
                if w.lower() not in self.stop_words and len(w) >= 3
            ]
            # Pencere icindeki kelimeleri skorla
            for i, word in enumerate(words):
                window = words[max(0, i - 2):i + 3]
                for neighbor in window:
                    if neighbor != word:
                        word_scores[word] += 1

        return [
            {"keyword": word, "score": round(score / max(word_scores.values()), 4)}
            for word, score in word_scores.most_common(num_keywords)
        ]

    def extract_phrases(self, text: str, num_phrases: int = 5) -> list[str]:
        """N-gram tabanli anahtar kelime obeği cikarma"""
        words = self._clean_text(text).lower().split()
        filtered = [w for w in words if w not in self.stop_words and len(w) >= 3]

        # Bigrams
        bigrams = [' '.join(filtered[i:i + 2]) for i in range(len(filtered) - 1)]
        bigram_freq = Counter(bigrams)

        return [phrase for phrase, _ in bigram_freq.most_common(num_phrases)]
