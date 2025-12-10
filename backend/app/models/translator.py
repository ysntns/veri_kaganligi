"""
Coklu Dil Ceviri Modulu
"""
import logging
from transformers import MarianMTModel, MarianTokenizer

logger = logging.getLogger(__name__)


class TranslationService:
    """Coklu dil ceviri servisi"""

    SUPPORTED_LANGUAGES = {
        'tr': 'Turkce',
        'en': 'Ingilizce',
        'de': 'Almanca',
        'fr': 'Fransizca',
        'es': 'Ispanyolca',
        'it': 'Italyanca',
        'ru': 'Rusca',
        'ar': 'Arapca',
        'zh': 'Cince',
        'ja': 'Japonca',
        'ko': 'Korece',
        'nl': 'Felemenkce',
        'pt': 'Portekizce',
        'pl': 'Lehce',
        'uk': 'Ukraynaca'
    }

    def __init__(self):
        self._models = {}

    def _get_model_name(self, source: str, target: str) -> str:
        """Helsinki-NLP model adini olusturur"""
        return f"Helsinki-NLP/opus-mt-{source}-{target}"

    def _load_model(self, source: str, target: str):
        """Modeli lazy loading ile yukler"""
        model_key = f"{source}-{target}"

        if model_key not in self._models:
            try:
                model_name = self._get_model_name(source, target)
                logger.info(f"Ceviri modeli yukleniyor: {model_name}")

                tokenizer = MarianTokenizer.from_pretrained(model_name)
                model = MarianMTModel.from_pretrained(model_name)
                self._models[model_key] = (tokenizer, model)

            except Exception as e:
                logger.warning(f"Direkt model bulunamadi ({model_key}), pivot kullanilacak: {e}")
                return None

        return self._models.get(model_key)

    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str
    ) -> str:
        """
        Metni kaynak dilden hedef dile cevirir.

        Args:
            text: Cevirilecek metin
            source_language: Kaynak dil kodu (tr, en, de, ...)
            target_language: Hedef dil kodu

        Returns:
            Cevrilmis metin
        """
        if source_language == target_language:
            return text

        # Direkt ceviri dene
        model = self._load_model(source_language, target_language)

        if model is None:
            # Pivot dil olarak Ingilizce kullan
            return self._pivot_translate(text, source_language, target_language)

        tokenizer, model = model

        try:
            inputs = tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            translated = model.generate(**inputs, max_length=512)
            return tokenizer.decode(translated[0], skip_special_tokens=True)

        except Exception as e:
            logger.error(f"Ceviri hatasi: {e}")
            raise

    def _pivot_translate(self, text: str, source: str, target: str) -> str:
        """Ingilizce uzerinden pivot ceviri"""
        if source != 'en':
            text = self.translate(text, source, 'en')
        if target != 'en':
            text = self.translate(text, 'en', target)
        return text

    def detect_language(self, text: str) -> str:
        """Metnin dilini tespit eder"""
        special_chars = {
            'tr': set('cigosucCGIOSU'),
            'de': set('aouAOU'),
            'fr': set('aceeiouACEEIOU'),
            'es': set('aeiounAEIOUN'),
            'ru': set(''),
            'ar': set(''),
            'zh': set(''),
            'ja': set(''),
            'ko': set('')
        }

        # Turkce karakterler
        if any(c in text for c in 'cigosucCGIOSU'):
            return 'tr'

        # Diger diller icin basit kontrol
        common_words = {
            'en': {'the', 'is', 'are', 'was', 'have', 'has', 'been', 'will'},
            'de': {'der', 'die', 'das', 'und', 'ist', 'sind', 'war', 'haben'},
            'fr': {'le', 'la', 'les', 'est', 'sont', 'avoir', 'etre', 'dans'},
            'es': {'el', 'la', 'los', 'es', 'son', 'estar', 'tener', 'para'}
        }

        words = set(text.lower().split())
        scores = {lang: len(words & word_set) for lang, word_set in common_words.items()}

        if max(scores.values()) > 0:
            return max(scores, key=scores.get)

        return 'en'  # Varsayilan

    def get_supported_languages(self) -> dict:
        """Desteklenen dilleri dondurur"""
        return self.SUPPORTED_LANGUAGES
