---
license: apache-2.0
tags:
  - conversational
  - prismml
  - bonsai
  - ternary
---

# Ternary Bonsai 27B — Unpacked FP16 Safetensors

FP16 safetensors (HuggingFace format) of the Ternary Bonsai 27B model. This repo exists for users who want to run Ternary Bonsai with stock HuggingFace tooling or frameworks that don't yet support the packed ternary format. The 2-bit hybrid-attention kernels are currently in our forks of [MLX](https://github.com/PrismML-Eng/mlx), [mlx-swift](https://github.com/PrismML-Eng/mlx-swift), and [llama.cpp](https://github.com/PrismML-Eng/llama.cpp) — once they land upstream, this unpacked version will no longer be needed.

> **We strongly recommend using the natively packed models instead.** The packed format is where all the benefits of Bonsai come from — a 7.2 GB deployed footprint (down from 54 GB), 95% of FP16 intelligence retained, and interactive decoding on everyday laptops (26 tok/s on an M5 Pro). This unpacked FP16 version is full-size and does not provide any of those advantages.

For the optimized ternary release models (recommended):

- **[Ternary-Bonsai-27B-mlx-2bit](https://huggingface.co/prism-ml/Ternary-Bonsai-27B-mlx-2bit)** — Ternary MLX for Apple Silicon
- **[Ternary GGUF (Q2_0_g128)](https://huggingface.co/prism-ml/Ternary-Bonsai-27B-gguf)** for llama.cpp (CUDA, Metal, CPU)

For the phone-class variant:

- **[Bonsai-27B-mlx-1bit](https://huggingface.co/prism-ml/Bonsai-27B-mlx-1bit)** — 1-bit Bonsai 27B (~3.9 GB), fits an iPhone 17 Pro Max
