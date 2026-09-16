---
license: apache-2.0
language:
- zh
- en
pipeline_tag: audio-text-to-text
tags:
- audio
- speech-recognition
- audio-understanding
- audio-qa
- transcription
- ggml
- gguf
- moss-audio
- qwen3
- deepstack
library_name: ggml
base_model: OpenMOSS-Team/MOSS-Audio-4B-Instruct
---

# MOSS-Audio-4B-Instruct -- GGUF (ggml-quantised)

GGUF / ggml conversions of [`OpenMOSS-Team/MOSS-Audio-4B-Instruct`](https://huggingface.co/OpenMOSS-Team/MOSS-Audio-4B-Instruct) for use with `crispasr --backend moss-audio` from **[CrispStrobe/CrispASR](https://github.com/CrispStrobe/CrispASR)**.

MOSS-Audio-4B-Instruct is OpenMOSS's ~4.6 B parameter **audio-understanding** model:

- **First audio-understanding backend in CrispASR** -- not just ASR but also audio QA, scene description, music analysis, meeting summarisation
- **Mandarin + English** speech recognition and audio understanding
- **DeepStack cross-layer feature injection** -- multi-resolution encoder taps at layers 8/16/24 injected into the LM's early layers for fine-grained prosody + semantic awareness
- **Time-aware ASR** with explicit time-marker tokens for word-level and sentence-level timestamps
- **Apache-2.0** licence

## Files

| File | Size | Notes |
| --- | ---: | --- |
| `moss-audio-4b-instruct-f16.gguf` | 9.73 GB | F16, full precision |
| `moss-audio-4b-instruct-q4_k.gguf` | 2.75 GB | **Q4_K -- recommended default** |

## Quick Start

```bash
# 1. Build the runtime
git clone https://github.com/CrispStrobe/CrispASR
cd CrispASR
cmake -G Ninja -B build -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=OFF
cmake --build build -j$(nproc) --target crispasr-cli

# 2. Download a quantisation
huggingface-cli download cstr/MOSS-Audio-4B-Instruct-GGUF \
    moss-audio-4b-instruct-q4_k.gguf --local-dir .

# 3. Transcribe audio
./build/bin/crispasr \
    -m moss-audio-4b-instruct-q4_k.gguf \
    -f your-audio.wav \
    --backend moss-audio -t 4

# 4. Audio understanding (custom prompt)
./build/bin/crispasr \
    -m moss-audio-4b-instruct-q4_k.gguf \
    -f your-audio.wav \
    --backend moss-audio \
    --prompt "Describe the sounds in this audio clip."
```


## Verified end-to-end output

**JFK sample (samples/jfk.wav, 11s):**
> And so, my fellow Americans, ask not what your country can do for you, ask what you can do for your country.

Verified on Q4_K (3.8 GB, F16 encoder + Q4_K LLM). All 6 crispasr-diff stages PASS at cos >= 0.999.

## Architecture

| Component | Details |
| --- | --- |
| Audio encoder | 32-layer Whisper-style transformer (d=1280, 20 heads, head_dim=64, FFN=5120, GELU, LayerNorm, eps=1e-5) |
| Conv stem | 3x Conv2d(stride=2, channels=480, kernel=3x3, pad=1) -> 8x temporal downsample (128 mel bins -> 16 freq bins) |
| Stem projection | Linear(480x16=7680 -> 1280) + sinusoidal positional embedding (max 1500 positions) |
| DeepStack taps | Encoder layers [8, 16, 24] -> 3 independent GatedMLP(1280 -> 8192 -> 2560, SiLU) |
| DeepStack injection | Residual add at LM layers [0, 1, 2] at audio-token positions |
| Audio adapter | GatedMLP(1280 -> 8192 -> 2560, SiLU) for final encoder output |
| LM backbone | 36-layer Qwen3 (hidden=2560, 32 Q-heads / 8 KV-heads, head_dim=128, QK-norm, SwiGLU FFN=9728, RoPE theta=1M) |
| Output head | Linear(2560 -> 151936), untied from embedding |
| Vocab | 151936 Qwen3 BPE (151643 regular + 293 special tokens) |
| Audio input | 16 kHz mono, 128 mel bins, n_fft=400, hop=160 |
| Audio tokens | 12.5 Hz after 8x conv downsample, time markers every 2 seconds |
| Parameters | ~4.6 B total (encoder ~650M + adapter/deepstack ~120M + LM ~3.8B) |

### Special tokens

| Token | ID | Purpose |
| --- | --- | --- |
| `<\|AUDIO\|>` | 151654 | Audio frame placeholder (replaced by encoder embeddings) |
| `<\|audio_bos\|>` | 151669 | Audio segment start marker |
| `<\|audio_eos\|>` | 151670 | Audio segment end marker |
| `<\|im_start\|>` | 151644 | Chat turn start |
| `<\|im_end\|>` | 151645 | Chat turn end / EOS |

## How this was made

1. **Inspect** the HF safetensors: 3 shards, 901 tensors total -- audio encoder (conv stem + 32 transformer layers + layer_norm), audio adapter (1 GatedMLP), deepstack mergers (3 GatedMLPs), language model (embedding + 36 Qwen3 layers + final norm + lm_head).

2. **Convert** with [`models/convert-moss-audio-to-gguf.py`](https://github.com/CrispStrobe/CrispASR/blob/feature/moss-audio/models/convert-moss-audio-to-gguf.py): stream BF16 tensors one-at-a-time via `safe_open`, remap HF tensor names (`audio_encoder.layers.N.self_attn.q_proj` -> `enc.blk.N.attn.q`, `deepstack_audio_merger_list.N.gate_proj` -> `deepstack.N.gate`, `language_model.layers.N.mlp.gate_proj` -> `llm.blk.N.ffn.gate`, etc.), write F16 + F32 (norms/biases). BPE vocab + merges from `vocab.json` + `merges.txt` + `added_tokens.json`.

3. **Quantize** with `crispasr-quantize`: F16 -> Q4_K (2D+ tensors quantised, 1D biases/norms kept F32).

4. **C++ runtime** in [`src/moss_audio.{h,cpp}`](https://github.com/CrispStrobe/CrispASR/blob/feature/moss-audio/src/moss_audio.cpp): GGUF mmap, encoder graph (conv stem + 32 WhisperEncoderLayers with bidirectional attention + DeepStack tap capture), adapter/merger GatedMLP graphs, per-layer DeepStack injection into LM via pre-scattered residuals, KV-cached Qwen3 decode with `core_attn::kv_self_attn` (QK-norm, RoPE, GQA), greedy decode with chat-template prompt builder.

## Upstream

- Model: [`OpenMOSS-Team/MOSS-Audio-4B-Instruct`](https://huggingface.co/OpenMOSS-Team/MOSS-Audio-4B-Instruct) (Apache-2.0)
- Code: [`OpenMOSS/MOSS-Audio`](https://github.com/OpenMOSS/MOSS-Audio)
- Runtime: [`CrispStrobe/CrispASR`](https://github.com/CrispStrobe/CrispASR) branch `feature/moss-audio`

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [OpenMOSS-Team/MOSS-Audio-4B-Instruct](https://huggingface.co/OpenMOSS-Team/MOSS-Audio-4B-Instruct) — published by `OpenMOSS-Team`.
- **Upstream licence:** `apache-2.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF/GGML). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository. No training-content summary was found on the upstream model card at the time of writing; that documentation gap is upstream's and is not filled here.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
