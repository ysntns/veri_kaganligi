"""
Turkce Duygu Analizi Modulu
"""
import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Turkce duygu analizi sinifi"""

    SENTIMENT_MAP = {
        0: "negative",
        1: "neutral",
        2: "positive",
        "LABEL_0": "negative",
        "LABEL_1": "positive",
        "negative": "negative",
        "positive": "positive",
        "neutral": "neutral"
    }

    def __init__(self, model_name: str = "savasy/bert-base-turkish-sentiment-cased"):
        self.model_name = model_name
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            logger.info(f"Sentiment modeli yukleniyor: {self.model_name}")
            self._pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.model_name
            )
        return self._pipeline

    def analyze(self, text: str) -> dict:
        """
        Metnin duygusunu analiz eder.

        Args:
            text: Analiz edilecek metin

        Returns:
            {"sentiment": "positive/negative/neutral", "score": float}
        """
        try:
            result = self.pipeline(text[:512])[0]
            sentiment = self.SENTIMENT_MAP.get(result['label'], result['label'])
            return {
                "sentiment": sentiment,
                "score": round(result['score'], 4)
            }
        except Exception as e:
            logger.error(f"Duygu analizi hatasi: {e}")
            return self._rule_based_analysis(text)

    def _rule_based_analysis(self, text: str) -> dict:
        """Kural tabanli duygu analizi (fallback)"""
        positive_words = {
            'iyi', 'guzel', 'harika', 'mukemmel', 'super', 'basarili',
            'mutlu', 'sevindirici', 'hos', 'tatli', 'keyifli', 'olumlu'
        }
        negative_words = {
            'kotu', 'berbat', 'korkunc', 'uzucu', 'basarisiz', 'mutsuz',
            'sinir', 'kirgin', 'hayal kirikligi', 'olumsuz', 'sikici'
        }

        words = text.lower().split()
        pos_count = sum(1 for w in words if w in positive_words)
        neg_count = sum(1 for w in words if w in negative_words)

        if pos_count > neg_count:
            return {"sentiment": "positive", "score": 0.7}
        elif neg_count > pos_count:
            return {"sentiment": "negative", "score": 0.7}
        return {"sentiment": "neutral", "score": 0.5}


class EntitySentimentAnalyzer:
    """Varlik bazli duygu analizi sinifi"""

    def __init__(self):
        self._ner_pipeline = None
        self._sentiment_analyzer = SentimentAnalyzer()

    @property
    def ner_pipeline(self):
        if self._ner_pipeline is None:
            logger.info("NER modeli yukleniyor...")
            self._ner_pipeline = pipeline(
                "ner",
                model="savasy/bert-base-turkish-ner-cased",
                aggregation_strategy="simple"
            )
        return self._ner_pipeline

    def analyze(self, text: str) -> dict:
        """
        Metindeki varliklarin duygusunu analiz eder.

        Args:
            text: Analiz edilecek metin

        Returns:
            {"entity_list": [...], "results": [{"entity": ..., "sentiment": ...}]}
        """
        try:
            # Varliklari cikar
            entities = self.ner_pipeline(text)
            unique_entities = list(set(e['word'].replace('##', '') for e in entities))

            # Her varlik icin duygu analizi
            results = []
            for entity in unique_entities[:10]:  # Maksimum 10 varlik
                # Varlik iceren cumleyi bul
                sentences = text.split('.')
                entity_sentence = next(
                    (s for s in sentences if entity.lower() in s.lower()),
                    text[:200]
                )
                sentiment = self._sentiment_analyzer.analyze(entity_sentence)
                results.append({
                    "entity": entity,
                    "sentiment": sentiment['sentiment']
                })

            return {
                "entity_list": unique_entities,
                "results": results
            }

        except Exception as e:
            logger.error(f"Varlik duygu analizi hatasi: {e}")
            return {"entity_list": [], "results": []}
