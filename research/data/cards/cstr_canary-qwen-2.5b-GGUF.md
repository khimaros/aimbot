---
license: cc-by-4.0
language:
- en
tags:
- gguf
- speech-recognition
- asr
- canary
- qwen
- nvidia
- crispasr
base_model: nvidia/canary-qwen-2.5b
---

# canary-qwen-2.5b GGUF

GGUF conversions of [nvidia/canary-qwen-2.5b](https://huggingface.co/nvidia/canary-qwen-2.5b) for use with [CrispASR](https://github.com/CrispStrobe/CrispASR).

## Model

SALM (Speech-Augmented Language Model): 32-layer FastConformer encoder (d=1024) + linear projection (1024 to 2048) + Qwen3-1.7B LLM decoder with merged LoRA. English ASR, up to ~40s audio.

- **Parameters**: 2.5B
- **Encoder**: FastConformer (from canary-1b-flash), 128 mel bins, 16 kHz
- **LLM**: Qwen3-1.7B (28 layers, GQA 16/8, SwiGLU)
- **LoRA**: merged at conversion time (r=128, alpha=256)
- **Language**: English only
- **License**: CC-BY-4.0

## Files

| File | Quant | Size | Notes |
|------|-------|------|-------|
| `canary-qwen-2.5b-f16.gguf` | F16 | 5.70 GB | Full precision |
| `canary-qwen-2.5b-q8_0.gguf` | Q8_0 | 4.38 GB | LLM blocks quantized, encoder F16 |
| `canary-qwen-2.5b-q4_k.gguf` | Q4_K | 3.67 GB | LLM blocks quantized, encoder F16 |

Encoder and projection weights are kept at source precision (F16/F32) in all quantized variants to avoid conformer drift.

## Usage

```bash
# With CrispASR CLI
crispasr --backend canary-qwen -m canary-qwen-2.5b-q8_0.gguf -f audio.wav

# Auto-download
crispasr --backend canary-qwen -m auto --auto-download -f audio.wav
```

## Conversion

```bash
python models/convert-canary-qwen-to-gguf.py \
  --input nvidia/canary-qwen-2.5b \
  --output canary-qwen-2.5b-f16.gguf

crispasr-quantize canary-qwen-2.5b-f16.gguf canary-qwen-2.5b-q8_0.gguf q8_0
crispasr-quantize canary-qwen-2.5b-f16.gguf canary-qwen-2.5b-q4_k.gguf q4_k
```

## Performance (Kaggle P100)

| Stage | Time |
|-------|------|
| Mel | 22 ms |
| Encoder + projection | 248 ms |
| LLM prefill (154 tokens) | 171 ms |
| LLM decode (22 tokens) | 348 ms |
| **Total** | **~0.8 s** |

On the JFK sample (11s audio): "And so my fellow Americans ask not what your country can do for you ask what you can do for your country"

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [nvidia/canary-qwen-2.5b](https://huggingface.co/nvidia/canary-qwen-2.5b) — published by `nvidia`.
- **Upstream licence:** `cc-by-4.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
