---
pipeline_tag: text-generation
library_name: transformers
model_name: K2-Horizon-MoVA-36B-A4B
language:
- en
license: apache-2.0
datasets:
- IFM/K2-Horizon-Pretrain-Data
- IFM/K2-Horizon-Midtrain-Data
tags:
- k2-horizon
- 36b
- mova
- moe
- open-weights
- ifm
base_model:
- IFM/K2-Horizon-MoVA-36B-A4B
---

# K2-Horizon-MoVA-36B-A4B-GGUF

> [!NOTE]
> This repository contains GGUF versions of the [IFM/K2-Horizon-MoVA-36B-A4B](https://huggingface.co/IFM/K2-Horizon-MoVA-36B-A4B) for use with `llama.cpp`.
>
> Multiple precision and quantization variants are available, including `BF16`, `Q8_0`, `Q6_K`, `Q5_K_M`, `Q5_0`, and `Q4_K_M`. All GGUF files include tokenizer metadata and a llama.cpp-compatible chat template.

> [!WARNING] 
> **💡 Important Deployment Notes:** These models require a version of `llama.cpp` containing K2 Horizon architecture support. PR to llama.cpp is in progress. MBZUAI-IFM fork of llama.cpp is in https://github.com/MBZUAI-IFM/llama.cpp/tree/model/K2Horizon



K2-Horizon-MoVA-36B-A4B is the sparse member of the K2-Horizon family: a Mixture-of-Experts model with Mixture-of-Values attention (MoVA) that stores 36B parameters and runs 4B per token. We have released the final checkpoint; intermediate checkpoints, along with the data and the training code, will be released.

<p align="center">
  <img src="assets/k2-horizon-mova-36b-a4b-benchmarks.png" alt="K2-Horizon-MoVA-36B-A4B benchmark results against open MoE, dense, and closed models" width="100%">
</p>

## K2-Horizon-MoVA-36B-A4B Highlights

- **Frontier-class results at 4B active parameters.** On agentic and reasoning benchmarks it outscores open weight dense (approximately 30B model size) and MoE models up to 15× its size; and also performs competitively against closed frontier models (see [Benchmark Results](#benchmark-results)).
- **512K context.** Native 524,288-token context from the midtraining stages onward.
- **Intermediate checkpoints.** Intermediate checkpoints will be released so capability changes can be studied across training rather than at a single checkpoint.
- **Fully open.** Training data/recipe and the training code will be made public.

## Benchmark Results

<!-- TABLE:START -->
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;margin:0 auto;padding:8px 0 16px;overflow-x:auto"><table style="display:table;width:100%;table-layout:fixed;border-collapse:collapse;font-size:12px;margin:0"><thead><tr><th style="width:22%;border-bottom:none"></th><th colspan="1" style="padding:6px 4px 2px;text-align:center;font-size:11px;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;opacity:0.65;border-bottom:1px solid rgba(128,128,128,0.25)"></th><th colspan="6" style="padding:6px 4px 2px;text-align:center;font-size:11px;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;opacity:0.65;border-bottom:1px solid rgba(128,128,128,0.25)">Open-weight models</th></tr><tr><th style="padding:10px 6px;text-align:left;border-bottom:2px solid #2450D6"></th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:11.14%;overflow-wrap:anywhere;background:rgba(36,80,214,0.08);">K2-Horizon-MoVA-36B-A4B</th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:11.14%;overflow-wrap:anywhere;">Nemotron 3 Ultra</th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:11.14%;overflow-wrap:anywhere;">Nemotron 3 Super</th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:11.14%;overflow-wrap:anywhere;">G9v3-39A5B</th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:11.14%;overflow-wrap:anywhere;">Qwen3.6-35B-A3B</th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:11.14%;overflow-wrap:anywhere;">Muse Glimmer-30B</th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:11.14%;overflow-wrap:anywhere;">Gemma 4 31B-it</th></tr></thead><tbody><tr><td style="padding:7px 4px 7px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;font-weight:600"># Params</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">36B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">550B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">120B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">39B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">35B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">30B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">31B</td></tr><tr><td style="padding:7px 4px 7px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;font-weight:600"># Activated params</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">4B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">55B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">12B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">5B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">3B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">30B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">31B</td></tr><tr><td style="padding:7px 4px 7px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;font-weight:600">Architecture</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">MoE</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">MoE</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">MoE</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">MoE</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">MoE</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">Dense</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">Dense</td></tr><tr><td colspan="8" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Agents</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">tau3-Banking</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Agentic tool use</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>26.8</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">14.2</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">10.3</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">22.1</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">9.3</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">23.5</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">14.8</td></tr><tr><td colspan="8" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Coding</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">Terminal-Bench 2.1</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Agentic terminal use</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>58.6</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">53.9</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">38.6</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">32.6</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">44.9</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">51.7</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">43.4</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">SciCode</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Scientific coding</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">38.9</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">39.9</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">36.0</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">34.0</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">35.8</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>43.6</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">43.4</td></tr><tr><td colspan="8" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Scientific Reasoning</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">Humanity's Last Exam (without tools)</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Expert-level reasoning</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">25.2</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>28.4</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">20.8</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">17.5</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">22.2</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">22.0</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">23.6</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">GPQA Diamond</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Graduate-level science QA</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">80.8</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>86.7</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">80.0</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">80.5</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">84.1</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">83.5</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">85.7</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">CritPt</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Frontier physics reasoning</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">2.1</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>3.1</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>3.1</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">0.3</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">0.3</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">2.6</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">1.4</td></tr><tr><td colspan="8" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">General</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">AA-LCR</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Long-context reasoning</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">66.3</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">71.0</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">60.3</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">62.0</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">66.7</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>80.0</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">68.3</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">AA-Omniscience Accuracy</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Factual accuracy</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">18.8</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">22.6</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">24.3</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">14.9</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">18.8</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>27.0</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">20.0</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">AA-Omniscience Non-Hallucination</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Non-hallucination rate</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">69.2</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">70.3</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">13.0</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>87.0</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">49.5</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">18.1</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">15.0</td></tr></tbody></table></div>
<!-- TABLE:END -->

<p style="font-size:1.25em;line-height:1.6">Scores in %. Bold marks the best score in each row. Sections follow the <a href="https://artificialanalysis.ai/methodology/intelligence-benchmarking">Artificial Analysis Intelligence Index</a> categories. Baseline scores are from Artificial Analysis; Muse Glimmer-30B at high reasoning effort, all other open models in their reasoning mode.</p>

## GGUF BF16 vs. Quantized
<!-- TABLE:START -->
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;margin:0 auto;padding:8px 0 16px;overflow-x:auto">
<table style="display:table;width:100%;border-collapse:collapse;font-size:12px;margin:0;table-layout:fixed;">

<thead>
<tr>
  <th style="width:16%;padding:10px 8px;text-align:left;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;">
    K2-Horizon-MoVA-36B-A4B
  </th>
  <th style="padding:10px 8px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;">IFEval (Prompt)</th>
  <th style="padding:10px 8px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;">GSM8K</th>
  <th style="padding:10px 8px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;">MBPP</th>
  <th style="padding:10px 8px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;">MMLU-Pro</th>
  <th style="padding:10px 8px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;">GPQA-Diamond</th>
  <th style="padding:10px 8px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;">BBH (3-shot)</th>
  <th style="padding:10px 8px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;">AIME 26 (avg @ 4)</th>
  <th style="padding:10px 8px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;">Average</th>
</tr>
</thead>

<tbody>

<!-- BF16 highlighted -->
<tr style="background:rgba(36,80,214,0.12);">
  <td style="padding:7px 8px;border-bottom:1px solid rgba(36,80,214,0.25);font-weight:700;color:#2450D6;">
    GGUF-BF16
  </td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">90.7</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">95.1</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">94.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">81.2</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">80.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">64.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">90.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">85.3</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q4_K_M</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">87.0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">95.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">94.2</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">80.5</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">81.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">65.1</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">95.0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">85.6</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q5_0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">89.0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">95.7</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">94.4</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">80.4</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">84.5</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">64.0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">94.1</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">86.0</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q5_K_M</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">90.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">96.2</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">93.2</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">80.4</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">80.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">64.7</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">94.1</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">85.6</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q6_K</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">91.5</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">95.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">92.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">80.5</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">78.7</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">63.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">94.1</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">85.3</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q8_0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">87.9</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">95.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">93.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">81.0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">83.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">63.7</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">94.1</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">85.6</td>
</tr>

</tbody>
</table>
</div>
<!-- TABLE:END -->
The evaluation context length is set to 65,536 tokens. Unless otherwise specified, all tasks are evaluated in a 0-shot setting.
The GGUF models have currently been evaluated only on non-agent tasks. Results for agent tasks will be released later.


## Quickstart

### Serving

vLLM, recipe at [recipes.vllm.ai/IFM](https://recipes.vllm.ai/IFM):

```shell
vllm serve IFM/K2-Horizon-MoVA-36B-A4B \
  --revision main \
  --tensor-parallel-size 2 \
  --enable-expert-parallel \
  --trust-remote-code \
  --dtype bfloat16 \
  --max-model-len 131072 \
  --reasoning-parser k2_horizon \
  --tool-call-parser k2_horizon \
  --enable-auto-tool-choice
```

SGLang recipe validated on 2× H200 in the [SGLang K2 Horizon cookbook](https://docs.sglang.io/cookbook/autoregressive/IFM/K2-Horizon):

```shell
python3 -m sglang.launch_server \
  --model-path IFM/K2-Horizon-MoVA-36B-A4B \
  --revision main \
  --tp 2 \
  --ep 2 \
  --dtype bfloat16 \
  --attention-backend fa3 \
  --json-model-override-args '{"xllm_source_router_gemm_partitions":2}' \
  --reasoning-parser k2_horizon \
  --tool-call-parser k2_horizon \
  --host 0.0.0.0 --port 30000
```

### API Usage

> [!Tip]
> Recommended settings: `reasoning_effort="high"`, `temperature=1.0`, `top_p=0.95`.
> Reasoning depth is selected per request through `chat_template_kwargs`. Thinking is returned in `reasoning_content` and the answer in `content`.

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:30000/v1", api_key="EMPTY")
response = client.chat.completions.create(
    model="IFM/K2-Horizon-MoVA-36B-A4B",
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

model_id = "IFM/K2-Horizon-MoVA-36B-A4B"
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

1. **Reasoning effort: always `high`.** All reported results use high reasoning effort. Pass `{"chat_template_kwargs": {"reasoning_effort": "high"}}` on every request.
2. **Sampling parameters.** `temperature=1.0`, `top_p=0.95`.
3. **Serving.** Use the validated SGLang recipe above: BF16, TP=2, FlashAttention-3, and the `xllm_source_router_gemm_partitions` override, which preserves the checkpoint's router numerics. Full recipes for every K2-Horizon size, with measured H200 latency and throughput, are in the [SGLang cookbook](https://docs.sglang.io/cookbook/autoregressive/IFM/K2-Horizon) and the [vLLM recipe](https://recipes.vllm.ai/IFM).
4. **Parsers.** Enable the `k2_horizon` reasoning parser for chat, and add the `k2_horizon` tool-call parser for agent use. Leave both off for plain completion-style generation.

## Citation

```bibtex
@misc{k2horizon2026,
  title  = {Introducing K2 Horizon: Frontier Performance, Radically Open},
  author = {{IFM Team}},
  year   = {2026},
  url    = {https://ifm.ai/blog/k2/},
}
```