---
license: other
license_name: see-base-model
license_link: https://huggingface.co/AutoArk-AI/ARK-ASR-3B
base_model: AutoArk-AI/ARK-ASR-3B
library_name: gguf
pipeline_tag: automatic-speech-recognition
tags:
  - automatic-speech-recognition
  - asr
  - gguf
  - whisper
  - qwen2
  - crispasr
  - ggml
language:
  - zh
  - en
  - de
  - ja
  - fr
  - ko
  - es
  - pl
  - it
  - ro
  - hu
  - cs
  - nl
  - fi
  - hr
  - sk
  - sl
  - et
  - lt
---

# ARK-ASR-3B — GGUF

GGUF conversions of [**AutoArk-AI/ARK-ASR-3B**](https://huggingface.co/AutoArk-AI/ARK-ASR-3B),
a 19-language automatic speech recognition model, for use with
[**CrispASR**](https://github.com/CrispStrobe/CrispASR) (a ggml/llama.cpp-style C++ engine).

> ⚠️ **Experimental / work-in-progress.** Core ASR is validated and accurate (see
> below), but the backend has known rough edges — read **Limitations** before relying on it.

## Architecture

ARK-ASR-3B = **Whisper-large-v3 encoder with partial rotary position embeddings**
→ **MLP adapter** → **Qwen2.5-3B decoder** with audio-token injection. A single
self-contained GGUF holds the encoder, adapter, and language model.

- **Encoder** — Whisper-large-v3 conv stem + 32 layers, but Whisper's learned
  positional embeddings are replaced by **partial interleaved RoPE** (rotates the
  first 32 of 64 head dims, θ=10000, on Q and K; `k_proj` has no bias; the
  encoder's own final LayerNorm is dropped). Because positions are rotary, the
  encoder handles **arbitrary-length audio in one pass** — there is no 30 s cap.
- **Adapter** — LayerNorm → merge 4 consecutive frames → Linear 5120→4096 → GELU
  → Linear 4096→2048.
- **Decoder** — stock Qwen2.5-3B (2048 hidden, 36 layers, GQA 16Q/2KV, SwiGLU,
  RMSNorm, θ=1e6, tied embeddings). The `<|audio|>` placeholder embeddings are
  overwritten by the adapter's audio features, then the transcript is decoded.

Mel features use the stock WhisperFeatureExtractor recipe (128 bins, n_fft 400,
hop 160).

## Files

| File | Size | Notes |
|------|------|-------|
| `ark-asr-3b-f16.gguf`  | 7.0 GB | Full precision. Reference quality. |
| `ark-asr-3b-q8_0.gguf` | 4.0 GB | **Recommended.** Near-lossless; validated against the F16/PyTorch reference. |
| `ark-asr-3b-q4_k.gguf` | 3.3 GB | Smallest. Encoder/adapter/embeddings kept in F16, only the Qwen2 decoder body is Q4_K. Verbatim on test clips. |

All three transcribe the JFK sample verbatim. Q8_0 is the best size/quality trade-off.

## Usage (CrispASR)

```bash
# Build CrispASR, then:
crispasr -m ark-asr-3b-q8_0.gguf --backend ark-asr -f audio.wav

# Optional best-effort language hint (the model is promptless; see Limitations):
crispasr -m ark-asr-3b-q8_0.gguf --backend ark-asr -l de -f audio.wav

# Force CPU (GPU is the default):
CRISPASR_ARKASR_CPU=1 crispasr -m ark-asr-3b-q8_0.gguf --backend ark-asr -f audio.wav
```

`-m auto --backend ark-asr` also resolves these files via the model registry.

## Validation

The C++ port was checked stage-by-stage against the original PyTorch model
(`trust_remote_code`, bf16) with CrispASR's diff harness on the JFK clip:

| Stage | Cosine vs. reference |
|-------|----------------------|
| log-mel spectrogram | 0.999993 |
| first decoder logits (Q8_0) | 0.999646 |
| audio embeddings (Q8_0, mean) | 0.999445 |

End-to-end the transcript matches the reference verbatim (English and German tested).

## Limitations (WIP)

- **Whole-audio by default.** Matching the reference, CrispASR encodes the entire
  clip in one pass (no chunking). Very long files fall back to internal 30 s
  chunking above a cap (`CRISPASR_ARKASR_MAX_SINGLE_PASS_S`, default 300 s) to
  bound memory; chunked segments can re-detect language independently, so pass
  `--vad` or raise the cap for long multilingual audio.
- **Promptless language steering.** The model has no language parameter; `-l`
  injects a best-effort "Transcribe the audio in <Language>." instruction, but
  the model was not instruction-trained, so it is not a hard guarantee.
- **GPU:** default and validated on Apple Metal (verbatim; ~5.6× faster prefill,
  roughly neutral per-token decode on unified memory). CUDA is not yet validated —
  use `CRISPASR_ARKASR_CPU=1` if you hit issues.

## Attribution & license

Base model: [AutoArk-AI/ARK-ASR-3B](https://huggingface.co/AutoArk-AI/ARK-ASR-3B)
(on-policy distilled, THU-NLP). These GGUFs are a community conversion; the
license follows the base model — **check the upstream repository** for terms.
Conversion and the CrispASR `ark-asr` backend by [CrispStrobe](https://github.com/CrispStrobe).
