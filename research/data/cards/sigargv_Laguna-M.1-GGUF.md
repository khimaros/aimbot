---
license: apache-2.0
base_model: poolside/Laguna-M.1
pipeline_tag: text-generation
tags:
- gguf
- llama.cpp
- ik_llama.cpp
- laguna
- laguna-m.1
- moe
- imatrix
- poolside
---

<p align="center">
  <img alt="Poolside Laguna M.1 banner" src="https://poolside.ai/assets/laguna/laguna-m1-banner.svg" width="800">
</p>

<p align="center">
  <a href="https://huggingface.co/poolside/Laguna-M.1"><strong>Upstream BF16 safetensors</strong></a> ·
  <a href="https://poolside.ai/blog/laguna-a-deeper-dive"><strong>Release blog</strong></a> ·
  <a href="https://poolside.ai/assets/laguna/laguna-m1-xs2-technical-report.pdf"><strong>Technical report</strong></a> ·
  <a href="https://github.com/ikawrakow/ik_llama.cpp/pull/2003"><strong>Merged ik_llama.cpp support</strong></a>
</p>

# Laguna M.1 Community GGUF imatrix quants

This is an independent community GGUF conversion and quantization upload, not an
official Poolside release.

[Laguna M.1](https://huggingface.co/poolside/Laguna-M.1) is Poolside's Apache-2.0
sparse MoE coding model: 225B total parameters, 23B activated parameters per
token, 70 global-attention layers, 256 sparse experts after the first three
dense layers, top-k=16 routing, RoPE with YaRN, softplus attention output
gating, and a 262,144-token context window.

This repository contains imatrix GGUF quantizations of Laguna M.1 for local
experimentation with long-context coding and agentic workloads. The files here
are derivative GGUF artifacts built from Poolside's upstream BF16 safetensors;
for model architecture, intended use, benchmark methodology, and serving notes,
start with the upstream model card, release blog, and technical report linked
above.

These GGUFs were produced during the Laguna support work that landed in
[ikawrakow/ik_llama.cpp#2003](https://github.com/ikawrakow/ik_llama.cpp/pull/2003),
"Add Laguna M.1 GGUF support". The PR was merged into ik_llama.cpp on
2026-06-22 as merge commit `b47b90d0be80981f6f476c997afbdfab99bba6c7`.
At the time of quantization, the support branch commit was
`be7d53ceec0c823c07d540e21828d7d187b02d3b`.

Laguna GGUF support is now available in ik_llama.cpp builds that include that
merge commit or newer. Other runners still need equivalent Laguna GGUF support;
the vanilla-compatible quant names below are chosen so that they should also be
useful if equivalent Laguna support lands in upstream llama.cpp later.

## License and attribution

The upstream Laguna M.1 checkpoint is licensed under the
[Apache License 2.0](https://huggingface.co/poolside/Laguna-M.1/blob/main/LICENSE.md),
copyright 2026 Poolside. This GGUF repository uses the same Apache-2.0 license
metadata and is based on [poolside/Laguna-M.1](https://huggingface.co/poolside/Laguna-M.1)
at upstream revision `5bb2892a899809fd903829735f927207da358f2f`.

Poolside's model names, branding, and logos remain Poolside's. This is an
independent community GGUF conversion and quantization upload, not an official
Poolside release.

## Quantization summary

| Quant | Status | Size | PPL | KL divergence | Same top |
| --- | ---: | ---: | ---: | ---: | ---: |
| `IQ1_S_R4` | uploaded | 43.54 GiB | 17.029677 +/- 0.150383 | 1.771976 +/- 0.006119 | 55.882% +/- 0.137 |
| `IQ1_S` | uploaded | 43.91 GiB | 20.451320 +/- 0.194807 | 1.920889 +/- 0.006747 | 53.988% +/- 0.138 |
| `IQ2_XS` | uploaded | 63.07 GiB | 12.307893 +/- 0.111532 | 1.325747 +/- 0.005793 | 63.043% +/- 0.133 |
| `IQ2_S` | uploaded | 63.08 GiB | 12.470802 +/- 0.113326 | 1.340981 +/- 0.005827 | 62.743% +/- 0.134 |
| `IQ2_K_R4` | uploaded | 64.35 GiB | 13.397426 +/- 0.128657 | 1.387314 +/- 0.006164 | 62.577% +/- 0.134 |
| `IQ2_M` | uploaded | 69.47 GiB | 12.101664 +/- 0.109158 | 1.294993 +/- 0.005730 | 63.149% +/- 0.133 |
| `Q2_K` | uploaded | 77.66 GiB | 12.881872 +/- 0.123074 | 1.330646 +/- 0.005951 | 63.376% +/- 0.133 |
| `IQ3_XXS` | uploaded | 81.98 GiB | 11.366560 +/- 0.103969 | 1.217616 +/- 0.005754 | 65.037% +/- 0.132 |
| `IQ3_S` | uploaded | 91.81 GiB | 10.821543 +/- 0.095954 | 1.169696 +/- 0.005503 | 65.583% +/- 0.131 |
| `IQ3_K_R4` | uploaded | 91.81 GiB | 11.210677 +/- 0.102925 | 1.181941 +/- 0.005637 | 65.717% +/- 0.131 |
| `Q3_K_S` | uploaded | 91.81 GiB | 11.531644 +/- 0.106822 | 1.214226 +/- 0.005712 | 65.297% +/- 0.132 |
| `Q3_K_M` | uploaded | 100.91 GiB | 11.246193 +/- 0.103685 | 1.186657 +/- 0.005657 | 65.816% +/- 0.131 |
| `IQ4_XS` | uploaded | 112.80 GiB | 4.615172 +/- 0.033625 | 0.067625 +/- 0.000706 | 88.899% +/- 0.087 |
| `IQ4_KS_R4` | uploaded | 113.20 GiB | 4.598246 +/- 0.033452 | 0.063984 +/- 0.000683 | 89.217% +/- 0.086 |
| `IQ4_NL` | uploaded | 119.26 GiB | 4.605535 +/- 0.033524 | 0.066829 +/- 0.000720 | 89.049% +/- 0.086 |
| `IQ4_K_R4` | uploaded | 119.26 GiB | 4.617317 +/- 0.033749 | 0.058367 +/- 0.000667 | 89.440% +/- 0.085 |
| `Q4_K_S` | uploaded | 119.91 GiB | 4.599690 +/- 0.033491 | 0.065115 +/- 0.000694 | 89.013% +/- 0.086 |
| `Q4_K_M` | uploaded | 127.33 GiB | 4.602518 +/- 0.033538 | 0.061163 +/- 0.000667 | 89.209% +/- 0.086 |
| `IQ5_KS_R4` | uploaded | 139.04 GiB | 4.608804 +/- 0.033738 | 0.046126 +/- 0.000597 | 90.056% +/- 0.083 |
| `IQ5_KS` | uploaded | 139.04 GiB | 4.608804 +/- 0.033738 | 0.046126 +/- 0.000597 | 90.056% +/- 0.083 |
| `Q5_K_S` | uploaded | 145.10 GiB | 4.598543 +/- 0.033604 | 0.048429 +/- 0.000630 | 89.865% +/- 0.083 |
| `IQ5_K_R4` | uploaded | 145.10 GiB | 4.624008 +/- 0.033904 | 0.041238 +/- 0.000541 | 90.446% +/- 0.081 |
| `IQ5_K` | uploaded | 145.10 GiB | 4.624008 +/- 0.033904 | 0.041238 +/- 0.000541 | 90.446% +/- 0.081 |
| `Q5_K_M` | uploaded | 149.26 GiB | 4.607405 +/- 0.033688 | 0.045827 +/- 0.000562 | 90.036% +/- 0.083 |
| `IQ6_K` | uploaded | 174.48 GiB | 4.633778 +/- 0.033986 | 0.028084 +/- 0.000440 | 91.120% +/- 0.079 |
| `Q6_K` | uploaded | 172.85 GiB | 4.647079 +/- 0.034139 | 0.029602 +/- 0.000429 | 90.977% +/- 0.079 |
| `Q8_0` | uploaded | 223.63 GiB | 4.633481 +/- 0.033995 | 0.022906 +/- 0.000376 | 91.302% +/- 0.078 |
| `BF16` | uploaded | 420.71 GiB | 4.683023 +/- 0.034506 | baseline | baseline |

Rows are ordered by effective bit-width. Queued rows with pending sizes are
placed by quant family and expected BPW.

## Imatrix and calibration corpus

The imatrix used for these quants is the 256-chunk public Q8_0 run:

- `laguna-m1-q8-public-v1-256-gatefix.imatrix`
- SHA256: `449427a1a4c5d2480d98e3fcccc3884bd3aafa325d937741a162adf84e7e7eed`
- Source model for imatrix collection: corrected Q8_0 GGUF of Laguna M.1
- Chunks: 256
- Tokens processed: 1,048,576
- Diagnostic imatrix collection PPL: `2.6084 +/- 0.00786`

The original imatrix was collected with `llama-imatrix` from
`Laguna-M.1-Q8_0-00001-of-00010.gguf` using `-c 4096`, `-ngl 999`,
`--chunks 256`, `--no-warmup`, and all available CPU threads. The derived
`gatefix` imatrix is a mechanically augmented copy of that original 256-chunk
file (`c8a98474542e2ae7636d7ad0578552398eec3d769b6f9a2981f111a4ba06af12`).
Laguna's fused up/gate graph records the shared activation stream under the
up-projection tensor name, so the original imatrix had the up-projection entries
but not all matching gate-projection names. The fix clones:

- `.ffn_up.weight` to `.ffn_gate.weight`
- `.ffn_up_exps.weight` to `.ffn_gate_exps.weight`
- `.ffn_up_shexp.weight` to `.ffn_gate_shexp.weight`

No numeric values were otherwise changed. Entry count went from 691 original
entries to 828 derived entries, adding 137 cloned gate entries. This removes the
shared-expert gate missing-weight warnings during quantization; the remaining
missing imatrix entries are `output.weight` and `token_embd.weight`, which are
explicitly kept at `q6_K` for these publication quants.

The calibration corpus is `laguna-m1-imatrix-calibration-v1.txt`:

- Size: 6,526,884 bytes
- Lines: 130,856
- SHA256: `4d478cc0d10da862b0f70040b0c1d948fb88ddac83a5307059e61f02c206622f`

The corpus was built by `build_laguna_imatrix_corpus.py`, with a companion
manifest at `laguna-m1-imatrix-calibration-v1.manifest.json`. It combines:

- A public baseline: `ubergarm-imatrix-calibration-corpus-v02.txt`
  (`6fd2187f10ab1b742cf85eaf35cf9fa20863a557f68451d6535195774cf1fd0a`,
  1,699,017 bytes). That baseline is described as combining v5 rc calibration
  text with exllamav3 standard calibration data.
- Local ik_llama.cpp source from the pre-merge `laguna-m1-support` branch, commit
  `be7d53ceec0c823c07d540e21828d7d187b02d3b`, with a clean worktree. The
  included source set covers the Laguna converter/runtime path, imatrix code,
  quantizer code, CUDA MMQ/MMVQ dispatch, common CLI/chat helpers, and IQK
  quantization code.
- A deterministic Laguna-specific supplement: 1,200 generated blocks
  (12 topics x 10 languages/formats x 10 operations), 2,060,879 bytes, SHA256
  `9aa0b10f45e79d7a7bfc2373375eec1890b92c8c1f76a74d9fa4c1b0bc8aeb5c`.
  The supplement focuses on Laguna M.1/XS.2 metadata, partial RoPE, SWA/global
  attention differences, MoE routing and deferred experts, GGUF tensor naming,
  CUDA inference, KV-cache quantization, speculative decoding, imatrix
  collection, and publication/reproducibility tasks.

For provenance, the builder also downloaded and hashed
`calibration_datav3.txt` from bartowski and `calibration_data_v5_rc.txt` from
Tristan Dampf/Kalomaze, but did not concatenate them separately because they are
already represented through the ubergarm v02 baseline. The Poolside technical
report text/PDF, private shell history, download logs, local machine notes, and
the earlier ad hoc `laguna-m1-code-calib.txt` were deliberately excluded.

## Compatibility notes

- `Q2_K`, `IQ2_M`, `IQ2_XS`, `IQ2_S`, `IQ3_S`, `Q4_K_M`, `IQ4_XS`, `Q5_K_M`, `Q6_K`, and `IQ1_S` are intended as broad compatibility artifacts once a runner has Laguna GGUF support.
- `IQ1_S` and `IQ1_S_R4` are experimental very-low-bit artifacts for quality/size probing.
- `IQ2_K_R4`, `IQ3_K_R4`, `IQ4_KS_R4`, `IQ4_K_R4`, `IQ5_KS_R4`, `IQ5_K_R4`, `IQ5_KS`, `IQ5_K`, and `IQ6_K` are ik_llama.cpp/Spark/Vector-oriented quants selected for direct CUDA MMQ fast paths in ik_llama.cpp.
- The `*_R4` quants are not intended as universal llama.cpp artifacts today; use them with ik_llama.cpp or another runner that explicitly supports those tensor types.

## Metrics

The PPL, KL divergence, and same-top percentages in the table come from the
shared 64-chunk validation harness against the BF16 GGUF baseline logits on a
fixed slice of the public calibration corpus. The first completed rows were run on
Vast, with the remaining smaller and larger rows continuing on Spark and
Vector using the same corpus, BF16 KL base, and parser. They are intended as reproducibility and regression checks
for these artifacts, not as a general benchmark of Laguna M.1. The imatrix
collection PPL above is recorded only as imatrix provenance and is not comparable
to these publication validation metrics.

Validation tries full GPU offload first and falls back to lower `-ngl` values if
the quant is too large for full offload on the validation machine. The validation
logs and results TSVs record the offload setting used where applicable.

Current smoke tests for completed rows produced coherent outputs on both
smoke prompts: an iterative Python Fibonacci function and the arithmetic answer
`17 + 25 = 42`. All uploaded non-BF16 quant rows above have completed the
same validation harness; `BF16` is the reference row used for KL divergence.

## Reproducibility

Quantization command shape:

```bash
llama-quantize \
  --keep-split \
  --partial-requant \
  --imatrix laguna-m1-q8-public-v1-256-gatefix.imatrix \
  --output-tensor-type q6_K \
  --token-embedding-type q6_K \
  Laguna-M.1-BF16-00001-of-00010.gguf \
  Laguna-M.1-<QUANT>-imatrix-public-v1.gguf \
  <QUANT> \
  $(nproc)
```

Evaluation command shape:

```bash
llama-perplexity \
  -m Laguna-M.1-<QUANT>-imatrix-public-v1-00001-of-00010.gguf \
  -f laguna-m1-imatrix-calibration-v1.txt \
  -c 4096 \
  --chunks 64 \
  -ngl 99 \
  -b 64 \
  -ub 16 \
  --defer-experts \
  --seed 42 \
  --kl-divergence \
  --kl-divergence-base bf16-reference-logprobs.ctx4096.chunks64.bin
```
