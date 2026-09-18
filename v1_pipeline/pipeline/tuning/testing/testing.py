from difflib import SequenceMatcher
from tqdm import tqdm 
import pandas as pd
import json
import re
from unsloth import FastLanguageModel

max_seq_length = 1024
dtype = None 
load_in_4bit = True

print("Loading Model and Adapters...")

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="../../../lora_model",
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit
)

FastLanguageModel.for_inference(model)

# Load the JSON test dataset
test_file_path = "../../../fine tuning data set/wikisql_test.json"
with open(test_file_path, 'r') as f:
    test_data = json.load(f)

# Evaluate on all examples
sample_data = test_data

alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.
### Instruction:
{}
### Input:
{}
### Response:
{}"""

instruction = "You Are a Smart SQL Assistant & Staff DB Engineer. Generate a SQL Query"

exact_match_count = 0
smart_match_count = 0
total_predictions = len(sample_data)
batch_size = 8

print(f"Starting Batched Smart Evaluation on {total_predictions} examples (Batch Size: {batch_size})...")

results = []

def clean_sql(sql):
    sql = sql.lower()
    sql = re.sub(r"['\"]", "", sql)
    sql = re.sub(r"\s+", " ", sql)
    return sql.strip()

def sql_similarity(sql1, sql2):
    return SequenceMatcher(None, clean_sql(sql1), clean_sql(sql2)).ratio()

# IMPORTANT: When doing batched generation, we must pad on the left side!
tokenizer.padding_side = "left"

for i in tqdm(range(0, total_predictions, batch_size)):
    batch = sample_data[i:i+batch_size]
    
    prompts = []
    for row in batch:
        input_text = f"Question: {row['question']}"
        prompt = alpaca_prompt.format(instruction, input_text, "")
        prompts.append(prompt)
        
    # Tokenize the whole batch at once
    inputs = tokenizer(prompts, return_tensors="pt", padding=True).to("cuda")
    
    # Generate for the whole batch
    outputs = model.generate(**inputs, max_new_tokens=128, use_cache=True, pad_token_id=tokenizer.eos_token_id)
    
    # Decode outputs
    decoded_outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    
    for idx, result in enumerate(decoded_outputs):
        true_output = batch[idx]["answer"].strip()
        question = batch[idx]["question"]
        
        try:
            generated_sql = result.split("### Response:\n")[1].strip()
        except IndexError:
            generated_sql = result.strip()
            
        # 1. Exact Match Check
        if generated_sql.lower() == true_output.lower():
            exact_match_count += 1
            
        # 2. Smart Match Check
        similarity = sql_similarity(generated_sql, true_output)
        is_smart_match = similarity > 0.70
        if is_smart_match:
            smart_match_count += 1
            
        results.append({
            "question": question, 
            "true_sql": true_output, 
            "generated_sql": generated_sql,
            "similarity_score": round(similarity, 2),
            "is_smart_match": is_smart_match
        })

exact_accuracy = (exact_match_count / total_predictions) * 100
smart_accuracy = (smart_match_count / total_predictions) * 100

print(f"\nEvaluation Finished!")
print(f"Strict Accuracy (Exact Match): {exact_accuracy:.2f}% ({exact_match_count}/{total_predictions})")
print(f"Smart Accuracy (Similarity > 70%): {smart_accuracy:.2f}% ({smart_match_count}/{total_predictions})")

results_df = pd.DataFrame(results)
results_df.to_csv("smart_evaluation_results_batched.csv", index=False)
print(results_df.head())
