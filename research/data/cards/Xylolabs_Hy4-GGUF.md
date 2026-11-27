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

Keep `--ubatch-size` at 8192 or below; larger ubatches can give wrong output in this llama.cpp build.

## Accuracy

Mean KL divergence and top-1 agreement against the BF16 model on WikiText-2, chat and held-out text; Answers is a five-question check.

| Quant | Size | WikiText-2 KL | top-1 | Chat KL | top-1 | Held-out KL | top-1 | Answers |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BF16, flash attention off (part of WikiText-2) | 1541.7 GB | 0.0336 | 95.1% |  |  |  |  |  |
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
| One B200 | 192 GB | offload | 32K |
| Mac Studio M5 Ultra | 256 GB unified | `Hy4-IQ2_XXS`* (219.4 GB) | 64K |
| Mac Studio M5 Ultra | 512 GB unified | `Hy4-IQ3_S` (328.0 GB) | 512K |
| One B300 (HBM3e) | 288 GB | `Hy4-IQ2_XXS` (219.4 GB) | 256K |
| 2 x H200 | 282 GB | `Hy4-IQ2_XXS` (219.4 GB) | 256K |
| 4 x H200 | 564 GB | `Hy4-Q4_K_M` (464.1 GB) | 256K |
| 8 x H200 | 1,128 GB | `Hy4-Q8_0` (818.5 GB) | 1M |
| 4 x B200 | 768 GB | `Hy4-Q6_K` (638.3 GB) | 64K |
| 8 x B200 | 1,536 GB | `Hy4-Q8_0` (818.5 GB) | 1M |

\* Needs the macOS GPU memory limit raised.

Offload: `llama-server -m FILE --n-cpu-moe 78` keeps the expert weights in system RAM.

## License and notices

These files are under the Tencent Hy License, Version 1.0, copied in `LICENSE`. We converted the weights to GGUF and quantized them.

## Updates

- 2026-11-22: Added Q6_K (638.3 GB) and IQ2_XXS (219.4 GB).
- 2026-11-21: Added IQ3_S and the importance matrices; accuracy re-measured on WikiText-2, chat and held-out text.
- 2026-11-20: First release: Q8_0 and Q4_K_M with BF16 and Q8_0 vision projectors.
