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
base_model:
- IFM/K2-Horizon-3.7B
---

# K2-Horizon-3.7B-GGUF

> [!NOTE]
> This repository contains GGUF versions of the [IFM/K2-Horizon-3.7B](https://huggingface.co/IFM/K2-Horizon-3.7B) for use with `llama.cpp`.
>
> The model tensors are stored in their original BF16 precision. The GGUF files include the tokenizer metadata and a `llama.cpp`-compatible chat template.
>
> **Compatibility:** These models require a version of `llama.cpp` containing K2 Horizon architecture support. PR to llama.cpp is in progress. MBZUAI-IFM fork of llama.cpp is in https://github.com/MBZUAI-IFM/llama.cpp/tree/model/K2Horizon


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
  --max-model-len 131072 \
  --tensor-parallel-size 1 \
  --reasoning-parser k2_horizon \
  --enable-auto-tool-choice \
  --tool-call-parser k2_horizon
```

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
    extra_body={"chat_template_kwargs": {"reasoning_effort": "high", "tool_call_format": "xml"}},
)
message = response.choices[0].message
print("Reasoning:", getattr(message, "reasoning_content", None))
print("Answer:", message.content)
```

Our model supports multiple tool calls formats, which can be changed with `chat_template_kwargs`. The supported values are `json`, `xml`, and `xml_typed` . The default is `xml`. Keep `--tool-call-parser k2_horizon` enabled to parse the selected format.

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