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
base_model: facebook/omniASR-LLM-300M
---

# OmniASR LLM-300M — GGUF

GGUF conversion of [`facebook/omniASR-LLM-300M`](https://huggingface.co/facebook/omniASR-LLM-300M) for use with [CrispASR](https://github.com/CrispStrobe/CrispASR).

OmniASR is Meta's **multilingual ASR** model family supporting **1600+ languages**. Apache-2.0 license.

Autoregressive LLM decoder with language conditioning. Near-perfect English output.

## Files

| File | Size |
| --- | ---: |
| `omniasr-llm-300m-v2-f16.gguf` | 3.0 GB |
| `omniasr-llm-300m-v2-q4_k.gguf` | 1018 MB |
| `omniasr-llm-300m-v2-q8_0.gguf` | 1.7 GB |

## Quick Start

```bash
git clone https://github.com/CrispStrobe/CrispASR && cd CrispASR
cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc)

./build/bin/crispasr --backend omniasr-llm -m auto --auto-download -f audio.wav
```

## Conversion

Converted using CrispASR's converter scripts with fixed positional conv weight normalization (per-kernel-position norm, not per-output-channel).

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [facebook/omniASR-LLM-300M](https://huggingface.co/facebook/omniASR-LLM-300M) — published by `facebook`.
- **Upstream licence:** `apache-2.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF/GGML). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
