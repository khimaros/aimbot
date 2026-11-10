---
license: apache-2.0
base_model: Cloudflare/clef-omni
base_model_relation: quantized
library_name: gguf
quantized_by: PollardWeights
pipeline_tag: text-classification
language:
- en
tags:
- pollard-weights
- pollard
- gguf
- llama.cpp
- imatrix
- qwen3_omni_moe
- quantized
- mixed-precision
- measured-allocation
- decision-model
- systemone
- structured-output
---

# clef-omni -- Pollard

> ### Pollard shrank this model: **70.52 GB (f16) -> 11.15 GB** -- **84% smaller, 6.3x down**.
> The smallest rung here; larger, higher-fidelity rungs are listed below.
>
> | format | this model's size |
> |---|---:|
> | f16 | 70.52 GB |
> | Q8_0 | ~37.38 GB |
> | Q6_K | 25.18 GB |
> | Q4_K_M | ~20.45 GB |
> | **PollardMix (this repo's IQ2_XXS)** | **11.15 GB** |

Pollard builds of [Cloudflare/clef-omni](https://huggingface.co/Cloudflare/clef-omni) made with [Pollard Weights](https://github.com/WestWaters/pollard-weights) -- a ladder of **measured-allocation** quants (bits placed by per-layer sensitivity, not a uniform crush).

**Needs llama.cpp with Pollard's `clef-omni` patch ([runtime-patches/llama.cpp-clef-omni.patch](https://github.com/WestWaters/pollard-weights/blob/main/runtime-patches/llama.cpp-clef-omni.patch); upstream PR pending).** This model's architecture (`clef-omni`) is implemented by a runtime patch Pollard ships and is not in upstream llama.cpp yet, so stock llama.cpp -- and therefore Ollama and LM Studio -- cannot load these files until it lands. Every rung here was built and verified with that runtime (see How to run).

## Model details

| | |
|---|---|
| Parameter count | ~35.3B |
| Architecture | `qwen3_omni_moe` |
| Input support | text   (the source also does audio -- build the projector with --mmproj to ship it) |
| imatrix | **yes** -- see [calibration](#imatrix-calibration) |
| Measured | **decision fidelity vs f16** through `/v1/systemone` -- [table below](#decision-fidelity) (perplexity does not apply: a decision model answers with probabilities, not text) |

## Which file should I choose?

Every rung is the **same weights**, sized to a different RAM budget by the measured allocation. Pick the largest one that fits your machine with room for context:

- **~27.2 GB RAM / VRAM** -> **`Q6_K`** (25.18 GB). *(needs llama.cpp + Pollard patch)*
- **~21.0 GB RAM / VRAM** -> **`IQ4_XS`** (19.01 GB). *(needs llama.cpp + Pollard patch)*
- **~16.8 GB RAM / VRAM** -> **`IQ3_S`** (14.84 GB). *(needs llama.cpp + Pollard patch)*
- **~13.2 GB RAM / VRAM** -> **`IQ2_XXS`** (11.15 GB). *(needs llama.cpp + Pollard patch)*

## Available files

| file | size | agrees with f16 | option KL | verified | notes |
|---|---:|---:|---:|---|---|
| `clef-omni-Pollard-IQ2_XXS.gguf` | 11.15 GB | 100% | 0.011 | yes |  |
| `clef-omni-Pollard-IQ3_S.gguf` | 14.84 GB | 100% | 0.0031 | yes |  |
| `clef-omni-Pollard-IQ4_XS.gguf` | 19.01 GB | 100% | 0.0013 | yes |  |
| `clef-omni-Pollard-Q6_K.gguf` | 25.18 GB | 100% | 0.00013 | yes |  |

_Verified = the rung passed `pollard-verify --gate`: its KLD / top-1 against the source and every other threshold in the gate file (retention, tool calls, runtime, coherence) were measured and met. A rung that failed is not published._

## Decision fidelity

This is a **decision model**: it answers typed questions (choice / score / yes-no) with a probability per option, so it is measured on its decisions, not on text. Each rung and the f16 answered the same 20 typed questions through llama-server's `/v1/systemone`, read the same way ([pollard-decision](https://github.com/WestWaters/pollard-weights)).

| file | size | agrees with f16 | option KL vs f16 | mean prob. drift | accuracy | ECE | flips vs f16 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `clef-omni-Pollard-Q6_K.gguf` | 25.18 GB | 100% | 0.00013 | 0.0013 | 100% | 0.0437 | 0 |
| `clef-omni-Pollard-IQ4_XS.gguf` | 19.01 GB | 100% | 0.0013 | 0.0039 | 100% | 0.0450 | 0 |
| `clef-omni-Pollard-IQ3_S.gguf` | 14.84 GB | 100% | 0.0031 | 0.0066 | 100% | 0.0502 | 0 |
| `clef-omni-Pollard-IQ2_XXS.gguf` | 11.15 GB | 100% | 0.011 | 0.0148 | 100% | 0.0679 | 0 |

_Agrees = the rung picks the same option as the f16. Option KL = how far its option probabilities moved from the f16's (0 = identical); it is the number that separates the rungs._ _ECE = expected calibration error against the gold labels (10 bins, top label; lower = its confidence means what it says)._ _Flips = decisions whose answer differs from the f16's._

_Mean KLD / PPL: not applicable: decision-only model (`clef-omni` ends in a decision head (no per-token logits)). Each rung's publish gate is this board: agreement and option KL vs the f16._

## Retention vs f16

What each rung keeps of the f16 on real work -- quantized score / f16 score on the same tasks, the same settings, the same harness (100% = no loss). Measured against our own f16, so the rungs compare directly; it is not comparable to a retention figure published on a different suite.

| file | Decisions (agree) |
|---|---:|
| `clef-omni-Pollard-Q6_K.gguf` | 100% |
| `clef-omni-Pollard-IQ4_XS.gguf` | 100% |
| `clef-omni-Pollard-IQ3_S.gguf` | 100% |
| `clef-omni-Pollard-IQ2_XXS.gguf` | 100% |

## Download a specific file

```bash
pip install -U "huggingface_hub[cli]"
hf download PollardWeights/clef-omni-Pollard \
  --include "clef-omni-Pollard-IQ2_XXS.gguf" --local-dir ./
```

## How to run

**Needs llama.cpp with Pollard's `clef-omni` patch ([runtime-patches/llama.cpp-clef-omni.patch](https://github.com/WestWaters/pollard-weights/blob/main/runtime-patches/llama.cpp-clef-omni.patch); upstream PR pending).** Build it, then serve any file here:

```bash
# with Pollard installed: builds runtime/llama.cpp with every patch it ships
pollard-runtime --update
runtime/llama.cpp/build/bin/llama-server -m <file>.gguf -ngl 99

# or by hand: the pinned upstream base + the patch
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
git checkout b76b133
git apply ../pollard-weights/runtime-patches/llama.cpp-clef-omni.patch
git apply ../pollard-weights/runtime-patches/llama.cpp-quantize-dec-blk.patch
cmake -B build && cmake --build build -j --target llama-server
build/bin/llama-server -m <file>.gguf -ngl 99
```

A decision model is served on **`/v1/systemone`** (no chat or completions):

```bash
llama-server -m clef-omni-Pollard-IQ2_XXS.gguf -ngl 99 --port 8080
curl http://127.0.0.1:8080/v1/systemone -H "Content-Type: application/json" -d '{
  "state": "Customer message: I was charged twice for my order last week and nobody has replied.",
  "questions": {
    "route":   {"type": "choice", "instructions": "Which team should handle this?",
                "criteria": {"billing": null, "shipping": null, "technical": null}},
    "angry":   {"type": "noul",   "instructions": "Is the customer angry?"},
    "urgency": {"type": "score",  "instructions": "How urgent is this?",
                "criteria": ["can wait", "this week", "today", "right now"]}
  }
}'
```

Each answer carries the probability of every option. Some decision models evaluate the whole prompt in one batch, so a long `state` may need a larger `--ubatch-size`.

## Use it in your harness

A decision model has no chat endpoint, so chat harnesses (Claude Code, Codex, OpenCode, ...) cannot drive it. It serves **`/v1/systemone`**, which is what [Oh My Pi](https://github.com/can1357/oh-my-pi)'s `api: typesafe` provider calls (`{baseUrl}/v1/systemone`) for its **`judge`** role:

```yaml
# ~/.omp/agent/models.yml
providers:
  pollard-judge:
    baseUrl: http://127.0.0.1:8080
    api: typesafe
    auth: none
    models:
      - id: clef-omni-Pollard-IQ2_XXS
        name: clef-omni-Pollard-IQ2_XXS (Pollard, /v1/systemone)

# ~/.omp/agent/config.yml
modelRoles:
  judge: pollard-judge/clef-omni-Pollard-IQ2_XXS
```

```bash
pollard serve PollardWeights/clef-omni-Pollard:IQ2_XXS --harness omp
```

## imatrix (calibration)

The importance matrix (`clef-omni.imatrix`, included) was computed on the pollard-calib 'auto' profile (sources, revisions and licences in the shipped .sources.json).

The exact corpus is included as `release-calib.txt`, so the allocation can be reproduced rather than taken on trust.

## ARM / AVX

llama.cpp repacks weights into an interleaved layout at load time for faster inference on ARM and AVX machines -- no special file needed, online repacking covers these quants. The old `Q4_0_4_4/4_8/8_8` variants are not required.

## Errata

- `general.architecture` is `clef-omni`, which upstream llama.cpp does not implement yet. Needs llama.cpp with Pollard's `clef-omni` patch ([runtime-patches/llama.cpp-clef-omni.patch](https://github.com/WestWaters/pollard-weights/blob/main/runtime-patches/llama.cpp-clef-omni.patch); upstream PR pending) -- the quant types are ordinary and irrelevant to that. Checked with `pollard-ggufcheck`, which reads the architecture out of the header and the patches Pollard ships out of `runtime-patches/`.
- Measured allocation places bits by per-layer sensitivity under a size budget.
- Single machine; replication invited.

## Credits & license

- Base model: [`Cloudflare/clef-omni`](https://huggingface.co/Cloudflare/clef-omni) (Cloudflare)
- Quantization tooling: [llama.cpp](https://github.com/ggml-org/llama.cpp) (ggml-org)
- Method + tooling: [Pollard Weights](https://github.com/WestWaters/pollard-weights) -- *measure first, no claim before a number.*
- License: `apache-2.0`, inherited from the base model.

*Built with [Pollard Weights](https://github.com/WestWaters/pollard-weights) -- frontier models, small hardware, no compromise.*
