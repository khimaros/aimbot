---
license: apache-2.0
language:
- ar
- da
- de
- el
- en
- es
- fi
- fr
- he
- hi
- id
- it
- ja
- km
- ko
- lo
- ms
- my
- nl
- no
- pl
- pt
- ru
- sv
- sw
- th
- tl
- tr
- vi
- zh
tags:
- tts
- text-to-speech
- speech-synthesis
- gguf
- crispasr
base_model: openbmb/VoxCPM2
pipeline_tag: text-to-speech
---

# VoxCPM2 GGUF

GGUF conversion of [openbmb/VoxCPM2](https://huggingface.co/openbmb/VoxCPM2) for use with [CrispASR](https://github.com/CrispStrobe/CrispASR).

## Model Details

- **Architecture:** TSLM (28L MiniCPM-4) + RALM (8L) + LocEnc (12L) + LocDiT (12L) + AudioVAE
- **Parameters:** ~2B
- **Output:** 48 kHz mono PCM
- **Languages:** 30 languages (Arabic, Burmese, Chinese, Danish, Dutch, English, Finnish, French, German, Greek, Hebrew, Hindi, Indonesian, Italian, Japanese, Khmer, Korean, Lao, Malay, Norwegian, Polish, Portuguese, Russian, Spanish, Swahili, Swedish, Tagalog, Thai, Turkish, Vietnamese) plus 9 Chinese dialects
- **License:** Apache 2.0
- **Voice Cloning:** Supported via reference audio

## Features

- **Tokenizer-free:** Directly generates audio patches via diffusion (no discrete audio tokens)
- **High quality:** CFM-based generation with classifier-free guidance
- **Multilingual:** 30-language support via CJK-split BPE tokenizer (73k vocab)
- **Voice cloning:** Zero-shot voice cloning from reference audio

## Usage with CrispASR

```bash
# Zero-shot TTS
crispasr -m voxcpm2-f16.gguf \
    --tts "Hello, this is VoxCPM2 speaking." \
    --tts-output output.wav

# Quantized (smaller, faster)
crispasr -m voxcpm2-q4_k.gguf \
    --tts "Hello world" --tts-output output.wav
```

## Files

| File | Size | Description |
|------|------|-------------|
| `voxcpm2-f16.gguf` | 4.63 GB | F16 weights (full precision) |
| `voxcpm2-q4_k.gguf` | ~1.5 GB | Q4_K quantized (faster, slightly lower quality) |
| `voxcpm2-q8_0.gguf` | 2.83 GB | Q8_0 quantized (near-F16 quality) |
| `voxcpm2-q8_0-locdit-f16.gguf` | 3.03 GB | Q8_0 with the LocDiT diffusion head kept in F16 — experimental mixed-precision Vulkan recipe (see below) |
| `voxcpm2-ref.gguf` | 371 KB | Reference activation dump for numerical validation |

### Which file on a Vulkan GPU?

Historical T4 Vulkan component measurements found CFM per audio step of 70.2 ms
for Q8_0 versus 59.4 ms for the mixed recipe at ten steps. An eight-step run
measured 46.7 ms. These component timings do **not** establish speech quality or
an accepted end-to-end speedup. The mixed file was built with
`crispasr-quantize voxcpm2-f16.gguf out.gguf q8_0 --tensor-type "^locdit\.=f16"`.
A previous CPU synthesis roundtrip is not GPU acceptance.

**Validation update, 2026-10-09:** matched real T4 tests at ten steps and seed 2
produced repeated tokens in the **Nemotron ASR transcripts** of the short test
sentence for both Q8_0 and the mixed recipe. Six of sixteen exact primary ASR
cases passed. This rejected gate is not proof that synthesized audio audibly
stutters: a later fixed-audio comparison found **both Parakeet and Qwen3
transcribe every one of 22 original Python/native CPU/GPU controls exactly**
across three resampling paths, while Nemotron retains errors. Resampling alone
does not resolve the discrepancy. The completed original NVIDIA float32 and
native F16 comparison reads **all 22 VoxCPM2 controls correctly**; native Q4
reads only 8/22. Original and F16 normalized words agree on all 26 tested clips,
and fresh/reused sessions agree. The repeated tokens are therefore attributable
to the native Nemotron Q4 recognizer on these fixed controls. Critical RNNT
precision guards are being tested before changing that quant or its defaults.
The published Q4 primary gate remains rejected while that recognizer is
repaired. This diagnosis does not certify eight steps, Intel B390 performance,
or complete original/native waveform parity. Defaults remain ten steps.

[Original NVIDIA/F16/Q4 inputs, features, encoder states and complete transcripts](https://huggingface.co/cstr/crispasr-regression-fixtures/blob/10e579dedf52a16a159cbc5d35e17f8bffa77190/tts-asr/nemotron-reference-20261009/proof.zip)
(SHA256 `7762f2a73d8ae7dad05d667fbf0bca393a0b3b7ad622b1b1f09473fa8f5d0463`).

[All 234 fixed-audio transcripts, recognizer pins and resampling controls](https://huggingface.co/cstr/crispasr-regression-fixtures/blob/0b434ca1ea6c34c9b462be4d3e689ba1713381e9/tts-asr/frontdoor-diagnostic-20261009/proof.zip)
(SHA256 `3dd2f988e327dd30bf3ae608edc7611e52aedf3a8374a3ea6e2f288342110b98`).

[Immutable raw PCM, transcripts, backend traces and recipe evidence](https://huggingface.co/cstr/crispasr-regression-fixtures/blob/449ed355010eddb8dcedef6c2ab0fa62431ebeb7/voxcpm2/path-diagnostic-20261009-v6/proof.zip)
(SHA256 `f52e5fbc49a0654bdcd13da6660c8e0841fbe87e80eb0cc158d74801339a5abc`).
See [CrispASR #461](https://github.com/CrispStrobe/CrispASR/issues/461) for hardware follow-up.

## Numerical Validation

The `voxcpm2-ref.gguf` file contains intermediate activation tensors captured from the PyTorch reference implementation. Used with `crispasr-diff` to validate the C++ inference path:

```bash
crispasr-diff voxcpm2-tts voxcpm2-f16.gguf voxcpm2-ref.gguf samples/jfk.wav
```

Historical F16 transformer-stage check: **12 pass, 0 fail** (TSLM, RALM, LocEnc, LocDiT, projections). This stage check does not certify complete generated speech, the current mixed quant, or every GPU backend.

Captured stages: `text_input_ids`, `locenc_in`, `locenc_out`, `enc_to_lm`, `tslm_layer_0_out`, `tslm_layer_27_out`, `tslm_prefill_out`, `ralm_prefill_out`, `lm_to_dit_hidden`, `res_to_dit_hidden`, `cfm_step0_z`, `cfm_step0_result`, `stop_logits_step0`.

## Architecture

```
Text → BPE tokenize → TSLM (28L causal MiniCPM-4, GQA 16h/2kv, LongRoPE)
                       ↓
                    FSQ bottleneck (tanh→round→linear)
                       ↓
              RALM (8L causal, no RoPE, GQA 16h/2kv)
                       ↓
         Projections: lm_to_dit + res_to_dit → mu [2048]
                       ↓
    LocDiT (12L bidirectional, CFM Euler solver, 10 steps, cfg=2.0)
                       ↓
              Predicted latent patch [4 frames × 64 dims]
                       ↓
         LocEnc (12L bidirectional) → next TSLM input
                       ↓ (AR loop until stop)
              AudioVAE decoder → 48 kHz PCM
```

## Conversion

Converted using `models/convert-voxcpm2-to-gguf.py` from the CrispASR repository:

```bash
python models/convert-voxcpm2-to-gguf.py \
    --input openbmb/VoxCPM2 \
    --output voxcpm2-f16.gguf
```

## Acknowledgments

Original model by [OpenBMB](https://github.com/OpenBMB/VoxCPM2). Apache 2.0 license.

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [openbmb/VoxCPM2](https://huggingface.co/openbmb/VoxCPM2) — published by `openbmb`.
- **Upstream licence:** `apache-2.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
