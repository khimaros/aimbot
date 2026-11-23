---
pipeline_tag: text-generation
library_name: transformers
model_name: K2-Horizon-32B-Stage1
language:
  - en
license: apache-2.0
datasets:
  - IFM/K2-Horizon-Pretrain-Data
  - IFM/K2-Horizon-Midtrain-Data
tags:
  - k2-horizon
  - 32b
  - dense
  - open-weights
  - ifm
---

# K2-Horizon-32B-Stage1-GGUF

> [!NOTE]
> This repository contains GGUF versions of the [IFM/K2-Horizon-32B](https://huggingface.co/IFM/K2-Horizon-32B) for use with `llama.cpp`.
>
> Multiple precision and quantization variants are available, including `BF16`, `Q8_0`, `Q6_K`, `Q5_K_M`, `Q5_0`, and `Q4_K_M`. All GGUF files include tokenizer metadata and a llama.cpp-compatible chat template.

> [!WARNING] 
> **💡 Important Deployment Notes:** These models require a version of `llama.cpp` containing K2 Horizon architecture support. Mainline support merged in release [b11454](https://github.com/ggml-org/llama.cpp/releases?page=5#release-b11454).


K2-Horizon-32B-Stage1 is the large dense member of the K2-Horizon family: a 32B decoder-only model with a 512K context window. <span style="color:#d92d20;font-weight:600">Note: final checkpoint to be released.</span>

<p align="center">
  <img src="assets/k2-horizon-32b-benchmarks.png" alt="K2-Horizon-32B-Stage1 benchmark results against open MoE, dense, and closed models" width="100%">
</p>

## K2-Horizon-32B-Stage1 Highlights

- **Strong dense baseline.** A 32B dense model evaluated on the same agentic, coding, and reasoning benchmarks as the rest of the family (see [Benchmark Results](#benchmark-results)). Results are for stage 1 of the final model training; results for stage 2 will be out soon.
- **512K context.** Native 524,288-token context from the midtraining stages onward.
- **Intermediate checkpoints.** Intermediate checkpoints will be released so capability changes can be studied across training rather than at a single checkpoint.
- **Fully open.** Training data/recipe and the training code will be made public.

## Benchmark Results

<!-- TABLE:START -->
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;margin:0 auto;padding:8px 0 16px;overflow-x:auto"><table style="display:table;width:100%;table-layout:fixed;border-collapse:collapse;font-size:12px;margin:0"><thead><tr><th style="width:30%;border-bottom:none"></th><th colspan="1" style="padding:6px 4px 2px;text-align:center;font-size:11px;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;opacity:0.65;border-bottom:1px solid rgba(128,128,128,0.25)"></th><th colspan="3" style="padding:6px 4px 2px;text-align:center;font-size:11px;font-weight:600;letter-spacing:0.04em;text-transform:uppercase;opacity:0.65;border-bottom:1px solid rgba(128,128,128,0.25)">Open-weight dense models</th></tr><tr><th style="padding:10px 6px;text-align:left;border-bottom:2px solid #2450D6"></th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:17.50%;overflow-wrap:anywhere;background:rgba(36,80,214,0.08);">K2-Horizon-32B-Stage1</th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:17.50%;overflow-wrap:anywhere;">Qwen3.8-27B</th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:17.50%;overflow-wrap:anywhere;">Muse Glimmer-30B</th><th style="padding:10px 3px;text-align:center;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;line-height:1.2;width:17.50%;overflow-wrap:anywhere;">IBM Granite 4.2 30B</th></tr></thead><tbody><tr><td style="padding:7px 4px 7px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;font-weight:600"># Params</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">32B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">27B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">30B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">30B</td></tr><tr><td style="padding:7px 4px 7px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;font-weight:600"># Activated params</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">32B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">27B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">30B</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">30B</td></tr><tr><td style="padding:7px 4px 7px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;font-weight:600">Architecture</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">Dense</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">Dense</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">Dense</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">Dense</td></tr><tr><td colspan="5" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Agents</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">tau3-Banking</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Agentic tool use</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">22.5</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>48.0</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">23.5</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">14.4</td></tr><tr><td colspan="5" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Coding</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">Terminal-Bench 2.1</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Agentic terminal use</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">36.6</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>79.8</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">51.7</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">26.6</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">SciCode</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Scientific coding</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">30.2</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>44.7</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">43.6</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">36.6</td></tr><tr><td colspan="5" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">Scientific Reasoning</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">Humanity's Last Exam (without tools)</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Expert-level reasoning</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">22.8</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>33.9</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">22.0</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">11.2</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">GPQA Diamond</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Graduate-level science QA</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">82.3</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>90.5</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">83.5</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">64.4</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">CritPt</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Frontier physics reasoning</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">1.4</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>5.4</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">2.6</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">0.3</td></tr><tr><td colspan="5" style="padding:6px 10px;font-weight:600;font-size:12.5px;color:#2450D6;border-bottom:1px solid rgba(36,80,214,0.25);background:rgba(36,80,214,0.12)">General</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">AA-LCR</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Long-context reasoning</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">65.3</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">77.3</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>80.0</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">46.7</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">AA-Omniscience Accuracy</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Factual accuracy</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">16.8</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">15.6</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>27.0</strong></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">10.1</td></tr><tr><td style="padding:6px 4px 6px 10px;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle"><div style="font-size:12.5px;font-weight:600;line-height:1.2;color:inherit">AA-Omniscience Non-Hallucination</div><div style="margin-top:2px;font-size:10px;opacity:0.65">Non-hallucination rate</div></td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;background:rgba(36,80,214,0.08);">58.3</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">69.7</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;">18.1</td><td style="padding:6px 2px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);vertical-align:middle;font-size:12.5px;line-height:1.2;"><strong>74.4</strong></td></tr></tbody></table></div>
<!-- TABLE:END -->

<p style="font-size:1.25em;line-height:1.6">Scores in %. Bold marks the best score in each row. Sections follow the <a href="https://artificialanalysis.ai/methodology/intelligence-benchmarking">Artificial Analysis Intelligence Index</a> categories. Baseline scores are from Artificial Analysis; Muse Glimmer-30B at high reasoning effort, other open models in their reasoning mode.</p>

## GGUF BF16 vs. Quantized
<!-- TABLE:START -->
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;margin:0 auto;padding:8px 0 16px;overflow-x:auto">
<table style="display:table;width:100%;border-collapse:collapse;font-size:12px;margin:0;table-layout:fixed;">

<thead>
<tr>
  <th style="width:16%;padding:10px 8px;text-align:left;font-weight:600;border-bottom:2px solid #2450D6;color:#2450D6;font-size:12.5px;">
    K2-Horizon-32B-Stage1
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
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">86.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">95.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">94.2</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">81.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">77.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">63.2</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">94.1</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(36,80,214,0.25);">84.7</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q4_K_M</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">87.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">95.1</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">93.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">81.4</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">80.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">64.7</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">95.0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">85.4</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q5_0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">84.4</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">96.4</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">94.0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">81.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">81.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">69.1</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">92.5</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">85.6</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q5_K_M</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">87.4</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">95.3</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">94.0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">81.7</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">77.2</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">62.5</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">95.0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">84.7</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q6_K</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">87.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">95.9</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">94.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">81.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">82.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">62.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">92.5</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">85.5</td>
</tr>

<tr>
  <td style="padding:7px 8px;border-bottom:1px solid rgba(128,128,128,0.15);font-weight:600;">GGUF-Q8_0</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">87.4</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">95.9</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">93.4</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">81.6</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">80.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">63.5</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">95.8</td>
  <td style="padding:7px 8px;text-align:center;border-bottom:1px solid rgba(128,128,128,0.15);">85.5</td>
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
vllm serve IFM/K2-Horizon-32B \
  --revision main \
  --model-impl vllm \
  --tensor-parallel-size 2 \
  --trust-remote-code \
  --dtype bfloat16 \
  --max-model-len 131072 \
  --reasoning-parser k2_horizon \
  --enable-auto-tool-choice \
  --tool-call-parser k2_horizon
```

SGLang recipe validated on 2× H200 in the [SGLang K2 Horizon cookbook](https://docs.sglang.io/cookbook/autoregressive/IFM/K2-Horizon):

```shell
python3 -m sglang.launch_server \
  --model-path IFM/K2-Horizon-32B \
  --revision main \
  --tp 2 \
  --dtype bfloat16 \
  --attention-backend fa3 \
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
    model="IFM/K2-Horizon-32B",
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

model_id = "IFM/K2-Horizon-32B"
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
3. **Serving.** Use the validated SGLang recipe above: BF16, TP=2, FlashAttention-3. Full recipes for every K2-Horizon size, with measured H200 latency and throughput, are in the [SGLang cookbook](https://docs.sglang.io/cookbook/autoregressive/IFM/K2-Horizon) and the [vLLM recipe](https://recipes.vllm.ai/IFM).
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