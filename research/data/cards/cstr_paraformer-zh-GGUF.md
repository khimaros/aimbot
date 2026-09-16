---
license: other
license_name: funasr-model-license
license_link: https://huggingface.co/funasr/paraformer-zh
language:
- zh
- en
pipeline_tag: automatic-speech-recognition
tags:
- audio
- speech-recognition
- transcription
- ggml
- gguf
- funasr
- paraformer
- sanm
- non-autoregressive
- mandarin
- chinese
library_name: ggml
base_model: funasr/paraformer-zh
---

# Paraformer-zh — GGUF (ggml-quantised)

GGUF / ggml conversion of [`funasr/paraformer-zh`](https://huggingface.co/funasr/paraformer-zh) for use with the `paraformer` backend in **[CrispStrobe/CrispASR](https://github.com/CrispStrobe/CrispASR)**.

Paraformer-zh is Alibaba's **non-autoregressive** ASR model (~220M params): a single forward pass through 50 SANM encoder blocks, a CIF (continuous integrate-and-fire) predictor, and 16 NAR decoder blocks produces the full transcript — no autoregressive token-by-token generation. Primarily **Mandarin Chinese** with English support. Character-level tokenizer (8404 vocab).

## Architecture

```
Audio (16 kHz mono)
  → Kaldi fbank (80 mel, 25 ms / 10 ms)
  → LFR: stack 7, stride 6 → (T_lfr, 560)
  → CMVN (AddShift + Rescale, 560-dim)
  → SANMEncoder: 1 entry block (560→512) + 49 main blocks (512→512)
      each: LayerNorm → fused QKV → FSMN(k=11) + MHA(4 heads) → FFN(2048)
  → CifPredictorV2:
      Conv1d(512,512,k=3) → ReLU → Linear(512,1) → sigmoid
      → CIF accumulation (fire when alpha ≥ 1.0)
      → acoustic_embeds: (N_tokens, 512)
  → ParaformerSANMDecoder: 16 blocks
      each: norm1 → FFN → norm2 → FSMN(k=11) → norm3 → cross-attn(Q=dec, KV=enc)
  → decoders3: 1 post-processing block (FFN only)
  → after_norm → output_layer(512→8404) → argmax → characters
```

- Encoder reuses the same SANM block as Fun-ASR-Nano and SenseVoice
- Decoder block order is unusual: **FFN → FSMN → cross-attn** (not the more common self-attn → cross-attn → FFN)
- FSMN = depthwise conv (no Q/K/V self-attention in the decoder)
- Cross-attention uses a fused K+V projection from encoder output

## Files

| File | Size | Notes |
| --- | ---: | --- |
| `paraformer-zh-q4_k.gguf` | 123 MB | **Recommended default.** Byte-identical transcript to F16 on both Chinese and English test clips. Auto-download target for `--backend paraformer -m auto`. |
| `paraformer-zh-q8_0.gguf` | 227 MB | Byte-identical transcript to F16. |
| `paraformer-zh-f16.gguf` | 421 MB | F16 reference weights (956 tensors). Use for diff testing against the upstream PyTorch reference. |

## Quick Start

```bash
git clone https://github.com/CrispStrobe/CrispASR
cd CrispASR
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --target crispasr-cli

# Chinese:
./build/bin/crispasr \
    --backend paraformer \
    -m /path/to/paraformer-zh-q4_k.gguf \
    -f chinese_audio.wav --no-prints
# → 正是因为存在绝对正义所以我们接受现实的相对正义...

# English:
./build/bin/crispasr \
    --backend paraformer \
    -m /path/to/paraformer-zh-q4_k.gguf \
    -f samples/jfk.wav --no-prints
# → and so my fellow americans ask not what your country can do for you ask what you can do for your country

# Or auto-download (resolves to Q4_K by default):
./build/bin/crispasr --backend paraformer -m auto -f audio.wav
```

## Output format

The output is raw character-level text:

- **Chinese**: characters concatenated directly (no spaces) — standard for Chinese text
- **English**: word-level tokens with spaces inserted between consecutive English words; BPE continuation markers (`@@`) handled internally
- **No punctuation or casing** — the model's character vocabulary has only lowercase English. Use `--punc-model` for punctuation restoration if needed.

## Verification

All three quants (F16, Q4_K, Q8_0) produce **byte-identical** transcripts vs the upstream Python reference (`funasr.AutoModel.generate()`) on:

- **Chinese** (13 s `asr_example.wav`): 66 characters, exact match
- **English** (11 s JFK `samples/jfk.wav`): 26 tokens, exact match

The `crispasr-diff paraformer` harness captures 73 intermediate stages (mel features, 50 encoder layers, CIF alphas, acoustic embeds, 16 decoder layers, decoder output, generated text) for element-wise cosine-similarity comparison.

## Converting from upstream

If you want to convert from the upstream PyTorch model yourself:

```bash
# Download upstream model
python3 -c "
from huggingface_hub import snapshot_download
snapshot_download('funasr/paraformer-zh',
    local_dir='paraformer-zh-upstream',
    local_dir_use_symlinks=False)
"

# Convert to GGUF
python3 models/convert-paraformer-to-gguf.py \
    --input paraformer-zh-upstream \
    --output paraformer-zh-f16.gguf

# Quantize
./build/bin/crispasr-quantize paraformer-zh-f16.gguf paraformer-zh-q4_k.gguf q4_k
./build/bin/crispasr-quantize paraformer-zh-f16.gguf paraformer-zh-q8_0.gguf q8_0
```

## Licence + attribution

Upstream **funasr/paraformer-zh**:

- **Code** (the `funasr` Python package): Apache-2.0.
- **Model weights**: [**FunASR Model License**](https://huggingface.co/funasr/paraformer-zh) (Alibaba) — commercial use OK with attribution.

These GGUF files are a quantised / repackaged distribution of the upstream weights and inherit the FunASR Model License. Please attribute Alibaba / FunAudioLLM in downstream products.

> If you use this model, please also cite the upstream FunASR work.
> See the [upstream model card](https://huggingface.co/funasr/paraformer-zh) for the canonical citation.
