---
library_name: transformers
language:
- en
pipeline_tag: text-generation
license: apache-2.0
base_model: JetBrains/Mellum2-12B-A2.5B-Base
model-index:
- name: Mellum2.1 Thinking
  results:
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: livecodebench
      name: "LiveCodeBench v6"
    metrics:
    - name: pass@1
      type: pass@1
      value: 82.0
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: humaneval-plus
      name: "HumanEval+"
    metrics:
    - name: pass@1
      type: pass@1
      value: 91.5
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: mbpp-plus
      name: "MBPP+"
    metrics:
    - name: pass@1
      type: pass@1
      value: 79.4
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: aime
      name: "AIME 25/26"
    metrics:
    - name: exact match
      type: exact_match
      value: 83.3
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: gsm-plus
      name: "GSM-Plus"
    metrics:
    - name: exact match
      type: exact_match
      value: 88.3
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: swe-bench-verified
      name: "SWE-bench Verified"
    metrics:
    - name: resolved rate
      type: resolved
      value: 47.0
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: terminal-bench
      name: "Terminal-Bench 2.1"
    metrics:
    - name: resolved rate
      type: resolved
      value: 17.4
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: swe-bench-pro
      name: "SWE-bench Pro"
    metrics:
    - name: resolved rate
      type: resolved
      value: 28.0
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: bfcl
      name: "BFCL v4"
    metrics:
    - name: accuracy
      type: acc
      value: 62.3
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: workbench
      name: "WorkBench"
    metrics:
    - name: task completion
      type: task_completion
      value: 44.6
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: toolhop
      name: "ToolHop"
    metrics:
    - name: accuracy
      type: acc
      value: 49.1
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: ifeval
      name: "IFEval"
    metrics:
    - name: accuracy
      type: acc
      value: 90.6
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: gpqa
      name: "GPQA Diamond"
    metrics:
    - name: accuracy
      type: acc
      value: 64.6
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: mmlu-redux
      name: "MMLU-Redux"
    metrics:
    - name: accuracy
      type: acc
      value: 87.8
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: mixeval
      name: "MixEval-Hard"
    metrics:
    - name: accuracy
      type: acc
      value: 46.4
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: xstest
      name: "XSTest"
    metrics:
    - name: safe compliance
      type: safe_compliance
      value: 88.8
      verified: false
  - task:
      type: text-generation
      name: Text Generation
    dataset:
      type: harmbench
      name: "HarmBench (harmful rate, lower is better)"
    metrics:
    - name: harmful rate
      type: harmful_rate
      value: 8.5
      verified: false
---

<img alt="Mellum" src="mellum-logo-dark.svg" width="320">

# Mellum2.1 Thinking

> [!Note]
> Mellum2.1 is a thinking model. Use it for complex agentic tasks, such as working in a repository, running commands, and calling tools, and for hard non-agentic problems in coding, math, and reasoning.

<img alt="Mellum2.1 benchmarks" src="mellum21_summary.png" width="100%">

## Mellum2.1 Highlights

Mellum2.1 is the next version of [Mellum2 Thinking](https://huggingface.co/JetBrains/Mellum2-12B-A2.5B-Thinking). The architecture is unchanged (a 12B mixture-of-experts model with 2.5B active parameters), and almost all of the work for this version went into post-training, primarily reinforcement learning (RL):

- **Reinforcement learning at a new scale:** RL went from a short final stage to the main part of training, after many experiments on both the methods and the data.
- **More data, filtered harder:** new RL tasks in math, competitive programming, science, tool use, and software engineering, combining open RL datasets with tasks we built ourselves and filtering every source before training.
- **Real environments for agentic skills:** for software engineering, the model trains inside real repositories with a shell and file-editing tools and is rewarded when the tests pass.

As a result, Mellum2.1 handles agentic tasks much better than Mellum2. After millions of sandboxed runs in real environments during training, it explores a codebase, edits files, and checks its own changes.

## Model Overview

**Mellum2.1 Thinking** has the following features:

- Number of Parameters: 12B total, 2.5B active
- Number of Layers: 28
- Hidden Size: 2304
- Intermediate Size: 7168
- MoE Intermediate Size: 896
- Number of Experts: 64
- Number of Activated Experts: 8
- Number of Attention Heads (GQA): 32 for Q and 4 for KV
- Context Length: 131,072
- Sliding Window: 1,024 (3 of every 4 layers)
- Vocabulary Size: 98,304
- Precision: bfloat16
- License: Apache 2.0

## Serving with vLLM

```sh
# Without tool calling
vllm serve JetBrains/Mellum2.1-12B-A2.5B-Thinking \
  --max-model-len 131072 \
  --reasoning-parser qwen3

# With tool calling
vllm serve JetBrains/Mellum2.1-12B-A2.5B-Thinking \
  --max-model-len 131072 \
  --reasoning-parser qwen3 \
  --enable-auto-tool-choice \
  --tool-call-parser hermes
```

GGUF builds for llama.cpp, Ollama, and LM Studio, as well as the multi-token prediction (MTP) head for speculative decoding in vLLM, are coming soon.

## Quickstart

```python
from openai import OpenAI
# Configured by environment variables
client = OpenAI()

messages = [
    {"role": "user", "content": "Find the bug in this function and explain the fix: def mean(xs): return sum(xs) / len(xs) - 1"},
]

chat_response = client.chat.completions.create(
    model="JetBrains/Mellum2.1-12B-A2.5B-Thinking",
    messages=messages,
    max_tokens=81920,
    temperature=0.6,
    top_p=0.95,
    extra_body={"top_k": 20},
)
print("Chat response:", chat_response)
```

## Evaluation

All values are percentages; higher is better except HarmBench, where lower is better. All models were evaluated by JetBrains with the same pipeline in thinking mode. All values are self-reported by JetBrains.

| Benchmark | Mellum2.1 Thinking | Mellum2 Thinking | Gemma 4 (E4B) | Qwen3.5 (9B) |
| :--- | ---: | ---: | ---: | ---: |
| **Coding** | | | | |
| LiveCodeBench v6 | 82.0 | 69.4 | 69.4 | 75.4 |
| HumanEval+ | 91.5 | 90.9 | 89.1 | 89.6 |
| MBPP+ | 79.4 | 75.4 | 70.9 | 69.8 |
| **Math** | | | | |
| AIME 25/26 | 83.3 | 60.1 | 45.0 | 86.7 |
| GSM-Plus | 88.3 | 87.1 | 87.4 | 91.4 |
| **Agentic** | | | | |
| SWE-bench Verified | 47.0 | 2.0 | 23.0 | 50.0 |
| Terminal-Bench 2.1 | 17.4 | 0.6 | 3.4 | 21.7 |
| SWE-bench Pro | 28.0 | 0.0 | 4.0 | 38.0 |
| **Tool Use** | | | | |
| BFCL v4 | 62.3 | 49.6 | 52.5 | 58.5 |
| WorkBench | 44.6 | 45.1 | 46.1 | 39.7 |
| ToolHop | 49.1 | 46.7 | 39.9 | 52.0 |
| **Conversational** | | | | |
| IFEval | 90.6 | 79.5 | 90.8 | 92.4 |
| **Knowledge** | | | | |
| GPQA Diamond | 64.6 | 51.0 | 53.1 | 77.8 |
| MMLU-Redux | 87.8 | 86.0 | 84.9 | 89.5 |
| MixEval-Hard | 46.4 | 41.6 | 41.4 | 50.3 |
| **Safety** | | | | |
| XSTest | 88.8 | 91.2 | 95.2 | 95.6 |
| HarmBench (↓) | 8.5 | 21.5 | 38.1 | 6.6 |

Notes:
- Non-agentic benchmarks use greedy decoding.
- **Agentic** benchmarks use the same open-source agent harness (Pi v0.73.1, shell and file tools) for every model, with each model's default sampling (temperature 1.0 for Mellum2.1), a 114K-token context, and up to 16K tokens per turn.
- **AIME** is the mean of AIME 2025 and AIME 2026 (30 questions each).
- **BFCL v4** is the macro-average of five subtasks: v1, v2, v3, web search, memory.
- Mellum2 Thinking was re-evaluated with this pipeline, so its numbers differ slightly from the [Mellum2 Technical Report](https://arxiv.org/abs/2605.31268).

## License

Released under the Apache 2.0 license.
