---
license: mit
language:
- en
pipeline_tag: automatic-speech-recognition
tags:
- audio
- speech-recognition
- transcription
- gguf
- moonshine
- streaming
- lightweight
library_name: ggml
base_model: UsefulSensors/moonshine-streaming-tiny
---

# Moonshine Streaming Tiny -- GGUF

GGUF conversions and quantisations of [`UsefulSensors/moonshine-streaming-tiny`](https://huggingface.co/UsefulSensors/moonshine-streaming-tiny) for use with **[CrispStrobe/CrispASR](https://github.com/CrispStrobe/CrispASR)**.

## Available variants

| File | Quant | Size | Notes |
|---|---|---|---|
| `moonshine-streaming-tiny.gguf` | F32 | 168 MB | Full precision |
| `moonshine-streaming-tiny-q4_k.gguf` | Q4_K | 31 MB | Quantized |

## Model details

- **Architecture:** Streaming encoder-decoder ASR. Raw-waveform audio frontend (no mel) + sliding-window transformer encoder (6L, 320d) + autoregressive transformer decoder (6L, 320d, SiLU-gated MLP, partial RoPE)
- **Parameters:** 34M
- **Languages:** English
- **License:** MIT
- **Source:** [`UsefulSensors/moonshine-streaming-tiny`](https://huggingface.co/UsefulSensors/moonshine-streaming-tiny)
- **Designed for:** Low-latency streaming ASR on edge devices

## Usage with CrispASR

```bash
./build/bin/crispasr --backend moonshine-streaming -m moonshine-streaming-tiny-q4_k.gguf -f audio.wav
```

## Notes

- Tokenizer (`tokenizer.bin`) must be in the same directory as the model file
- Streaming architecture: sliding-window attention with 80ms lookahead
- Audio frontend processes raw waveform (no mel spectrogram needed)

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [UsefulSensors/moonshine-streaming-tiny](https://huggingface.co/UsefulSensors/moonshine-streaming-tiny) — published by `UsefulSensors`.
- **Upstream licence:** `mit`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF/GGML). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
