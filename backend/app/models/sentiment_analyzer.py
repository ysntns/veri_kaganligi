from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class SentimentAnalyzer:
    def __init__(self):
        self.model_name = "savasy/bert-base-turkish-sentiment-cased"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

    def analyze(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sentiment = torch.argmax(probabilities).item()
        score = probabilities[0][sentiment].item()
        
        sentiment_map = {0: "negative", 1: "neutral", 2: "positive"}
        return {"sentiment": sentiment_map[sentiment], "score": score}
