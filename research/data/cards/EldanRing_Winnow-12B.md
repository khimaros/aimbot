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
  - decision-model
---

# Winnow-12B

Winnow-12B is an EldanRing fine-tune of [Gemma 4 12B IT](https://huggingface.co/google/gemma-4-12B-it) for local typed decisions, chat, and image input. Give it a shared state and questions with known answer options; the [Winnow server](https://github.com/EldanRing/winnow-inference) scores those options through `/v1/systemone` without generating an explanation. Ordinary chat uses `/v1/chat/completions` from the same loaded model.

The GGUF downloads contain the merged fine-tune. No separate adapter or base-model download is needed.

[Quickstart](https://github.com/EldanRing/winnow-inference/blob/main/docs/QUICKSTART.md) · [API reference](https://github.com/EldanRing/winnow-inference/blob/main/docs/API.md) · [Benchmarks](docs/BENCHMARKS.md)

## Decision quality

| Model | JevBench public subset, 231 items | Kev-v9 clean, 1,046 items |
|---|---:|---:|
| **Winnow-12B BF16** | **85.28%** | **81.45%** |
| **Winnow-12B Q8** | **85.71%** | **81.55%** |
| Jev 1.13, hosted via OpenRouter | 85.71% | 87.00% |

Winnow Q8 and Jev each answered **198 of 231** JevBench questions correctly on these frozen inputs. JevBench reports public-subset accuracy rather than the composite leaderboard score. These panels were used during development. The BF16 results use an earlier GGUF export; see [export provenance](release-manifest.json) and the [evaluation report](docs/BENCHMARKS.md).

![Winnow BF16 and Q8 versus Jev, Kev and Laya on the frozen public decision benchmarks](docs/assets/02-decision-quality.png)

## Downloads

Choose one target model. Add the matching projector for image input.

| File | Use | Size |
|---|---|---:|
| [Winnow-12B-Q8_0.gguf](https://huggingface.co/EldanRing/Winnow-12B/resolve/main/gguf/Winnow-12B-Q8_0.gguf?download=true) | Q8_0; tested with 64K context and vision | 12.67 GB / 11.80 GiB |
| [Winnow-12B-BF16.gguf](https://huggingface.co/EldanRing/Winnow-12B/resolve/main/gguf/Winnow-12B-BF16.gguf?download=true) | BF16; larger-memory systems or CPU/GPU offload | 23.83 GB / 22.20 GiB |
| [Winnow-12B-NVFP4.gguf](https://huggingface.co/EldanRing/Winnow-12B/resolve/main/gguf/Winnow-12B-NVFP4.gguf?download=true) | Smaller Linux/CUDA 8K text and vision presets | 8.16 GB / 7.60 GiB |
| [mmproj-Winnow-12B.gguf](https://huggingface.co/EldanRing/Winnow-12B/resolve/main/gguf/mmproj-Winnow-12B.gguf?download=true) | F16 vision projector for any of the three targets | 175 MB / 0.163 GiB |

Use the exact target filename or a [Winnow preset](docs/RUNTIME-PROFILES.md). [Checksums](https://huggingface.co/EldanRing/Winnow-12B/blob/main/SHA256SUMS) identify every file.

## Running the model

The [quickstart](https://github.com/EldanRing/winnow-inference/blob/main/docs/QUICKSTART.md) covers installation, downloads, and launch commands. Direct decisions support `noul` (yes/no), `choice` (named options), and `score` (ordered levels). Multiple questions share a state prefill and can reuse a cached prefix.

**F16 is the default and recommended target K/V cache.** Cache precision is separate from the GGUF weight format; use `--cache q8_0` for an explicit Q8 override. The pinned MTP assistant uses the target's shared K/V cache.

### Q8 context and vision

The measured RTX 5070 Ti 16 GB profile used Q8 weights, Q8 KV, full GPU offload, the matching projector, and exclusive memory scheduling.

| Measurement | Result |
|---|---:|
| Configured context capacity | 65,536 positions |
| Verified shared prefix with an image | 65,022 positions, including 1,024 image positions |
| Observed peak device VRAM | 15.01 GiB |
| Four questions at near-full context, cold | 25.00 s |
| Same request, cached median of three repeats | 143.0 ms |
| Short-prompt generation, median of three 512-token runs | 55.5 tokens/s |

Context includes formatting, images, questions, and output. Chat and decisions take turns using their K/V contexts in this profile; switching can evict the cached prefix. See [full timing definitions](docs/BENCHMARKS.md) for the separate capacity and generation measurements. BF16 weights alone exceed 16 GB VRAM.

### NVFP4 tradeoffs

On a matched direct-text workload, Q8 versus NVFP4 used **13,529 versus 9,229 MiB** peak device memory and served **3.43 versus 4.98 decisions/s**. The RTX 5070 Ti test used four concurrent requests, 4K decision/16K chat context, Q8 KV, and no vision or MTP. Startup was excluded; this is native decision throughput, not generation speed or sustained service capacity.

| Historical matched direct panel | Q8 GGUF | NVFP4 GGUF |
|---|---:|---:|
| Jev public, 231 decisions | 198/231 (85.71%) | 193/231 (83.55%) |
| Kev-clean, 1,046 decisions | 852/1,046 (81.45%) | 814/1,046 (77.82%) |
| Typed teacher agreement, 2,000 decisions / 400 groups | 1,398/2,000 (69.90%) | 1,412/2,000 (70.60%) |

NVFP4 reduced memory use and improved measured throughput while losing verified-label accuracy on Jev and Kev. Typed measures synthetic teacher agreement. This historical native-T1 comparison used previously observed panels; its Q8 Kev count differs from the separate release campaign above. GGUF results do not transfer to HF/vLLM NVFP4 backends.

### Adaptive reasoning and MTP

Direct decisions are the default. Adaptive reasoning generates context before scoring a question again. In the Q8 confirmation, source-equal accuracy/consensus agreement changed **62.50% → 64.06%**, with a paired 95% change interval of **−2.34 to +5.47 pp**. NLL worsened, and mean CLI latency rose from **198 to 743 ms**.

MTP separately drafts ordinary chat tokens using the matching [12B assistant](https://huggingface.co/EldanRing/Winnow-12B/resolve/main/gguf/Gemma-4-12B-IT-Assistant-BF16.gguf?download=true). Direct serving needs only the target. Linux/CUDA presets cover Q8 text and NVFP4 vision with MTP at 8K; the Q8 direct 64K vision profile runs without MTP.

See [reasoning evaluations](docs/REASONING.md), [runtime profiles](docs/RUNTIME-PROFILES.md), and [assistant attribution](docs/assistants/README.md) for settings and commands.

## Training and limitations

Winnow is a rank-32, alpha-64 LoRA fine-tune with zero dropout, merged into the base model before GGUF export. It adapts the attention and MLP projections. The base revision is `707f0a3b8a3c7ad586ed01e27eafbad8a27dd0f7`.

The private training data combines synthetic scenarios, teacher-supervised examples, and labeled semantic tasks, including routing, rule application, evidence selection, ordinal judgments, entailment, and answerability. Training and validation were split. The training data and pipeline are private.

Candidate probabilities are normalized over the supplied options. Confidence describes concentration among those options, not a guarantee of correctness. The reported default decision temperature is 1.0.

## Credits and license

Winnow-12B is an independent fine-tune by EldanRing of Google DeepMind's [Gemma 4 12B IT](https://huggingface.co/google/gemma-4-12B-it), released under [Apache 2.0](https://ai.google.dev/gemma/docs/gemma_4_license). See [LICENSE](https://huggingface.co/EldanRing/Winnow-12B/blob/main/LICENSE) and [NOTICE](https://huggingface.co/EldanRing/Winnow-12B/blob/main/NOTICE).

The separate inference code builds on [llama.cpp](https://github.com/ggml-org/llama.cpp) by Georgi Gerganov and contributors and preserves its MIT license. Jev-style refers to the typed-decision interface; Winnow is not affiliated with or endorsed by TypeSafe, Google, or llama.cpp.
