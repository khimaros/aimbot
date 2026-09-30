---
license: cc-by-sa-3.0
library_name: gguf
pipeline_tag: text-classification
tags:
  - language-identification
  - lid
  - fasttext
  - gguf
  - ggml
  - crispasr
  - hierarchical-softmax
language:
  - multilingual
---

# fastText LID-176 — GGUF

GGUF build of Facebook's [`lid.176.bin`](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin)
fastText supervised LID classifier covering **176 languages** with
ISO 639-1 short codes (`en`, `de`, `fr`, `ru`, `zh`, `ja`, …).

Designed to drop into the [crispasr](https://github.com/CrispStrobe/CrispASR)
runtime alongside the GlotLID-V3 GGUF for post-ASR text language
identification.

## ⚠️ License — CC-BY-SA-3.0 (viral)

The upstream `lid.176.bin` is distributed under
**Creative Commons Attribution-ShareAlike 3.0** ([CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/)).
Anyone redistributing this GGUF — or anything derived from it that
includes its weights — **must keep the same license terms**:

- Attribute Facebook (the upstream authors).
- Distribute under CC-BY-SA-3.0 or a compatible license.

This is more restrictive than most ASR/LID models on the Hub. If
that does not match your project's license posture, use the
[GlotLID-V3 GGUF](https://huggingface.co/cstr/glotlid-GGUF)
(Apache-2.0) instead — it covers a strict superset of LID-176's
languages.

## Files

| Quant | Size | Notes |
|-------|------|-------|
| F16   | 63 MB | only quant shipped — the input matrix is small (`dim=16`) so K-quants degrade quality more than they save space |

K-quants require 256-element row alignment; LID-176's `dim=16`
rows are below that, so K-quants would silently fall back to legacy
Q4_0 / Q5_0 / Q8_0. The F16 build is already small enough that
quantization is not worth the loss in precision — the embedding bag
fits entirely in L1 cache regardless.

## Architecture — hierarchical softmax

Unlike GlotLID (flat softmax), LID-176 uses fastText's hierarchical
softmax (HS) loss with a deterministic Huffman tree built from
training-frequency label counts. The output matrix's `n_labels` rows
parameterize internal tree nodes; per-label log-probability is
computed by walking from the leaf to the root and summing
`log_sigmoid((2*code - 1) * (output[node] · hidden))` along the path.

Tensors:

- `lid_fasttext.embedding.weight`     `[n_words + bucket, dim]` = `[2,040,010, 16]`
- `lid_fasttext.output.weight`        `[n_labels, dim]`         = `[176, 16]`
- `lid_fasttext.hs_path_offsets`      `[n_labels + 1] i32`      — CSR-style path offsets per label
- `lid_fasttext.hs_paths`             `[total_steps] i32`       — flattened internal-node indices
- `lid_fasttext.hs_codes`             `[total_steps] i8`        — flattened code bits (0/1) per step

Hyperparams:

- `n_words = 40,010`
- `bucket  = 2,000,000`
- `dim     = 16`
- `n_labels = 176`
- `minn, maxn = 2, 4`
- `loss = hs`
- `wordNgrams = 1`
- HS tree: 1,855 total path steps, average path length 10.54

## Use with crispasr

Standalone text-LID CLI:

```sh
crispasr-lid -m fasttext-lid176-f16.gguf --text "Hallo Welt"
# de  0.999

crispasr-lid -m fasttext-lid176-f16.gguf -k 3 < transcript.txt
```

Post-ASR via main `crispasr` binary:

```sh
crispasr -m ggml-base.bin -f input.wav \
    --lid-on-transcript fasttext-lid176-f16.gguf
# lang=en  conf=0.934
```

## Validation

Per-stage diff harness against a Python ground-truth dump (uses
`fasttext.predict()` as the reference for HS top-1 labels):

```
[PASS] input_ids          shape=[163]   cos=1.000000  max_abs=0.00e+00
[PASS] embedding_bag_out  shape=[16]    cos=1.000000  max_abs=3.55e-05
[PASS] logits             shape=[176]   cos=1.000000  max_abs=1.48e-03
[PASS] softmax            shape=[176]   cos=1.000000  max_abs=6.54e-05
[PASS] top1_score         shape=[1]     cos=1.000000
[INFO] top1_label         ours='fr'  ref='fr'
```

8/8 multilingual smoke tests correctly identified
(en/de/fr/ru/zh/ja/pt; mr/hi can swap on 2-word Devanagari inputs —
this is upstream model behaviour, not a port artefact).

## Conversion

Built via crispasr's `models/convert-glotlid-to-gguf.py` (the same
converter handles both flat-softmax GlotLID and HS LID-176 — variant
flag selects which):

```sh
python models/convert-glotlid-to-gguf.py \
    --variant fasttext-lid176 \
    --input  /path/to/lid.176.bin \
    --output fasttext-lid176-f16.gguf \
    --dtype  f16
```

The converter parses `lid.176.bin` directly to extract per-label
training frequencies, deterministically rebuilds fastText's Huffman
tree (port of `Model::buildTree` from the upstream source), and emits
the path/code metadata alongside the weights.

## Citation & license

Upstream:

- Joulin, A., Grave, E., Bojanowski, P., Mikolov, T. *Bag of Tricks for
  Efficient Text Classification.* EACL 2017.
- Joulin, A., Grave, E., Bojanowski, P., Douze, M., Jégou, H.,
  Mikolov, T. *FastText.zip: Compressing text classification models.*

This GGUF rebuild inherits the upstream **CC-BY-SA-3.0** license.
Redistributors must preserve the SA terms.

## Note on `base_model` (corrected 2026-08-02)

This repo's frontmatter pointed at
[`facebook/fasttext-language-identification`](https://huggingface.co/facebook/fasttext-language-identification),
which is a **different model** — the NLLB-based LID-201 classifier, published
under CC-BY-NC-4.0. The weights here are Facebook's original
[`lid.176.bin`](https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin),
distributed from fasttext.cc under **CC-BY-SA-3.0**, exactly as the licence
section above describes.

The pointer has been removed rather than repaired, because `lid.176.bin` has no
Hub repo to point at. The licence field was already correct and is unchanged —
recording that here because an automated sweep flagged this repo as a licence
mismatch on the strength of the wrong pointer, and relabelling it
non-commercial would have imposed a restriction the upstream does not.
