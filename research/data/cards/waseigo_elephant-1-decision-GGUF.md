---
license: mit
base_model: baselabs/elephant-1
library_name: gguf
pipeline_tag: image-text-to-text
language:
  - en
tags:
  - gguf
  - decision-model
  - vision
  - llama-cpp
  - system-one
---

# elephant-1 — Q4_K_M, decision-wired GGUF

`baselabs/elephant-1` (9B decision model, Qwen3.5-9B post-train, vision) in **Q4_K_M**, with the
llama.cpp **decision metadata** and a `systemone` prompt template so that `POST /v1/systemone`
works.

- Base model: [`baselabs/elephant-1`](https://huggingface.co/baselabs/elephant-1) — MIT, Base Labs at Baseten.
- Q4_K_M weights and Q8_0 vision tower: [`mradermacher/elephant-1-GGUF`](https://huggingface.co/mradermacher/elephant-1-GGUF).
- This repo adds metadata/template only. **No weights were changed or re-quantized.**

## ⚠️ Correction (2026-10-25)

The first upload of this repo was **wrong** and has been replaced. Its template used `{{ o.label }}`,
but llama.cpp's `OPENJEV` renderer does not pass a `label` field for this decision type. The prompt
rendered as:

```
Options:
. billing: payments and refunds. shipping. technicalAnswer with one letter: , , .
```

The model saw no option letters. On the reference request it returned `billing` 0.513, while the
qev/BF16 reference returns 0.999. The corrected template generates the letters itself. The file in
this repo also carries `qwen35.attention.causal = false`, which the first upload was missing.

## Why this repo exists

A plain GGUF conversion of elephant-1 is a `qwen35` text model. llama.cpp/llama-swap's
`/v1/systemone` then answers `501 "This model is not a decision model"`, because the file has no
`<arch>.decision.*` keys and no named `systemone` template. The decision readout is headless —
qev's `slot_lm` falls back to the LM logits of the slot labels — which llama.cpp already implements
as `OPENJEV`.

This build adds:

| Key | Value |
|---|---|
| `qwen35.decision.type` | `openjev` |
| `qwen35.decision.temperature.choice` | `1.0` |
| `qwen35.decision.temperature.score` | `1.0` |
| `qwen35.decision.temperature.noul` | `1.0` |
| `qwen35.attention.causal` | `false` |
| `tokenizer.chat_template.systemone` | qev prompt template (see `systemone.jinja`) |

The template reproduces qev's `qev/prompt.py` layout **byte-for-byte** for `choice`, `noul` and
`score`, wrapped in the base Qwen chat template's markers. Verify with
`test-chat-template --no-common`; the choice/score/noul renders are identical to the transformers
`apply_chat_template` output that qev feeds the model.

Two template details matter and are easy to get wrong:

1. **Generate the labels in the template.** `OPENJEV` reads the logits of the label tokens (A–Z,
   a–z) but does not pass a `label` to the template. Use
   `{% set letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' %}` and
   `{{ letters[loop.index0] }}`.
2. **Emit newlines explicitly.** transformers' Jinja (`trim_blocks=True`) and llama.cpp's minja trim
   differently. A literal newline after a block tag disappears in minja, which concatenates option
   lines. Use `{{ '\n' }}`.

## Files

| File | Size | SHA-256 |
|---|---|---|
| `elephant-1-Q4_K_M.gguf` | 5,629,111,648 B | `5bc2a8f7c707da1680b49a3984a762478733f894eb38c9b4d07babf2f0004b6a` |
| `elephant-1.mmproj-Q8_0.gguf` | 624,229,760 B | `6906d682cc8ca0e353c39e4f9926c9a02c7770fd2f367ace5cb08c5b2cc48603` |
| `systemone.jinja` | 1,479 B | the template above |
| `graft_decision_metadata.py` | — | adds the decision keys + template to a plain GGUF |
| `graft_noncausal.py` | — | adds `qwen35.attention.causal = false` |

The source Q4_K_M was `10c77ea2339ffe7e012db453e77fa30762ba27377b117985db5141743ad17939`
(5,629,109,824 B). The grafted file is metadata-only; all 427 tensors keep their names and types
(`Q4_K` 217, `Q6_K` 33, `F32` 177).

## Usage

Build with decision support (llama.cpp b11820 or newer):

```bash
llama-server \
  -m elephant-1-Q4_K_M.gguf \
  --mmproj elephant-1.mmproj-Q8_0.gguf --mmproj-offload \
  --image-min-tokens 1024 -c 32768 -fa on --jinja --cache-ram 0 \
  --host 127.0.0.1 --port 8999
```

The log must say `decision model type: openjev`. `--mmproj-offload` keeps the vision tower on the
GPU. Pass `--cache-ram 0` explicitly when your server flags enable the RAM prompt cache; decision
models default to no prompt cache.

```bash
curl -s http://127.0.0.1:8999/v1/systemone -H 'Content-Type: application/json' -d '{
  "state": "I was charged twice for my order last week and nobody has replied.",
  "questions": {
    "route": {
      "type": "choice",
      "instructions": "Which team should handle this?",
      "criteria": {"billing": "payments and refunds", "shipping": null, "technical": null}
    },
    "urgency": {
      "type": "score",
      "instructions": "How urgent is this?",
      "criteria": ["can wait", "this week", "today", "right now"]
    },
    "angry": {"type": "noul", "instructions": "Is the customer angry?"}
  }
}'
```

## Validation against the qev reference

Reference: `baselabs/elephant-1` BF16 on CPU with OneJev `qev` at `81ce62f` + `serve.patch`
(transformers 5.19, torch 2.14.1+cpu, `attention=noncausal`, `readout=slot_lm`, calibration none).
llama.cpp: build 11858.

Same request as above:

| Decision | qev BF16 | this GGUF, CUDA, f16 KV | this GGUF, Vulkan, q8_0 KV |
|---|---|---|---|
| route `billing` | 0.999 | 0.990 | 0.993 |
| urgency score | 1.803 | 1.772 | 1.773 |
| angry | 0.778 | 0.760 | 0.752 |

8 states × 4 questions (`route` choice, `urgency` score, `angry` noul, `refund` noul with custom
criteria), compared question by question:

| Build | Agreement | Max probability delta |
|---|---|---|
| Q4_K_M (this file) | 28/32 (87.5%) | 0.260 |
| Q8_0, locally built | 29/32 (90.6%) | 0.198 |

- Choice: 8/8 identical.
- `angry` (noul): 8/8 identical at the 0.5 threshold.
- `refund` (noul): 7/8; the miss is a genuine coin flip in the reference (`0.530` vs `0.412`).
- Score: the expected value is close; the peak level differs on 3 near-ties (for example qev
  `1.80` vs llama.cpp `1.76`). This is the shape of a numerical delta, not a prompt or mask error:
  a Q8_0 build moves the agreement by one case and shrinks the maximum delta.

Images (skyline, Vulkan, tower on GPU, `--image-min-tokens 1024`): green swatch → `green` 0.998;
blue swatch → `blue` 0.991. The broken first build gave `green` 0.652 on the same kind of image.

## Caveats

- **Q4_K_M**: quantized by mradermacher. Quality tracks that quant, not BF16; the table above shows
  the size of the residual.
- **Attention mask**: the base declares `full_attention: block_bidirectional`. llama.cpp has no
  per-block mask key, so `attention.causal = false` makes the full-attention layers fully
  noncausal. Because llama.cpp evaluates the shared prefix on its own and each question suffix
  afterwards, this reproduces qev's two-block mask (prefix block, suffix block). A prompt that is
  evaluated as one unsplit batch would not have the same semantics.
- **Label space**: `OPENJEV` reads 52 single-token labels (A–Z, a–z). qev's `slot_lm` defines up to
  256 labels (A–Z plus two-letter codes). Up to 26 options is the validated path; larger option
  sets were not validated.
- **Temperature**: 1.0. The base repo has no `calibration.json`; qev's calibration defaults to
  identity.
- **JSON states**: a state object is rendered with `tojson(indent=2)`, matching qev's
  `json.dumps(..., indent=2)`. Non-ASCII escaping may differ from Python's `ensure_ascii=False`.

## Credits and license

- Model: Base Labs at Baseten, `baselabs/elephant-1`, MIT.
- Quant and vision tower: mradermacher, `mradermacher/elephant-1-GGUF`.
- Prompt/readout reference: OneJev `qev` (`qev/prompt.py`, `serve.patch`).
- llama.cpp decision models: ggml-org, PR #29818 and follow-ups.

The graft and this packaging are released under the base model's MIT terms. No warranty.
