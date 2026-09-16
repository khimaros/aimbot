---
license: apache-2.0
tags:
  - conversational
  - prismml
  - bonsai
  - 1-bit
---

# 1-bit Bonsai 27B — Unpacked FP16 Safetensors

FP16 safetensors (HuggingFace format) of the 1-bit Bonsai 27B model. This repo exists for users who want to run Bonsai with stock HuggingFace tooling or frameworks that don't yet support 1-bit weights natively. The 1-bit hybrid-attention kernels are currently in our forks of [MLX](https://github.com/PrismML-Eng/mlx), [mlx-swift](https://github.com/PrismML-Eng/mlx-swift), and [llama.cpp](https://github.com/PrismML-Eng/llama.cpp) — once they land upstream, this unpacked version will no longer be needed.

> **We strongly recommend using the native 1-bit models instead.** The 1-bit format is where all the benefits of Bonsai come from — a 14.2x memory reduction to 3.9 GB, interactive decoding on everyday laptops (44 tok/s on an M5 Pro), and the first 27B-class model that runs on a phone (11 tok/s on iPhone 17 Pro Max). This unpacked FP16 version is full-size (~54 GB) and does not provide any of those advantages.

For the optimized 1-bit release models (recommended):

- **[Bonsai-27B-mlx-1bit](https://huggingface.co/prism-ml/Bonsai-27B-mlx-1bit)** — 1-bit MLX for Apple Silicon (Mac, iPhone, iPad)
- **[1-bit GGUF (Q1_0_g128)](https://huggingface.co/prism-ml/Bonsai-27B-gguf)** for llama.cpp (CUDA, Metal, CPU)

For the quality-oriented variant:

- **[Ternary-Bonsai-27B-mlx-2bit](https://huggingface.co/prism-ml/Ternary-Bonsai-27B-mlx-2bit)** — Ternary Bonsai 27B (~7.2 GB, 95% of FP16) for laptops and GPUs
