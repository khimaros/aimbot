---
license: mit
language:
- en
- ha
- is
- ja
- cs
- ru
- zh
- de
base_model:
- facebook/wmt21-dense-24-wide-en-x
pipeline_tag: translation
tags:
- translation
- m2m_100
- wmt21
- text2text-generation
- multilingual
- encoder-decoder
- gguf
- crispasr
library_name: ggml
arxiv: "2108.03265"
---

# WMT21 Dense 24-Wide (EN→X) — GGUF (ggml)

GGUF / ggml conversion of [`facebook/wmt21-dense-24-wide-en-x`](https://huggingface.co/facebook/wmt21-dense-24-wide-en-x) for use with **[CrispStrobe/CrispASR](https://github.com/CrispStrobe/CrispASR)**.

This is the **English-to-many** WMT21 competition model — a 4.7B-parameter dense encoder-decoder transformer trained for high-quality translation from English into 7 target languages. It won the WMT21 shared task for multiple language pairs. Architecture: 24 encoder + 24 decoder layers (d=2048, 32 heads, FFN=16384, ReLU, pre-norm, sinusoidal positions). Distributed under **MIT license**.

## Files

| File | Size | Notes |
|---|---:|---|
| `wmt21-dense-24-wide-en-x-f16.gguf` | 8.8 GB | F16 weights (reference quality) |
| `wmt21-dense-24-wide-en-x-q8_0.gguf` | 4.7 GB | Q8_0 quantized (identical quality to F16 on test set) |
| `wmt21-dense-24-wide-en-x-q4_k.gguf` | 2.5 GB | Q4_K quantized (minor word choice differences) |

## Supported languages (English → 7)

| Code | Language |
|---|---|
| de | German |
| cs | Czech |
| ru | Russian |
| ja | Japanese |
| zh | Chinese |
| is | Icelandic |
| ha | Hausa |

Source is always English (`en`).

## Quick start

```bash
# 1. Build CrispASR
git clone https://github.com/CrispStrobe/CrispASR
cd CrispASR
cmake -B build -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF
cmake --build build -j

# 2. Pull model
huggingface-cli download cstr/wmt21-dense-24-wide-en-x-GGUF wmt21-dense-24-wide-en-x-q8_0.gguf --local-dir .

# 3. Translate
./build/bin/crispasr --backend m2m100 -m wmt21-dense-24-wide-en-x-q8_0.gguf \
    --text "Machine learning is changing the world." \
    -sl en -tl de

# English → Japanese
./build/bin/crispasr --backend m2m100 -m wmt21-dense-24-wide-en-x-q8_0.gguf \
    --text "Hello, how are you today?" \
    -sl en -tl ja
```

## Quality verification

| Input (English) | Target | F16 | Q4_K |
|---|---|---|---|
| Machine learning is changing the world. | de | Maschinelles Lernen verändert die Welt. | Maschinelles Lernen verändert die Welt. |
| Hello, how are you today? | ja | こんにちは、今日はいかがですか? | こんにちは、今日はいかがですか? |
| The president said he would not attend the meeting. | ru | Президент заявил, что не будет участвовать в заседании. | Президент заявил, что не будет участвовать в заседании. |

## Architecture

```
Text → SentencePiece BPE tokenizer (128K vocab, 8 lang codes)
     → English lang token (__en__) + text tokens + </s>
     → 24-layer transformer encoder (d=2048, 32 heads, FFN=16384, ReLU, pre-norm)
     → Sinusoidal positional embeddings (pre-computed)
     → 24-layer transformer decoder (self-attn + cross-attn + FFN)
     → Shared embedding LM head (tied weights)
     → Target lang forced as first decoder token
     → Greedy decode → translated text
```

## Conversion

```bash
python models/convert-m2m100-to-gguf.py \
    --input facebook/wmt21-dense-24-wide-en-x \
    --output wmt21-dense-24-wide-en-x-f16.gguf
```

## Related models

- [`cstr/wmt21-dense-24-wide-x-en-GGUF`](https://huggingface.co/cstr/wmt21-dense-24-wide-x-en-GGUF) — many-to-English (reverse direction)
- [`cstr/m2m100-418m-GGUF`](https://huggingface.co/cstr/m2m100-418m-GGUF) — smaller 100-language any-to-any model
- [`facebook/wmt21-dense-24-wide-en-x`](https://huggingface.co/facebook/wmt21-dense-24-wide-en-x) — original PyTorch model

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [facebook/wmt21-dense-24-wide-en-x](https://huggingface.co/facebook/wmt21-dense-24-wide-en-x) — published by `facebook`.
- **Upstream licence:** `mit`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF/GGML). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository. No training-content summary was found on the upstream model card at the time of writing; that documentation gap is upstream's and is not filled here.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
