---
license: apache-2.0
language:
- en
- multilingual
tags:
- speech
- asr
- gguf
- ggml
- omniasr
pipeline_tag: automatic-speech-recognition
base_model: aadel4/omniASR-CTC-1B-v2
---

# OmniASR CTC-1B-v2 — GGUF

GGUF conversion of [`aadel4/omniASR-CTC-1B-v2`](https://huggingface.co/aadel4/omniASR-CTC-1B-v2) for use with [CrispASR](https://github.com/CrispStrobe/CrispASR).

OmniASR is Meta's **multilingual ASR** model family supporting **1600+ languages**. Apache-2.0 license.

**Recommended CTC model.** Q4_K uses a mixed-quantization recipe
(first 4 of 48 encoder layers kept at F16) that recovers nearly all
of Q8_0's quality at ~65% of the size. Plain uniform Q4_K is
preserved as `*_old.gguf` for reference.

## Files

| File | Size | Notes |
| --- | ---: | --- |
| `omniasr-ctc-1b-v2-q4_k.gguf` | **658 MB** | **Recommended.** Mixed Q4_K (first 4 encoder layers F16, rest Q4_K). 5% WER on JFK (one-word artefact `americans`→`americas`, model-internal). |
| `omniasr-ctc-1b-v2-q8_0.gguf` | 1007 MB | Byte-perfect against the FP32 transformers reference. Use this if 5% WER on edge cases is unacceptable. |
| `omniasr-ctc-1b-v2.gguf` | 1.8 GB | F16 source — feed to `crispasr-quantize` for custom recipes. |
| `omniasr-ctc-1b-v2-q4_k_old.gguf` | 551 MB | **Legacy.** Uniform Q4_K. Drops characters under CTC argmax pressure (~22.7% WER on JFK). Kept for reproducibility / size-vs-quality study; do not use for production. |

## Why mixed Q4_K?

CTC argmax decoding is structurally sensitive to weight drift —
small perturbations to encoder weights flip frame-level argmax
decisions toward the blank token, which manifests as missing
characters in the output (e.g. `"americans" → "amercans" → "americas"`).
Per-layer activation analysis (via `OMNIASR_DUMP_DIR=...`) shows
quantization noise enters at every encoder layer's matmul and
*compounds* through the residual stream, peaking at layers 36-47
even though the cause is upstream.

Counter-intuitively, keeping the *late* layers at F16 made things
worse — F16 math preserves accumulated upstream noise more faithfully
than Q4_K math does (Q4_K rounding occasionally lands back near the
right bin). The fix is to keep the *first* 4 layers at F16, stopping
noise from entering the residual stream. This is automatic in
`crispasr-quantize` for any GGUF whose `general.architecture` is
`omniasr-ctc`. Override via env vars:

```
CRISPASR_OMNIASR_KEEP_F16_HEAD=N   # default 4; 0 = uniform Q4_K
CRISPASR_OMNIASR_KEEP_F16_TAIL=N   # default 0; >0 is counter-productive
CRISPASR_OMNIASR_QUANT_ALL=1       # full quant, smaller, ~22% WER
```

Full diagnosis in
[`LEARNINGS.md`](https://github.com/CrispStrobe/CrispASR/blob/main/LEARNINGS.md)
under "Q4_K is too lossy as the default for CTC-decoded ASR" and
its follow-up "mixed Q4_K head-skip recovers nearly all Q8_0 quality".

## Quick Start

```bash
git clone https://github.com/CrispStrobe/CrispASR && cd CrispASR
cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc)

./build/bin/crispasr --backend omniasr -m auto --auto-download -f audio.wav
```

## Conversion

Converted using CrispASR's converter scripts with fixed positional conv weight normalization (per-kernel-position norm, not per-output-channel).

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [aadel4/omniASR-CTC-1B-v2](https://huggingface.co/aadel4/omniASR-CTC-1B-v2) — published by `aadel4`.
- **Upstream licence:** `apache-2.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF/GGML). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository. No training-content summary was found on the upstream model card at the time of writing; that documentation gap is upstream's and is not filled here.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
