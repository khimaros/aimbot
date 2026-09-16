---
license: apache-2.0
base_model:
- OpenMOSS-Team/MOSS-TTS-v1.5
- OpenMOSS-Team/MOSS-Audio-Tokenizer
library_name: gguf
pipeline_tag: text-to-speech
tags: [tts, gguf, crispasr, moss-tts]
---

# MOSS-TTS-v1.5 — GGUF (for CrispASR)

GGUF conversion of [`OpenMOSS-Team/MOSS-TTS-v1.5`](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5)
(MossTTSDelay: a Qwen3-8B backbone emitting 32 RVQ audio codebooks under a delay
pattern) + its [`MOSS-Audio-Tokenizer`](https://huggingface.co/OpenMOSS-Team/MOSS-Audio-Tokenizer)
1.6B transformer codec, for the [CrispASR](https://github.com/CrispStrobe/CrispASR)
`moss-tts` backend.

## Files
| File | What | Size |
|------|------|------|
| `moss-tts-v1.5-q4_k.gguf` | Q4_K backbone (default; audio tables kept F16) | ~7 GB |
| `moss-tts-v1.5-f16.gguf` | F16 backbone (needs >20 GB VRAM or CPU; for re-quant) | ~17 GB |
| `moss-tts-v1.5-codec.gguf` | F16 transformer codec companion | ~3.5 GB |

## Use
```bash
crispasr --backend moss-tts -m moss-tts-v1.5-q4_k.gguf \
         --codec-model moss-tts-v1.5-codec.gguf \
         --tts "Hello world." --tts-output out.wav
# or: crispasr --backend moss-tts -m auto --auto-download --tts "..."
```

Validated on CUDA (P100) by decoded round-trip (synthesize → ASR): the Q4_K
backbone produces intelligible, accurate speech end-to-end.

## License
Apache-2.0, inherited from the base MOSS-TTS-v1.5 + MOSS-Audio-Tokenizer models
(OpenMOSS-Team). This repo redistributes derived GGUF weights under the same terms.

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [OpenMOSS-Team/MOSS-TTS-v1.5](https://huggingface.co/OpenMOSS-Team/MOSS-TTS-v1.5) — published by `OpenMOSS-Team`.
- **Upstream licence:** `apache-2.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository. No training-content summary was found on the upstream model card at the time of writing; that documentation gap is upstream's and is not filled here.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
