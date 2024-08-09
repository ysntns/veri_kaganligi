from transformers import MarianMTModel, MarianTokenizer

class TranslationService:
    def __init__(self):
        self.model_name_tr_en = "Helsinki-NLP/opus-mt-tr-en"
        self.model_name_en_tr = "Helsinki-NLP/opus-mt-en-tr"
        self.tokenizer_tr_en = MarianTokenizer.from_pretrained(self.model_name_tr_en)
        self.model_tr_en = MarianMTModel.from_pretrained(self.model_name_tr_en)
        self.tokenizer_en_tr = MarianTokenizer.from_pretrained(self.model_name_en_tr)
        self.model_en_tr = MarianMTModel.from_pretrained(self.model_name_en_tr)

    def translate(self, text, target_language):
        if target_language == "en":
            return self._translate(text, self.tokenizer_tr_en, self.model_tr_en)
        elif target_language == "tr":
            return self._translate(text, self.tokenizer_en_tr, self.model_en_tr)
        else:
            raise ValueError("Unsupported target language")

    def _translate(self, text, tokenizer, model):
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        translated = model.generate(**inputs)
        return tokenizer.decode(translated[0], skip_special_tokens=True)

    def detect_language(self, text):
        turkish_chars = set('çğıöşüÇĞİÖŞÜ')
        if any(char in turkish_chars for char in text):
            return 'tr'
        return 'en'
