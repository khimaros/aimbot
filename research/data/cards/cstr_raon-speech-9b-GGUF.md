---
license: cc-by-nc-4.0
base_model: KRAFTON/Raon-Speech-9B
language:
- en
- ko
tags:
- gguf
- ggml
- crispasr
- speech-to-text
pipeline_tag: automatic-speech-recognition
---

# Raon-Speech-9B — speech-to-text GGUF (CrispASR)

GGUF conversion of the **speech-to-text subset** of [KRAFTON/Raon-Speech-9B](https://huggingface.co/KRAFTON/Raon-Speech-9B) for [CrispASR](https://github.com/CrispStrobe/CrispASR) (`--backend raon-speech`, or `-m raon-speech` to auto-download Q4_K).

> **Licence: CC-BY-NC-4.0 — non-commercial use only**, inherited from the original model. The GGUFs are a derivative of KRAFTON's weights.

## What is included

| part | origin |
|---|---|
| Audio encoder | Qwen3-Omni audio tower (24 layers, d=1024, output 2048) |
| Input adaptor | 2048 → 4096 → GELU → 4096, RMSNorm |
| LLM | Qwen3, 36 layers, hidden 4096, GQA 32/8, RoPE θ = 5e6, untied lm_head, vocab 153723 |

The talker, code predictor, Mimi codec, output adaptor and speaker encoder serve speech *output* only, so they are not converted.

CrispASR reproduces `RaonPipeline.stt`'s front end:
- the input is resampled 16k → 24k, as the processor does;
- the audio is cut into 8 s chunks, each resampled 24k → 16k (a port of torchaudio's sinc resampler);
- each chunk gets its own log-mel (per-chunk max) and is encoded on its own;
- the 13 Hz encoder output is truncated to the 12.5 Hz frame grid.

The prompt is "Transcribe the audio into text"; `--ask "..."` replaces it.

## Files

| file | size | notes |
|---|---|---|
| `raon-speech-9b-q4_k.gguf` | 5.0 GB | registry default; same words as the reference on both test clips |
| `raon-speech-9b-q8_0.gguf` | 9.1 GB | transcripts identical to the reference |
| `raon-speech-9b-f16.gguf` | 17.1 GB | transcripts identical to the reference |

## Verification

Reference: the model's own remote code (transformers 4.57.3). The audio stages were run in fp32, and the text with greedy decoding on the bf16 model.

- **Diff harness (F16):** mel, encoder and adaptor outputs pass on jfk (11 s, two chunks) and on a Korean clip (one chunk). Worst frame cosine is 0.99995.
- **Transcripts:** F16 and Q8_0 are character-identical to the reference greedy output on both clips. Q4_K has the same words; on English it swaps one comma for a period.

```
en: and so my fellow americans, ask not what your country can do for you, ask what you can do for your country.
ko: 내일 오전에 회의 자료를 보내주세요
```

The official pipeline samples with temperature 0.2. CrispASR decodes greedily by default; `--temperature` is available.
