"""Tiny contrastive fine-tune of the retrieval component; no quality claim."""
from pathlib import Path
from datasets import Dataset
from sentence_transformers import SentenceTransformer, SentenceTransformerTrainer, SentenceTransformerTrainingArguments, losses

root = Path(__file__).resolve().parents[1]
questions = ["What is the refund deadline?", "What time do lessons start?", "Is Python needed?", "How do I arrange accessibility support?"]
names = ["refund", "schedule", "laptop", "support"]
data = Dataset.from_dict({"anchor": questions, "positive": [(root / "data" / f"{n}.txt").read_text(encoding="utf-8") for n in names]})
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
args = SentenceTransformerTrainingArguments(
    output_dir="outputs/retriever-checkpoints", num_train_epochs=1,
    per_device_train_batch_size=4, learning_rate=2e-5,
    save_strategy="no", report_to="none", seed=42,
)
trainer = SentenceTransformerTrainer(model=model, args=args, train_dataset=data,
                                    loss=losses.MultipleNegativesRankingLoss(model))
trainer.train()
model.save_pretrained("outputs/course-retriever")
print("Now compare rag.py --model outputs/course-retriever against the base model.")
