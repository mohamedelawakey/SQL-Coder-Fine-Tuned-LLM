from clean import clean_data

import pandas as pd
import json
import random

data = pd.read_csv("../fine tuning data set/train.csv")
cleaned_data = clean_data(data)


def get_columns(sql: str) -> str:
    try:
        cols_part = sql.split("SELECT")[1].split("FROM")[0]
        clean_cols = cols_part.replace("COUNT", "").replace("(", "").replace(")", "").strip()

        return clean_cols
    except:
        return ""


def create_prompt(row: pd.Series) -> dict:
    instruction = "You Are a Smart SQL Assistant & Staff DB Engineer. Generate a SQL Query"

    if random.choice([True, False]):
        cols = get_columns(row["sql"])
        input_text = f"Columns: [{cols}]. Question: {row['question']}"
    else:
        input_text = f"Question: {row['question']}"

    return {
        "instruction": instruction,
        "input": input_text,
        "output": row["sql"]
    }

# crate & save formated data
final_data = cleaned_data.apply(create_prompt, axis=1).tolist()

with open("../fine tuning data set/train_formatted.jsonl", "w") as f:
    for item in final_data:
        f.write(json.dumps(item) + "\n")

print("reformulation successfully")
