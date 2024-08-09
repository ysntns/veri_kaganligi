from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

class QuestionAnswerer:
    def __init__(self):
        self.model_name = "savasy/bert-base-turkish-squad"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)

    def answer(self, context, question):
        inputs = self.tokenizer(question, context, return_tensors="pt")
        outputs = self.model(**inputs)
        
        answer_start = torch.argmax(outputs.start_logits)
        answer_end = torch.argmax(outputs.end_logits) + 1
        
        answer = self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end])
        )
        
        return {"answer": answer, "score": float(outputs.start_logits.max() + outputs.end_logits.max())}
