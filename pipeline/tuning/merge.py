from unsloth import FastLanguageModel
import configurations as conf


print("1. Loading Base Model and LoRA Adapters...")
model_path = "../../lora_model"

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_path,
    max_seq_length=conf.max_seq_length,
    dtype=conf.dtype,
    load_in_4bit=conf.load_in_4bit
)

# vllm mearge
print("\n2. Saving merged model for vLLM (16-bit)...")
model.save_pretrained_merged(
    "vllm_merged_model",
    tokenizer,
    save_method = "merged_16bit",
)
print("vLLM export complete!")

# Ollama (GGUF Format) mearge
print("\n3. Saving model to GGUF format for Ollama...")
model.save_pretrained_gguf(
    "ollama_gguf_model", 
    tokenizer, 
    quantization_method="q4_k_m"
)
print("Ollama export complete!")
