---
license: apache-2.0
tags:
  - asr
  - speech-recognition
  - speaker-diarization
  - timestamps
  - gguf
  - crispasr
base_model: OpenMOSS-Team/MOSS-Transcribe-Diarize
language:
  - en
  - zh
  - multilingual
---

# MOSS-Transcribe-Diarize-0.9B GGUF

GGUF conversions of [OpenMOSS-Team/MOSS-Transcribe-Diarize](https://huggingface.co/OpenMOSS-Team/MOSS-Transcribe-Diarize) for [CrispASR](https://github.com/CrispStrobe/CrispASR).

Joint ASR + speaker diarization + timestamps in a single 0.9B model. Produces timestamped, speaker-labelled transcripts in one pass.

## Files

| File | Size | Description |
|------|------|-------------|
| `moss-transcribe-diarize-0.9b-f16.gguf` | 1.7 GB | Full precision (F16) |
| `moss-transcribe-diarize-0.9b-q8_0.gguf` | 1.4 GB | 8-bit quantized |
| `moss-transcribe-diarize-0.9b-q4_k.gguf` | 1.2 GB | 4-bit quantized (recommended) |
| `diff-harness-ref/moss-diarize-ref.gguf` | 9.5 MB | Diff harness reference (jfk.wav ground truth) |

## Usage

```bash
crispasr --backend moss-diarize -m auto -f audio.wav -osrt
```

With hotwords:

```bash
crispasr --backend moss-diarize \
  -m moss-transcribe-diarize-0.9b-q4_k.gguf \
  -f meeting.wav \
  --hotwords "MOSS,CrispASR" \
  -osrt
```

## Output Format

```
[00:00:00.320 --> 00:00:02.220]  (Speaker 1) And so, my fellow Americans,
[00:00:03.020 --> 00:00:07.640]  (Speaker 1) ask not what your country can do for you,
[00:00:08.110 --> 00:00:10.540]  (Speaker 1) ask what you can do for your country.
[00:00:11.440 --> 00:00:15.580]  (Speaker 2) And so, my fellow Americans, ask not...
```

## Architecture

Stock Whisper encoder (24L, 80 mel, Conv1d) with 4x temporal merge, VQAdaptor, time markers every 5s, and Qwen3-0.6B LM decoder. Output: `[timestamp][Sxx]text[timestamp]` format with speaker labels.

## Diff Harness

All 4 stages pass at cos=1.000 on both F32 and Q4_K:

| Stage | cos_min | max_abs |
|-------|---------|---------|
| mel_spectrogram | 1.000000 | 1.20e-04 |
| conv_stem_out | 1.000000 | 6.11e-05 |
| encoder_output | 1.000000 | 1.24e-04 |
| audio_embeds | 1.000000 | 1.35e-02 |

## Conversion

```bash
python models/convert-moss-transcribe-diarize-to-gguf.py \
  --input OpenMOSS-Team/MOSS-Transcribe-Diarize \
  --output moss-transcribe-diarize-0.9b-f16.gguf

crispasr-quantize moss-transcribe-diarize-0.9b-f16.gguf \
                  moss-transcribe-diarize-0.9b-q4_k.gguf q4_k
```

## License

Apache-2.0 (same as the base model).

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [OpenMOSS-Team/MOSS-Transcribe-Diarize](https://huggingface.co/OpenMOSS-Team/MOSS-Transcribe-Diarize) — published by `OpenMOSS-Team`.
- **Upstream licence:** `apache-2.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository. No training-content summary was found on the upstream model card at the time of writing; that documentation gap is upstream's and is not filled here.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
