---
license: mit
tags:
  - speaker-diarization
  - pyannote
  - gguf
  - crispasr
base_model: pyannote/segmentation-3.0
pipeline_tag: voice-activity-detection
library_name: ggml
---

# Pyannote Segmentation 3.0 — GGUF

Native GGUF port of [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0) for speaker diarization.

## Model details

| Property | Value |
|---|---|
| Architecture | SincNet + 4× biLSTM + Linear + LogSoftmax |
| Format | GGUF (F32) |
| Size | 5.7 MB |
| Tensors | 41 |
| Output classes | 7 (powerset mapping → 3 speakers) |
| Input | 10 s mono 16 kHz audio frames |

The model performs joint voice-activity detection, speaker segmentation, and overlapped-speech detection on short audio chunks. Downstream clustering then produces full-file speaker diarization.

## Usage with CrispASR

```bash
crispasr \
  --diarize-method pyannote \
  --sherpa-segment-model pyannote-seg-3.0.gguf \
  audio.wav
```

## Provenance

Weights were exported directly from the original PyTorch checkpoint (`pyannote/segmentation-3.0`) into GGUF format, preserving full F32 precision across all 41 tensors.

## License

MIT — same as the original pyannote-audio segmentation-3.0 model.

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0) — published by `pyannote`.
- **Upstream licence:** `mit`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF/GGML). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
