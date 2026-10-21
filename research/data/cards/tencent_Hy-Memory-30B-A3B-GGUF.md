---
language:
  - en
  - zh
pipeline_tag: text-generation
library_name: transformers
license: apache-2.0
base_model: tencent/Hy-Memory-30B-A3B
tags:
  - gguf
  - llama.cpp
---

<div align="center">
  <img src="./logo/hunyuanlogo.png" alt="Tencent Hunyuan" width="180"/>
  <h1>Hy-Memory-30B-A3B-GGUF</h1>
  <p><strong>Tencent Hunyuan</strong></p>
  <p>
    <a href="https://huggingface.co/tencent/Hy-Memory-30B-A3B-GGUF"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Hy--Memory--30B--A3B--GGUF-blue" alt="Model on Hugging Face"/></a>
    <a href="https://github.com/Tencent-Hunyuan/Hy-Memory"><img src="https://img.shields.io/badge/GitHub-Hy--Memory-181717?logo=github" alt="GitHub Repository"/></a>
    <a href="https://arxiv.org/pdf/2610.22196"><img src="https://img.shields.io/badge/Tech%20Report-arXiv%3A2610.22196-b31b1b?logo=arxiv&logoColor=white" alt="Tech Report"/></a>
  </p>
</div>

---

## GGUF Quantization

This repository provides GGUF quantizations of [Hy-Memory-30B-A3B](https://huggingface.co/tencent/Hy-Memory-30B-A3B) for efficient local inference with [llama.cpp](https://github.com/ggml-org/llama.cpp). Three quantization levels are available:

| Quantization | File | Size | LoCoMo Judge |
| :--- | :--- | ---: | ---: |
| Q6_K imatrix | `hy3a3b-memrl1009-step250-Q6_K-imat.gguf` | 24.71 GB | **58.78%** (154/262) |
| Q8_0 | `Hy-Memory-Step250-Q8_0.gguf` | 31.99 GB | 57.63% (151/262) |
| Q4_K_M imatrix | `hy3a3b-memrl1009-step250-Q4_K_M-imat.gguf` | 18.24 GB | 56.49% (148/262) |

All three files passed llama.cpp `--check-tensors`, real no-think generation, and the complete quantization evaluation described below.

### GGUF Evaluation Setup

- **Harness:** Mem0 2.0.19
- **Benchmark:** Fixed 20% LoCoMo test split
- **Evaluation size:** 2 users, 262 questions, and 59 memory chunks
- **Retrieval:** `top_k=10`, 10 turns per memory chunk
- **Memory temperature:** 0.7
- **Reasoning mode:** no-think
- **Embedding model:** `qwen3-embedding-8b-for-online` (4096 dimensions)
- **Answer and judge model:** `gpt-5.6-sol`
- **Inference framework:** official llama.cpp, commit `5aeac37a35b44fde4bdffaec9159f2fcb253b622`
- **KV cache:** F16

> The Q6_K imatrix version provides the strongest measured quality in this evaluation. The Q4_K_M imatrix version offers the smallest download and memory footprint.

---

## Model Introduction

**Hy-Memory-30B-A3B** is a compact long-term-memory writer model (~3B active parameters) developed by Tencent Hunyuan to execute the write path inside external memory frameworks. It directly replaces the general-purpose LLM inside **Mem0**, **MemOS**, and **Hy-Memory** (covering Chat, Working, and Coding scenarios), deciding what information to retain, how precisely to represent it, and how new evidence should update the persistent memory bank. The model is trained in two stages—Memory On-Policy Distillation (OPD) followed by Attributed Memory Reinforcement Learning—and transfers directly to unseen memory frameworks such as **EverMemOS**.

<div align="center">
  <img src="./figures/fig3_cross_harness_colm.png" alt="Cross-harness macro-average scores" width="90%"/>
  <p><em>Cross-harness macro-average scores on the fixed 20% benchmark matrix. Each harness score averages six metrics equally; Overall averages the four harnesses equally. EverMemOS is held out from training.</em></p>
</div>

---

## Two-Stage Training

<div align="center">
  <img src="./figures/fig1_training_process.png" alt="Two-stage training process" width="96%"/>
  <p><em>Figure 1: Hy-Memory-30B-A3B is trained inside the same deployed harness configurations in both stages. OPD supplies dense teacher supervision on student-written state chains; RL examines the resulting banks, assigns chunk-level credit, and carries the selected bank across windows. In the rollout grid, each cell is the bank after chunk t of rollout i, shaded by its chunk score s_i[t]. Advantages are normalized within each column (dashed: one chunk-level group), so the best rollout can differ from chunk to chunk. The outlined cell is the final bank with the highest sum_t s_i[t], which becomes the parent of the next window.</em></p>
</div>

---

## Experiments

> The full cross-harness results below are reproduced from the original Hy-Memory-30B-A3B model card. GGUF-specific measurements are reported in the **GGUF Quantization** section above.

### Evaluation Principles

The evaluation changes only the memory writer. For each comparison, the harness version and prompts are fixed, retrieval configuration is fixed, and the answer model, judge, and other framework-side components are held fixed. Throughout this report, every reference to a DeepSeek Flash endpoint denotes **DeepSeek V4.1 Flash**. Decoding settings are matched where APIs permit, each writer builds its own bank from an empty state, and test examples and scoring rules are identical.

For computational efficiency, every benchmark in the main four-harness matrix is evaluated on a fixed 20% subsample. Each harness score is the equal-weight average of six metrics: **LoCoMo Judge**, **LongMemEval (LME)**, **PersonaMem-v2 (PM-v2)**, **Travel SPS**, **Shopping PS**, and **Code Memory Bench (CMB)**. CMB is itself the equal-weight average of two repository QA evaluations. The overall score is the equal-weight average of the four harness scores.

### Final Cross-Harness Results

| Memory writer | Mem0 | Hy-Mem. | MemOS | EverMem. | Avg. |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **Hy-Memory-30B-A3B** | **54.02** | **60.55** | **50.51** | **56.89** | **55.49** |
| Claude Opus 5 | 53.43 | 60.53 | 50.50 | 54.04 | 54.62 |
| DeepSeek V4.1 Flash | 49.73 | 60.20 | 49.17 | 55.47 | 53.64 |
| Hy3 | 45.99 | 58.06 | 50.19 | 52.30 | 51.63 |
| Qwen3.6-35B-A3B | 47.51 | 55.87 | 47.36 | 50.75 | 50.37 |
| Hy3-A3B Base | 40.20 | 50.39 | 49.05 | 50.98 | 47.66 |
| Qwen3-30B-A3B | 39.81 | 45.67 | 45.44 | 46.57 | 44.37 |

*Table 1: Six-metric means on fixed 20% benchmark subsamples. The macro average weights the four harnesses equally.*

### Detailed Benchmark Results

Tables 2–5 report the six benchmark scores used to compute each harness mean in Table 1 on the same fixed 20% benchmark subsamples.

#### Table 2: Detailed results on the Mem0 harness

| Writer | LoCoMo | LME | PM-v2 | Travel | Shop. | CMB | Avg. |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Hy-Memory-30B-A3B** | 59.54 | **73.00** | 51.62 | **54.51** | 18.33 | 67.13 | **54.02** |
| Claude Opus 5 | **69.47** | 66.00 | **53.58** | 42.98 | 17.78 | **70.74** | 53.43 |
| DeepSeek V4.1 Flash | 58.78 | 69.39 | 49.56 | 35.07 | 16.67 | 68.92 | 49.73 |
| Hy3 | 41.22 | 62.00 | 44.44 | 46.87 | 17.22 | 64.16 | 45.99 |
| Qwen3.6-35B-A3B | 50.00 | 69.00 | 49.38 | 36.39 | **20.00** | 60.30 | 47.51 |
| Hy3-A3B Base | 50.00 | 47.00 | 40.82 | 37.91 | 14.44 | 51.03 | 40.20 |
| Qwen3-30B-A3B | 46.18 | 56.00 | 42.32 | 31.98 | 16.67 | 45.68 | 39.81 |

#### Table 3: Detailed results on the Hy-Memory harness

| Writer | LoCoMo | LME | PM-v2 | Travel | Shop. | CMB | Avg. |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Hy-Memory-30B-A3B** | 73.28 | 89.00 | 51.54 | **57.65** | 21.11 | 70.73 | **60.55** |
| Claude Opus 5 | **74.43** | **89.69** | 48.71 | 51.34 | **23.33** | 75.70 | 60.53 |
| DeepSeek V4.1 Flash | 72.90 | 85.86 | 49.00 | 53.46 | 22.78 | **77.18** | 60.20 |
| Hy3 | 69.47 | 89.00 | **52.76** | 49.01 | 21.67 | 66.44 | 58.06 |
| Qwen3.6-35B-A3B | 70.99 | 84.85 | 43.56 | 49.82 | 20.00 | 65.98 | 55.87 |
| Hy3-A3B Base | 66.41 | 87.00 | 49.84 | 31.36 | 17.78 | 49.97 | 50.39 |
| Qwen3-30B-A3B | 64.12 | 82.00 | 41.06 | 32.83 | 18.89 | 35.10 | 45.67 |

#### Table 4: Detailed results on the MemOS harness

| Writer | LoCoMo | LME | PM-v2 | Travel | Shop. | CMB | Avg. |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Hy-Memory-30B-A3B** | 62.98 | 73.00 | 51.92 | 24.15 | 21.11 | 69.91 | **50.51** |
| Claude Opus 5 | **63.74** | 79.38 | **52.84** | 22.14 | 19.44 | 65.46 | 50.50 |
| DeepSeek V4.1 Flash | 61.07 | 73.00 | 50.68 | 18.61 | **21.67** | **69.97** | 49.17 |
| Hy3 | 62.98 | **81.00** | 49.64 | 18.87 | 18.89 | 69.78 | 50.19 |
| Qwen3.6-35B-A3B | 55.34 | 79.00 | 51.34 | 20.08 | 15.56 | 62.82 | 47.36 |
| Hy3-A3B Base | 58.40 | 73.00 | 50.86 | **26.05** | 21.11 | 64.88 | 49.05 |
| Qwen3-30B-A3B | 59.16 | 73.00 | 48.28 | 23.03 | 16.67 | 52.49 | 45.44 |

#### Table 5: Detailed results on the held-out EverMemOS harness

| Writer | LoCoMo | LME | PM-v2 | Travel | Shop. | CMB | Avg. |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Hy-Memory-30B-A3B** | **73.28** | 76.00 | 53.28 | 56.56 | 19.05 | **63.19** | **56.89** |
| Claude Opus 5 | **73.28** | 80.41 | 51.19 | 45.91 | **23.89** | 49.53 | 54.04 |
| DeepSeek V4.1 Flash | 72.52 | 82.83 | 49.74 | **59.47** | 18.89 | 49.38 | 55.47 |
| Hy3 | 68.70 | **83.00** | 48.68 | 46.52 | 19.44 | 47.44 | 52.30 |
| Qwen3.6-35B-A3B | 69.08 | 79.00 | 50.60 | 43.53 | 18.77 | 43.52 | 50.75 |
| Hy3-A3B Base | 64.50 | 81.00 | 52.14 | 41.74 | 20.56 | 45.93 | 50.98 |
| Qwen3-30B-A3B | 67.94 | 60.00 | 47.10 | 44.80 | 18.33 | 41.27 | 46.57 |

---

## Quickstart

We recommend using a recent official llama.cpp build. The commands below were validated with llama.cpp commit `5aeac37a35b44fde4bdffaec9159f2fcb253b622` and the Q6_K imatrix model.

### 1. Launch the llama.cpp server

```bash
llama-server \
  --model ./hy3a3b-memrl1009-step250-Q6_K-imat.gguf \
  --alias hy-memory-q6-k-imat \
  --host 127.0.0.1 \
  --port 8000 \
  --n-gpu-layers all \
  --flash-attn on \
  --ctx-size 65536 \
  --parallel 1 \
  --batch-size 2048 \
  --ubatch-size 512 \
  --cache-type-k f16 \
  --cache-type-v f16 \
  --temp 0.7 \
  --top-k 0 \
  --top-p 1.0 \
  --repeat-penalty 1.0 \
  --jinja \
  --chat-template-kwargs '{"reasoning_effort":"no_think"}' \
  --check-tensors
```

`--ctx-size` is the total context available to the server. The single-slot configuration above provides a 64K context window. If you use `--parallel 2` to provide two slots, set `--ctx-size 131072` to retain up to 64K context per request.

### 2. Call the server with the OpenAI Python SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="EMPTY",
)

response = client.chat.completions.create(
    model="hy-memory-q6-k-imat",
    messages=[
        {
            "role": "user",
            "content": (
                "Extract the durable memory from the following conversation and "
                "return only one concise sentence:\n\n"
                "User: I moved from Boston to Seattle in March 2025, and my "
                "preferred contact method is email."
            ),
        }
    ],
    temperature=0.7,
    top_p=1.0,
    max_tokens=512,
    extra_body={"reasoning_effort": "no_think"},
)

print(response.choices[0].message.content)
```

### 3. Call the server with curl

```bash
curl http://127.0.0.1:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "hy-memory-q6-k-imat",
    "messages": [
      {
        "role": "user",
        "content": "Extract the durable memory and return only one concise sentence: User: I moved from Boston to Seattle in March 2025, and my preferred contact method is email."
      }
    ],
    "temperature": 0.7,
    "top_p": 1.0,
    "max_tokens": 512,
    "reasoning_effort": "no_think"
  }'
```

The server-level `--chat-template-kwargs` enables no-think mode by default. Setting `reasoning_effort=no_think` in each request makes the behavior explicit and easier to audit.

---

## Resource Availability

- **Framework Code & Evaluation Utilities:** [https://github.com/Tencent-Hunyuan/Hy-Memory](https://github.com/Tencent-Hunyuan/Hy-Memory)
- **GGUF Model Weights and Model Card:** [https://huggingface.co/tencent/Hy-Memory-30B-A3B-GGUF](https://huggingface.co/tencent/Hy-Memory-30B-A3B-GGUF)
- **Original BF16 Model:** [https://huggingface.co/tencent/Hy-Memory-30B-A3B](https://huggingface.co/tencent/Hy-Memory-30B-A3B)
- **Technical Report:** [https://arxiv.org/pdf/2610.22196](https://arxiv.org/pdf/2610.22196)

