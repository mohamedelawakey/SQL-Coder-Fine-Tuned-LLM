from clean import clean_data

import pandas as pd
import json
import random

import re

data = pd.read_csv("../../fine tuning data set/train.csv")
cleaned_data = clean_data(data)

def infer_schema(sql: str) -> str:
    columns = set()
    try:
        select_part = sql.split("SELECT", 1)[1].split("FROM", 1)[0]
        select_part = re.sub(r'(MAX|MIN|COUNT|AVG|SUM)\((.*?)\)', r'\2', select_part, flags=re.IGNORECASE)
        columns.add(select_part.strip())
    except:
        pass
        
    if "WHERE" in sql:
        try:
            where_part = sql.split("WHERE", 1)[1]
            conditions = re.split(r' AND | OR ', where_part, flags=re.IGNORECASE)
            for cond in conditions:
                col_match = re.split(r'=|>|<|!=', cond)
                if len(col_match) > 1:
                    columns.add(col_match[0].strip())
        except:
            pass
            
    clean_columns = [c for c in columns if c and not c.lower() in ['*', '1']]
    schema_parts = [f"[{c}] VARCHAR" for c in clean_columns]
    schema_str = "CREATE TABLE table (\n  " + ",\n  ".join(schema_parts) + "\n)"
    return schema_str


def create_prompt(row: pd.Series) -> dict:
    instruction = "You Are a Smart SQL Assistant & Staff DB Engineer. Generate a SQL Query"
    schema = infer_schema(row["sql"])
    input_text = f"Tables: {schema}\nQuestion: {row['question']}"

    return {
        "instruction": instruction,
        "input": input_text,
        "output": row["sql"]
    }

# Shuffle and balance dataset to 40,000 examples
print("Sampling 40,000 WikiSQL examples...")
sampled_data = cleaned_data.sample(n=40000, random_state=42)
final_data = sampled_data.apply(create_prompt, axis=1).tolist()

output_path = "../../fine tuning data set/train_formatted_v2.jsonl"
print(f"Saving to {output_path}...")
with open(output_path, "w") as f:
    for item in final_data:
        f.write(json.dumps(item) + "\n")

print("reformulation successfully")
