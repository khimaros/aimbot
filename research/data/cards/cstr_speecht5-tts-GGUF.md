---
license: mit
language:
- en
- de
base_model:
- microsoft/speecht5_tts
pipeline_tag: text-to-speech
tags:
- tts
- text-to-speech
- speecht5
- hifi-gan
- gguf
- crispasr
library_name: ggml
---

# SpeechT5 TTS — GGUF (ggml-quantised)

GGUF / ggml conversion of [`microsoft/speecht5_tts`](https://huggingface.co/microsoft/speecht5_tts) for use with **[CrispStrobe/CrispASR](https://github.com/CrispStrobe/CrispASR)**.

SpeechT5 is a lightweight (~80M param) encoder-decoder TTS model:
- **Text encoder** — 12-layer transformer (768d) with relative positional encoding
- **Speech decoder** — 6-layer AR decoder generating continuous mel frames (no codebook tokens)
- **Postnet** — 5-layer Conv1d + BatchNorm + Tanh residual stack
- **HiFi-GAN vocoder** — 4x upsample (rates [4,4,4,4]) with MRF resblocks to 16 kHz PCM

Speaker conditioning via 512-d x-vector (e.g. from `Matthijs/cmu-arctic-xvectors`). Deterministic output (greedy decoding, no sampling).

Released under **MIT** license.

## Files

| File | Language | Size | Notes |
|---|---|---:|---|
| `speecht5-tts-f16.gguf` | English | 301 MB | encoder + decoder + postnet + HiFi-GAN vocoder |
| `speecht5-german-f16.gguf` | German | 300 MB | German fine-tune, same architecture |
| `speaker.bin` | — | 2 KB | Default 512-d x-vector for speaker conditioning |

## Quick start

```bash
# 1. Build CrispASR
git clone https://github.com/CrispStrobe/CrispASR
cd CrispASR
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j --target crispasr-cli

# 2. Download model + speaker
huggingface-cli download cstr/speecht5-tts-GGUF speecht5-tts-f16.gguf speaker.bin --local-dir .

# 3. Synthesize
./build/bin/crispasr --backend speecht5 -m speecht5-tts-f16.gguf \
    --voice speaker.bin \
    --tts "Hello, how are you today?" \
    --tts-output hello.wav
```

Or with auto-download:
```bash
./build/bin/crispasr -m speecht5 --auto-download \
    --tts "The quick brown fox jumps over the lazy dog." \
    --tts-output fox.wav
```

## Python binding

```python
from crispasr import Session

sess = Session("speecht5-tts-f16.gguf")
sess.set_voice("speaker.bin")
pcm = sess.synthesize("Hello world.")
sess.write_wav("hello.wav", pcm)
```

## Architecture details

See [`docs/architecture.md#speecht5`](https://github.com/CrispStrobe/CrispASR/blob/main/docs/architecture.md#speecht5) for the full architecture breakdown.

## Conversion

Converted with `models/convert-speecht5-tts-to-gguf.py` from the CrispASR repo. The HiFi-GAN vocoder weights are from [`microsoft/speecht5_hifigan`](https://huggingface.co/microsoft/speecht5_hifigan) and are embedded in the same GGUF file.

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [microsoft/speecht5_tts](https://huggingface.co/microsoft/speecht5_tts) — published by `microsoft`.
- **Upstream licence:** `mit`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF/GGML). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
