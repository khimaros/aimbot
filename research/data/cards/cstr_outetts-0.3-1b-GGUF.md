---
license: cc-by-nc-sa-4.0
tags:
  - tts
  - text-to-speech
  - outetts
  - wavtokenizer
  - gguf
  - crispasr
base_model: OuteAI/OuteTTS-0.3-1B
pipeline_tag: text-to-speech
---

# OuteTTS-0.3-1B GGUF

GGUF quantizations of [OuteAI/OuteTTS-0.3-1B](https://huggingface.co/OuteAI/OuteTTS-0.3-1B) for use with [CrispASR](https://github.com/CrispStrobe/CrispASR).

## Files

| File | Size | Quant | Notes |
|---|---|---|---|
| `outetts-0.3-1b-f16.gguf` | 2.4 GB | F16 | Full precision (reference quality) |
| `outetts-0.3-1b-q8_0.gguf` | 1.2 GB | Q8_0 | Recommended — near-lossless quality |
| `outetts-0.3-1b-q5_k.gguf` | 783 MB | Q5_K | Good quality, balanced size |
| `outetts-0.3-1b-q4_k.gguf` | 802 MB | Q4_K | Smallest — verified intelligible (requires CrispASR >= cbe208fa) |
| `wavtokenizer-decoder-f16.gguf` | 130 MB | F16 | WavTokenizer decoder (required companion) |

The talker GGUF contains the OLMo-1B LLM. The WavTokenizer decoder GGUF is always needed as a companion file. Q8_0 is recommended for best quality/size balance. Q4_K works but may occasionally shift word boundaries on short utterances.

**Note:** Q4_K requires CrispASR commit `cbe208fa` or later, which fixed a WavTokenizer activation bug (SiLU -> GELU in ResNet blocks) that previously degraded quantized output.

## Usage with CrispASR

```bash
# Build CrispASR
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j$(nproc) --target crispasr-cli

# Create a speaker profile from reference audio
python tools/reference_backends/outetts_create_speaker.py \
    --audio ref.wav --text "transcript of the reference audio" \
    --out speaker.json

# Synthesize with voice cloning
./build/bin/crispasr --backend outetts \
    -m outetts-0.3-1b-q8_0.gguf \
    --codec-model wavtokenizer-decoder-f16.gguf \
    --voice speaker.json \
    --tts "Hello, how are you today?" \
    --tts-output hello.wav --seed 42
```

## Architecture

- **LLM**: OLMo-1B (16 layers, 2048 hidden, 16 MHA heads, SwiGLU FFN, parameter-free LayerNorm, RoPE)
- **Codec**: WavTokenizer single-codebook VQ-GAN (4096 entries, 512-d, 75 tokens/sec)
- **Decoder**: Vocos backbone (ConvNeXt + pos_net with GroupNorm/GELU ResBlocks) + ISTFTHead
- **Output**: 24 kHz mono PCM
- **License**: CC BY 4.0

## Conversion

```bash
# From HuggingFace model
python models/convert-outetts-to-gguf.py \
    --input OuteAI/OuteTTS-0.3-1B \
    --output outetts-0.3-1b-f16.gguf

python models/convert-wavtokenizer-to-gguf.py \
    --input OuteAI/wavtokenizer-large-75token-interface \
    --output wavtokenizer-decoder-f16.gguf

# Quantize
crispasr-quantize outetts-0.3-1b-f16.gguf outetts-0.3-1b-q8_0.gguf q8_0
```

## Licence — CC-BY-NC-SA-4.0 (corrected 2026-08-02)

This repository previously declared `license: cc-by-4.0`, dropping the
`NC` and `SA` terms. The upstream checkpoint
[`OuteAI/OuteTTS-0.3-1B`](https://huggingface.co/OuteAI/OuteTTS-0.3-1B) is
**CC-BY-NC-SA-4.0**, and format conversion does not relax it.

What that means here:

- **NonCommercial** — no commercial use of these weights.
- **ShareAlike** — anything you distribute that contains these weights must
  carry CC-BY-NC-SA-4.0 too. The term is viral.
- **Attribution** — credit OuteAI.
