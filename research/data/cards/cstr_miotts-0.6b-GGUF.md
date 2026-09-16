---
language:
- en
- ja
license: apache-2.0
library_name: crispasr
base_model:
- Aratako/MioTTS-0.6B
- Aratako/MioCodec-25Hz-44.1kHz-v2
pipeline_tag: text-to-speech
tags:
- speech
- tts
- gguf
- crispasr
---

# MioTTS-0.6B GGUF (v2 codec — 44.1kHz)

GGUF conversion of [Aratako/MioTTS-0.6B](https://huggingface.co/Aratako/MioTTS-0.6B) + [Aratako/MioCodec-25Hz-44.1kHz-v2](https://huggingface.co/Aratako/MioCodec-25Hz-44.1kHz-v2) for [CrispASR](https://github.com/CrispStrobe/CrispASR).

Single GGUF containing the LLM (Qwen3, 28 layers, 1024d) and the MioCodec-v2 waveform decoder with UpSampler. Produces **44.1 kHz mono audio**.

## Files

| File | Size | Description |
|------|------|-------------|
| `miotts-0.6b-f16.gguf` | 1.4 GB | Full precision (F16 weights) |
| `miotts-0.6b-q8_0.gguf` | 793 MB | LLM Q8_0 + codec F16 |
| `miotts-0.6b-q4_k.gguf` | 502 MB | **Recommended** — LLM Q4_K + codec F16 |
| `tokenizer.json` | ~14 MB | Qwen3 BPE tokenizer (place next to GGUF) |
| `en_female.emb.gguf` | <1 KB | English female voice preset |
| `en_male.emb.gguf` | <1 KB | English male voice preset |
| `jp_female.emb.gguf` | <1 KB | Japanese female voice preset |
| `jp_male.emb.gguf` | <1 KB | Japanese male voice preset |

## Usage

```bash
crispasr --backend miotts -m miotts-0.6b-q4_k.gguf \
  --voice en_female.emb.gguf \
  --tts "Hello world, how are you today?" \
  -of output
```

**Important:** A voice preset (`--voice` or `-emb`) is required for good audio quality. Without it, the codec produces unintelligible audio.

The tokenizer.json must be in the same directory as the GGUF file.

## Verified ASR Roundtrip

| Quantization | Size | Input | ASR Output |
|-------------|------|-------|------------|
| Q4_K+F16 | 502 MB | "The quick brown fox jumps over the lazy dog." | "The quick brown fox jumps over the lazy dog." ✅ |
| F32 | 2.6 GB | "Hello world, how are you today?" | "Hello world, how are you today? What?" ✅ |
| F16 (uniform) | 1.4 GB | — | Codec too noisy (SnakeBeta precision) ❌ |

The mixed quantization (LLM=Q4_K, codec=F16) is critical — uniform quantization degrades the UpSampler's SnakeBeta activation.

## Architecture

- **LLM**: Qwen3ForCausalLM (28L, 1024d, GQA 16/8, head_dim=128, vocab=164480)
- **Codec**: MioCodec-25Hz-44.1kHz-v2 (FSQ → wave_prenet → conv_upsample → ResNet → AdaLN-Zero decoder → ResNet → UpSampler with SnakeBeta → iSTFT)
- **Output**: 44.1 kHz mono PCM

## License

Apache 2.0 (MioTTS-0.6B is Qwen3-based). MioCodec weights under MIT.

## Credits

- Model: [Aratako](https://huggingface.co/Aratako)
- GGUF conversion + C++ port: [CrispASR](https://github.com/CrispStrobe/CrispASR)
- Voice presets: [mmnga/mio-tts-cpp](https://github.com/mmnga/mio-tts-cpp)

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [Aratako/MioTTS-0.6B](https://huggingface.co/Aratako/MioTTS-0.6B) — published by `Aratako`.
- **Upstream licence:** `apache-2.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
