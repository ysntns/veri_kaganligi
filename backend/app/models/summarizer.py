"""
Turkce Metin Ozetleme Modulu
"""
import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

logger = logging.getLogger(__name__)


class Summarizer:
    """Turkce metin ozetleme sinifi"""

    def __init__(self, model_name: str = "ozcangundes/mt5-small-turkish-summarization"):
        self.model_name = model_name
        self._tokenizer = None
        self._model = None

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            logger.info(f"Tokenizer yukleniyor: {self.model_name}")
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        return self._tokenizer

    @property
    def model(self):
        if self._model is None:
            logger.info(f"Model yukleniyor: {self.model_name}")
            self._model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        return self._model

    def summarize(
        self,
        text: str,
        max_length: int = 150,
        min_length: int = 50,
        num_beams: int = 4
    ) -> str:
        """
        Metni ozetler.

        Args:
            text: Ozetlenecek metin
            max_length: Maksimum ozet uzunlugu
            min_length: Minimum ozet uzunlugu
            num_beams: Beam search sayisi

        Returns:
            Ozetlenmis metin
        """
        try:
            inputs = self.tokenizer.encode(
                "ozetle: " + text,
                return_tensors="pt",
                max_length=512,
                truncation=True
            )

            summary_ids = self.model.generate(
                inputs,
                max_length=max_length,
                min_length=min_length,
                length_penalty=2.0,
                num_beams=num_beams,
                early_stopping=True
            )

            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary

        except Exception as e:
            logger.error(f"Ozetleme hatasi: {e}")
            return self._extractive_summary(text)

    def _extractive_summary(self, text: str, num_sentences: int = 3) -> str:
        """Basit cumleciksel ozetleme (fallback)"""
        import re
        from collections import Counter

        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if len(sentences) <= num_sentences:
            return text

        # TF-IDF benzeri puanlama
        words = text.lower().split()
        word_freq = Counter(words)

        sentence_scores = []
        for sent in sentences:
            score = sum(word_freq[w.lower()] for w in sent.split())
            sentence_scores.append((sent, score))

        top_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:num_sentences]
        return '. '.join(s for s, _ in top_sentences) + '.'
