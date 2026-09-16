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
- lightweight
library_name: ggml
base_model: UsefulSensors/moonshine-base
---

# Moonshine Base -- GGUF

GGUF conversions and quantisations of [`UsefulSensors/moonshine-base`](https://huggingface.co/UsefulSensors/moonshine-base) for use with **[CrispStrobe/CrispASR](https://github.com/CrispStrobe/CrispASR)**.

## Available variants

| File | Quant | Size | Notes |
|---|---|---|---|
| `moonshine-base.gguf` | F32 | 235 MB | Full precision |
| `moonshine-base-q4_k.gguf` | Q4_K | 40 MB | Best size/quality tradeoff |

## Model details

- **Architecture:** Conv1d stem + 8L transformer encoder + 8L transformer decoder (416d, 8 heads, partial RoPE, SiLU/GELU)
- **Parameters:** 61M
- **Languages:** English only
- **License:** MIT
- **Source:** [`UsefulSensors/moonshine-base`](https://huggingface.co/UsefulSensors/moonshine-base)

## Usage with CrispASR

```bash
# Auto-download (English tiny only)
./build/bin/crispasr --backend moonshine -m auto -f audio.wav

# Explicit model path
./build/bin/crispasr --backend moonshine -m moonshine-base-q4_k.gguf -f audio.wav
```

## Notes

- Moonshine models run on CPU only (GPU not needed for these small models)
- Tokenizer (`tokenizer.bin`) must be in the same directory as the model file
- Base models use head_dim=52 which works on CPU flash_attn

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [UsefulSensors/moonshine-base](https://huggingface.co/UsefulSensors/moonshine-base) — published by `UsefulSensors`.
- **Upstream licence:** `mit`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF/GGML). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
