---
license: apache-2.0
language:
- en
tags:
- gguf
- audio
- speech-recognition
- hubert
- wav2vec2
- ctc
- automatic-speech-recognition
base_model: facebook/hubert-large-ls960-ft
pipeline_tag: automatic-speech-recognition
---

# HuBERT Large (GGUF)

GGUF conversion of [facebook/hubert-large-ls960-ft](https://huggingface.co/facebook/hubert-large-ls960-ft) for use with [CrispASR](https://github.com/CrispStrobe/CrispASR).

## Model Details

- **Architecture**: HuBERT — wav2vec2-style CNN (7L, 512-dim) + 24-layer transformer (1024-dim, 16 heads, pre-norm) + CTC head
- **Parameters**: ~316M
- **Training**: Self-supervised pre-training on LibriSpeech 960h, fine-tuned with CTC loss
- **Language**: English only
- **License**: Apache 2.0

## Usage

```bash
crispasr --backend wav2vec2 -m hubert-large-ls960-ft-q4_k.gguf -f audio.wav
```

## Files

| File | Size | JFK Result |
|------|------|-----------|
| hubert-large-ls960-ft-f16.gguf | 627 MB | perfect |
| hubert-large-ls960-ft-q4_k.gguf | 212 MB | perfect |

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [facebook/hubert-large-ls960-ft](https://huggingface.co/facebook/hubert-large-ls960-ft) — published by `facebook`.
- **Upstream licence:** `apache-2.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
