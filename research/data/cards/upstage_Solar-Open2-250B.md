---
language:
  - en
  - ko
  - ja
library_name: transformers
license: other
license_name: upstage-solar-license
license_link: LICENSE
pipeline_tag: text-generation
tags:
  - upstage
  - solar
  - moe
  - llm
  - vllm
---

![Solar Open 2](assets/solar-open2.gif)

# Solar Open 2

Solar Open 2 is Upstage’s 250B-A15B open-weight large language model, built for agentic use cases such as office productivity, document-intensive work, and coding. Its Hybrid-Attention Mixture-of-Experts (MoE) architecture with linear attention delivers highly efficient inference even in long-context settings.

[**Technical Report**](https://arxiv.org/abs/2607.20062) | [**Blog**](https://www.upstage.ai/blog/en/solar-open-2?utm_source=hf&utm_medium=referral&utm_campaign=so2-launch&utm_content=modelcard) | [**Upstage Website**](https://www.upstage.ai/) 

### Highlights

![Highlights_en](assets/Highlights_en.png)
![Highlights_kr](assets/Highlights_kr.png)

- **Agentic Specialist:** Purpose-built for agentic workflows — tool calling, multi-step reasoning, and end-to-end task execution. Competitive with the strongest open-weight models on agent benchmarks.

- **Minimal Inference Cost:** A 250B-parameter MoE that activates only 15B per token, built on a hybrid attention stack that interleaves three linear-attention layers with one softmax-attention layer — large-model capacity at small-model inference cost.

- **1M-Token Context:** The linear-attention layers encode token order intrinsically in their recurrent state, so positional encoding is removed entirely (NoPE), lifting the RoPE extrapolation limit. Only 12 of the 48 layers keep a KV cache, holding long-context memory to roughly a quarter of an all-softmax model of the same shape.

- **Efficiently Trained at Low Cost:** Initialized by selective weight transfer from Solar Open 1 (102B) — only the 2.3% of weights that survive the architectural change are carried over, and everything else is randomly initialized — which raises the starting point and accelerates early convergence at 250B scale.

- **Multilingual:** English, Korean, and Japanese.

---

## Model Overview

| Field                           | Value                                                                   |
| ------------------------------- | ----------------------------------------------------------------------- |
| Model Name                      | Solar Open 2 (250B-A15B)                                                |
| Architecture                    | Hybrid-Attention Mixture-of-Experts (MoE)                               |
| Total Parameters                | 250B (250,287,794,944)                                                  |
| Active Parameters               | 15B (per token)                                                         |
| Layers                          | 48                                                                      |
| Hidden Size                     | 4096                                                                    |
| Attention                       | Hybrid — Softmax + Linear Attention, pattern `[Softmax, Linear×3] × 12` |
| Position Encoding               | NoPE (no rotary positional encoding)                                    |
| Number of Attention Heads (GQA) | (Softmax) 64 query / 8 KV, (Linear) 64 query                            |
| Number of Experts               | 321 (320 routed + 1 shared)                                             |
| Number of Activated Experts     | 8 routed (top-8) + 1 shared                                             |
| Vocabulary                      | 196,608                                                                 |
| Context Length                  | 1M                                                                      |
| Pre-training Tokens             | ~12 Trillion                                                            |
| Supported Languages             | English, Korean, Japanese                                               |
| Training Hardware               | NVIDIA B200 GPUs                                                        |
| Training GPU Time               | 2M GPU Hours                                                            |
| License                         | Upstage Solar License (see [LICENSE](https://huggingface.co/upstage/Solar-Open2-250B/blob/main/LICENSE))                                     |
| Hardware Requirements           | Minimum: H200 \* 4ea / Recommended: H200 \* 8ea                        |

---

## Performance

### English Benchmarks

| Benchmark             | **Solar Open 2**<br>250B-A15B | **Solar Open 100B**<br>102B-A12B | **Command A+**<br>218B-A25B | **Mistral Medium 3.5**<br>128B dense, high | **MiMo-V2.5**<br>310B-A15B | **DeepSeek-V4-Flash**<br>284B-A13B, max |
| --------------------- | ----------------------------: | -------------------------------: | --------------------------: | -----------------------------------------: | -------------------------: | --------------------------------------: |
| **Know. & Reasoning** |                               |                                  |                             |                                            |                            |                                         |
| MMLU-Pro              |                      **86.2** |                             80.4 |                        79.0 |                                       81.2 |                       84.6 |                             <u>85.9</u> |
| GPQA-Diamond          |                   <u>86.3</u> |                             66.2 |                        75.6 |                                       77.5 |                       83.0 |                                **88.9** |
| HLE (w/o tools)       |                   <u>28.8</u> |                             11.5 |                        11.4 |                                       12.8 |                       24.3 |                                **32.3** |
| LiveCodeBench (v6)    |                      **92.4** |                             56.5 |                        86.1 |                                       84.9 |                       89.1 |                             <u>92.3</u> |
| ArtifactsBench        |                          55.9 |                             43.4 |                        42.8 |                                       49.8 |                <u>59.3</u> |                                **61.0** |
| HMMT2602              |                   <u>93.9</u> |                             68.9 |                        73.5 |                                       62.9 |                       61.4 |                                **94.7** |
| AIME2026              |                          95.7 |                             87.7 |                 <u>96.0</u> |                                       89.0 |                       92.3 |                                **97.0** |
| **IF / Long**         |                               |                                  |                             |                                            |                            |                                         |
| Multi-Challenge       |                   <u>61.0</u> |                             40.5 |                        45.8 |                                       49.8 |                       39.0 |                                **62.0** |
| IFBench               |                   <u>80.0</u> |                             57.7 |                        73.9 |                                       69.0 |                       67.1 |                                **80.3** |
| AA-LCR                |                          62.3 |                             36.0 |                        46.0 |                                       61.0 |                <u>62.7</u> |                                **63.7** |
| **Agent**             |                               |                                  |                             |                                            |                            |                                         |
| SWE-Bench Verified    |                          70.4 |                             15.4 |                        14.4 |                                       69.6 |                <u>73.0</u> |                                **73.8** |
| Terminal Bench Hard   |                          28.3 |                              2.3 |                        25.0 |                                       33.3 |                   **41.7** |                             <u>34.1</u> |
| APEX-Agents           |                      **16.6** |                              2.4 |                         1.6 |                                        6.1 |                <u>13.4</u> |                                    13.2 |
| MCP-Atlas             |                   <u>58.2</u> |                             34.4 |                        27.2 |                                       30.7 |                   **63.9** |                             <u>58.2</u> |
| τ³ (banking)          |                   <u>19.6</u> |                              7.4 |                         5.8 |                                        5.8 |                        8.7 |                                **22.3** |
| GDPval-AA v2 (ELO)    |                          1128 |                                – |                         712 |                                        929 |                <u>1145</u> |                                **1187** |

### Korean Benchmarks

| Benchmark    | **Solar Open 2**<br>250B-A15B | **Solar Open 100B**<br>102B-A12B | **MiMo-V2.5**<br>310B-A15B | **DeepSeek-V4-Flash**<br>284B-A13B, max | **Claude Haiku 4.5**<br>closed | **GPT-5.4 mini**<br>closed |
| ------------ | ----------------------------: | --------------------------------: | -------------------------: | --------------------------------------: | -----------------------------: | -------------------------: |
| KMMLU-Pro    |                   <u>78.4</u> |                              64.0 |                       69.1 |                                **78.9** |                           67.9 |                       78.1 |
| CLIcK        |                      **90.7** |                              78.9 |                       78.4 |                                    89.2 |                           53.5 |                <u>89.6</u> |
| HAE-RAE v1.1 |                      **73.8** |                       <u>73.3</u> |                       61.7 |                                    73.1 |                           38.5 |                       69.4 |
| Ko-AIME’25†  |                   <u>97.7</u> |                              80.0 |                       88.0 |                                **98.0** |                           81.7 |                       90.7 |
| HRM8K        |                   <u>92.2</u> |                              87.6 |                       90.7 |                                **93.4** |                           90.6 |                       91.3 |
| KBank-MMLU†  |                      **80.8** |                              65.5 |                       71.0 |                             <u>79.5</u> |                           68.9 |                       79.0 |
| KBL          |                      **75.5** |                              65.5 |                       69.8 |                                    72.8 |                           69.9 |                <u>75.3</u> |
| KorMedMCQA   |                          93.0 |                              84.4 |                       87.7 |                             <u>94.1</u> |                           87.0 |                   **94.2** |
| Ko-GDPval†   |                      **86.8** |                               3.4 |                       81.0 |                             <u>85.0</u> |                           68.3 |                       59.4 |

† in-house benchmarks.

---

## Quickstart

The examples below assume 8 GPUs with at least 141 GB of memory each, such as NVIDIA H200 or B200 GPUs.
Actual memory requirements depend on the context length and serving settings.

### Transformers

Use the [Upstage Transformers branch with native Solar Open 2 support](https://github.com/upstageAI/transformers/tree/v5.14.1-solar-open2) for local experimentation. For production serving, we recommend vLLM.

Install the dependencies:

> Install a CUDA-enabled PyTorch build for your platform before running this command. `fla-core` enables the optimized KDA kernels; without it, Transformers uses a substantially slower PyTorch fallback.

```bash
python -m pip install -U \
  "git+https://github.com/upstageAI/transformers.git@v5.14.1-solar-open2" \
  "fla-core[cuda]>=0.5.1" \
  accelerate einops
```

Run the model:

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "upstage/Solar-Open2-250B"

tokenizer = AutoTokenizer.from_pretrained(
    model_id,
    trust_remote_code=False,
)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    dtype=torch.bfloat16,
    trust_remote_code=False,
)
model.eval()

messages = [
    {"role": "user", "content": "What is Upstage?"},
]
prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    reasoning_effort="high",
    think_render_option="preserved",
)
input_device = model.get_input_embeddings().weight.device
model_inputs = tokenizer(prompt, return_tensors="pt").to(input_device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=32768,
    do_sample=True,
    temperature=1.0,
    top_p=1.0,
)

new_token_ids = generated_ids[0, model_inputs.input_ids.shape[-1] :].tolist()
think_end_id = tokenizer.convert_tokens_to_ids("<|think:end|>")

if think_end_id in new_token_ids:
    # Split immediately after the final <|think:end|> token.
    answer_start = len(new_token_ids) - new_token_ids[::-1].index(think_end_id)
else:
    # No end marker usually means generation stopped while the model was reasoning.
    answer_start = len(new_token_ids)

reasoning = tokenizer.decode(
    new_token_ids[:answer_start],
    skip_special_tokens=True,
).strip()
answer = tokenizer.decode(
    new_token_ids[answer_start:],
    skip_special_tokens=True,
).strip()

print("[reasoning]", reasoning)
print("[answer]", answer)
```

If the answer is empty, generation likely reached `max_new_tokens` before the reasoning block ended. Increase `max_new_tokens` and try again.

### Serving with vLLM (Recommended)

#### **Option 1: Docker**

The image below is based on vLLM v0.22.0 and CUDA 12.9.

```bash
docker run --rm --gpus all --ipc=host \
  -p 8000:8000 \
  -v "${HF_HOME:-$HOME/.cache/huggingface}:/root/.cache/huggingface" \
  upstage/vllm-solar-open2 \
  upstage/Solar-Open2-250B \
  --served-model-name solar-open2-250b \
  --tensor-parallel-size 8 \
  --enable-expert-parallel \
  --moe-backend triton \
  --default-chat-template-kwargs '{"think_render_option":"preserved"}' \
  --reasoning-parser solar_open2 \
  --tool-call-parser solar_open2 \
  --enable-auto-tool-choice \
  --logits-processors vllm.v1.sample.logits_processor.solar_open2:SolarOpen2TemplateLogitsProcessor
```

#### **Option 2: Install from source**

Install the [Upstage fork](https://github.com/UpstageAI/vllm/tree/v0.22.0-solar-open2) while reusing the matching vLLM v0.22.0 CUDA 12.9 wheel:

```bash
pip install -U uv

VLLM_PRECOMPILED_WHEEL_LOCATION="https://github.com/vllm-project/vllm/releases/download/v0.22.0/vllm-0.22.0%2Bcu129-cp38-abi3-manylinux_2_28_x86_64.whl" \
VLLM_USE_PRECOMPILED=1 \
uv pip install --reinstall-package vllm --torch-backend=cu129 \
  "git+https://github.com/UpstageAI/vllm.git@v0.22.0-solar-open2"
```

Start the server:

```bash
vllm serve upstage/Solar-Open2-250B \
  --served-model-name solar-open2-250b \
  --tensor-parallel-size 8 \
  --enable-expert-parallel \
  --moe-backend triton \
  --default-chat-template-kwargs '{"think_render_option":"preserved"}' \
  --reasoning-parser solar_open2 \
  --tool-call-parser solar_open2 \
  --enable-auto-tool-choice \
  --logits-processors vllm.v1.sample.logits_processor.solar_open2:SolarOpen2TemplateLogitsProcessor
```

Send a chat completion request:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "solar-open2-250b",
    "messages": [
      {"role": "user", "content": "What is Upstage?"}
    ],
    "max_tokens": 131584,
    "temperature": 1.0,
    "top_p": 1.0,
    "reasoning_effort": "high"
  }'
```

### Quantized Versions

Official quantized models by [NotaAI](https://huggingface.co/nota-ai) are available for deployment on smaller GPU configurations:
- [Solar-Open2-250B-Nota-INT4-GlobalPruned](https://huggingface.co/nota-ai/Solar-Open2-250B-Nota-INT4-GlobalPruned)
- [Solar-Open2-250B-Nota-NVFP4](https://huggingface.co/nota-ai/Solar-Open2-250B-Nota-NVFP4)
- [Solar-Open2-250B-Nota-INT4](https://huggingface.co/nota-ai/Solar-Open2-250B-Nota-INT4)

---

## Capabilities

### **Reasoning**

Use `reasoning_effort="high"` for reasoning and `reasoning_effort="none"` for a direct response. The recommended vLLM configuration limits a reasoning block to 131,072 tokens.

| Effort | Behavior                            |
| ------ | ----------------------------------- |
| `none` | Direct response                     |
| `high` | Reasoning, capped at 131,072 tokens |

`max_tokens` limits the complete response, including reasoning and the final answer, so leave room beyond the reasoning cap.

```python
from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

response = client.chat.completions.create(
    model="solar-open2-250b",
    messages=[
        {
            "role": "user",
            "content": "Prove that the square root of 2 is irrational.",
        },
    ],
    reasoning_effort="high",
    temperature=1.0,
    top_p=1.0,
    max_tokens=131584,
)

# The reasoning trace is returned separately from the final answer.
print(response.choices[0].message.reasoning)
print(response.choices[0].message.content)
```

### **Tool Calling**

Tool calls follow the standard OpenAI function-calling interface. Start the server with `--tool-call-parser solar_open2` and `--enable-auto-tool-choice`.

```python
from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                },
                "required": ["location"],
            },
        },
    },
]

response = client.chat.completions.create(
    model="solar-open2-250b",
    messages=[
        {
            "role": "user",
            "content": "What's the weather in Seoul?",
        },
    ],
    tools=tools,
)

print(response.choices[0].message.tool_calls)
```

## **Agentic Use**

Both Anthropic's Claude Code and Nous Research's Hermes Agent can run on Solar Open 2 served locally with vLLM (see the vLLM deployment guide). A single vLLM server exposes both interfaces: Claude Code connects through the Anthropic-compatible /v1/messages endpoint and Hermes Agent through the OpenAI-compatible /v1 endpoint (model id solar-open2-250b), each needing only a few environment variables or one provider entry — no setup script required. Tools exposed over the Model Context Protocol (MCP) reach the model through the same tool-calling interface, and both agents support MCP natively.

### **Claude Code**

vLLM exposes an Anthropic-compatible /v1/messages endpoint, so Claude Code connects directly — no proxy needed:

```
export ANTHROPIC_BASE_URL=http://localhost:8000
export ANTHROPIC_AUTH_TOKEN=dummy   # any non-empty value
export ANTHROPIC_MODEL=solar-open2-250b
export ANTHROPIC_SMALL_FAST_MODEL=solar-open2-250b
claude
```

The model name must match the server's --served-model-name (solar-open2-250b).

Prerequisites: the Claude Code CLI installed and a running vLLM server.

### **Hermes Agent**

Register the local vLLM server as a custom OpenAI-compatible provider in ~/.hermes/config.yaml:

```yaml
model:
  provider: custom
  default: solar-open2-250b
  base_url: http://localhost:8000/v1
  api_key: dummy
```

---

## Best Practices

Recommended **client-side generation settings** (the values a client / API caller should send)

Solar Open 2 is a reasoning-capable model. Use `reasoning_effort="high"` for complex or agentic tasks. The recommended vLLM configuration preserves the reasoning trace.

| Parameter          | Recommended | Notes                                               |
| ------------------ | ----------- | --------------------------------------------------- |
| `reasoning_effort` | `high`      | Recommended for complex reasoning and agentic tasks |
| `temperature`      | 1.0         |                                                     |
| `top_p`            | 1.0         |                                                     |
| `max_tokens`       | up to 256K  | Covers reasoning + output budget                    |

**Recommended settings by reasoning mode**

| Mode                      | temperature | top_p | max_tokens |
| ------------------------- | ----------- | ----- | ---------- |
| `reasoning_effort="none"` | 1.0         | 1.0   | up to 128K |
| `reasoning_effort="high"` | 1.0         | 1.0   | up to 256K |

- Set `max_tokens` high enough (up to 256K) — reasoning traces can be long and may otherwise truncate the answer.

- The reasoning trace is preserved by default (`think_render_option=preserved`).

- Multi-turn: Keep prior reasoning traces in the conversation history. The default `think_render_option=preserved` handles this automatically — do not strip reasoning from previous turns when constructing follow-up requests.

- **Parsing:** the OpenAI-compatible server returns reasoning in a separate `message.reasoning` field with local `transformers`, split the raw output on the reasoning markers yourself.

---

## License

Solar Open 2 is distributed under the [**Upstage Solar License**](https://huggingface.co/upstage/Solar-Open2-250B/blob/main/LICENSE).

**Key requirements for Derivative AI Models** (create / train / fine-tune / distill / improve using Solar Open 2):

- **Naming:** prefix your model name with "Solar" (e.g., `Solar-MyModel-v1`).

- **Attribution:** prominently display "Built with Solar" in related public-facing materials.

- **Notice:** include a copy of the Upstage Solar License with your derivative model.

---

## Citation

```bibtex
@misc{solaropen2-2026,
    title={Solar Open 2 Technical Report},
    author={Upstage AI},
    year={2026},
    eprint={2607.20062},
    archivePrefix={arXiv},
    primaryClass={cs.CL},
    url={https://arxiv.org/abs/2607.20062}
}
```

---
