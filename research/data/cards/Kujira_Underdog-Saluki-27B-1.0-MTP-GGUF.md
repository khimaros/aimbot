---
license: apache-2.0
base_model:
  - ConwayResearch/Underdog-Saluki-27B-1.0
  - Qwen/Qwen3.8-27B
base_model_relation: quantized
pipeline_tag: text-generation
language:
  - en
library_name: gguf
tags:
  - gguf
  - llama.cpp
  - 2-bit
  - mtp
  - speculative-decoding
  - tool-calling
  - agents
  - qwen3.8
---

# Underdog Saluki 27B 1.0 + MTP (GGUF)

[Underdog Saluki 27B 1.0](https://huggingface.co/ConwayResearch/Underdog-Saluki-27B-1.0) with the
**Qwen3.8-27B multi-token-prediction (MTP) head** added, so llama.cpp can run it with
self-speculative decoding (`--spec-type draft-mtp`). The original Saluki release has no MTP head.

| | |
|---|---|
| File | `Underdog-Saluki-27B-1.0-IQ2-mix-MTP.gguf`, 8.35 GB |
| sha256 | `98f6ebb527917a2541df8e667d51c3ec8a8bb135b44c606d40cc6ed924e89e52` |
| Main weights | all 851 tensors **byte-identical** to Saluki's `Underdog-Saluki-27B-1.0-IQ2-mix.gguf` (sha256 `4a673518…5d9efb`, revision `1336c0b`) |
| Added | 15 tensors `blk.64.*` (the MTP layer, Q8_0/F32, ~0.45 GB); `qwen35.block_count` 64 → 65; `qwen35.nextn_predict_layers = 1` |
| MTP head origin | Qwen3.8-27B's own MTP head as quantized in `unsloth/Qwen3.8-27B-GGUF`, taken verbatim from `BoldingBuilds/Ternary-Bonsai-2-27B-Abliterated-v2-PQ2_0-MTP-GGUF` (sha256 `a4e4c7b5…3ebebf8`) |

Nothing was trained or re-quantized. Saluki is built from Qwen3.8-27B, so the head is the one that
belongs to its base model.

## Usage

Works with stock llama.cpp (tested on upstream `03aa006`, 2026-10-08, just after release `b11493`)
and any build that has MTP drafting (`--spec-type draft-mtp`).

```bash
llama-server -m Underdog-Saluki-27B-1.0-IQ2-mix-MTP.gguf --jinja -ngl 99 -fa on \
  -c 32768 -np 1 -ctk q8_0 -ctv q8_0 \
  --spec-type draft-mtp --spec-draft-n-max 2
```

Sampling and thinking settings are the same as for Saluki (see its card). Without the
`--spec-type` flags the file runs like the original Saluki: llama.cpp logs the MTP tensors as unused,
skips them, and uses the same VRAM as the original file.

## Measured (one machine)

RTX 3080 12 GB, WSL2, 32K context, q8_0 KV cache, `-np 1`, 6 prompts (code / Japanese / English,
thinking on and off), temperature 0.

**Stock llama.cpp** (upstream `03aa006`):

| | Original Saluki | This file, no `--spec-type` | **This file, MTP on** |
|---|---|---|---|
| Generation (mean of 6) | 41.2 tok/s | 40.7 tok/s | **66.2 tok/s** (58–75) |
| Draft acceptance | — | — | 62–96% |
| VRAM | 10.3 GB | 10.3 GB | 11.5 GB |

**PrismML fork** `prism-b10754-2459f68` ([PrismML-Eng/llama.cpp](https://github.com/PrismML-Eng/llama.cpp)):
42.7 → **68.2 tok/s** (58–77), acceptance 60–96%, 10.9 GB VRAM with MTP on.

- **Not bit-identical to Saluki at temperature 0.** The MTP path verifies drafts in batches, which
  changes floating-point accumulation order, so near-tied tokens sometimes flip (e.g. "約2万円" vs
  "2万円"). In 6 test prompts, 1 matched exactly and 5 diverged at a near-tie, after 9–95% of the text.
- **12 GB cards: keep the context at 32K.** With 64K context + q8_0 KV + MTP the VRAM overflowed on
  this machine and speed fell to 24–29 tok/s.
- No new benchmarks: the quality numbers on Saluki's card are for the original file. Two small agent
  tasks (write a module with tests; fix three bugs) were passed through
  [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) with MTP on.

## Reproduce

`graft_mtp.py` in this repo builds the file from the two upstream GGUFs (needs `gguf-py` from llama.cpp):

```bash
ALLOW_TYPE_MISMATCH=1 python graft_mtp.py <llama.cpp>/gguf-py \
  Underdog-Saluki-27B-1.0-IQ2-mix.gguf \
  Ternary-Bonsai-2-27B-Abliterated-v2-PQ2_0-MTP.gguf \
  Underdog-Saluki-27B-1.0-IQ2-mix-MTP.gguf
```

Only the donor's `blk.64.*` tensors and MTP metadata are used. `ALLOW_TYPE_MISMATCH=1` is needed
because the donor's main weights are a different quantization (PQ2_0); they are checked for matching
shapes and then ignored.

## Credits and license

Apache-2.0, see `LICENSE` and `NOTICE`.

- **Underdog Saluki 27B 1.0** by Underdog (ConwayResearch), built on Qwen3.8-27B and ISTA-DASLab's Qwen3.8-27B-GSQ-RCO-GGUF.
- **Qwen3.8-27B** and its MTP head by the Qwen team.
- MTP head GGUF quantization by **Unsloth** (`unsloth/Qwen3.8-27B-GGUF`).
- The MTP grafting approach credited by BoldingBuilds to decent-jawfish, ProCreations and sudoingX/qwen38-mtp.

Not affiliated with or endorsed by Underdog/ConwayResearch, Qwen, Unsloth, PrismML or BoldingBuilds.

## 日本語メモ

Underdog Saluki 27B 1.0 に、Qwen3.8-27B 公式の MTP ヘッド（15 テンソル）を足しただけのファイルです。
本体の重みは元ファイルとバイト単位で同一です。普通の llama.cpp で動きます。RTX 3080 12GB で 41 → 66 tok/s（平均）になりました。
12GB のカードでは文脈を 32K に抑えてください（64K だと VRAM が溢れて遅くなります）。
