import json

wiki_path = "../../fine tuning data set/wiki_raw_50k.jsonl"
spider_path = "../../fine tuning data set/spider_raw_50k.jsonl"
combined_path = "../../fine tuning data set/combined_raw_100k.jsonl"

print("Loading WikiSQL data...")
with open(wiki_path, "r") as f:
    wiki_data = [json.loads(line) for line in f]
    
print("Loading Spider data...")
with open(spider_path, "r") as f:
    spider_data = [json.loads(line) for line in f]

# We will balance them, for example 10,000 spider + whatever wiki we have (maybe sample down to 5000 wiki)
# But let's just append them together
combined = wiki_data + spider_data

print(f"Total Combined Examples: {len(combined)}")

print("Saving combined dataset...")
with open(combined_path, "w") as f:
    for item in combined:
        f.write(json.dumps(item) + "\n")

print(f"Dataset successfully merged and saved to {combined_path}")
