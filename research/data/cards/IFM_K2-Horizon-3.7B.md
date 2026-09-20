---
pipeline_tag: text-generation
library_name: transformers
model_name: K2-Horizon-3.7B
language:
  - en
license: apache-2.0
datasets:
  - IFM/K2-Horizon-Pretrain-Data
  - IFM/K2-Horizon-Midtrain-Data
tags:
  - k2-horizon
  - 3.7b
  - dense
  - open-weights
  - ifm
---

# K2-Horizon-3.7B


K2-Horizon-3.7B is the small dense member of the K2-Horizon family: a 3.7B-core decoder-only model with a 512K context window.

<p align="center">
  <img src="assets/k2-horizon-3.7b-benchmarks.png" alt="K2-Horizon-3.7B benchmark results" width="100%">
</p>

## K2-Horizon-3.7B Highlights

- **Strong small-model baseline.** A dense model evaluated on the same agentic, coding, and reasoning benchmarks as the rest of the family.
- **512K context.** Native 524,288-token context from the midtraining stages onward.
- **Intermediate checkpoints.** Intermediate checkpoints are released so capability changes can be studied across training rather than at a single checkpoint.
- **Fully open.** Training data and recipe, training code, and evaluation resources are public.

## Benchmark Results

The chart at the top of this card shows K2-Horizon-3.7B against selected reference models. The table below lists every comparison model used in the figure.

### Full Results

<!-- TABLE:START -->
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;margin:0 auto;padding:8px 0 16px;overflow-x:auto"><table style="display:table;width:100%;table-layout:fixed;border-collapse:collapse;font-size:12px;margin:0"><thead><tr><th style="width:30%;border-bottom:none"></th><th colspan="5" style="padding:6px 4px 2px;text-align:center;font-size:11px;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;opacity:0.65;border-bottom:1px solid rgba(128,128,128,0.25)">Open-weight dense models</th></tr><tr><th style="padding:10px 6px;text-align:left;border-bottom:2px solid #2450D6"></th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:14%;overflow-wrap:anywhere;background:rgba(36,80,214,0.08);">K2-Horizon-3.7B</th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:14%;overflow-wrap:anywhere;">Qwen3.5-4B</th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:14%;overflow-wrap:anywhere;">G9v3-3B</th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:14%;overflow-wrap:anywhere;">Granite 4.2-3B</th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:14%;overflow-wrap:anywhere;">Nemotron 3 Nano-4B</th></tr></thead><tbody><tr><td style="padding:7px 4px 7px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;font-weight:600"># Params</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">3.7B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">4B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">3B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">3B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">4B</td></tr><tr><td style="padding:7px 4px 7px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;font-weight:600"># Activated params</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">3.7B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">4B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">3B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">3B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">4B</td></tr><tr><td style="padding:7px 4px 7px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;font-weight:600">Architecture</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">Dense</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">Dense</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">Dense</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">Dense</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">Dense</td></tr><tr><td colspan="6" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Math</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">HMMT Feb 2026</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Competition mathematics</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>70.5</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">61.6</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">34.1</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">57.2</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">34.7</td></tr><tr><td colspan="6" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Coding</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">SWE-bench Verified</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Software engineering</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>68.6</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">41.2</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">16.4</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">32.2</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">1.8</td></tr><tr><td colspan="6" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Scientific Reasoning</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">GPQA Diamond</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Graduate-level science QA</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>65.4</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">77.1</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">43.8</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">55.9</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">51.3</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">HLE</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Expert-level reasoning</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>12.9</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">9.9</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">4.5</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">6.6</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">4.9</td></tr><tr><td colspan="6" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Coding</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">SciCode</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Scientific coding</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>25.9</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">16.1</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">17.7</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">24.9</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">16.4</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">Terminal-Bench 2.1</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Agentic terminal use</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>25.1</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">25.8</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">6.0</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">13.9</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">3.7</td></tr><tr><td colspan="6" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Agents</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">tau3-Banking</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Agentic tool use</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>17.7</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">6.8</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">—</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">5.6</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">—</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">BFCL v4</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Function calling</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>50.9</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">55.7</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">47.9</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">50.8</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">36.8</td></tr></tbody></table></div>
<!-- TABLE:END -->

Scores in %. Bold marks the best score in each row. Baseline protocols may differ; 

## Quickstart

### Serving

vLLM, recipe at [recipes.vllm.ai/IFM](https://recipes.vllm.ai/IFM):

```shell
vllm serve IFM/K2-Horizon-3.7B \
  --trust-remote-code \
  --dtype bfloat16 \
  --tensor-parallel-size 1 \
  --reasoning-parser k2_horizon \
  --enable-auto-tool-choice \
  --tool-call-parser k2_horizon
```

Use an exact branch name from the inventory with vLLM's `--revision` option. For example, `--revision pretrain_1100000` selects the final checkpoint of Pretraining, at step 1,100,000.

SGLang, this is the recipe validated in the [SGLang K2 Horizon cookbook](https://docs.sglang.io/cookbook/autoregressive/IFM/K2-Horizon):

```shell
sglang serve \
  --model-path IFM/K2-Horizon-3.7B \
  --revision c177771836a4c460743c00002c22483f6f18d1eb \
  --tp 1 \
  --dtype bfloat16 \
  --attention-backend fa3 \
  --reasoning-parser k2_horizon \
  --host 0.0.0.0 \
  --port 30000
```

### API Usage

> [!Tip]
> Recommended settings: `reasoning_effort="high"`, `temperature=1.0`, `top_p=0.95`, and at least 32,768 output tokens.
> Reasoning depth is selected per request through `chat_template_kwargs`. Thinking is returned in `reasoning_content` and the answer in `content`.

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:30000/v1", api_key="EMPTY")
response = client.chat.completions.create(
    model="IFM/K2-Horizon-3.7B",
    messages=[{"role": "user", "content": "Explain the result step by step."}],
    temperature=1.0,
    top_p=0.95,
    max_tokens=32768,
    extra_body={"chat_template_kwargs": {"reasoning_effort": "high"}},
)
message = response.choices[0].message
print("Reasoning:", getattr(message, "reasoning_content", None))
print("Answer:", message.content)
```

### Transformers

Validated with Transformers 5.15.0, PyTorch 2.13.0, Safetensors 0.8.0.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "IFM/K2-Horizon-3.7B"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id, device_map="auto", dtype="bfloat16", low_cpu_mem_usage=True, trust_remote_code=True
)

inputs = tokenizer("Explain why long-context evaluation is difficult.", return_tensors="pt").to(model.device)
inputs.pop("token_type_ids", None)
outputs = model.generate(**inputs, max_new_tokens=32768, temperature=1.0, top_p=0.95, do_sample=True)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Training Overview

The table below lists the training stages in order and the purpose of each stage.

Training steps are counted within each stage or phase. Token budgets cover only the additional training in that stage or phase. For example, the 50B tokens listed for SFT Phase 2 are additional to the 219B tokens in Phase 1, bringing the cumulative budget to 269B tokens by the end of Phase 2. Here, B and T denote billion and trillion tokens, respectively.

Each stage or phase continues from the final checkpoint of the preceding stage or phase.

Some stages, such as SFT, have multiple phases with slight changes to the data mix while retaining the same overall purpose. During RL, training branches into multiple expert models, which are then merged, as described below.

| Training stage | Training steps | Training tokens | Sequence length | Purpose |
| --- | --- | --- | --- | --- |
| Pretraining | 1100000 | 22.9T | 8K | Pretraining. |
| Midtraining — Stage 1 | 55000 | 1.1T | 32K | Context extension. |
| Midtraining — Stage 2 | 25000 | 498B | 128K | Context extension. |
| Midtraining — Stage 3 | 5500 | 110B | 512K | Context extension. |
| Midtraining — Stage 4 | 10000 | 199B | 512K | Continued context extension from Stage 3, with the data mix shifted toward agentic and reasoning SFT data. |
| RL — Math expert | 2549 | 28.9B | 64K | Math RL from Midtraining Stage 4; common ancestor of the Code and STEM-Code experts. |
| RL — Code expert | 949 | 15.5B | 64K | Code RL from the Math expert. |
| RL — STEM-Code expert | 451 | 1.3B | 64K | STEM and code RL from the Math expert. |
| RL — Merge | — | — | — | ISO merge on self-attention, RAM on the remaining weights; inputs: Midtraining Stage 4 base + Math, Code, STEM-Code experts. |
| SFT — Phase 1 | 10000 | 199B | 512K | SFT for better domain coverage, starting from the merged RL checkpoint. |
| SFT — Phase 2 | 2500 | 50B | 512K | SFT on a high-quality subset of the data used in Phase 1, with learning rate decay. |

## Release Artifacts

The tables below list the release artifacts for **K2-Horizon-3.7B**, their availability, and the expected release dates for remaining items.

**Last updated:** 2026-09-11

**Status:**

- **Available** — fully released for the scope listed;
- **Partial** — some items are available, with remaining items listed in the notes;
- **In Progress** — being prepared for release but not yet available.

### Artifact Index

| Artifact | Link | Status | Remaining items / expected availability |
| --- | --- | --- | --- |
| Model card | [Hugging Face](https://huggingface.co/IFM/K2-Horizon-3.7B) | Available | N/A |
| Training logs | [W&B](https://wandb.ai/llm360/K2-Horizon-3.7B) | Available | N/A |
| Blog post | [Blog post](https://ifm.ai/blog/k2/) | Available | N/A |
| Checkpoints | [Checkpoint inventory](#checkpoint-inventory) | Available | N/A |
| Technical report | Not yet available | In Progress | End of September 2026 |
| Code repository | [GitHub](https://github.com/ifm-ai/xllm) | In Progress | End of September 2026 |

### Checkpoint Inventory

**Model repository:** [IFM/K2-Horizon-3.7B](https://huggingface.co/IFM/K2-Horizon-3.7B)

Branch names below refer to this repository. Patterns containing `*` group branches by training stage or phase. The `*` is a placeholder for a training-step number, not a literal branch name. Intermediate checkpoint groups exclude the final checkpoint listed separately; a pattern does not imply that a checkpoint is available at every step.

For example, `sft_1_10000` is the checkpoint saved at training step 11,000 within SFT Phase 1, and is the final checkpoint of that phase. The numeric suffix is the step within the named stage or phase, not the cumulative step across all training. Thus, `sft_2_2500` refers to step 2,500 within SFT Phase 2.

For a partially released group, the available checkpoints and the remaining checkpoints are listed in the notes.

| Checkpoint | Branch / repository | Status | Remaining items / expected availability |
| --- | --- | --- | --- |
| Pretrain Intermediate Checkpoints | `pretrain_*` | Available | N/A |
| Pretrain Final Checkpoint | `pretrain_1100000` | Available | N/A |
| Midtrain Stage 1 Intermediate Checkpoints | `mid_1_*` | Available | N/A |
| Midtrain Stage 1 Final Checkpoint | `mid_1_55000` | Available | N/A |
| Midtrain Stage 2 Intermediate Checkpoints | `mid_2_*` | Available | N/A |
| Midtrain Stage 2 Final Checkpoint | `mid_2_25000` | Available | N/A |
| Midtrain Stage 3 Intermediate Checkpoints | `mid_3_*` | Available | N/A |
| Midtrain Stage 3 Final Checkpoint | `mid_3_5500` | Available | N/A |
| Midtrain Stage 4 Intermediate Checkpoints | `mid_4_*` | Available | N/A |
| Midtrain Stage 4 Final Checkpoint | `mid_4_10000` | Available | N/A |
| RL Math Expert Checkpoint | `rl_math` | Available | N/A |
| RL Code Expert Checkpoint | `rl_code` | Available | N/A |
| RL Stem Code Expert Checkpoint | `rl_stemcode` | Available | N/A |
| RL Merged Final Checkpoint | `rl_merged` | Available | N/A |
| SFT Phase 1 Intermediate Checkpoints | `sft_1_*` | Available | N/A |
| SFT Phase 1 Final Checkpoint | `sft_1_10000` | Available | N/A |
| SFT Phase 2 Intermediate Checkpoints | `sft_2_*` | Available | N/A |
| SFT Phase 2 Final Checkpoint | `sft_2_2500` | Available | N/A |

## Best Practices

1. **Reasoning effort: always `high`.** All reported results use high reasoning effort. Pass `{"chat_template_kwargs": {"reasoning_effort": "high"}}` on every request; `medium` and `low` trade accuracy for speed and are not recommended for evaluation.
2. **Sampling parameters.** `temperature=1.0`, `top_p=0.95`.
3. **Output length.** Allow at least 32,768 output tokens so reasoning is never cut off. Truncated reasoning is a failed response, not a shorter one.
4. **Serving.** Use the validated SGLang recipe above: BF16, TP=1, FlashAttention-3. Full recipes for every K2-Horizon size, with measured H200 latency and throughput, are in the [SGLang cookbook](https://docs.sglang.io/cookbook/autoregressive/IFM/K2-Horizon).
5. **Parsers.** Enable the `k2_horizon` reasoning parser for chat, and add the `k2_horizon` tool-call parser for agent use. Leave both off for plain completion-style generation.
6. **Revisions.** Pin a revision tag when reproducibility matters. `main` is the default checkpoint; `base_final` and the `mid_*_final` tags identify training stages.

## Citation

```bibtex
@misc{k2horizon2026,
  title  = {Introducing K2 Horizon: Frontier Performance, Radically Open},
  author = {{IFM Team}},
  year   = {2026},
  url    = {https://ifm.ai/blog/k2/},
}
```

