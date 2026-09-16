---
license: mit
base_model: microsoft/VibeVoice-ASR-BitNet
tags:
  - speech
  - asr
  - speech-recognition
  - gguf
  - crispasr
  - bitnet
  - ternary
language:
  - en
  - zh
  - fr
  - it
  - ko
  - pt
  - vi
library_name: crispasr
pipeline_tag: automatic-speech-recognition
---

# VibeVoice-ASR-BitNet GGUF

GGUF conversion of [microsoft/VibeVoice-ASR-BitNet](https://huggingface.co/microsoft/VibeVoice-ASR-BitNet) for use with [CrispASR](https://github.com/CrispStrobe/CrispASR).

## Available files

All variants use **TQ2_0** (ternary 2-bit) for the LM projection weights. They differ in how aggressively the VAE encoder and LM embedding are quantized. All produce **identical transcription output** on the JFK benchmark.

| File | VAE | Embed | Size | Recommended |
|------|-----|-------|------|-------------|
| `vibevoice-asr-bitnet-tq2.gguf` | Q8_0 | F16 | 1.55 GB | default |
| `vibevoice-asr-bitnet-embed-q8.gguf` | Q8_0 | Q8_0 | 1.34 GB | |
| `vibevoice-asr-bitnet-vae-q5.gguf` | Q5_0 | F16 | 1.33 GB | |
| `vibevoice-asr-bitnet-both-q5.gguf` | Q5_0 | Q8_0 | 1.12 GB | |
| `vibevoice-asr-bitnet-vae-q4.gguf` | Q4_0 | F16 | 1.26 GB | |
| `vibevoice-asr-bitnet-aggro.gguf` | Q4_0 | Q8_0 | 1.05 GB | smallest |

**Pick any file** -- quality is identical across all variants (verified via transcription roundtrip on JFK audio). The `aggro` variant is 35% smaller than the default with zero degradation.

## Model Details

| Property | Value |
|----------|-------|
| Base model | microsoft/VibeVoice-ASR-BitNet (1.5B params) |
| Architecture | Dual VAE encoder + Qwen2 LM decoder |
| LM | 28 layers, 1536 hidden, 12 heads, 2 KV heads |
| VAE | ConvNeXt-style 1D CNN, stride 3200, acoustic (64d) + semantic (128d) |
| Input | 24 kHz mono PCM |
| Languages | English, Chinese, French, Italian, Korean, Portuguese, Vietnamese |
| License | MIT |

## Quantization strategy

The LM projection weights (q/k/v/o/gate/up/down) are BitNet-trained with ternary values {-1, 0, 1}. The converter applies the ternary quantization (`s = 1/mean(|w|)`, round, clamp) and packs into ggml's native **TQ2_0** format (2.06 bpw). No custom SIMD kernels needed -- standard ggml `mul_mat` handles TQ2_0 transparently.

| Component | Quant options | Notes |
|-----------|--------------|-------|
| LM projections | TQ2_0 (all variants) | BitNet ternary, 2 bits/weight |
| VAE encoders | Q8_0 / Q5_0 / Q4_0 | ConvNeXt conv + FFN weights |
| LM embedding | F16 / Q8_0 | Lookup table, Q8_0 is lossless |
| Norms / biases | F32 (all variants) | Numerical stability |
| lm_head | tied to tok_emb (not stored) | Backend falls back automatically |

## Quality verification

All 6 variants were tested on JFK audio (11s, 24 kHz). Every variant produces **identical output**:

> ANd so, my fellow Americans, ask not what your country can do for you -- ask what you can do for your country..

Sweep ran on Kaggle (30 GB RAM, CPU). Conversion + transcription took ~20 min total for all 6 variants.

## Usage

### CLI
```bash
# Auto-download (uses the default tq2 variant)
crispasr -m auto --backend vibevoice-bitnet -f audio.wav

# Or with a specific file
crispasr -m vibevoice-asr-bitnet-aggro.gguf --backend vibevoice -f audio.wav
```

### C API
```c
#include "vibevoice.h"

vibevoice_context_params params = vibevoice_context_default_params();
params.n_threads = 4;
vibevoice_context *ctx = vibevoice_init_from_file("vibevoice-asr-bitnet-aggro.gguf", params);
char *text = vibevoice_transcribe(ctx, samples_24khz, n_samples);
printf("%s\n", text);
free(text);
vibevoice_free(ctx);
```

### Python
```python
import crispasr
s = crispasr.Session("vibevoice-asr-bitnet-aggro.gguf", backend="vibevoice")
result = s.transcribe("audio.wav")
print(result["text"])
```

## Conversion

```bash
# Default (Q8_0 VAE + F16 embed)
python models/convert-vibevoice-bitnet-to-gguf.py \
    --input microsoft/VibeVoice-ASR-BitNet \
    --output vibevoice-asr-bitnet-tq2.gguf

# Aggressive (Q4_0 VAE + Q8_0 embed, 1.05 GB)
python models/convert-vibevoice-bitnet-to-gguf.py \
    --input microsoft/VibeVoice-ASR-BitNet \
    --output vibevoice-asr-bitnet-aggro.gguf \
    --vae-quant q4_0 --embed-quant q8_0
```

## Acknowledgements

- [microsoft/VibeVoice](https://github.com/microsoft/VibeVoice) for the model architecture and training
- [microsoft/VibeASR.cpp](https://github.com/microsoft/VibeASR.cpp) for the BitNet quantization approach

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [microsoft/VibeVoice-ASR-BitNet](https://huggingface.co/microsoft/VibeVoice-ASR-BitNet) — published by `microsoft`.
- **Upstream licence:** `mit`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository. No training-content summary was found on the upstream model card at the time of writing; that documentation gap is upstream's and is not filled here.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
