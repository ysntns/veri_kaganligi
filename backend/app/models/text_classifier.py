from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class TextClassifier:
    def __init__(self):
        self.model_name = "savasy/bert-base-turkish-text-classification"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

    def classify(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(probabilities).item()
        score = probabilities[0][predicted_class].item()
        
        class_map = {0: "economics", 1: "sports", 2: "politics", 3: "technology"}
        return {"class": class_map[predicted_class], "score": score}
