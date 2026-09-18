import os
import shutil
import urllib.request
import tarfile
import json
import pandas as pd
import subprocess

def main():
    print("=========================================")
    print("   SQL Fine-Tuning Data Setup Pipeline")
    print("          (Cross-Platform / Windows)     ")
    print("=========================================")

    data_dir = "fine tuning data set"

    print("\n[1/4] Preparing data directory...")
    # Create directory if it doesn't exist, or clear it if it does
    if os.path.exists(data_dir):
        print(f"Directory '{data_dir}' already exists. Cleaning up old files to avoid conflicts...")
        shutil.rmtree(data_dir)
    
    os.makedirs(data_dir, exist_ok=True)
    print(f"Directory ready: {data_dir}")

    print("\n[2/4] Downloading WikiSQL raw data (train, validation, test)...")
    url = "https://github.com/salesforce/WikiSQL/raw/master/data.tar.bz2"
    tar_path = "data.tar.bz2"
    
    print("Fetching WikiSQL from original repository (this may take a minute)...")
    urllib.request.urlretrieve(url, tar_path)

    print("Extracting files...")
    with tarfile.open(tar_path, "r:bz2") as tar:
        tar.extractall()

    print("Moving and renaming files...")
    # Move files to our data folder and rename dev to validation
    shutil.move(os.path.join("data", "train.jsonl"), os.path.join(data_dir, "train.jsonl"))
    shutil.move(os.path.join("data", "dev.jsonl"), os.path.join(data_dir, "validation.jsonl"))
    shutil.move(os.path.join("data", "test.jsonl"), os.path.join(data_dir, "test.jsonl"))

    # Cleanup extracted folder and tar file
    shutil.rmtree("data")
    os.remove(tar_path)

    print("Converting JSONL to CSV to match pipeline expectations...")
    def jsonl_to_csv(jsonl_path, csv_path):
        data = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                data.append(json.loads(line))
        pd.DataFrame(data).to_csv(csv_path, index=False)

    jsonl_to_csv(os.path.join(data_dir, "train.jsonl"), os.path.join(data_dir, "train.csv"))
    jsonl_to_csv(os.path.join(data_dir, "validation.jsonl"), os.path.join(data_dir, "validation.csv"))
    jsonl_to_csv(os.path.join(data_dir, "test.jsonl"), os.path.join(data_dir, "test.csv"))
    
    print("Raw WikiSQL data downloaded and converted successfully.")

    print("\n[3/4] Running Python formatting scripts...")
    
    # Run data_preparation.py from inside the pipeline folder
    print("--> Running data_preparation.py (WikiSQL Formatting)...")
    subprocess.run(["python", "data_preparation.py"], cwd="pipeline", check=True)

    # Run the other scripts from the root folder
    print("--> Running data_preparation_spider.py (Spider Download & Formatting)...")
    subprocess.run(["python", os.path.join("pipeline", "data_preparation_spider.py")], check=True)

    print("--> Running merge_datasets.py (Combining datasets)...")
    subprocess.run(["python", os.path.join("pipeline", "merge_datasets.py")], check=True)

    print("\n=========================================")
    print("   Pipeline Completed Successfully! 🎉")
    print("=========================================")
    print("Your final combined dataset is ready at:")
    print(f"👉 {os.path.join(data_dir, 'combined_train.jsonl')}")

if __name__ == "__main__":
    main()
