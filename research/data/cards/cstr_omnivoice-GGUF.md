---
license: other
license_name: omnivoice-and-boson-tokenizer-terms
license_link: https://huggingface.co/k2-fsa/OmniVoice/blob/c5fdb5ccb189668d56333f77ba2629f4cd7535f4/README.md
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
./crispasr --backend omnivoice -m auto --accept-license omnivoice-terms --tts "Hello world."

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

The inference code license does **not** describe the weight bundle. The original
[OmniVoice model card](https://huggingface.co/k2-fsa/OmniVoice/blob/c5fdb5ccb189668d56333f77ba2629f4cd7535f4/README.md#license)
states that its code is Apache-2.0 and its pretrained model weights are CC-BY-NC.
The bundled HiggsAudioV2 tokenizer separately carries the
[Boson Higgs Audio 2 Community License](https://huggingface.co/k2-fsa/OmniVoice/blob/c5fdb5ccb189668d56333f77ba2629f4cd7535f4/audio_tokenizer/LICENSE),
which includes additional use and user-count conditions.

These GGUF files inherit their respective upstream terms; conversion and
quantization grant no additional rights. This bundle is **not Apache-2.0** and
plain NC acceptance does not cover the tokenizer's additional terms. CrispASR
requires distinct `omnivoice-terms` acceptance for managed downloads. Supplying it affirms that you accept both components' terms, are eligible to use them, and will comply with all applicable conditions, including obtaining any separately required permission. The switch grants no additional rights. Main weights remain non-commercial absent separate permission; the companion's Boson conditions also apply. The main card does not
specify a CC-BY-NC version, so we do not infer one.

License correction, 2026-10-20: the previous blanket Apache-2.0 label confused
code and weight licensing. This metadata correction changes no model bytes.

### Tokenizer attribution and full companion terms

Built with Higgs Materials licensed from Boson AI USA, Inc., Copyright Boson AI USA, Inc., All Rights Reserved and Meta Llama 3 licensed under the Meta Llama 3 Community License, Copyright Meta Platforms, Inc., All Right Reserved. Based on Meta Llama 3.

The Higgs Audio 2 tokenizer is the companion listed above. Copies of its
[Boson agreement](LICENSE.boson-higgs-audio-2.txt), incorporated
[Meta Llama 3 agreement](LICENSE.meta-llama-3.txt),
[acceptable-use policy](USE-POLICY.meta-llama-3.md), and [NOTICE](NOTICE.txt)
accompany these files. Boson section 2 requires expanded permission above
100,000 annual active users under its licensee/affiliate wording; section 1.b.v
restricts improving other LLMs with the materials or outputs/results. The full
terms, including attribution and naming conditions, control. Acceptance is an
affirmation of compliance, not a waiver or a certificate for every use.

License-documentation update, 2026-10-22: corrected the stale Apache-only
provenance footer and added companion notices/full terms. No model bytes changed.

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [k2-fsa/OmniVoice](https://huggingface.co/k2-fsa/OmniVoice) — published by `k2-fsa`.
- **Upstream licences:** Apache-2.0 describes the upstream inference code. Main model weights are CC-BY-NC (version unspecified by the pinned upstream card); the HiggsAudioV2 tokenizer has the separate Boson/Meta terms described above. Each weight component inherits its applicable upstream terms.
- **What was done here:** format conversion and/or quantisation only (GGUF). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
