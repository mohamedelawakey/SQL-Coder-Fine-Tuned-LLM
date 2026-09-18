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
# We only take 10,000 examples to keep training time reasonable and match WikiSQL scale
formatted_data = []
for idx, row in enumerate(ds):
    if idx >= 10000:
        break
    formatted_data.append(create_prompt(row))

output_path = "fine tuning data set/spider_formatted.jsonl"
print(f"Saving to {output_path}...")
with open(output_path, "w") as f:
    for item in formatted_data:
        f.write(json.dumps(item) + "\n")

print(f"Successfully processed {len(formatted_data)} examples!")
