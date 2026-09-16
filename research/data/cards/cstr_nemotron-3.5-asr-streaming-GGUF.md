---
license: openmdw-1.1
language:
  - ar
  - bg
  - cs
  - da
  - de
  - el
  - en
  - es
  - et
  - fi
  - fr
  - he
  - hi
  - hr
  - hu
  - it
  - ja
  - ko
  - lt
  - lv
  - nb
  - nl
  - nn
  - pl
  - pt
  - ro
  - ru
  - sk
  - sl
  - sv
  - th
  - tr
  - uk
  - vi
  - zh
tags:
  - asr
  - speech-recognition
  - gguf
  - streaming
  - fastconformer
  - rnnt
  - multilingual
  - crispasr
pipeline_tag: automatic-speech-recognition
base_model: nvidia/nemotron-3.5-asr-streaming-0.6b
---

# Nemotron-3.5-ASR-Streaming-0.6B GGUF

GGUF conversion of [nvidia/nemotron-3.5-asr-streaming-0.6b](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b) for use with [CrispASR](https://github.com/CrispStrobe/CrispASR).

## Model details

**Architecture:** Cache-Aware Streaming FastConformer encoder (24 layers, d=1024, 8 heads) + RNN-T decoder (2-layer LSTM, hidden=640) + joint network (640 → 13088 vocab).

**Languages:** 39 languages, selected via `prompt_kernel` MLP conditioning (one-hot lang → 2048-dim hidden → 1024-dim encoder conditioning):

| Code | Language | Code | Language | Code | Language |
|------|----------|------|----------|------|----------|
| ar-AR | Arabic | fr-CA | French (CA) | nn-NO | Norwegian (NN) |
| bg-BG | Bulgarian | fr-FR | French (FR) | pl-PL | Polish |
| cs-CZ | Czech | he-IL | Hebrew | pt-BR | Portuguese (BR) |
| da-DK | Danish | hi-IN | Hindi | pt-PT | Portuguese (PT) |
| de-DE | German | hr-HR | Croatian | ro-RO | Romanian |
| el-GR | Greek | hu-HU | Hungarian | ru-RU | Russian |
| en-GB | English (GB) | it-IT | Italian | sk-SK | Slovak |
| en-US | English (US) | ja-JP | Japanese | sl-SI | Slovenian |
| es-ES | Spanish (ES) | ko-KR | Korean | sv-SE | Swedish |
| es-US | Spanish (US) | lt-LT | Lithuanian | th-TH | Thai |
| et-EE | Estonian | lv-LV | Latvian | tr-TR | Turkish |
| fi-FI | Finnish | nb-NO | Norwegian (NB) | uk-UA | Ukrainian |
| | | nl-NL | Dutch | vi-VN | Vietnamese |
| | | | | zh-CN / zh-TW | Chinese |

**Key properties:**
- Sample rate: 16 kHz mono
- 128 mel filterbank features, n_fft=512, hop=160 (10ms), win=400 (25ms)
- 8x time downsampling (causal) → 80ms frame duration
- Streaming: cache-aware attention with 4 context presets (see below)
- Vocab: 13087 SentencePiece tokens + 1 blank (pure RNN-T, no TDT durations)
- Native punctuation and capitalization
- License: [OpenMDW-1.1](https://github.com/linux-foundation/open-model-developer-weight-license/blob/main/LICENSE.md) (permissive, commercial OK)

## Files

| File | Size | Description |
|------|------|-------------|
| `nemotron-3.5-asr-streaming-0.6b-f16.gguf` | 1.3 GB | F16 weights (full precision, F32 pre-encode) |
| `nemotron-3.5-asr-streaming-0.6b-q4_k.gguf` | 458 MB | **Recommended.** Q4_K quantized, identical text output, ~2x faster. |

Pre-encode weights are kept at F32 in both GGUFs (F16 causes 1.56 max accumulation error across the 4352-dim projection).

## Usage with CrispASR

```bash
# Auto-download (Q4_K, 458 MB)
crispasr --backend nemotron -m auto --auto-download -f audio.wav

# Or download manually
huggingface-cli download cstr/nemotron-3.5-asr-streaming-GGUF \
  nemotron-3.5-asr-streaming-0.6b-q4_k.gguf --local-dir models/

# Transcribe (English, default)
crispasr --backend nemotron \
  -m models/nemotron-3.5-asr-streaming-0.6b-q4_k.gguf \
  -f audio.wav

# Transcribe in German
crispasr --backend nemotron \
  -m models/nemotron-3.5-asr-streaming-0.6b-q4_k.gguf \
  -f audio.wav -l de-DE

# Beam search (default is greedy)
crispasr --backend nemotron -m auto --auto-download -f audio.wav --beam-size 4

# Streaming from stdin
ffmpeg -i audio.wav -f s16le -ar 16000 -ac 1 - | \
  crispasr --backend nemotron -m auto --auto-download --stream
```

## Streaming encoder

The model supports true cache-aware streaming via the NeMo `cache_last_channel` + `cache_last_time` architecture. Enable with:

```bash
CRISPASR_NEMOTRON_STREAMING=1 crispasr --backend nemotron -m model.gguf -f audio.wav
```

Four attention context presets trade latency for accuracy (published WER from NVIDIA's Open ASR Leaderboard):

| Preset | Left ctx | Right ctx | Chunk size | Approx latency | Published WER |
|--------|----------|-----------|------------|----------------|---------------|
| 0 (default) | 56 frames | 3 frames | 4 frames | ~160 ms | 7.67% |
| 1 | 56 frames | 0 frames | 1 frame | ~80 ms | 8.43% |
| 2 | 56 frames | 6 frames | 7 frames | ~560 ms | 7.07% |
| 3 | 56 frames | 13 frames | 14 frames | ~1120 ms | 6.93% |

Select preset: `CRISPASR_NEMOTRON_CONTEXT_PRESET=3` (default: 0)

The same GGUF works for all presets — the context window is a runtime knob, not a retraining artifact.

### Environment variables

| Variable | Effect |
|----------|--------|
| `CRISPASR_NEMOTRON_STREAMING=1` | Enable cache-aware streaming encoder |
| `CRISPASR_NEMOTRON_CONTEXT_PRESET=N` | Attention context preset (0-3) |
| `CRISPASR_NEMOTRON_NO_WINDOW_MASK=1` | Disable banded attention mask (bidirectional fallback) |
| `CRISPASR_NEMOTRON_DEBUG=1` | Enable encoder/decoder debug prints |

## Architecture

```
Audio (16kHz mono)
  → Mel spectrogram (128 bins, 10ms hop, no normalization)
  → Pre-encode (3x causal Conv2d, 8x downsample, Linear 4352→1024, F32 weights)
  → 24x Cache-Aware FastConformer block:
      FFN1(½) → MHA(rel_pos, cache-aware) → DWConv(k=9, causal, LN) → FFN2(½) → LN
  → Prompt kernel (MLP: concat(enc[1024], lang_onehot[128]) → 2048 → ReLU → 1024)
  → RNN-T decoder:
      Prediction: Embed(13088, 640) + 2-layer LSTM(640)
      Joint: enc(1024→640) + pred(640→640) → ReLU → Linear(640→13088)
  → Greedy / beam search decode
```

**Streaming caches (per layer):**
- `cache_last_channel`: post-FFN1 output (up to L frames), used as K/V context for asymmetric attention (Q from new frames only)
- `cache_last_time`: last K-1=8 frames of post-GLU signal before depthwise conv, prepended instead of zero-padding

## Conversion

```bash
python models/convert-nemotron-to-gguf.py \
  --nemo nvidia/nemotron-3.5-asr-streaming-0.6b \
  --output nemotron-3.5-asr-streaming-0.6b-f16.gguf

crispasr-quantize nemotron-3.5-asr-streaming-0.6b-f16.gguf \
  nemotron-3.5-asr-streaming-0.6b-q4_k.gguf q4_k
```

## Quality reference (JFK 11s)

| Variant | Output |
|---------|--------|
| F16 | And so my fellow Americans ask not what your country can do for you. \<en-US\> Ask what you can do for your country. \<en-US\> |
| Q4_K | And so my fellow Americans ask not what your country can do for you. \<en-US\> Ask what you can do for your country. \<en-US\> |
| Streaming (preset 0) | And so, my fellow Americans ask not what your country can do for you. \<en-US\> Ask what you can do for your country. \<en-US\> |

F16 and Q4_K produce identical text. Streaming output has minor punctuation differences but same content.

## Original model

- **Source:** [nvidia/nemotron-3.5-asr-streaming-0.6b](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b)
- **License:** [OpenMDW-1.1](https://github.com/linux-foundation/open-model-developer-weight-license/blob/main/LICENSE.md) — permissive, commercial use OK, derivatives OK with attribution
- **Training data:** 530k hours (NVIDIA Riva ASR set + Granary)
