---
base_model: Qwen/Qwen3.8-Flash-Next
base_model_relation: quantized
pipeline_tag: image-text-to-text
library_name: gguf
license: apache-2.0
tags:
  - gguf
  - gsq
  - rco
  - quantization
  - mixed-precision
  - ist-daslab
  - moe
  - multimodal
  - vision
---

<!--
  GSQ-RCO GGUF release card for Qwen3.8-Flash-Next.
  Mirrors the Qwen3.8-27B card.
  NB: the YAML block must remain the very first bytes of the file (HF requirement).
-->

<div align="center">

<a href="https://github.com/IST-DASLab"><img src="https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF/resolve/main/assets/banner.png" alt="GGUF, GSQ-RCO dynamic non-uniform quantization" width="100%"/></a>

<br/>

# Qwen3.8-Flash-Next &middot; GSQ-RCO GGUFs

**Non-uniform GGUF quantizations** of a 512-expert MoE, produced with **GSQ** and **RCO**, with a vision projector for multimodal use.

[![arXiv: GSQ](https://img.shields.io/badge/arXiv-GSQ_2604.18556-b31b1b?logo=arxiv&logoColor=white)](https://arxiv.org/abs/2604.18556)
[![arXiv: RCO](https://img.shields.io/badge/arXiv-RCO_2605.00649-b31b1b?logo=arxiv&logoColor=white)](https://arxiv.org/abs/2605.00649)
[![GSQ code](https://img.shields.io/badge/code-GSQ-181717?logo=github&logoColor=white)](https://github.com/IST-DASLab/GSQ)
[![RCO code](https://img.shields.io/badge/code-RCO-181717?logo=github&logoColor=white)](https://github.com/IST-DASLab/RCO)
[![DASLab](https://img.shields.io/badge/DASLab-GitHub-101048?logo=github&logoColor=white)](https://github.com/IST-DASLab)
[![license](https://img.shields.io/badge/license-apache--2.0-19a34a)](#license)

</div>

![Task average vs bit-width](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF/resolve/main/assets/plots/Qwen3.8-Flash-Next-task_avg_vs_avg_bit_width.png)

---

## Overview

This repository provides GGUF quantizations of **Qwen3.8-Flash-Next** at three sizes, together with the model's vision projector (`mmproj`) for multimodal use. In contrast to uniform quantization, which applies a single quantization type to all weight tensors, each model here assigns a separate quantization type to every tensor. The assignment is obtained by a gradient-based search that allocates precision according to per-tensor sensitivity, subject to a total size budget. The resulting files are standard GGUF and run unmodified in `llama.cpp`, Ollama, and LM Studio.

Flash-Next is a sparse mixture-of-experts model: **512 routed experts per layer across 48 layers**, of which 10 are active per token. The routed expert matrices dominate the parameter count, so they also dominate the size budget: 95% of the searchable weights live in the experts. The search therefore spends most of its freedom there, assigning a quantization type **per layer** (not per expert, which GGUF cannot express).

> **Method summary.** GSQ provides accurate low-bit scalar quantization of each tensor at a given quantization type; RCO assigns the per-tensor quantization types under a size budget. Together they yield a non-uniform GGUF at the requested size.

| Method | Description |
|---|---|
| **GSQ** (Gumbel-Softmax Quantization, [paper](https://arxiv.org/abs/2604.18556), [code](https://github.com/IST-DASLab/GSQ)) | Post-training scalar quantization that jointly learns the per-coordinate grid assignments and the per-group scales via a Gumbel-Softmax relaxation. GSQ closes most of the gap between scalar and vector quantization at 2 to 3 bits while remaining deployable in standard scalar formats such as GGUF. |
| **RCO** (Riemannian Constrained Optimization, [paper](https://arxiv.org/abs/2605.00649), [code](https://github.com/IST-DASLab/RCO)) | Assigns one of K quantization types to each of N tensors under a total size budget. The budget constraint is reformulated as a smooth Riemannian manifold in logit space, which permits gradient-based optimization directly on the task loss while enforcing the budget exactly, without constraint-specific hyperparameter tuning. |

Both methods were developed at the [Deep Algorithms and Systems Lab (DASLab)](https://github.com/IST-DASLab), Institute of Science and Technology Austria.

---

## Available files

Files follow the convention **`<model>-GSQ-RCO-<type>.gguf`**, where the suffix names the quantization class; the table lists each file's average bit-width over the transformer weights.

The `mmproj` file carries the vision encoder and projector at BF16; one copy serves all quantizations. Each quantized model ships as **two shards**. The second shard is identical across all three variants: it holds the per-layer n-gram embedding table (`per_layer_token_embd`, 51.2B parameters) at IQ4_NL. That table is a lookup, not a matmul weight, so it is held at a fixed 4.5 bpw in every build and excluded from the search. It is quantized in the evaluated models, not just the shipped ones.

| Directory | bpw | Shard 1 (weights) | Shard 2 (n-gram) | Total | Notes |
|---|---|---|---|---|---|
| `Q2_0/` | 2.40 | 37.6 GB | 28.8 GB | **66.4 GB** | Fastest; avoids lookup-table formats |
| `IQ2_XS/` | 2.50 | 39.2 GB | 28.8 GB | **68.0 GB** | Smallest at equal quality |
| `IQ3_XXS/` | 3.00 | 47.0 GB | 28.8 GB | **75.8 GB** | Recommended; matches the base model on AIME25 |
| `mmproj-Qwen3.8-Flash-Next-BF16.gguf` | 16 | 0.91 GB | n/a | **0.91 GB** | Vision encoder + projector, for multimodal use |

**Q2_0** is built for speed. It avoids the quantization formats that rely on large lookup tables: those formats pack more accuracy into a given bit-width, but decoding them costs real time, and on this model that cost dominates inference. Q2_0 delivers **3.4x the prompt throughput** and **1.9x lower end-to-end latency** than IQ2_XS at a slightly smaller file size, and its decode rate stays flat across workloads instead of varying with the content. The trade is a little quality: 89.07 task average against 89.16 for IQ2_XS, and 3.5 points below IQ3_XXS. Pick it when throughput matters most, and see [Performance](#performance) for the measurements.

The IQ3_XXS model is the strongest operating point: it matches the base model exactly on AIME25 (100.00) and is within 0.51 points on GPQA-Diamond and 1.14 on LiveCodeBench v6, at roughly one fifth of the BF16 size.

### Memory requirements

Only the first shard holds transformer weights and needs to be resident. The second shard is the n-gram lookup table: it is read sparsely, one row per token, so it can stay memory-mapped on disk and does not need to occupy VRAM. Run with `-lm mmap --lazy-mode on` to get this behaviour, plan for **shard 1 in VRAM**, and keep shard 2 on an SSD so the paging stays cheap.

| Model | Must be resident (shard 1) | Can stay on disk (shard 2) | Total download |
|---|---|---|---|
| `Q2_0` | 37.6 GB | 28.8 GB | 66.4 GB |
| `IQ2_XS` | 39.2 GB | 28.8 GB | 68.0 GB |
| `IQ3_XXS` | 47.0 GB | 28.8 GB | 75.8 GB |

Add headroom for the KV cache and the vision projector (0.91 GB) if used. Keeping the n-gram table in RAM rather than on disk removes the paging cost entirely and is worth it where memory allows.

---

## Performance

Measured with `llama.cpp` over 55 prompts spanning eleven categories (coding, humanities, math, QA, RAG, reasoning, STEM, writing, multilingual, summarization, roleplay).

| Model | Prompt t/s | Decode t/s | Avg latency |
|---|---|---|---|
| `Q2_0` | **367.49** | **93.79** | **6.70 s** |
| `IQ2_XS` | 108.19 | 70.30 | 12.68 s |

![Prefill throughput by category](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF/resolve/main/assets/plots/Qwen3.8-Flash-Next-prefill_throughput.png)

The gap comes from the quantization formats rather than the size: the two files differ by only 1.6 GB, and Q2_0 is the smaller of the two. Q2_0's decode rate is also far more stable across categories, 92.5 to 94.5 t/s (a 2.0 t/s spread), where IQ2_XS swings from 49.4 to 94.5 t/s (a 45.1 t/s spread), because the lookup cost varies with how much of each layer a request touches.

The prefill advantage is uneven, and largest where prompts are long: 9.6x on RAG, 6.8x on writing and 6.2x on coding. On short-prompt, reasoning-heavy categories the two are level or Q2_0 is marginally behind (0.8x to 0.9x on stem, math and reasoning), where prefill is too brief for the format's decoding cost to matter.

---

## Results

All models are evaluated against the **BF16** base model. We report the average over five zero-shot tasks (arc_easy, arc_challenge, hellaswag, winogrande, piqa), recovery (zero-shot average relative to BF16), and three reasoning and generation benchmarks: **AIME25**, **GPQA-Diamond**, and **LiveCodeBench v6**. Task average is the mean of the three. Sizes are the full download, including the n-gram shard; the bit-width column is the average over the transformer weights, which is what the search controls.

> **Reasoning effort.** These quantized models are primarily optimized for **xhigh reasoning effort**, and we recommend using them in that mode for best quality. The reported reasoning results should therefore be interpreted in that setting. At lower reasoning-effort levels, quantization-induced degradation can be larger than what is observed at xhigh, so the quality gap relative to the BF16 base model may increase.

| Variant | bpw | GB | ZS avg↑ | recovery | AIME25↑ | GPQA-D↑ | LCB v6↑ | Task avg↑ |
|---|---|---|---|---|---|---|---|---|
| BF16 | 16.00 | 354 | 76.94 | 100.0% | 100.00 | 91.92 | 87.43 | 93.12 |
| **GSQ-RCO Q2_0** | 2.40 | 66.4 | **78.00** | **101.4%** | 96.67 | 89.39 | 81.14 | 89.07 |
| **GSQ-RCO IQ2_XS** | 2.50 | 68.0 | 77.16 | 100.3% | 96.67 | 87.37 | 83.43 | 89.16 |
| **GSQ-RCO IQ3_XXS** | 3.00 | 75.8 | 77.23 | 100.4% | **100.00** | **91.41** | **86.29** | **92.57** |

All three models exceed the BF16 base on the zero-shot average (100.3% to 101.4%), which is common for careful low-bit quantization on these five tasks: the differences are within roughly one standard error and should be read as parity rather than improvement. The reasoning and generation benchmarks separate the models far more clearly.

At 3.00 bpw, IQ3_XXS reaches **99.4%** of the base model's task average (92.57 against 93.12) while being **4.7x smaller** (75.8 GB against 354 GB). It matches the base exactly on AIME25 (100.00), and trails by 0.51 on GPQA-Diamond and 1.14 on LiveCodeBench v6. At 2.50 bpw, IQ2_XS retains 95.7% of the task average at 68.0 GB, and the smallest build, Q2_0, holds 96.67 on AIME25 at 66.4 GB, a 5.3x reduction.

The two sub-2.5 bpw builds land within 0.1 points of each other on task average despite different allocations: Q2_0 is stronger on GPQA-Diamond (89.39 against 87.37) while IQ2_XS is stronger on LiveCodeBench v6 (83.43 against 81.14).

![AIME25 vs bit-width](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF/resolve/main/assets/plots/Qwen3.8-Flash-Next-aime25_vs_avg_bit_width.png)

![GPQA-Diamond vs bit-width](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF/resolve/main/assets/plots/Qwen3.8-Flash-Next-gpqa_diamond_vs_avg_bit_width.png)

![LiveCodeBench v6 vs bit-width](https://huggingface.co/ISTA-DASLab/Qwen3.8-Flash-Next-GSQ-RCO-GGUF/resolve/main/assets/plots/Qwen3.8-Flash-Next-lcb_vs_avg_bit_width.png)

---

## Usage

Both shards must be downloaded; `llama.cpp` loads the split automatically when given the first one.

### llama.cpp
```bash
# download (requires: pip install -U "huggingface_hub[cli]")
hf download <this-repo> --include "IQ3_XXS/*" --local-dir .

llama-cli -m IQ3_XXS/Qwen3.8-Flash-Next-GSQ-RCO-IQ3_XXS-00001-of-00002.gguf \
  -lm mmap --lazy-mode on \
  -p "Explain mixed-precision quantization." -ngl 99
```
`-lm mmap --lazy-mode on` keeps the n-gram table memory-mapped on disk instead of loading it into memory, which removes 28.8 GB from the resident footprint. See [Memory requirements](#memory-requirements).

### Vision (multimodal)
```bash
hf download <this-repo> mmproj-Qwen3.8-Flash-Next-BF16.gguf --local-dir .

llama-mtmd-cli -m IQ3_XXS/Qwen3.8-Flash-Next-GSQ-RCO-IQ3_XXS-00001-of-00002.gguf \
  --mmproj mmproj-Qwen3.8-Flash-Next-BF16.gguf \
  -lm mmap --lazy-mode on \
  --image photo.jpg -p "Describe this image."
```
The projector was converted directly from the base checkpoint and is shared by all three quantizations.

### Ollama
```bash
ollama run hf.co/<this-repo>   # pick the directory matching your memory budget
```

### LM Studio
Search the repo name, then pick a `GSQ-RCO-*` build from the file list.

---

## Quantization procedure

1. **Per-tensor database.** Each weight tensor is quantized at every candidate GGUF quantization type with GSQ, yielding a searchable database of quantized tensor variants.
2. **RCO search.** The budget-constrained Riemannian search assigns one quantization type per tensor such that the whole-file average bit-width meets the target.
3. **Assembly.** The selected per-tensor variants are stitched into a single standard GGUF file.

For this model the search covers **352 tensors**: the 304 dense tensors (attention, SSM projections, shared experts, embeddings, output head) and the 48 fused routed-expert matrices, one per layer. Two classes draw on separate quantization ladders, because the routed experts sit at a much lower bit-width than the dense path at any given budget. `ffn_down_exps` is excluded from the search and held at Q2_0. Its 640 rows are not divisible by 256, which rules out every block-256 K and I quant format; only the block-32 and block-64 types can represent it, so there is little to search over.

Reference implementations: **GSQ** at [IST-DASLab/GSQ](https://github.com/IST-DASLab/GSQ) and **RCO** at [IST-DASLab/RCO](https://github.com/IST-DASLab/RCO).

### Reproducibility artifacts

Each released GGUF ships the files needed to audit how it was built:

| File | Contents |
|---|---|
| `tensor-allocation/<model>.rco-allocation.txt` | The quantization type assigned to every tensor in that file, with a quant-type histogram and the target bit-width. This is the RCO search result, so the allocation can be inspected without opening the model. |

---

## Citation

If you use these models or methods, please cite both papers:

```bibtex
@article{gsq2026,
  title  = {GSQ: Highly-Accurate Low-Precision Scalar Quantization for LLMs via Gumbel-Softmax Sampling},
  author = {Dadgarnia, Alireza and Tabesh, Soroush and Nikdan, Mahdi and Helcig, Michael and Kurtic, Eldar and Kleinegger, Maximilian and Alistarh, Dan},
  journal= {arXiv preprint arXiv:2604.18556},
  year   = {2026}
}
@article{rco2026,
  title  = {Model Compression with Exact Budget Constraints via Riemannian Manifolds},
  author = {Helcig, Michael and Alistarh, Dan},
  journal= {arXiv preprint arXiv:2605.00649},
  year   = {2026}
}
```

---

## Acknowledgements

We thank [Verda](https://verda.com/) and Scientific Computing at the Institute of Science and Technology Austria for providing the compute resources used to produce these models.

---

## License

These quantized weights inherit the license of the base model (**Qwen3.8-Flash-Next**). The GSQ-RCO tooling is released by the Deep Algorithms and Systems Lab under its repository license.

<div align="center">
<sub>Built with <b>GSQ</b> and <b>RCO</b> at the <a href="https://github.com/IST-DASLab">Deep Algorithms and Systems Lab</a> &middot; Institute of Science and Technology Austria</sub>
</div>