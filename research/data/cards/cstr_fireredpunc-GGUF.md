---
license: apache-2.0
language:
- zh
- en
tags:
- gguf
- ggml
- punctuation
- text-processing
- bert
- nlp
base_model: FireRedTeam/FireRedPunc
pipeline_tag: token-classification
---

# FireRedPunc (GGUF)

GGUF conversion of [FireRedTeam/FireRedPunc](https://huggingface.co/FireRedTeam/FireRedPunc) for use with [CrispASR](https://github.com/CrispStrobe/CrispASR).

Adds punctuation to unpunctuated ASR output using a BERT-based token classifier.

## Model Details

- **Architecture**: BERT-base (LERT) — 12L, d=768, 12 heads, d_ffn=3072, GELU
- **Parameters**: ~102M
- **Classifier**: Linear(768, 5) — 5 punctuation classes
- **Labels**: space, ，(comma), 。(period), ？(question), ！(exclamation)
- **Vocabulary**: chinese-bert-wwm-ext (21,128 tokens, WordPiece)
- **Max sequence**: 512 tokens (longer texts are automatically chunked)
- **Languages**: Chinese + English
- **License**: Apache 2.0

## Usage with CrispASR

```bash
# Add punctuation to any ASR backend's output
crispasr --backend wav2vec2 -m wav2vec2.gguf --punc-model fireredpunc-q8_0.gguf -f audio.wav

# Works with all backends
crispasr --backend omniasr -m omniasr-ctc-1b-q4_k.gguf --punc-model fireredpunc-q8_0.gguf -f audio.wav
```

## Available Files

| File | Quant | Size | Description |
|------|-------|------|-------------|
| `fireredpunc.gguf` | F16 | 195 MB | Full precision |
| `fireredpunc-q8_0.gguf` | Q8_0 | 104 MB | Recommended — lossless quality |
| `fireredpunc-q4_k.gguf` | Q4_K | 56 MB | Smaller but may miss some punctuation |

**Recommendation**: Use Q8_0. Token classification is more sensitive to quantization than language modeling — Q4_K occasionally drops commas that Q8_0 and F16 correctly predict.

## Example

Input (from CTC ASR):
```
and so my fellow americans ask not what your country can do for you ask what you can do for your country
```

Output (with FireRedPunc):
```
And so my fellow americans， ask not what your country can do for you， ask what you can do for your country？
```

## Conversion

```bash
python models/convert-fireredpunc-to-gguf.py \
  --input /path/to/FireRedPunc \
  --output fireredpunc.gguf
```

## Original Model

- **Source**: [FireRedTeam/FireRedPunc](https://huggingface.co/FireRedTeam/FireRedPunc)
- **Paper**: [FireRedASR2S](https://arxiv.org/abs/2603.10420)
- **Base**: [LERT (Linguistically-motivated BERT)](https://github.com/ymcui/LERT)
- **Training**: 18.57B Chinese characters + 2.20B English words

## Provenance and EU AI Act Art. 53 note

- **Upstream model:** [FireRedTeam/FireRedPunc](https://huggingface.co/FireRedTeam/FireRedPunc) — published by `FireRedTeam`.
- **Upstream licence:** `apache-2.0`. This repository redistributes under the same terms; it grants no rights the upstream licence does not.
- **What was done here:** format conversion and/or quantisation only (GGUF/GGML). No training, no fine-tuning, no merging, no distillation, no change to architecture, vocabulary or capability. Only the numeric representation of the upstream weights differs.
- **Training data:** documented — where it is documented at all — by the upstream provider; see the upstream model card. No training data was used, added or selected by this repository. No training-content summary was found on the upstream model card at the time of writing; that documentation gap is upstream's and is not filled here.
- **Provider status:** under Regulation (EU) 2024/1689 the upstream authors remain the provider of this model. Converting the serialisation format does not make this repository the provider of a new general-purpose AI model, and no such claim is made. Questions about training content, copyright policy or model capability belong upstream.
