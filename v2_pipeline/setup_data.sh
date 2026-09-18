#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "========================================="
echo "   SQL Fine-Tuning Data Setup Pipeline"
echo "========================================="

DATA_DIR="fine tuning data set"

if [ -d "../venv" ]; then
    echo "Activating virtual environment..."
    source ../venv/bin/activate
fi


echo "[1/4] Preparing data directory..."
# Create directory if it doesn't exist, or clear it if it does to avoid conflicts
if [ -d "$DATA_DIR" ]; then
    echo "Directory '$DATA_DIR' already exists. Cleaning up old files to avoid conflicts..."
    rm -rf "$DATA_DIR"/*
else
    mkdir -p "$DATA_DIR"
fi

echo "Directory ready: $DATA_DIR"

echo ""
echo "[2/4] Downloading WikiSQL raw data (train, validation, test)..."
echo "Fetching WikiSQL from original repository..."
wget -q "https://github.com/salesforce/WikiSQL/raw/master/data.tar.bz2" -O "data.tar.bz2"
tar -xjf data.tar.bz2
mv data/train.jsonl "$DATA_DIR/train.jsonl"
mv data/dev.jsonl "$DATA_DIR/validation.jsonl"
mv data/test.jsonl "$DATA_DIR/test.jsonl"
rm -rf data data.tar.bz2

echo "Converting JSONL to CSV to match pipeline expectations..."
python3 -c '
import pandas as pd
import json

def jsonl_to_csv(jsonl_path, csv_path):
    data = []
    with open(jsonl_path, "r") as f:
        for line in f:
            data.append(json.loads(line))
    pd.DataFrame(data).to_csv(csv_path, index=False)

jsonl_to_csv("fine tuning data set/train.jsonl", "fine tuning data set/train.csv")
jsonl_to_csv("fine tuning data set/validation.jsonl", "fine tuning data set/validation.csv")
jsonl_to_csv("fine tuning data set/test.jsonl", "fine tuning data set/test.csv")
'


echo "Raw WikiSQL data downloaded successfully."

echo ""
echo "[3/4] Running Python formatting scripts..."

# Move into pipeline folder to run data_preparation.py because it uses ../ paths
cd pipeline

echo "--> Running data_preparation.py (WikiSQL Formatting)..."
python3 data_preparation.py

# Move back to root for the other scripts because they use root-relative paths
cd ..

echo "--> Running data_preparation_spider.py (Spider Download & Formatting)..."
python3 pipeline/data_preparation_spider.py

echo "--> Running merge_datasets.py (Combining datasets)..."
python3 pipeline/merge_datasets.py

echo ""
echo "========================================="
echo "   Pipeline Completed Successfully! 🎉"
echo "========================================="
echo "Your final combined dataset is ready at:"
echo "👉 $DATA_DIR/combined_train_v2.jsonl"
