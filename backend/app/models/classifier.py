"""
Turkce Metin Siniflandirma Modulu
"""
import logging
from transformers import pipeline

logger = logging.getLogger(__name__)


class TextClassifier:
    """Turkce metin siniflandirma sinifi"""

    CATEGORIES = {
        "LABEL_0": "ekonomi",
        "LABEL_1": "spor",
        "LABEL_2": "politika",
        "LABEL_3": "teknoloji",
        "LABEL_4": "kultur-sanat",
        "LABEL_5": "saglik",
        "LABEL_6": "egitim"
    }

    def __init__(self, model_name: str = "savasy/bert-turkish-text-classification"):
        self.model_name = model_name
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            logger.info(f"Siniflandirma modeli yukleniyor: {self.model_name}")
            self._pipeline = pipeline(
                "text-classification",
                model=self.model_name,
                tokenizer=self.model_name
            )
        return self._pipeline

    def classify(self, text: str, top_k: int = 3) -> dict:
        """
        Metni kategorilere siniflandirir.

        Args:
            text: Siniflandirilacak metin
            top_k: Dondurulecek en yuksek k kategori

        Returns:
            {"category": str, "score": float, "all_scores": [...]}
        """
        try:
            results = self.pipeline(text[:512], top_k=top_k)

            # Sonuclari duzenle
            all_scores = []
            for r in results:
                category = self.CATEGORIES.get(r['label'], r['label'])
                all_scores.append({
                    "category": category,
                    "score": round(r['score'], 4)
                })

            top_result = all_scores[0] if all_scores else {"category": "belirsiz", "score": 0.0}

            return {
                "category": top_result['category'],
                "score": top_result['score'],
                "all_scores": all_scores
            }

        except Exception as e:
            logger.error(f"Siniflandirma hatasi: {e}")
            return self._keyword_classification(text)

    def _keyword_classification(self, text: str) -> dict:
        """Anahtar kelime tabanli siniflandirma (fallback)"""
        keywords = {
            "ekonomi": {"dolar", "euro", "borsa", "faiz", "enflasyon", "banka", "kredi"},
            "spor": {"mac", "gol", "takim", "sampiyona", "futbol", "basketbol", "sampion"},
            "politika": {"secim", "parti", "hukumet", "meclis", "cumhurbaskani", "milletvekili"},
            "teknoloji": {"yazilim", "bilgisayar", "internet", "yapay", "zeka", "robot", "dijital"},
            "saglik": {"hastane", "doktor", "ilac", "tedavi", "virus", "hastalik", "saglik"}
        }

        words = set(text.lower().split())
        scores = {cat: len(words & kws) for cat, kws in keywords.items()}

        if max(scores.values()) > 0:
            category = max(scores, key=scores.get)
            return {"category": category, "score": 0.6, "all_scores": []}

        return {"category": "genel", "score": 0.5, "all_scores": []}
