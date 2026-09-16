---
license: apache-2.0
tags:
  - tts
  - omnivoice
  - gguf
  - crispasr
  - speech-synthesis
  - voice-cloning
language:
  - en
  - zh
  - ja
  - de
  - fr
  - es
  - multilingual
base_model: k2-fsa/OmniVoice
---

# OmniVoice GGUF

GGUF conversions of [k2-fsa/OmniVoice](https://huggingface.co/k2-fsa/OmniVoice) for the [CrispASR](https://github.com/CrispStrobe/CrispASR) `omnivoice` backend.

## Files

| File | Size | Description |
|------|------|-------------|
| `omnivoice-f16.gguf` | 1.23 GB | Main model (Qwen3-0.6B LLM + audio embeddings/heads), F16 |
| `omnivoice-q8_0.gguf` | 780 MB | Main model, Q8_0 quantized (embeddings/heads kept at F32) |
| `omnivoice-tokenizer-f16.gguf` | 403 MB | HiggsAudioV2 audio tokenizer (HuBERT + DAC codec), F16 |

## Usage

```bash
# Auto-download
./crispasr --backend omnivoice -m auto --tts "Hello world."

# Manual
./crispasr --backend omnivoice --model omnivoice-q8_0.gguf \
    --codec-model omnivoice-tokenizer-f16.gguf --tts "Hello world."
```

## Status

- Main model GGUF conversion (F16 + Q8_0)
- Qwen3 LLM forward pass (28L, flash_attn)
- Masked iterative code generation (32 steps)
- HiggsAudioV2 DAC decoder (codes to 24 kHz PCM)
- Special token handling (text_start/end, lang_start/end, etc.)
- Audio output: end-to-end text to WAV

**Parity note:** The C++ generation loop implements the basic masked iterative algorithm. Classifier-free guidance (the unconditional branch that OmniVoice uses for quality) is not yet implemented -- output quality does not yet match the Python reference. The Kaggle parity test confirmed the Python pipeline produces correct speech (ASR roundtrip: exact match).

## License

Apache-2.0 (same as k2-fsa/OmniVoice).

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [k2-fsa/OmniVoice](https://huggingface.co/k2-fsa/OmniVoice) — published by `k2-fsa`.
- **Upstream licence:** `apache-2.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
