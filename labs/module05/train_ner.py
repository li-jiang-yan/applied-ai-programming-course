"""Tiny NER lab: align word labels to subword tokens; train a token head."""
import numpy as np
from datasets import Dataset
from sklearn.metrics import f1_score
from transformers import AutoTokenizer, AutoModelForTokenClassification, DataCollatorForTokenClassification, Trainer, TrainingArguments, set_seed

set_seed(42)
labels = ["O", "B-PER", "B-ORG", "I-ORG"]
tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased")
train = Dataset.from_dict({
    "tokens": [["Maya", "works", "at", "North", "College"], ["Leo", "joined", "South", "School"], ["Aisha", "teaches", "Python"], ["Ravi", "visits", "East", "Academy"]],
    "tags": [[1, 0, 0, 2, 3], [1, 0, 2, 3], [1, 0, 0], [1, 0, 2, 3]]})
validation = Dataset.from_dict({"tokens": [["Elena", "joined", "West", "College"], ["Chen", "teaches", "Python"]], "tags": [[1, 0, 2, 3], [1, 0, 0]]})

def align(batch):
    encoded = tokenizer(batch["tokens"], is_split_into_words=True, truncation=True)
    aligned = []
    for i, tags in enumerate(batch["tags"]):
        previous = None
        row = []
        for word in encoded.word_ids(batch_index=i):
            row.append(tags[word] if word is not None and word != previous else -100)
            previous = word
        aligned.append(row)
    encoded["labels"] = aligned
    return encoded

def metrics(pred):
    logits, targets = pred
    guesses = np.argmax(logits, axis=-1)
    valid = targets != -100
    return {"token_macro_f1": f1_score(targets[valid], guesses[valid], average="macro", zero_division=0)}

model = AutoModelForTokenClassification.from_pretrained("distilbert/distilbert-base-uncased",
    num_labels=4, id2label=dict(enumerate(labels)), label2id={s:i for i,s in enumerate(labels)})
trainer = Trainer(model=model, processing_class=tokenizer,
    args=TrainingArguments(output_dir="outputs/ner", num_train_epochs=1,
        per_device_train_batch_size=2, learning_rate=2e-5, eval_strategy="epoch",
        save_strategy="no", report_to="none", seed=42),
    train_dataset=train.map(align, batched=True, remove_columns=train.column_names),
    eval_dataset=validation.map(align, batched=True, remove_columns=validation.column_names),
    data_collator=DataCollatorForTokenClassification(tokenizer), compute_metrics=metrics)
print("Before:", trainer.evaluate())
trainer.train()
print("After:", trainer.evaluate())
trainer.save_model("outputs/ner")
tokenizer.save_pretrained("outputs/ner")
