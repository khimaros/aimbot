---
license: other
license_name: breezeblue-research-and-non-commercial-license-1.1
license_link: https://huggingface.co/BreezeBlue/Breeze-TTS-2/blob/main/LICENSE
base_model: BreezeBlue/Breeze-TTS-2
language:
  - en
  - zh
tags:
  - text-to-speech
  - gguf
  - crispasr
  - non-commercial
extra_gated_prompt: >-
  These weights are for research and non-commercial use only.
---

# Breeze TTS 2 — GGUF (CrispASR)

> **Derived from Breeze TTS 2 by BreezeBlue and licensed for research and non-commercial use only.**

> ⚠️ **NON-COMMERCIAL.** These files are Derivative Models under §1.3 of the
> BreezeBlue Research and Non-Commercial License Agreement, which names
> quantization explicitly. They inherit the licence of the original weights.
> Hosting them as a service is a commercial use under §1.7(b).
> The full Agreement is in [`LICENSE`](./LICENSE); the required notice is in
> [`NOTICE`](./NOTICE).

GGUF conversion of [BreezeBlue/Breeze-TTS-2](https://huggingface.co/BreezeBlue/Breeze-TTS-2) for
[CrispASR](https://github.com/CrispStrobe/CrispASR).

| File | Size | Notes |
|---|---|---|
| `breeze-tts-2-f16.gguf` | ~5.7 GB | reference precision |
| `breeze-tts-2-q8_0.gguf` | ~3.0 GB | |
| `breeze-tts-2-q4_k.gguf` | ~2.2 GB | default for the CrispASR registry |

Architecture: a CSM fork — T5Gemma2 text encoder (26L, bidirectional, symmetric
sliding window) → Qwen3 backbone (28L) → depth decoder (12L) over 16 codebooks
at 12.5 Hz. Languages: English and Chinese.

**The codec is not in these files.** Breeze's bundled audio tokenizer is
bit-identical to `Qwen/Qwen3-TTS-Tokenizer-12Hz`, which CrispASR already ships
as [`cstr/qwen3-tts-tokenizer-12hz-GGUF`](https://huggingface.co/cstr/qwen3-tts-tokenizer-12hz-GGUF).
It is wired in as a registry companion and downloaded alongside the model.
Roughly 1.16 GB of the original checkpoint (`embed_text_tokens` and a leftover
Mimi `codec_model.*`) is unreachable at inference and is dropped by the
converter.

Inference code in the upstream repo is Apache-2.0 and is not covered by the
Agreement (§1.2); the restriction here is on the **weights**.

All credit for the model goes to BreezeBlue / RESONIA, INC.
