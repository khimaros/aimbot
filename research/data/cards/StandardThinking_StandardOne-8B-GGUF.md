---
base_model: StandardThinking/StandardOne-8B
base_model_relation: quantized
license: apache-2.0
library_name: gguf
pipeline_tag: text-generation
tags:
  - gguf
  - llama.cpp
  - mistral3
  - decision-model
---

# Standard One 8B — GGUF

> **Updated weights (v2.2, 2026-10-04).** These files are built from Standard One 8B v2.2. If you downloaded them before, download them again or
> pin `revision="v2.2"`. Earlier versions stay available under the tags `v1`, `v1.1` and `v2`.

**Version:** v2.2

GGUF builds of [Standard One 8B](https://huggingface.co/StandardThinking/StandardOne-8B) (Ministral 3 8B text + Pixtral vision tower,
`mistral3` architecture) for use with [llama.cpp](https://github.com/ggml-org/llama.cpp).

## Files

Most quant levels below (marked "imatrix") were built with an importance matrix calibrated on 1,512
prompts sampled from our own training rows (see "Importance-matrix calibration" below), which
recovers some of the accuracy quantization would otherwise lose. `Q8_0` and `BF16` don't need one.

| File | Quant | Size | imatrix |
|---|---|---:|:---:|
| `StandardOne-8B-BF16.gguf` | BF16 (no quantization) | 17.0 GB | — |
| `StandardOne-8B-Q8_0.gguf` | Q8_0 | 9.0 GB | no |
| `StandardOne-8B-Q5_K_M.gguf` | Q5_K_M | 6.1 GB | yes |
| `StandardOne-8B-Q4_K_M.gguf` | Q4_K_M | 5.2 GB | yes |
| `StandardOne-8B-IQ4_XS.gguf` | IQ4_XS | 4.7 GB | yes |
| `StandardOne-8B-Q3_K_M.gguf` | Q3_K_M | 4.2 GB | yes |
| `StandardOne-8B-IQ3_M.gguf` | IQ3_M | 4.0 GB | yes |
| `StandardOne-8B-Q2_K.gguf` | Q2_K | 3.4 GB | yes |
| `StandardOne-8B-IQ2_M.gguf` | IQ2_M | 3.1 GB | yes |
| `mmproj-StandardOne-8B.gguf` | F16 vision projector | 857 MB | — |

SHA256 checksums: `SHA256SUMS`. Source revisions, conversion tool version and full validation
numbers: `release-manifest.json`.

**Q4_K_M note:** this is the imatrix-calibrated version, not a plain quantization. We generated both and
chose whichever scored higher on the mean of 10 held-out and public-dataset decision suites (no JevBench items; imatrix 76.56 vs. plain 76.33; measured on an earlier version). v2.2 keeps the imatrix build.

## Usage

Text-only:

```
llama-cli -m StandardOne-8B-Q4_K_M.gguf -ngl 99 -p "Your prompt"
```

With vision (image input):

```
llama-server -m StandardOne-8B-Q4_K_M.gguf --mmproj mmproj-StandardOne-8B.gguf -ngl 99
```

The GGUF's own embedded chat template (converted from the model's `chat_template.jinja`) is applied
automatically; no extra flags needed for chat formatting.

## Importance-matrix calibration

`Q5_K_M` down to `IQ2_M` were quantized with `llama-imatrix` calibrated on 1,512 prompts (spread evenly across 72 training-data cohorts; training data only — no benchmark/held-out file was used), context 2048. `Q8_0` and `BF16` don't
use an imatrix (high enough precision that it doesn't move the needle).

## Validation

CPU check of v2.2 with llama.cpp `llama-server` (no GPU offload): accuracy of the most probable option label at the
answer position, native prompt wording, GGUF's own chat template, one option order, measured 2026-10-04.
BF16-GGUF, Q8_0, Q4_K_M and IQ2_M were scored on all suites below; the other quants on the two JevBench tiers.
Score changes from v2.1 to v2.2 are listed in the
[StandardOne-8B card](https://huggingface.co/StandardThinking/StandardOne-8B#changes-in-v22).

| Quant | Easy (48) | Original (72) | Judge proxy (60) | Realistic (60) | Hard proxy (80) | Same answer as BF16-GGUF |
|---|---:|---:|---:|---:|---:|---:|
| BF16-GGUF | 100.00 | 97.22 | 90.00 | 68.33 | 56.25 | — |
| Q8_0 | 100.00 | 98.61 | 90.00 | 68.33 | 56.25 | 99.06 % (n=320) |
| Q5_K_M | 100.00 | 97.22 | — | — | — | 100.00 % (n=120) |
| Q4_K_M (shipped, imatrix) | 100.00 | 95.83 | 91.67 | 66.67 | 50.00 | 94.69 % (n=320) |
| IQ4_XS | 100.00 | 98.61 | — | — | — | 99.17 % (n=120) |
| Q3_K_M | 100.00 | 93.06 | — | — | — | 97.50 % (n=120) |
| IQ3_M | 100.00 | 88.89 | — | — | — | 93.33 % (n=120) |
| Q2_K | 100.00 | 94.44 | — | — | — | 95.00 % (n=120) |
| IQ2_M | 100.00 | 87.50 | 86.67 | 65.00 | 45.00 | 86.88 % (n=320) |

## Note on the mmproj conversion

llama.cpp's stock `--mmproj` converter (as of the commit used here) drops the `[IMG_BREAK]` token
embedding for HF-format `Mistral3ForConditionalGeneration` checkpoints (a filter meant to strip
text-model tensors also strips the one row of the text embedding matrix the vision projector needs),
so the mmproj file it produces fails to load in `llama-server`/`llama-cli`
("unable to find tensor v.token_embd.img_break"). The mmproj file in this folder was built with a
small local patch that lets that one tensor through; see `release-manifest.json` ->
`known_issues_fixed` for details. It loads and runs correctly with `--mmproj`.

## License

Apache License 2.0 — see `LICENSE` and `NOTICE`. Same terms as the source `StandardOne-8B` release;
this GGUF conversion adds no additional restrictions.
