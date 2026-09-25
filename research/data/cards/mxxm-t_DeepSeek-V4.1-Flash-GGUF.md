---
license: mit
base_model:
  - deepseek-ai/DeepSeek-V4.1-Flash
base_model_relation: quantized
library_name: gguf
pipeline_tag: text-generation
tags:
  - gguf
  - deepseek
  - deepseek-v4
  - moe
  - mxfp4
  - dspark
  - speculative-decoding
  - llama.cpp
  - mx-llama.cpp
---

# DeepSeek-V4.1-Flash (GGUF)

> These files are built for **[mx-llama.cpp](https://github.com/mxxm-t/mx-llama.cpp)**, a fork of
> llama.cpp focused on multi-GPU inference: layer pipeline parallelism, tensor parallelism
> (`-sm tensor`) with a custom AllReduce, and DSpark / MTP speculative decoding. Prebuilt AMD / ROCm
> and NVIDIA / CUDA images are on Docker Hub at
> **[mxxm/mx-llama.cpp](https://hub.docker.com/r/mxxm/mx-llama.cpp)**.
>
> It runs this model on both `-sm layer` and `-sm tensor`: see the DeepSeek-V4.1-Flash section of
> [FEATURES.md](https://github.com/mxxm-t/mx-llama.cpp/blob/master/FEATURES.md) for scope and
> measurements.

[deepseek-ai/DeepSeek-V4.1-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) converted to
GGUF, plus its DSpark draft stages as a separate sidecar file. These files hold the text model only:
the vision tower and its projector are not included, and there is no `mmproj`. DeepSeek's original model
card follows below.

## Files

| file | size | notes |
|---|---|---|
| `DeepSeek-V4.1-Flash-MXFP4-00001-of-00012.gguf` .. `-00012-of-00012.gguf` | 375.8 GiB total | main model, routed experts MXFP4 |
| `DeepSeek-V4.1-Flash-DSpark-MXFP4.gguf` | 7.43 GiB | DSpark draft stages, not a standalone model |

Shards `00009` and `00011` each hold one Engram table (about 97 GiB together). They are read at random
during prompt processing and stay on disk rather than in VRAM, so they belong on the fastest storage
you have: moving them from a SATA SSD pool to NVMe roughly doubles prompt processing.

The sidecar holds the three `mtp.*` draft stages, 128 routed experts each with 3 active, plus the
DSpark heads: `fc` and `enc.output_norm` from stage 0, the markov and confidence heads from stage 2.
It taps the attention input of target layers 37, 38 and 39. It cannot generate on its own. It is a
draft model for speculative decoding against the main file.

## Running it

The weights occupy roughly 302 GiB once loaded with repack enabled, before KV cache and compute
buffers. An example command:

```
llama-server -m DeepSeek-V4.1-Flash-MXFP4-00001-of-00012.gguf \
  -sm tensor -tps 2 -ngl 99 -fit off \
  -c 32768 -b 8192 -ub 512 -fa 1 -lm dio
```

`-tps` sets the width of each tensor-parallel group, and the remaining GPUs form pipeline stages. For
this model a group must divide both the head count (64) and the output group count (8), so the usable
widths are 1, 2, 4 and 8, and the number of groups has to divide the number of GPUs.
`-sm layer` also runs and keeps an advantage for prompt processing on long inputs; `-sm tensor` is the
faster of the two for generation on PCIe systems, and returns the same tokens from boot to boot.

Chat completions place the reply in `reasoning_content` rather than `content` for this architecture.

## What this build brings to the model

- Architecture support: compressed KV tiers from model metadata, the shifted hyper-connection mix, head
  fold without `output_hc_*` tensors.
- Engram memory read on demand rather than held resident.
- MXFP4 weight repack for gfx906, in every split mode.
- Tensor parallelism across pipeline stages, with whole-token graph capture and stage-local mirrored
  weights.
- DSpark speculative decoding against the sidecar, including under tensor parallelism. The sidecar is
  resident alongside the model, so a tightly sized system may need a smaller `-ub`.

## What is checked

- every tensor the architecture declares is present, checked against the source checkpoint's own
  `weight_map`
- FP8 tensors dequantized with the checkpoint's 32 x 32 scale blocks and compared against the source,
  dtype by dtype
- the sidecar accounts for all 69 source `mtp.*` names, with shapes matching `config.json` and
  quantization types matching the V4 sidecar on shared tensors
- the Engram hash tables reproduce the reference `engram.py` derivation: its primes, multipliers,
  offsets and index order

## Quantization

Routed experts are repacked from the checkpoint's own FP4 to MXFP4, a format change rather than a
requantization. FP8 block-scaled tensors are dequantized and stored Q8_0. Norms, hyper-connection
coefficients and the router bias stay F32. The router, markov and confidence weights stay BF16.

No weights were retrained, fine-tuned or otherwise altered.

## License

MIT, inherited from the base model. A copy is included in this repository as `LICENSE`, as its terms
require. Copyright (c) 2023 DeepSeek.

---

## Original model card

Reproduced from [deepseek-ai/DeepSeek-V4.1-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash),
unchanged except that its relative links now point to that repository.

# DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression

<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

<div align="center">
  <img src="https://github.com/deepseek-ai/DeepSeek-V2/blob/main/figures/logo.svg?raw=true" width="60%" alt="DeepSeek-V4.1" />
</div>
<hr>
<div align="center" style="line-height: 1;">
  <a href="https://www.deepseek.com/" target="_blank" style="margin: 2px;">
    <img alt="Homepage" src="https://github.com/deepseek-ai/DeepSeek-V2/blob/main/figures/badge.svg?raw=true" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://chat.deepseek.com/" target="_blank" style="margin: 2px;">
    <img alt="Chat" src="https://img.shields.io/badge/🤖%20Chat-DeepSeek%20V4.1-536af5?color=536af5&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>
<div align="center" style="line-height: 1;">
  <a href="https://huggingface.co/deepseek-ai" target="_blank" style="margin: 2px;">
    <img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-DeepSeek%20AI-ffc107?color=ffc107&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://twitter.com/deepseek_ai" target="_blank" style="margin: 2px;">
    <img alt="Twitter Follow" src="https://img.shields.io/badge/Twitter-deepseek_ai-white?logo=x&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>
<div align="center" style="line-height: 1;">
  <a href="https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/LICENSE" style="margin: 2px;">
    <img alt="License" src="https://img.shields.io/badge/License-MIT-f5de53?&color=f5de53" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>

<p align="center">
  <a href="https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/DeepSeek_V41_Tech_Report.pdf"><b>Technical Report</b> 👁️</a>
</p>

## Introduction

We introduce **DeepSeek-V4.1-Flash**, a multimodal Mixture-of-Experts (MoE) model with 552B backbone parameters and support for contexts of up to one million tokens. The model natively processes images and text, and generates text autoregressively.

**Architecture.** DeepSeek-V4.1-Flash adopts a **Causal Encoder-Decoder (CED)** architecture: a 40-layer Transformer organized as a 20-layer causal encoder followed by a 20-layer decoder. With CED, the decoder's global KV cache is projected from the final encoder hidden states rather than derived from each decoder layer's own hidden states. This allows the model to activate only **8B parameters per token during prefill** and **16B during decode**, substantially improving cost efficiency for input-heavy agentic workloads. **SWA Bounded Replay** reconstructs missing SWA KV states by replaying only the most recent *n*_win tokens, avoiding the need to persist SWA KV to SSD and reducing the persistent KV cache footprint to roughly **1/8** of that of DeepSeek-V4-Flash.

**Compressed Sparse Attention 2 (CSA2).** DeepSeek-V4.1-Flash uses CSA2, which assigns each attention layer one of three static modes — **Full**, **Reindex**, or **Reuse** — to share main KV and indexer K across layers and reuse Top-K sparse-attention indices. In the decoder, a **Hierarchical Sparse Indexer** further restricts later indexing layers to a candidate pool constructed by the first Full Mode layer, bounding deeper indexer cost independently of context length. Combined with **FP4 main KV caching** (E2M1 format, one E4M3 scale per 16 channels), these designs reduce the global KV cache footprint to **890 bytes per token** — roughly **1/4** of DeepSeek-V4-Flash.

**Additional architectural components** include Single-Pass mHC (revised residual-stream mixing with an efficient Mega-mHC kernel), Engram conditional memory (196B parameters, sparsely accessed via token-based lookup), and DSpark speculative decoding (semi-autoregressive draft generation with confidence-scheduled verification). The model uses 1 shared expert and 384 routed experts per MoE layer, activating 6 routed experts per token.

**Multimodal architecture.** A vision encoder (DeepSeek-ViT, trained from scratch with 2D-RoPE and 3×3 pixel-unshuffle downsampling) and a two-layer MLP projector convert images into visual embeddings, processed jointly with text embeddings from the start of language-model pre-training.

**Pre-training.** DeepSeek-V4.1-Flash is trained from scratch on a multimodal corpus comprising **45T tokens**, with sparse attention trained at a sequence length of 64K and context extended to 1M tokens at 34T tokens.

**Post-training.** The post-training recipe follows the standard SFT → RL → on-policy distillation (OPD) paradigm without algorithmic modifications. All substantive changes lie instead in the data pipeline: large-scale automated synthesis of agent tasks and environments with progressive scaling of data, tasks, and rollouts. The model supports a **continuously controllable reasoning effort** setting (integer 1–100) that trades inference cost for accuracy.

<div align="center">
  <img src="https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/resolve/main/assets/dsv41_agentic_performance.png" width="48%" alt="DeepSeek-V4.1-Flash agentic benchmark performance" style="display: inline-block; margin: 0 1%;" />
  <img src="https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/resolve/main/assets/dsv41_kv_cache.png" width="48%" alt="Global KV cache size per token across DeepSeek generations" style="display: inline-block; margin: 0 1%;" />
</div>

*Figure 1. (a) Performance of DeepSeek-V4.1-Flash and counterparts on agentic benchmarks. (b) Global KV cache size per token (bytes) across generations of DeepSeek models. DeepSeek-V4.1-Flash achieves approximately 4-fold and 437-fold reductions relative to DeepSeek-V4-Flash and DeepSeek-V1, respectively.*

## Evaluation Results

### Base Model

All base models are evaluated in our internal framework under the same evaluation settings. Scores within 0.3 of each other are considered equivalent.

<div align="center">

| Benchmark (Metric) | # Shots | DeepSeek-V4-Flash-Base | DeepSeek-V4-Pro-Base | DeepSeek-V4.1-Flash-Base |
| :--- | :---: | :---: | :---: | :---: |
| Architecture | — | MoE | MoE | MoE |
| # Backbone Params | — | 284B | 1.6T | 552B |
| # Activated Params | — | 13B | 49B | 8B / 16B |
| **World Knowledge** | | | | |
| AGIEval (EM) | 3–5-shot | 83.9 | **84.4** | 83.4 |
| MMLU-Pro (EM) | 5-shot | 68.3 | 73.5 | **74.1** |
| C-Eval (EM) | 5-shot | 92.1 | **93.1** | 92.1 |
| MultiLoKo (LLM-Judge) | 5-shot | 42.6 | **50.9** | 45.5 |
| SimpleQA-Verified (EM) | 25-shot | 30.1 | **55.2** | 42.3 |
| SuperGPQA (EM) | 5-shot | 46.5 | **53.9** | 53.1 |
| **Language & Reasoning** | | | | |
| BBH (EM) | 3-shot | 86.9 | **87.5** | 86.1 |
| BBEH (EM) | 1-shot | 25.4 | **29.8** | 27.2 |
| DROP (F1) | 1-shot | **88.6** | **88.7** | 87.9 |
| HellaSwag (EM) | 0-shot | 85.7 | **88.0** | 87.2 |
| **Code & Math** | | | | |
| BigCodeBench (Pass@1) | 3-shot | 56.8 | 59.2 | **60.6** |
| HumanEval (Pass@1) | 0-shot | 69.5 | 76.8 | **79.4** |
| GSM8K (EM) | 8-shot | 90.8 | 92.6 | **93.0** |
| MATH (EM) | 4-shot | 57.4 | **64.5** | 61.1 |
| MGSM (EM) | 8-shot | **85.7** | 84.4 | 80.2 |
| **Long Context** | | | | |
| LongBench-V2 (EM) | 1-shot | 44.7 | **51.5** | 45.2 |
| **Multimodal** | | | | |
| MMMU-Pro (EM) | 4-shot | — | — | 56.5 |
| CVBench (EM) | 4-shot | — | — | 77.9 |
| DocVQA (LLM-Judge) | 4-shot | — | — | 95.6 |
| RefCOCO-avg (Acc@0.5) | 0-shot | — | — | 86.0 |

</div>

### Instruct Model

DeepSeek-V4.1-Flash supports a continuously controllable reasoning effort from 1 to 100. All instruct results below use the maximum effort setting (`reasoning_effort=100`). Evaluations use `temperature=1.0, top_p=0.95`.

For code agent benchmarks (Terminal-Bench 2.1/3.0/4.0, DeepSWE v1.1, NL2Repo-Bench, ProgramBench), the model is evaluated with the Minimal mode of DeepSeek Harness and a 1M-token context window. To align with official setup requirements, the mini-SWE harness is used for DeepSWE v1.1, and the Claude Code harness for SEC-Bench Pro. Visual agent benchmarks (Chartography, BabyVision, ZeroBench) use the Claude Code harness with a 512k-token context window. Agent's Last Exam and AutomationBench use their official scaffolds. All agentic evaluations use `temperature=1.0, top_p=0.95`.

#### Comparison with frontier models (Max reasoning effort)

<div align="center">

| Benchmark (Metric) | Opus-5.0 | GPT-5.6 Sol | K3 | GLM-5.3 | DS-V4-Pro | DS-V4-Flash | DS-V4.1-Flash |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Reasoning** | | | | | | | |
| GPQA Diamond (Pass@1) | 93.4 | **94.1** | 92.9 | 88.1 | 92.4 | 89.9 | 90.9 |
| HLE (Pass@1) | **56.3** | 44.5 | 43.5 | 42.0† | 42.7† | 37.8† | 36.8 (39.1†) |
| Codeforces (Rating) | — | — | — | — | 3348 | 3289 | **3471** |
| MathArena Apex (Pass@1) | — | — | **65.6** | — | 65.3 | 58.6 | **65.6** |
| **Agentic** | | | | | | | |
| Terminal-Bench 2.1 (Pass@1) | 89.1 | 88.8 | 88.3 | 88.2 | 87.9 | 82.7 | **90.6** |
| Terminal-Bench 3.0 (Pass@1) | **43.3** | 34.4 | 17.7 | 28.3 | 11.8 | 7.6 | 30.0 |
| Terminal-Bench 4.0 (Pass@1) | **51.8** | 39.9 | 12.6 | 37.9 | 12.4 | 7.0 | 31.2 |
| DeepSWE v1.1 (Resolved) | 74.0 | 73.0 | 67.5 | 66.9 | 62.7 | 54.4 | **74.2** |
| ProgramBench (Almost@1) | **37.0** | 23.0 | 17.5 | 19.0 | 15.5 | — | 20.3 |
| NL2Repo-Bench (Score) | **75.3** | 56.8 | 58.0 | 58.0 | 61.5 | 54.2 | 64.0 |
| CyberGym (Pass@1) | — | 84.5 | 80.0 | 84.5 | 83.3 | 76.7 | **88.1** |
| SEC-Bench Pro (Pass@1) | — | **74.3** | — | — | 56.4 | 30.9 | 62.8 |
| ExploitGym (Pass@1) | 22.1 | **33.7** | — | 15.0 | 5.4 | 1.8 | 15.3 |
| HLE w/ tools (Pass@1) | 63.6 | — | 59.8 | 62.5 | 60.0 | 51.5 | **63.9** |
| AutomationBench (Pass@1) | 50.3 | 45.8 | 46.7 | 48.8 | 43.2 | 37.7 | **54.8** |
| Agent's Last Exam (Pass@1) | 28.6 | 26.7 | 27.6 | 28.5 | 25.7 | 25.2 | **31.8** |
| Chartography w/ tools (Pass@1) | **84.0** | 79.9 | 68.1 | — | — | — | 78.9 |
| BabyVision w/ tools (Pass@1) | **94.1** | 88.9 | 85.7 | — | — | — | 89.6 |
| ZeroBench-main w/ tools (Pass@5) | 52.0 | **53.0** | 41.0 | — | — | — | 49.0 |

</div>

*† Text-only subset of HLE.*

#### Performance across agent scaffolds (DeepSWE v1.1 and Terminal-Bench 2.1, Max reasoning effort)

All scaffolds use N=8 samples per task on DeepSWE v1.1 and N=3 on Terminal-Bench 2.1, with Linux containers, `temperature=1.0`, `top_p=0.95`, a 1M-token context limit, and max_steps=500 per agent. Terminal-Bench 2.1 is evaluated without network access.

<div align="center">

| Benchmark (Metric) | Claude Code | Codex | OpenCode | Pi | mini-SWE | DSH Minimal | DSH Standard | DSH PTC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| DeepSWE v1.1 (Resolved) | 69.8 | 65.6 | 65.5 | 66.2 | 74.2 | 72.6 | 70.5 | 67.6 |
| Terminal-Bench 2.1 (Pass@1) | 88.0 | 84.1 | 85.0 | 86.1 | 90.3 | 90.6 | 85.8 | 85.8 |

</div>

## Prompt Encoding

This release does not include a Jinja-format chat template. The [`encoding`](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/encoding/README.md) folder contains a self-contained Python reference implementation (`encoding.py`) with test cases for multi-turn conversations, tool calling, thinking mode, numeric reasoning effort, mid-conversation system messages, and interleaved image content.

For production use, we additionally release [deepseek-recipe](https://github.com/deepseek-ai/deepseek-recipe), a set of Rust libraries with Python bindings that provides the same prompt format as a maintained, protocol-aware toolkit. It converts Messages, Chat Completions, and Responses API requests into the Conversation format, encodes them into DeepSeek V4 and V4.1 prompts or token IDs, and parses model output back into complete or streamed responses — covering thinking, tool calls, images, and generation settings. Model inference, tool execution, and HTTP transport are left to the caller.

## Minimal Inference

Please refer to the [`inference`](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/inference/README.md) folder for instructions on weight conversion and running inference locally.

**Recommended sampling parameters:**

| Parameter | Value |
| :--- | :--- |
| `temperature` | 1.0 |
| `top_p` | 0.95 or 1.0 |
| `context_window` | 1M tokens |
| `max_tokens` | ≥ 256K |

## Reproducing DeepSWE Benchmark Results

The [`evaluation`](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/evaluation/README.md) folder contains step-by-step instructions for reproducing the DeepSWE v1.1 benchmark results, covering both the `dsh-minimal` agent and the official `mini-swe-agent`. The patch required to integrate `dsh-minimal` with [Pier](https://github.com/datacurve-ai/pier) is also included there.

## License

This repository and the model weights are licensed under the [MIT License](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/LICENSE).

## Citation

```bibtex
@misc{deepseekai2026deepseekv41flash,
      title={DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression},
      author={DeepSeek-AI},
      year={2026},
}
```

## Contact

If you have any questions, please raise an issue or contact us at [service@deepseek.com](mailto:service@deepseek.com).
