---
license: apache-2.0
language:
- en
- multilingual
pipeline_tag: automatic-speech-recognition
tags:
- audio
- speech-recognition
- gguf
- gemma
- conformer
library_name: ggml
base_model: google/gemma-4-E4B-it
---

# Gemma-4-E4B-it — GGUF

GGUF conversion of [`google/gemma-4-E4B-it`](https://huggingface.co/google/gemma-4-E4B-it) for use with **[CrispStrobe/CrispASR](https://github.com/CrispStrobe/CrispASR)**.

E4B is the larger sibling of [`cstr/gemma4-e2b-it-GGUF`](https://huggingface.co/cstr/gemma4-e2b-it-GGUF): the **same `gemma4` architecture** (byte-identical 1024-dim USM Conformer audio tower) with a larger decoder. It runs on the same CrispASR backend with no code changes.

> The Gemma-4 **12B** model is a *different* architecture (`gemma4_unified`, 640-dim audio encoder) and is **not** supported by this backend.

## Available variants

| File | Quant | Size | Notes |
|---|---|---|---|
| `gemma4-e4b-it-f16.gguf` | F16 | ~14.6 GB | Full precision |
| `gemma4-e4b-it-q8_0.gguf` | Q8_0 | ~7.8 GB | Near-lossless quant |
| `gemma4-e4b-it-q4_k.gguf` | Q4_K | ~4.1 GB | Standard quant (auto-download default) |

## Model details

- **Architecture:** USM Conformer audio encoder (12L, 1024d, chunked-local attention with relative position bias, LightConv1d, ClippableLinear with QAT scalars) + Gemma4 LLM decoder (42L, 2560d, GQA 8Q/2KV, per-layer embeddings, hybrid sliding/full attention, GeGLU)
- **Parameters:** ~4B effective (~8B with embeddings)
- **Audio:** Gemma4AudioFeatureExtractor — 128-bin mel, 16 kHz, frame_length=320, hop=160, fft_length=512, semicausal padding, log(mel + mel_floor=0.001), no normalisation
- **Languages:** 140+ (ASR + speech translation)
- **License:** Apache 2.0
- **Source:** [`google/gemma-4-E4B-it`](https://huggingface.co/google/gemma-4-E4B-it)

## Usage

```bash
# Auto-download the Q4_K default and transcribe:
crispasr -m gemma4-e4b --auto-download -f audio.wav

# Or point at a local file (backend auto-detected from the GGUF):
crispasr --backend gemma4-e2b -m gemma4-e4b-it-q4_k.gguf -f audio.wav
```

The CrispASR backend is named `gemma4-e2b` (it serves the whole `gemma4` E2B/E4B family).

## What's included vs an upstream Gemma-4 GGUF

This GGUF is built specifically for ASR with CrispASR and includes the audio path that standard text/vision Gemma-4 GGUFs omit:

- 12-layer audio conformer encoder.
- Gemma4MultimodalEmbedder audio→LLM adapter (`embed_audio.embedding_projection`, pre-projection RMSNorm).
- Mel filterbank + Hann window baked into the GGUF.

Converted with [`models/convert-gemma4-e2b-to-gguf.py`](https://github.com/CrispStrobe/CrispASR/blob/main/models/convert-gemma4-e2b-to-gguf.py).

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [google/gemma-4-E4B-it](https://huggingface.co/google/gemma-4-E4B-it) — published by `google`.
- **Upstream licence:** `apache-2.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF/GGML). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
