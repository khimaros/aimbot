---
license: apache-2.0
language:
- en
- de
- fr
- es
- ja
- zh
- ko
- pt
- it
- ru
- ar
- hi
- nl
- pl
- sv
- da
- fi
- el
- cs
- hu
tags:
- tts
- text-to-speech
- speech-synthesis
- gguf
- crispasr
- zonos
- zyphra
- voice-cloning
- emotion-control
library_name: crispasr
base_model: Zyphra/Zonos-v0.1-transformer
pipeline_tag: text-to-speech
---

# Zonos v0.1 Transformer — GGUF

GGUF conversion of [Zyphra/Zonos-v0.1-transformer](https://huggingface.co/Zyphra/Zonos-v0.1-transformer) for use with [CrispASR](https://github.com/CrispStrobe/CrispASR) and [CrisperWeaver](https://github.com/CrispStrobe/CrisperWeaver).

## Model

Zonos v0.1 is a ~500M-parameter text-to-speech model trained on 200k+ hours of multilingual speech. It delivers expressive, high-quality synthesis with fine-grained control over:

- **Speaker cloning** from a few seconds of reference audio
- **Emotion control** (happiness, sadness, disgust, fear, surprise, anger, neutral)
- **Speaking rate** (phonemes/second)
- **Pitch variation** (pitch standard deviation)
- **Audio quality** (fmax parameter)

Output is native **44.1 kHz** mono PCM via a 9-codebook DAC decoder.

### Architecture

1. **Text input** → eSpeak phonemization → phoneme embeddings
2. **Prefix conditioner**: concatenates conditioning embeddings (phonemes, speaker, emotion, fmax, pitch_std, rate, language) through projection + LayerNorm
3. **AR backbone**: 26-layer GPT-style transformer (d=2048, GQA 16q/4kv, SwiGLU, LayerNorm with bias, RoPE) generates 9 interleaved DAC codebook streams with delay pattern
4. **Classifier-free guidance** (CFG): both conditioned and unconditioned prefixes are decoded; logits are interpolated with configurable scale (default 2.0)
5. **DAC decoder**: separate GGUF converts 9-codebook RVQ codes → 44.1 kHz PCM

## Files

| File | Size | Description |
|------|------|-------------|
| `zonos-v0.1-transformer-f16.gguf` | 3.1 GB | Full-precision (F16) — reference quality |
| `zonos-v0.1-transformer-q4_k.gguf` | 872 MB | Q4_K quantised — ~3.5x smaller, good quality |

### Required companion

Zonos needs the **DAC 44.1 kHz decoder** GGUF for audio output. Use `dac-44khz.gguf` from [cstr/dia-1.6b-GGUF](https://huggingface.co/cstr/dia-1.6b-GGUF/resolve/main/dac-44khz.gguf) (same codec, shared between Zonos and Dia backends).

## Usage

### CrispASR CLI

```bash
# Download
crispasr -m auto --backend zonos

# Synthesize
crispasr --backend zonos \
  -m zonos-v0.1-transformer-q4_k.gguf \
  --tts-codec dac-44khz.gguf \
  --tts "Hello, this is a test of the Zonos text to speech system." \
  -o output.wav

# With emotion control
crispasr --backend zonos \
  -m zonos-v0.1-transformer-q4_k.gguf \
  --tts-codec dac-44khz.gguf \
  --tts "I'm so happy to see you!" \
  --emotion "0.8,0,0,0,0,0,0,0.2" \
  -o happy.wav

# With voice cloning
crispasr --backend zonos \
  -m zonos-v0.1-transformer-f16.gguf \
  --tts-codec dac-44khz.gguf \
  --voice reference.wav \
  --tts "Cloned voice output." \
  -o cloned.wav
```

### CrisperWeaver (Flutter GUI)

Download from Model Management, select on the Synthesize screen, and set `dac-44khz.gguf` as the codec companion.

### C API

```c
#include "crispasr.h"

// Open session
crispasr_session* s = crispasr_session_open("zonos-v0.1-transformer-q4_k.gguf", "zonos");
crispasr_session_set_codec_path(s, "dac-44khz.gguf");

// Configure (optional)
crispasr_session_set_temperature(s, 0.7);

// Synthesize
int n_samples;
float* pcm = crispasr_session_synthesize(s, "Hello world", &n_samples);
// ... write pcm to WAV ...
free(pcm);
crispasr_session_free(s);
```

## Conditioning Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `pitch_std` | 0-400 | 45 | Pitch variation. 20-45 = normal, 60-150 = expressive |
| `speaking_rate` | 0-40 | 15 | Phonemes per second. 10 = slow, 15 = normal, 30 = fast |
| `fmax` | 0-24000 | 24000 | Maximum frequency. 22050 for voice cloning |
| `cfg_scale` | 0-10 | 2.0 | Classifier-free guidance scale |
| `emotion` | 8 floats | neutral | [happiness, sadness, disgust, fear, surprise, anger, other, neutral] |
| `temperature` | 0-2 | 0.0 | Sampling temperature (0 = greedy) |

## Conversion

Converted from the upstream PyTorch checkpoint using:

```bash
python models/convert-zonos-to-gguf.py \
  --input Zyphra/Zonos-v0.1-transformer \
  --output zonos-v0.1-transformer-f16.gguf
```

Quantised with:

```bash
crispasr-quantize zonos-v0.1-transformer-f16.gguf zonos-v0.1-transformer-q4_k.gguf q4_k
```

## License

Apache 2.0 (same as [Zyphra/Zonos-v0.1-transformer](https://huggingface.co/Zyphra/Zonos-v0.1-transformer)).

## Links

- Upstream model: [Zyphra/Zonos-v0.1-transformer](https://huggingface.co/Zyphra/Zonos-v0.1-transformer)
- Blog post: [zyphra.com/post/beta-release-of-zonos-v0-1](https://www.zyphra.com/post/beta-release-of-zonos-v0-1)
- Engine: [CrispASR](https://github.com/CrispStrobe/CrispASR)
- App: [CrisperWeaver](https://github.com/CrispStrobe/CrisperWeaver)
