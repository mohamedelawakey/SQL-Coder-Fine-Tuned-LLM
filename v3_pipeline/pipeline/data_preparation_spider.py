from datasets import load_dataset
import json

print("Downloading spider/sql-create-context dataset...")
ds = load_dataset("b-mc2/sql-create-context", split="train")

def create_prompt(row) -> dict:
    instruction = "You Are a Smart SQL Assistant & Staff DB Engineer. Generate a SQL Query"
    input_text = f"Tables: {row['context']}\nQuestion: {row['question']}"

    return {
        "instruction": instruction,
        "input": input_text,
        "output": row['answer']
    }

print("Formatting data...")
# We shuffle the dataset and select 50,000 random samples to ensure diversity
ds = ds.shuffle(seed=42).select(range(50000))

formatted_data = []
for row in ds:
    formatted_data.append(create_prompt(row))

output_path = "../../fine tuning data set/spider_raw_50k.jsonl"
print(f"Saving to {output_path}...")
with open(output_path, "w") as f:
    for item in formatted_data:
        f.write(json.dumps(item) + "\n")

print(f"Successfully processed {len(formatted_data)} examples!")
