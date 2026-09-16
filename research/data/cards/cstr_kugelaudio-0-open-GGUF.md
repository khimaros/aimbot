---
license: mit
language:
  - en
  - de
  - fr
  - es
  - it
  - pt
  - nl
  - pl
  - ru
  - uk
  - cs
  - ro
  - hu
  - sv
  - da
  - fi
  - "no"
  - el
  - bg
  - sk
  - hr
  - sr
  - tr
tags:
  - tts
  - text-to-speech
  - speech-synthesis
  - gguf
  - crispasr
  - kugelaudio
base_model: kugelaudio/kugelaudio-0-open
pipeline_tag: text-to-speech
---

# KugelAudio-0-Open GGUF

GGUF conversions of [kugelaudio/kugelaudio-0-open](https://huggingface.co/kugelaudio/kugelaudio-0-open) for use with [CrispASR](https://github.com/CrispStrobe/CrispASR).

## Files

| File | Quant | Size | Notes |
|------|-------|------|-------|
| `kugelaudio-0-open-f16.gguf` | F16 | 16.1 GB | Full precision, inference-only (no encoders) |
| `kugelaudio-0-open-q4_k.gguf` | Q4_K | 5.3 GB | 4-bit quantized, inference-only (no encoders) |

Both files contain the inference-only components (`--no-encoders`): Qwen2.5-7B language model, 4-layer DiT diffusion head, acoustic connector, and acoustic VAE decoder. Encoder weights (for voice cloning from raw audio) are omitted since the open-source release only supports pre-encoded voices.

## Architecture

```
Text → Qwen2.5-7B (28L, 3584d, GQA 28/4)
  → AR decode with constrained token set
  → 4-layer DiT diffusion head (AdaLN, SwiGLU, v-prediction)
  → 20-step SDE-DPMSolver++ (cosine beta schedule)
  → Acoustic VAE decoder (6-stage ConvNeXt, 3200x upsample)
  → 24 kHz mono PCM
```

- **23 languages**: en, de, fr, es, it, pt, nl, pl, ru, uk, cs, ro, hu, sv, da, fi, no, el, bg, sk, hr, sr, tr
- **License**: MIT
- **Output**: 24 kHz mono PCM
- **Classifier-free guidance**: cfg_scale=3.0 (default)

## Usage with CrispASR

```bash
# Synthesize speech
crispasr --backend kugelaudio \
  -m kugelaudio-0-open-q4_k.gguf \
  --tts "Hello, this is a test of the speech synthesis system." \
  --tts-output output.wav

# With auto-download
crispasr --backend kugelaudio -m auto \
  --tts "Hallo, dies ist ein Test." -l de
```

## Conversion

Converted with:
```bash
python models/convert-kugelaudio-to-gguf.py \
  --input kugelaudio/kugelaudio-0-open \
  --output kugelaudio-0-open-f16.gguf \
  --no-encoders --type f16

crispasr-quantize kugelaudio-0-open-f16.gguf kugelaudio-0-open-q4_k.gguf q4_k
```

## Original Model

- **Paper/repo**: [kugelaudio/kugelaudio-0-open](https://huggingface.co/kugelaudio/kugelaudio-0-open)
- **Architecture**: Based on Microsoft VibeVoice — hybrid AR + diffusion TTS
- **Parameters**: ~7B (Qwen2.5-7B backbone)
- **Training data**: Undisclosed
- **License**: MIT
