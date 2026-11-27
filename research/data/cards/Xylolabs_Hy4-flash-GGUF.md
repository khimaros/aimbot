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
[![Formats](https://img.shields.io/badge/formats-Q8__0%20%2F%20Q6__K%20%2F%20Q5__K__M%20%2F%20Q4__K__M%20%2F%20Q4__K__S%20%2F%20NVFP4%20%2F%20IQ4__XS%20%2F%20Q3__K__M%20%2F%20IQ3__M%20%2F%20IQ3__XXS%20%2F%20IQ2__M%20%2F%20IQ2__XXS-5B2C83)](#files)
[![License](https://img.shields.io/badge/license-Tencent%20Hy%20License-green)](https://huggingface.co/Xylolabs/Hy4-flash-GGUF/blob/main/LICENSE)
[![Code](https://img.shields.io/badge/code-llama.cpp%20PR%2032517-black)](https://github.com/ggml-org/llama.cpp/pull/32517)

</div>

GGUF quants of [tencent/Hy4-flash](https://huggingface.co/tencent/Hy4-flash) (220B parameters, 12B active) for llama.cpp on CUDA, Metal or CPU. The DFly2 speculative-decoding drafter is not included.

## Files

| Quant | Parts | Size |
|---|---:|---:|
| Q8_0 | 2 | 228.9 GB |
| Q6_K | 2 | 193.3 GB |
| Q5_K_M | 2 | 176.7 GB |
| Q4_K_M | 2 | 161.2 GB |
| Q4_K_S | 2 | 155.5 GB |
| NVFP4 | 2 | 154.9 GB |
| Q4M-E5 | 2 | 141.4 GB |
| Q4M-E4 | 2 | 133.5 GB |
| IQ4_XS-E4 | 2 | 122.6 GB |
| Q3_K_M-E4 | 2 | 114.2 GB |
| IQ3_M-E4 | 2 | 108.1 GB |
| IQ3_XXS-E4 | 2 | 100.5 GB |
| IQ2_M-E4 | 2 | 91.9 GB |
| IQ2_XXS-E4 | 2 | 83.1 GB |
| `mmproj-Hy4-flash-BF16.gguf` (vision) | 1 | 1.0 GB |
| `mmproj-Hy4-flash-Q8_0.gguf` (vision) | 1 | 0.8 GB |
| `Hy4-flash.imatrix.gguf` | 1 | 0.8 GB |

Part 2 of each quant is the Engram table: FP8 E4M3, or Q5_0 in `-E5` files and IQ4_NL in `-E4` files (MXFP4 in `IQ2_XXS-E4`). NVFP4 is for NVIDIA Blackwell GPUs.

## How to run

Hy4-flash support is llama.cpp pull request [#32517](https://github.com/ggml-org/llama.cpp/pull/32517) until it is merged. Keep both parts of a quant in one folder and pass part 1:

```sh
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
git fetch origin pull/32517/head:hy4-flash && git checkout hy4-flash
cmake -B build -DCMAKE_BUILD_TYPE=Release        # add -DGGML_CUDA=ON for NVIDIA GPUs
cmake --build build -j --target llama-cli llama-server

./build/bin/llama-cli -m Hy4-flash-Q4_K_M-00001-of-00002.gguf \
  --override-tensor '^per_layer_token_embd\.weight$=CPU' --load-mode mmap --lazy-mode on \
  -ngl 99 --jinja -c 8192
```

The `--override-tensor` and `--load-mode` flags keep the Engram table in system RAM and read only the rows a prompt needs.

## Accuracy

Mean KL divergence and top-1 agreement against the BF16 model on WikiText-2, chat and held-out text; Answers is a five-question check.

| Quant | Size | WikiText-2 KL | top-1 | Chat KL | top-1 | Held-out KL | top-1 | Answers |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BF16, flash attention off | 375.4 GB | 0.1152 | 89.8% | 0.1987 | 89.0% | 0.0818 | 91.7% |  |
| Q8_0 / E4M3 | 228.9 GB | 0.1450 | 88.3% | 0.2483 | 87.5% | 0.1051 | 90.3% | 5/5 |
| Q6_K / E4M3 | 193.3 GB | 0.1458 | 87.9% | 0.2486 | 87.2% | 0.0998 | 90.4% | 5/5 |
| Q5_K_M / E4M3 | 176.7 GB | 0.1664 | 87.5% | 0.2705 | 86.6% | 0.1127 | 89.5% | 5/5 |
| AngelSlim Q4_K_M | 168.3 GB | 0.2161 | 85.1% | 0.3335 | 84.8% | 0.1384 | 88.7% |  |
| Q4_K_M / E4M3 | 161.2 GB | 0.2123 | 85.1% | 0.3205 | 85.3% | 0.1444 | 88.5% | 5/5 |
| Q4_K_S / E4M3 | 155.5 GB | 0.2202 | 84.9% | 0.3498 | 85.1% | 0.1489 | 88.2% | 5/5 |
| AngelSlim Q3_K | 155.4 GB | 0.2969 | 82.4% | 0.4543 | 82.2% | 0.2109 | 86.1% |  |
| NVFP4 / E4M3 | 154.9 GB | 0.2511 | 83.8% | 0.4033 | 83.3% | 0.1724 | 87.3% | 5/5 |
| Q4_K_M / Q5_0 | 141.4 GB | 0.2235 | 85.0% | 0.3586 | 85.1% | 0.1416 | 88.9% | 5/5 |
| AngelSlim IQ2_AH | 135.0 GB | 0.7328 | 71.4% | 1.0025 | 73.8% | 0.5515 | 76.6% |  |
| Q4_K_M / IQ4_NL | 133.5 GB | 0.2333 | 85.0% | 0.3514 | 84.4% | 0.1556 | 88.3% | 5/5 |
| IQ4_XS / IQ4_NL | 122.6 GB | 0.2362 | 84.4% | 0.3671 | 84.3% | 0.1706 | 87.7% | 5/5 |
| Q3_K_M / IQ4_NL | 114.2 GB | 0.3393 | 81.0% | 0.5192 | 81.2% | 0.2446 | 84.8% | 5/5 |
| IQ3_M / IQ4_NL | 108.1 GB | 0.4028 | 79.4% | 0.5664 | 79.8% | 0.3105 | 82.8% | 5/5 |
| IQ3_XXS / IQ4_NL | 100.5 GB | 0.4698 | 77.3% | 0.6502 | 78.6% | 0.3389 | 81.4% | 5/5 |
| IQ2_M / IQ4_NL | 91.9 GB | 0.6412 | 73.3% | 0.8604 | 74.9% | 0.4699 | 78.2% | 5/5 |
| IQ2_XXS + IQ2_S / MXFP4 | 83.1 GB | 0.8349 | 69.3% | 1.1280 | 72.1% | 0.6276 | 75.1% | 5/5 |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://huggingface.co/Xylolabs/Hy4-flash-GGUF/resolve/main/accuracy-by-size-dark.png">
  <img src="https://huggingface.co/Xylolabs/Hy4-flash-GGUF/resolve/main/accuracy-by-size.png" alt="Hy4-flash-GGUF mean KL divergence">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://huggingface.co/Xylolabs/Hy4-flash-GGUF/resolve/main/top1-by-size-dark.png">
  <img src="https://huggingface.co/Xylolabs/Hy4-flash-GGUF/resolve/main/top1-by-size.png" alt="Hy4-flash-GGUF top-1 accuracy">
</picture>

## Which file for your hardware

| Hardware | Memory | File | Context |
|---|---|---|---:|
| RTX 4090 / RTX 3090 | 24 GB | offload | 32K |
| RTX 5090 | 32 GB | offload | 32K |
| RTX 6000 Ada, or 2 x 24 GB | 48 GB | offload | 32K |
| One H100 | 80 GB | `Hy4-flash-IQ3_XXS-E4` (100.5 GB, 64.9 GB on the GPU) | 128K |
| RTX PRO 6000 Blackwell (GDDR7) | 96 GB | `Hy4-flash-Q3_K_M-E4` (114.2 GB, 78.6 GB on the GPU) | 128K |
| DGX Spark | 128 GB unified | `Hy4-flash-IQ3_M-E4` (108.1 GB) | 128K |
| Mac Studio M5 Max | 128 GB unified | `Hy4-flash-IQ2_M-E4` (91.9 GB) | 64K |
| One H200 (HBM3e) | 141 GB | `Hy4-flash-Q5_K_M` (176.7 GB, 113.4 GB on the GPU) | 256K |
| One B200 | 192 GB | `Hy4-flash-Q6_K` (193.3 GB, 129.9 GB on the GPU) | 1M |
| Mac Studio M5 Ultra | 256 GB unified | `Hy4-flash-Q5_K_M` (176.7 GB) | 512K |
| Mac Studio M5 Ultra | 512 GB unified | `Hy4-flash-Q8_0` (228.9 GB) | 1M |
| One B300 (HBM3e) | 288 GB | `Hy4-flash-Q8_0` (228.9 GB, 165.5 GB on the GPU) | 1M |

Offload: `llama-server -m FILE --n-cpu-moe 42` keeps the expert weights in system RAM.

## License and notices

These files are under the Tencent Hy License, Version 1.0, copied in `LICENSE`. We converted the weights to GGUF and quantized them.

## Updates

- 2026-11-22: NVFP4 replaced by a more accurate file; seven smaller files removed; smaller-Engram files renamed (-E4, -E5).
- 2026-11-22: Added IQ2_XXS-E4 to IQ4_XS-E4 and NVFP4; accuracy re-measured against a rebuilt BF16 reference.
- 2026-11-20: First release: Q8_0 to IQ2_M, Q4M-E5, Q4M-E4, the importance matrix and two vision projectors.
