---
license: apache-2.0
base_model:
- baidu/ERNIE-5.5-Flash-Preview
base_model_relation: quantized
library_name: gguf
pipeline_tag: text-generation
language:
- en
- zh
tags:
- gguf
- llama-cpp
- quantized
- moe
---

<div align="center">

<img class="block dark:hidden mx-auto" src="https://raw.githubusercontent.com/XylolabsInc/tensix-bfp-gptq/main/assets/xylolabs-lockup.svg" alt="Xylolabs" width="256" height="40">
<img class="hidden dark:block mx-auto" src="https://raw.githubusercontent.com/XylolabsInc/tensix-bfp-gptq/main/assets/xylolabs-lockup-dark.svg" alt="Xylolabs" width="256" height="40">

<h1>ERNIE-5.5-Flash-Preview GGUF</h1>

</div>

GGUF files of Baidu's [ERNIE-5.5-Flash-Preview](https://huggingface.co/baidu/ERNIE-5.5-Flash-Preview) for llama.cpp, without the DSpark draft head.

Needs llama.cpp built from pull request [#31925](https://github.com/ggml-org/llama.cpp/pull/31925) (commit `7d9d5c35`).

## Files

| File | Parts | Size |
|---|---:|---:|
| `ERNIE-5.5-Flash-Preview-MXFP4-BF16.gguf` (original weights: routed experts MXFP4 as released; norms and small tensors F32; every other tensor BF16, the FP8 values exactly) | 5 | 162.20 GB |
| `ERNIE-5.5-Flash-Preview-Q3_K_M.gguf` | 5 | 138.51 GB |
| `ERNIE-5.5-Flash-Preview-IQ3_XXS.gguf` | 5 | 127.23 GB |
| `ERNIE-5.5-Flash-Preview-Q2_K.gguf` | 5 | 108.21 GB |
| `ERNIE-5.5-Flash-Preview-IQ2_XXS.gguf` | 5 | 82.84 GB |
| `ERNIE-5.5-Flash-Preview-IQ1_M.gguf` | 5 | 72.97 GB |

## How to run

```sh
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
git fetch origin pull/31925/head:ernie5_5 && git checkout 7d9d5c35117dc67a70fb0ec6e0fb9e104633c158
cmake -B build -DGGML_CUDA=ON && cmake --build build -j --target llama-server
./build/bin/llama-server -m ERNIE-5.5-Flash-Preview-IQ2_XXS-00001-of-00005.gguf --jinja --chat-template-file chat_template.jinja -ngl 99 -c 32768
```

## Accuracy

Against the original weights.

| Quant | Size | WikiText-2 KL | top-1 | Chat KL | top-1 | Held-out KL | top-1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Q3_K_M | 138.51 GB | 0.159302 | 88.93% | 0.034455 | 93.82% | 0.064832 | 91.10% |
| IQ3_XXS | 127.23 GB | 0.225180 | 86.94% | 0.050677 | 92.61% | 0.101372 | 87.88% |
| Q2_K | 108.21 GB | 0.451899 | 80.26% | 0.099800 | 88.94% | 0.197415 | 83.57% |
| IQ2_XXS | 82.84 GB | 0.781156 | 72.97% | 0.251677 | 84.04% | 0.370447 | 78.00% |
| IQ1_M | 72.97 GB | 1.119074 | 66.62% | 0.404082 | 79.51% | 0.622966 | 70.45% |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://huggingface.co/Xylolabs/ERNIE-5.5-Flash-Preview-GGUF/resolve/main/accuracy-mean-kl-dark.png">
  <img src="https://huggingface.co/Xylolabs/ERNIE-5.5-Flash-Preview-GGUF/resolve/main/accuracy-mean-kl.png" alt="Mean KL divergence by quant file size">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://huggingface.co/Xylolabs/ERNIE-5.5-Flash-Preview-GGUF/resolve/main/accuracy-top1-dark.png">
  <img src="https://huggingface.co/Xylolabs/ERNIE-5.5-Flash-Preview-GGUF/resolve/main/accuracy-top1.png" alt="Top-1 agreement by quant file size">
</picture>

## Which file for your hardware

Estimates from file size plus KV cache memory, not measured speeds.

| Hardware | Memory | File | Context (f16 KV) |
|---|---|---|---:|
| RTX PRO 6000 Blackwell (GDDR7) | 96 GB | `ERNIE-5.5-Flash-Preview-IQ2_XXS-00001-of-00005.gguf` (82.8 GB) | 32K |
| DGX Spark | 128 GB unified | `ERNIE-5.5-Flash-Preview-Q2_K-00001-of-00005.gguf` (108.2 GB) | 256K |
| Mac Studio M5 Max | 128 GB unified | `ERNIE-5.5-Flash-Preview-Q2_K-00001-of-00005.gguf` (108.2 GB) | 256K |
| One H200 (HBM3e) | 141 GB | `ERNIE-5.5-Flash-Preview-Q2_K-00001-of-00005.gguf` (108.2 GB) | 1M |
| One B200 | 192 GB | `ERNIE-5.5-Flash-Preview-MXFP4-BF16-00001-of-00005.gguf` (162.2 GB) | 256K |
| Mac Studio M5 Ultra | 256 GB unified | `ERNIE-5.5-Flash-Preview-MXFP4-BF16-00001-of-00005.gguf` (162.2 GB) | 1M |
| One B300 (HBM3e) | 288 GB | `ERNIE-5.5-Flash-Preview-MXFP4-BF16-00001-of-00005.gguf` (162.2 GB) | 1M |
| Mac Studio M5 Ultra | 512 GB unified | `ERNIE-5.5-Flash-Preview-MXFP4-BF16-00001-of-00005.gguf` (162.2 GB) | 1M |

Offload: `--n-cpu-moe 43` keeps the expert weights in system RAM: 97.9 GB of them with `ERNIE-5.5-Flash-Preview-Q2_K`, an estimate of the RAM it needs.

## License

Apache License 2.0 (`LICENSE`, from Baidu's release); we converted the weights to GGUF and quantized them.

## Updates

- 2026-11-27: Added IQ1_M.
- 2026-11-27: Added IQ3_XXS.
- 2026-11-27: Added IQ2_XXS.
