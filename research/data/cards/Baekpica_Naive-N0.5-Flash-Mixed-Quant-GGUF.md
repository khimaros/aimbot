---
license: mit
base_model: NaiveAI/Naive-N0.5-Flash
pipeline_tag: text-generation
library_name: gguf
tags:
- gguf
- mixed-quant
- imatrix
- moe
- long-context
- ds4
- dgx-spark
---

# Naive-N0.5-Flash — Mixed Quant for DGX Spark

**Status: all four main GGUF shards and the companion Q8_0 DSpark draft are
available. Independent tensor checks and the post-upload BF16/converted-weight
numerical comparison are complete; measured results are below.**

Source: [NaiveAI/Naive-N0.5-Flash](https://huggingface.co/NaiveAI/Naive-N0.5-Flash),
revision `0235b3b5ff27422b1f57cdc2acddfaf643e08356`.
All 49 safetensors headers contain **308,859,589,056 parameters** in 36,568
source tensors. Routed experts account for 302,795,194,368 parameters.

The target is a resident mixed GGUF around the Qwen Q5 backbone budget of
83.275 decimal GB reference budget, aiming to leave memory for long contexts.
Completed native serving gates reach 512K; 1M remains unqualified.
The selected precision-first target is 86.908 GB, 3.633 GB above that reference. All 48 layers,
47 MoE layers, 256 experts per MoE layer and top-8 routing are retained.
All original experts, layers and parameters are retained.

## Target tensor recipe

Variant: `MQ87-IQ2XXS-IQ2XS-Q6Q8-BF16`.
Layer indices below are zero-based. [Machine-readable recipe](quant-recipe.json).

| Tensor group | Target | Purpose |
|---|---|---|
| Routed expert gate, all MoE layers | IQ2_XXS, 2.0625 BPW | Preserve the selected higher gate tier |
| Routed expert up, all MoE layers | IQ2_XXS, 2.0625 BPW | Match the selected gate precision |
| Routed expert down, all MoE layers | IQ2_XS, 2.3125 BPW | Protect return to the residual stream |
| Attention Q and O | Q6_K, 6.5625 BPW | Balance shared precision and resident capacity |
| Attention K and V | Q8_0, 8.5 BPW | Protect cached attention representations |
| Token embedding, output head, L0 dense FFN | Q8_0 | Protect token ingress and logits |
| DSA indexer projection matrices | BF16 | Preserve native token-selection computation |
| Router weights/correction bias, norms, indexer LayerNorm, sinks | F32 | Preserve routing and numerical controls |

The measured **tensor payload is 86,908,487,424 bytes =
86.908487 GB = 80.939836 GiB**, or
**2.251081 effective BPW**. The four complete GGUF files total
**86,960,547,072 bytes = 86.960547 GB / 80.988321 GiB**, including metadata,
tokenizer and alignment.

The selected layout promotes every gate to IQ2_XXS. Compared with the
83.301386 GB IQ1_M-interior target, this costs **3.607101 GB / 3.359375 GiB
(4.33%)**. Up and down precision and all shared-tensor formats are unchanged.

This recipe records the precision and storage layout used in the completed
conversion. The numerical comparison below was measured after the public upload.

## Model files

Download all four main shards into the same directory.

| Main GGUF shard | Bytes | GB |
|---|---:|---:|
| [Naive-N0.5-Flash-MQ87-00001-of-00004.gguf](Naive-N0.5-Flash-MQ87-00001-of-00004.gguf) | 20,942,674,048 | 20.942674 |
| [Naive-N0.5-Flash-MQ87-00002-of-00004.gguf](Naive-N0.5-Flash-MQ87-00002-of-00004.gguf) | 21,784,615,264 | 21.784615 |
| [Naive-N0.5-Flash-MQ87-00003-of-00004.gguf](Naive-N0.5-Flash-MQ87-00003-of-00004.gguf) | 21,784,615,264 | 21.784615 |
| [Naive-N0.5-Flash-MQ87-00004-of-00004.gguf](Naive-N0.5-Flash-MQ87-00004-of-00004.gguf) | 22,448,642,496 | 22.448642 |

[File manifest](main-file-manifest.json), [SHA256 checksums](SHA256SUMS),
[conversion provenance](conversion-provenance.json).

## Native 1M context and memory budget

The source has 39 sliding-window layers with a 128-token window and 9 DSA
layers selecting up to 2,048 history positions. DSA uses four GQA KV heads,
192-dimensional keys and 128-dimensional values. The source retains full
DSA K/V history; sparse attention reduces selected computation, not that
cache allocation. See the [official architecture](https://github.com/NaiveAI-Labs/Naive-N0.5-Flash).

Analytical one-sequence budget at 1,048,576 tokens and a 2,048-token prefill chunk:

| Component | GiB |
|---|---:|
| Main weight payload | 80.940 |
| Companion draft payload | 0.646 |
| All 9 DSA K/V histories, BF16 | 22.500 |
| 39 SWA caches, window plus prefill chunk | 0.404 |
| Indexer E4M3 codes plus original F32 row scales | 1.160 |
| Main activation, score and top-k workspace | 1.712 |
| Eight main partial checkpoints | 0.190 |

The native indexer stores the source's FP8-rounded codes with their original
F32 row scales. Actual-weight index/cache regressions pass; it does not add
another quantization step. The shared VMM owner reports 81.75 GiB including
byte-neutral aligned expert replacements and the draft. Draft scratch/cache,
allocator overhead, host services and headroom remain additional. This table
is an allocation plan, not a completed 1M serving proof.

The runtime uses bounded query/history tiles and incremental top-k: materializing
all 16-head index scores for a full prefill chunk at 1M would exceed the budget.
No SSD weight/embedding sidecar is planned. The Qwen SSD-PLE design does not
remove Naive's attention-cache requirement.

## Calibration

Calibration ran on eight A100 SXM 80GB GPUs with the pinned original BF16
checkpoint and original F32 router. Routed-input and post-SwiGLU second moments
were collected separately for every expert, with valid lengths and no padding.

The first **2,367,654 tokens** were processed through all 48 layers. A further
**1,581,699 tokens** broadened the language/domain mix through the first nine
layers. Inputs came from
[Solar Healing Mix](https://huggingface.co/datasets/Baekpica/Solar-Open2-120B-A15B-REAM-148E-Healing-Mix),
[Inkling Calibration](https://huggingface.co/datasets/Baekpica/Inkling-Small-Multimodal-Calibration),
[Nemotron Cascade tools](https://huggingface.co/datasets/nvidia/Nemotron-Cascade-SFT-Stage-2),
and [Wikipedia](https://huggingface.co/datasets/wikimedia/wikipedia), retokenized
with the original Naive tokenizer and chat template.

**12,015 / 12,032 layer/expert pairs** were naturally routed, with
**991,466,640 recorded selections**. The remaining **17** were measured
separately using **56,639 actual BF16 source-layer input states per expert**.
Their zero natural-route counts are retained; directly measured input and
SwiGLU moments provide their quantization importance. All other experts use
routed moments. All original experts and parameters are retained.

The final **48-document / 95,244-token** comparison set was checked against all
2,498 training records for exact content and truncation-prefix overlap,
including sequences of different lengths. Raw natural and direct moments were
independently recomputed before production conversion. Source BF16 layer
checks were bit-identical to the released eager graph, including a 2,304-token
DSA probe.

The original BF16 generation checks were completed before conversion finished.
The main GGUF files were then uploaded, followed by the numerical comparison
below.

## Measured checks

[Independent tensor audit](verification/main-tensor-audit.json) verified all
36,568 source payload hashes and their mapping into 613 GGUF tensors. All 248
F32 control tensors and 27 BF16 indexer matrices preserve their source values
exactly. One deterministic row from each of the 36,293 quantized source matrices
was independently re-encoded and compared with the actual GGUF bytes.

[Post-upload numerical comparison](verification/main-quality-summary.json)
processed all 48 layers on 48 clean documents totaling 95,244 tokens. Scores use
32 sampled next-token positions per document, totaling 1,536 positions.

| Measurement | Value |
|---|---:|
| BF16 sampled-position target NLL | 3.463912 |
| Mixed GGUF sampled-position target NLL | 3.385064 |
| Mean KL, BF16 → mixed GGUF | 0.597300 |
| Top-1 prediction agreement | 73.6979% |
| Mean logit cosine similarity | 0.967016 |

All scores were recomputed from the saved full-vocabulary logits. These sampled
observations do not establish a general quality ranking. Actual GGUF weights
were decoded with canonical ggml and evaluated in the original BF16/F32 eager
graph; the measurement does not exercise native quantized serving kernels.
The 108 sampled query positions at or beyond 2,048 had 75% top-1 agreement and
mean KL 0.439294. The longest evaluated documents were 4,096 tokens.

## Runtime

Target runtime: [Baekpica/ds4-dfm-rs](https://github.com/Baekpica/ds4-dfm-rs).
Verified implementation: [`6966dd80`](https://github.com/Baekpica/ds4-dfm-rs/tree/6966dd80)
([PR #70](https://github.com/Baekpica/ds4-dfm-rs/pull/70)); use this revision for the new family.
Native Naive CUDA execution is implemented on the Rust host. Bounded DGX
Spark gates cover continuous banks, partial prefix reuse, disk restart,
automatic XML tools and stream cancellation. The exact artifact retains
its Naive architecture identity and original indexer tensors.

The source configuration fixes 64 rotary dimensions, split-half RoPE,
different SWA/DSA theta values, value scale 0.707, sigmoid/noaux_tc routing
with correction bias, and per-row FP8 E4M3 indexer rounding. These are the source semantics used for the reference comparisons, including
the stable tie behavior of index selection.
The main checkpoint has no embedded MTP. The newly added external DSpark draft
package is described below and shares the target's embedding/output tensors.

## Verified DGX Spark native scope

GB10, driver 615.71.09, CUDA 13.3, user clock range 300–2200 MHz;
active samples 2184 or 2190 MHz. MQ87 revision `65b235a4`, resident shared
VMM owner, main-only workers, greedy generation and chunk 2048.
Each side of each performance pair uses three fresh processes, separate
warmups, shard/fixture hashes and full-vocabulary/token correctness proofs.

| Recorded workload | Mean before / after prefill tok/s | Mean before / after decode tok/s |
|---|---:|---:|
| 8192 book tokens + 32 generated, exact index-query packing off/on | 498.07 / 506.16 | 17.43 / 17.44 |
| 32768 book tokens + 32 generated, same off/on pair | 407.86 / 431.27 | 17.17 / 17.19 |

The retained campaign contains four useful prefill and three decode rounds.
Each preserves native logits/tokens and relevant target/indexer/draft state.
The latest 8K automatic comparison passes; the 32K first-decode timing
screen is inconclusive despite the repeated prefill gain. Ordinary decode
differences in this table lie within observed noise. These are exact fixture
measurements, not general throughput or DSpark acceleration claims.

Short HTTP gates at configured 8K pass two-bank overlap, partial prefix
reuse, fresh-process disk restart, XML tools and cancellation/recovery;
actual prompts contain 624–702 tokens. Explicit one-bank reuse also passes.
A separate one-bank 32K retrieval pilot processes 32512 input tokens and
passes warm and disk-restored continuations. At configured 256K with two
banks, a cold 261888-token request retrieves the distant phrase. Buffered
fresh-process disk continuations reach 262011 input tokens and restore
261901 cached tokens, returning the exact phrase with normal stops.
The original 64-token stream follow fails because reasoning exhausts its
budget; extended cold/warm streams differ by one leading newline. This
qualifies the recorded buffered fixture, not arbitrary stream budgets or
long full-logit parity. [256K receipts](https://github.com/Baekpica/ds4-dfm-rs/blob/6bc02011/docs/benchmarks/naive-2026-09-30/long-context.md).
At 512K with one bank, the cold buffered seed processes 523264 tokens;
follow and fresh disk restart process 523300 and 523441 tokens, restore
523277 cached tokens and stop with the complete phrase. Minimum available
host memory is 17.656 GiB over the initial worker lifetime. These gates
use MTP off and qualify one distant-fact fixture, not broad quality or
long full-logit parity. [512K receipts](https://github.com/Baekpica/ds4-dfm-rs/blob/10684310/docs/benchmarks/naive-2026-09-30/long-context.md).
The 1M request was stopped by the user after 210.9 monitored minutes of
prefill without an answer. The first boot had failed its memory guard; a
second boot with unchanged limits reached readiness. No completed 1M
retrieval or continuation is qualified. [1M stop receipt](https://github.com/Baekpica/ds4-dfm-rs/blob/777c7bdd/docs/benchmarks/naive-2026-09-30/long-context.md#1m-stopped-incomplete).

Six fresh native holdout cases also compare 192 full-vocabulary rows against
prerecorded pinned original BF16 logits from eight A100s: top-1 agreement
140/192, mean KL 0.438550, sampled NLL 3.392476 BF16 / 3.215876 native.
This is not a fresh DGX BF16 run or a quality ranking. It is distinct from
the 48-document canonical decoded-weight comparison above.

Receipts: [performance and serving reports](https://github.com/Baekpica/ds4-dfm-rs/tree/6966dd80/docs/benchmarks/naive-2026-09-30).

## Companion DSpark draft

[`NaiveAI/Naive-N0.5-Flash-FP8-Draft`](https://huggingface.co/NaiveAI/Naive-N0.5-Flash-FP8-Draft),
revision `b2b8ee9f5d6b3fd1dfba113d3a363138e37c83b0`, is included in
[draft/](draft/README.md). Despite FP8 in the source name, the downloaded
checkpoint contains **652,797,441 BF16 parameters in 63 tensors**.

| Draft group | Final format |
|---|---|
| Five-layer attention/FFN and eight-tap `fc` projection matrices | Q8_0 |
| Vanilla rank-256 Markov embedding and vocabulary projection | Q8_0 |
| Norms, trained mask embedding and confidence weight/bias | F32 |

The measured draft file is **693,777,632 bytes = 0.693778 GB / 0.646131 GiB**;
the payload is **693,770,244 bytes**. The main selected payload plus draft
payload is **87,602,257,668 bytes = 87.602258 GB / 81.585960 GiB**, before
GGUF metadata and alignment. The measured main and draft files together total
**87,654,324,704 bytes = 87.654325 GB / 81.634451 GiB**.
The target's token embedding and output head are shared and not duplicated. [Complete draft precision map](draft-recipe.json).

The source uses five SWA/1024 layers, seven-position blocks (one anchor plus
six proposals), target hidden taps `[1,7,14,20,26,32,39,45]`, a learned mask
vector, Markov correction and confidence tensors. Those mechanics and the
exact target/source revisions are preserved in the draft GGUF metadata and
original configuration. Hidden-tap capture, draft caches, activation scratch,
logits and resident repacks add to the weight-storage figure.

[Independent draft tensor checks](draft/verification/tensor-audit.json)
cover all 63 tensors and all 652,797,441 elements, including exact independent
Q8_0 scale/code reconstruction and F32 controls. A
[CPU source-graph probe](draft/verification/source-graph-probe.json)
exercises the packaged source with synthetic context and real target
anchor/output tensors. Native Naive DSpark integration passes explicit speculation, accepted-prefix
state, cache reuse and disk restart gates on GB10. Acceleration is not
qualified; automatic speculation remains off.

Actual BF16 target-prefix comparisons cover **182 cases / 1,092 proposals**.
Source-versus-Q8 draft top-1 agreement is **96.7033%** for the base path and
**98.3516%** with identical gold previous-token Markov input.
[Detailed natural-input measurements](draft/verification/natural-graph-probe.json).
These are teacher-forced draft-fidelity measurements, separate from native
speculative acceptance. An 8K/64-token diagnostic at depth six and margin
zero accepts 10 of 293 proposals and runs slower than ordinary decode;
this is not a matched repeated speed claim.

## References and license

Recipe precedents: [DS4 Mixed Quant collection](https://huggingface.co/collections/Baekpica/ds4-mixed-quant-for-spark),
[MiMo RL](https://huggingface.co/Baekpica/MiMo-V2.6-Flash-RL-Mixed-Quant-GGUF),
[Qwen Q5](https://huggingface.co/Baekpica/Qwen3.8-Flash-Next-Mixed-Quant-SSD-PLE-GGUF)
and [Motif-3](https://huggingface.co/Baekpica/Motif-3-GGUF).
DSA implementation reference: [antirez/ds4](https://github.com/antirez/ds4).

Model weights retain the upstream MIT license. Upstream implementation files
and calibration sources retain their respective licenses; they are recorded
in the reproduction package.
