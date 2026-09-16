---
license: apache-2.0
base_model: cis-lmu/glotlid
base_model_relation: quantized
library_name: gguf
pipeline_tag: text-classification
tags:
  - language-identification
  - lid
  - fasttext
  - gguf
  - ggml
  - crispasr
language:
  - multilingual
---

# GlotLID-V3 — GGUF

GGUF builds of [`cis-lmu/glotlid`](https://huggingface.co/cis-lmu/glotlid)
(V3, Apache-2.0) — a fastText-supervised classifier covering **2,102
languages × scripts** (ISO 639-3 + ISO 15924, e.g. `eng_Latn`,
`deu_Latn`, `cmn_Hani`, `arb_Arab`).

Designed to drop into the [crispasr](https://github.com/CrispStrobe/CrispASR)
runtime as a post-ASR text language identifier. The native fastText
`.bin` format is converted to GGUF so the C++ runtime can mmap weights
and dequantize on the fly without a Python dependency.

## Files

| Quant | Size  | embedding_bag cos | logits cos | softmax cos | When to use |
|-------|-------|-------------------|------------|-------------|-------------|
| F16   | 808 MB | 1.0 | 1.0 | 1.0 | reference / accuracy-critical |
| Q8_0  | 434 MB | 0.999990 | 0.999991 | 1.000000 | recommended default |
| Q5_K  | 284 MB | 0.999440 | 0.999530 | 1.000000 | smaller, still passes 0.999 floor |
| Q4_K  | 234 MB | 0.998303 | 0.998356 | 1.000000 | smallest; below 0.999 cosine floor on intermediate stages — top-1 stable across 8 multilingual smoke tests |

Cosine numbers are vs the F32 reference (`model.predict()` cross-checked
against the upstream fastText forward) on a held-out English sample.
Top-1 label is identical across all four quants on the standard
multilingual smoke set (en/de/fr/ru/zh/ja/hi/pt).

## Architecture

Hashed character n-gram embedding bag → mean pool → linear → flat
softmax. Two tensors:

- `lid_fasttext.embedding.weight`  `[n_words + bucket, dim]`  = `[1,634,361, 256]`
- `lid_fasttext.output.weight`     `[n_labels, dim]`           = `[2,102, 256]`

Where:

- `n_words = 634,361` (in-vocab word embeddings, used as additional
  rows looked up alongside subword bucket hashes)
- `bucket  = 1,000,000` (hashed n-gram buckets, indices `n_words..n_words+bucket`)
- `dim     = 256`
- `n_labels = 2,102`
- `minn, maxn = 2, 5` (char n-gram lengths)
- `loss = softmax` (flat — distinct from LID-176, which uses HS)
- `wordNgrams = 1`

## Use with crispasr

Standalone text-LID CLI:

```sh
crispasr-lid -m glotlid-q8_0.gguf --text "Hallo Welt"
# deu_Latn  0.999

crispasr-lid -m glotlid-q8_0.gguf -k 5 < transcript.txt
```

Post-ASR via main `crispasr` binary:

```sh
crispasr -m ggml-base.bin -f input.wav \
    --lid-on-transcript glotlid-q8_0.gguf
# [00:00:00.000 --> ...]   And so, my fellow Americans...
# lang=eng_Latn  conf=0.999712
```

Per-stage diff harness (validates a quantized GGUF against a Python
ground-truth dump):

```sh
python tools/dump_reference.py --backend lid-glotlid \
    --model-dir /path/to/glotlid \
    --audio samples/jfk.wav \
    --output /tmp/glotlid-ref.gguf
crispasr-diff lid-glotlid glotlid-q8_0.gguf /tmp/glotlid-ref.gguf samples/jfk.wav
```

## Conversion

Built from the upstream `model.bin` via the converter shipped with
crispasr at `models/convert-glotlid-to-gguf.py`:

```sh
python models/convert-glotlid-to-gguf.py \
    --variant glotlid-v3 \
    --input  /path/to/glotlid/model.bin \
    --output glotlid-f16.gguf \
    --dtype  f16
crispasr-quantize glotlid-f16.gguf glotlid-q8_0.gguf q8_0
```

## Citation & license

Upstream model: cis-lmu/glotlid V3, Apache-2.0. If you use this in
research, cite:

```bibtex
@inproceedings{kargaran2023glotlid,
  title={GlotLID: Language Identification for Low-Resource Languages},
  author={Kargaran, Amir Hossein and Imani, Ayyoob and Yvon, Fran{\c{c}}ois and Sch{\"u}tze, Hinrich},
  booktitle={Findings of EMNLP 2023},
  year={2023}
}
```

This GGUF rebuild inherits the upstream Apache-2.0 license. No
additional restrictions.
