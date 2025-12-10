"""
Turkce Soru-Cevap Modulu
"""
import logging
from transformers import pipeline

logger = logging.getLogger(__name__)


class QuestionAnswerer:
    """Turkce soru-cevap sinifi"""

    def __init__(self, model_name: str = "savasy/bert-base-turkish-squad"):
        self.model_name = model_name
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            logger.info(f"QA modeli yukleniyor: {self.model_name}")
            self._pipeline = pipeline(
                "question-answering",
                model=self.model_name,
                tokenizer=self.model_name
            )
        return self._pipeline

    def answer(self, context: str, question: str) -> dict:
        """
        Verilen baglam icerisinde soruyu cevaplar.

        Args:
            context: Cevabi iceren metin/baglam
            question: Cevaplanacak soru

        Returns:
            {"answer": str, "score": float, "start": int, "end": int}
        """
        try:
            result = self.pipeline(
                question=question,
                context=context[:2000]  # Maksimum baglam uzunlugu
            )

            return {
                "answer": result['answer'],
                "score": round(result['score'], 4),
                "start": result['start'],
                "end": result['end']
            }

        except Exception as e:
            logger.error(f"Soru-cevap hatasi: {e}")
            return {
                "answer": "Cevap bulunamadi.",
                "score": 0.0,
                "start": 0,
                "end": 0
            }

    def answer_multiple(self, context: str, questions: list[str]) -> list[dict]:
        """Birden fazla soruyu cevaplar"""
        return [self.answer(context, q) for q in questions]
