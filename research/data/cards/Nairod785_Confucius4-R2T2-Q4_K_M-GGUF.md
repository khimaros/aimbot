---
base_model: netease-youdao/Confucius4-R2T2
library_name: transcribe.cpp
pipeline_tag: automatic-speech-recognition
license: other
license_name: netease-model-use-license
license_link: https://github.com/netease-youdao/Confucius4-R2T2/blob/master/MODEL_LICENSE
language:
  - zh
  - en
  - yue
  - ar
  - de
  - fr
  - es
  - pt
  - id
  - it
  - ko
  - ru
  - th
  - vi
  - ja
  - tr
  - hi
  - ms
  - nl
  - sv
  - da
  - fi
  - pl
  - cs
  - fil
  - fa
  - el
  - hu
  - mk
  - ro
tags:
  - gguf
  - asr
  - automatic-speech-recognition
  - streaming
  - real-time
  - low-latency
  - quantized
  - q4_k_m
  - qwen3-asr
  - confucius4
  - r2t2
  - audio.cpp
  - transcribe.cpp
---

# Confucius4-R2T2 — Q4_K_M GGUF

Optimized **Q4_K_M GGUF** quantization of **NetEase Youdao Confucius4-R2T2**, a low-latency, append-only streaming ASR model (fine-tuned from Qwen3-ASR-1.7B with Longest Stable Prefix decoding), ready for native execution in [transcribe.cpp](https://github.com/NairoDorian/transcribe.cpp) and [audio.cpp](https://github.com/0xShug0/audio.cpp).

* **Original model:** [netease-youdao/Confucius4-R2T2](https://huggingface.co/netease-youdao/Confucius4-R2T2) · [source code](https://github.com/netease-youdao/Confucius4-R2T2) · [demo](https://r2t2.youdao.com/demo)
* **Base Architecture:** Qwen3-ASR audio encoder (24 layers, 1024 width, 2048 projected width) + Causal LM decoder (28 layers, 16 query heads, 8 KV heads, 128 head width).
* **Reference GGUF repo & inspiration:** [davidxifeng/Confucius4-R2T2-gguf](https://huggingface.co/davidxifeng/Confucius4-R2T2-gguf) by David Xi Feng
* **Quantization & Benchmarking:** Researched and benchmarked in [transcribe.cpp](https://github.com/NairoDorian/transcribe.cpp).

---

## Technical Overview

Previous GGUF releases were constrained to Q8_0 or higher because uniform 4-bit and 5-bit quantizations either suffered from catastrophic empty-output cliffs or exhibited silent language drift (e.g. flipping to English when transcribing German or Russian).

This release introduces an **asymmetric per-tensor quantization recipe** that breaks through that barrier:

- **File:** `r2t2-q4_k_m.gguf`
- **File size:** **1.187 GB** (1,186,939,968 bytes) — **52% smaller** than the 2.478 GB Q8_0 reference.
- **Accuracy & Parity:** Preserves multilingual stability (verified across English, Chinese, German, and French).
- **Speed:** Faster than Q8_0 on CPU, avoiding the slow non-vectorized paths found in Q5_K.
- **Measured speed (transcribe.cpp, 2026-09-26):** **69.6× realtime on CUDA** (RTX 4070 Laptop, 29 s German clip: 421 ms total, 137 decode tokens/s) and 3.1× realtime on CPU (i9-13900H). Output is byte-identical to the unoptimized build on 100 FLEURS clips in 5 languages. See [QUANTIZATION.md](QUANTIZATION.md#5b-cuda).

### Quantization Composition

| Block | Target Dtype | Architectural Role |
|---|---|---|
| **Audio Tower** | `BF16 / Q4_K` | Audio encoder layers quantized to Q4_K with sensitive projection weights preserved at BF16. |
| **Attention Projections** | `Q4_K` | Fits within the LM error budget when down projections are held at higher precision. |
| **MLP Gate / Up** | `Q4_K` | Errors are bounded through SwiGLU activation. |
| **MLP Down** | **`Q6_K`** | **Hard Floor.** Writes into residual stream; lower precision triggers multilingual degradation. |
| **Embeddings** | **`Q2_K`** | Lookup table error does not compound; cuts 311M parameters with negligible loss. |

---

## Technical Documentation & Reports

Detailed technical documentation and empirical logs accompanying this model:

- 📄 **[QUANTIZATION.md](QUANTIZATION.md)** — Empirical quantization report, 20+ arm evaluation table, failure mode analysis (cliff vs drift), speed benchmarks, and reproduction recipe.
- 📄 **[QUANTIZATION_ARMS.md](QUANTIZATION_ARMS.md)** — The general per-tensor quantization arms methodology, `--keep-type` semantics, census asserting, and lessons learned.

---

## Files

| File | Type | Size | Description |
|---|---|---|---|
| `r2t2-q4_k_m.gguf` | Model | 1.187 GB | High-performance floor quantization; passes multilingual validation |
| `QUANTIZATION.md` | Doc | — | Detailed technical report, ablation study, and benchmarks |
| `QUANTIZATION_ARMS.md` | Doc | — | General per-tensor quantization arms methodology |
| `NOTICE` | Legal | — | Attribution and derivative work disclaimers |
| `LICENSE` / `LICENSE_zh` | Legal | — | NetEase Youdao Model Use License Agreement |

---

## Usage

### With `transcribe-cli`
```bash
transcribe-cli -m r2t2-q4_k_m.gguf samples/audio.wav
```

### With `audiocpp_cli`
```bash
# Offline transcription
audiocpp_cli --task asr --family confucius4_r2t2   --model r2t2-q4_k_m.gguf   --backend metal --audio speech_16k.wav --text-out transcript.txt

# Streaming (real-time, append-only)
audiocpp_cli --task asr --mode streaming --family confucius4_r2t2   --model r2t2-q4_k_m.gguf   --backend metal --audio speech_16k.wav   --session-option confucius4_r2t2.chunk_size_ms=320   --text-out transcript.txt
```

### Server (OpenAI-compatible)
```bash
curl http://127.0.0.1:8488/v1/audio/transcriptions -F model=r2t2-asr -F file=@speech.wav
curl -N http://127.0.0.1:8488/v1/audio/transcriptions   -F model=r2t2-asr -F stream=true -F file=@speech.wav
```

Streaming chunk sizes from **80 ms to 2000 ms** are supported (320 ms recommended default).

---

## Supported Languages

Optimized for Chinese and English, with support for Cantonese, Arabic, German, French, Spanish, Portuguese, Indonesian, Italian, Korean, Russian, Thai, Vietnamese, Japanese, Turkish, Hindi, Malay, Dutch, Swedish, Danish, Finnish, Polish, Czech, Filipino, Persian, Greek, Romanian, Hungarian, and Macedonian.

---

## License and Attribution

This is a **quantized Derivative Work** of [NetEase Youdao Confucius4-R2T2](https://huggingface.co/netease-youdao/Confucius4-R2T2), distributed under the **NetEase Youdao Model Use License Agreement** — full text in [`LICENSE`](LICENSE) (English) and [`LICENSE_zh`](LICENSE_zh) (Chinese); see also [`NOTICE`](NOTICE). The source code of the original model is Apache-2.0, the model weights are not.

Required statement (license section 4.1(a)):

> Any modifications made to the original model in this Derivative Work are not
> endorsed, warranted, or guaranteed by the original right-holder of the
> original model, and the original right-holder disclaims all liability related
> to this Derivative Work.

Key restrictions: a separate commercial license is required above 100 M monthly active users or RMB 1 B annual revenue (section 2.2); the model may not be used to improve other AI models except Confucius4-R2T2, its derivatives, or non-commercial models (section 3.4(c)); high-risk uses such as medical diagnosis, autonomous driving, military, critical-infrastructure control, large-scale biometric surveillance and automated decision-making are prohibited (section 4.2). No trademark rights are granted (section 5.2).

## Citation

```bibtex
@misc{Confucius4-R2T2,
  title        = {Confucius4-R2T2: A Low Latency and High Accuracy Real-Time Speech Recognition Model},
  author       = {NetEase Youdao},
  year         = {2026},
  howpublished = {https://github.com/netease-youdao/Confucius4-R2T2}
}
```
