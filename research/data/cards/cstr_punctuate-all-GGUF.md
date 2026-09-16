---
license: mit
language:
- en
- de
- fr
- es
- bg
- it
- pl
- nl
- cs
- pt
- sk
- sl
tags:
- gguf
- ggml
- punctuation
- text-processing
- xlm-roberta
- nlp
base_model: kredor/punctuate-all
pipeline_tag: token-classification
---

# Punctuate-All (GGUF)

GGUF conversion of [kredor/punctuate-all](https://huggingface.co/kredor/punctuate-all) for use with [CrispASR](https://github.com/CrispStrobe/CrispASR).

Adds punctuation to unpunctuated ASR output. **12 languages** with ASCII punctuation output. Smaller and faster alternative to fullstop-punc-multilang (base vs large).

## Model Details

- **Architecture**: XLM-RoBERTa-base — 12L, d=768, 12 heads, d_ffn=3072, GELU
- **Parameters**: ~278M
- **Classifier**: Linear(768, 6) — 6 punctuation classes
- **Labels**: none, `.` (period), `,` (comma), `?` (question), `-` (dash), `:` (colon)
- **Vocabulary**: SentencePiece (250,002 tokens)
- **Max sequence**: 512 tokens (auto-chunked)
- **Languages**: en, de, fr, es, bg, it, pl, nl, cs, pt, sk, sl
- **License**: MIT

## Usage with CrispASR

```bash
crispasr --backend wav2vec2 -m wav2vec2.gguf --punc-model punctuate-all -f audio.wav
```

## Available Files

| File | Quant | Size | Description |
|------|-------|------|-------------|
| `punctuate-all-q4_k.gguf` | Q4_K | 162 MB | **Recommended.** Rebuilt 2026-08-25 |
| `punctuate-all-f16.gguf` | F16 | 946 MB | Half precision. Rebuilt 2026-08-25 |
| `punctuate-all-orig-q4_k.gguf` | Q4_K | 161 MB | The original conversion, kept verbatim |
| `punctuate-all-orig-f16.gguf` | F16 | 945 MB | The original conversion, kept verbatim |

## What changed on 2026-08-25

The canonical files were rebuilt. The originals are preserved unchanged as
`punctuate-all-orig-*` — nothing was deleted.

**One real fix.** The original conversion shipped `tokenizer.ggml.tokens` but no
`tokenizer.ggml.scores`, so the runtime fell back to greedy longest-match.
XLM-R's SentencePiece model is **Unigram**, where greedy is not an approximation
but the wrong algorithm: `fox` has no `▁fox` piece, so Viterbi produces
`▁` + `fox` (ids 6, 147797) while greedy takes the longest prefix `▁fo` and is
left with `x` (5775, 425). Different ids, different embeddings, silently. On
public-domain prose the original matched HuggingFace's tokenizer on 0 of 7
segments; the rebuild matches on 6 of 7.

**One thing deliberately kept.** `kredor/punctuate-all` zeroes 9531 token
embedding rows — four contiguous ranges (4086–5449, 6816–9545, 10912–12276,
51895–55966), which look like pruned token ranges for languages it does not
serve. The original conversion happened to retain `xlm-roberta-base`'s vectors
there. That turns out to help, so the rebuild keeps it deliberately rather than
by accident, via `--restore-zeroed-embeddings-from xlm-roberta-base`.

## Measured

120 sentences of public-domain prose (English, German, French — 40 each,
2349 words, 350 marks), scoring restored punctuation against the original
editors'. `markF1` is exact-mark agreement; `bndF1` asks only whether a sentence
ended there, which is far less sensitive to house style.

| artifact | markF1 | bndF1 | per-word exact |
|---|--:|--:|--:|
| `punctuate-all-q4_k` (rebuild) | **0.771** | 0.922 | **0.944** |
| `punctuate-all-orig-q4_k` | 0.762 | 0.922 | 0.941 |
| faithful rebuild with kredor's zeroed rows | 0.713 | 0.884 | 0.931 |

Paired bootstrap, 2000 resamples, 95% interval on the markF1 difference:

```
rebuild vs orig                      +0.0092  [-0.0174, +0.0344]  not distinguishable
rebuild vs kredor's zeroed rows      +0.0542  [+0.0245, +0.0838]  significant
```

So the rebuild is **at least as good** as the original on punctuation quality
and additionally tokenizes correctly. Restoring the zeroed embeddings is a real,
significant gain — those zero rows cost quality.

## ⚠ Note for anyone running a parity check

**No file in this repo** will match a reference dumped from
`kredor/punctuate-all` via `transformers` on text that uses the 9531 zeroed
rows — not the rebuild and not the originals, for the same reason in both cases.
`transformers` loads the zeros; every file here carries base vectors there.

That is by design, not a defect, and it is why the rebuild scores where it does.
If you need blueprint-exact behaviour, convert `kredor/punctuate-all` yourself
**without** `--restore-zeroed-embeddings-from` and expect the third row of the
table above (markF1 0.713).

## Original Model

- **Source**: [kredor/punctuate-all](https://huggingface.co/kredor/punctuate-all)
- **Training**: WMT/Europarl dataset
- **Conversion**: `models/convert-fullstop-punc-to-gguf.py` in
  [CrispASR](https://github.com/CrispStrobe/CrispASR)
