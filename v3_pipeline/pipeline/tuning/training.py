import os
os.environ['UNSLOTH_SKIP_TORCHVISION_CHECK'] = '1'

from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM
from transformers import TrainingArguments
import configurations as conf

print("Loading Model...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=conf.model_name,
    max_seq_length=conf.max_seq_length,
    dtype=conf.dtype,
    load_in_4bit=conf.load_in_4bit
)

model = FastLanguageModel.get_peft_model(
    model,
    r=conf.r,
    target_modules=conf.target_modules,
    lora_alpha=conf.lora_alpha,
    lora_dropout=conf.lora_dropout,
    bias=conf.bias,
    use_gradient_checkpointing = conf.use_gradient_checkpointing,
    random_state=conf.random_state
)


print("Loading Dataset...")
dataset = load_dataset(
    "json",
    data_files=conf.data_files,
    split=conf.data_split
)
print("Dataset Loaded Successfully ...")


alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""


def formate_prompts(examples):
    instructions = examples["instruction"]
    inputs       = examples["input"]
    outputs      = examples["output"]

    texts = []

    for instruction, input_text, output in zip(instructions, inputs, outputs):
        text = alpaca_prompt.format(instruction, input_text, output) + tokenizer.eos_token
        texts.append(text)

    return {
        "text": texts
    }

dataset = dataset.map(formate_prompts, batched=True)


print("Starting Trainer...")
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field=conf.dataset_text_field,
    max_seq_length=conf.max_seq_length,
    dataset_num_proc=conf.dataset_num_proc,
    data_collator=DataCollatorForCompletionOnlyLM("### Response:\n", tokenizer=tokenizer),
    args = TrainingArguments(
        per_device_train_batch_size=conf.per_device_train_batch_size,
        gradient_accumulation_steps=conf.gradient_accumulation_steps,
        warmup_steps=conf.warmup_steps,
        num_train_epochs=conf.num_train_epochs,
        learning_rate=conf.learning_rate,
        fp16=conf.fp16,
        bf16=conf.bf16,
        optim=conf.optim,
        weight_decay=conf.weight_decay,
        lr_scheduler_type=conf.lr_scheduler_type,
        seed=conf.seed,
        output_dir=conf.output_dir
    ),
)


trainer_stats = trainer.train()

print("Saving Model...")
model.save_pretrained("lora_model")
tokenizer.save_pretrained("lora_model")
print("Training Done & Model Saved Successfully!")
