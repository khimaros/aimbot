---
license: apache-2.0
library_name: llama.cpp
pipeline_tag: text-generation
tags:
- conversational
- ternary
- 2-bit
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

# Ternary Bonsai 27B — GGUF

Full 27B-class reasoning in ternary transformer weights, for llama.cpp (CUDA, Metal, CPU)

> **\~9.4x** smaller than FP16 (ideal) | **95%** of FP16 intelligence retained | **\~26 tok/s** on an Apple M5 Pro laptop

## Highlights

- **\~7.2 GB** deployed footprint (down from \~54 GB FP16) — full 27B-class reasoning on a standard laptop or a single GPU
- **95% of FP16 intelligence retained**: 80.49 average across 15 thinking-mode benchmarks — a *higher* score than the conventional IQ2_XXS build (72.73) at less than two-thirds of its footprint
- **Retains thinking, reasoning, and agentic behavior** deep in the sub-4-bit regime, where conventional low-bit representations collapse: math within two points of full precision (93.40), coding at 85.96, agentic tool use at 74.01
- **End-to-end ternary language weights** across embeddings, attention projections, MLP projections, and LM head, at a *true* 1.71 bits per weight — no high-precision escape hatches behind a low-bit label; the vision tower ships in compact 4-bit HQQ
- **262K-token context** on-device, kept practical by the Qwen3.6-27B hybrid-attention backbone (\~75% linear attention) and 4-bit KV-cache quantization
- **GGUF Q2_0_g128** format with custom 2-bit hybrid-attention kernels for llama.cpp (CUDA, Metal) — packed weights are consumed directly, never expanded back to FP16
- **Ships with a DSpark speculative-decoding drafter layer** trained against the Bonsai 27B target — a lossless **1.34x** decode speedup on the CUDA serving path
- **MLX companion**: also available as [Ternary-Bonsai-27B-mlx-2bit](https://huggingface.co/prism-ml/Ternary-Bonsai-27B-mlx-2bit) for native Apple Silicon inference
- **1-bit companion**: the phone-class operating point (\~3.9 GB) that fits an iPhone 17 Pro Max, published in GGUF as [Bonsai-27B-gguf](https://huggingface.co/prism-ml/Bonsai-27B-gguf)

## Resources

- **[Whitepaper](https://github.com/PrismML-Eng/Bonsai-demo/blob/main/bonsai-27b-whitepaper.pdf)** — full methodology, benchmarks, and measurement notes
- **[Demo & examples](https://github.com/PrismML-Eng/Bonsai-demo)** — serving, benchmarking, and integrating Bonsai
- **Low-bit kernels**: [llama.cpp fork](https://github.com/PrismML-Eng/llama.cpp) (CUDA + Metal) · [MLX fork](https://github.com/PrismML-Eng/mlx) (Apple Silicon) · [mlx-swift fork](https://github.com/PrismML-Eng/mlx-swift) (iOS/macOS)
- **[Discord](https://discord.gg/prismml)** — join the community for support, discussion, and updates

## Model Overview

| Item              | Specification                                                                                    |
| :---------------- | :----------------------------------------------------------------------------------------------- |
| Base model        | Derived from Qwen3.6-27B, a 27B hybrid-attention causal language model (architecture unchanged)  |
| Parameters        | \~27.3B ternary language weights (\~24.8B backbone across 64 blocks + \~2.5B embedding/LM head) + \~0.46B vision tower (27 blocks) |
| Architecture      | Hybrid attention (\~75% linear / \~25% full attention), SwiGLU MLP, RoPE, RMSNorm                   |
| Context length    | 262K tokens (full-context capable on-device, enabled by the predominantly linear-attention backbone) |
| KV cache          | Near-lossless 4-bit KV quantization; the hybrid backbone grows a full-attention cache on only 16 of 64 layers (\~4.3 GB at the full 262K window) |
| Weight format     | GGUF Q2_0_g128: {−1, 0, +1} weights in 2-bit slots with FP16 group-wise scaling                   |
| Low-bit coverage  | Embeddings, attention projections, MLP projections, LM head                                       |
| Vision tower      | HQQ 4-bit; optional \~0.63 GB mmproj pack (Q8_0 container), loaded only for image input            |
| Deployed size     | **\~7.2 GB** (5.9 GB ideal at 1.71 bits/weight; see below)                                         |
| Acceleration      | DSpark speculative-decoding drafter layer provided                                                |
| Backends          | llama.cpp (CUDA, Metal, CPU)                                                                      |
| License           | Apache 2.0                                                                                        |

## Weight Representation: Q2_0_g128

Each weight takes a value from {−1, 0, +1}, with one shared FP16 scale factor for every group of 128 weights. A ternary value carries log₂3 ≈ 1.585 bits of information, so the effective storage cost is **\~1.71 bits/weight** (ternary code + 16-bit scale amortized over 128 weights) — an idealized \~9.4x reduction vs FP16.

Relative to the binary format, the extra zero state gives a more expressive weight alphabet and recovers more of the full-precision model's behavior, which makes ternary the **quality-oriented operating point** of the Bonsai 27B family.

### Memory Requirement

| Format              | True bits/weight | Ideal size | Deployed size | Reduction (ideal) |
| :------------------ | ---------------: | ---------: | ------------: | ----------------: |
| FP16 (baseline)     | 16.0             | \~54 GB     | —             | 1.0x              |
| **GGUF Q2_0_g128**  | **1.71**         | **5.9 GB** | **\~7.2 GB**   | **\~9.4x**         |

Today's kernels store each ternary value in a 2-bit slot (2.125 bits/weight deployed), so the deployed footprint sits above the representation's information-theoretic minimum until native ternary kernels close the gap. The deployed figure describes the language model alone — the only component that must stay resident for text inference; a negligible tail of normalization and scale parameters remains in higher precision.

Unlike conventional low-bit builds — whose advertised labels understate their true average bit-width (a widely-used "2-bit" build of Qwen3.6-27B is really 2.8 bits/weight at 9.4 GB) — the Bonsai representation carries a bit-width that matches its name.

### Shipped Components

Two optional components ship alongside the language model (on-disk sizes):

| Component      | Pack                               | Size     | Residency                          |
| :------------- | :--------------------------------- | -------: | :--------------------------------- |
| Language model | 2-bit g128 slots (Q2_0)            | 7.17 GB  | resident                            |
| DSpark drafter | Q4_1 (default)                     | 1.95 GB  | optional — speculative decoding     |
| DSpark drafter | bf16 (reference)                   | 7.29 GB  | optional                            |
| Vision tower   | mmproj HQQ 4-bit (Q8_0 container)  | 0.63 GB  | optional — multimodal input only    |
| Vision tower   | mmproj BF16 (reference)            | 0.93 GB  | optional                            |

The vision tower is usually offloaded: it sits outside the accelerator's resident budget and is loaded only when an image actually arrives, so text-only serving never pays for it. A group-64 ternary pack (7.59 GB) is also published, matching the 64-value-group Q2_0 packing in llama.cpp — the same native g128 representation with each scale repeated per 64-value block.

### Peak Memory at Context

What a device must actually accommodate is *peak* memory — weights plus KV cache plus activations and runtime buffers (\~1.3 GB across backends). Measured, language model only, no KV-cache compression (sizes in decimal GB; the Q4_K_XL row is derived from its weight footprint plus the same measured cache-and-overhead build-up, all other rows directly measured):

| Build                                | Weights | 4K ctx | 10K ctx | 100K ctx |
| :----------------------------------- | ------: | -----: | ------: | -------: |
| **Ternary Bonsai (llama.cpp Q2_0)**  | 7.15    | 8.4    | 8.7     | 14.7     |
| Qwen3.6-27B "4-bit" (Q4_K_XL)        | 17.6    | 19.2   | 19.6    | 25.6     |
| 27B 16-bit (GGUF bf16)               | 51.25   | 52.6   | 53.3    | 59.3     |

The ternary build holds a **100K-token context at 14.7 GB without any KV-cache compression** — a budget that fits mainstream laptops outright; the conventional Q4_K_XL build needs \~25.6 GB before the first long document is loaded. These peaks are the conservative case, with the cache left at FP16. Enabling the 4-bit KV cache shrinks the context-dependent term \~4x: the 100K peak drops to \~10.1 GB, and the full 262K window fits in \~12.8 GB peak.

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
# Clone the PrismML fork of llama.cpp (includes the Q2_0_g128 hybrid-attention kernels)
git clone https://github.com/PrismML-Eng/llama.cpp
cd llama.cpp

# Build with CUDA support
cmake -B build -DGGML_CUDA=ON && cmake --build build -j

# Download the 2-bit GGUF weights
# (PQ2_0 = the group-128 pack this fork's kernels expect. For an upstream
#  llama.cpp build, use Ternary-Bonsai-27B-Q2_g64.gguf instead.)
hf download prism-ml/Ternary-Bonsai-27B-gguf Ternary-Bonsai-27B-PQ2_0.gguf --local-dir .

# Run inference
./build/bin/llama-cli \
    -m Ternary-Bonsai-27B-PQ2_0.gguf \
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
    -m Ternary-Bonsai-27B-PQ2_0.gguf \
    -p "Explain quantum computing in simple terms." \
    -n 256 \
    --temp 0.7 --top-p 0.95 --top-k 20 \
    -ngl 99
```

### llama.cpp Server

```bash
./build/bin/llama-server \
    -m Ternary-Bonsai-27B-PQ2_0.gguf \
    --host 0.0.0.0 --port 8080 -ngl 99
```

Open the web UI at [http://127.0.0.1:8080](http://127.0.0.1:8080), or see our [llama.cpp fork](https://github.com/PrismML-Eng/llama.cpp) for more examples.

> **Deploying to a phone?** The ternary build (\~7.2 GB) exceeds the \~6 GB per-app iOS memory budget and is laptop/GPU-only. Use the 1-bit companion (\~3.9 GB), which fits an iPhone 17 Pro Max via [MLX Swift](https://huggingface.co/prism-ml/Bonsai-27B-mlx-1bit).

## Cross-Platform Throughput

`tg128` is token-generation throughput over 128 generated tokens (the memory-bandwidth-bound, interactive phase); `pp512` is prompt-processing throughput over 512 input tokens (the compute-bound phase). Both in tokens/s, measured with `llama-bench` on this GGUF pack (custom low-bit kernels).

| Platform                     | Footprint | TG128 (tok/s) | PP512 (tok/s) |
| :--------------------------- | --------: | ------------: | ------------: |
| Laptop (Apple M5 Max, Metal) | 7.2 GB    | 44.0          | 830           |
| Laptop (Apple M5 Pro, Metal) | 7.2 GB    | 26.2          | 393           |
| Laptop (Apple M4 Pro, Metal) | 7.2 GB    | 18.0          | 125           |
| Single GPU (H100, CUDA)      | 7.2 GB    | 98.0          | 2596          |

On the laptop, the FP16 baseline (\~54 GB) and even conventional "4-bit" builds (17.6 GB) do not fit at all — the meaningful statement is not a speedup ratio but that a 27B model runs interactively on an everyday laptop. The measured decode streams \~186 GB/s of weights on the M5 Pro, confirming the memory-bandwidth-dominated profile that the low-bit representation is built to exploit. The H100 row is the exception that proves the rule: at batch size 1 a datacenter GPU is limited by kernel-launch and synchronization latency rather than weight bandwidth, so the ternary and binary variants converge there (98 vs 104.8 tok/s) despite their \~1.9x difference in bytes per step.

## Speculative Decoding: DSpark

Ternary Bonsai 27B ships with a **DSpark** drafter layer trained against the low-bit target — a semi-autoregressive drafter with confidence-scheduled verification. Speculative decoding is lossless: verification preserves the target distribution exactly, so accepted tokens are indistinguishable from ordinary generation.

The drafter is a compact **six-layer block-parallel transformer** conditioned on hidden states tapped from five evenly spaced layers of the target; its drafter-unique weights add roughly **0.5 GB at serving precision** (embeddings and output head are shared with the resident target). It follows the DSpark recipe with a diffusion-flavored block-denoising objective, survival-probability-weighted distillation, per-source-normalized hidden-state taps, and a draft block size chosen from a measured verify-cost model of the serving stack. The drafter ships 4-bit quantized — the \~1.95 GB Q4_1 pack is the default; it drafts faster than the bf16 reference at essentially unchanged draft quality, and because verification preserves the target distribution exactly, drafter precision affects only speed, never output quality.

On the CUDA serving path the drafter is a measured net win — an accepted length of τ ≈ 3.7 at draft depth k = 4 turns into a **1.34x** end-to-end decode speedup on H100 (98 → 131.8 tok/s). On Apple Silicon the batch-1 verification pass does not yet amortize, so the drafter layer is not enabled by default on-device.

## Benchmarks

Evaluated with EvalScope + vLLM on NVIDIA H100 under identical infrastructure, decoding, and scoring, in **thinking mode** — where the model's full reasoning is exercised and the sub-4-bit collapse of conventional methods is most visible. 15 benchmarks across six skill categories. For cross-family context the table also includes Gemma-4-31B, a model of the same capability tier, with its conventional low-bit builds — the collapse below 4 bits is a property of the methods, not of one base model. Bit-widths are true averages; "vs FP16" is relative to the Qwen3.6-27B FP16 reference.

| Variant                                                                    | True bpw | Footprint  | Thinking avg | vs FP16    |
| :-------------------------------------------------------------------------- | -------: | ---------: | -----------: | ---------: |
| Qwen3.6-27B FP16                                                            | 16.0     | 54 GB      | 85.07        | 100%       |
| Qwen3.6-27B Q4_K_XL ("4-bit")                                               | 5.2      | 17.6 GB    | 84.99        | 99.9%      |
| Qwen3.6-27B IQ2_XXS ("2-bit")                                               | 2.8      | 9.4 GB     | 72.73        | 85.5%      |
| Gemma-4-31B FP16                                                            | 16.0     | 61.5 GB    | 84.58        | 99.4%      |
| Gemma-4-31B QAT ("4-bit")                                                   | 6.0      | 23.3 GB    | 83.41        | 98.0%      |
| Gemma-4-31B Q2_K_XL ("2-bit")                                               | 3.0      | 11.8 GB    | 73.31        | 86.2%      |
| **Ternary Bonsai 27B**                                                      | **1.71** | **5.9 GB** | **80.49**    | **94.6%**  |
| 1-bit Bonsai 27B                                                            | 1.125    | 3.9 GB     | 76.11        | 89.5%      |

At 5.9 GB, Ternary Bonsai 27B outscores both sub-4-bit conventional builds by more than seven points at one-half to two-thirds of their size.

The aggregate gap also understates *how* the conventional builds fail: their degradation is selective, concentrated on the benchmarks that demand sustained chains of reasoning. IQ2_XXS falls to 57.5 on AIME26 and 56.4 on LiveCodeBench while still scoring 88.93 on MMLU-Redux — which is why casual testing misses the collapse. Ternary Bonsai holds exactly these benchmarks, keeping AIME at 87.5–90.8 and LiveCodeBench at 82.8.

### By Skill Category

| Category                | Benchmarks                          | FP16  | Ternary 27B |
| :---------------------- | :---------------------------------- | ----: | ----------: |
| Knowledge & reasoning   | MMLU-Redux, MuSR                    | 83.15 | 76.96       |
| Math                    | GSM8K, MATH-500, AIME25, AIME26     | 95.33 | 93.40       |
| Coding                  | HumanEval+, MBPP+, LiveCodeBench    | 88.74 | 85.96       |
| Instruction following   | IFEval, IFBench                     | 78.47 | 71.77       |
| Agentic / tool calling  | BFCL v3, τ²-Bench                   | 80.00 | 74.01       |
| Vision                  | MMMU-Pro, OCR Bench v2              | 72.61 | 65.19       |
| **Overall (15)**        |                                     | **85.07** | **80.49** |

The reasoning backbone comes through intact: math stays within two points of full precision (93.40), coding at 85.96, and the ternary model spends its extra footprint to hold the most demanding categories — agentic tool use at 74.01 and vision at 65.19 — the behaviors that conventional sub-4-bit representations lose first.

### Full Per-Benchmark Results

<details>
<summary>Expand full per-benchmark results (thinking mode)</summary>

| Benchmark              | FP16  | Ternary 27B |
| :--------------------- | ----: | ----------: |
| MMLU-Redux             | 93.42 | 88.05       |
| MuSR                   | 72.88 | 65.87       |
| GSM8K                  | 95.30 | 96.06       |
| MATH-500               | 99.40 | 99.20       |
| AIME25                 | 93.29 | 90.84       |
| AIME26                 | 93.33 | 87.50       |
| HumanEval+             | 95.12 | 93.90       |
| MBPP+                  | 83.33 | 81.22       |
| LiveCodeBench          | 87.77 | 82.75       |
| IFEval                 | 88.91 | 85.03       |
| IFBench (prompt-loose) | 68.03 | 58.50       |
| BFCL v3                | 77.10 | 74.41       |
| τ²-Bench               | 82.90 | 73.61       |
| MMMU-Pro               | 79.94 | 68.96       |
| OCR Bench v2           | 65.28 | 61.42       |
| **Average (15)**       | **85.07** | **80.49** |

</details>

## Intelligence Density

Intelligence density captures the ratio of a model's capability to its deployed size:

```
D = -log2(1 - score/100) / size_GB
```

| Variant                                                                    | Size (GB) | Benchmark avg | Intelligence Density (1/GB) |
| :-------------------------------------------------------------------------- | --------: | -----------: | --------------------------: |
| 1-bit Bonsai 27B                                                            | 3.9       | 76.11        | 0.530                       |
| **Ternary Bonsai 27B**                                                      | **5.9**   | 80.49        | **0.400**                   |
| Qwen3.6-27B IQ2_XXS                                                         | 9.4       | 72.73        | 0.199                       |
| Gemma-4-31B Q2_K_XL                                                         | 11.8      | 73.31        | 0.162                       |
| Qwen3.6-27B Q4_K_XL                                                         | 17.6      | 84.99        | 0.155                       |
| Gemma-4-31B QAT                                                             | 23.3      | 83.41        | 0.111                       |
| Qwen3.6-27B FP16                                                            | 54        | 85.07        | 0.051                       |
| Gemma-4-31B FP16                                                            | 61.5      | 84.58        | 0.044                       |

Ternary Bonsai 27B delivers **2x** the density of the densest conventional build (IQ2_XXS at 0.199) and nearly **8x** FP16 — no conventional build of Qwen3.6-27B or Gemma-4-31B exceeds 0.2. Each stored gigabyte is translated into far more usable intelligence.

## Use Cases

- **Laptop-local 27B agents**: full 27B reasoning and tool use on a standard laptop at \~26 tok/s, with the 262K context available for long-document analysis, full-repository code work, and other tasks that depend on holding a large working set in context
- **Privacy-sensitive and offline settings**: on-device execution keeps prompts and data on the device by construction, and works with intermittent or no connectivity
- **Single-GPU and commodity-GPU serving**: 27B-class quality from a single consumer or entry-level datacenter GPU, with headroom for larger batches, longer contexts, or co-resident models — combined with the KV-cache quantization, high-throughput serving and long-context document analysis become practical on a single 24 GB GPU
- **Quality-first low-bit deployment**: when the deployment target has laptop-class memory or better, ternary is the operating point that retains the most of the full-precision model's behavior

## Limitations

- **The quality–footprint trade-off**: the ternary model retains 94.6% of the full-precision average, and the gap is modest and predictable — the reasoning core (math, coding) stays within a few points of baseline, with the difference concentrated in the most demanding categories
- **Does not fit a phone**: at \~7.2 GB the ternary build exceeds the \~6 GB per-app iOS memory budget; use the 1-bit companion via [MLX Swift](https://huggingface.co/prism-ml/Bonsai-27B-mlx-1bit) for phone deployment
- **Served in 2-bit slots today**: the deployed footprint (\~7.2 GB) sits above the representation's \~5.9 GB native target; native ternary kernels are an active engineering target and would return the remaining bandwidth and footprint advantage directly as latency and energy improvements
- **Agentic coding** (long-horizon, multi-file, run-test-and-repair workflows) is not yet a strong target of this release; a Bonsai 27B variant tuned for agentic coding is next on the roadmap
- **KV compression headroom**: this release standardizes on a 4-bit KV cache; early results show the key cache can be pushed toward the sub-2-bit regime — a path to still longer contexts within a fixed device-memory budget

## Citation

If you use Ternary Bonsai 27B, please cite:

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
