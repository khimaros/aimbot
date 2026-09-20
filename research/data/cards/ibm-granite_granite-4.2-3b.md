---
license: apache-2.0
library_name: transformers
pipeline_tag: text-generation
language: [en, de, es, fr, ja, pt, ar, cs, it, ko, nl, zh]
tags: [granite, granite-4.2, reasoning, thinking, tool-calling, ibm]
base_model: [ibm-granite/granite-4.1-3b-base]
---

# Granite-4.2-3B

[![Collection](https://img.shields.io/badge/Granite_4.2-Collection-3B82F6?style=flat-square)](https://huggingface.co/collections/ibm-granite/granite-42-language-models)
[![Blog](https://img.shields.io/badge/Technical-Blog-10B981?style=flat-square)](https://huggingface.co/blog/ibm-granite/granite-4-2)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=flat-square&logo=github)](https://github.com/ibm-granite/granite-4.2-language-models)
[![License](https://img.shields.io/badge/License-Apache_2.0-EAB308?style=flat-square)](https://www.apache.org/licenses/LICENSE-2.0)

---

## Model Summary

| | |
|---|---|
| **Developers** | Granite Team, IBM |
| **Model Type** | Decoder-only Dense Transformer (Reasoning) |
| **Architecture** | GraniteForCausalLM |
| **Base Model** | [Granite-4.1-3B-Base](https://huggingface.co/ibm-granite/granite-4.1-3b-base) |
| **Parameters** | 3B |
| **Context Length** | Natively Supports 128K (Long-context extension to 512K) |
| **Precision** | bfloat16 |
| **Tested Languages** | English, German, Spanish, French, Japanese, Portuguese, Arabic, Czech, Italian, Korean, Dutch, Chinese (other languages may work but have not been fully tested) |
| **Reasoning Mode** | Built-in `<think>...</think>` chain-of-thought |
| **Best For** | Reasoning, Code Generation, Tool Calling, Agentic Workflows, Multilingual Dialog |
| **License** | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| **HF Collection** | [Granite 4.2 Language Models](https://huggingface.co/collections/ibm-granite/granite-42-language-models) |
| **Release Date** | August 25, 2026 |

---

## Model Overview

### What is IBM Granite?

Granite is a family of open-source large language models developed by IBM, designed for enterprise and research use. Granite models are built to be versatile, safe, and efficient — covering a range of sizes and capabilities from compact edge-deployable models to large-scale reasoning systems. All Granite models are released under the Apache 2.0 license, enabling unrestricted commercial and academic use.

The Granite 4.2 generation introduces native reasoning (thinking) capabilities, allowing models to perform step-by-step chain-of-thought reasoning before producing final answers. This significantly improves performance on complex math, coding, multi-step logic, and agentic tool-calling tasks.

### Description

**Granite-4.2-3B** is the compact reasoning model in the Granite 4.2 family. Despite its small parameter count, it delivers strong performance on reasoning-intensive tasks by leveraging built-in `<think>...</think>` chain-of-thought. It supports flexible thinking modes — full thinking (default), non-thinking, and low-effort — allowing users to balance depth vs. latency on a per-query basis.

Key capabilities:
- **Built-in Reasoning:** Native chain-of-thought that significantly improves performance on math, coding, and complex multi-step problems.
- **Flexible Thinking Modes:** Seamlessly switch between full thinking, non-thinking, and low-effort modes within a single model.
- **Reasoning-Augmented Tool Calling:** The model reasons about which tools to invoke and why, producing more accurate function calls.
- **512K Context Window:** Supports long documents, multi-turn conversations, and complex agentic workflows.
- **Apache 2.0 Licensed:** Fully open for commercial and research use.

---

## Model Design

Granite-4.2-3B is built on a decoder-only dense transformer architecture with the following core components:

* **Attention:** Grouped Query Attention (GQA) with 40 attention heads and 8 KV heads
* **Position Embedding:** Rotary Position Embedding (RoPE) with θ = 10,000,000
* **Feed-Forward:** MLP with SwiGLU activation (hidden size 8192)
* **Normalization:** RMSNorm (ε = 1e-5)
* **Embeddings:** Separate input/output embeddings (not tied)
* **Precision:** bfloat16

<table>
<thead>
  <tr>
    <th style="text-align:left; background-color: #001d6c; color: white;">Component</th>
    <th style="text-align:center; background-color: #001d6c; color: white;">3B Dense</th>
    <th style="text-align:center; background-color: #001d6c; color: white;">8B Dense</th>
    <th style="text-align:center; background-color: #001d6c; color: white;">30B Dense</th>
  </tr></thead>
<tbody>
  <tr>
    <td style="text-align:left;">Embedding size</td>
    <td style="text-align:center; background-color: #DAE8FF;">2560</td>
    <td style="text-align:center;">4096</td>
    <td style="text-align:center;">4096</td>
  </tr>
  <tr>
    <td style="text-align:left;">Number of layers</td>
    <td style="text-align:center; background-color: #DAE8FF;">40</td>
    <td style="text-align:center;">40</td>
    <td style="text-align:center;">64</td>
  </tr>
  <tr>
    <td style="text-align:left;">Attention head size</td>
    <td style="text-align:center; background-color: #DAE8FF;">64</td>
    <td style="text-align:center;">128</td>
    <td style="text-align:center;">128</td>
  </tr>
  <tr>
    <td style="text-align:left;">Number of attention heads</td>
    <td style="text-align:center; background-color: #DAE8FF;">40</td>
    <td style="text-align:center;">32</td>
    <td style="text-align:center;">32</td>
  </tr>
  <tr>
    <td style="text-align:left;">Number of KV heads</td>
    <td style="text-align:center; background-color: #DAE8FF;">8</td>
    <td style="text-align:center;">8</td>
    <td style="text-align:center;">8</td>
  </tr>
  <tr>
    <td style="text-align:left;">MLP hidden size</td>
    <td style="text-align:center; background-color: #DAE8FF;">8192</td>
    <td style="text-align:center;">12800</td>
    <td style="text-align:center;">32768</td>
  </tr>
  <tr>
    <td style="text-align:left;">MLP activation</td>
    <td style="text-align:center; background-color: #DAE8FF;">SwiGLU</td>
    <td style="text-align:center;">SwiGLU</td>
    <td style="text-align:center;">SwiGLU</td>
  </tr>
  <tr>
    <td style="text-align:left;">Sequence length</td>
    <td style="text-align:center; background-color: #DAE8FF;">131072</td>
    <td style="text-align:center;">131072</td>
    <td style="text-align:center;">131072</td>
  </tr>
  <tr>
    <td style="text-align:left;">Position embedding</td>
    <td style="text-align:center; background-color: #DAE8FF;">RoPE</td>
    <td style="text-align:center;">RoPE</td>
    <td style="text-align:center;">RoPE</td>
  </tr>
  <tr>
    <td style="text-align:left;"># Parameters</td>
    <td style="text-align:center; background-color: #DAE8FF;">3B</td>
    <td style="text-align:center;">8B</td>
    <td style="text-align:center;">30B</td>
  </tr>
</tbody></table>

---

## Training Methodology

Granite-4.2-3B is post-trained from [Granite-4.1-3B-Base](https://huggingface.co/ibm-granite/granite-4.1-3b-base) through a rigorous multi-stage pipeline that progressively unlocks reasoning, tool use, and instruction-following capabilities. A full listing of training datasets is available in the [Granite 4.2 GitHub repository](https://github.com/ibm-granite/granite-4.2-language-models). The training pipeline consists of three stages:

### Stage 1: Pre-Training

<!-- TODO: Add pre-training details here -->

Granite-4.2-3B builds on [Granite-4.1-3B-Base](https://huggingface.co/ibm-granite/granite-4.1-3b-base), which was pre-trained on a large-scale English as well as multilingual corpus. For full pre-training details (data composition, training recipe, and infrastructure), refer to our [Granite 4.1 Technical Blog](https://huggingface.co/blog/ibm-granite/granite-4-1).

### Stage 2: Supervised Fine-Tuning

<!-- TODO: Add SFT details here -->

 The SFT stage draws on instruction-following, chain-of-thought, and reasoning data to cultivate the model's reasoning and thinking abilities. For all the three, 3B, 8B and 30B models, the training corpus comprises four sources: (1) publicly available datasets under permissive licenses, (2) internally generated synthetic data targeting reasoning, tool calling, and chain-of-thought capabilities, (3) agentic traces collected across a diverse range of tasks, and (4) a curated selection of human-authored data. Hyperparameters were tuned before training was scaled to all three model sizes. For the 30B model, we conducted a second SFT phase, in which the agentic data was up-sampled while a smaller share of general replay data was retained. This phase trained for a single epoch, starting from a lower learning rate than Phase 1.

<!--...Please mention details on multi-phase SFT if necessary... This should be brief we will have more detailed version in technical blog. -->

### Stage 3: Reinforcement Learning

<!-- TODO: Add RL details here -->

The final stage of training applies multi-phase, multi-environment reinforcement learning using Group Relative Policy Optimization (GRPO). Training spans a broad mix of environments including math, code, science, instruction following, tool use, general chat and structured output. Most environments provide verifiable rewards, while open-ended prompts are scored by a generative reward model. Training runs asynchronously: generation and policy updates occupy separate GPU pools rather than proceeding in lockstep, and weights are refreshed in flight. 

After the reward-driven phases, a preference-alignment (RLHF) phase tunes helpfulness, conversational quality, and safety. Reinforcement learning is carried out with NeMo RL, and the RL environments run on NeMo Gym.

<!-- After the reward-driven phases, a preference-alignment (RLHF) phase tunes helpfulness, conversational quality, and safety, and a closing phase shortens the model's chain-of-thought for improved token efficiency. Reinforcement learning is carried out with NeMo RL, and the RL environments run on NeMo Gym. -->

<!--
The final stage of training applies multi-phase, multi-environment reinforcement learning using Group Relative Policy Optimization (GRPO). Training begins with several rounds of reinforcement learning across a broad mix of environments including math, code, science, instruction following, tool use, and structured output, followed by targeted phases that further sharpen key capabilities such as instruction following and coding. Most environments provide verifiable rewards, while open-ended prompts are scored by a generative reward model. Training runs asynchronously: generation and policy updates occupy separate GPU pools rather than proceeding in lockstep, and weights are refreshed in flight.

Several dedicated agentic RL phases then target multi-step tool use and long-horizon workflows across three settings: software engineering, where the model edits code and runs tests to resolve real repository issues in sandboxed containers; terminal use, where it operates a command-line shell to accomplish multi-step objectives; and web search, where it issues successive queries and reads results to gather evidence. Rollouts are complete agent trajectories that can span up to 200 tool-calling turns, so the model learns to plan, invoke tools, observe outcomes, and iterate toward a goal.

Finally, a preference-alignment (RLHF) phase tunes helpfulness, conversational quality, and safety. Reinforcement learning is carried out with NeMo RL, and the RL environments run on NeMo Gym.
-->

<!-- (Initial placeholder description) The RL stage further aligns the model for instruction following and safety. An additional agentic RL stage specifically targets multi-step tool use and agentic workflows, improving the model's ability to reason about when and how to invoke tools. ...Mention some details on conventional RL and Agentic RL...This should be brief we will have more detailed version in technical blog.  -->

---

**Infrastructure:**
We trained the Granite 4.2 Language Models utilizing an NVIDIA GB200 NVL72 cluster hosted in CoreWeave. Intra-rack communication occurs via the 72-GPU NVLink domain, and a non-blocking, full Fat-Tree NDR 400 Gb/s InfiniBand network provides inter-rack communication.

For further details on the post-training methodology, please refer to the [Granite-4.2 Technical Blog](https://huggingface.co/blog/ibm-granite/granite-4-2).

---

## Evaluation Results

<table>
<thead>
  <tr>
    <th style="text-align:left; background-color: #001d6c; color: white;">Task</th>
    <th style="text-align:center; background-color: #001d6c; color: white;">3B Dense</th>
    <th style="text-align:center; background-color: #001d6c; color: white;">8B Dense</th>
    <th style="text-align:center; background-color: #001d6c; color: white;">30B Dense</th>
  </tr>
</thead>
<tbody>
<tr>
  <td colspan="4" style="text-align:center; font-style:italic;">Agentic (Coding)</td>
</tr>
<tr>
    <td>SWE Bench Multilingual</td>
    <td style="text-align:center; background-color: #DAE8FF;">NA</td>
    <td style="text-align:center;">30.78</td><td style="text-align:center;">41.89</td>
</tr>
<tr>
    <td>SWE Bench Pro</td>
    <td style="text-align:center; background-color: #DAE8FF;">NA</td>
    <td style="text-align:center;">19.11</td><td style="text-align:center;">33.29</td>
</tr>
<tr>
    <td>SWE Bench Verified</td>
    <td style="text-align:center; background-color: #DAE8FF;">NA</td>
    <td style="text-align:center;">47.67</td><td style="text-align:center;">57</td>
</tr>
<tr>
    <td>Terminal-Bench 2.1</td>
    <td style="text-align:center; background-color: #DAE8FF;">NA</td>
    <td style="text-align:center;">20.56</td><td style="text-align:center;">29.24</td>
</tr>
<tr>
  <td colspan="4" style="text-align:center; font-style:italic;">Agentic (General)</td>
</tr>
<!-- <tr>
    <td>τ³-bench</td>
    <td style="text-align:center; background-color: #DAE8FF;">50.99</td>
    <td style="text-align:center;">66.34</td><td style="text-align:center;">68.05</td>
</tr> -->
<tr>
    <td>τ³-bench (AVG)</td>
    <td style="text-align:center;background-color: #DAE8FF;">45.78</td>
    <td style="text-align:center;">58.06</td><td style="text-align:center;">62.00</td>
</tr>
<tr>
    <td>BFCL (v4)</td>
    <td style="text-align:center; background-color: #DAE8FF;">52.41</td>
    <td style="text-align:center;">52.39</td><td style="text-align:center;">61.39</td>
</tr>
<tr>
    <td>ProfBench</td>
    <td style="text-align:center; background-color: #DAE8FF;">32.10</td>
    <td style="text-align:center;">41.20</td><td style="text-align:center;">42.90</td>
</tr>
<tr>
    <td>BirdBench</td>
    <td style="text-align:center; background-color: #DAE8FF;">NA</td>
    <td style="text-align:center;">41.07</td><td style="text-align:center;">41.85</td>
</tr>
<tr>
    <td>GDPval</td>
    <td style="text-align:center; background-color: #DAE8FF;">NA</td>
    <td style="text-align:center;">1189</td><td style="text-align:center;">1225</td>
</tr>
<tr>
  <td colspan="4" style="text-align:center; font-style:italic;">Reasoning</td>
</tr>
<tr>
    <td>AIME25</td>
    <td style="text-align:center; background-color: #DAE8FF;">78.33</td>
    <td style="text-align:center;">86.67</td><td style="text-align:center;">89.17</td>
</tr>
<tr>
    <td>HMMT Feb25</td>
    <td style="text-align:center; background-color: #DAE8FF;">66.67</td>
    <td style="text-align:center;">78.33</td><td style="text-align:center;">89.17</td>
</tr>
<tr>
    <td>GPQA</td>
    <td style="text-align:center; background-color: #DAE8FF;">54.80</td>
    <td style="text-align:center;">64.14</td><td style="text-align:center;">66.41</td>
</tr>
<tr>
    <td>LiveCodeBench v6</td>
    <td style="text-align:center; background-color: #DAE8FF;">69.71</td>
    <td style="text-align:center;">73.24</td><td style="text-align:center;">75.77</td>
</tr>
<tr>
    <td>SciCode</td>
    <td style="text-align:center; background-color: #DAE8FF;">24.11</td>
    <td style="text-align:center;">36.09</td><td style="text-align:center;">38.76</td>
</tr>
<tr>
  <td colspan="4" style="text-align:center; font-style:italic;">Chat & Instruction Following</td>
</tr>
<tr>
    <td>MMLU-Pro</td>
    <td style="text-align:center; background-color: #DAE8FF;">67.84</td>
    <td style="text-align:center;">74.04</td><td style="text-align:center;">77.60</td>
</tr>
<tr>
    <td>MMLU-ProX lite (IBM)</td>
    <td style="text-align:center; background-color: #DAE8FF;">27.78</td>
    <td style="text-align:center;">61.06</td><td style="text-align:center;">66.64</td>
</tr>
<tr>
    <td>Arena-Hard-V2</td>
    <td style="text-align:center; background-color: #DAE8FF;">34.96</td>
    <td style="text-align:center;">65.19</td><td style="text-align:center;">67.93</td>
</tr>
<tr>
    <td>IFBench (prompt)</td>
    <td style="text-align:center; background-color: #DAE8FF;">74.33</td>
    <td style="text-align:center;">79.33</td><td style="text-align:center;">77.17</td>
</tr>
<tr>
  <td colspan="4" style="text-align:center; font-style:italic;">Long Context</td>
</tr>
<tr>
    <td>RULER 64K</td>
    <td style="text-align:center; background-color: #DAE8FF;">67.52</td>
    <td style="text-align:center;">80.99</td><td style="text-align:center;">89.96</td>
</tr>
<tr>
    <td>RULER 128K</td>
    <td style="text-align:center; background-color: #DAE8FF;">55.30</td>
    <td style="text-align:center;">71.41</td><td style="text-align:center;">81.38</td>
</tr>
</tbody></table>

Evaluations are run with an evaluation framework based on NeMo [Evaluator SDK](https://github.com/NVIDIA-NeMo/Evaluator).

---

## Inference

### Generation Parameters

> **Important:** Use `temperature=1.0` and `top_p=0.95` across **all tasks and serving backends**, including general chat, reasoning, and tool calling.

| Parameter | Value | Notes |
|:----------|:------|:------|
| `temperature` | `1.0` | Required for all modes |
| `top_p` | `0.95` | Nucleus sampling threshold |
| `max_new_tokens` | `8192` | Thinking mode (increase for complex reasoning) |
| `max_new_tokens` | `2048` | Non-thinking mode |
| `do_sample` | `True` | Required when temperature > 0 |

### Thinking Modes

| Mode | Template Parameters | Behavior |
|:-----|:-------------------|:---------|
| **Thinking** (default) | `enable_thinking=True` | Full chain-of-thought reasoning inside `<think>...</think>` |
| **Non-thinking** | `enable_thinking=False` | Direct answer with no reasoning overhead |
| **Low-effort** | `enable_thinking=True, low_effort=True` | Brief reasoning for simpler queries |

### How It Works

- **Thinking enabled** — The generation prompt ends with `<|im_start|>assistant\n<think>\n`, causing the model to reason until it emits `</think>`, then produce the final answer.
- **Thinking disabled** — The prompt ends with `<|im_start|>assistant\n<think></think>`, bypassing reasoning entirely.
- **Low-effort** — Appends `{reasoning effort: low}` to the user message, signaling shorter reasoning chains.

### History Truncation

In multi-turn conversations, thinking content from previous assistant turns is automatically stripped (`truncate_history_thinking=True` by default) to conserve context window space. Only the current generation produces full reasoning. Set `truncate_history_thinking=False` to preserve full reasoning history.

---

## Serving with vLLM

Granite-4.2-3B is optimized for deployment with [vLLM](https://github.com/vllm-project/vllm).

> **Reasoning parser:** Use the custom `granite_thinking_parser` included in this repository (requires vLLM v0.20+). The model also works with the built-in `nemotron_v3` parser, but `granite_thinking_parser` provides better formatting of reasoning output. Native support for granite_thinking_parser will be added to vLLM and SGLang very soon.
> **Tool calling parser:** Use `qwen3_coder`.

### Starting the Server

```bash
vllm serve ibm-granite/granite-4.2-3b \
    --served-model-name granite-4.2-3b \
    --dtype bfloat16 \
    --max-model-len 131072 \
    --reasoning-parser granite_thinking_parser \
    --reasoning-parser-plugin ./granite_thinking_parser.py \
    --tool-call-parser qwen3_coder \
    --enable-auto-tool-choice
```

### OpenAI-Compatible API Usage

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="unused")

response = client.chat.completions.create(
    model="granite-4.2-3b",
    messages=[{"role": "user", "content": "Explain the Riemann hypothesis in simple terms."}],
    temperature=1.0,
    top_p=0.95,
    max_tokens=8192,
)

print(response.choices[0].message.content)
```

### Tool Calling via vLLM

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="unused")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather for a specified city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Name of the city"}
                },
                "required": ["city"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="granite-4.2-3b",
    messages=[{"role": "user", "content": "What's the weather like in Boston right now?"}],
    tools=tools,
    temperature=1.0,
    top_p=0.95,
    max_tokens=4096,
)

print(response.choices[0].message.tool_calls)
```


## Serving with SGLang

Granite-4.2-3B can also be served with [SGLang](https://github.com/sgl-project/sglang) (v0.5.18+) for high-throughput inference.


> **Reasoning parser:** Use `--reasoning-parser auto`, which resolves to the built-in `nemotron_3` parser for this checkpoint. It separates the thinking trace into `reasoning_content` and the final answer into `content`, and it handles all three thinking modes (`enable_thinking=True/False`, `low_effort=True`) described in [Thinking Modes](#thinking-modes).
> **Tool calling parser:** Use `--tool-call-parser auto`, which resolves to `qwen3_coder` for this checkpoint.

### Starting the Server

```bash
python3 -m sglang.launch_server \
    --model-path ibm-granite/granite-4.2-3b \
    --dtype bfloat16 \
    --context-length 131072 \
    --reasoning-parser auto \
    --tool-call-parser auto
```

### OpenAI-Compatible API Usage

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:30000/v1", api_key="unused")

response = client.chat.completions.create(
    model="ibm-granite/granite-4.2-3b",
    messages=[{"role": "user", "content": "Explain the Riemann hypothesis in simple terms."}],
    temperature=1.0,
    top_p=0.95,
    max_tokens=8192,
)

print(response.choices[0].message.reasoning_content)
print(response.choices[0].message.content)
```

### Tool Calling via SGLang

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:30000/v1", api_key="unused")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather for a specified city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Name of the city"}
                },
                "required": ["city"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="ibm-granite/granite-4.2-3b",
    messages=[{"role": "user", "content": "What's the weather like in Boston right now?"}],
    tools=tools,
    temperature=1.0,
    top_p=0.95,
    max_tokens=4096,
)

print(response.choices[0].message.tool_calls)
```

For a full deployment recipe (Docker, H200/B200 launch matrix, thinking-mode examples, and benchmark data), see the [SGLang Granite 4.2 cookbook](https://docs.sglang.io/cookbook/autoregressive/IBM/Granite-4.2).

---

## Using with Agentic Coding Harnesses

Granite-4.2-3B can be used as the backbone model for agentic coding tools. Since it supports reasoning and tool calling via the OpenAI-compatible API, it integrates with popular agentic harnesses out of the box. Start the vLLM server as shown in the [Serving with vLLM](#serving-with-vllm) section above, then follow the harness-specific instructions below.

### OpenCode

[OpenCode](https://opencode.ai) is an AI coding agent that runs in your terminal.

**Install:**

```bash
curl -fsSL https://opencode.ai/install | bash
```

**Configure** `~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "local/granite-4.2-3b",
  "provider": {
    "local": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "vLLM (local)",
      "options": {
        "baseURL": "http://localhost:8000/v1",
        "apiKey": "EMPTY"
      },
      "models": {
        "granite-4.2-3b": {
          "name": "Granite 4.2 3B",
          "limit": {
            "context": 131072,
            "output": 8192
          }
        }
      }
    }
  }
}
```

**Run:**

```bash
opencode
opencode run "your task description"
```

For full documentation, see [opencode.ai/docs](https://opencode.ai/docs).

### Pi

[Pi](https://pi.dev) is a minimal agent harness for AI-powered coding that runs in your terminal. It supports custom providers via a `models.json` configuration file.

**Install:**

```bash
curl -fsSL https://pi.dev/install.sh | sh
```

**Configure** `~/.pi/agent/models.json`:

```json
{
  "providers": {
    "vllm": {
      "baseUrl": "http://localhost:8000/v1",
      "api": "openai-completions",
      "apiKey": "EMPTY",
      "compat": {
        "supportsDeveloperRole": false,
        "supportsReasoningEffort": false
      },
      "models": [
        {
          "id": "granite-4.2-3b",
          "name": "Granite 4.2 3B",
          "reasoning": true,
          "input": ["text"],
          "contextWindow": 131072,
          "maxTokens": 8192,
          "samplingParams": {
            "temperature": 1.0,
            "top_p": 0.95
          },
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
        }
      ]
    }
  }
}
```

**Run:**

```bash
pi
```

Then select the `granite-4.2-3b` model with `/model` or `Ctrl+L` in the interactive session.

For full documentation, see [pi.dev/docs](https://pi.dev/docs/latest).

### OpenHands

[OpenHands](https://www.openhands.dev) is an AI software engineer that can plan, write code, and execute commands.

1. **Install and launch OpenHands** following the [official installation guide](https://docs.openhands.dev/openhands/usage/agent-canvas/setup).

2. **Configure the LLM** in the OpenHands settings with:
   - **Model:** `granite-4.2-3b`
   - **Base URL:** `http://localhost:8000/v1`
   - **API Key:** your vLLM `--api-key` value

> **Note:** The `openai/` prefix is required when connecting to OpenAI-compatible endpoints like vLLM. Refer to the [OpenHands local LLM documentation](https://docs.openhands.dev/openhands/usage/llms/local-llms) for detailed setup instructions, troubleshooting, and alternative installation methods.

---

## Quick Start (Transformers)

### Installation

```bash
pip install torch torchvision torchaudio
pip install accelerate transformers
```

### Basic Inference (Thinking Mode)

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = "ibm-granite/granite-4.2-3b"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="cuda", torch_dtype=torch.bfloat16)
model.eval()

messages = [
    {"role": "user", "content": "How many r's are in the word 'strawberry'?"},
]

text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

with torch.no_grad():
    output = model.generate(**inputs, max_new_tokens=8192, temperature=1.0, top_p=0.95, do_sample=True)

print(tokenizer.decode(output[0][inputs.input_ids.shape[-1]:], skip_special_tokens=False))
```

<details>
<summary><b>Example Output</b></summary>

```
<think>
Okay, let's see. The problem is to find how many 'r's are in the word 'strawberry'.

First, I need to write out the word: s t r a w b e r r y.

Now, I need to count the number of 'r' letters. Let's list each letter and check for 'r'.

1. s – not r
2. t – not r
3. r – yes, that's one
4. a – no
5. w – no
6. b – no
7. e – no
8. r – yes, that's two
9. r – yes, that's three
10. y – no

Total r's = 3.
</think>
There are **3** r's in the word "strawberry".<|im_end|>
```

</details>

### Non-Thinking Mode

```python
messages = [
    {"role": "user", "content": "What is the capital of France?"},
]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

output = model.generate(**inputs, max_new_tokens=2048, temperature=1.0, top_p=0.95, do_sample=True)
print(tokenizer.decode(output[0][inputs.input_ids.shape[-1]:], skip_special_tokens=False))
```

<details>
<summary><b>Example Output</b></summary>

```
<think></think>The capital of France is Paris.<|im_end|>
```

</details>

### Low-Effort Thinking

```python
messages = [
    {"role": "user", "content": "What is 2 + 2?"},
]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True,
                                     enable_thinking=True, low_effort=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

output = model.generate(**inputs, max_new_tokens=4096, temperature=1.0, top_p=0.95, do_sample=True)
print(tokenizer.decode(output[0][inputs.input_ids.shape[-1]:], skip_special_tokens=False))
```

<details>
<summary><b>Example Output</b></summary>

```
<think>
Simple answer.
</think>
2 + 2 = 4.<|im_end|>
```

</details>

---

## Tool Calling

Granite-4.2-3B supports tool calling with integrated reasoning — the model thinks about which tool to call and why before making the call. Tools are defined using the [OpenAI function definition schema](https://platform.openai.com/docs/guides/function-calling).

### Basic Tool Calling

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather for a specified city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Name of the city"}
                },
                "required": ["city"]
            }
        }
    }
]

messages = [
    {"role": "user", "content": "What's the weather like in Boston right now?"},
]
text = tokenizer.apply_chat_template(messages, tokenize=False, tools=tools,
                                     add_generation_prompt=True, enable_thinking=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

output = model.generate(**inputs, max_new_tokens=4096, temperature=1.0, top_p=0.95, do_sample=True)
print(tokenizer.decode(output[0][inputs.input_ids.shape[-1]:], skip_special_tokens=False))
```

<details>
<summary><b>Example Output</b></summary>

```
<think>
Okay, the user is asking for the weather in Boston right now. Let me check the tools
available. There's a function called get_current_weather that takes a city parameter.
I need to call that with the city set to Boston.
</think>
<tool_call>
<function=get_current_weather>
<parameter=city>
Boston
</parameter>
</function>
</tool_call>
<|im_end|>
```

</details>

### Multi-Turn with Tool Response

```python
messages = [
    {"role": "user", "content": "What's the weather like in Boston right now?"},
    {"role": "assistant", "content": "<think>\nThe user wants to know the current weather in Boston. I should call get_current_weather.\n</think>",
     "tool_calls": [{"function": {"name": "get_current_weather", "arguments": {"city": "Boston"}}}]},
    {"role": "tool", "content": '{"temperature": "72°F", "condition": "Partly cloudy", "humidity": "65%"}'},
]
text = tokenizer.apply_chat_template(messages, tokenize=False, tools=tools,
                                     add_generation_prompt=True, enable_thinking=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

output = model.generate(**inputs, max_new_tokens=4096, temperature=1.0, top_p=0.95, do_sample=True)
print(tokenizer.decode(output[0][inputs.input_ids.shape[-1]:], skip_special_tokens=False))
```

<details>
<summary><b>Example Output</b></summary>

```
<think>
The tool returned the weather data for Boston: temperature 72°F, partly cloudy, humidity 65%.
I need to present this information clearly to the user.
</think>
The current weather in Boston is 72°F, partly cloudy, with 65% humidity.<|im_end|>
```

</details>

---

## Multi-Turn Conversations

### History Thinking Truncation

```python
messages = [
    {"role": "user", "content": "What is 15 * 37?"},
    {"role": "assistant", "content": "<think>\nLet me calculate 15 * 37.\n15 * 37 = 15 * 30 + 15 * 7 = 450 + 105 = 555\n</think>\n15 * 37 = 555"},
    {"role": "user", "content": "Now divide that by 5"},
]

# Default: previous thinking is stripped to save context
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True,
                                     enable_thinking=True, truncate_history_thinking=True)

# To preserve full history:
text_full = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True,
                                          enable_thinking=True, truncate_history_thinking=False)
```

### Parsing Thinking vs. Final Answer

```python
import re

def parse_model_output(text):
    """Separate thinking content from final answer."""
    think_match = re.search(r'<think>(.*?)</think>', text, re.DOTALL)
    if think_match:
        thinking = think_match.group(1).strip()
        answer_start = text.find('</think>') + len('</think>')
        answer_end = text.find('<|im_end|>', answer_start)
        answer = text[answer_start:answer_end].strip() if answer_end != -1 else text[answer_start:].strip()
    else:
        thinking, answer = "", text.strip()
    return thinking, answer

thinking, answer = parse_model_output(output_text)
```

---

## Ethical Considerations and Limitations

Granite 4.2 models are primarily finetuned using instruction-response pairs mostly in English, but also multilingual data covering the supported languages listed above. Although this model handles multilingual dialog, its performance may vary compared to English. Few-shot examples can help in such cases.

While aligned for safety, the model may occasionally produce inaccurate, biased, or unsafe responses. The content within `<think>...</think>` tags represents internal reasoning and may contain unpolished or intermediate thoughts that do not represent final conclusions.

 To enhance safety in deployments, we recommend using Granite 4.2 alongside [Granite Guardian](https://huggingface.co/ibm-granite/granite-guardian-4.1-8b) to detect and flag risks across key dimensions outlined in the IBM AI Risk Atlas.

---

## Resources

- **Product Page:** https://www.ibm.com/granite
- **Documentation:** https://www.ibm.com/granite/docs/
- **Learning Resources:** https://ibm.biz/granite-learning-resources
- **Technical Blog:** https://huggingface.co/blog/ibm-granite/granite-4-2
- **GitHub:** https://github.com/ibm-granite/granite-4.2-language-models
- **HF Collection:** https://huggingface.co/collections/ibm-granite/granite-42-language-models
