"""
Turkce Adlandirilmis Varlik Tanima (NER) Modulu
"""
import logging
from transformers import pipeline

logger = logging.getLogger(__name__)


class NamedEntityRecognizer:
    """Turkce NER sinifi"""

    ENTITY_LABELS = {
        "PER": "Kisi",
        "LOC": "Yer",
        "ORG": "Organizasyon",
        "MISC": "Diger",
        "B-PER": "Kisi",
        "I-PER": "Kisi",
        "B-LOC": "Yer",
        "I-LOC": "Yer",
        "B-ORG": "Organizasyon",
        "I-ORG": "Organizasyon"
    }

    def __init__(self, model_name: str = "savasy/bert-base-turkish-ner-cased"):
        self.model_name = model_name
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            logger.info(f"NER modeli yukleniyor: {self.model_name}")
            self._pipeline = pipeline(
                "ner",
                model=self.model_name,
                tokenizer=self.model_name,
                aggregation_strategy="simple"
            )
        return self._pipeline

    def recognize(self, text: str) -> dict:
        """
        Metindeki varliklari tanir.

        Args:
            text: Analiz edilecek metin

        Returns:
            {
                "entities": [{"text": str, "type": str, "score": float}],
                "persons": [...],
                "locations": [...],
                "organizations": [...]
            }
        """
        try:
            results = self.pipeline(text)

            entities = []
            persons = []
            locations = []
            organizations = []

            for entity in results:
                entity_type = self.ENTITY_LABELS.get(
                    entity['entity_group'],
                    entity['entity_group']
                )
                entity_text = entity['word'].replace('##', '')

                entity_dict = {
                    "text": entity_text,
                    "type": entity_type,
                    "score": round(entity['score'], 4)
                }
                entities.append(entity_dict)

                # Kategorilere ayir
                if entity_type == "Kisi":
                    persons.append(entity_text)
                elif entity_type == "Yer":
                    locations.append(entity_text)
                elif entity_type == "Organizasyon":
                    organizations.append(entity_text)

            return {
                "entities": entities,
                "persons": list(set(persons)),
                "locations": list(set(locations)),
                "organizations": list(set(organizations))
            }

        except Exception as e:
            logger.error(f"NER hatasi: {e}")
            return {
                "entities": [],
                "persons": [],
                "locations": [],
                "organizations": []
            }

    def extract_persons(self, text: str) -> list[str]:
        """Sadece kisileri cikarir"""
        return self.recognize(text)['persons']

    def extract_locations(self, text: str) -> list[str]:
        """Sadece yerleri cikarir"""
        return self.recognize(text)['locations']

    def extract_organizations(self, text: str) -> list[str]:
        """Sadece organizasyonlari cikarir"""
        return self.recognize(text)['organizations']
