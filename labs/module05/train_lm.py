"""LoRA causal-LM smoke exercise on synthetic training text, separate validation text."""
import math
from datasets import Dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling, set_seed

set_seed(42)
checkpoint = "HuggingFaceTB/SmolLM2-135M"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(checkpoint)
model = get_peft_model(model, LoraConfig(task_type=TaskType.CAUSAL_LM, r=8,
    lora_alpha=16, lora_dropout=0.05, target_modules=["q_proj", "v_proj"]))
model.print_trainable_parameters()
train = Dataset.from_dict({"text": [
    f"Question: What is {topic}? Answer: {answer}{tokenizer.eos_token}"
    for topic, answer in [
        ("a dictionary", "A Python mapping from keys to values."),
        ("a list", "An ordered collection of values."),
        ("a function", "A reusable block of code with inputs and outputs."),
        ("an embedding", "A vector used to represent an item."),
        ("retrieval", "Finding relevant evidence for a question."),
        ("validation", "Checking performance on examples excluded from training."),
        ("a token", "A unit used to represent text to a language model."),
        ("a prompt", "The input and instructions given to a model."),
    ]]})
validation = Dataset.from_dict({"text": [
    "Question: What is a tuple? Answer: An ordered immutable sequence." + tokenizer.eos_token,
    "Question: What is a set? Answer: A collection of distinct elements." + tokenizer.eos_token]})

def encode(batch):
    return tokenizer(batch["text"], truncation=True, max_length=128)

train = train.map(encode, batched=True, remove_columns=["text"])
validation = validation.map(encode, batched=True, remove_columns=["text"])
trainer = Trainer(model=model, processing_class=tokenizer,
    args=TrainingArguments(output_dir="outputs/lm", num_train_epochs=1,
        learning_rate=2e-4, per_device_train_batch_size=2, per_device_eval_batch_size=2,
        eval_strategy="epoch", save_strategy="no", report_to="none", seed=42),
    train_dataset=train, eval_dataset=validation,
    data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False))
before = trainer.evaluate()["eval_loss"]
trainer.train()
after = trainer.evaluate()["eval_loss"]
print({"before_loss": before, "after_loss": after,
       "before_perplexity": math.exp(before), "after_perplexity": math.exp(after)})
model.save_pretrained("outputs/lm-adapter")
tokenizer.save_pretrained("outputs/lm-adapter")
print("Adapter saved. Eight examples demonstrate mechanics, not generalization.")
