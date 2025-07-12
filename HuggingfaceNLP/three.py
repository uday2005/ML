from datasets import load_dataset
from transformers import AutoTokenizer


imdb_dataset = load_dataset('imdb')
checkpoint = 'bert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(checkpoint)  


def tokenizer_function(example):
    lower_cased_text = [text.lower() for text in example["text"]]
    return tokenizer(lower_cased_text , truncation=True)

sample_example = imdb_dataset["train"][0]
tokenized_sample = tokenizer_function(sample_example)



# print("--- Original Text ---")
# print(sample_example["text"])
# print("\n--- Tokenized Sample (Input IDs) ---")
# print(tokenized_sample["input_ids"][:20])

# print("---- Decoded Tokens ---")
# print(tokenizer.convert_ids_to_tokens(tokenized_sample["input_ids"][:20]))

tokenized_datasets = imdb_dataset.map(tokenizer_function,batched=True)
print(tokenized_datasets)


from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer

model = AutoModelForSequenceClassification.from_pretrained(checkpoint,num_labels=2)

training_args = TrainingArguments(
    output_dir="bert-finetuned-imdb",
    learning_rate= 2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=1,
)

trainer = Trainer(
    model = model,
    args = training_args,
    tokenizer = tokenizer,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)
print("Trainer is initialized and ready to start training.")

trainer.train()
print("Training complete!")