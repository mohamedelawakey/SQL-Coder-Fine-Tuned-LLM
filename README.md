# SQL Coder - Fine-Tuned Text-to-SQL Assistant

A highly optimized, fine-tuned series of **Qwen2.5-Coder** models, specifically trained to act as a Senior Staff Database Engineer. These models translate natural language questions into accurate, production-ready, raw SQL queries.

This repository contains an end-to-end pipeline for fine-tuning Large Language Models (LLMs) to perform complex Text-to-SQL tasks. The pipeline leverages `Unsloth` for fast, memory-efficient LoRA fine-tuning and exports the final model into GGUF format for local hosting via `Ollama`.

## 📦 Available Versions

This repository contains multiple versions of the model. You can specify the version you want to use via tags:

### 1. `sql_coder_v3:latest` (Recommended & Most Powerful)
- **Base Model:** Qwen2.5-Coder-3B-Instruct
- **Status:** **Active & Highly Capable**
- **Overview:** The ultimate version! Trained on a massive 100,000+ example dataset with advanced **Noise-Injection** techniques to handle incredibly noisy production database schemas. It features **Zero-Chat Formatting (100% adherence)**, meaning it outputs *only* raw SQL without any conversational filler, making it immediately production-ready for automated backend pipelines.
- **Command:** `ollama run sql_coder_v3:latest`

### 2. `sql_coder:v2` (Legacy)
- **Base Model:** Qwen2.5-Coder-1.5B
- **Status:** **Deprecated**
- **Overview:** Fine-tuned on a combined dataset of WikiSQL and Spider. While it understands database schemas, it suffers from "Chatty Format" issues (outputting conversational text alongside SQL) which can crash automated execution engines.
- **Command:** `ollama run mohamedelawakey/sql_coder:v2`

### 3. `sql_coder:latest` (V1 - Prototype)
- **Base Model:** Qwen2.5-Coder-1.5B
- **Status:** **Deprecated / Weak**
- **Overview:** The initial experimental version. It struggles with complex schemas, advanced joins, and frequently hallucinates non-existent columns. Kept only for historical comparison.
- **Command:** `ollama run mohamedelawakey/sql_coder:latest`

---

## ⚡ How to Use

You can run any of the versions locally using Ollama by specifying the correct tag:

**For V3 (Recommended):**
```bash
ollama run sql_coder_v3:latest
```

**For V2:**
```bash
ollama run mohamedelawakey/sql_coder:v2
```

**For V1:**
```bash
ollama run mohamedelawakey/sql_coder:latest
```

## 💡 Example Usage

### Example Usage (For V3)
Because V3 was highly optimized using a very specific simulated Database Schema format, **you MUST format your prompts exactly as shown below** to get accurate results. The model has been stripped of unnecessary conversational abilities to output raw, syntactically correct SQL queries.

Always provide your schema and question in this exact format:

```text
>>> Tables: CREATE TABLE items (
...   [notes] VARCHAR,
...   [Year] VARCHAR
... )
... Question: How much is the purse worth after 2012?
... 
SELECT SUM(Purse) FROM items WHERE Year > 2012
```

### Example Usage (For V1 & V2)
In the older versions, providing a schema was optional but recommended. You could ask direct questions like this:

```sql
>>> what is the nationality of the player messi?
SELECT Nationality FROM table WHERE Player = 'messi'
```

## 📊 Performance & Evaluation
Evaluated locally across graded test batches (200 queries) ranging from simple aggregations to complex intersections (Level 1 to Level 5).

### V3 Benchmarks
- **Absolute Logic Accuracy (~75%):** Rivals much larger models (7B+) in handling deep relational logic, multi-table joins, and complex subqueries.
- **Format Adherence (100%):** Achieved perfect "Zero-Chat" output across all tests, making it fully crash-proof for automated APIs.
- **Fast Inference:** Averages **~0.5s per query** generation on standard local hardware.
- **Context Handling:** Optimized with a 4096 context window to process complex, multi-table database schemas without losing focus.

### V2 Benchmarks
- **Usable Accuracy (~30%):** While the model understands database schemas and basic SQL, its actual usability drops significantly due to "Chatty Format" issues (wrapping outputs in markdown or conversational text).
- **Fast Inference:** ~0.4s per query generation on average hardware.
- **Context Handling:** Processes complex schemas but occasionally struggles with deep relational logic.

### V1 Benchmarks
- **Accuracy (Low):** Heavily biased towards simple queries and frequently hallucinates non-existent columns.
- **Fast Inference:** ~0.4s per query generation.
- **Context Handling:** Struggles to maintain focus on complex schemas.

## ⚙️ Model Details
- **Base Models:** Qwen2.5-Coder-3B-Instruct (V3) / Qwen2.5-Coder-1.5B (V1, V2)
- **Quantization:** Q4_K_M (GGUF) for extreme memory efficiency and fast local inference.
- **Fine-Tuning Framework:** Unsloth & LoRA

---

## 🛠️ How to Run the Pipelines (V1, V2, or V3)

The project structure is identical across all versions. Whether you are running this locally (Windows/Linux/Mac) or on Kaggle, follow these steps. Replace `v3_pipeline` with your desired version directory (`v1_pipeline` or `v2_pipeline`) if you want to test older models.

### 1. Install Dependencies
Make sure you have Python 3.10+ installed. Install the required libraries using the provided `requirements.txt`:
```bash
pip install -r requirements.txt
```
*(Note for Kaggle Users: You may need to run `!pip install "unsloth[kaggle-new] @ git+https://github.com/unslothai/unsloth.git"` directly in the notebook, and ensure the **Internet** toggle is turned ON).*

### 2. Prepare the Dataset
You need to download and structure the dataset before training. We provide an automated bash script for this.

**For Linux & Mac (Native Terminal):**
```bash
# Choose the pipeline version you want to run (e.g., v3_pipeline)
cd v3_pipeline
bash setup_data.sh
```

**For Windows (Git Bash or WSL):**
Because this is a Bash script (`.sh`), it will **not** work in the standard Windows Command Prompt or PowerShell. You must open **Git Bash** (or a WSL terminal) in the project folder and run:
```bash
# Choose the pipeline version you want to run (e.g., v3_pipeline)
cd v3_pipeline
bash setup_data.sh
```

### 3. Train the Model
Our training scripts use memory-optimized parameters (Batch Size=2, Gradient Accumulation=4, Checkpointing=True) to prevent RAM/VRAM OOM errors on smaller GPUs (e.g., Kaggle T4 or local RTX cards).
```bash
cd pipeline/tuning
python3 training.py
```

### 4. Merge and Export to GGUF
Once training finishes, merge the LoRA adapters into the base model and export it to a quantized `q4_k_m` GGUF format:
```bash
python3 merge.py
```

### 5. Deploy with Ollama
Return to the root pipeline directory and create the local Ollama model using the customized Modelfile:
```bash
cd ../..
# Change 'v3' to 'v2' or 'v1' if running an older pipeline
ollama create sql_coder_v3 -f Modelfile
```

### 6. Evaluate the Model
Run the evaluation suite to test the model's complex reasoning and SQL precision:
```bash
# The test script name may vary slightly depending on the pipeline version
python3 pipeline/tuning/testing/run_200_tests_v3_formatted.py
```

---

## ⚖️ License

This project and the resulting models are open for public use under the **CC BY-NC 4.0** license, which enforces the following strict conditions:
- **Attribution Required:** You must give appropriate credit to the original author ([Mohamed Alawakey](https://github.com/mohamedelawakey)) if you use, distribute, or modify this work.
- **Non-Commercial Use Only:** You may not use this material for commercial purposes (e.g., selling the model, wrapping it in a paid API, or using it as part of a commercial product).

---

### 💼 Commercial Licensing & Consulting
If you represent a company and wish to use this model in a commercial product, or if you need a custom fine-tuned version trained on your private database schema, you must purchase a **Commercial License**. 

For commercial inquiries and consulting, please contact: **[mohamedelawakey@gmail.com](mailto:mohamedelawakey@gmail.com)**

---
