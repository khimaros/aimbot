---
license: other
license_name: tencent-hy-license
license_link: LICENSE
base_model:
- tencent/Hy4-flash
base_model_relation: quantized
library_name: gguf
pipeline_tag: image-text-to-text
language:
- en
- zh
tags:
- gguf
- llama-cpp
- quantized
- hy4-flash
- moe
- multimodal
---

<div align="center">

<img class="block dark:hidden mx-auto" src="https://raw.githubusercontent.com/XylolabsInc/tensix-bfp-gptq/main/assets/xylolabs-lockup.svg" alt="Xylolabs" width="256" height="40">
<img class="hidden dark:block mx-auto" src="https://raw.githubusercontent.com/XylolabsInc/tensix-bfp-gptq/main/assets/xylolabs-lockup-dark.svg" alt="Xylolabs" width="256" height="40">

<h1>Hy4 flash GGUF</h1>

[![Base model](https://img.shields.io/badge/base-tencent%2FHy4--flash-blue)](https://huggingface.co/tencent/Hy4-flash)
[![Formats](https://img.shields.io/badge/formats-Q8__0%20%2F%20Q6__K%20%2F%20Q5__K__M%20%2F%20Q4__K__M%20%2F%20Q4__K__S%20%2F%20IQ4__XS%20%2F%20Q3__K__M%20%2F%20IQ3__M%20%2F%20IQ3__XXS%20%2F%20Q2__K%20%2F%20IQ2__M-5B2C83)](#files)
[![License](https://img.shields.io/badge/license-Tencent%20Hy%20License-green)](https://huggingface.co/Xylolabs/Hy4-flash-GGUF/blob/main/LICENSE)
[![Code](https://img.shields.io/badge/code-llama.cpp%20PR%2032517-black)](https://github.com/ggml-org/llama.cpp/pull/32517)

`gguf` · `llama-cpp` · `quantized` · `hy4-flash` · `moe` · `multimodal`

</div>

[tencent/Hy4-flash](https://huggingface.co/tencent/Hy4-flash) (220B parameters, 12B active) as llama.cpp GGUF quants for CUDA, Metal or CPU, with the Engram tables in their own memory-mapped file. Made by Xylolabs.

- **What is in it:** Q8_0, Q6_K, Q5_K_M, Q4_K_M, Q4_K_S, IQ4_XS, Q3_K_M, IQ3_M, IQ3_XXS, Q2_K and IQ2_M, each as a two-shard gguf-split set (trunk plus the shared Engram shard, 63.36 GB, FP8 E4M3), the vision tower (bf16), the importance matrix and the conversion patch.
- **Accuracy:** Q4_K_M: mean KL to our Q8_0 reference 0.2415, same top-1 84.3%, no wrong or broken answer on our five-item check (Tencent's Q4_K_M, same build and text: KL 0.2908, 83.4%). Pick a file for your memory with "Which quant fits" below.
- **Role:** the llama.cpp release of the model. Tencent's own description of the model is reproduced further down, attributed.

## Files

Each quant is a two-shard `gguf-split` set: `Hy4-flash-<QUANT>-00001-of-00002.gguf` (trunk) and `-00002-of-00002.gguf` (Engram tables, 63.36 GB, FP8 E4M3). Shard 2 is the same file for every quant (sha256 `c3589e8789026f7de689a5bd2258daf018deddcbd903a443713051a6d84351a9`); llama.cpp finds it by name next to shard 1. `mmproj-Hy4-flash-BF16.gguf` (1.04 GB) is the vision tower, converted and untested. `Hy4-flash.imatrix.gguf` is the importance matrix.

| Quant | Shard 1 (trunk) | Trunk bpw | PPL | Mean KL vs Q8_0 | Same top-1 | Answers (5 items) | pp512 tok/s | tg128 tok/s | GPU memory (MiB) |
|---|---|---|---|---|---|---|---|---|---|
| Q8_0 | 165.50 GB | 8.51 | 31.70 | reference | reference | not run | not measured | not measured | two GPUs (does not fit one) |
| Q6_K | 129.89 GB | 6.68 | 30.69 | 0.1689 | 87.6% | 5/5 | 1270 | 72.7 | 124,679 |
| Q5_K_M | 113.37 GB | 5.83 | 31.58 | 0.1907 | 86.5% | 5/5 | 1516 | 72.8 | 108,921 |
| Q4_K_M | 97.81 GB | 5.03 | 32.56 | 0.2415 | 84.3% | 5/5 | 1502 | 75.7 | 94,089 |
| Q4_K_S | 92.19 GB | 4.74 | 33.38 | 0.2464 | 84.1% | 5/5 | 1490 | 72.7 | not measured |
| IQ4_XS | 86.94 GB | 4.47 | 30.27 | 0.2603 | 84.4% | 5/5 | 1690 | 72.0 | 83,721 |
| Q3_K_M | 78.58 GB | 4.04 | 27.41 | 0.3659 | 81.7% | 5/5 | 1644 | 70.0 | 75,747 |
| IQ3_M | 72.49 GB | 3.73 | 37.28 | 0.4485 | 78.4% | 5/5 | 1486 | 67.4 | 69,941 |
| IQ3_XXS | 64.89 GB | 3.34 | 31.47 | 0.4953 | 77.1% | 5/5 | 1608 | 68.6 | 62,687 |
| Q2_K | 61.79 GB | 3.18 | 29.48 | 0.6808 | 73.6% | 5/5 | 1539 | 72.4 | 59,735 |
| IQ2_M | 56.26 GB | 2.89 | 33.49 | 0.6869 | 73.0% | 5/5 | 1566 | 69.6 | 54,461 |

Q8_0 is the reference of the KL and top-1 columns; it does not fit one GPU, so its speed is not measured. Mean KL is over 24×512 tokens of wikitext-2 against Q8_0; the runtime is deterministic. Speed is `llama-bench` pp512 and tg128 at depth 0 on one NVIDIA H200 with both shards warm in the page cache. Answers: five short items (a capital, a product, a Python function, an English-to-Korean sentence, a time difference), greedy, 4,096-token cap.

**Source:** quantized from `tencent/Hy4-flash-FP8` (Tencent's FP8 release, upcast to BF16); KL is measured against our Q8_0 from that source. BF16-based files (from `tencent/Hy4-flash`) replace these as they pass; Q8_0, Q6_K and Q5_K_M first.

### Compared with Tencent's Q4_K_M

| Q4_K_M from | PPL (PR build) | PPL (Tencent's patched build) | Mean KL vs Q8_0 | Same top-1 |
|---|---|---|---|---|
| Xylolabs (this repository) | 32.56 | 31.88 | 0.2415 | 84.3% |
| AngelSlim (Tencent) | 31.92 | 30.84 | 0.2908 | 83.4% |

Same runtime and text; raw-text perplexity does not rank quants on this model, so judge by KL and top-1.

## Which quant fits

Budget the trunk + ~3 GB at 32K context + 8-10 GB for the system; shard 2 is memory-mapped.

| Machine | Memory | Pick | Notes |
|---|---|---|---|
| 128 GB | 128 GB (GPU or unified) | Q4_K_M (97.8 GB) or Q4_K_S (92.2 GB) | Q5_K_M (113.4 GB) fits with almost nothing else running; Q6_K (129.9 GB) does not fit. If the trunk will not load on a unified-memory machine, raise the GPU wired-memory limit (`sudo sysctl iogpu.wired_limit_mb=<MB>`). |
| 96 GB | 96 GB | Q3_K_M (78.6 GB) | IQ4_XS (86.9 GB) leaves too little for context. |
| 64 GB | 64 GB | none whole | Q2_K (61.8 GB) leaves no room for context. |
| 141 GB GPU | 141 GB | Q6_K or Q5_K_M | The numbers come from one GPU of this size. |

## Tensor recipe

| Tensor class | Format |
|---|---|
| Routed experts `ffn_gate_exps`, `ffn_up_exps`, `ffn_down_exps` (148.6B parameters) | the quant type of the file |
| Attention (MLA projections, gate, output), shared experts, latent projections, layer-0 dense MLP, token embedding, indexer projections, Engram key/value projections | Q8_0 |
| Router `ffn_gate_inp`, hyper-connection functions, indexer `proj` and compressor, small Engram weights, norms, biases | F32 |
| LM head `output.weight` | bf16 |
| Engram tables `per_layer_token_embd` (63.4B parameters) | FP8 E4M3 |

## How to run

llama.cpp support for `hy_v4_flash` is PR [#32517](https://github.com/ggml-org/llama.cpp/pull/32517), commit `0a054d0b0`. The pair also loads in Tencent's patched build (AngelSlim's `hy4-flash-spark.patch`, Metal `hy4-flash-mac-minimal.patch`, on commit `2cbca389f515df455412dafa07e2b1359cc72a6d`).

**CUDA**

```sh
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
git fetch origin pull/32517/head:hy4-flash && git checkout hy4-flash
cmake -B build -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release
cmake --build build -j --target llama-cli llama-server

./build/bin/llama-cli -m Hy4-flash-Q4_K_M-00001-of-00002.gguf \
  --override-tensor '^per_layer_token_embd\.weight$=CPU' --load-mode mmap --lazy-mode on \
  -ngl 99 --jinja -c 8192
```

**Metal**

```sh
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
git checkout 2cbca389f515df455412dafa07e2b1359cc72a6d
git apply /path/to/AngelSlim/patch/hy4-flash-mac-minimal.patch   # from Tencent's AngelSlim GGUF repository
cmake -B build -DCMAKE_BUILD_TYPE=Release                         # Metal is on by default
cmake --build build -j --target llama-cli llama-server

./build/bin/llama-cli -m Hy4-flash-Q4_K_M-00001-of-00002.gguf \
  --override-tensor '^per_layer_token_embd\.weight$=CPU' --load-mode mmap --lazy-mode on \
  -ngl 99 --jinja -c 8192
```

The three flags keep the Engram tables on the host, memory-mapped and paged in on demand. `llama-server` takes the same flags. The Metal route uses Tencent's patched build; we have run it on CUDA only.

## How these were made

1. `convert_hf_to_gguf.py` from the PR, with `hy4-flash-release-convert.patch` from this repository: trunk (bf16), Engram shard, `--mmproj`.
2. `llama-imatrix` on the Q8_0 trunk, 125 chunks of 512 tokens.
3. `llama-quantize --imatrix Hy4-flash.imatrix.gguf --output-tensor-type bf16 --tensor-type-file tensor_types_base.txt <bf16 trunk> <out> <QUANT>`.
4. `llama-gguf-split` into the two shards.

## License and notices

These files are derived from Tencent's Hy4-flash and are distributed under the Tencent Hy License, Version 1.0 (`LICENSE` in this repository, a copy of the license as released with the source model). **Modified by Xylolabs:** the weights were quantized and converted to GGUF (see "How these were made"; the conversion patch is included as `hy4-flash-release-convert.patch`). All of the source model's notices are retained: `NOTICE` names the source and copyright holder. The license's terms, including its additional terms for large Model-as-a-Service operators, apply to these files and to any use of them. This repository is not affiliated with or endorsed by Tencent.

## Tencent's original model description

The text below is reproduced from the README of [tencent/Hy4-flash](https://huggingface.co/tencent/Hy4-flash) (the model introduction, highlights, benchmarks, quickstart and deployment sections), copyright Tencent, under the Tencent Hy License (see above). It describes Tencent's original model, not these files, and its usage instructions (Transformers, vLLM, SGLang) are for Tencent's checkpoints; for the GGUF files use "How to run" above. Changes by Xylolabs: heading levels are one level deeper, and image and link paths point to Tencent's repository instead of copies; the wording is unchanged. Tencent's own README is the authoritative version.

### Model Introduction

**Hy4 flash** is our most cost-effective Hy model to date, featuring 220B total parameters (including 64B Engram parameters) with just 12B active parameters per token. It natively accepts text and image inputs, generates text, and supports a context window of up to 1M tokens.

Its 42-layer language backbone consists of one dense feed-forward layer and 41 MoE layers, with identity Hyper-Connections (iHC) supporting inter-layer information flow. A vision encoder (adapted from SigLIP2-So400m-Patch16-Res512) is connected to the backbone through an MLP projector. In addition to the backbone, a built-in 5-layer drafter, [DFly2](#dfly2-for-speculative-decoding) (0.85B parameters), reuses the target model's KV cache and sparse indices to support long-context speculative decoding at a low, constant cost.

Compared with Hy4, Hy4 Flash introduces three notable architectural changes:

1. **Hybrid attention.** Sparse attention (IndexPool) and sliding-window attention (SWA) are interleaved at a 1:3 ratio.
2. **LatentMoE.** Routed experts operate in a lower-dimensional latent space. Each token activates 16 of 512 routed experts, alongside one shared expert.
3. **N-gram embedding (Engram).** The backbone is augmented with learned bigram and trigram representations, retrieved via multi-head hash lookups.

| Property | Value |
| --- | --- |
| **Overview** | |
| Architecture | Mixture-of-Experts (MoE) |
| Total Parameters (excluding Engram, ViT, and DFly2) | 155.5B |
| Engram Parameters | 63.5B |
| ViT Parameters | 0.43B |
| DFly2 Parameters | 0.85B |
| Activated Parameters per Token | Text 11.3B + Vision 0.43B |
| Context Length | 1M (1,048,576 tokens) |
| **Language Backbone** | |
| Backbone Layers | 42 — 1 dense layer and 41 MoE layers |
| Hidden Size | 3,072 |
| Vocabulary Size | 120,832 |
| Residual Connections | iHC (identity Hyper-Connections) with 4 residual streams |
| **Attention — Hybrid Layout** | |
| Attention Architecture | Sparse attention + sliding-window attention (SWA) |
| Backbone Layer Pattern | 2 × Sparse → 10 × (3 × SWA → Sparse) |
| Attention Formulation | Multi-head Latent Attention (MLA) |
| Multimodal Position Encoding | Interleaved MRoPE |
| **Attention — Layers** | **Sparse / SWA** |
| Backbone Layers | 12 / 30 |
| Attention Heads | 32 / 64 |
| MLA q_lora_rank | 1,024 / 1,024 |
| MLA kv_lora_rank | 512 / 512 |
| QK Head Dimension (non-RoPE + RoPE) | 192 + 64 / 192 + 64 |
| Value Head Dimension | 256 / 256 |
| RoPE Base | 10,000,000 / 10,000 |
| Sparse Context Selection | Up to 2,048 tokens via group-level selection |
| SWA Context Window | 512-token causal window (511 preceding + current) |
| **Feed-Forward Networks** | |
| Dense FFN Intermediate Size | 13,824 |
| Routed Experts per MoE Layer | 512 |
| Shared Experts per MoE Layer | 1 |
| Activated Routed Experts per Token | 16 |
| MoE Latent Dimension | 1,536 |
| Expert Intermediate Size | 1,536 |
| **N-gram Embedding** | |
| N-gram Orders | Bigrams and trigrams |
| Backbone Layer Indices (starting from 0) | 1, 11, 21, 31 |
| Hash Heads per N-gram Order | 8 |
| Hash Vocabulary Size per Head | 10.3M |
| Embedding Dimension per N-gram Order | 768 (8 heads × 96 dimensions) |
| Embedding Table Parameters | 63.4B |
| **Vision Encoder** | |
| Vision Encoder Layers | 27 |
| Vision Encoder Hidden Size | 1,152 |
| Vision Encoder Intermediate Size | 4,304 |
| Vision Encoder Attention Heads | 16 |
| Vision Patch Size | 16 × 16 |
| Vision Position Embedding Size | 128 × 128 |
| Visual Feature Merging | 2 x 2 |

### Pretrained model capability

Bits-per-byte (BPB) on internal code & agent validation, lower is better:

<p align="center">
  <a href="https://huggingface.co/tencent/Hy4-flash/resolve/main/pretrained-model-bpb.png"><img src="https://huggingface.co/tencent/Hy4-flash/resolve/main/pretrained-model-bpb.png" alt="Bits-per-byte on internal code and agent validation versus active parameters; lower is better" width="75%"/></a>
</p>

Few-shot pretrain benchmark evaluation:

| Category | Benchmark | #Shots | Hy4 flash Base | Hy4 Base | Hy3 preview Base | DeepSeek-V4-flash-Base | DeepSeek-V4-Pro-Base |
| --- | --- | :---: | ---: | ---: | ---: | ---: | ---: |
| **Knowledge** | MMLU† | 5 | 88.7 | **91.6** | 87.5 | 89.7 | 91.1 |
|  | MMLU-Pro† | 5 | 71.1 | **73.9** | 65.8 | 68.6 | 73.4 |
|  | MMLU-Redux† | 5 | 87.6 | **90.6** | 87.0 | 88.8 | 90.2 |
|  | SuperGPQA† | 5 | 57.8 | **62.7** | 52.3 | 52.5 | 54.8 |
|  | C-Eval† | 5 | 92.0 | **95.0** | 90.1 | 91.9 | 93.4 |
|  | CMMLU† | 5 | 91.6 | **93.1** | 89.6 | 89.8 | 90.7 |
|  | SimpleQA | 5 | 37.5 | **57.2** | 26.4 | 31.3 | 52.1 |
|  | Chinese-SimpleQA† | 5 | 74.6 | **83.9** | 69.6 | 71.9 | 76.6 |
|  | AGIEval (English)† | 3 | 75.4 | **79.3** | 76.0 | 76.3 | 78.2 |
|  | AGIEval (Chinese)† | 3 | 90.6 | **91.2** | 87.8 | 88.5 | 89.8 |
| **Reasoning** | HellaSwag (3,000-item subset) | 10 | 85.2 | **87.1** | 85.7 | 85.1 | 86.8 |
|  | PIQA | 4 | 84.4 | **85.3** | 84.6 | 83.8 | 84.9 |
|  | ARC-Challenge | 0 | 95.0 | **97.3** | 96.0 | **97.3** | 97.0 |
|  | Social IQa | 0 | 80.1 | **82.7** | 80.5 | 72.5 | 73.1 |
|  | KOR-Bench | 3 | 54.7 | **57.6** | 54.6 | 53.4 | 55.4 |
|  | C³ | 0 | 77.3 | **82.4** | 75.9 | 74.1 | 78.3 |
| **Math** | U-MATH | 5 | 69.8 | **71.6** | 60.9 | 57.4 | 64.8 |
|  | OCW Courses | 5 | 64.0 | 66.7 | 62.6 | 63.3 | **68.2** |
| **Code** | MBPP-plus | 3 | 73.7 | 74.0 | 77.4 | 76.8 | **79.1** |
| **Multilingual** | Belebele (5-language subset)† | 5 | 93.8 | 95.0 | 94.2 | 94.4 | **95.2** |
|  | INCLUDE† | 5 | 82.8 | **88.1** | 84.3 | 84.0 | 84.3 |
| **Multimodal** | MMMU-Pro (Standard, 10 opts) | 4 | 52.0 | **59.6** | — | — | — |
|  | SimpleVQA | 4 | 48.5 | **54.5** | — | — | — |
|  | CVBench | 4 | 83.4 | **86.7** | — | — | — |
|  | RealWorldQA | 4 | 71.1 | **72.3** | — | — | — |
|  | TextVQA | 4 | 73.4 | **78.2** | — | — | — |
|  | CountBenchQA | 4 | 86.6 | **90.6** | — | — | — |

† Macro-averaged accuracy for the marked text benchmarks. Other text rows use the accuracy metric reported by our evaluation suite. Bold marks the highest available numerical score in each row; it does not indicate statistical significance.

Multimodal results are reported only for Hy4 flash Base and Hy4 Base.

ARC-Challenge and HellaSwag use 299-item and 3,000-item subsets, respectively. INCLUDE uses a 5,000-example Lite subset covering 44 languages. Belebele covers German, Korean, Vietnamese, Spanish, and Russian (4,475 examples in total).

**Disclaimer: Because our base model was exposed to a large amount of synthetic instruction data during mid-training, it occasionally fails to follow the expected answer format in few-shot evaluations, which may distort the scores.**

### Practicality and Cost Efficiency

#### Optimization Approach

Across training, evaluation, and inference, we aggressively optimized for cost efficiency while preserving intelligence:

- **Pre-training**: Hy4 flash integrates hybrid attention, LatentMoE, and Engram into its architecture—reducing KV cache size to just **1/24 of Hy3** and **1/6 of Hy4**, with extensive scaling ladder experiments ensuring performance meets expectations.
- **Post-training**: Self-distillation from Hy4 establishes strong general intelligence, while reinforcement learning cuts average end-to-end output tokens by **50%**.
- **Evaluation**: We built WorkIndex, an internal benchmark grounded in typical WorkBuddy tasks, and paired it with human evaluation—focusing on **deliverable quality, single-turn output length, and task turnaround time** rather than public benchmark scores detached from everyday work.
- **Inference**: Combining megakernels, 4-bit quantization, and [DFly2](#dfly2-for-speculative-decoding) pushes decoding speed past **150 tokens/s**, enabling low-cost serving at scale.

#### Task Performance and Cost

**Hy4 flash delivers overall task performance slightly above Hy4 preview at a much lower cost per task.** On WorkIndex, it scores **42.1**, compared with **39.7** for Hy4 preview, while its average cost per task is just **1/13 of Hy4 preview**, **1/20 of Hy4**, and **1/8 of DeepSeek-V4.1-Flash-1017** (Max tier, peak-hour pricing).

<p align="center">
  <a href="https://huggingface.co/tencent/Hy4-flash/resolve/main/assets/performance-cost-workindex.png"><img src="https://huggingface.co/tencent/Hy4-flash/resolve/main/assets/performance-cost-workindex.png" alt="Performance and cost per task on WorkIndex for Hy4 flash and comparison models" width="49%"/></a>
  <a href="https://huggingface.co/tencent/Hy4-flash/resolve/main/assets/performance-cost-open-benchmarks.png"><img src="https://huggingface.co/tencent/Hy4-flash/resolve/main/assets/performance-cost-open-benchmarks.png" alt="Performance and cost per task on Open Benchmarks for Hy4 flash and comparison models" width="49%"/></a>
</p>
<p align="left"><sub>Figure 1: Performance and cost across internal and external tasks. WorkIndex (internal) comprises 8 evaluation sets covering slide creation, slide editing, human-AI slide co-writing, Markdown human-AI co-writing, document editing, spreadsheet repair, audio/video processing, and visual understanding.<br/>Open Benchmarks includes 7 public agent benchmarks: DeepSWE, ProgramBench, Terminal-Bench 4.0, APEX-Agents, AutomationBench, HLE, and OSWorld 2.1.</sub></p>

<p align="center">
  <a href="https://huggingface.co/tencent/Hy4-flash/resolve/main/assets/workindex-cost.png"><img src="https://huggingface.co/tencent/Hy4-flash/resolve/main/assets/workindex-cost.png" alt="Average cost per task on WorkIndex for Hy4 flash, Hy4 preview, and Hy4" width="100%"/></a>
</p>
<p align="left"><sub>Figure 2: Average cost per task on WorkIndex. Task scores are 42.1 for Hy4 flash, 39.7 for Hy4 preview, and 51.4 for Hy4.</sub></p>

We recommend Hy4 flash for most everyday productivity tasks, including **deep search, document processing, slide creation, simple frontend demos, and computer use**. For complex tasks such as long-horizon software engineering, we recommend Hy4 for its higher intelligence ceiling.

#### User Blind Evaluation

In the blind evaluation, **Hy4 flash achieved user satisfaction close to Claude Haiku 5.5, while recording the lowest cost per task and shortest median end-to-end completion time among the evaluated models**. Its user satisfaction score was **2.79/4** (Claude Haiku 5.5: **2.81/4**), with a median end-to-end completion time of **6.7 minutes** and a cost of **RMB 0.26 per task**.

<p align="center">
  <a href="https://huggingface.co/tencent/Hy4-flash/resolve/main/assets/blind-evaluation-en.png"><img src="https://huggingface.co/tencent/Hy4-flash/resolve/main/assets/blind-evaluation-en.png" alt="Blind evaluation comparing user satisfaction, median end-to-end completion time, and cost per task" width="100%"/></a>
</p>
<p align="left"><sub>Figure 3: Blind evaluation with 85 internal WorkBuddy users across 259 tasks spanning 27 categories.</sub></p>

### Appendix: Benchmark results

<p align="center">
  <a href="https://huggingface.co/tencent/Hy4-flash/resolve/main/assets/benchmark.png"><img src="https://huggingface.co/tencent/Hy4-flash/resolve/main/assets/benchmark.png" alt="Full benchmark scores, task costs, and evaluation notes for Hy4 flash and comparison models" width="100%"/></a>
</p>

### Quickstart

Use [Transformers](#transformers) to load the model for local inference, or deploy a server and access it through the [OpenAI-compatible API](#openai-compatible-api).

> **Reasoning mode (instruct models)**: `reasoning_effort` supports `"high"` (default, thinking enabled) and `"no_think"` (direct responses). Both examples below use `"no_think"`.
>
> **Recommended sampling parameters**: `temperature=0.9`, `top_p=1.0`.

#### Transformers

> Support for Hy4 flash will be merged into the `transformers` main branch soon. Until then, install from the commit below.

```bash
pip install "transformers[torch,vision] @ git+https://github.com/huggingface/transformers.git@refs/pull/50903/head"
```

The following example generates a brief image description:

```python
from transformers import AutoModelForImageTextToText, AutoProcessor

model_id = "tencent/Hy4-flash"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForImageTextToText.from_pretrained(model_id, device_map="auto")

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg",
            },
            {"type": "text", "text": "Describe this image in one sentence."},
        ],
    }
]

inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
    reasoning_effort="no_think",
).to(model.device)

outputs = model.generate(**inputs, max_new_tokens=256)
print(processor.decode(outputs[0, inputs["input_ids"].shape[1] :], skip_special_tokens=True))
```

#### OpenAI-compatible API

For API access, start a server using the [vLLM deployment instructions](#vllm), then run the following client example:

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="EMPTY")

response = client.chat.completions.create(
    model="hy4-flash",
    messages=[
        {"role": "user", "content": "Hello! Can you briefly introduce yourself?"},
    ],
    temperature=0.9,
    top_p=1.0,
    extra_body={"chat_template_kwargs": {"reasoning_effort": "no_think"}},
)
print(response.choices[0].message.content)
```

### Deployment

#### DFly2 for Speculative Decoding

DFly2 is Hy4 flash's speculative-decoding drafter, trained with [AngelSpec](https://github.com/Tencent/AngelSpec) and built directly on the target model's **Top-k Sparse KV**: each draft layer shares the KV cache (**KV Share**) and the compressed indexer's selection of up to 2,048 positions (**Index Share**) with its corresponding sparse attention layer. This yields three advantages:

- **Constant cost**: each draft token attends to at most ~2K keys, regardless of context length.
- **Zero extra KV memory**: no separate KV cache is maintained for the drafter.
- **PD-disaggregation ready**: not involved in prefill; the prefill-to-decode transfer adds only one last-layer hidden state.

<p align="center">
  <a href="https://huggingface.co/tencent/Hy4-flash/resolve/main/assets/dfly2.png"><img src="https://huggingface.co/tencent/Hy4-flash/resolve/main/assets/dfly2.png" alt="DFly2 architecture: each draft layer reuses the KV cache and the indexer-selected positions of a sparse attention layer of Hy4 flash" width="75%"/></a>
</p>

#### Quantization

We provide [AngelSlim](https://github.com/tencent/AngelSlim), a more accessible, comprehensive, and efficient toolkit for large model compression. AngelSlim supports a comprehensive suite of compression tools for large-scale multimodal models, including common quantization algorithms, low-bit quantization, and speculative sampling.

For this model, we have provided a [GGUF](https://huggingface.co/AngelSlim/Hy4-flash-GGUF) compressed version for end-to-end testing purposes.

#### Inference Frameworks

For production serving, we recommend using [vLLM](https://github.com/vllm-project/vllm) or [SGLang](https://docs.sglang.io/). Please refer to the recipes:
- [Hy4 flash vLLM Recipe](https://recipes.vllm.ai/tencent/Hy4-flash)
- [Hy4 flash SGLang Cookbook](https://docs.sglang.io/cookbook/autoregressive/Tencent/Hy4-flash)

##### vLLM

Use official prebuilt image `vllm/vllm-openai:hy4-flash`:

```bash
docker run --gpus all \
  -p 8000:8000 \
  --ipc=host \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  vllm/vllm-openai:hy4-flash tencent/Hy4-flash-FP8 \
    --tensor-parallel-size 8 \
    --speculative-config '{"num_speculative_tokens":5,"method":"dfly"}' \
    --attention-backend FLASHMLA_SPARSE \
    --tool-call-parser hy_v4 \
    --reasoning-parser hy_v4 \
    --enable-auto-tool-choice \
    --port 8000 \
    --served-model-name hy4-flash
```

##### SGLang

Use the official prebuilt image `lmsysorg/sglang:hy4-flash` (multi-arch, x86 and Arm):

```bash
docker pull lmsysorg/sglang:hy4-flash

docker run --gpus all \
  -p 8000:8000 \
  --ipc=host \
  lmsysorg/sglang:hy4-flash \
  sglang serve \
    --trust-remote-code \
    --model-path tencent/Hy4-flash-FP8 \
    --tp 8 \
    --cuda-graph-backend-prefill disabled \
    --speculative-algorithm DFLY \
    --speculative-dfly-block-size 6 \
    --host 127.0.0.1 \
    --port 8000
```

