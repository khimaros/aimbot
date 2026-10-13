---
license: apache-2.0
base_model: FINAL-Bench/Darwin-27B-Opus
library_name: transformers
pipeline_tag: text-generation
language:
- en
- ko
- multilingual
tags:
- darwin
- darwin-rsi
- recursive-self-improvement
- model-level-rsi
- rsi
- self-improvement
- self-improving-ai
- self-evolving
- no-human-labels
- label-free
- reasoning
- thinking
- chain-of-thought
- gpqa
- supergpqa
- decision-index
- typed-decisions
- jev
- system-2
- qwen3.5
- 27b
- vidraft
- final-bench
---

<p align="center">
  <a href="https://vidraft.net"><img src="https://img.shields.io/badge/🌐_VIDRAFT-vidraft.net-111111?style=for-the-badge" alt="VIDRAFT"></a>
  <a href="https://huggingface.co/FINAL-Bench"><img src="https://img.shields.io/badge/🤗_FINAL--Bench-Organization-ffce3a?style=for-the-badge" alt="FINAL-Bench"></a>
  <a href="https://huggingface.co/collections/FINAL-Bench/darwin-family"><img src="https://img.shields.io/badge/🏠_Darwin_Family-Collection-green?style=for-the-badge" alt="Darwin Family"></a>
</p>

# Darwin-27B-RSI: A Model That Improved Itself — Learning Only From Its Own Solutions

<p align="center">
  <a href="https://huggingface.co/FINAL-Bench/Darwin-27B-RSI"><img src="https://img.shields.io/badge/🔁_RSI-GPQA_+5.24pp-gold?style=for-the-badge" alt="RSI gain"></a>
  <a href="https://huggingface.co/spaces/multimodalart/jev-decision-index"><img src="https://img.shields.io/badge/🏁_Decision_Index-Darwin--27B--JEV_≈61.1-blue?style=for-the-badge" alt="Decision Index"></a>
  <a href="https://huggingface.co/datasets/FINAL-Bench/Darwin-27B-JEV-decision-index"><img src="https://img.shields.io/badge/📊_Full_run-121K_decisions-lightgrey?style=for-the-badge" alt="Results"></a>
</p>

<p align="center">
  <a href="https://huggingface.co/FINAL-Bench/Darwin-27B-Opus"><img src="https://img.shields.io/badge/🧬_Parent-Darwin--27B--Opus-blue?style=for-the-badge" alt="Parent"></a>
  <a href="https://huggingface.co/FINAL-Bench/Darwin-31B-Opus"><img src="https://img.shields.io/badge/🧬_Model-Darwin--31B--Opus-blue?style=for-the-badge" alt="31B"></a>
  <a href="https://huggingface.co/FINAL-Bench/Darwin-9B-Opus"><img src="https://img.shields.io/badge/🧬_Model-Darwin--9B--Opus-blue?style=for-the-badge" alt="9B"></a>
</p>

> Qwen3.5-27B family · 27B dense · Thinking mode · BF16 · Apache 2.0
> **No human-written answers. The model generated its own learning signal — and got measurably better.**

---

## Abstract

**Darwin-27B-RSI** is [Darwin-27B-Opus](https://huggingface.co/FINAL-Bench/Darwin-27B-Opus) after **Recursive Self-Improvement (RSI)**: the model was improved using only signal it produced itself. During self-improvement, the model itself (its weights) improves by learning only from its own solutions. No human-written solutions or reasoning traces are used; correctness is checked automatically (agreement across its own samples and code execution).

Under an identical evaluation protocol, Darwin-27B-RSI improves over its parent on graduate-level science reasoning — **+5.24 points on GPQA Diamond** (single sample) and **+3.79 points** with majority voting — with every gain statistically significant in paired tests.

As the reasoning engine of **Darwin-27B-JEV** on the [Decision Index](https://huggingface.co/spaces/multimodalart/jev-decision-index), it lifts the hardest reasoning decisions: GPQA Diamond skill **0.31 → 0.71**, GSM8K **0.61 → 0.97**, MMLU-Pro **0.60 → 0.82**.

---

## Model-level RSI vs. harness-level RSI

**Darwin-27B-RSI is Model-level RSI: the model itself (its weights) improves by learning only from its own solutions. No human-written solutions or reasoning traces are used; correctness is checked automatically.** You download a new model file, and it is smarter on its own.

Harness-level RSI (for example, Google's [RRSI](https://github.com/google-research/rrsi)) improves the prompts, tools and workflow *around* a fixed model — like rewriting an employee's manual, while Model-level RSI is the employee getting smarter. The two are complementary: a harness-level loop can run on top of a Model-level RSI model.

## What Is RSI?

Most models improve only when people write more answers for them. **Recursive Self-Improvement** removes that bottleneck: the model works on problems, judges its own work, and learns from what it produced — then repeats. Each improved model becomes the starting point for the next improvement.

Darwin-27B-RSI demonstrates this loop on a 27B model:

- **Human-written solutions or reasoning traces used:** 0
- **Direction of change:** measurably better on held-out graduate-level science
- **Contamination check:** training problems share 0 items with the evaluation sets reported here

The training procedure itself is not released.

---

## Results

### Science reasoning (same protocol for both models)

| Benchmark | Darwin-27B-Opus | **Darwin-27B-RSI** | Δ |
|---|---|---|---|
| GPQA Diamond (1 sample) | 72.85 | **78.09** | **+5.24** |
| GPQA Diamond (majority@16) | 79.80 | **83.59** | **+3.79** |
| SuperGPQA (1 sample) | | | **+4.03** |

Both models were measured under the same protocol (single sample, identical sampling settings and token budget), so numbers differ from the Darwin-27B-Opus card, which reports a different protocol. All gains are statistically significant in paired tests.

### Decision Index — as the reasoning engine of Darwin-27B-JEV

The [Decision Index](https://huggingface.co/spaces/multimodalart/jev-decision-index) scores typed-decision engines on 43 benchmarks and ~121K decisions (chance-corrected: 0 = random, 1 = perfect). Darwin-27B-RSI handles the decisions that need real thinking:

| Benchmark (skill) | before | **with Darwin-27B-RSI** |
|---|---|---|
| GPQA Diamond ★ | 0.31 | **0.71** |
| GSM8K | 0.61 | **0.97** |
| CRUXEval | 0.61 | **0.87** |
| MMLU-Pro ★ | 0.60 | **0.82** |
| BBH ★ | 0.68 | **0.83** |
| CLadder | 0.49 | **0.70** |

★ = gold benchmark (weighted 1.2× on the board).
**Darwin-27B-JEV: ≈ 61.1** under the v0.2.1 board rules (our recomputation; official score pending review). Full run: [FINAL-Bench/Darwin-27B-JEV-decision-index](https://huggingface.co/datasets/FINAL-Bench/Darwin-27B-JEV-decision-index).

---

## Usage

Darwin-27B-RSI is a thinking model. Give it room to reason and read the answer after the reasoning block.

### Transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "FINAL-Bench/Darwin-27B-RSI"
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype="bfloat16", device_map="auto")

messages = [{"role": "user", "content": "A ball is thrown upward at 40 m/s. For how long is it above 40 m? (g = 10 m/s²) Think, then give the final answer."}]
inputs = tok.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(model.device)
out = model.generate(inputs, max_new_tokens=8192, temperature=0.6, top_p=0.95, do_sample=True)
print(tok.decode(out[0][inputs.shape[1]:], skip_special_tokens=True))
```

### vLLM

```bash
vllm serve FINAL-Bench/Darwin-27B-RSI --max-model-len 32768
```

Recommended: temperature 0.6, top_p 0.95, generous token budget (8K–16K) for hard problems.

---

## Model Details

| | |
|---|---|
| Parent | [FINAL-Bench/Darwin-27B-Opus](https://huggingface.co/FINAL-Bench/Darwin-27B-Opus) |
| Architecture | Qwen3.5 family, 27B dense |
| Precision | BF16 |
| Improvement method | Recursive Self-Improvement, no human labels |
| License | Apache 2.0 |
| Developer | [VIDRAFT](https://vidraft.net) · [FINAL-Bench](https://huggingface.co/FINAL-Bench) |

## Limitations and Disclosure

- Gains were measured on graduate-level science; other domains may change less.
- As a thinking model, it can produce long reasoning; cap `max_new_tokens` for latency-sensitive use.
- 31 training problems (0.22% of the benchmark) overlap with the Decision Index MMLU set; the model learned only from its own solutions to them.
- Not affiliated with TypeSafe AI or its Jev product.

## Citation

```bibtex
@misc{darwin27b_rsi_2026,
  title  = {Darwin-27B-RSI: Recursive Self-Improvement without Human Labels},
  author = {VIDRAFT and FINAL-Bench},
  year   = {2026},
  url    = {https://huggingface.co/FINAL-Bench/Darwin-27B-RSI}
}
```

<p align="center"><a href="https://vidraft.net"><img src="https://img.shields.io/badge/Made_by-VIDRAFT-111111?style=flat-square" alt="VIDRAFT"></a></p>
