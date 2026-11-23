---
license: other
license_name: kimi-k3.1-pro
license_link: https://huggingface.co/KarLexAI/Kimi-K3.1-Pro-GGUF/blob/main/LICENSE
base_model: moonshotai/Kimi-K3.1-Pro
base_model_relation: quantized
library_name: gguf
pipeline_tag: text-generation
tags:
  - gguf
  - llama.cpp
  - quantized
  - 1-bit
  - 2-bit
  - kimi
  - moe
  - reasoning
---

<div align="center">

# Kimi K3.1 Pro · KLX GGUF

### 2.8 trillion parameters on one 8×H100 node. It still reasons.

![Format](https://img.shields.io/badge/format-GGUF-3d7be0) ![Runtime](https://img.shields.io/badge/runtime-stock%20llama.cpp-3d7be0) ![Fits](https://img.shields.io/badge/fits-one%208%C3%97H100%20node-3d7be0) ![AIME](https://img.shields.io/badge/AIME%202025-80%25%20at%20593%20GB-0891b2)

</div>

Kimi K3.1 Pro is 1.56 TB even as a lossless GGUF. **KLX-IQ1_S is 593 GB, about 1.7 bits per weight, and runs entirely
on the GPUs of a single 8×H100 node. It still solves 80% of AIME 2025.** Standard GGUF, stock llama.cpp, no fork.

## ✨ Highlights

- 🖥️ **The whole model on one node.** KLX-IQ1_S loads entirely into 8× H100 80 GB with 131K tokens of context:
  19 tokens/s generating, with no expert left on the CPU.
- 🧠 **It still thinks at 1.7 bits per weight.** KLX-IQ1_S scores 80.0% on AIME 2025, 91.0% on MATH-500 and 94.0% on
  IFEval.
- 📉 **Closer to the full model than a standard quant of the same size.** Mean KL divergence 14.5% lower at 710 GB and
  6.2% lower at 648 GB.
- 🔌 **Plain GGUF.** Only standard llama.cpp tensor types. Runs on upstream llama.cpp as it is.

## 📦 Pick your file

| Folder | Size | Mean KL vs. full model ↓ | Pick it for |
|---|---|---|---|
| [KLX-IQ1_S](https://huggingface.co/KarLexAI/Kimi-K3.1-Pro-GGUF/tree/main/KLX-IQ1_S) | **592.7 GB** | 0.106 | fitting on one 8×H100 node |
| [KLX-IQ1_M](https://huggingface.co/KarLexAI/Kimi-K3.1-Pro-GGUF/tree/main/KLX-IQ1_M) | **647.9 GB** | 0.084 | the middle ground |
| [KLX-IQ2_XXS](https://huggingface.co/KarLexAI/Kimi-K3.1-Pro-GGUF/tree/main/KLX-IQ2_XXS) | **709.9 GB** | 0.072 | the closest to the full model |

You need more memory than the file size, in GPU memory plus system RAM. The two larger files keep part of the experts
in system RAM on an 8×H100 node. Scores, speeds and how every number was measured:
[BENCHMARKS.md](https://huggingface.co/KarLexAI/Kimi-K3.1-Pro-GGUF/blob/main/BENCHMARKS.md).

## 🚀 Run it with two commands

```bash
hf download KarLexAI/Kimi-K3.1-Pro-GGUF --include "KLX-IQ1_S/*" --local-dir .
llama-server -m KLX-IQ1_S/Kimi-K3.1-Pro-KLX-IQ1_S-00001-of-00014.gguf -ngl 999 --fit off -c 131072 -np 4 --jinja --temp 1.0 --top-p 0.95
```

Then open http://localhost:8080 and chat. You need llama.cpp with Kimi K3.1 support
([#31779](https://github.com/ggml-org/llama.cpp/pull/31779), merged 6 Nov 2026). With less GPU memory, or for the larger
files, use `--fit on` in place of `-ngl 999 --fit off`, and llama.cpp decides what stays in system RAM.

### 🖼️ Images

Kimi K3.1 Pro also reads images. Download the vision projector (about 0.9 GB) and add `--mmproj`:

```bash
hf download KarLexAI/Kimi-K3.1-Pro-GGUF mmproj-F16.gguf --local-dir .
llama-server -m KLX-IQ1_S/Kimi-K3.1-Pro-KLX-IQ1_S-00001-of-00014.gguf --mmproj mmproj-F16.gguf -ngl 999 --fit off -c 131072 -np 4 --jinja --temp 1.0 --top-p 0.95
```

`mmproj-BF16.gguf` works the same way. Image input needs llama.cpp with Kimi K3.1 vision
([#31980](https://github.com/ggml-org/llama.cpp/pull/31980), merged 10 Nov 2026).

## 🧾 The fine print

- Post-training quantization of [moonshotai/Kimi-K3.1-Pro](https://huggingface.co/moonshotai/Kimi-K3.1-Pro). No
  fine-tuning. The vision encoder is in the separate mmproj files, unquantized (F16 and BF16), converted with
  upstream llama.cpp and tested with KLX-IQ1_S.
- Use is governed by the Kimi K3.1-Pro License: see [LICENSE](https://huggingface.co/KarLexAI/Kimi-K3.1-Pro-GGUF/blob/main/LICENSE).

<div align="center">

**Made by [KarLex AI](https://karlex.ai).** If these files save you memory, a ❤️ on this repo helps others find them.

<sub>Not affiliated with Moonshot AI.</sub>

</div>
