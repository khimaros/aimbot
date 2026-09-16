---
license: apache-2.0
library_name: llama.cpp
pipeline_tag: text-generation
tags:
- conversational
- 1-bit
- gguf
- llama-cpp
- cuda
- metal
- on-device
- hybrid-attention
- prismml
- bonsai
base_model:
- Qwen/Qwen3.6-27B
---

<p align="center">
  <img src="./assets/bonsai-logo.svg" width="280" alt="Bonsai">
</p>

<p align="center">
  <a href="https://prismml.com"><b>Prism ML Website</b></a> &nbsp;|&nbsp;
  <a href="https://github.com/PrismML-Eng/Bonsai-demo"><b>Whitepaper</b></a> &nbsp;|&nbsp;
  <a href="https://github.com/PrismML-Eng/Bonsai-demo"><b>Demo &amp; Examples</b></a> &nbsp;|&nbsp;
  <a href="https://discord.gg/prismml"><b>Discord</b></a>
</p>

# 1-bit Bonsai 27B — GGUF

Full 27B-class reasoning in binary transformer weights, for llama.cpp (CUDA, Metal, CPU)

> **\~14.2x** smaller than FP16 | **\~90%** of FP16 intelligence retained | **\~44 tok/s** on an Apple M5 Pro laptop

## Highlights

- **\~3.9 GB** deployed footprint (down from \~54 GB FP16) — a 27B model on everyday laptops and single GPUs
- **Retains thinking, reasoning, and agentic behavior** deep in the sub-4-bit regime, where conventional low-bit representations collapse — 76.11 average across 15 thinking-mode benchmarks (89.5% of FP16), including math at 91.66 and coding at 81.88
- **End-to-end binary language weights** across embeddings, attention projections, MLP projections, and LM head, at a *true* 1.125 bits per weight — no high-precision escape hatches behind a low-bit label; the vision tower ships in compact 4-bit HQQ
- **262K-token context** on-device, kept practical by the Qwen3.6-27B hybrid-attention backbone (\~75% linear attention) and 4-bit KV-cache quantization
- **GGUF Q1_0_g128** format with custom 1-bit hybrid-attention kernels for llama.cpp (CUDA, Metal) — packed weights are consumed directly, never expanded back to FP16
- **Ships with a DSpark speculative-decoding drafter layer** trained against the Bonsai 27B target — a lossless **1.37x** decode speedup on the CUDA serving path
- **MLX companion**: also available as [Bonsai-27B-mlx-1bit](https://huggingface.co/prism-ml/Bonsai-27B-mlx-1bit) for native Apple Silicon inference, including iPhone (\~11 tok/s on iPhone 17 Pro Max via MLX Swift)
- **Ternary companion**: the quality-oriented operating point (\~7.2 GB, 95% of FP16) is also published in GGUF as [Ternary-Bonsai-27B-gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-27B-gguf)

## Resources

- **[Whitepaper](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/bonsai-27b-whitepaper.pdf)** — full methodology, benchmarks, and measurement notes
- **[Demo & examples](https://github.com/PrismML-Eng/Bonsai-demo)** — serving, benchmarking, and integrating Bonsai
- **Low-bit kernels**: [llama.cpp fork](https://github.com/PrismML-Eng/llama.cpp) (CUDA + Metal) · [MLX fork](https://github.com/PrismML-Eng/mlx) (Apple Silicon) · [mlx-swift fork](https://github.com/PrismML-Eng/mlx-swift) (iOS/macOS)
- **[Discord](https://discord.gg/prismml)** — join the community for support, discussion, and updates

## Model Overview

| Item              | Specification                                                                                    |
| :---------------- | :----------------------------------------------------------------------------------------------- |
| Base model        | Derived from Qwen3.6-27B, a 27B hybrid-attention causal language model (architecture unchanged)  |
| Parameters        | \~27.3B binary language weights (\~24.8B backbone across 64 blocks + \~2.5B embedding/LM head) + \~0.46B vision tower (27 blocks) |
| Architecture      | Hybrid attention (\~75% linear / \~25% full attention), SwiGLU MLP, RoPE, RMSNorm                   |
| Context length    | 262K tokens (full-context capable on-device, enabled by the predominantly linear-attention backbone) |
| KV cache          | Near-lossless 4-bit KV quantization; the hybrid backbone grows a full-attention cache on only 16 of 64 layers (\~4.3 GB at the full 262K window) |
| Weight format     | GGUF Q1_0_g128: {−1, +1} weights with FP16 group-wise scaling                                     |
| Low-bit coverage  | Embeddings, attention projections, MLP projections, LM head                                       |
| Vision tower      | HQQ 4-bit; optional \~0.63 GB mmproj pack (Q8_0 container), loaded only for image input            |
| Deployed size     | **\~3.9 GB** (\~14.2x smaller than FP16)                                                            |
| Acceleration      | DSpark speculative-decoding drafter layer provided                                                |
| Backends          | llama.cpp (CUDA, Metal, CPU)                                                                      |
| License           | Apache 2.0                                                                                        |

## Weight Representation: Q1_0_g128

Each weight is a single sign bit: `0` maps to `−scale`, `1` maps to `+scale`. Every group of 128 weights shares one FP16 scale factor.

Effective bits per weight: **1.125** (1 sign bit + 16-bit scale amortized over 128 weights) — an idealized \~14.2x reduction vs FP16. This is the most aggressive operating point in the Bonsai 27B family: it minimizes both stored footprint and the weight traffic incurred at every decoding step. The GGUF Q1_0_g128 pack is the model's native layout — ideal and deployed sizes match.

### Memory Requirement

| Format              | True bits/weight | Size        | Reduction   |
| :------------------ | ---------------: | ----------: | ----------: |
| FP16 (baseline)     | 16.0             | \~54 GB      | 1.0x        |
| **GGUF Q1_0_g128**  | **1.125**        | **\~3.9 GB** | **\~14.2x**  |

The deployed figure describes the language model alone — the only component that must stay resident for text inference; a negligible tail of normalization and scale parameters remains in higher precision.

Unlike conventional low-bit builds — whose advertised labels understate their true average bit-width (a widely-used "2-bit" build of Qwen3.6-27B is really 2.8 bits/weight at 9.4 GB) — the Bonsai representation carries a bit-width that matches its name.

### Shipped Components

Two optional components ship alongside the language model (on-disk sizes):

| Component      | Pack                               | Size     | Residency                          |
| :------------- | :--------------------------------- | -------: | :--------------------------------- |
| Language model | 1-bit g128 (Q1_0)                  | \~3.9 GB  | resident                            |
| DSpark drafter | Q4_1 (default)                     | 1.79 GB  | optional — speculative decoding     |
| DSpark drafter | bf16 (reference)                   | 7.29 GB  | optional                            |
| Vision tower   | mmproj HQQ 4-bit (Q8_0 container)  | 0.63 GB  | optional — multimodal input only    |
| Vision tower   | mmproj BF16 (reference)            | 0.93 GB  | optional                            |

The vision tower is usually offloaded: it sits outside the accelerator's resident budget and is loaded only when an image actually arrives, so text-only serving never pays for it.

### Peak Memory at Context

What a device must actually accommodate is *peak* memory — weights plus KV cache plus activations and runtime buffers (\~1.3 GB across backends). Measured, language model only, no KV-cache compression (sizes in decimal GB; the Q4_K_XL row is derived from its weight footprint plus the same measured cache-and-overhead build-up, all other rows directly measured):

| Build                                | Weights | 4K ctx | 10K ctx | 100K ctx |
| :----------------------------------- | ------: | -----: | ------: | -------: |
| **1-bit Bonsai (llama.cpp Q1_0)**    | 3.79    | 5.2    | 5.6     | 11.6     |
| Qwen3.6-27B "4-bit" (Q4_K_XL)        | 17.6    | 19.2   | 19.6    | 25.6     |
| 27B 16-bit (GGUF bf16)               | 51.25   | 52.6   | 53.3    | 59.3     |

The 1-bit build holds a **100K-token context at 11.6 GB without any KV-cache compression** — a budget that fits mainstream laptops outright; the conventional Q4_K_XL build needs \~25.6 GB before the first long document is loaded. These peaks are the conservative case, with the cache left at FP16. Enabling the 4-bit KV cache shrinks the context-dependent term \~4x: the 100K peak drops to \~6.8 GB, and the full 262K window fits in \~9.4 GB peak.

## Best Practices

### Generation Parameters

| Parameter   | Suggested |
| :---------- | :-------- |
| Temperature | 0.7       |
| Top-p       | 0.95      |
| Top-k       | 20        |

These are the settings used for all reported benchmark results (thinking mode).

### System Prompt

You can use a simple system prompt such as:

```
You are a helpful assistant
```

## Quickstart

### llama.cpp (CUDA)

```bash
# Clone the PrismML fork of llama.cpp (includes the Q1_0_g128 hybrid-attention kernels)
git clone https://github.com/PrismML-Eng/llama.cpp
cd llama.cpp

# Build with CUDA support
cmake -B build -DGGML_CUDA=ON && cmake --build build -j

# Download the 1-bit GGUF weights
hf download prism-ml/Bonsai-27B-gguf Bonsai-27B-Q1_0.gguf --local-dir .

# Run inference
./build/bin/llama-cli \
    -m Bonsai-27B-Q1_0.gguf \
    -p "Explain quantum computing in simple terms." \
    -n 256 \
    --temp 0.7 --top-p 0.95 --top-k 20 \
    -ngl 99
```

### llama.cpp (Metal / macOS)

```bash
# Build with Metal support (default on macOS)
cmake -B build && cmake --build build -j

# Run inference
./build/bin/llama-cli \
    -m Bonsai-27B-Q1_0.gguf \
    -p "Explain quantum computing in simple terms." \
    -n 256 \
    --temp 0.7 --top-p 0.95 --top-k 20 \
    -ngl 99
```

### llama.cpp Server

```bash
./build/bin/llama-server \
    -m Bonsai-27B-Q1_0.gguf \
    --host 0.0.0.0 --port 8080 -ngl 99
```

Open the web UI at [http://127.0.0.1:8080](http://127.0.0.1:8080), or see our [llama.cpp fork](https://github.com/PrismML-Eng/llama.cpp) for more examples.

> **Deploying to a phone?** iPhone deployment uses the MLX Swift runtime — see [Bonsai-27B-mlx-1bit](https://huggingface.co/prism-ml/Bonsai-27B-mlx-1bit) (\~11 tok/s on iPhone 17 Pro Max).

## Cross-Platform Throughput

`tg128` is token-generation throughput over 128 generated tokens (the memory-bandwidth-bound, interactive phase); `pp512` is prompt-processing throughput over 512 input tokens (the compute-bound phase). Both in tokens/s, measured with `llama-bench` on this GGUF pack (custom low-bit kernels).

| Platform                     | Footprint | TG128 (tok/s) | PP512 (tok/s) |
| :--------------------------- | --------: | ------------: | ------------: |
| Laptop (Apple M5 Max, Metal) | 3.9 GB    | 66.4          | 874           |
| Laptop (Apple M5 Pro, Metal) | 3.9 GB    | 44.2          | 421           |
| Laptop (Apple M4 Pro, Metal) | 3.9 GB    | 26.0          | 133           |
| Single GPU (H100, CUDA)      | 3.9 GB    | 104.8         | 2755          |

On the edge platforms the FP16 baseline (\~54 GB) and even conventional "4-bit" builds (17.6 GB) do not fit at all — the meaningful statement is not a speedup ratio but that a 27B model runs on the device in the first place. The H100 row is the exception that proves the rule: at batch size 1 a datacenter GPU is limited by kernel-launch and synchronization latency rather than weight bandwidth, so the binary and ternary variants converge there (104.8 vs 98 tok/s) despite their \~1.9x difference in bytes per step.

Decode energy on the M5 Pro measures **0.275 mWh/token** (with the DSpark drafter enabled) — an order of magnitude more energy-efficient per token than datacenter GPUs (0.63–1.32 mWh/token across the GPU classes). Local inference is not just private and low-latency but cheap in energy.

## Speculative Decoding: DSpark

1-bit Bonsai 27B ships with a **DSpark** drafter layer trained against the low-bit target — a semi-autoregressive drafter with confidence-scheduled verification. Speculative decoding is lossless: verification preserves the target distribution exactly, so accepted tokens are indistinguishable from ordinary generation.

The drafter is a compact **six-layer block-parallel transformer** conditioned on hidden states tapped from five evenly spaced layers of the target; its drafter-unique weights add roughly **0.5 GB at serving precision** (embeddings and output head are shared with the resident target). It follows the DSpark recipe with a diffusion-flavored block-denoising objective, survival-probability-weighted distillation, per-source-normalized hidden-state taps, and a draft block size chosen from a measured verify-cost model of the serving stack. The drafter ships 4-bit quantized — the \~1.79 GB Q4_1 pack is the default; it drafts faster than the bf16 reference at essentially unchanged draft quality, and because verification preserves the target distribution exactly, drafter precision affects only speed, never output quality.

On the CUDA serving path the drafter is a measured net win — an accepted length of τ ≈ 3.6 at draft depth k = 4 turns into a **1.37x** end-to-end decode speedup on H100 (104.8 → 143.8 tok/s). On Apple Silicon the batch-1 verification pass does not yet amortize, so the drafter layer is not enabled by default on-device.

## Benchmarks

Evaluated with EvalScope + vLLM on NVIDIA H100 under identical infrastructure, decoding, and scoring, in **thinking mode** — where the model's full reasoning is exercised and the sub-4-bit collapse of conventional methods is most visible. 15 benchmarks across six skill categories. For cross-family context the table also includes Gemma-4-31B, a model of the same capability tier, with its conventional low-bit builds — the collapse below 4 bits is a property of the methods, not of one base model. Bit-widths are true averages; "vs FP16" is relative to the Qwen3.6-27B FP16 reference.

| Variant                                                                       | True bpw  | Footprint   | Thinking avg | vs FP16    |
| :---------------------------------------------------------------------------- | --------: | ----------: | -----------: | ---------: |
| Qwen3.6-27B FP16                                                              | 16.0      | 54 GB       | 85.07        | 100%       |
| Qwen3.6-27B Q4_K_XL ("4-bit")                                                 | 5.2       | 17.6 GB     | 84.99        | 99.9%      |
| Qwen3.6-27B IQ2_XXS ("2-bit")                                                 | 2.8       | 9.4 GB      | 72.73        | 85.5%      |
| Gemma-4-31B FP16                                                              | 16.0      | 61.5 GB     | 84.58        | 99.4%      |
| Gemma-4-31B QAT ("4-bit")                                                     | 6.0       | 23.3 GB     | 83.41        | 98.0%      |
| Gemma-4-31B Q2_K_XL ("2-bit")                                                 | 3.0       | 11.8 GB     | 73.31        | 86.2%      |
| Ternary Bonsai 27B                                                            | 1.71      | 5.9 GB      | 80.49        | 94.6%      |
| **1-bit Bonsai 27B**                                                          | **1.125** | **3.9 GB**  | **76.11**    | **89.5%**  |

The aggregate gap also understates *how* the conventional builds fail: their degradation is selective, concentrated on the benchmarks that demand sustained chains of reasoning. IQ2_XXS falls to 57.5 on AIME26 and 56.4 on LiveCodeBench while still scoring 88.93 on MMLU-Redux — which is why casual testing misses the collapse. 1-bit Bonsai holds exactly these benchmarks, keeping AIME above 87 at a third of IQ2_XXS's footprint.

### By Skill Category

| Category                | Benchmarks                          | FP16  | 1-bit 27B |
| :---------------------- | :---------------------------------- | ----: | --------: |
| Knowledge & reasoning   | MMLU-Redux, MuSR                    | 83.15 | 73.39     |
| Math                    | GSM8K, MATH-500, AIME25, AIME26     | 95.33 | 91.66     |
| Coding                  | HumanEval+, MBPP+, LiveCodeBench    | 88.74 | 81.88     |
| Instruction following   | IFEval, IFBench                     | 78.47 | 65.74     |
| Agentic / tool calling  | BFCL v3, τ²-Bench                   | 80.00 | 66.03     |
| Vision                  | MMMU-Pro, OCR Bench v2              | 72.61 | 59.57     |
| **Overall (15)**        |                                     | **85.07** | **76.11** |

The reasoning backbone comes through intact: math stays at 91.66 — within four points of full precision — and coding at 81.88, the behaviors that conventional sub-4-bit representations lose first. The 1-bit model trades part of the ternary model's margin on the most demanding categories for the smallest footprint in the family.

### Full Per-Benchmark Results

<details>
<summary>Expand full per-benchmark results (thinking mode)</summary>

| Benchmark              | FP16  | 1-bit 27B |
| :--------------------- | ----: | --------: |
| MMLU-Redux             | 93.42 | 82.75     |
| MuSR                   | 72.88 | 64.02     |
| GSM8K                  | 95.30 | 92.80     |
| MATH-500               | 99.40 | 98.00     |
| AIME25                 | 93.29 | 88.75     |
| AIME26                 | 93.33 | 87.08     |
| HumanEval+             | 95.12 | 89.63     |
| MBPP+                  | 83.33 | 79.60     |
| LiveCodeBench          | 87.77 | 76.40     |
| IFEval                 | 88.91 | 79.11     |
| IFBench (prompt-loose) | 68.03 | 52.36     |
| BFCL v3                | 77.10 | 70.72     |
| τ²-Bench               | 82.90 | 61.34     |
| MMMU-Pro               | 79.94 | 60.48     |
| OCR Bench v2           | 65.28 | 58.65     |
| **Average (15)**       | **85.07** | **76.11** |

</details>

## Intelligence Density

Intelligence density captures the ratio of a model's capability to its deployed size:

```
D = -log2(1 - score/100) / size_GB
```

| Variant                                                                       | Size (GB) | Benchmark avg | Intelligence Density (1/GB) |
| :---------------------------------------------------------------------------- | --------: | -----------: | --------------------------: |
| **1-bit Bonsai 27B**                                                          | **3.9**   | 76.11        | **0.530**                   |
| Ternary Bonsai 27B                                                            | 5.9       | 80.49        | 0.400                       |
| Qwen3.6-27B IQ2_XXS                                                           | 9.4       | 72.73        | 0.199                       |
| Gemma-4-31B Q2_K_XL                                                           | 11.8      | 73.31        | 0.162                       |
| Qwen3.6-27B Q4_K_XL                                                           | 17.6      | 84.99        | 0.155                       |
| Gemma-4-31B QAT                                                               | 23.3      | 83.41        | 0.111                       |
| Qwen3.6-27B FP16                                                              | 54        | 85.07        | 0.051                       |
| Gemma-4-31B FP16                                                              | 61.5      | 84.58        | 0.044                       |

1-bit Bonsai 27B delivers roughly **2.7x** the density of the densest conventional build (IQ2_XXS at 0.199) and over **10x** FP16 — no conventional build of Qwen3.6-27B or Gemma-4-31B exceeds 0.2. Each stored gigabyte is translated into far more usable intelligence.

## Use Cases

- **Laptop-local 27B agents**: full 27B reasoning and tool use on any standard laptop at \~26–66 tok/s (M4 Pro through M5 Max), with the 262K context available for long-document analysis and full-repository code work
- **Privacy-sensitive and offline settings**: on-device execution keeps prompts and data on the device by construction, and works with intermittent or no connectivity
- **Single-GPU and commodity-GPU serving**: 27B-class quality from a single consumer or entry-level datacenter GPU, with headroom for larger batches, longer contexts, or co-resident models — combined with the KV-cache quantization, high-throughput serving and long-context document analysis become practical on a single 24 GB GPU
- **Phone deployment via MLX**: the same weights ship as [Bonsai-27B-mlx-1bit](https://huggingface.co/prism-ml/Bonsai-27B-mlx-1bit) — the first 27B-class model to run on a phone

## Limitations

- **The quality–footprint trade-off**: the binary model retains 89.5% of the full-precision average, and the gap is modest and predictable — the reasoning core (math, coding) stays within a few points of baseline, with the difference concentrated in the most demanding categories; if quality is the priority, consider the ternary GGUF build (94.6%)
- **Agentic coding** (long-horizon, multi-file, run-test-and-repair workflows) is not yet a strong target of this release; a Bonsai 27B variant tuned for agentic coding is next on the roadmap
- **KV compression headroom**: this release standardizes on a 4-bit KV cache; Bonsai's tolerance to KV-cache error grows with context length, and early results show the key cache can be pushed toward the sub-2-bit regime — a path to still longer contexts within a fixed device-memory budget

## Citation

If you use 1-bit Bonsai 27B, please cite:

```bibtex
@techreport{bonsai27b,
    title   = {Bonsai 27B: Full 27B-Class Reasoning in Binary and Ternary
               Transformer Weights --- on Laptops and Phones},
    author  = {Prism ML},
    year    = {2026},
    month   = {July},
    url     = {https://prismml.com}
}
```

## Contact

For questions, feedback, or collaboration inquiries: **contact@prismml.com**
