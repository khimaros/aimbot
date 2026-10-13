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
> pin a full commit revision. Earlier versions stay available under the tags `v1`, `v1.1` and `v2`.


> **Decision API update (2026-10-08).** All nine `StandardOne-8B-*.gguf` language model files now support stock llama.cpp's text `/v1/systemone` endpoint. Only five metadata fields were added; every tensor byte is unchanged. Download the updated files from `main`. The pre-update binaries remain at `v2.2`. `mmproj` is unchanged. See [Decision API quick start](#decision-api-quick-start).

**Version:** v2.2 weights + decision metadata (2026-10-08)

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

## Decision API quick start

Use any of the nine language model files in this repository; Q4_K_M is used below as an example.
The update uses llama.cpp's existing `openjev` letter-logit readout with a Standard One native template.
It is still Standard One weights. No engine fork, adapter server, or new weight conversion is needed.
To use another precision, replace the Q4_K_M filename in the download, checksum verification, and server commands with the selected filename from the table. All nine files use the same endpoint.

### 1. Install and download

Use the tested official [llama.cpp b11495 release](https://github.com/ggml-org/llama.cpp/releases/tag/b11495)
for your platform. Extract the runtime, retain its companion libraries, and put
`llama-server` on `PATH` (or use the full executable path). This release reports
`0.6.0-dev`, commit `37ac63456`. Older builds may lack the decision endpoint;
newer builds were not tested here.

In a Python 3.10+ virtual environment, install the Hub CLI:

```bash
python -m pip install --upgrade huggingface_hub
hf download StandardThinking/StandardOne-8B-GGUF \
  StandardOne-8B-Q4_K_M.gguf SHA256SUMS release-manifest.json \
  --revision main --local-dir models/standardone-8b-systemone
```

These shell examples use Bash/Zsh. The repository is public; login is unnecessary.
For a reproducible snapshot, replace `main` with a full commit hash from
[Files and versions](https://huggingface.co/StandardThinking/StandardOne-8B-GGUF/tree/main).
The `v2.2` tag contains the original binaries without decision metadata. Use `main` or the metadata-update commit for this endpoint.

Verify just the downloaded model (the other entries in `SHA256SUMS` are optional):

```bash
python - <<'PYVERIFY'
import hashlib
from pathlib import Path
root = Path("models/standardone-8b-systemone")
name = "StandardOne-8B-Q4_K_M.gguf"
expected = {}
for line in (root / "SHA256SUMS").read_text().splitlines():
    if line.strip():
        digest, filename = line.split(maxsplit=1)
        expected[filename.lstrip("*")] = digest
h = hashlib.sha256()
with (root / name).open("rb") as stream:
    for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
        h.update(chunk)
if h.hexdigest() != expected.get(name):
    raise SystemExit("SHA256 mismatch")
print("SHA256 OK")
PYVERIFY
```

### 2. Run the local decision endpoint

```bash
llama-server \
  -m models/standardone-8b-systemone/StandardOne-8B-Q4_K_M.gguf \
  -ngl 0 -t 4 -tb 4 -c 4096 -np 1 --jinja \
  --host 127.0.0.1 --port 8080 --alias standardone-8b
```

This is the tested CPU configuration. The model file is about 5.2 GB; RAM use
also includes the KV cache and working buffers. Keep the server running. In
another terminal, wait until `curl --fail http://127.0.0.1:8080/health` returns
`{"status":"ok"}`. Stop the server with `Ctrl+C` when finished.
GPU offload and image input were not validated for this decision API.

### 3. Send Jev-style typed questions

```bash
curl --fail http://127.0.0.1:8080/v1/systemone \
  -H 'Content-Type: application/json' \
  --data-binary @- <<'JSON'
{
  "state": "A parcel has a large tear and its contents are visible.",
  "questions": {
    "route": {
      "type": "choice",
      "instructions": "Should this parcel pass inspection?",
      "criteria": {
        "pass": "The packaging is intact.",
        "review": "The packaging is visibly damaged.",
        "unclear": "There is not enough information."
      }
    },
    "damaged": {
      "type": "noul",
      "instructions": "Is the packaging visibly damaged?",
      "criteria": {
        "true": "A large tear is visible.",
        "false": "The packaging is intact."
      }
    },
    "damage": {
      "type": "score",
      "instructions": "How damaged is the packaging?",
      "criteria": ["intact", "minor cosmetic damage", "large tear with visible contents"]
    }
  }
}
JSON
```

Read `answers.route.choice` and `answers.route.probabilities`,
`answers.damaged.noul` (probability of yes), and `answers.damage.score`
(expected zero-based level). `score` can be fractional. The server constructs
JSON from option logits; the model does not generate a letter or JSON text.
`usage.output_tokens` is **0**. A downloadable request is in
[`systemone-request.json`](systemone-request.json).

The request demonstrates the response fields. Values differ across model sizes and quantizations; inspect the live response rather than treating one fixture as an accuracy guarantee.

### What was verified, and what differs from the merged model's served endpoint

Each of the **nine files** passed six real-model fixtures: `choice`, `noul`, `score`, object state, reversed lexical choice-key order, and all three types in one request. Direct option-logprob readout agreed within **5.27e-09** for single-question fixtures and **4.44e-09** for the multi-question fixture. Multi-question reference calls follow the same question order and reuse prefix state after the first question. Independently prefilled references can differ due to CPU batching and cache behavior. Per-file results and tolerances are in [`systemone-validation.json`](systemone-validation.json). These checks verify endpoint calculations, not task accuracy.

- This API uses the **native** prompt, with temperatures `choice=0.85`,
  `noul=0.85`, `score=0.70`. They are the published native preset carried forward
  from v2 fitting, not temperatures fitted on these quantized weights.
- The current merged v2.2 default endpoint uses **served** wording, temperature
  1.65, and extended uppercase labels. This implementation does not reproduce that preset.
- Supply at most **26 options**. The embedded template rejects more; do not infer
  Standard One support for the underlying `openjev` path's larger label count.
- Text `state`, string `instructions`, string choice descriptions, and
  string score levels are the tested path. Object state is supported by
  this template, but preserves submitted key order; the existing adapter's native
  state renderer sorts keys. Keep state and option ordering fixed for comparisons.
- llama.cpp's `confidence` formulas differ from the existing adapter's normalized
  entropy. Matching probability fields does not imply identical confidence semantics.
- All **nine 8B language files** were tested on CPU with text requests. GPU execution, images, structured question/description values, and complete request-option/error parity are unverified. Do not send images to this text-only template.

The template is published as [`systemone-native-template.jinja`](systemone-native-template.jinja).
The [release manifest](release-manifest.json) records every added metadata field
and the identical tensor-data hash. Current checksums reflect the added metadata. Original binaries and checksums remain in the `v2.2` snapshot; the manifest also records every source-file SHA256.
For the default BF16 endpoint, use the
[merged model's serving instructions](https://huggingface.co/StandardThinking/StandardOne-8B#serving).

## Importance-matrix calibration

`Q5_K_M` down to `IQ2_M` were quantized with `llama-imatrix` calibrated on 1,512 prompts (spread evenly across 72 training-data cohorts; training data only — no benchmark/held-out file was used), context 2048. `Q8_0` and `BF16` don't
use an imatrix (high enough precision that it doesn't move the needle).

## Historical weight accuracy validation

The following measurements predate the metadata update. Tensor data is unchanged; these are not a new benchmark of the native decision endpoint.

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

## Update history

### 2026-10-08 — llama.cpp decision API metadata

- Added metadata for stock llama.cpp's `/v1/systemone` endpoint to **all nine language GGUF files**: BF16, Q8_0, Q5_K_M, Q4_K_M, IQ4_XS, Q3_K_M, IQ3_M, Q2_K, and IQ2_M.
- Added the decision type, a named native decision template, and per-type temperatures. **The v2.2 weights and every tensor byte are unchanged**; the vision projector (`mmproj`) is unchanged.
- Verified `choice`, `noul`, and `score` with official llama.cpp **b11495** on every precision: **54 API fixture requests** for this repository, including object state, option order, and multi-question requests. See [`systemone-validation.json`](systemone-validation.json).
- Added decision endpoint instructions and request examples, and updated `SHA256SUMS` and `release-manifest.json`. This implementation uses native wording with **at most 26 options and text input**; it does not reproduce the merged model's default served preset.
- Pre-update GGUF binaries remain available at `v2.2`. [Metadata update commit](https://huggingface.co/StandardThinking/StandardOne-8B-GGUF/commit/2dc26d974fa076caf0e985f01aa020a97ac66736).

## License

Apache License 2.0 — see `LICENSE` and `NOTICE`. Same terms as the source `StandardOne-8B` release;
this GGUF conversion adds no additional restrictions.
