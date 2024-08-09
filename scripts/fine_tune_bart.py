from transformers import BartForConditionalGeneration, BartTokenizer, Trainer, TrainingArguments
from datasets import load_dataset


def fine_tune_bart():
    # Load pre-trained model and tokenizer
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")

    # Load and preprocess your dataset
    dataset = load_dataset("your_dataset_name")  # Replace with your dataset

    def preprocess_function(examples):
        inputs = tokenizer(examples["text"], truncation=True, padding="max_length", max_length=1024)
        targets = tokenizer(examples["summary"], truncation=True, padding="max_length", max_length=128)
        return {
            "input_ids": inputs.input_ids,
            "attention_mask": inputs.attention_mask,
            "labels": targets.input_ids,
        }

    tokenized_dataset = dataset.map(preprocess_function, batched=True)

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="./logs",
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
    )

    # Start training
    trainer.train()

    # Save the fine-tuned model
    model.save_pretrained("./fine_tuned_bart")
    tokenizer.save_pretrained("./fine_tuned_bart")


if __name__ == "__main__":
    fine_tune_bart()
