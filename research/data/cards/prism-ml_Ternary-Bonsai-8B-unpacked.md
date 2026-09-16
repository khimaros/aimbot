---
license: apache-2.0
tags:
  - prismml
  - bonsai
  - ternary
---

# Ternary-Bonsai-8B — Unpacked FP16 Safetensors

FP16 safetensors (HuggingFace format) of the ternary Bonsai-8B model. This repo exists for users who want to run Ternary Bonsai with stock HuggingFace tooling or frameworks that don't yet support any of the packed ternary format. The MLX 2-bit format is currently the only packed format available; more formats for other backends are coming soon.

> **We strongly recommend using the natively packed models instead.** The packed format is where all the benefits of Bonsai come from — up to 9x memory reduction, 5x faster inference, and lower energy per token. This unpacked FP16 version is full-size and does not provide any of those advantages.

For the optimized ternary release model (recommended):

- **[Ternary-Bonsai-8B MLX 2-bit](https://huggingface.co/prism-ml/Ternary-Bonsai-8B-mlx-2bit)** — Ternary MLX for Apple Silicon
