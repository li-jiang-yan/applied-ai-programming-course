"""Small IMDb experiment with train/validation/test separation."""
import argparse
import numpy as np
from datasets import load_dataset
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding, Trainer, TrainingArguments, set_seed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lr", type=float, default=2e-5)
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--output", default="outputs/sentiment")
    parser.add_argument("--final-test", action="store_true")
    args = parser.parse_args()
    set_seed(42)
    checkpoint = "distilbert/distilbert-base-uncased"
    raw = load_dataset("stanfordnlp/imdb")
    subset = raw["train"].shuffle(seed=42).select(range(800))
    split = subset.train_test_split(test_size=0.2, seed=42, stratify_by_column="label")
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, max_length=128)

    tokenized = split.map(tokenize, batched=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        checkpoint, num_labels=2,
        id2label={0: "NEGATIVE", 1: "POSITIVE"}, label2id={"NEGATIVE": 0, "POSITIVE": 1})

    def metrics(pred):
        logits, labels = pred
        guesses = np.argmax(logits, axis=-1)
        return {"accuracy": accuracy_score(labels, guesses), "macro_f1": f1_score(labels, guesses, average="macro")}

    settings = TrainingArguments(
        output_dir=args.output, learning_rate=args.lr, num_train_epochs=args.epochs,
        per_device_train_batch_size=4, per_device_eval_batch_size=8,
        gradient_accumulation_steps=2, weight_decay=0.01,
        eval_strategy="epoch", save_strategy="epoch", save_total_limit=1,
        load_best_model_at_end=True, metric_for_best_model="macro_f1",
        report_to="none", seed=42, logging_steps=20,
    )
    trainer = Trainer(model=model, args=settings, train_dataset=tokenized["train"],
                      eval_dataset=tokenized["test"], processing_class=tokenizer,
                      data_collator=DataCollatorWithPadding(tokenizer), compute_metrics=metrics)
    print("Untrained task-head validation:", trainer.evaluate())
    trainer.train()
    print("Tuned validation:", trainer.evaluate())
    trainer.save_model(args.output)
    tokenizer.save_pretrained(args.output)
    if args.final_test:
        test = raw["test"].shuffle(seed=17).select(range(200)).map(tokenize, batched=True)
        result = trainer.predict(test)
        print("Final held-out test:", result.metrics)
        print("Confusion matrix (rows=true, columns=predicted):")
        print(confusion_matrix(result.label_ids, result.predictions.argmax(-1)))

if __name__ == "__main__":
    main()
