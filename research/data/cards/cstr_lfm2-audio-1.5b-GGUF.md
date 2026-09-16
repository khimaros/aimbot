---
license: other
license_name: lfm-open-license-v1.0
license_link: https://huggingface.co/LiquidAI/LFM2.5-Audio-1.5B/blob/main/LICENSE
language:
  - en
tags:
  - gguf
  - crispasr
  - asr
  - tts
  - speech-to-speech
  - audio
  - liquid-ai
  - lfm2
base_model: LiquidAI/LFM2.5-Audio-1.5B
---

# LFM2.5-Audio-1.5B GGUF

GGUF quantizations of [LiquidAI/LFM2.5-Audio-1.5B](https://huggingface.co/LiquidAI/LFM2.5-Audio-1.5B) for [CrispASR](https://github.com/crispasr/crispasr).

LFM2.5-Audio is Liquid AI's end-to-end multimodal speech model supporting ASR (speech-to-text), TTS (text-to-speech), and speech-to-speech in a single 1.5B parameter model. This is the **English** base variant. Achieves 7.53 average WER across standard English ASR benchmarks, competitive with models 3x its size.

## Architecture

| Component | Details |
|-----------|---------|
| Encoder | 17-layer FastConformer (512-dim, 8 heads, rel-pos attention, dw-striding 8x subsampling) |
| Adapter | LayerNorm + Linear(512->2048) + GELU + Linear(2048->2048) |
| Backbone | 16-layer LFM2 hybrid conv+attention (2048-dim, 32 heads / 8 KV heads, RoPE theta=1M) |
| Depthformer | 6-layer transformer (1024-dim) with 8-codebook Mimi audio token generation |
| Audio codec | Mimi (8 codebooks, 24 kHz) |
| Parameters | 1.5B total |

## Available quantizations

| File | Quant | Size | Notes |
|------|-------|------|-------|
| `lfm2-audio-1.5b-f16.gguf` | F16 | ~3.1 GB | Full precision reference |
| `lfm2-audio-1.5b-q8_0.gguf` | Q8_0 | ~1.7 GB | High quality |
| `lfm2-audio-1.5b-q5_k.gguf` | Q5_K | ~1.6 GB | Recommended (verified identical output) |

Note: Q4_K is too aggressive for the English variant and causes early EOS. Use Q5_K or Q8_0.

## Usage with CrispASR

```bash
# Transcribe English audio
./crispasr -m lfm2-audio-1.5b-q5_k.gguf -f audio.wav -l en

# Or with auto-download
./crispasr --backend lfm2-audio -m auto -f audio.wav
```

## Conversion

Converted from the original safetensors using:

```bash
python models/convert-lfm2-audio-to-gguf.py \
    --input LiquidAI/LFM2.5-Audio-1.5B \
    --output lfm2-audio-1.5b-f16.gguf

# Quantize
./crispasr-quantize lfm2-audio-1.5b-f16.gguf lfm2-audio-1.5b-q5_k.gguf q5_k
```

## License

**LFM Open License v1.0** - Commercial use permitted for entities with annual revenue under $10M USD. See the [upstream license](https://huggingface.co/LiquidAI/LFM2.5-Audio-1.5B/blob/main/LICENSE) for full terms.

Components include: Apache-2.0 (NVIDIA NeMo), MIT (Kyutai Moshi), CC-BY-4.0 (Canary checkpoint).

## Credits

- Model weights: [LiquidAI](https://liquid.ai)
- GGUF conversion: [CrispASR](https://github.com/crispasr/crispasr)

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [LiquidAI/LFM2.5-Audio-1.5B](https://huggingface.co/LiquidAI/LFM2.5-Audio-1.5B) — published by `LiquidAI`.
- **Upstream licence:** `other`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository. No training-content summary was found on the upstream model card at the time of writing; that documentation gap is upstream's and is not filled here.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
