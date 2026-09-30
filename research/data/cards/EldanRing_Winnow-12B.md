---
base_model: google/gemma-4-12B-it
base_model_relation: finetune
license: apache-2.0
library_name: gguf
pipeline_tag: image-text-to-text
tags:
  - winnow
  - gemma4
  - typed-decisions
  - local-inference
  - vision
  - gguf
---

# Winnow-12B — GGUF

**Local Jev-style decisions, chat, and vision. Q8 tested with 64K context and vision on a 16 GB RTX 5070 Ti.**

Winnow-12B fine-tunes [Gemma 4 12B IT](https://huggingface.co/google/gemma-4-12B-it)
for typed decisions. Its [llama.cpp-based inference server](https://github.com/EldanRing/winnow-inference)
provides `/v1/systemone` and ordinary `/v1/chat/completions` from the same loaded model.

- **Typed decisions:** ask `noul`, `choice`, and `score` questions against shared state.
- **Shared computation:** prefill the state once, fork question branches, and read answer-token logits without generating answer text.
- **Chat and vision:** regular chat, streaming, and image inputs through the same server.
- **Two GGUF model downloads:** BF16 (16-bit floating point) and Q8_0 (8-bit quantized), both ready for llama.cpp. Neither needs conversion or a separate LoRA adapter.

[Inference code](https://github.com/EldanRing/winnow-inference) ·
[Quickstart](docs/QUICKSTART.md) ·
[Full benchmark report](docs/BENCHMARKS.md) ·
[Artifact manifest](release-manifest.json)

## GGUF downloads

**Choose one model file.** Both versions run directly in the
[Winnow llama.cpp-based server](https://github.com/EldanRing/winnow-inference).
The optional vision projector is listed separately below.

| Download | Precision and use | File size |
|---|---|---:|
| [Winnow-12B-Q8_0.gguf](https://huggingface.co/EldanRing/Winnow-12B/resolve/main/gguf/Winnow-12B-Q8_0.gguf?download=true) | **Q8_0, 8-bit quantized. Recommended for the tested 16 GB RTX 5070 Ti setup.** | 12.67 GB / 11.80 GiB |
| [Winnow-12B-BF16.gguf](https://huggingface.co/EldanRing/Winnow-12B/resolve/main/gguf/Winnow-12B-BF16.gguf?download=true) | **BF16, 16-bit floating point.** Larger-memory systems or CPU/GPU offload. | 23.83 GB / 22.20 GiB |

BF16 weights alone exceed 16 GB VRAM; the 5070 Ti full-offload measurements below
apply to **Q8_0**. Text-only use needs just the chosen model GGUF. Vision needs
that model plus `mmproj-Winnow-12B.gguf`.

### Optional vision projector

[**Download mmproj-Winnow-12B.gguf**](https://huggingface.co/EldanRing/Winnow-12B/resolve/main/gguf/mmproj-Winnow-12B.gguf?download=true) — **175 MB / 0.163 GiB**.

This is the **F16 vision projector**, not another model or quantization choice.
Use it alongside either **BF16** or **Q8_0** for image inputs; skip it for text-only
use. The same projector works with both model downloads above.

This repository distributes **GGUF model weights only**. No safetensors shards
or conversion step are required. See [Quickstart](docs/QUICKSTART.md) for exact
download and launch commands, and [SHA256SUMS](SHA256SUMS) for file checksums.

## Decision quality

![Winnow BF16 and Q8 versus Jev, Kev and Laya on the frozen public decision benchmarks](docs/assets/02-decision-quality.png)

Both Winnow variants below were evaluated in the same RTX PRO 5000 Blackwell
campaign. Jev was evaluated through OpenRouter on the same frozen inputs and
scoring rules. Both BF16 and Q8 were served as GGUF models. The released
GGUF files are listed above; evaluation hashes are in the benchmark report.

| Model | JevBench public subset, 231 items | Kev-v9 clean, 1,046 items |
|---|---:|---:|
| **Winnow-12B BF16** | **85.28%** | **81.45%** |
| **Winnow-12B Q8** | **85.71%** | **81.55%** |
| Jev 1.13, hosted via OpenRouter | 85.71% | 87.00% |

**Winnow Q8 matches Jev on this JevBench public subset: 198 of 231 correct.**
This is a result on that subset, not a claim of universal parity.
JevBench here means **public-subset accuracy**, not the official composite
leaderboard score. The [complete report](docs/BENCHMARKS.md) includes competitor
comparisons, all measured suites, calibration, hardware and evaluation scope.

## RTX 5070 Ti: 64K context with vision

![Winnow Q8 64K context and vision measurements on the RTX 5070 Ti](docs/assets/01-5070ti-capability.png)

The released Q8 model and matching projector were tested with full GPU offload,
Q8 KV cache, four decision branches, one chat slot, and exclusive memory scheduling.

| Measurement | Result |
|---|---:|
| Configured context capacity | 65,536 positions |
| Verified shared prefix with an image | 65,022 positions, including 1,024 image positions |
| Peak device VRAM during the 64K smoke | 15.01 GiB, including the desktop |
| Peak process-tree system RAM during loading and smoke | 12.25 GiB PSS |
| Four questions at near-full context, cold | 25.00 s |
| Same four-question request, cached median of three repeats | 143.0 ms |
| Short-prompt generation, median of three 512-token runs | 55.5 tokens/s |
| Long vision prompt prefill, 62,435 positions | 2,893.9 tokens/s |
| Generation following that long prompt, 512 tokens | 46.9 tokens/s |
| Time to first token on that cold long prompt | 21.75 s |

These are separate capacity and timing probes, not a single simultaneous workload.
The host had 96 GB system RAM; the observed PSS is not a minimum installed-RAM
recommendation. Full hardware, repetition counts, and timing definitions are in
the [report](docs/BENCHMARKS.md).

64K includes prompt formatting, image positions, questions, and generated output.
In the tested exclusive profile, chat and decision requests share the weights
but take turns using their KV contexts; switching can evict a cached prefix.

## GGUF packaging

Each model GGUF contains its language weights, tokenizer, and chat template.
BF16 and Q8_0 are exports of the same merged fine-tune; they are alternative
model files, not parts to combine. The F16 projector supplies vision support.
The remaining root configuration/tokenizer files are reference assets; llama.cpp
loads the GGUF directly. No separate LoRA adapter is needed.

## Training

Winnow is a **LoRA fine-tune**, released after merging the learned update into
the base model. It is not a full-parameter training run.

| Setting | Value |
|---|---|
| Base | `google/gemma-4-12B-it` |
| Base revision | `707f0a3b8a3c7ad586ed01e27eafbad8a27dd0f7` |
| LoRA rank / alpha | 32 / 64 |
| LoRA dropout | 0 |
| Adapted projections | `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj` |
| Export | Adapter merged into BF16 weights, then exported as BF16 GGUF and Q8_0 GGUF |

**The training dataset is private and is not released.** It contains curated
typed-decision examples: synthetic scenarios, teacher-supervised examples, and
labeled semantic tasks. Task coverage includes routing, policy and rule application, evidence
selection, workflow decisions, ordinal judgments, entailment, paraphrase, and
answerability. Contrastive examples vary
facts that should change an answer. An initial decision fine-tune was followed by a 26,000-example refinement
mixture that included replay of earlier examples. This release was selected
after 19,200 refinement examples had been processed; these are training
presentations, not a claim of that many unique new examples. Refinement used
BF16 LoRA, an effective batch size of 8, and an 8,192-token training cap. The
objective combined gold-label cross-entropy with teacher-distribution
cross-entropy only when the teacher agreed with the gold label.

Training and validation were split; the public benchmark report documents the separate evaluation scope and any known
development exposure. No claim is made about excluding public benchmarks from
the base model's pretraining data.

## Probabilities and scope

The decision server normalizes logits over the supplied answer options. Its
entropy-based confidence summarizes concentration within that distribution;
it is not a guaranteed probability of correctness. Reported default decision
temperature is 1.0, without a separately fitted calibration map.

Chat and image input are functional in the release runtime. A complete paired
general-chat quality comparison against the unfine-tuned base was not completed;
this release does not claim identical chat quality. Near-full-context retrieval
checks establish capacity and operation, not general 64K reasoning quality.
Audio/video capability is not evaluated by this release.

## Credits and license

Winnow-12B is an independent fine-tune by EldanRing of Google DeepMind's
[Gemma 4 12B IT](https://huggingface.co/google/gemma-4-12B-it), released under
[Apache 2.0](https://ai.google.dev/gemma/docs/gemma_4_license).
See [LICENSE](LICENSE) and [NOTICE](NOTICE).

The separate inference repository builds on
[llama.cpp](https://github.com/ggml-org/llama.cpp) by Georgi Gerganov and contributors
and preserves its MIT license. Jev-style refers to the typed-decision interface;
Winnow is not affiliated with or endorsed by TypeSafe, Google, or llama.cpp.
