# data set
data_files = "/kaggle/input/datasets/mohamedalawakey/sql-fine-tuning-data/train_formatted_v3.jsonl"
data_split = "train"
dataset_text_field = "text"

# memory optemization & model loading
model_name = "unsloth/Qwen2.5-Coder-3B-Instruct-bnb-4bit"
max_seq_length = 1024
dtype = None
load_in_4bit = True

# LoRA Configurations
r = 32
target_modules = [
    "q_proj", "k_proj", "v_proj",
    "o_proj", "gate_proj", "up_proj",
    "down_proj",
]
lora_alpha = 32
lora_dropout = 0.05
bias = "none"
use_gradient_checkpointing = True
random_state = 3407

# GPU Configurations (GTX 1650)
dataset_num_proc = 2

per_device_train_batch_size = 2
gradient_accumulation_steps = 4
warmup_steps = 100
num_train_epochs = 1
learning_rate = 2e-4
fp16 = True
bf16 = False
optim = "adamw_8bit"
weight_decay = 0.01
lr_scheduler_type = "linear"
seed = 3407
output_dir = "/kaggle/working/"