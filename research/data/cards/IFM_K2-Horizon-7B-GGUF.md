---
pipeline_tag: text-generation
library_name: transformers
model_name: K2-Horizon-7B
language:
- en
license: apache-2.0
datasets:
- IFM/K2-Horizon-Pretrain-Data
- IFM/K2-Horizon-Midtrain-Data
tags:
- k2-horizon
- 7b
- dense
- open-weights
- ifm
base_model:
- IFM/K2-Horizon-7B
---

# K2-Horizon-7B-GGUF

> [!NOTE]
> This repository contains GGUF versions of the [IFM/K2-Horizon-7B](https://huggingface.co/IFM/K2-Horizon-7B) for use with `llama.cpp`.
>
> Multiple precision and quantization variants are available, including `BF16`, `Q8_0`, `Q6_K`, `Q5_K_M`, `Q5_0`, and `Q4_K_M`. All GGUF files include tokenizer metadata and a llama.cpp-compatible chat template.

> [!WARNING] 
> **💡 Important Deployment Notes:** These models require a version of `llama.cpp` containing K2 Horizon architecture support. PR to llama.cpp is in progress. MBZUAI-IFM fork of llama.cpp is in https://github.com/MBZUAI-IFM/llama.cpp/tree/model/K2Horizon


K2-Horizon-7B is the medium dense member of the K2-Horizon family: a 7B-core decoder-only model with a 512K context window.

<p align="center">
  <img src="assets/k2-horizon-7b-benchmarks.png" alt="K2-Horizon-7B benchmark results" width="100%">
</p>

## K2-Horizon-7B Highlights

- **Strong dense baseline.** A 7B-class dense model evaluated across agentic, coding, long-context, and reasoning benchmarks.
- **512K context.** Native 524,288-token context from the midtraining stages onward.
- **Intermediate checkpoints.** Intermediate checkpoints are released so capability changes can be studied across training rather than at a single checkpoint.
- **Fully open.** Training data and recipe, training code, and evaluation resources are public.

## Benchmark Results

The chart at the top of this card shows K2-Horizon-7B against selected reference models. The table below lists every comparison model used in the figure.

### Full Results

<!-- TABLE:START -->
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;margin:0 auto;padding:8px 0 16px;overflow-x:auto"><table style="display:table;width:100%;table-layout:fixed;border-collapse:collapse;font-size:12px;margin:0"><thead><tr><th style="width:28%;border-bottom:none"></th><th style="border-bottom:1px solid rgba(128,128,128,0.25)"></th><th colspan="3" style="padding:6px 4px 2px;text-align:center;font-size:11px;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;opacity:0.65;border-bottom:1px solid rgba(128,128,128,0.25)">Reference models · weak to strong</th></tr><tr><th style="padding:10px 6px;text-align:left;border-bottom:2px solid #2450D6">Benchmark</th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;background:rgba(36,80,214,0.08)">K2-Horizon-7B</th><th style="padding:10px 3px;text-align:center;border-bottom:2px solid #2450D6">Reference 1</th><th style="padding:10px 3px;text-align:center;border-bottom:2px solid #2450D6">Reference 2</th><th style="padding:10px 3px;text-align:center;border-bottom:2px solid #2450D6">Reference 3</th></tr></thead><tbody><tr><td colspan="5" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Math</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">HMMT Feb 2026</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Competition mathematics</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>73.3</strong></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Gemma 4-12B</div><div style="margin-top:3px;font-weight:600">63.1</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Qwen3.5-9B</div><div style="margin-top:3px;font-weight:600">65.7</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Granite 4.2-8B</div><div style="margin-top:3px;font-weight:600">66.5</div></td></tr><tr><td colspan="5" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Coding</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">SWE-bench Verified</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Software engineering</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>70.6</strong></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Gemma 4-12B</div><div style="margin-top:3px;font-weight:600">30.6</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Granite 4.2-8B</div><div style="margin-top:3px;font-weight:600">47.7</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Qwen3.5-9B</div><div style="margin-top:3px;font-weight:600">50.8</div></td></tr><tr><td colspan="5" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Scientific Reasoning</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">HLE</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Expert-level reasoning</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>18.6</strong></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Granite 4.2-8B</div><div style="margin-top:3px;font-weight:600">9.7</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Qwen3.5-9B</div><div style="margin-top:3px;font-weight:600">14.9</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Gemma 4-12B</div><div style="margin-top:3px;font-weight:600">15.7</div></td></tr><tr><td colspan="5" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Coding</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">SciCode</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Scientific coding</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>31.6</strong></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Qwen3.5-9B</div><div style="margin-top:3px;font-weight:600">27.5</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Mistral Small 4</div><div style="margin-top:3px;font-weight:600">28.0</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Granite 4.2-8B</div><div style="margin-top:3px;font-weight:600">30.4</div></td></tr><tr><td colspan="5" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">General</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">LCR</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Long-context reasoning</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>68.0</strong></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Granite 4.2-8B</div><div style="margin-top:3px;font-weight:600">43.3</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Gemma 4-12B</div><div style="margin-top:3px;font-weight:600">61.7</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Qwen3.5-9B</div><div style="margin-top:3px;font-weight:600">65.3</div></td></tr><tr><td colspan="5" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Coding</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">Terminal-Bench 2.1</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Agentic terminal use</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>39.1</strong></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Granite 4.2-8B</div><div style="margin-top:3px;font-weight:600">18.4</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Gemma 4-12B</div><div style="margin-top:3px;font-weight:600">27.3</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Qwen3.5-9B</div><div style="margin-top:3px;font-weight:600">29.2</div></td></tr><tr><td colspan="5" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Agents</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">tau3-Banking</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Agentic tool use</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>25.8</strong></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Qwen3.5-9B</div><div style="margin-top:3px;font-weight:600">7.0</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Granite 4.2-8B</div><div style="margin-top:3px;font-weight:600">7.6</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">Muse Glimmer-30B</div><div style="margin-top:3px;font-weight:600">24.0</div></td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2">BrowseComp</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Web browsing</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);"><strong>59.0</strong></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">DeepSeek V4 Flash-0423</div><div style="margin-top:3px;font-weight:600">53.5</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">GPT-5</div><div style="margin-top:3px;font-weight:600">54.9</div></td><td style="padding:6px 3px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><div style="font-size:10.5px;opacity:0.72;line-height:1.15">LongCat Flash Thinking-2601</div><div style="margin-top:3px;font-weight:600">56.6</div></td></tr></tbody></table></div>
<!-- TABLE:END -->

Scores in %. Bold marks the best score in each row. BrowseComp: our model uses the Discard-all@95k context-length protocol proposed in the DeepSeek-V3.2 technical report; comparison models may use different harnesses.

## GGUF BF16 vs. Quantized
<!-- TABLE:START -->
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;margin:0 auto;padding:8px 0 16px;overflow-x:auto">
<table style="display:table;width:100%;border-collapse:collapse;font-size:12px;margin:0;table-layout:fixed;">

<thead>
<tr>
  <th style="width:16%;padding:10px 8px;text-align:left;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;">
    K2-Horizon-7B
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
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">82.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">93.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">89.4</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">73.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">73.7</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">54.2</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">88.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">79.4</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q4_K_M</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">82.9</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">94.4</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">87.2</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">71.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">67.1</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">49.0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">89.1</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">77.3</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q5_0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">80.5</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">93.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">83.4</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">71.7</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">75.2</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">61.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">86.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">79.0</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q5_K_M</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">83.7</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">94.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">86.2</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">73.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">69.7</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">65.2</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">88.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">80.1</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q6_K</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">81.7</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">94.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">86.4</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">73.4</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">74.7</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">59.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">85.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">79.4</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q8_0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">84.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">95.0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">89.0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">74.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">69.7</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">54.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">90.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">79.7</td>
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
vllm serve IFM/K2-Horizon-7B \
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
  --model-path IFM/K2-Horizon-7B \
  --revision 69ada542b68fe13d767479db2ab9421baff88681 \
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
    model="IFM/K2-Horizon-7B",
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

model_id = "IFM/K2-Horizon-7B"
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