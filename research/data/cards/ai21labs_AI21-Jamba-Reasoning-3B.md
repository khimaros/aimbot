---
license: apache-2.0
license_name: jamba-open-model-license
license_link: https://www.ai21.com/licenses/jamba-open-model-license
pipeline_tag: text-generation
library_name: transformers
---
## Introduction

AI21’s Jamba Reasoning 3B is a top-performing reasoning model that packs leading scores on intelligence benchmarks and highly-efficient processing into a compact 3B build. 
<br> Read the full blog post [here](https://www.ai21.com/blog/introducing-jamba-reasoning-3B). 


### Key Advantages

**Fast: Optimized for efficient sequence processing**

The hybrid design combines Transformer attention with Mamba (a state-space model). Mamba layers are more efficient for sequence processing, while attention layers capture complex dependencies. This mix reduces memory overhead, improves throughput, and makes the model run smoothly on laptops, GPUs, and even mobile devices, while maintainig impressive quality. 

<img src="https://huggingface.co/ai21labs/AI21-Jamba-Reasoning-3B-GGUF/resolve/main/assets/Intelligence%20vs%20Speed%20Jamba%20Reasoning%203B.png" width="900"/>


**Smart: Leading intelligence scores** 
The model outperforms competitors, such as Gemma 3 4B, Llama 3.2 3B, and Granite 4.0 Micro, on a combined intelligence score that averages 6 standard benchmarks.  

<img src="https://huggingface.co/ai21labs/AI21-Jamba-Reasoning-3B-GGUF/resolve/main/assets/Benchmark%20Performance%20-%20Jamba%20Reasoning%203B.png" width="900"/>


**Scalable: Handles very long contexts**

Unlike most compact models, Jamba Reasoning 3B supports extremely long contexts. Mamba layers allow the model to process inputs without storing massive attention caches, so it scales to **256K tokens** while keeping inference practical. This makes it suitable for edge deployment as well as datacenter workloads.
<img src="https://huggingface.co/ai21labs/AI21-Jamba-Reasoning-3B-GGUF/resolve/main/assets/Speed%20vs%20Context%20Length.png" width="900"/>


## Model Details

- Number of Parameters: 3B
- Number of Layers: 28 (26 Mamba, 2 Attention)
- Number of Attention Heads: 20 MQA (20 for Q, 1 for KV)
- Vocabulary Size: 64K
- Context Length: **256k**
- Architecture: Hybrid Transformer–Mamba with efficient attention and long-context support
- **Developed by:** [**AI21**](https://www.ai21.com/)
- **Supported languages:** English, Spanish, French, Portuguese, Italian, Dutch, German, Arabic and Hebrew
- Intelligence benchmark results:

|  | **MMLU-Pro** | **Humanity’s Last Exam** | **IFBench** |
| --- | --- | --- | --- |
| DeepSeek R1 Distill Qwen 1.5B | 27.0% | 3.3% | 13.0% |
| Phi-4 mini | 47.0% | 4.2% | 21.0% |
| Granite 4.0 Micro | 44.7% | 5.1% | 24.8% |
| Llama 3.2 3B | 35.0% | 5.2% | 26.0% |
| Gemma 3 4B | 42.0% | 5.2% | 28.0% |
| Qwen 3 1.7B | 57.0% | 4.8% | 27.0% |
| Qwen 3 4B | 70% | 5.1% | 33% |
| **Jamba Reasoning 3B** | **61.0%** | **6.0%** | **52.0%** |

## Quickstart

### Run the model locally

> [!NOTE]
> Please reference the GGUF model card [here](https://huggingface.co/ai21labs/AI21-Jamba-Reasoning-3B-GGUF#quickstart).

### **Run the model with vLLM**

For best results, we recommend using vLLM version 0.11.0 or higher and enabling `--mamba-ssm-cache-dtype=float32` 

```bash
pip install vllm>=0.11.0
```

Using vllm in online server mode:

```bash
vllm serve "ai21labs/AI21-Jamba-Reasoning-3B" --mamba-ssm-cache-dtype float32 --reasoning-parser deepseek_r1 --enable-auto-tool-choice --tool-call-parser hermes
```

Using vllm in offline mode:

```jsx
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

model = "ai21labs/AI21-Jamba-Reasoning-3B"

llm = LLM(model=model,
          tensor_parallel_size=1,
          mamba_ssm_cache_dtype="float32")

tokenizer = AutoTokenizer.from_pretrained(model)

messages = [
    {"role": "user", "content": "You are analyzing customer support tickets to decide which need escalation.\nTicket 1: 'App crashes when uploading files >50MB.'\nTicket 2: 'Forgot password, can’t log in.'\nTicket 3: 'Billing page missing enterprise pricing.'\nClassify each ticket as Critical, Medium, or Low and explain your reasoning.\n"},
]

prompts = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)

sampling_params = SamplingParams(temperature=0.6, max_tokens=4096)
outputs = llm.generate(prompts, sampling_params)

generated_text = outputs[0].outputs[0].text
print(generated_text)

```

### **Run the model with Transformers**

```jsx
pip install transformers>= 4.54.0
pip install flash-attn --no-build-isolation
pip install causal-conv1d>=1.2.0
pip install mamba-ssm
```

```jsx
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("ai21labs/AI21-Jamba-Reasoning-3B",
                                             dtype=torch.bfloat16,
                                             attn_implementation="flash_attention_2",
                                             device_map="auto")

tokenizer = AutoTokenizer.from_pretrained("ai21labs/AI21-Jamba-Reasoning-3B")

messages = [
    {"role": "user", "content": "You are analyzing customer support tickets to decide which need escalation.\nTicket 1: 'App crashes when uploading files >50MB.'\nTicket 2: 'Forgot password, can’t log in.'\nTicket 3: 'Billing page missing enterprise pricing.'\nClassify each ticket as Critical, Medium, or Low and explain your reasoning.\n"},
]

prompts = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)

outputs = model.generate(**tokenizer(prompts, return_tensors="pt").to(model.device), do_sample=True, temperature=0.6, max_new_tokens=4096)

generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)
```
        
## Training Details

We trained the model in multiple stages, each designed to strengthen reasoning and long-context performance. The process began with large-scale pre-training on a diverse corpus of natural documents. We then mid-trained on ~0.5T tokens of math and code, while extending the context length to 32K tokens. During this stage we also applied a [Mamba-specific long-context method](https://arxiv.org/abs/2507.02782), which we found to significantly improve long-context abilities.

To improve reasoning, tool use, and instruction following, we applied cold-start distillation: supervised fine-tuning with a 32K window and direct preference optimization with a 64K window. Finally, we enhanced reasoning performance further through online reinforcement learning with RLVR, targeting tasks such as code generation, mathematical problem solving, structured output, and information extraction.

## Reinforcement “Fine-Tuning”

Full support for training Jamba through VeRL will be available soon. AI21 has introduced several improvements to the VeRL framework (https://github.com/volcengine/verl), including new capabilities for training hybrid models, and stability improvements for GRPO training. These improvements will soon be available to the open source community. 

---

## License

- `Apache 2.0`

---

## Citation

- Blog post- Read the full blog post [here](https://www.ai21.com/blog/introducing-jamba-reasoning-3B)