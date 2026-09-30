---
base_model: mistralai/Ministral-3-8B-Instruct-2512-BF16
library_name: transformers
license: apache-2.0
pipeline_tag: text-generation
language:
  - en
  - ja
  - zh
  - es
  - fr
  - de
  - pt
  - ru
  - ko
tags:
  - mistral3
  - decision-model
  - typed-decisions
  - jev
  - jevbench
  - calibration
  - decode-free
  - multilingual
  - vision-language
---

# Standard One 8B

> **Updated weights (v2, 2026-09-26).** If you downloaded this model before, download it again or pin
> `revision="v2"`. Earlier versions stay available under the tags `v1` and `v1.1`.

**Version:** v2

Standard One scores a bounded set of answers for a supplied scenario and returns probabilities through
`POST /v1/systemone`. It does not generate free-form response text. This repository contains the merged
BF16 8B checkpoint and the server code.

| If you need | Repository |
|---|---|
| Merged 8B checkpoint and server code | [StandardOne-8B](https://huggingface.co/StandardThinking/StandardOne-8B) (this repository) |
| 8B adapter weights and merge recipe | [StandardOne-8B-LoRA](https://huggingface.co/StandardThinking/StandardOne-8B-LoRA) |
| Smaller merged checkpoint | [StandardOne-3B](https://huggingface.co/StandardThinking/StandardOne-3B) |
| Smaller adapter weights and merge recipe | [StandardOne-3B-LoRA](https://huggingface.co/StandardThinking/StandardOne-3B-LoRA) |

In the reported served evaluations, 8B scores higher than 3B on the public standard and hard tiers;
3B has a lower median latency on the measured short-request profile. See [Benchmarks](#benchmarks)
for the measurement conditions and limitations.

![Standard One benchmark card: JevBench public tiers, held-out suites, stated-distribution probability, hard-tier calibration, latency and throughput for Standard One 8B, Standard One 3B and Jev 1.13.](docs/assets/00-benchmark-card.png)

*The figure combines results from different measurement paths. See [Benchmarks](#benchmarks) for
served versus offline conditions; measured 24–26 September 2026.*

## At a glance

- Send a state and a bounded rubric to receive probabilities for the supplied labels:
  `choice` selects among labeled options, `noul` is yes/no, and `score` uses an ordinal scale.
  The endpoint scores the labels in one forward pass without decoding answer text.
- In the same-run **offline** comparison with its untuned base, 8B improves on four of six suites and declines on public easy (2.08 percentage points) and public hard (4.50 percentage points). These are not
  served-endpoint results.
- Probabilities are temperature-scaled and calibration-checked (hard-tier ECE, distribution
  total-variation) — see Benchmarks below.
- The shared training mixture covers English, Japanese, Chinese, Spanish, French, German,
  Portuguese, Russian, and a smaller Korean share. See the nine-language MASSIVE intent results in
  [`docs/public-classification-suites.md`](docs/public-classification-suites.md); performance varies
  by language. The retained Pixtral vision tower accepts image data URLs; no separate image-input
  decision benchmark is reported.
- Apache-2.0: base model, adapter, merged weights, and shared server code hosted in the 8B repository.

## Quantized versions

| Format | Repository |
|---|---|
| FP8 (compressed-tensors, validated with SGLang) | [StandardOne-8B-FP8](https://huggingface.co/StandardThinking/StandardOne-8B-FP8) |
| GGUF for llama.cpp (BF16, Q8_0 down to IQ2_M, vision projector) | [StandardOne-8B-GGUF](https://huggingface.co/StandardThinking/StandardOne-8B-GGUF) |

Validation numbers are in each repository's card.

## Quick start

Follow the setup in [QUICKSTART.md](QUICKSTART.md#standard-one-8b) first: on a CUDA-capable Linux
host, clone this repository and create the SGLang and adapter virtual environments with `uv`.
The commands below assume the working directory and installations from that guide. Run the engine
and adapter in separate terminals.

Engine (stock SGLang 0.5.20):

```bash
CUDA_VISIBLE_DEVICES=0 SGLANG_VLM_CACHE_SIZE_MB=0 .venv-sglang/bin/python -m sglang.launch_server \
  --model-path ./StandardOne-8B --served-model-name standard-one-8b \
  --host 127.0.0.1 --port 30000 --tp-size 1 --model-impl sglang --dtype bfloat16 \
  --context-length 8192 --max-running-requests 32 --mem-fraction-static 0.8 \
  --chunked-prefill-size -1 --disable-radix-cache --mm-preprocess-cache-size-mb 0 \
  --model-config-parser hf --load-format safetensors
```

Adapter (`jev-adapter`, ships as `server/` in this repository):

```bash
.venv-native/bin/jev-adapter --engine-url http://127.0.0.1:30000 --model standard-one-8b --alias jev-latest \
  --host 0.0.0.0 --port 30120 --max-concurrency 1 \
  --tokenizer-model mistralai/Ministral-3-8B-Instruct-2512-BF16 \
  --tokenizer-revision f6fae9795746f63c9be8344932f01275f3c63734 \
  --prompt-wording native --native-system-prompt none --default-temperature 0.85 \
  --temperature-by-type choice=0.85,noul=0.85,score=0.70
```

### Prompt wording

`jev-adapter` can phrase a request in two ways. Both were measured on the same served endpoint (no system prompt) and each has its
own fitted temperatures; the recommended default is `native` unless `served` scores at least 1.0 percentage point higher on
the suites below and an offline check agrees.

| `--prompt-wording` | What the prompt looks like | Temperatures (default; choice / noul / score) | Mean accuracy, 10 suites |
|---|---|---|---:|
| `native` (recommended default) | `State:` / `Question:` / `Options:` headers, options as `A. name: description` | 0.85; 0.85 / 0.85 / 0.70 | 76.6 % |
| `served` | `Context:` / `Question:` / `Options:` headers, options as `A: name: description` | 0.80; 0.80 / 0.90 / 0.95 | 76.4 % |

The 10 suites: judge proxy, hard proxy, stated-distribution probability, realistic transfer set, MuSiQue (multiple choice), SQuAD 2.0 unanswerable questions, ContractNLI, PAWS-X (English), a held-out hard decision set and a consistency set. None of them is a JevBench tier, and no JevBench item was used to choose the wording or the temperatures.
To use `served`, pass `--prompt-wording served --default-temperature 0.80 --temperature-by-type choice=0.80,noul=0.90,score=0.95`.

Try it:

```bash
curl -s http://127.0.0.1:30120/v1/systemone -X POST -H 'content-type: application/json' -d '{
  "model": "jev-latest",
  "state": "Policy: refunds require a receipt and purchase within 30 days. A customer bought 12 days ago but has no receipt. Issue a refund.",
  "questions": {
    "decision": {
      "type": "noul",
      "instructions": "Under the stated policy, is the requested action permitted? Treat unproved required conditions as not satisfied.",
      "criteria": {"true": "Every required condition is established and no prohibition applies.", "false": "A condition is missing or a prohibition applies."}
    }
  }
}'
```

Response shape (example values, default temperature applied):

```json
{
  "model": "standard-one-8b",
  "answers": {"decision": {"type": "noul", "noul": 0.08}},
  "usage": {"input_tokens": 96, "output_tokens": 0},
  "metadata": {
    "confidence_method": "1 - normalized_entropy",
    "temperature": 0.85,
    "temperature_by_type": {"choice": 0.85, "noul": 0.85, "score": 0.70},
    "evaluations": 1,
    "adapter_elapsed_ms": 26.1
  }
}
```

More (client command, 3B variant, request format): see [QUICKSTART.md](QUICKSTART.md).

## Benchmarks

**Served endpoint results (the release configuration).** Merged BF16 weights through SGLang 0.5.20
and `jev-adapter`, native wording, no system prompt, one option order, per-answer-type temperatures (choice 0.85, noul 0.85, score 0.70). The wording and the temperatures were chosen on non-JevBench data. Jev 1.13 was
measured on the same items through its hosted endpoint; its probabilities are raw, with no
temperature applied. These are our measurements, not official sealed-set JevBench scores.

| Suite | **Standard One 8B** | Jev 1.13 |
|---|---|---|
| JevBench public easy (48) | **100.00 %** | 100.00 % |
| JevBench public standard (72) | **93.06 %** | 98.61 % |
| JevBench public hard (111) | **54.95 %** | 72.07 % |
| judge proxy (600: routing + answer adequacy) | **89.33 %** | 90.50 % |
| realistic transfer set (600) | **90.83 %** | 86.67 % |
| stated-distribution probability (1,036) | **81.18 %** | 72.97 % |
| hard proxy (600) | **53.00 %** | 54.83 % |

**Offline comparison with the untuned base.** This separate `transformers` runner used native
wording, no system prompt, one option order, T=1. The base and tuned checkpoint were scored by the
same offline path; these numbers are indicative of the base-model change, not the served scores above.

| Suite | Untuned base | **Standard One 8B** |
|---|---|---|
| JevBench public easy (48) | 100.00 % | **97.92 %** |
| JevBench public standard (72) | 79.17 % | **97.22 %** |
| JevBench public hard (111) | 60.36 % | **55.86 %** |
| judge proxy (600: routing + answer adequacy) | 79.33 % | **88.33 %** |
| realistic transfer set (600) | 72.83 % | **90.00 %** |
| stated-distribution probability (1,036) | 34.85 % | **82.63 %** |

Against the untuned base, four suites improve, and public easy falls by 2.08 percentage points and public hard falls by 4.50 percentage points on this offline run. Served and offline probabilities differ even on identical
prompts, so use the served table for expected endpoint behavior. Hard-tier ECE at the served temperatures is
0.184 against Jev 1.13's 0.099 raw, and mean TV to the stated distributions is 0.108 at served T
against Jev's 0.192 raw; full calibration table: [`docs/BENCHMARKS.md`](docs/BENCHMARKS.md#calibration).

**Speed** — raw serial latency on one H200 with SGLang 0.5.20, using a 242-decision profile averaging
about 280 input tokens per decision. The 25.8 ms figure is p50 for this profile, not a latency
guarantee for other request lengths, concurrency or hardware. Qwen checkpoints are untuned and shown
for speed only; no accuracy comparison is implied.

| Model | p50 | p95 | Input tokens/decision |
|---|---|---|---|
| Standard One 3B | 22.6 ms | 33.2 ms | ≈280 |
| **Standard One 8B** | **25.8 ms** | **41.9 ms** | ≈280 |
| Qwen3-8B (untuned) | 28.5 ms | 57.2 ms | 278 |
| Qwen3.5-4B (untuned) | 48.8 ms | 72.7 ms | 283 |

Throughput on one H200 (hard+standard mix, 1,322 tokens/request): 29.3k tok/s at concurrency 1, rising to 39.5k tok/s at concurrency 64 (≈40 decisions/s at concurrency 8 on the 280-token profile above).

On the public classification and decision suites (400 cases/suite, seed 13, served endpoints): AG News 84.2 %, typed decisions 71.1 %, MASSIVE intent mean 86.1 %, email spam 91.8 %, phishing 85.2 %. Full table, per-language and per-workflow breakdown: [`docs/BENCHMARKS.md`](docs/BENCHMARKS.md#public-classification-and-decision-suites) and [`docs/public-classification-suites.md`](docs/public-classification-suites.md).

A JevBench v1.4.1 run has been requested; the sealed-set result is not yet available. Full report: [`docs/BENCHMARKS.md`](docs/BENCHMARKS.md).

## Model details

- **Base model:** `mistralai/Ministral-3-8B-Instruct-2512-BF16`, revision `f6fae9795746f63c9be8344932f01275f3c63734` (Apache-2.0).
- **Adapter:** LoRA r=16, α=32, dropout 0, on `q_proj k_proj v_proj o_proj gate_proj up_proj down_proj` of the language-model projections only (vision tower and multimodal projector excluded), **44,564,480** trainable parameters, PEFT 0.21.0. Adapter file `adapter_model.safetensors`, 214,559,872 bytes, sha256 `53e41238cd55567cfbc75efdf61d354da39771573f56f74bb1440c9ffdd1bd4a`.
- **Merged BF16 checkpoint:** merging the adapter into the base changed **238 tensors** (293 unchanged), none outside the language-model projections, max absolute weight change **0.00201**.
- **Serving details:** native chat-template wording, no system prompt, fixed per-answer-type temperatures (choice 0.85, noul 0.85, score 0.70; fitted on held-out and public-train calibration data, no JevBench item); served model name `standard-one-8b` behind stock SGLang 0.5.20 via `jev-adapter` (`POST /v1/systemone`); single caller-supplied option order, no rotation ensemble; 8,192-token context.

| Path | Contents |
|---|---|
| `*.safetensors` | Merged BF16 checkpoint (base + LoRA) |
| `config.json`, `tokenizer*`, `chat_template*`, `preprocessor*` | Base model's non-weight files |
| `server/` | `jev-adapter` source (`POST /v1/systemone`) |
| `docs/`, `QUICKSTART.md` | Benchmarks, figures, quick-start guide |
| `SHA256SUMS`, `release-manifest.json`, `MERGE_REPORT.json`, `evidence/`, `LICENSE`, `README.md` | File hashes, training manifest, merge report, supporting artifacts, licence, this card |

## Training data

Training data is synthetic and format-augmented decision data plus decision items converted from public
datasets (listed below); the JevBench public tiers used only for evaluation carry MIT. Full per-cohort breakdown (row counts, what each covers, licence): [`docs/BENCHMARKS.md`](docs/BENCHMARKS.md#training-data-provenance).

Public datasets used (train splits where the dataset has one; licence as stated by each dataset; labels come from the
datasets, distractor options are generated by code):

| Dataset | Licence |
|---|---|
| SQuAD 2.0 | CC BY-SA 4.0 |
| ARC | CC BY-SA 4.0 |
| BoolQ | CC BY-SA 3.0 |
| CommonsenseQA | MIT |
| HellaSwag | MIT |
| Banking77 | CC BY 4.0 |
| Bias in Bios | MIT |
| Bitext customer support | CDLA-Sharing-1.0 |
| CLINC150 | CC BY 3.0 |
| Amazon Counterfactual | CC BY 4.0 |
| DBpedia-14 | CC BY-SA 3.0 |
| Dolly 15k | CC BY-SA 3.0 |
| GoEmotions | Apache-2.0 |
| MASSIVE | CC BY 4.0 |
| Twitter Financial News Sentiment | MIT |
| HelpSteer3 | CC BY 4.0 |
| HelpSteer2 | CC BY 4.0 |
| 2WikiMultihopQA | Apache-2.0 |
| HotpotQA | CC BY-SA 4.0 |
| MuSiQue | CC BY 4.0 |
| QASC | CC BY 4.0 |
| DROP | CC BY-SA 4.0 |
| GSM8K | MIT |
| TempReason | CC BY-SA 3.0 |
| MultiNLI | OANC / CC BY-SA 3.0 / CC BY 3.0 |
| PAWS | Google terms, free for any purpose |
| PAWS-X | Google terms, free for any purpose |
| SNLI | CC BY-SA 4.0 |
| WANLI | CC BY 4.0 |
| ContractNLI | CC BY 4.0 |
| CUAD | CC BY 4.0 |
| ShARC | CC BY-SA 3.0 |
| Jailbreak classification | Apache-2.0 |
| Prompt injections | Apache-2.0 |
| Aegis AI Content Safety 2.0 | CC BY 4.0 |
| Jigsaw Toxic Comment Classification (mirror of the Kaggle data) | CC0 (data); comment text CC BY-SA 3.0 (Wikipedia) |
| Measuring Hate Speech | CC BY 4.0 |
| Image safety classes | MIT |

Upstream ids and the cohort each one feeds: [`docs/BENCHMARKS.md`](docs/BENCHMARKS.md#training-data-provenance).

An exact-text overlap audit against the public JevBench tiers found 0 exact scenario matches and 181 exact instruction matches — rows in two adequacy-rubric cohorts whose entire instruction field, a generic 58-character adequacy question, is byte-identical to one public hard-tier instruction (0.03 % of the 520,754-row training mixture). These rows are kept and disclosed here rather than regenerated, since the overlap is limited to one rubric question's wording and never touches a scenario or an answer.

## Limitations

- **Public hard tier:** the served 8B score is **54.95 %**, versus **72.07 %** for Jev 1.13. In the
  separate offline base comparison, Standard One 8B scores **55.86 %**, below the untuned base's
  **60.36 %**.
- Served probabilities are temperature-scaled by one value per answer type; if you apply this model to a
  materially different question distribution, re-fitting that temperature is advisable rather than
  assuming these values transfer.
- At most 26 options per question (one uppercase letter per option, `A`–`Z`).
- The sealed JevBench set has not been measured for this model.
- Served and offline probabilities can differ on identical prompts (mean total-variation ≈0.06 on the
  hard tier); served numbers are treated as authoritative.
- Korean is a small share of multilingual training relative to the other seven languages.
- The card reports text benchmarks; it does not establish decision accuracy on image inputs.
- Ten-way support triage (36 %) and RAG passage relevance (59 %) are weak zero-shot; fine-tune
  for those.

## Licence

Adapter weights, merged weights, server code (`server/`) and this card: Apache-2.0. Base model `mistralai/Ministral-3-8B-Instruct-2512` (and `-BF16`): Apache-2.0 per its Hugging Face model card, which adds that the model must not be used in a way that infringes, misappropriates, or otherwise violates any third party's rights. `jev-adapter` and SGLang: Apache-2.0. The JevBench harness and public tiers used for evaluation: MIT; other benchmark items keep their own upstream terms.

## Citation

`StandardThinking/StandardOne-8B` (merged weights + server code) · `StandardThinking/StandardOne-8B-LoRA` (adapter + merge recipe).
