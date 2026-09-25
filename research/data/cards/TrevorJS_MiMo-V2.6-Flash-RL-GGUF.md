---
base_model: XiaomiMiMo/MiMo-V2.6-Flash-RL
base_model_relation: quantized
license: mit
language:
  - en
  - zh
tags:
  - gguf
  - llama.cpp
  - imatrix
  - moe
  - mimo
  - dgx-spark
  - speculative-decoding
pipeline_tag: text-generation
---

# MiMo-V2.6-Flash-RL GGUF for a single DGX Spark

An imatrix-calibrated IQ2 build of
[XiaomiMiMo/MiMo-V2.6-Flash-RL](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Flash-RL)
(309B total / 15B active MoE, 1M context) that fits and runs on one DGX Spark
(GB10, 128 GB unified memory), plus a GGUF of Xiaomi's DFlash drafter.
Converted from snapshot `3b38d063`.

This is **v2.1**. It replaces the first upload (v1), which was 22% slower at
decode and scored lower on GSM8K; see [Changes from v1](#changes-from-v1).

## Files

| file | size | what |
|---|---:|---|
| `MiMo-V2.6-Flash-RL-IQ2_XS_M-v2.1-*.gguf` | 91.9 GiB, 10 shards | the model; load the first shard |
| `MiMo-V2.6-Flash-RL-DFlash-Q8_0.gguf` | 2.1 GiB | DFlash speculative drafter (see [DFlash](#dflash-drafter)) |
| `recipe-iq2_xs_m-v2.1.txt` | | `--tensor-type-file` used with `llama-quantize` |

Text only. The vision and audio encoders convert separately (mmproj) and are
not included.

## Measured on a DGX Spark (GB10)

### Speed

`llama-bench`, `-fa 1 -ngl 99`:

| test | `-ub 512` (default) | `-ub 2048` | `-ub 4096` |
|---|---:|---:|---:|
| pp2048 | 421.7 | **733.5** | 730.0 |
| pp8192 | 418.6 | 725.1 | **799.5** |
| pp2048 at 8K depth | | 719.3 | |
| tg32 | 32.1 | | |

**Pass `-ub 2048`.** The default micro-batch of 512 leaves ~45% of prefill on
the table: at 512 each of the 256 experts sees too few tokens per matmul.

Server, 512-token greedy generations, thinking off:

| config | code | reasoning | prose |
|---|---:|---:|---:|
| no draft | 30.6 | 30.7 | 30.8 |
| DFlash, 5 drafted, `p_min` 0.7 | **42.9** | **38.7** | 26.9 |

DFlash helps code (+40%) and reasoning (+26%) and costs prose about 13%,
where the drafter is rarely right. For prose-heavy use, run without it.

A 5.5K-token prompt at `-ub 2048`: prefill 671 t/s without the drafter,
656 t/s with it at `-b 8192` (647 at `-b 2048`); decode on the reply 29 vs
about 33 t/s. The drafter only reads the prompt's last 1024 positions, so
only those are fed to it; a larger `-b` means fewer feeds per prompt.

### Quality

GSM8K, 500 items, greedy, zero-shot, thinking off. The items and prompt
length are matched to the harness used for
[benthecarman/MiMo-V2.6-Flash-RL-exl3](https://huggingface.co/benthecarman/MiMo-V2.6-Flash-RL-exl3)
(the same 500 test items, prompts totalling the same 49,205 tokens), so the
columns are comparable:

| build | GSM8K |
|---|---:|
| FP8 reference, unquantized (from the EXL3 card) | 96.4% |
| EXL3 2.36 bpw (from the EXL3 card) | 95.8% |
| **this build (v2.1)** | **95.6%** (478/500) |
| v1 of this repo | 95.0% |

Perplexity on `wiki.test.raw` (full file, `-c 512`): 5.7225 ± 0.034, which is
+11.2% over the BF16 reference of 5.1455 reported by
[AesSedai](https://huggingface.co/AesSedai/MiMo-V2.6-Flash-GGUF) with the same
method. Arithmetic survives this bitrate far better than perplexity suggests.

## Recipe

| tensors | type |
|---|---|
| routed expert gate, up | IQ2_XS |
| routed expert down | IQ2_S |
| layer 47 routed experts (gate, up, down) | Q6_K |
| attention QKV and output | IQ4_XS |
| dense FFN (layer 0, MTP blocks), MTP `eh_proj` | Q6_K |
| token embeddings | Q8_0 |
| output head | Q6_K |
| router, norms, sinks, expert bias | F32 |

2.55 bits per weight overall.

**Why attention is IQ4_XS:** on this model the non-expert tensors are over half
of what each token reads from memory at IQ2, so dropping attention from Q6_K
to IQ4_XS bought 22% decode speed with no measurable GSM8K cost.

**Why layer 47 is Q6_K:** layer 47's expert intermediates (the input to its
down projection) get large enough that a 32-value sum passes f16's 65504. In
llama.cpp's CUDA kernels, Q4_K and Q5_K (and Q4_0/Q4_1/Q5_0/Q5_1/Q2_K/IQ1_S)
store the activation block sum in f16, so a build with layer 47 at Q5_K turned
every perplexity chunk into NaN. Q6_K and the IQ types use an
f32 scale and are unaffected, so this file runs correctly on stock llama.cpp.

```
llama-quantize --allow-requantize \
  --imatrix <imatrix.gguf> \
  --tensor-type-file recipe-iq2_xs_m-v2.1.txt \
  --token-embedding-type q8_0 --output-tensor-type q6_k \
  MiMo-V2.6-Flash-MXFP4_MOE.gguf out.gguf IQ2_XS
```

`--allow-requantize` is required because the source experts are already
4-bit.

## Calibration

The importance matrix is
[Baekpica's](https://huggingface.co/Baekpica/MiMo-V2.6-Flash-RL-Mixed-Quant-GGUF),
collected from the full MXFP4 model on text and multimodal inputs. It covers
12,030 of 12,032 layer/expert slots; the two never observed are block 7
experts 13 and 184, which our own calibration runs never reached either, so
they look unrouted rather than under-sampled.

## Running it

Needs llama.cpp with `mimo2` support, including
[#28865](https://github.com/ggml-org/llama.cpp/pull/28865) (older loaders
reject the per-layer sliding-window pattern).

```
llama-server -m MiMo-V2.6-Flash-RL-IQ2_XS_M-v2.1-00001-of-00010.gguf \
  -ngl 99 -fa on -c 16384 -b 2048 -ub 2048 --jinja
```

Memory: about 92 GiB of weights leaves ~25 GiB on a 128 GB Spark. Contexts of
16K were fine throughout our testing. A `llama-bench` run with a 32K prompt
froze our machine (unified memory does not OOM-kill; it stalls), so measure
headroom before going much larger.

KV is cheap regardless of context: only 9 of the 48 layers are global
attention, 22.5 KB per token at F16 (2.7 GiB at 128K); the other 39 keep a
128-token sliding window.

## DFlash drafter

`MiMo-V2.6-Flash-RL-DFlash-Q8_0.gguf` is Xiaomi's 5-layer block-diffusion
drafter from the release's `dflash/` directory, at Q8_0. Stock llama.cpp does
not run DFlash for MiMo yet. Anyone porting it should know three things the
bundled Python example leaves out, all of which this file already encodes:

- **The mask token needs its learned vector.** The target's embedding row for
  the mask token (151675) is all zeros, never trained. The drafter was trained
  with the vector in `mask_embedding.pt`. This GGUF carries its own
  `token_embd` with that row replaced; a runtime that embeds mask slots through
  the target's table feeds the drafter zeros.
- **Partial rotary:** 64 of 128 head dimensions rotate (`partial_rotary_factor`
  0.5); `rope.dimension_count` is set.
- **Value scale 0.612** on the attention output (`attention.value_scale`).

Target features come from layers 0/11/23/35/47 (the residual stream before the
final norm), 8-token blocks, non-causal within the block, 1024-token sliding
window. `--spec-draft-p-min 0.7` (cut a block at the first low-confidence
token) was the best setting we measured; without it (on v1, 7 drafted) prose ran at 0.57x.

The three MTP blocks are included in the main file but not recommended.
MiMo's MTP heads are not chained: head k reads the target's hidden state,
with the token k places further ahead (SGLang pairs them this way).
llama.cpp's multi-head driver feeds each head the previous head's output
instead, which makes heads 2 and 3 draft noise. With the pairing fixed,
drafting one token gives 0.97x overall and deeper drafts are slower on
this MoE, so DFlash remains the faster option.

## Changes from v1

| | v1 | v2.1 |
|---|---:|---:|
| size | 90.1 GiB | 91.9 GiB |
| decode (tg32) | 26.3 t/s | 32.1 t/s |
| GSM8K | 95.0% | 95.6% |
| wiki PPL | 5.7824 | 5.7225 |
| attention | Q6_K | IQ4_XS |
| layer 47 experts | IQ2_XS / IQ2_S | Q6_K |
| imatrix | ours, from a Q2_K bootstrap | Baekpica's, from the full model |

## Architecture notes

48 layers, 39 sliding-window (window 128) and 9 global, interleaved. 64 query
heads at head_dim 192 (QK) / 128 (V); 4 KV heads on global layers, 8 on SWA.
256 routed experts, 8 active, no shared expert, sigmoid routing. Layer 0 is
dense.

The release stores the routed experts as MXFP4 (one E8M0 exponent per 32
values) under `quant_method: "fp8"` with `store_dtype: "mxfp4"`; QKV is
block-scaled FP8 sharded across TP=4. llama.cpp converts it natively as of
[#29257](https://github.com/ggml-org/llama.cpp/pull/29257).
