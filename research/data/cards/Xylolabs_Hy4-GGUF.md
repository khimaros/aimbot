---
license: other
license_name: tencent-hy-license
license_link: LICENSE
base_model:
- tencent/Hy4
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
- hy4
- moe
- multimodal
---

<div align="center">

<img class="block dark:hidden mx-auto" src="https://raw.githubusercontent.com/XylolabsInc/tensix-bfp-gptq/main/assets/xylolabs-lockup.svg" alt="Xylolabs" width="256" height="40">
<img class="hidden dark:block mx-auto" src="https://raw.githubusercontent.com/XylolabsInc/tensix-bfp-gptq/main/assets/xylolabs-lockup-dark.svg" alt="Xylolabs" width="256" height="40">

<h1>Hy4 GGUF</h1>

[![Base model](https://img.shields.io/badge/base-tencent%2FHy4-blue)](https://huggingface.co/tencent/Hy4)
[![Formats](https://img.shields.io/badge/formats-Q8__0%20%2F%20Q6__K%20%2F%20Q4__K__M%20%2F%20IQ3__S%20%2F%20IQ2__XXS-5B2C83)](#files)
[![License](https://img.shields.io/badge/license-Tencent%20Hy%20License-green)](https://huggingface.co/Xylolabs/Hy4-GGUF/blob/main/LICENSE)
[![Code](https://img.shields.io/badge/code-llama.cpp%20PR%2032517-black)](https://github.com/ggml-org/llama.cpp/pull/32517)

</div>

GGUF quants of [tencent/Hy4](https://huggingface.co/tencent/Hy4) for multimodal inference with llama.cpp.

## Files

| Quant | Parts | Size |
|---|---:|---:|
| Q8_0 | 13 | 818.5 GB |
| Q6_K | 13 | 638.3 GB |
| Q4_K_M | 13 | 464.1 GB |
| IQ3_S | 13 | 328.0 GB |
| IQ2_XXS | 13 | 219.4 GB |
| `mmproj-Hy4-BF16.gguf` (vision) | 1 | 2.7 GB |
| `mmproj-Hy4-Q8_0.gguf` (vision) | 1 | 1.6 GB |
| `Hy4.imatrix.gguf` | 1 | 2.4 GB |
| `Hy4.imatrix.ub12288.gguf` | 1 | 2.4 GB |

## How to run

Hy4 support is llama.cpp pull request [#32517](https://github.com/ggml-org/llama.cpp/pull/32517) until it is merged. Keep all parts of a quant in one folder and pass part 1:

```sh
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
git fetch origin pull/32517/head:hy4 && git checkout hy4
cmake -B build -DCMAKE_BUILD_TYPE=Release        # add -DGGML_CUDA=ON for NVIDIA GPUs
cmake --build build -j --target llama-cli llama-server

./build/bin/llama-cli -m Hy4-Q4_K_M-00001-of-00013.gguf -ngl 99 --jinja -c 8192
```

`llama-server` takes the same flags. Keep `--ubatch-size` at 8192 or below; larger ubatches can give wrong output in this llama.cpp build.

## Accuracy

Mean KL divergence and top-1 agreement against the BF16 model, measured with llama.cpp on WikiText-2, chat and held-out text; Answers is a five-question check.

| Quant | Size | WikiText-2 KL | top-1 | Chat KL | top-1 | Held-out KL | top-1 | Answers |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Q8_0 | 818.5 GB | 0.0373 | 94.6% | 0.1187 | 93.3% | 0.0173 | 96.0% | 5/5 |
| Q6_K | 638.3 GB | 0.0431 | 93.8% | 0.1235 | 92.8% | 0.0188 | 95.5% | 5/5 |
| Q4_K_M | 464.1 GB | 0.0920 | 90.8% | 0.1590 | 91.3% | 0.0408 | 93.8% | 5/5 |
| AngelSlim Q4_K_M | 470.2 GB | 0.1464 | 88.3% | 0.2315 | 88.8% | 0.0713 | 91.9% | 5/5 |
| IQ3_S | 328.0 GB | 0.3237 | 82.8% | 0.2851 | 87.3% | 0.1535 | 88.1% | 5/5 |
| AngelSlim IQ2 | 332.4 GB | 0.5673 | 76.9% | 0.4303 | 83.5% | 0.2802 | 83.8% | 5/5 |
| IQ2_XXS | 219.4 GB | 0.8881 | 70.1% | 0.5610 | 80.7% | 0.4522 | 80.3% | 5/5 |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://huggingface.co/Xylolabs/Hy4-GGUF/resolve/main/accuracy-mean-kl-dark.png">
  <img src="https://huggingface.co/Xylolabs/Hy4-GGUF/resolve/main/accuracy-mean-kl.png" alt="Mean KL divergence by text-model GGUF size">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://huggingface.co/Xylolabs/Hy4-GGUF/resolve/main/accuracy-top1-dark.png">
  <img src="https://huggingface.co/Xylolabs/Hy4-GGUF/resolve/main/accuracy-top1.png" alt="Top-1 accuracy by text-model GGUF size">
</picture>

## Which file for your hardware

A file fits when its size plus the KV cache at that context (f16) plus 2 GB for the runtime is under 90% of the memory.

| Hardware | Memory | File | Context |
|---|---|---|---:|
| RTX 4090 / RTX 3090 | 24 GB | none | |
| RTX 5090 | 32 GB | offload | 32K |
| RTX 6000 Ada, or 2 x 24 GB | 48 GB | offload | 32K |
| One H100 | 80 GB | offload | 32K |
| RTX PRO 6000 Blackwell (GDDR7) | 96 GB | offload | 32K |
| DGX Spark | 128 GB unified | none | |
| Mac Studio M5 Max | 128 GB unified | none | |
| One H200 (HBM3e) | 141 GB | offload | 32K |
| One B200 (about 180 GB usable in a DGX B200) | 192 GB | offload | 32K |
| Mac Studio M5 Ultra | 256 GB unified | `Hy4-IQ2_XXS`* (219.4 GB) | 64K |
| Mac Studio M5 Ultra | 512 GB unified | `Hy4-IQ3_S` (328.0 GB) | 512K |
| One B300 (HBM3e; usable a little less) | 288 GB | `Hy4-IQ2_XXS` (219.4 GB) | 256K |
| 2 x H200 | 282 GB | `Hy4-IQ2_XXS` (219.4 GB) | 256K |
| 4 x H200 | 564 GB | `Hy4-Q4_K_M` (464.1 GB) | 256K |
| 8 x H200 | 1,128 GB | `Hy4-Q8_0` (818.5 GB) | 1M |
| 4 x B200 (about 720 GB usable) | 768 GB | `Hy4-Q6_K` (638.3 GB) | 64K |
| 8 x B200 (about 1,440 GB usable) | 1,536 GB | `Hy4-Q8_0` (818.5 GB) | 1M |

\* Needs the macOS GPU memory limit raised.

Offload: keep the expert weights in system RAM with `--n-cpu-moe N` (the experts of the first N layers), for example `llama-server -m FILE --n-cpu-moe 40`; lower N for speed while the model still fits your GPU. Use a smaller file if your RAM is short.

## License and notices

These files are under the Tencent Hy License, Version 1.0 (`LICENSE`), including its extra terms for large Model-as-a-Service operators; `NOTICE` names the source model and its copyright holder. Xylolabs is not affiliated with or endorsed by Tencent.

## Updates

- 2026-11-22: Added Q6_K (638.3 GB) and IQ2_XXS (219.4 GB).
- 2026-11-21: Added IQ3_S and the importance matrices; accuracy re-measured on WikiText-2, chat and held-out text.
- 2026-11-20: First release: Q8_0 and Q4_K_M with BF16 and Q8_0 vision projectors.

## Tencent's original model description

Below is Tencent's README for [tencent/Hy4](https://huggingface.co/tencent/Hy4) (copyright Tencent, Tencent Hy License) without its metadata header, unchanged except for heading levels and image paths; it describes the original checkpoints, so use "How to run" above for these files.

<p align="left">
    <a href="https://huggingface.co/tencent/Hy4/blob/main/README_CN.md">中文</a>&nbsp;｜&nbsp;English
</p>
<br>

<p align="center">
 <img src="https://huggingface.co/tencent/Hy4/resolve/main/assets/logo-en.png" width="400"/> <br>
</p>

<div align="center" style="line-height: 1;">

[![License](https://img.shields.io/badge/License-Tencent%20Hy%20License-blue)](#license)
&nbsp;&nbsp;
[![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Tencent%20Hy-ffc107?color=ffc107&logoColor=white)](https://huggingface.co/tencent/Hy4)
&nbsp;&nbsp;
[![ModelScope](https://img.shields.io/badge/ModelScope-Tencent%20Hy-624aff)](https://modelscope.cn/models/Tencent-Hunyuan/Hy4)
&nbsp;&nbsp;
[![GitCode](https://img.shields.io/badge/GitCode-Tencent%20Hy-red?logoColor=white)](https://ai.gitcode.com/tencent_hunyuan/Hy4)

</div>

<p align="center">
    🖥️&nbsp;<a href="https://hy.tencent.ai/research/hy4"><b>Official Website</b></a>&nbsp;&nbsp;|&nbsp;&nbsp;
    💬&nbsp;<a href="https://github.com/Tencent-Hunyuan/Hy4"><b>GitHub</b></a>&nbsp;&nbsp;|&nbsp;&nbsp;
    📱&nbsp;<a href="https://huggingface.co/AngelSlim/Hy4-GGUF"><b>GGUF</b></a></p>

---

### Table of Contents

- [Model Introduction](#model-introduction)
- [Pretrained model capability](#pretrained-model-capability)
- [Key Improvements](#key-improvements)
- [Capabilities and Use Cases](#capabilities-and-use-cases)
  - [Vision and computer use](#vision-and-computer-use)
  - [Frontend and game development](#frontend-and-game-development)
  - [Finance and office workflows](#finance-and-office-workflows)
  - [Scientific research and AI R&D](#scientific-research-and-ai-rd)
  - [Long-horizon personal assistant](#long-horizon-personal-assistant)
- [Known Limitations](#known-limitations)
- [Appendix: benchmark results](#appendix-benchmark-results)
- [News](#news)
- [Model Links](#model-links)
- [Quickstart](#quickstart)
- [Deployment](#deployment)
  - [DFly2 for Speculative Decoding](#dfly2-for-speculative-decoding)
  - [Quantization](#quantization)
  - [Inference Frameworks](#inference-frameworks)
    - [vLLM](#vllm)
    - [SGLang](#sglang)
- [Finetuning](#finetuning)
- [System Card](#system-card)
- [License](#license)
- [Contact Us](#contact-us)

---

### Model Introduction

**Hy4** is a new-generation Mixture-of-Experts (MoE) flagship model developed by the Tencent Hy Team, supporting text, image, and video understanding. The language backbone comprises 770B total parameters, of which 49B are activated per token. It consists of 78 layers, with a standard dense FFN in the first layer and MoE FFNs in the remaining 77 layers. Each MoE layer contains 256 routed experts and 1 shared expert; every token activates the top-8 routed experts along with the shared expert. In addition to the backbone, a 5-layer DFly2 drafter (3.3B parameters) is built in for speculative decoding.

On the architecture side, inspired by DeepSeek and GLM, the attention module employs Gated [DeepSeek Sparse Attention](https://arxiv.org/abs/2512.02556) (Gated DSA) with [IndexCache](https://arxiv.org/abs/2603.12201) for cross-layer sparse index reuse. The residual pathway uses [iHC (identity Hyper-Connections)](https://zhuanlan.zhihu.com/p/2010852389670908320) to expand inter-layer information flow. A ViT supports dynamic image resolutions, with an adapter converting image and video frame features into visual tokens for the language model to process alongside text tokens. [DFly2](#dfly2-for-speculative-decoding), a parallel drafter, reuses Hy4's KV cache and sparse indices to support long-context speculative decoding at a low, constant cost.

#### Model Specifications

| Property | Value |
|:---|:---|
| **Overview** | |
| Architecture | Mixture-of-Experts (MoE) |
| Total Parameters (excluding ViT, adapter, and DFly2) | 770B |
| Activated Parameters per Token | Text 49B + Vision 1.23B |
| ViT Parameters | 1.23B |
| DFly2 Parameters | 3.3B |
| Context Length | 1M (1,048,576 tokens) |
| **Language Backbone** | |
| Backbone Layers | 78 — 1 dense layer and 77 MoE layers |
| Hidden Size | 6,144 |
| Vocabulary Size | 120,832 |
| Residual Connections | iHC (identity Hyper-Connections) with 4 residual streams |
| **Attention** | |
| Attention Architecture | Gated DeepSeek Sparse Attention (Gated DSA) with IndexCache |
| Attention Formulation | Multi-head Latent Attention (MLA) |
| Attention Heads | 64 |
| MLA q_lora_rank | 2,048 |
| MLA kv_lora_rank | 512 |
| Indexer Heads / Head Dimension | 32 / 128 |
| Sparse Context Selection | Top-2,048 tokens selected by the indexer |
| **Feed-Forward Networks** | |
| Dense FFN Intermediate Size | 18,432 |
| Routed Experts per MoE Layer | 256 |
| Shared Experts per MoE Layer | 1 |
| Activated Routed Experts per Token | 8 |
| Expert Intermediate Size | 2,048 |
| **Vision Encoder** | |
| Vision Encoder Layers | 40 |
| Vision Encoder Hidden Size | 1,536 |
| Vision Encoder Intermediate Size | 6,144 |
| Vision Encoder Attention Heads | 16 |
| Vision Patch Size | 16 × 16 |
| Vision Position Embedding Size | 128 × 128 |
| Visual Feature Merging | 2 x 2 |

### Pretrained model capability

Bits-per-byte (BPB) on internal code & agent validation, lower is better:

<p align="center">
  <a href="https://huggingface.co/tencent/Hy4/resolve/main/assets/pretrained-model-bpb.png"><img src="https://huggingface.co/tencent/Hy4/resolve/main/assets/pretrained-model-bpb.png" alt="Bits-per-byte on internal code and agent validation versus active parameters; lower is better" width="75%"/></a>
</p>

Few-shot pretrain benchmark evaluation:

| Category | Benchmark | #Shots | Hy4 Base | Hy4 flash Base | Hy3 preview Base | DeepSeek-V4-flash-Base | DeepSeek-V4-Pro-Base |
| --- | --- | :---: | ---: | ---: | ---: | ---: | ---: |
| **Knowledge** | MMLU† | 5 | **91.6** | 88.7 | 87.5 | 89.7 | 91.1 |
|  | MMLU-Pro† | 5 | **73.9** | 71.1 | 65.8 | 68.6 | 73.4 |
|  | MMLU-Redux† | 5 | **90.6** | 87.6 | 87.0 | 88.8 | 90.2 |
|  | SuperGPQA† | 5 | **62.7** | 57.8 | 52.3 | 52.5 | 54.8 |
|  | C-Eval† | 5 | **95.0** | 92.0 | 90.1 | 91.9 | 93.4 |
|  | CMMLU† | 5 | **93.1** | 91.6 | 89.6 | 89.8 | 90.7 |
|  | SimpleQA | 5 | **57.2** | 37.5 | 26.4 | 31.3 | 52.1 |
|  | Chinese-SimpleQA† | 5 | **83.9** | 74.6 | 69.6 | 71.9 | 76.6 |
|  | AGIEval (English)† | 3 | **79.3** | 75.4 | 76.0 | 76.3 | 78.2 |
|  | AGIEval (Chinese)† | 3 | **91.2** | 90.6 | 87.8 | 88.5 | 89.8 |
| **Reasoning** | HellaSwag (3,000-item subset) | 10 | **87.1** | 85.2 | 85.7 | 85.1 | 86.8 |
|  | PIQA | 4 | **85.3** | 84.4 | 84.6 | 83.8 | 84.9 |
|  | ARC-Challenge | 0 | **97.3** | 95.0 | 96.0 | **97.3** | 97.0 |
|  | Social IQa | 0 | **82.7** | 80.1 | 80.5 | 72.5 | 73.1 |
|  | KOR-Bench | 3 | **57.6** | 54.7 | 54.6 | 53.4 | 55.4 |
|  | C³ | 0 | **82.4** | 77.3 | 75.9 | 74.1 | 78.3 |
| **Math** | U-MATH | 5 | **71.6** | 69.8 | 60.9 | 57.4 | 64.8 |
|  | OCW Courses | 5 | 66.7 | 64.0 | 62.6 | 63.3 | **68.2** |
| **Code** | MBPP-plus | 3 | 74.0 | 73.7 | 77.4 | 76.8 | **79.1** |
| **Multilingual** | Belebele (5-language subset)† | 5 | 95.0 | 93.8 | 94.2 | 94.4 | **95.2** |
|  | INCLUDE† | 5 | **88.1** | 82.8 | 84.3 | 84.0 | 84.3 |
| **Multimodal** | MMMU-Pro (Standard, 10 opts) | 4 | **59.6** | 52.0 | — | — | — |
|  | SimpleVQA | 4 | **54.5** | 48.5 | — | — | — |
|  | CVBench | 4 | **86.7** | 83.4 | — | — | — |
|  | RealWorldQA | 4 | **72.3** | 71.1 | — | — | — |
|  | TextVQA | 4 | **78.2** | 73.4 | — | — | — |
|  | CountBenchQA | 4 | **90.6** | 86.6 | — | — | — |

† Macro-averaged accuracy for the marked text benchmarks. Other text rows use the accuracy metric reported by our evaluation suite. Bold marks the highest available numerical score in each row; it does not indicate statistical significance.

Multimodal results are reported only for Hy4 Base and Hy4 flash Base.

ARC-Challenge and HellaSwag use 299-item and 3,000-item subsets, respectively. INCLUDE uses a 5,000-example Lite subset covering 44 languages. Belebele covers German, Korean, Vietnamese, Spanish, and Russian (4,475 examples in total).

**Disclaimer: Because our base model was exposed to a large amount of synthetic instruction data during mid-training, it occasionally fails to follow the expected answer format in few-shot evaluations, which may distort the scores.**

### Key Improvements

Compared with Hy4 preview, Hy4 substantially scales up both pre-training and post-training. It adds vision capabilities and delivers major gains in instruction following, long-context understanding, long-horizon tasks, and deep research.

<p align="center">
  <a href="https://huggingface.co/tencent/Hy4/resolve/main/assets/benchmark.jpg"><img src="https://huggingface.co/tencent/Hy4/resolve/main/assets/benchmark.jpg" alt="Hy4 benchmark highlights compared with Hy4 preview and other models" width="100%"/></a>
</p>

### Capabilities and Use Cases

#### Vision and computer use

By combining perception, reasoning, and tool use, Hy4 can understand fine-grained image details and interpret complex charts. It supports computer-use workflows across command-line interfaces (CLI) and graphical user interfaces (GUI). Targeted training on specialized software such as Blender and CAD, as well as long-horizon workflows spanning multiple applications, improves task planning and execution.

#### Frontend and game development

For frontend work, we optimized Hy4 for complex UI interactions, business logic, state management, and full-stack integration, so that generated interfaces are not only visually polished but also functionally complete.

For game development, we partnered with professional developers at Tencent Interactive Entertainment Group (IEG) to curate high-quality training data and build evaluations. We focused on feature implementation, gameplay logic, state tracking, and asset pipelines. We also extensively adapted Hy4 for major engines such as Unreal Engine, Unity, and Godot, and expanded its capabilities to multiplayer game development. Compared with Hy4 preview, Hy4 improves by 19.1% on GameDev and 9.8% on GameLogic.

#### Finance and office workflows

To ground Hy4 in real-world financial work, we built thousands of realistic workspaces and tens of thousands of tasks spanning fund research, equity analysis, quantitative strategies, asset allocation, corporate finance, and tax accounting. Working with Tencent Financial Technology (FiT), we evaluated Hy4 with 213 finance professionals, including 153 experts from leading financial institutions. More than 70% of these experts have over five years of industry experience. Across 579 real-world financial tasks, Hy4 ranks first among open-weight models:

| Model | Average Score (out of 4) |
|:---|:---:|
| **Hy4** | **3.04** |
| DeepSeek-V4.1-Flash-1017 | 2.97 |
| Kimi K3.1 Pro | 2.68 |
| GLM-5.3 | 2.68 |

On IRAB, an internal benchmark from financial AI agent company RabyteTech, Hy4 also scores 12.03 percentage points higher than Hy4 preview. To make Hy4 more reliable for financial and office workflows, we made targeted upgrades to search, focusing on time-sensitive retrieval, multi-source synthesis, and factual consistency verification. In internal evaluations, Hy4 cut the hallucination rate from 15.76% (on Hy4 preview) to 5.45%, and reduced speculative errors from 23.1% to 5.6%. We also improved Hy4’s ability to co-edit Word, Excel, and PowerPoint files with people in real time. In blind evaluations, Hy4 shows clear gains over Hy4 preview in document formatting, reliability, and overall usability.

#### Scientific research and AI R&D

Hy4 combines deep reasoning, scientific computing, and long-horizon execution for research workflows. On TenureTrail, our internal benchmark of 123 research tasks across seven disciplines, Hy4 ranks first among open-weight models. It shows strong capabilities in mathematical construction, physical modeling, earth sciences, systems engineering, and socioeconomic decision-making. Paired with our [Hyra 2.0](https://hy.tencent.ai/research/hyra2) harness, Hy4 optimized our internal pre-training infrastructure for smaller models with the same architecture, and autonomously trained a variant that outperforms the official Jev baseline on multiple benchmarks.

#### Long-horizon personal assistant

Given relevant work context, Hy4 can synthesize information from chat history, emails, documents, calendars, and meeting notes. It can track project history and updates, surface action items, prepare meeting briefs, flag upcoming deadlines, and help prioritize tasks.

### Known Limitations

Although Hy4 is one of the strongest open-weight models available today, a notable gap remains between it and top proprietary models, particularly on challenging internal benchmarks for research-level mathematics, long-horizon coding, model self-improvement, and advanced visual question answering.

<p align="center">
  <a href="https://huggingface.co/tencent/Hy4/resolve/main/assets/benchmark-limitations.jpg"><img src="https://huggingface.co/tencent/Hy4/resolve/main/assets/benchmark-limitations.jpg" alt="Challenging benchmarks illustrating remaining gaps between Hy4 and leading proprietary models" width="100%"/></a>
</p>

### Appendix: benchmark results

<p align="center">
  <a href="https://huggingface.co/tencent/Hy4/resolve/main/assets/benchmark-appendix.jpg"><img src="https://huggingface.co/tencent/Hy4/resolve/main/assets/benchmark-appendix.jpg" alt="Full Hy4 benchmark results, comparison models, and evaluation notes" width="100%"/></a>
</p>

### News

* We open-source **Hy4**, **Hy4-FP8**, and the pre-trained **Hy4 base** model weights on [Hugging Face](https://huggingface.co/tencent/Hy4), [ModelScope](https://modelscope.cn/models/Tencent-Hunyuan/Hy4), and [GitCode](https://ai.gitcode.com/tencent_hunyuan/Hy4).

### Model Links

| Model Name | Description | Hugging Face | ModelScope | GitCode |
|:---|:---|:---:|:---:|:---:|
| Hy4 | Instruct model | [Model](https://huggingface.co/tencent/Hy4) | [Model](https://modelscope.cn/models/Tencent-Hunyuan/Hy4) | [Model](https://ai.gitcode.com/tencent_hunyuan/Hy4) |
| Hy4-FP8 | FP8 quantized instruct model | [Model](https://huggingface.co/tencent/Hy4-FP8) | [Model](https://modelscope.cn/models/Tencent-Hunyuan/Hy4-FP8) | [Model](https://ai.gitcode.com/tencent_hunyuan/Hy4-FP8) |
| Hy4 base | Pre-trained base model | [Model](https://huggingface.co/tencent/Hy4-base) | [Model](https://modelscope.cn/models/Tencent-Hunyuan/Hy4-base) | [Model](https://ai.gitcode.com/tencent_hunyuan/Hy4-base) |

Hy4 base is a pre-trained base model, not an instruction-tuned chat model. The chat and reasoning examples below apply to Hy4 and Hy4-FP8.

### Quickstart

Deploy Hy4 with [vLLM](#vllm) or [SGLang](#sglang) first, then call the OpenAI-compatible API:

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="EMPTY")

response = client.chat.completions.create(
    model="hy4",
    messages=[
        {"role": "user", "content": "Hello! Can you briefly introduce yourself?"},
    ],
    temperature=0.9,
    top_p=1.0,
)
print(response.choices[0].message.content)
```

> **Recommended parameters**: `temperature=0.9`, `top_p=1.0`.
>
> **Reasoning mode**: `reasoning_effort` accepts `"no_think"` and `"high"`. It defaults to `"high"` (deep chain-of-thought), which suits complex tasks such as math, coding, and reasoning. For direct responses, pass `extra_body={"chat_template_kwargs": {"reasoning_effort": "no_think"}}`.

See the [Deployment](#deployment) section below for how to start the API server.

### Deployment

#### DFly2 for Speculative Decoding

DFly2 is Hy4's speculative-decoding drafter, trained with [AngelSpec](https://github.com/Tencent/AngelSpec) and built directly on Hy4's **Top-k Sparse KV**: each draft layer shares the KV cache (**KV Share**) and the indexer-selected top-2048 positions (**Index Share**) with its corresponding Hy4 DSA layer. This yields three advantages:

- **Constant cost**: each draft token attends to at most ~2K keys, regardless of context length.
- **Zero extra KV memory**: no separate KV cache is maintained for the drafter.
- **PD-disaggregation ready**: not involved in prefill; the prefill-to-decode transfer adds only one last-layer hidden state.

<p align="center">
  <a href="https://huggingface.co/tencent/Hy4/resolve/main/assets/dfly2.png"><img src="https://huggingface.co/tencent/Hy4/resolve/main/assets/dfly2.png" alt="DFly2 architecture: each draft layer reuses the KV cache and indexer-selected top-k positions of a Hy4 DSA layer" width="75%"/></a>
</p>

#### Quantization

We provide [AngelSlim](https://github.com/tencent/AngelSlim), a more accessible, comprehensive, and efficient toolkit for large model compression. AngelSlim supports a comprehensive suite of compression tools for large-scale multimodal models, including common quantization algorithms, low-bit quantization, and speculative sampling.

For this model, we have provided a [GGUF](https://huggingface.co/AngelSlim/Hy4-GGUF) compressed version for end-to-end testing purposes.

#### Inference Frameworks

For production serving, we recommend using [vLLM](https://github.com/vllm-project/vllm) or [SGLang](https://docs.sglang.io/). Please refer to the recipes:
- [Hy4 vLLM Recipe](https://recipes.vllm.ai/tencent/Hy4)
- [Hy4 SGLang Cookbook](https://docs.sglang.io/cookbook/autoregressive/Tencent/Hy4)

##### vLLM

Use official prebuilt image `vllm/vllm-openai:hy4`:

```bash
docker run --gpus all \
  --privileged --ipc=host -p 8000:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -e VLLM_USE_RUST_FRONTEND=1 \
  vllm/vllm-openai:hy4 tencent/Hy4-FP8 \
  --dtype bfloat16 \
  --limit-mm-per-prompt '{"image":1,"video":0}' \
  --tensor-parallel-size 8 \
  --enable-auto-tool-choice \
  --reasoning-parser hy_v4 \
  --tool-call-parser hy_v4 \
  --speculative-config '{"num_speculative_tokens":5,"method":"dfly"}' \
  --attention-backend FLASHMLA_SPARSE \
  --port 8000 \
  --served-model-name hy4
```

##### SGLang

Use the official prebuilt image `lmsysorg/sglang:hy4` (multi-arch, x86 and Arm):

```bash
docker pull lmsysorg/sglang:hy4

docker run --gpus all --ipc=host -p 8000:8000 lmsysorg/sglang:hy4 \
  sglang serve \
    --model-path tencent/Hy4-FP8 \
    --tp 8 \
    --speculative-algorithm DFLY \
    --port 8000 \
    --served-model-name hy4

```

### Finetuning

Hy4 provides a complete model finetuning pipeline. For detailed documentation, please refer to: [Finetuning Guide](https://huggingface.co/tencent/Hy4/blob/main/finetune/README.md).

### System Card

Please refer to the [Hy4 System Card](https://hy.tencent.ai/Hy4_system_card.pdf).

### License

Hy4 is released under the **Tencent Hy License**. See [LICENSE](https://huggingface.co/tencent/Hy4/blob/main/LICENSE) for details.

### Contact Us

If you have any questions or suggestions, feel free to reach out to our R&D and product teams via email:

📧 **hunyuan_opensource@tencent.com**

---

<p align="center">
  <i>Hy4 is developed by the Tencent Hy Team.</i>
</p>
