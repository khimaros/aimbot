---
license: apache-2.0
language:
  - en
  - zh
library_name: transformers
pipeline_tag: text-generation
tags:
  - g9v3
  - llama
  - text-generation
  - long-context
  - tool-calling
---

<div align="center">
<h1>G9v3-3B</h1>
</div>

<p align="center">
<a href="https://github.com/AI9Stars" target="_blank">GitHub</a> |
<a href="https://huggingface.co/ai9stars" target="_blank">Hugging Face</a>
</p>

## Introduction

**G9v3-3B** is a dense 3B causal language model from the **AI9Stars** team, built for local deployment and resource-constrained scenarios. It targets everyday assistant use, coding, tool-use workflows, and reasoning tasks where a compact model is preferred.


## Model Information

- **Type**: Causal Language Model
- **Architecture**: Standard `LlamaForCausalLM`
- **Number of Parameters**: ~3B
- **Context Length**: 131,072

## Quickstart

### vLLM

```bash
pip install "vllm>=0.21"
vllm serve ai9stars/G9v3-3B --port 8000
```

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai9stars/G9v3-3B",
    "messages": [{"role": "user", "content": "Who are you?"}],
    "max_tokens": 128,
    "temperature": 0.7
  }'
```

### SGLang

```bash
pip install "sglang[srt]>=0.5.12"
python -m sglang.launch_server --model-path ai9stars/G9v3-3B --port 30000
```

```bash
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai9stars/G9v3-3B",
    "messages": [{"role": "user", "content": "Who are you?"}],
    "max_tokens": 128,
    "temperature": 0.7
  }'
```

### Transformers

```bash
pip install -U "transformers>=5.6" accelerate torch
```

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "ai9stars/G9v3-3B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto",
    device_map="auto",
)

messages = [{"role": "user", "content": "Who are you?"}]
inputs = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    enable_thinking=False,
    return_dict=True,
    return_tensors="pt",
).to(model.device)

outputs = model.generate(**inputs, max_new_tokens=128)
print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True))
```

Recommended sampling parameters:

| Mode | Recommended params | Enable |
| --- | --- | --- |
| **Think** | `temperature=0.9, top_p=0.95` | `enable_thinking=True` |
| **No Think** | `temperature=0.7, top_p=0.95` | `enable_thinking=False` |

## Limitations and Responsible Use

G9v3-3B is a language model that generates content based on learned statistical patterns from training data. It may produce inaccurate, biased, or unsafe outputs, and generated content should be reviewed and verified before use in high-stakes settings. Users are responsible for evaluating outputs, applying appropriate safeguards, and complying with applicable laws, regulations, and platform policies.

## License

This repository and the G9v3 model weights are released under the Apache-2.0 License.
