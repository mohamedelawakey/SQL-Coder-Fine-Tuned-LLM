# SQL Fine-Tuning Pipeline

This repository contains an end-to-end pipeline for fine-tuning a Large Language Model (Qwen2.5-Coder-1.5B) to perform Text-to-SQL tasks. It uses Unsloth for fast and memory-efficient LoRA fine-tuning, and then exports the final model into GGUF format to be hosted locally using Ollama.

## Project Structure

* `setup_data.sh` and `setup_data_windows.py`: Scripts used to download and combine the WikiSQL and Spider datasets into a single JSONL format for training.
* `pipeline/tuning/training.py`: The main fine-tuning script utilizing Hugging Face's SFTTrainer and Unsloth optimizations.
* `pipeline/tuning/testing/testing.py`: Script to run batched evaluations against test data to calculate exact match and smart similarity accuracy.
* `pipeline/tuning/merge.py`: Merges the trained LoRA adapters back into the base model and converts the final model to Q4_K_M GGUF format.
* `Modelfile`: Configuration file used by Ollama to define the system prompt, stop parameters, and context limits.

## How to Run the Project

Follow these steps to replicate the training and deploy the model locally:

1. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

2. Prepare the Dataset
Run the data setup script to download and structure the JSONL files:
```bash
bash setup_data.sh
```

3. Train the Model
Navigate to the tuning pipeline and start the LoRA fine-tuning process:
```bash
cd pipeline/tuning
python3 training.py
```

4. Merge and Export
Once training is complete, merge the weights and convert the model to GGUF so it can run efficiently on CPU/GPU:
```bash
python3 merge.py
```

5. Deploy with Ollama
Return to the root directory and create the local Ollama model using the provided Modelfile:
```bash
cd ../..
ollama create sql_coder -f Modelfile
```

6. Run the Model
You can now chat with the model or integrate it via API:
```bash
ollama run sql_coder
```

To run a suite of 50 graded test cases against your local Ollama instance:
```bash
python3 pipeline/tuning/testing/run_50_tests.py
```
