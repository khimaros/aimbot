---
language:
  - multilingual
license: apache-2.0
tags:
  - gguf
  - asr
  - speech-recognition
  - multilingual
  - 1600-languages
  - omniasr
  - crispasr
pipeline_tag: automatic-speech-recognition
---

# OmniASR-LLM-Unlimited-300M-v2 — GGUF

GGUF conversion of Meta's OmniASR-LLM-Unlimited-300M-v2 from [facebookresearch/omnilingual-asr](https://github.com/facebookresearch/omnilingual-asr) for the [CrispASR](https://github.com/CrispStrobe/CrispASR) `omniasr` backend.

1600+ language ASR with a 300M encoder + LLaMA decoder (~1.6B total params). The "Unlimited" variant handles arbitrarily long audio via a 15-second sliding-segment protocol.

## Architecture

- **Input**: raw 16 kHz mono PCM (no mel features)
- **Frontend**: 7-layer CNN positional conv stack
- **Encoder**: 24-layer transformer (1024-dim, 4096 FFN, 16 heads), vocab=9812
- **Projection**: enc_proj bridge to decoder
- **Decoder**: 12-layer LLaMA (4096-dim, 2816 FFN, 8 heads)
- **Tokenizer**: SentencePiece; output: UTF-8 text
- **Unlimited mode**: 15s-segment streaming for audio of any length

## Files

| File | Size | Description |
|------|------|-------------|
| `omniasr-llm-unlimited-300m-v2-q4_k.gguf` | 1.0 GB | Q4_K quantized (recommended) |
| `omniasr-llm-unlimited-300m-v2-f16.gguf` | 3.1 GB | F16 full precision |

## Usage

```bash
crispasr --backend omniasr -m omniasr-llm-unlimited-300m-v2-q4_k.gguf \
    -f audio.wav -l auto
```

## License

Apache 2.0.

## Credits

- Original model: [Meta / facebookresearch](https://github.com/facebookresearch/omnilingual-asr)
- GGUF conversion & runtime: [CrispASR](https://github.com/CrispStrobe/CrispASR)

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [facebookresearch/omnilingual-asr (Meta OmniASR-LLM-Unlimited-300M-v2)](https://github.com/facebookresearch/omnilingual-asr).
- **Upstream licence:** `apache-2.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
