---
base_model: IFM/K2-Horizon-3.7B
language:
  - en
license: apache-2.0
tags:
  - gguf
  - quantized
  - llama.cpp
  - k2-horizon
  - causal-lm
  - text-generation
pipeline_tag: text-generation
---

# K2-Horizon-3.7B — GGUF Quantizations

GGUF quantizations of [IFM/K2-Horizon-3.7B](https://huggingface.co/IFM/K2-Horizon-3.7B),
a dense 3.7B-parameter causal decoder (`K2HorizonForCausalLM`, `model_type: k2_horizon`).

Quantized by **NANI-Nithin** using a custom pipeline built on the
[MBZUAI-IFM llama.cpp fork](https://github.com/MBZUAI-IFM/llama.cpp) (branch `model/K2Horizon`).

> **Note on file naming:** IFM's official GGUF repo ships this model as
> `K2-Horizon-4B-BF16.gguf` (rounded name). Files in this repo are renamed
> to the `K2-Horizon-3.7B-*` convention for consistency.

---

## Model Details

| Property | Value |
|---|---|
| **Base model** | [IFM/K2-Horizon-3.7B](https://huggingface.co/IFM/K2-Horizon-3.7B) |
| **Architecture** | `K2HorizonForCausalLM` (`k2_horizon`) |
| **Parameters** | ~3.7B (dense decoder, no MoE) |
| **Original dtype** | BF16 |
| **BF16 GGUF size** | ~10.13 GB |
| **Source GGUF** | [IFM/K2-Horizon-3.7B-GGUF](https://huggingface.co/IFM/K2-Horizon-3.7B-GGUF) |
| **llama.cpp fork** | [MBZUAI-IFM/llama.cpp @ model/K2Horizon](https://github.com/MBZUAI-IFM/llama.cpp) |

> **Note:** These GGUFs carry the `k2-horizon` architecture token and require
> the MBZUAI-IFM fork (or upstream llama.cpp once support is merged) to run.
> Vanilla upstream llama.cpp (as of September 2026) does **not** support
> `K2HorizonForCausalLM`.

---

## Included Files

### Standard Quantizations

| File | Bits/Weight | Notes |
|---|---|---|
| `K2-Horizon-3.7B-BF16.gguf` | 16 bpw | Source quant, full precision |
| `K2-Horizon-3.7B-Q8_0.gguf` | 8 bpw | Near-lossless, recommended reference |
| `K2-Horizon-3.7B-Q6_K.gguf` | 6 bpw | Near-lossless K-quant |
| `K2-Horizon-3.7B-Q5_K_M.gguf` | 5 bpw | Best quality/size in the 5-bit range |
| `K2-Horizon-3.7B-Q5_K_S.gguf` | 5 bpw | Smaller 5-bit variant |
| `K2-Horizon-3.7B-Q5_1.gguf` | 5 bpw | Legacy 5-bit |
| `K2-Horizon-3.7B-Q5_0.gguf` | 5 bpw | Legacy 5-bit |
| `K2-Horizon-3.7B-Q4_K_M.gguf` | 4 bpw | **Recommended general use** |
| `K2-Horizon-3.7B-Q4_K_S.gguf` | 4 bpw | Smaller 4-bit K-quant |
| `K2-Horizon-3.7B-Q4_1.gguf` | 4 bpw | Legacy 4-bit |
| `K2-Horizon-3.7B-Q4_0.gguf` | 4 bpw | Legacy 4-bit |
| `K2-Horizon-3.7B-Q3_K_L.gguf` | 3 bpw | Large 3-bit K-quant |
| `K2-Horizon-3.7B-Q3_K_M.gguf` | 3 bpw | Medium 3-bit K-quant |
| `K2-Horizon-3.7B-Q3_K_S.gguf` | 3 bpw | Small 3-bit K-quant |
| `K2-Horizon-3.7B-Q2_K.gguf` | 2 bpw | Aggressive compression |
| `K2-Horizon-3.7B-Q2_K_S.gguf` | 2 bpw | Smaller 2-bit K-quant (imatrix-guided) |
| `K2-Horizon-3.7B-Q2_0.gguf` | 2.25 bpw | Group-64 2-bit |
| `K2-Horizon-3.7B-Q1_0.gguf` | 1.125 bpw | Maximum compression |

### IQ (Importance-Matrix) Quantizations

| File | Bits/Weight |
|---|---|
| `K2-Horizon-3.7B-IQ4_NL.gguf` | ~4 bpw |
| `K2-Horizon-3.7B-IQ4_XS.gguf` | ~4 bpw |
| `K2-Horizon-3.7B-IQ3_M.gguf` | ~3 bpw |
| `K2-Horizon-3.7B-IQ3_S.gguf` | ~3 bpw |
| `K2-Horizon-3.7B-IQ3_XS.gguf` | ~3 bpw |
| `K2-Horizon-3.7B-IQ3_XXS.gguf` | ~3 bpw |
| `K2-Horizon-3.7B-IQ2_M.gguf` | ~2 bpw |
| `K2-Horizon-3.7B-IQ2_S.gguf` | ~2 bpw |
| `K2-Horizon-3.7B-IQ2_XS.gguf` | ~2 bpw |
| `K2-Horizon-3.7B-IQ2_XXS.gguf` | ~2 bpw |
| `K2-Horizon-3.7B-IQ1_M.gguf` | 1.75 bpw |
| `K2-Horizon-3.7B-IQ1_S.gguf` | 1.56 bpw |

---

## Quantization Method

- **Source:** IFM's official BF16 GGUF (originally named `K2-Horizon-4B-BF16.gguf`, renamed here).
- **imatrix:** Computed from [Salesforce/wikitext](https://huggingface.co/datasets/Salesforce/wikitext)
  (`wikitext-2-raw-v1`, 500 rows) with **24 GPU layers offloaded** on an RTX 4060 Laptop (8 GB VRAM).
  Applied to all K-quants below Q6 and all IQ quants.
- **Fork:** [MBZUAI-IFM/llama.cpp](https://github.com/MBZUAI-IFM/llama.cpp), branch `model/K2Horizon`.

---

## Usage

> Requires the **MBZUAI-IFM llama.cpp fork** (`model/K2Horizon` branch).

```bash
git clone -b model/K2Horizon https://github.com/MBZUAI-IFM/llama.cpp
cd llama.cpp && cmake -B build -DGGML_CUDA=ON && cmake --build build --config Release

./build/bin/llama-cli \
  -m K2-Horizon-3.7B-Q4_K_M.gguf \
  -p "Hello, I am" \
  -n 128
```

---

## License

Weights are released under the same license as the original
[IFM/K2-Horizon-3.7B](https://huggingface.co/IFM/K2-Horizon-3.7B) model.
Please refer to the original repository for full license terms.

---

## Credits

- **Original model:** [MBZUAI IFM](https://huggingface.co/IFM)
- **Quantized by:** [NANI-Nithin](https://huggingface.co/NANI-Nithin)
- **Quantization tool:** [MBZUAI-IFM/llama.cpp](https://github.com/MBZUAI-IFM/llama.cpp)