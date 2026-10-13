---
license: apache-2.0
base_model: nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2
pipeline_tag: image-text-to-text
language:
- en
- zh
tags:
- qwen3.8
- efficient-thinking
- reasoning
- coding
- uncensored
- sft
- simpo
- rloo
- gguf
- q6_k
- imatrix
- quantization
- llama.cpp
- ninfer
- mtp
- speculative-decoding
- multimodal
- vision
---

![vs. the original](assets/coder390-vs-original-en.png)

![GGUF tiers: scores, size and speed](assets/header-gguf-tier-table-en.png)

<!-- CARD_EN_START -->
# Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-GGUF-NInfer

A model post-trained with several rounds of SFT and RLOO on top of [Qwen3.8-27B-EfficientThink-SFT-SimPO-DFlash2](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2), which is itself the official [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) post-trained with SFT and SimPO. It is built to fix the original model's habit of failing to stop: it already has an answer, yet keeps re-deriving until it hits the 94K cap with no final answer. This repository is the standalone **GGUF** repository with eight GGUF packages under `GGUF/`: **Q2 / Q3 / Q4 LynnStyle** (built-in **Q4_0** MTP head), the same three as **-Q8MTP** versions (built-in **Q8_0** MTP head), **Q6_K**, and **Q8_0** (each with a built-in MTP head), plus the matching NInfer packages under `GGUF-NInfer/` (vision built in). The raw BF16 vision-tower file (`GGUF-NInfer/vision-bf16.safetensors`) is included for your own packaging/conversion; V3 `.ninfer` packages already have vision built in and do not need it at runtime. For llama.cpp multimodal, use `--mmproj GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` (Q8_0 mmproj in `GGUF/` only; not required inside NInfer packages). The BF16, static FP8, NVFP4, NInfer W4A4, INT8 W8A8, INT4 W4A16, and other tiers are in the main repository [Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2).

- **Baseline**: the original Qwen3.8 27B (FP8) scores GPQA 177/198, MMLU 444/500, LCB 83/100; its GPQA reasoning length (P50 / P70 / P90 tokens) is 5,299 / 12,607 / 50,577.
- **GGUF Q2 LynnStyle · scores**: GPQA 177/198, MMLU 433/500, LCB 90/100 (llama.cpp, C4, 100K full sets; scored before the built-in MTP head was attached (external Q8 MTP draft); same quantized weights).
- **GGUF Q2 LynnStyle · reasoning length (P50 / P70 / P90 tokens)**: GPQA 2,989.5 / 8,923.8 / 27,156.1; MMLU 181 / 326.3 / 1,020.5; LCB 5,656.5 / 17,835.8 / 40,067.3.
- **GGUF Q2 LynnStyle · speed**: NInfer with built-in Q4 MTP, C8 aggregate 521.0 tok/s (512-token cap, short run); llama.cpp with built-in Q4 MTP, C4 aggregate 174.8 tok/s (4096-token cap, long run). Protocols differ; do not compare directly.
- **GGUF Q2 LynnStyle · size**: GGUF 13,276,009,792 bytes (BPW 3.89), NInfer 13,568,617,472 bytes with vision (text + MTP BPW 3.89).
- **GGUF Q3 LynnStyle · scores**: GPQA 173/198, MMLU 449/500, LCB 92/100 (llama.cpp, C4, 100K full sets; scored before the built-in MTP head was attached (external Q8 MTP draft); same quantized weights).
- **GGUF Q3 LynnStyle · reasoning length (P50 / P70 / P90 tokens)**: GPQA 3,125.5 / 7,265.2 / 24,343.1; MMLU 148 / 279.3 / 923.4; LCB 4,421 / 14,232.2 / 34,946.
- **GGUF Q3 LynnStyle · speed**: NInfer with built-in Q4 MTP, C8 aggregate 512.3 tok/s (512-token cap, short run); llama.cpp with built-in Q4 MTP, C4 aggregate 191.8 tok/s (4096-token cap, long run). Protocols differ; do not compare directly.
- **GGUF Q3 LynnStyle · size**: GGUF 17,303,770,432 bytes (BPW 5.07), NInfer 17,596,369,920 bytes with vision (text + MTP BPW 5.07).
- **GGUF Q4 LynnStyle · scores**: GPQA 175/198, MMLU 448/500, LCB 89/100 (llama.cpp, C4, 100K full sets; scored before the built-in MTP head was attached (external Q8 MTP draft); same quantized weights).
- **GGUF Q4 LynnStyle · reasoning length (P50 / P70 / P90 tokens)**: GPQA 2,951.0 / 8,159.3 / 25,649.0; MMLU 164 / 312.9 / 1,077.7; LCB 3,669.5 / 14,810.5 / 38,182.1.
- **GGUF Q4 LynnStyle · speed**: NInfer with built-in Q4 MTP, C8 aggregate 436.4 tok/s (512-token cap, short run); llama.cpp with built-in Q4 MTP, C4 aggregate 81.1 tok/s (4096-token cap, long run). Protocols differ; do not compare directly.
- **GGUF Q4 LynnStyle · size**: GGUF 19,620,406,592 bytes (BPW 5.75), NInfer 19,913,006,080 bytes with vision (text + MTP BPW 5.74).
- **GGUF Q6_K · scores**: GPQA 174/198, MMLU 448/500, LCB 91/100 (llama.cpp, C4, 100K full sets).
- **GGUF Q6_K · reasoning length (P50 / P70 / P90 tokens)**: GPQA 3,683 / 9,814 / 27,966.
- **GGUF Q6_K · speed**: NInfer with MTP, C4 aggregate 235.5 tok/s; llama.cpp with MTP, C8 aggregate 189.0 tok/s (both 512-token-cap quick runs).
- **GGUF Q6_K · size**: GGUF 23,177,516,384 bytes (BPW 6.79), NInfer 23,379,962,880 bytes with vision (text + MTP BPW 6.76).
- **GGUF Q8_0 · scores**: GPQA 171/198, MMLU 443/500, LCB 90/100 (llama.cpp, C4, 100K full sets).
- **GGUF Q8_0 · reasoning length (P50 / P70 / P90 tokens)**: GPQA 3,102.5 / 7,971 / 28,891.6; MMLU 164 / 291 / 741; LCB 4,098.5 / 16,087.8 / 39,135.5.
- **GGUF Q8_0 · speed**: NInfer with MTP, C8 aggregate 486.3 tok/s (same-caliber bench); llama.cpp with MTP, C4 aggregate 190.8 tok/s.
- **GGUF Q8_0 · size**: GGUF 29,069,202,688 bytes (BPW 8.51), NInfer 29,361,802,240 bytes with vision (text + MTP BPW 8.51).
- The BPW denominator is always the text + MTP parameter count 27,320,697,856.

**Related repositories**

- Main repository (BF16 / FP8 / NVFP4 / INT8 / INT4 / GGUF and all other tiers): [Hugging Face](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2) · [ModelScope](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2)
- NVFP4-NInfer (NVFP4 and NInfer W4A4 / W4A4-W8A8 with built-in MTP and DFlash2, plus INT8 W8A8 and INT4 W4A16): [Hugging Face](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-NVFP4-NInfer) · [ModelScope](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-NVFP4-NInfer)

## Training method

**Lineage**: original Qwen3.8 27B (FP8; 177 / 444 / 83) → our SFT + SimPO110 final, i.e. the [EfficientThink base](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2) (171 / 442 / 89) → K3 continuation SFT → week-2 SFT (week2dose, update-225) → first RLOO round (182 groups) → another SFT round (merge-sft-100), giving sft-base-rloo (177 / 448 / 90) → second RLOO round (172 groups) → **Coder390** (178 / 445 / 90, dynamic FP8). Numbers are GPQA / MMLU / LCB, all full suites under the same 100K protocol.

**Training base**: this model starts from our own EfficientThink SFT + SimPO model (the SimPO110 final) and goes through several rounds of SFT and RLOO, which is itself a post-trained version of the official Qwen3.8-27B: [Qwen3.8-27B-EfficientThink-SFT-SimPO-DFlash2](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2).

| Name part | Meaning |
|---|---|
| Coder | Strengthened coding |
| 390 | GPQA, MMLU, and LCB all reach 90 |
| EfficientThink | Training goal: remove unproductive reasoning tails while keeping necessary long reasoning |
| Opus5.5, GPT6Astra | Wrote the gold answers and teacher trajectories |
| Grok4.7 | Host of this training run; checked and filtered data throughout |
| DSV4Pro, K3 | Their trajectories served as teacher-model data; K3 also performed the RLOO value review and wrote part of the problems |
| SFT-RLOO | Method: alternating SFT and RLOO rounds on an SFT (incl. SimPO) base |
| GGUF-NInfer | Contents of this repository: GGUF Q2 / Q3 / Q4 LynnStyle (plus Q8 MTP versions), Q6_K, and Q8_0 packages, each with a built-in MTP head, and the NInfer packages converted from them (vision built in) |

**The problem**: after the model already has a local answer, it keeps re-running the same derivation with Wait / Actually until the context is full, and the final answer is empty. In most of these cases the model can solve the problem; it just does not stop.

**RLOO data**: 8 trajectories sampled per problem; only groups with both correct and wrong trajectories are kept (all-correct groups are dropped). Groups with 0 or 1 correct trajectory receive one reviewed short teacher trajectory, which replaces the shortest wrong trajectory in that group (27 groups). Final set: 172 groups, 1,376 trajectories: 859 correct and 517 wrong, including 68 empty answers.

**Reward**: penalties apply only to wrong trajectories; long correct reasoning still earns a positive reward, so necessary long reasoning is not suppressed.

| Case | Reward |
|---|---:|
| Short and correct (<24K) | +1.05 |
| Long and correct | +1.0 |
| Short and wrong (<24K) | −0.2 |
| Wrong, 24K–48K | −0.5 |
| Wrong, ≥48K | −0.7 |
| Reached 94K with an answer letter, but wrong | −0.9 |
| Empty answer | −1.0 |

**Result**: under the same protocol, 94K truncations drop from 4 to 1 on GPQA and from 13 to 3 on LCB (FP8) compared with the original FP8, and none of the three scores falls below the original FP8 (all FP8 figures; see Scores below for GGUF Q6_K).

## Scores

**Protocol**: one RTX PRO 6000, llama.cpp (`llama-server`) loading `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`, C4, 100K context, 94,208 generation cap, client not timed, reasoning effort xhigh; full GPQA 198 / MMLU 500 / LCB 100; empty answers count as wrong, truncations that still answer correctly count as correct, and every failure stays in the denominator. `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer` is converted from the same GGUF with the same backbone quantization; the full triad was run only on the GGUF.

Reasoning length is `usage.reasoning_tokens`; a 94K truncation means the generation cap was hit. LCB empty answers are the number of problems for which no runnable code could be extracted. Bold means better than the original Qwen3.8 27B (FP8).

The original Qwen3.8 27B (FP8) was measured on two RTX PRO 6000 GPUs at C8 per GPU with SGLang; the rest of the protocol is the same.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | Original Qwen3.8 27B (FP8) | 177/198 | 5,299 / 12,607 / 50,577 | 4 | 3 |
| GPQA | GGUF Q3 LynnStyle | 173/198 | **3,125.5** / **7,265.2** / **24,343.1** | **1** | **1** |
| MMLU | GGUF Q3 LynnStyle | **449/500** | **148** / **279.3** / **923.4** | **0** | 0 |
| LCB | GGUF Q3 LynnStyle | **92/100** | **4,421** / **14,232.2** / **34,946** | **1** | **1** |
| GPQA | GGUF Q4 LynnStyle | 175/198 | **2,951.0** / **8,159.3** / **25,649.0** | **1** | **2** |
| MMLU | GGUF Q4 LynnStyle | **448/500** | **164** / **312.9** / **1,077.7** | **0** | 0 |
| LCB | GGUF Q4 LynnStyle | **89/100** | **3,669.5** / **14,810.5** / **38,182.1** | **2** | **2** |
| GPQA | GGUF Q2 LynnStyle | 177/198 | **2,989.5** / **8,923.8** / **27,156.1** | **3** | **0** |
| MMLU | GGUF Q2 LynnStyle | 433/500 | **181** / **326.3** / **1,020.5** | 1 | 0 |
| LCB | GGUF Q2 LynnStyle | **90/100** | **5,656.5** / **17,835.8** / **40,067.3** | **1** | **1** |
| GPQA | GGUF Q8_0 | 171/198 | **3,102.5** / **7,971** / **28,891.6** | **2** | **0** |
| GPQA | GGUF Q6_K | 174/198 | **3,683** / **9,814** / **27,966** | **2** | **2** |
| MMLU | Original Qwen3.8 27B (FP8) | 444/500 | 205 / 373 / 1,622 | 1 | 0 |
| MMLU | GGUF Q8_0 | 443/500 | **164** / **291** / **741** | **0** | 0 |
| MMLU | GGUF Q6_K | **448/500** | **162** / **310.3** / **939.4** | **0** | 0 |
| LCB | Original Qwen3.8 27B (FP8) | 83/100 | 8,388 / 24,241 / 94,208 | 13 | 13 |
| LCB | GGUF Q8_0 | **90/100** | **4,098.5** / **16,087.8** / **39,135.5** | **3** | **3** |
| LCB | GGUF Q6_K | **91/100** | — | **0** | **1** |

Note: reasoning lengths for Q2 / Q3 / Q4 LynnStyle, Q8_0, and Q6_K MMLU are counted from the raw text with the BF16 tokenizer (GPQA/LCB: `reasoning` field; MMLU: text before the last line of `response`), not from the API `reasoning_tokens`. Q6_K LCB has no saved reasoning text and cannot be counted; that cell reads "—".

Q6_K: GPQA's 2 truncations are problems 79 and 127; both hit 94,208 with an empty pred, so they also count as the empty answers. MMLU has no truncations and no empty answers.

LCB has no 94K truncations; its 1 empty answer is problem 92, which stopped normally without producing code.

LCB is scored on llama.cpp: the LCB eval script gets replies from NInfer that are not valid JSON. This is a compatibility issue between the eval script and the API, not a model-quality issue; the same GGUF on llama.cpp passed every problem in the same spot-check batch.

## Run this model in Lynn desktop Agent (V0.87.1)

[Lynn](https://github.com/MerkyorLynn/Lynn) is an open-source desktop AI Agent (GUI + standalone CLI): chat, search, file edits, coding, and realtime voice in one app, or as a headless worker for other tools and CI. **Free. Quick Start needs no configuration and no API key.**

Current defaults (V0.87.1):

| Role | Stack |
|---|---|
| Cloud chat / coding / tools | **Step 5 Preview** (native vision — send images directly) |
| Realtime voice | **StepAudio 2.5 Realtime** |
| On-device local | **This Coder390 EfficientThink 27B** Q2 / Q3 GGUF (built-in Q4 MTP; llama.cpp — **not NInfer**; this Lynn install ships **no vision** component) |

Hardware guidance: Apple Silicon uses unified memory; NVIDIA uses the largest single GPU VRAM (not summed GPUs, not host RAM). **Install is blocked below 14GiB.** Prefer **Q2 at 16GB**, **Q3 at 24GB+**. Leave headroom for KV cache and runtime buffers beyond the GGUF file size.

Tool arguments (places, dates, leagues, tickers, currency pairs, and so on) are filled by the model rather than guessed from the whole user sentence. Desktop features such as long-term memory and writing Diff ship with Lynn; see the release notes for the full changelog.

- [V0.87.1 release notes](https://github.com/MerkyorLynn/Lynn/releases/tag/v0.87.1)
- [China download page (recommended)](https://download.merkyorlynn.com/download.html)
- macOS Apple Silicon: [mirror](https://download.merkyorlynn.com/downloads/Lynn-0.87.1-macOS-arm64.dmg) · [GitHub](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.1/Lynn-0.87.1-macOS-arm64.dmg)
- macOS Intel: [mirror](https://download.merkyorlynn.com/downloads/Lynn-0.87.1-macOS-x64.dmg) · [GitHub](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.1/Lynn-0.87.1-macOS-x64.dmg)
- Windows: [mirror](https://download.merkyorlynn.com/downloads/Lynn-0.87.1-Windows-Setup.exe) · [GitHub](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.1/Lynn-0.87.1-Windows-Setup.exe)

In Lynn: **Settings → Models → Local Qwen3.8-27B → pick Q2 / Q3 → Install & start**. Local tiers load only the Q2 / Q3 LynnStyle-MTP files under this repo’s `GGUF/` directory. NInfer / NVFP4 and other formats stay outside Lynn’s one-click install — use their own engines.

## Quantization tiers

| Tier | Directory | Notes | Package size (bytes) | BPW | GPQA / MMLU / LCB |
|---|---|---|---:|---:|---|
| GGUF Q3 LynnStyle | `GGUF/` | Mixed-precision LynnStyle GGUF for llama.cpp (`Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.gguf`): lowest type reaches Q3; **built-in Q4 MTP** (not Q8); llama.cpp vision via `--mmproj` with the mmproj in `GGUF/` | 17,303,770,432 (~16.1 GiB) | 5.07 | 173 / 449 / 92 |
| GGUF Q3 LynnStyle · NInfer | `GGUF-NInfer/` | NInfer package from the same Q3 LynnStyle GGUF (`.ninfer`), built-in Q4_K MTP and vision; NInfer-all and ninfer-fusion-kvmem; scored on llama.cpp before the built-in MTP head was attached (external Q8 MTP draft); same quantized weights | 17,596,369,920 (~16.4 GiB) | 5.07 | 173 / 449 / 92 |
| GGUF Q3 LynnStyle · Q8MTP | `GGUF/` | The same Q3 LynnStyle GGUF with only the built-in MTP head re-encoded as Q8_0 (`Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf`); every other tensor is byte-identical to the original; an alternative with a Q8_0 MTP head (the original's Q4_0 MTP head is supported by llama.cpp); llama.cpp vision via the mmproj in `GGUF/` | 17,516,107,072 (~16.3 GiB) | 5.13 | 173 / 449 / 92 |
| GGUF Q3 LynnStyle · Q8MTP · NInfer | `GGUF-NInfer/` | NInfer package from the Q8MTP GGUF above (`Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.ninfer`), built-in Q8_0 MTP head and vision, model id `qwen3.8-27b-coder390-Q3LynnStyle-Q8Mtp`; body weights identical to the original Q3 LynnStyle package, scores carried over | 17,808,706,560 (~16.6 GiB) | 5.13 | 173 / 449 / 92 |
| GGUF Q4 LynnStyle | `GGUF/` | Mixed-precision LynnStyle GGUF for llama.cpp (`Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.gguf`): lowest type reaches Q4; **built-in Q4 MTP** (not Q8); llama.cpp vision via `--mmproj` with the mmproj in `GGUF/` | 19,620,406,592 (~18.3 GiB) | 5.75 | 175 / 448 / 89 |
| GGUF Q4 LynnStyle · NInfer | `GGUF-NInfer/` | NInfer package from the same Q4 LynnStyle GGUF (`.ninfer`), built-in Q4_K MTP and vision; NInfer-all and ninfer-fusion-kvmem; scored on llama.cpp before the built-in MTP head was attached (external Q8 MTP draft); same quantized weights | 19,913,006,080 (~18.5 GiB) | 5.74 | 175 / 448 / 89 |
| GGUF Q4 LynnStyle · Q8MTP | `GGUF/` | The same Q4 LynnStyle GGUF with only the built-in MTP head re-encoded as Q8_0 (`Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf`); every other tensor is byte-identical to the original; an alternative with a Q8_0 MTP head (the original's Q4_0 MTP head is supported by llama.cpp); llama.cpp vision via the mmproj in `GGUF/` | 19,832,743,232 (~18.5 GiB) | 5.81 | 175 / 448 / 89 |
| GGUF Q4 LynnStyle · Q8MTP · NInfer | `GGUF-NInfer/` | NInfer package from the Q8MTP GGUF above (`Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer`), built-in Q8_0 MTP head and vision, model id `qwen3.8-27b-coder390-Q4LynnStyle-Q8Mtp`; body weights identical to the original Q4 LynnStyle package, scores carried over | 20,125,342,720 (~18.7 GiB) | 5.81 | 175 / 448 / 89 |
| GGUF Q2 LynnStyle | `GGUF/` | Mixed-precision LynnStyle GGUF for llama.cpp (`Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf`): lowest type reaches Q2; **built-in Q4 MTP** (not Q8); llama.cpp vision via `--mmproj` with the mmproj in `GGUF/` | 13,276,009,792 (~12.4 GiB) | 3.89 | 177 / 433 / 90 |
| GGUF Q2 LynnStyle · NInfer | `GGUF-NInfer/` | NInfer package from the same Q2 LynnStyle GGUF (`.ninfer`), built-in Q4_K MTP and vision; NInfer-all and ninfer-fusion-kvmem; scores from GGUF on llama.cpp | 13,568,617,472 (~12.6 GiB) | 3.89 | 177 / 433 / 90 |
| GGUF Q2 LynnStyle · Q8MTP | `GGUF/` | The same Q2 LynnStyle GGUF with only the built-in MTP head re-encoded as Q8_0 (`Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf`); every other tensor is byte-identical to the original; an alternative with a Q8_0 MTP head (the original's Q4_0 MTP head is supported by llama.cpp); llama.cpp vision via the mmproj in `GGUF/` | 13,488,346,432 (~12.6 GiB) | 3.95 | 177 / 433 / 90 |
| GGUF Q2 LynnStyle · Q8MTP · NInfer | `GGUF-NInfer/` | NInfer package from the Q8MTP GGUF above (`Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.ninfer`), built-in Q8_0 MTP head and vision, model id `qwen3.8-27b-coder390-Q2LynnStyle-Q8Mtp`; body weights identical to the original Q2 LynnStyle package, scores carried over | 13,780,954,112 (~12.8 GiB) | 3.95 | 177 / 433 / 90 |
| GGUF Q8_0 | `GGUF/` | Single GGUF file for llama.cpp (`Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf`): Q8_0 backbone, built-in MTP head | 29,069,202,688 (~27.1 GiB) | 8.51 | 171 / 443 / 90 |
| GGUF Q8_0 · NInfer | `GGUF-NInfer/` | NInfer package converted from the same Q8_0 GGUF (`.ninfer`), built-in MTP head and vision component; loadable only by NInfer-all (`iamwavecut/ninfer-all`); scores from the same GGUF on llama.cpp | 29,361,802,240 (~27.3 GiB) | 8.51 | 171 / 443 / 90 |
| GGUF Q6_K | `GGUF/` | Single GGUF file for llama.cpp (`Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`): Q6_K backbone with imatrix calibration and a built-in Q8 MTP head, so no external draft is needed; llama.cpp vision: `--mmproj GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` | 23,177,516,384 (≈21.6 GiB) | 6.79 | 174 / 448 / 91 |
| GGUF Q6_K · NInfer | `GGUF-NInfer/` | NInfer package (`.ninfer`) converted from the same GGUF, same backbone quantization, built-in MTP head (attention/MLP weights Q6_K, input projection Q8_0); vision component built in (image input with `--vision`); loadable only by NInfer-all (`iamwavecut/ninfer-all`); scores measured on the same GGUF with llama.cpp | 23,379,962,880 (≈21.8 GiB) | 6.76 | 174 / 448 / 91 |

**Community fork ninfer-fusion-kvmem:** the Q2 / Q3 / Q4 LynnStyle NInfer packages (`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer`, `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer`, `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer`) carry a built-in MTP head re-encoded as Q4_K and load and run MTP on both the official NInfer-all `master` and the community fork ninfer-fusion-kvmem (tested 2026-10-11). The `.gguf` files in `GGUF/` keep a Q4_0 MTP head, which llama.cpp supports. The Q8 MTP versions remain available as an alternative (same weights, only the MTP head re-encoded as Q8_0): `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf`, `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf` and `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf` for llama.cpp, and `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.ninfer`, `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.ninfer` and `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer` for NInfer (model ids `qwen3.8-27b-coder390-Q2LynnStyle-Q8Mtp`, `qwen3.8-27b-coder390-Q3LynnStyle-Q8Mtp`, `qwen3.8-27b-coder390-Q4LynnStyle-Q8Mtp`).

**Q8 MTP versions · check** (2026-10-09, one RTX PRO 6000): NInfer-all `master` with `--spec mtp --draft-tokens 3 --vision`, int8 KV, 8,192 context; llama.cpp with `--spec-type draft-mtp --spec-draft-n-max 4` and `--mmproj`; one image request each, short runs. The image question was answered correctly in every run (llama.cpp with thinking on and off).

| Package | NInfer decode tok/s | NInfer MTP acceptance (tokens/round) | llama.cpp decode tok/s | llama.cpp draft acceptance | Image |
|---|---:|---:|---:|---:|---|
| Q2 LynnStyle · Q8MTP | 211.7 | 64.2% (3.14) | 180.1 | 0.879 | correct |
| Q3 LynnStyle · Q8MTP | 134.9 | 51.7% (2.55) | 138.3 | 0.904 | correct |
| Q4 LynnStyle · Q8MTP | 154.8 | 71.0% (3.13) | 135.6 | 0.879 | correct |

BPW for GGUF Q3 LynnStyle is 17303770432 × 8 ÷ the text + MTP parameter count 27,320,697,856 = 5.07; the Q3 NInfer package was 17300551168 bytes before the vision component was added, BPW 5.07. BPW for GGUF Q4 LynnStyle is 19620406592 × 8 ÷ the text + MTP parameter count 27,320,697,856 = 5.75; the Q4 NInfer package was 19617187328 bytes before the vision component was added, BPW 5.74. BPW for GGUF Q2 LynnStyle is 13,276,009,792 × 8 ÷ the text + MTP parameter count 27,320,697,856 = 3.89; the Q2 NInfer package was 13,272,798,720 bytes before the vision component was added, BPW 3.89. BPW for GGUF Q8_0 is 29,069,202,688 × 8 ÷ 27,320,697,856 = 8.51; the Q8_0 NInfer package was 29,065,983,488 bytes before the vision component was added, BPW 8.51. BPW for the two GGUF Q6_K packages is the single file's bytes × 8 ÷ the text + MTP parameter count 27,320,697,856: the GGUF is 23,177,516,384 bytes, giving 6.79, and the NInfer package was 23,084,144,128 bytes before the vision component was added, giving 6.76. The parameter count comes from the GGUF header (866 tensors: text 26,895,998,464 + MTP 424,699,392); vision is not counted in the denominator (neither the llama.cpp mmproj nor the 295,720,448-byte vision part now inside each `.ninfer`). The BF16 / FP8 / NVFP4 tiers in the main repository use 27,781,427,952 (including the vision tower), so BPW should not be compared directly across the two.

## Best-TPS and concurrency recommendations

Setup: one RTX PRO 6000 Blackwell; 1-minute quick benchmark, 512 generation cap, thinking on (xhigh), sampling temperature 1.0, top_p 0.95, top_k 20; each level sends only as many requests as its concurrency (1 at C1, 2 at C2, 4 at C4, 8 at C8). Numbers are aggregate tok/s (all output tokens ÷ wall-clock time). This is a quick benchmark with few requests and short outputs, so the numbers are not directly comparable with benchmarks run under other protocols. NInfer rows were measured on the `GGUF-NInfer/` package with the server at `--max-context 32768 --kv-capacity 32768 --kv-dtype rk8v4 --max-concurrency 8`; llama.cpp rows were measured on the `GGUF/` package.

| Engine · speculation | C1 | C2 | C4 | C8 |
|---|---:|---:|---:|---:|
| NInfer · Q8_0 MTP (4 draft tokens) | 109.5 | not measured | 332.0 | **486.3** |
| NInfer · Q6_K MTP (3 draft tokens) | 131.9 | 161.9 | **235.5** | 388.1 |
| NInfer · no speculation | 56.0 | 93.9 | 162.1 | 298.1 |
| NInfer · Q3 LynnStyle MTP (4 draft, 512-cap short) | 167.4 | 179.8 | 285.1 | **512.3** |
| llama.cpp · Q3 LynnStyle MTP (4096-cap long) | 78.5 | 161.6 | **191.8** | not measured |
| NInfer · Q4 LynnStyle MTP (4 draft, 512-cap short) | 157.0 | 174.3 | 287.5 | **436.4** |
| llama.cpp · Q4 LynnStyle MTP (4096-cap long) | 73.6 | 77.7 | **81.1** | not measured |
| NInfer · Q2 LynnStyle MTP (4 draft) | 205.7 | 210.4 | 308.0 | **521.0** |
| llama.cpp · Q2 LynnStyle MTP | 104.9 | 167.6 | **174.8** | not measured |
| llama.cpp · Q8_0 MTP | 85.3 | 133.6 | **190.8** | not measured |
| llama.cpp · Q6_K MTP | 97.2 | 95.3 | 168.1 | 189.0 |
| llama.cpp · no speculation | 53.4 | not measured | 123.0 | not measured |

- **Recommendation (Q8)**: NInfer + C8 + MTP (486.3 tok/s). Q6_K is still recommended at NInfer + C4 + MTP (235.5 tok/s), matching its launch command below (`--max-concurrency 4`); for aggregate throughput alone, Q6_K at C8 is higher (388.1 tok/s).
- **MTP is built in**: every package carries a built-in MTP head (Q2 / Q3 / Q4 LynnStyle: Q4_0 in the `.gguf`, Q4_K in the `-Q4MTP.ninfer`, their -Q8MTP versions: Q8_0; Q6_K: GGUF Q8_0, NInfer Q6_K attention/MLP weights), so no external draft model is needed. For Q6_K at a single request, NInfer with MTP reaches 131.9 tok/s, about 2.5× llama.cpp without speculation (53.4 tok/s); llama.cpp with MTP reaches 97.2 tok/s aggregate at C1 (119.0 tok/s single-request decode).

## Recommended launch commands

### Quantization scheme

**GGUF Q6_K** (`GGUF/`, `GGUF-NInfer/`): Q6_K backbone calibrated with a 512-chunk imatrix, plus structure protection: the linear-attention (SSM) `ssm_alpha` / `ssm_beta` stay BF16, the token embedding and output head are Q8_0, and the MTP head (`blk.64` attn q/k/v/output, ffn gate/up/down, and `nextn.eh_proj`) is entirely Q8_0 with its norms kept in F32. The GGUF has 866 tensors in 65 blocks (64 backbone layers + 1 MTP layer). The `.ninfer` is converted from the same GGUF with the same backbone quantization; its MTP attention/MLP weights are Q6_K (`gguf_q6_k`) and only `mtp/input_projection` is Q8_0; the GGUF has no vision weights (llama.cpp uses `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` via `--mmproj`); the `.ninfer` carries the vision component inside the package (add `--vision`; see NInfer · vision below).

### Commands

Load the `.ninfer` with NInfer-all (the `master` branch of `iamwavecut/ninfer-all`): the package keeps the GGUF quantization blocks, which other NInfer builds cannot read. llama.cpp needs an upstream build that supports `--spec-type draft-mtp`. NInfer's `--kv-capacity` is one KV pool shared by all requests; llama.cpp's `-c 409600 -np 4` splits the context evenly across 4 slots, so each request gets at most 102,400 tokens, enough for a single request to reach 94K. The chat endpoint is `POST /v1/chat/completions`; for NInfer the request `model` must match `--model-id`. Vision: `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` for llama.cpp `--mmproj` (629,247,008 bytes, sha256 `cae9799dc9196449b0d83f716e64af89d5cf65147510462e5a629a2aa23adb32`). Each `.ninfer` package carries the vision component; add `--vision` to `ninfer-serve` to accept images (see NInfer · vision below).

**16 GB VRAM / single-stream pick:** for 16 GB cards and single-user use, `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer` is the friendlier choice. It is the smallest NInfer package in this repo (13,568,617,472 bytes, about 12.6 GiB), has a built-in Q4_K MTP head and built-in vision (add `--vision`; no mmproj needed), and runs on both the official NInfer-all `master` and the community fork ninfer-fusion-kvmem. No 16 GB card was tested; this recommendation is by size. Start at 32K context and lower it if memory runs short.

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer \
  --model-id qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --max-context 32768 --kv-capacity 32768 --kv-dtype rk8v4 \
  --max-concurrency 1 --spec mtp --draft-tokens 4 --vision
```

**Community fork ninfer-fusion-kvmem:** the Q2 / Q3 / Q4 LynnStyle NInfer packages (`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer`, `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer`, `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer`) carry a built-in MTP head re-encoded as Q4_K and load and run MTP on both the official NInfer-all `master` and the community fork ninfer-fusion-kvmem (tested 2026-10-11). The `.gguf` files in `GGUF/` keep a Q4_0 MTP head, which llama.cpp supports. The Q8 MTP versions remain available as an alternative (same weights, only the MTP head re-encoded as Q8_0): `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf`, `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf` and `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf` for llama.cpp, and `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.ninfer`, `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.ninfer` and `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer` for NInfer (model ids `qwen3.8-27b-coder390-Q2LynnStyle-Q8Mtp`, `qwen3.8-27b-coder390-Q3LynnStyle-Q8Mtp`, `qwen3.8-27b-coder390-Q4LynnStyle-Q8Mtp`).

**MTP and DFlash2**: every GGUF / NInfer package in this repository has a built-in MTP head (Q2 / Q3 / Q4 LynnStyle use built-in **Q4** MTP: Q4_0 in the `.gguf`, Q4_K in the `-Q4MTP.ninfer`; their `-Q8MTP` versions use a Q8_0 MTP head). To enable it, add `--spec mtp --draft-tokens N` for NInfer or `--spec-type draft-mtp --spec-draft-n-max N` for llama.cpp; leave these out to run without speculation. DFlash2 is an external draft model and is not in these packages; this repository does not ship a DFlash2 draft for GGUF / NInfer. For DFlash2, use the `DFlash2-FP8/` draft that ships with the BF16 / FP8 / NVFP4 tiers in the main repository (SGLang `--speculative-algorithm DFLASH`) or the `.ninfer` packages in the NVFP4-NInfer repository (`--spec dflash2`). MTP and DFlash2 are mutually exclusive: a server runs one or the other, never both.

#### NInfer

**NInfer · GGUF Q2 LynnStyle · MTP (draft 4, recommended concurrency 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer \
  --model-id qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --kv-dtype rk8v4 \
  --max-concurrency 8 --spec mtp --draft-tokens 4
```

**NInfer · GGUF Q3 LynnStyle · MTP (draft 4, recommended concurrency 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q3LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4
```

**NInfer · GGUF Q4 LynnStyle · MTP (draft 4, recommended concurrency 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q4LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4
```

**NInfer · GGUF Q4 LynnStyle · Q8MTP · MTP (draft 4, recommended concurrency 8)**: an alternative with a Q8_0 MTP head (the `-Q4MTP` packages also run on NInfer-all and ninfer-fusion-kvmem); for Q2 / Q3 replace `Q4` with `Q2` / `Q3` in the file name and model id.

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q4LynnStyle-Q8Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4
```

**NInfer · GGUF Q6_K · MTP (draft 3, recommended concurrency 4)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer \
  --model-id qwen3.8-27b-coder390-q6k-mtp \
  --max-context 102400 --kv-capacity 409600 --kv-dtype rk8v4 \
  --max-concurrency 4 --spec mtp --draft-tokens 3
```

**NInfer · GGUF Q8_0 · MTP (draft 4, recommended concurrency 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer \
  --model-id qwen3.8-27b-coder390-q8-mtp \
  --max-context 102400 --kv-capacity 819200 --kv-dtype rk8v4 \
  --max-concurrency 8 --spec mtp --draft-tokens 4
```

Do not use `--max-context 131072 --kv-capacity 131072` (the KV pool then holds only one full context and queued requests return HTTP 503). Do not use `--lm-head-q6` / `--embedding-q4`. Requires NInfer-all (`ninfer-serve`); official ninfer-src cannot read `gguf_blocks_v1`.

**NInfer · vision (image input)**

Every `.ninfer` in `GGUF-NInfer/` contains the vision component (295,720,448 bytes, added on 2026-10-09). It was quantized from the BF16 vision weights in the NInfer vision formats: patch embedding Q6, attention q/k/v and MLP fc1 Q4, other projections Q5, merger Q8, norms and biases BF16. The text and MTP weights are byte-for-byte the same as before. Add `--vision` to any NInfer command above; nothing else is needed (the separate `vision-bf16.safetensors` is not used). These packages have a built-in MTP head but no DFlash2 draft, so each package has two commands: no speculation and MTP.

```bash
# Q2LynnStyle · no speculation
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --vision

# Q2LynnStyle · MTP (4 draft tokens)
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4 \
  --vision

# Q3LynnStyle · no speculation
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q3LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --vision

# Q3LynnStyle · MTP (4 draft tokens)
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q3LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4 \
  --vision

# Q4LynnStyle · no speculation
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q4LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --vision

# Q4LynnStyle · MTP (4 draft tokens)
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q4LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4 \
  --vision

# Q6_K · no speculation
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-q6k-mtp \
  --max-context 102400 --kv-capacity 409600 --max-concurrency 4 \
  --kv-dtype rk8v4 \
  --vision

# Q6_K · MTP (3 draft tokens)
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-q6k-mtp \
  --max-context 102400 --kv-capacity 409600 --max-concurrency 4 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 3 \
  --vision

# Q8_0 · no speculation
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-q8-mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --vision

# Q8_0 · MTP (4 draft tokens)
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-q8-mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4 \
  --vision
```

Image request (OpenAI-style `image_url` part; `url` takes an `http(s)://` image link; a data URI of a local image also works; `model` must match `--model-id`):

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.8-27b-coder390-Q4LynnStyle-Mtp",
    "messages": [{"role": "user", "content": [
      {"type": "image_url", "image_url": {"url": "https://example.com/demo.png"}},
      {"type": "text", "text": "Describe this image."}
    ]}],
    "max_tokens": 2048
  }'
```

Send images as OpenAI-style `image_url` parts to `POST /v1/chat/completions`. `--vision` keeps the vision encoder on the GPU; if VRAM is tight, use `--vision-cpu` instead (it runs on the CPU, and each image is capped at 256 merged tokens unless you set `--vision-max-merged`). Without `--vision` the package runs text-only, as before. `GGUF-NInfer/vision-bf16.safetensors` is the BF16 source of the vision part and is not needed to run NInfer. Engine test (2026-10-09, one RTX PRO 6000): the Q2 LynnStyle package with `--vision` answered an image prompt correctly; with MTP at 3 draft tokens the accept length was 3.00 and decode speed 207 tok/s. On NInfer-all `master`, the Q3 / Q4 LynnStyle, Q6_K, and Q8_0 packages were also tested with MTP and `--vision` and all answered correctly (short single runs: Q4 151.9 tok/s, accept rate 66.7%; Q6_K 131.1 tok/s, 65.4%; Q8_0 121.5 tok/s, 68.2%); for the Q8 MTP versions see "Q8 MTP versions · check" above.

#### llama.cpp

**llama.cpp · GGUF Q2 LynnStyle · MTP (representative; swap the `-m` path for Q3 / Q4 / Q6_K / Q8_0)**

```bash
llama-server -m ./GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf \
  -c 409600 -np 4 -ngl 99 --jinja \
  --host 127.0.0.1 --port 8080 \
  --alias qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --spec-type draft-mtp --spec-draft-n-max 4
```

To use another GGUF tier, only change `-m` to `...-Q3LynnStyle-MTP.gguf`, `...-Q4LynnStyle-MTP.gguf`, `...-Q6_K-MTP.gguf`, or `...-Q8_0-MTP.gguf` (and the `--alias`, e.g. `qwen3.8-27b-coder390-q6k-mtp`, `qwen3.8-27b-coder390-q8-mtp`). MTP is fused inside the GGUF (`blk.64`); do not attach an external draft; the log should show `creating MTP draft context against the target model`. For image input add `--mmproj ./GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`.

**llama.cpp · vision (image input)**

```bash
llama-server -m ./GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf \
  --mmproj ./GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf \
  -c 409600 -np 4 -ngl 99 --jinja \
  --host 127.0.0.1 --port 8080 \
  --alias qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --spec-type draft-mtp --spec-draft-n-max 4
```

The GGUF files have no vision weights; `--mmproj ./GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` adds them and works with all eight GGUF files (swap `-m` and `--alias` as above; image input tested on Q3 / Q4 LynnStyle, Q6_K, and Q8_0). Leave out `--spec-type` / `--spec-draft-n-max` to run without speculation. Without `--mmproj` llama.cpp runs text-only. Images go as OpenAI-style `image_url` parts to `POST /v1/chat/completions` (same request as the NInfer example, with `model` set to the `--alias`).

**Optional: external Q8_0 MTP draft.** `GGUF/mtp-Qwen3.8-27B-Coder390-EfficientThink-Q8_0.gguf` (3,164,006,656 bytes) is a standalone Q8_0 MTP head, the same weights as the built-in MTP head of the Q6_K and Q8_0 packages. Q2, Q3 and Q4 LynnStyle ship a smaller Q4 MTP head; add `-md` pointing at this file to use the Q8 head instead. Q6_K and Q8_0 already contain a Q8 head, so they gain nothing from it. With `-md` the log shows `loading draft model` rather than `creating MTP draft context against the target model`. Checked on one RTX PRO 6000 on 2026-10-09 (llama.cpp, Q3 LynnStyle target, `--spec-draft-n-max 4`): the log shows `loading draft model`. Greedy acceptance is 66.1% at 110.2 tok/s, against 66.0% at 112.2 tok/s for the built-in Q4 MTP head with the same command and no `-md`. At temperature 1.0 the two are 52.4% at 94.4 tok/s and 51.9% at 95.6 tok/s. All 12 prompts produced the same text; the Q8 file is not faster.

```bash
llama-server -m ./GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.gguf \
  -md ./GGUF/mtp-Qwen3.8-27B-Coder390-EfficientThink-Q8_0.gguf \
  -c 409600 -np 4 -ngl 99 --jinja \
  --host 127.0.0.1 --port 8080 \
  --alias qwen3.8-27b-coder390-Q3LynnStyle-Mtp \
  --spec-type draft-mtp --spec-draft-n-max 4
```
## Files overview

### `GGUF/` (Q3/Q4/Q2/Q8/Q6 packages + Q3/Q4/Q2 Q8MTP packages + Q8 MTP draft + mmproj + SHA256SUMS)

| File | Bytes | SHA256 |
|---|---:|---|
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.gguf` | 17,303,770,432 | `9985b3d41fc7dc0bb5d493f7523d4515504912a3a7fc830f66e0fd2f90f9fd95` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.gguf` | 19,620,406,592 | `56c7c605a59764d9f0bb645d4eb335f1574af2c9e74020386139597df0e872f5` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf` | 13,276,009,792 | `cad973b3b7cc0d86bd39968209268318a746673c12c9536e5c37408baa7b5e6e` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf` | 13,488,346,432 | `62fd6cf6079dfb02b3e3aab68e39b4cdc6a471a51a82b56c9a76068e961d8a4a` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf` | 17,516,107,072 | `2c74a65df9d229bfba2eb3a878a25b84d4035d1be4061c9a665af213d98cae58` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf` | 19,832,743,232 | `5e2a1784298f696cb38f063962da0ad4acd1fd020c6e7c6e520df54acf8f57eb` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf` | 29,069,202,688 | `b24e8c5fe3f2b282cce841400c740fcaca48afcdcf9e991f7bbe9a59a78cabfe` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf` | 23,177,516,384 | `302597c53d1b00f7230b53a8a050831390a4371e92a80c1ac644fa920af76ab1` |
| `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` | 629,247,008 | `cae9799dc9196449b0d83f716e64af89d5cf65147510462e5a629a2aa23adb32` |
| `GGUF/mtp-Qwen3.8-27B-Coder390-EfficientThink-Q8_0.gguf` | 3,164,006,656 | `50a030e852289eed86065e2e2de57d89241174e99faa2c1c2f06c29c270789ee` |
| `GGUF/SHA256SUMS` | 1,187 | `7677cef32b796c8c54d18592e8d198a14563a994496c8161b84ab7bdba30d183` |

### `GGUF-NInfer/` (Q3/Q4/Q2 -Q4MTP packages (Q4_K MTP head) + Q8/Q6 + Q3/Q4/Q2 Q8MTP packages (Q8_0 MTP head), all with vision + vision-bf16.safetensors (BF16 source, not needed at runtime) + SHA256SUMS)

| File | Bytes | SHA256 |
|---|---:|---|
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer` | 17,596,369,920 | `f1d4e45fb12db2a0b142c00badc14f1413869acbeb8b40bc0898c4f4610f322e` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer` | 19,913,006,080 | `e445a0a970ea10975858c6ee679741be0a119fc763c9d7fa23c3999094aa032b` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer` | 13,568,617,472 | `a6555ef4623fa0d0cc81a5674bff724c60bf69bdcd70dc6e5be97c4afbfab040` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.ninfer` | 13,780,954,112 | `993ff3e54f7bd697c2f88b62b9d00455fb95c095d7d99d4cd458868cf6b5c6d3` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.ninfer` | 17,808,706,560 | `815241ba4d8f62055720d8632617b24814da3bf881948867b8eb65dbccd4bdb3` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer` | 20,125,342,720 | `f88730f1fc8d65d720780da6b305e9c943c016f4660695923d7023eddd6b2fad` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer` | 29,361,802,240 | `8ace439259c8ade2b7dacee8aca92df62d7cc93d6c7d40ac026be797bb02a9c5` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer` | 23,379,962,880 | `60d7b3f4f79304e1ab1e22c161cdace29e7f8f9b8350755e4eab45e2d5e0d168` |
| `GGUF-NInfer/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `GGUF-NInfer/SHA256SUMS` | 1,082 | `7cb6f58402c7fc14b7740487407c285232a54989e3ad1ebf25892c597944af38` |

### `imatrix/` (GGUF imatrix + calibration set)

`imatrix/coder390-imatrix-calibration.txt` is the calibration text for recomputing the importance matrix (imatrix) of the GGUF files: 1,368 records (171 problems × 8) rebuilt from the inputs of this model's RL training rollouts, 500,816 tokens. It contains no benchmark questions (a 13-gram overlap check against MMLU, GPQA Diamond and LiveCodeBench found 0 hits). It is functionally equivalent to, but not byte-identical with, the set used for the published GGUFs; the original imatrix data file was not kept. `imatrix/coder390-imatrix.gguf` is an imatrix recomputed from this set on 2026-10-09 (BF16 GGUF of this model, llama.cpp `71ad059`, `-c 512 --chunks 512`; 496 entries and 512 chunks, the same counts as the published GGUF metadata) and can be passed to `llama-quantize --imatrix` directly. Commands and checks are in `imatrix/README.md`.

| File | Bytes | SHA256 |
|---|---:|---|
| `imatrix/coder390-imatrix-calibration.txt` | 1,710,336 | `2113e4f3720c88621e05fc0424008d45bbb05d2ad338e082c6d52662c1f2ef94` |
| `imatrix/coder390-imatrix.gguf` | 27,300,160 | `be0924f24bd82c05b28da0c1d803ef29c1961f60bf9e978a16ffe746ee2adcf1` |
| `imatrix/SHA256SUMS` | 187 | `215787c717b8260885dd95af463c246a3e37a38aa05d1a1fb68c61261bd0dd37` |

### Verification

```bash
(cd GGUF && sha256sum -c SHA256SUMS)
(cd GGUF-NInfer && sha256sum -c SHA256SUMS)
(cd imatrix && sha256sum -c SHA256SUMS)
```

## Loading notes

- Q6_K: both packages share the same backbone quantization (Q6_K + imatrix + structure protection; see Quantization scheme above) and carry a built-in MTP head (GGUF `blk.64` is Q8_0; NInfer MTP attention/MLP weights are Q6_K, input projection Q8_0), so no external draft model is needed; NInfer + C4 + MTP is recommended.
- `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`: loads directly in llama.cpp; the GGUF architecture is `qwen35` with 65 blocks, the last of which (`blk.64`) is MTP.
- `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer`: loadable only by NInfer-all; SGLang, vLLM, llama.cpp, and transformers cannot read it.
- Vision: llama.cpp `--mmproj GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` (629,247,008 bytes, sha256 `cae9799dc9196449b0d83f716e64af89d5cf65147510462e5a629a2aa23adb32`). NInfer: each `.ninfer` package carries the vision component; add `--vision`. `GGUF-NInfer/vision-bf16.safetensors` (921,497,224 bytes, sha256 `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33`) is the BF16 source of that part and is not needed at run time.
- Scores were measured with the GGUF package on llama.cpp; the LCB eval script is not compatible with the NInfer API (its replies are not valid JSON), which is an eval-script issue rather than a model-quality issue, so LCB is scored on llama.cpp.

## Known limitations

- GGUF Q6_K: GPQA 174 is below the 177 of the original Qwen3.8 27B (FP8); MMLU reasoning length is counted from the raw text with the BF16 tokenizer, and LCB kept no reasoning text, so it has no reasoning-length percentiles; the full triad was run only on the GGUF (llama.cpp), not separately on the NInfer package; speeds come from a quick benchmark (requests per level equal to the concurrency, 512 generation cap) and are not directly comparable with the other tiers; mmproj is provided in `GGUF/`; image input was tested with llama.cpp + mmproj on Q3 / Q4 LynnStyle, Q6_K, and Q8_0, and with NInfer `--vision` on Q2 / Q3 / Q4 LynnStyle, Q6_K, and Q8_0.
- Scores depend on the protocol above (100K context, 94,208-token cap, no timeout) and should not be compared directly with numbers from other protocols; MMLU shows sampling variation.

## License and acknowledgements

Licensed under Apache-2.0, following the license of the base model Qwen3.8-27B.

Thanks to the Qwen team for the base model and the official FP8 scheme; to Opus5.5, GPT6Astra, Grok4.7, DSV4Pro, and K3 for problem writing, gold labels, teacher trajectories, data review, and the RLOO value review; and to the llama.cpp and NInfer communities.
<!-- CARD_EN_END -->

<!-- LANG_SEPARATOR -->

---

<!-- CARD_ZH_START -->
# Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-GGUF-NInfer

![和原版对比](assets/coder390-vs-original-zh.png)

![GGUF 各档成绩、体积与速度](assets/header-gguf-tier-table-zh.png)

在 [Qwen3.8-27B-EfficientThink-SFT-SimPO-DFlash2](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2)(官方 [Qwen3.8-27B](https://modelscope.cn/models/Qwen/Qwen3.8-27B) 经 SFT + SimPO 后训练得到的模型)基础上继续做多轮 SFT 与 RLOO 后训练,专治原版「已有答案却停不下来、写满 94K 也不给最终答案」的问题。本仓库是 **GGUF** 档的独立仓库,目前提供 `GGUF/` 下的八个 GGUF 包:**Q2 / Q3 / Q4 LynnStyle**(内置 **Q4_0** MTP 头)、同样三档的 **-Q8MTP** 版(内置 **Q8_0** MTP 头)、**Q6_K** 与 **Q8_0**(均内置 MTP 头),以及 `GGUF-NInfer/` 下对应的 NInfer 包(已内置视觉)。另附 BF16 视觉塔原始文件(`GGUF-NInfer/vision-bf16.safetensors`),供自行打包/转换;V3 `.ninfer` 已内置视觉,运行时不需要。llama.cpp 多模态请用 `--mmproj GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`(mmproj 只在 `GGUF/`,不要求放进 NInfer 包)。BF16、静态 FP8、NVFP4、NInfer W4A4、INT8 W8A8、INT4 W4A16 等其他档见主仓库 [Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2)。

- **对照基线**:原版 Qwen3.8 27B（FP8）三项为 GPQA 177/198、MMLU 444/500、LCB 83/100;GPQA 思考长度(P50 / P70 / P90 token)为 5,299 / 12,607 / 50,577。
- **GGUF Q2 LynnStyle · 成绩**:GPQA 177/198、MMLU 433/500、LCB 90/100(llama.cpp,C4,100K 全量;成绩在内置 MTP 前测得(外挂 Q8 MTP 草稿),量化权重相同)。
- **GGUF Q2 LynnStyle · 思考长度(P50 / P70 / P90 token)**:GPQA 2,989.5 / 8,923.8 / 27,156.1;MMLU 181 / 326.3 / 1,020.5;LCB 5,656.5 / 17,835.8 / 40,067.3。
- **GGUF Q2 LynnStyle · 速度**:NInfer 内置 Q4 MTP,C8 合计 521.0 tok/s(生成上限 512 短测);llama.cpp 内置 Q4 MTP,C4 合计 174.8 tok/s(生成上限 4096 长测)。口径不同,勿直接横比。
- **GGUF Q2 LynnStyle · 体积**:GGUF 13,276,009,792 字节(BPW 3.89),NInfer 13,568,617,472 字节,含视觉(文本 + MTP BPW 3.89)。
- **GGUF Q3 LynnStyle · 成绩**:GPQA 173/198、MMLU 449/500、LCB 92/100(llama.cpp,C4,100K 全量;成绩在内置 MTP 前测得(外挂 Q8 MTP 草稿),量化权重相同)。
- **GGUF Q3 LynnStyle · 思考长度(P50 / P70 / P90 token)**:GPQA 3,125.5 / 7,265.2 / 24,343.1;MMLU 148 / 279.3 / 923.4;LCB 4,421 / 14,232.2 / 34,946。
- **GGUF Q3 LynnStyle · 速度**:NInfer 内置 Q4 MTP,C8 合计 512.3 tok/s(生成上限 512 短测);llama.cpp 内置 Q4 MTP,C4 合计 191.8 tok/s(生成上限 4096 长测)。口径不同,勿直接横比。
- **GGUF Q3 LynnStyle · 体积**:GGUF 17,303,770,432 字节(BPW 5.07),NInfer 17,596,369,920 字节,含视觉(文本 + MTP BPW 5.07)。
- **GGUF Q4 LynnStyle · 成绩**:GPQA 175/198、MMLU 448/500、LCB 89/100(llama.cpp,C4,100K 全量;成绩在内置 MTP 前测得(外挂 Q8 MTP 草稿),量化权重相同)。
- **GGUF Q4 LynnStyle · 思考长度(P50 / P70 / P90 token)**:GPQA 2,951.0 / 8,159.3 / 25,649.0;MMLU 164 / 312.9 / 1,077.7;LCB 3,669.5 / 14,810.5 / 38,182.1。
- **GGUF Q4 LynnStyle · 速度**:NInfer 内置 Q4 MTP,C8 合计 436.4 tok/s(生成上限 512 短测);llama.cpp 内置 Q4 MTP,C4 合计 81.1 tok/s(生成上限 4096 长测)。口径不同,勿直接横比。
- **GGUF Q4 LynnStyle · 体积**:GGUF 19,620,406,592 字节(BPW 5.75),NInfer 19,913,006,080 字节,含视觉(文本 + MTP BPW 5.74)。
- **GGUF Q6_K · 成绩**:GPQA 174/198、MMLU 448/500、LCB 91/100(llama.cpp,C4,100K 全量)。
- **GGUF Q6_K · 思考长度(P50 / P70 / P90 token)**:GPQA 3,683 / 9,814 / 27,966。
- **GGUF Q6_K · 速度**:NInfer 开 MTP,C4 合计 235.5 tok/s;llama.cpp 开 MTP,C8 合计 189.0 tok/s(均为生成上限 512 快测)。
- **GGUF Q6_K · 体积**:GGUF 23,177,516,384 字节(BPW 6.79),NInfer 23,379,962,880 字节,含视觉(文本 + MTP BPW 6.76)。
- **GGUF Q8_0 · 成绩**:GPQA 171/198、MMLU 443/500、LCB 90/100(llama.cpp,C4,100K 全量)。
- **GGUF Q8_0 · 思考长度(P50 / P70 / P90 token)**:GPQA 3,102.5 / 7,971 / 28,891.6;MMLU 164 / 291 / 741;LCB 4,098.5 / 16,087.8 / 39,135.5。
- **GGUF Q8_0 · 速度**:NInfer 开 MTP,C8 合计 486.3 tok/s(同口径测速);llama.cpp 开 MTP,C4 合计 190.8 tok/s。
- **GGUF Q8_0 · 体积**:GGUF 29,069,202,688 字节(BPW 8.51),NInfer 29,361,802,240 字节,含视觉(文本 + MTP BPW 8.51)。
- BPW 分母均为文本 + MTP 参数数 27,320,697,856。

**相关仓库**

- 主仓（BF16 / FP8 / NVFP4 / INT8 / INT4 / GGUF 等全部版本）：[Hugging Face](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2) · [ModelScope](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2)
- NVFP4-NInfer（NVFP4 与 NInfer W4A4 / W4A4-W8A8，内置 MTP 与 DFlash2；另有 INT8 W8A8 与 INT4 W4A16）：[Hugging Face](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-NVFP4-NInfer) · [ModelScope](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-NVFP4-NInfer)

## 训练方法

**谱系**:原版 Qwen3.8 27B(FP8;177 / 444 / 83)→ 我们的 SFT + SimPO110 终版,即 [EfficientThink 基座](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2)(171 / 442 / 89)→ K3 续训 SFT → 第二周 SFT(week2dose,update-225)→ 第一轮 RLOO(182 组)→ 再一轮 SFT(merge-sft-100),得 sft-base-rloo(177 / 448 / 90)→ 第二轮 RLOO(172 组)→ **Coder390**(178 / 445 / 90,动态 FP8 口径)。括号内依次为 GPQA / MMLU / LCB,均为 100K 同口径全量。

**训练基座**:本模型以我们自己的 EfficientThink SFT + SimPO 模型(SimPO110 终版)为起点,继续做多轮 SFT 与 RLOO,该基座模型本身是官方 Qwen3.8-27B 的后训练版本,见 [Qwen3.8-27B-EfficientThink-SFT-SimPO-DFlash2](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2)。

| 名字片段 | 含义 |
|---|---|
| Coder | 代码强化 |
| 390 | GPQA、MMLU、LCB 三项都到 90 分 |
| EfficientThink | 训练目标:去掉无效的长推理尾巴,保留必要的长推理 |
| Opus5.5、GPT6Astra | 撰写出题金标与教师模型轨迹 |
| Grok4.7 | 本次训练的主持人,全程核对、筛选数据 |
| DSV4Pro、K3 | 其轨迹作为教师模型用于训练;K3 还做了 RLOO 价值评审和一部分出题工作 |
| SFT-RLOO | 训练方法:SFT(含 SimPO)基座上,SFT 与 RLOO 交替进行 |
| GGUF-NInfer | 本仓库内容:GGUF Q2 / Q3 / Q4 LynnStyle(含 Q8 MTP 版)、Q6_K、Q8_0 包(均内置 MTP 头),以及由它们转换的 NInfer 包(已内置视觉) |

**要解决的问题**:模型在局部已经有答案之后,仍用 Wait / Actually 把同一套推导反复再推,直到写满上下文,最终答案为空。这类题多数不是不会,而是停不下来。

**RLOO 数据**:每题采样 8 条轨迹,只保留组内有对有错的题(8 条全对的不入训);组内 0 或 1 条对的,补 1 条审过的短教师轨迹,替换该组最短的一条错轨迹(共 27 组)。最终 172 组、1,376 条:正确 859 条、错误 517 条,其中空答 68 条。

**奖励**:惩罚只打在错的一侧,长而正确的推理仍得正奖励,以免压制必要的长推理。

| 情形 | 奖励 |
|---|---:|
| 短且对(<24K) | +1.05 |
| 长且对 | +1.0 |
| 短且错(<24K) | −0.2 |
| 错,24K–48K | −0.5 |
| 错,≥48K | −0.7 |
| 写到 94K 有选项字母但错 | −0.9 |
| 空答 | −1.0 |

**结果**:同口径下,GPQA 的 94K 截断从原版 FP8 的 4 降到 1,LCB 从 13 降到 3,三项分数均不低于原版 FP8(均为 FP8 档;GGUF Q6_K 见下文成绩)。

## 成绩

**口径**:单张 RTX PRO 6000,llama.cpp(`llama-server`)加载 `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`,C4,上下文 100K,生成上限 94,208,客户端不计超时,思考档位 xhigh;GPQA 198、MMLU 500、LCB 100 全量;空答记错,截断但答对记对,失败样本全部留在分母里。`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer` 由同一份 GGUF 转换而来,主干量化相同,全量三联只在 GGUF 上跑。

思考长度取 `usage.reasoning_tokens`;94K 截断指写满生成上限。LCB 空答指没有提取到可运行代码的题数。加粗表示优于原版 Qwen3.8 27B(FP8)。

原版 Qwen3.8 27B(FP8)为两张 RTX PRO 6000、每卡 C8、SGLang 测得,其余口径相同。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | 原版 Qwen3.8 27B(FP8) | 177/198 | 5,299 / 12,607 / 50,577 | 4 | 3 |
| GPQA | GGUF Q3 LynnStyle | 173/198 | **3,125.5** / **7,265.2** / **24,343.1** | **1** | **1** |
| MMLU | GGUF Q3 LynnStyle | **449/500** | **148** / **279.3** / **923.4** | **0** | 0 |
| LCB | GGUF Q3 LynnStyle | **92/100** | **4,421** / **14,232.2** / **34,946** | **1** | **1** |
| GPQA | GGUF Q4 LynnStyle | 175/198 | **2,951.0** / **8,159.3** / **25,649.0** | **1** | **2** |
| MMLU | GGUF Q4 LynnStyle | **448/500** | **164** / **312.9** / **1,077.7** | **0** | 0 |
| LCB | GGUF Q4 LynnStyle | **89/100** | **3,669.5** / **14,810.5** / **38,182.1** | **2** | **2** |
| GPQA | GGUF Q2 LynnStyle | 177/198 | **2,989.5** / **8,923.8** / **27,156.1** | **3** | **0** |
| MMLU | GGUF Q2 LynnStyle | 433/500 | **181** / **326.3** / **1,020.5** | 1 | 0 |
| LCB | GGUF Q2 LynnStyle | **90/100** | **5,656.5** / **17,835.8** / **40,067.3** | **1** | **1** |
| GPQA | GGUF Q8_0 | 171/198 | **3,102.5** / **7,971** / **28,891.6** | **2** | **0** |
| GPQA | GGUF Q6_K | 174/198 | **3,683** / **9,814** / **27,966** | **2** | **2** |
| MMLU | 原版 Qwen3.8 27B(FP8) | 444/500 | 205 / 373 / 1,622 | 1 | 0 |
| MMLU | GGUF Q8_0 | 443/500 | **164** / **291** / **741** | **0** | 0 |
| MMLU | GGUF Q6_K | **448/500** | **162** / **310.3** / **939.4** | **0** | 0 |
| LCB | 原版 Qwen3.8 27B(FP8) | 83/100 | 8,388 / 24,241 / 94,208 | 13 | 13 |
| LCB | GGUF Q8_0 | **90/100** | **4,098.5** / **16,087.8** / **39,135.5** | **3** | **3** |
| LCB | GGUF Q6_K | **91/100** | — | **0** | **1** |

注:Q2 / Q3 / Q4 LynnStyle、Q8_0 三项与 Q6_K 的 MMLU 思考长度从原文用 BF16 tokenizer 计数(GPQA/LCB 用 `reasoning` 字段,MMLU 由 `response` 末行前文本拆分;不以接口 `reasoning_tokens` 为准)。Q6_K 的 LCB 没有保存思考原文,无法计数,对应格记「—」。

Q6_K:GPQA 的 2 条截断是第 79、127 题,均写满 94,208 且 pred 为空,同时记为空答。MMLU 无截断、无空答。

LCB 无 94K 截断;空答 1 条是第 92 题,正常停止但没有给出代码。

LCB 以 llama.cpp 的结果为准:LCB 测评脚本请求 NInfer 时收到的回复不是合法 JSON,这是测评脚本与接口的兼容问题,不是模型质量问题;同一份 GGUF 用 llama.cpp 跑同一批抽测题全部通过。

## 用 Lynn 桌面 Agent 跑本模型（V0.87.1）

[Lynn](https://github.com/MerkyorLynn/Lynn) 是开源桌面 AI Agent（GUI + 独立 CLI）：对话、搜资料、改文件、写代码、实时语音都能在同一套界面里完成，也可以当其他工具或 CI 的无头 worker。**全部免费，Quick Start 无需配置、无需 API Key。**

当前默认能力（V0.87.1）：

| 用途 | 方案 |
|---|---|
| 云端对话 / 编码 / 工具 | **Step 5 Preview**（原生识图，直接发图即可） |
| 实时语音 | **StepAudio 2.5 Realtime** |
| 端侧本地 | **本仓 Coder390 EfficientThink 27B** 的 Q2 / Q3 GGUF（内置 Q4 MTP；走 llama.cpp，**不是 NInfer**；本次 Lynn 安装不含视觉组件） |

端侧硬件建议：Apple Silicon 看统一内存，NVIDIA 看单卡显存（不叠多卡、不用系统内存顶替）。**低于 14GiB 禁止安装**；**16GB 推荐 Q2**，**24GB 及以上推荐 Q3**。模型文件之外还需预留上下文缓存和运行缓冲。

工具参数由模型自己填写（地点、日期、联赛、行情代码、货币对等），不再从整句问题硬猜实体。长期记忆与写作 Diff 等桌面能力随 Lynn 提供；完整说明与更新见发布页。

- [V0.87.1 发布说明](https://github.com/MerkyorLynn/Lynn/releases/tag/v0.87.1)
- [国内下载页（推荐）](https://download.merkyorlynn.com/download.html)
- macOS Apple Silicon：[国内](https://download.merkyorlynn.com/downloads/Lynn-0.87.1-macOS-arm64.dmg) · [GitHub](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.1/Lynn-0.87.1-macOS-arm64.dmg)
- macOS Intel：[国内](https://download.merkyorlynn.com/downloads/Lynn-0.87.1-macOS-x64.dmg) · [GitHub](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.1/Lynn-0.87.1-macOS-x64.dmg)
- Windows：[国内](https://download.merkyorlynn.com/downloads/Lynn-0.87.1-Windows-Setup.exe) · [GitHub](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.1/Lynn-0.87.1-Windows-Setup.exe)

在 Lynn 里：**设置 → 模型 → 本地 Qwen3.8-27B → 选 Q2 / Q3 → 安装并启动**。本地档位只加载本仓库 `GGUF/` 下的 Q2 / Q3 LynnStyle-MTP 文件；NInfer / NVFP4 等其他格式请用对应引擎自行部署，不走 Lynn 一键安装。

## 量化档

| 档位 | 目录 | 说明 | 包大小(字节) | BPW | GPQA / MMLU / LCB |
|---|---|---|---:|---:|---|
| GGUF Q3 LynnStyle | `GGUF/` | llama.cpp 用混合精度 LynnStyle GGUF(`Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.gguf`):最低精度到 Q3;内置 **Q4 MTP**(不是 Q8);视觉用 `GGUF/` 内的 mmproj(llama.cpp `--mmproj`) | 17,303,770,432(约 16.1 GiB) | 5.07 | 173 / 449 / 92 |
| GGUF Q3 LynnStyle · NInfer | `GGUF-NInfer/` | 由同一份 Q3 LynnStyle GGUF 转换的 NInfer 包(`.ninfer`),内置 Q4_K MTP 与视觉;NInfer-all 与 ninfer-fusion-kvmem 均可;成绩在内置 MTP 前测得(外挂 Q8 MTP 草稿),量化权重相同,成绩在 llama.cpp 上测得 | 17,596,369,920(约 16.4 GiB) | 5.07 | 173 / 449 / 92 |
| GGUF Q3 LynnStyle · Q8MTP | `GGUF/` | 同一个 Q3 LynnStyle GGUF,只把内置 MTP 头改为 Q8_0(`Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf`),其他张量与原包逐字节相同;Q8_0 MTP 头备选版(原包的 Q4_0 MTP 头 llama.cpp 支持);llama.cpp 看图同样用 `GGUF/` 里的 mmproj | 17,516,107,072(约 16.3 GiB) | 5.13 | 173 / 449 / 92 |
| GGUF Q3 LynnStyle · Q8MTP · NInfer | `GGUF-NInfer/` | 由上面的 Q8MTP GGUF 转成的 NInfer 包(`Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.ninfer`),内置 Q8_0 MTP 头和视觉组件,model id `qwen3.8-27b-coder390-Q3LynnStyle-Q8Mtp`;主体权重与原 Q3 LynnStyle 包相同,分数沿用原包 | 17,808,706,560(约 16.6 GiB) | 5.13 | 173 / 449 / 92 |
| GGUF Q4 LynnStyle | `GGUF/` | llama.cpp 用混合精度 LynnStyle GGUF(`Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.gguf`):最低精度到 Q4;内置 **Q4 MTP**(不是 Q8);视觉用 `GGUF/` 内的 mmproj(llama.cpp `--mmproj`) | 19,620,406,592(约 18.3 GiB) | 5.75 | 175 / 448 / 89 |
| GGUF Q4 LynnStyle · NInfer | `GGUF-NInfer/` | 由同一份 Q4 LynnStyle GGUF 转换的 NInfer 包(`.ninfer`),内置 Q4_K MTP 与视觉;NInfer-all 与 ninfer-fusion-kvmem 均可;成绩在内置 MTP 前测得(外挂 Q8 MTP 草稿),量化权重相同,成绩在 llama.cpp 上测得 | 19,913,006,080(约 18.5 GiB) | 5.74 | 175 / 448 / 89 |
| GGUF Q4 LynnStyle · Q8MTP | `GGUF/` | 同一个 Q4 LynnStyle GGUF,只把内置 MTP 头改为 Q8_0(`Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf`),其他张量与原包逐字节相同;Q8_0 MTP 头备选版(原包的 Q4_0 MTP 头 llama.cpp 支持);llama.cpp 看图同样用 `GGUF/` 里的 mmproj | 19,832,743,232(约 18.5 GiB) | 5.81 | 175 / 448 / 89 |
| GGUF Q4 LynnStyle · Q8MTP · NInfer | `GGUF-NInfer/` | 由上面的 Q8MTP GGUF 转成的 NInfer 包(`Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer`),内置 Q8_0 MTP 头和视觉组件,model id `qwen3.8-27b-coder390-Q4LynnStyle-Q8Mtp`;主体权重与原 Q4 LynnStyle 包相同,分数沿用原包 | 20,125,342,720(约 18.7 GiB) | 5.81 | 175 / 448 / 89 |
| GGUF Q2 LynnStyle | `GGUF/` | llama.cpp 用混合精度 LynnStyle GGUF(`Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf`):最低精度到 Q2;内置 **Q4 MTP**(不是 Q8);视觉用 `GGUF/` 内的 mmproj(llama.cpp `--mmproj`) | 13,276,009,792(约 12.4 GiB) | 3.89 | 177 / 433 / 90 |
| GGUF Q2 LynnStyle · NInfer | `GGUF-NInfer/` | 由同一份 Q2 LynnStyle GGUF 转换的 NInfer 包(`.ninfer`),内置 Q4_K MTP 与视觉;NInfer-all 与 ninfer-fusion-kvmem 均可;成绩为 GGUF 在 llama.cpp 上测得 | 13,568,617,472(约 12.6 GiB) | 3.89 | 177 / 433 / 90 |
| GGUF Q2 LynnStyle · Q8MTP | `GGUF/` | 同一个 Q2 LynnStyle GGUF,只把内置 MTP 头改为 Q8_0(`Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf`),其他张量与原包逐字节相同;Q8_0 MTP 头备选版(原包的 Q4_0 MTP 头 llama.cpp 支持);llama.cpp 看图同样用 `GGUF/` 里的 mmproj | 13,488,346,432(约 12.6 GiB) | 3.95 | 177 / 433 / 90 |
| GGUF Q2 LynnStyle · Q8MTP · NInfer | `GGUF-NInfer/` | 由上面的 Q8MTP GGUF 转成的 NInfer 包(`Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.ninfer`),内置 Q8_0 MTP 头和视觉组件,model id `qwen3.8-27b-coder390-Q2LynnStyle-Q8Mtp`;主体权重与原 Q2 LynnStyle 包相同,分数沿用原包 | 13,780,954,112(约 12.8 GiB) | 3.95 | 177 / 433 / 90 |
| GGUF Q8_0 | `GGUF/` | llama.cpp 用 GGUF 单文件(`Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf`):主干 Q8_0,内置 MTP 头,不需要外挂草稿;llama.cpp 视觉用 `--mmproj GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` | 29,069,202,688(约 27.1 GiB) | 8.51 | 171 / 443 / 90 |
| GGUF Q8_0 · NInfer | `GGUF-NInfer/` | 由同一份 Q8_0 GGUF 转换的 NInfer 包(`.ninfer`),内置 MTP 头与视觉部分;仅 NInfer-all(`iamwavecut/ninfer-all`)可加载;成绩为同一份 GGUF 在 llama.cpp 上测得 | 29,361,802,240(约 27.3 GiB) | 8.51 | 171 / 443 / 90 |
| GGUF Q6_K | `GGUF/` | llama.cpp 用 GGUF 单文件(`Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`):主干 Q6_K + imatrix 校准,内置 Q8 MTP 头,不需要外挂草稿;llama.cpp 视觉用 `--mmproj GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` | 23,177,516,384(约 21.6 GiB) | 6.79 | 174 / 448 / 91 |
| GGUF Q6_K · NInfer | `GGUF-NInfer/` | 由同一份 GGUF 转换的 NInfer 包(`.ninfer`),主干量化相同,内置 MTP 头(attention/MLP 权重 Q6_K,输入投影 Q8_0);包内含视觉部分(加 `--vision` 可输入图片);仅 NInfer-all(`iamwavecut/ninfer-all`)可加载;成绩为同一份 GGUF 在 llama.cpp 上测得 | 23,379,962,880(约 21.8 GiB) | 6.76 | 174 / 448 / 91 |

**社区分支 ninfer-fusion-kvmem**:Q2～Q4 LynnStyle 的 NInfer 包(`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer`)内置 MTP 头已改为 Q4_K,在官方 NInfer-all master 和社区分支 ninfer-fusion-kvmem 上都能正常加载并开启 MTP(2026-10-11 实测)。`GGUF/` 下的 `.gguf` 内置 MTP 头仍为 Q4_0,llama.cpp 支持。Q8 MTP 版本继续保留作为备选(权重相同,只把 MTP 头改为 Q8_0):llama.cpp 用 `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf`、`GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf`、`GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf`;NInfer 用 `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer`(model id 分别为 `qwen3.8-27b-coder390-Q2LynnStyle-Q8Mtp`、`qwen3.8-27b-coder390-Q3LynnStyle-Q8Mtp`、`qwen3.8-27b-coder390-Q4LynnStyle-Q8Mtp`)。

**Q8 MTP 版本 · 检查**(2026-10-09,单张 RTX PRO 6000):NInfer-all `master`,`--spec mtp --draft-tokens 3 --vision`,int8 KV,上下文 8,192;llama.cpp 用 `--spec-type draft-mtp --spec-draft-n-max 4` 加 `--mmproj`;各发一个看图请求,短跑。所有运行看图都答对(llama.cpp 开关思考均答对)。

| 包 | NInfer decode tok/s | NInfer MTP 接受率(每轮 token 数) | llama.cpp decode tok/s | llama.cpp 草稿接受率 | 看图 |
|---|---:|---:|---:|---:|---|
| Q2 LynnStyle · Q8MTP | 211.7 | 64.2%(3.14) | 180.1 | 0.879 | 正确 |
| Q3 LynnStyle · Q8MTP | 134.9 | 51.7%(2.55) | 138.3 | 0.904 | 正确 |
| Q4 LynnStyle · Q8MTP | 154.8 | 71.0%(3.13) | 135.6 | 0.879 | 正确 |

GGUF Q3 LynnStyle 的 BPW 按 17303770432 × 8 ÷ 文本 + MTP 参数数 27,320,697,856 = 5.07;Q3 NInfer 加视觉前为 17300551168 字节、BPW 5.07。GGUF Q4 LynnStyle 的 BPW 按 19620406592 × 8 ÷ 文本 + MTP 参数数 27,320,697,856 = 5.75;Q4 NInfer 加视觉前为 19617187328 字节、BPW 5.74。GGUF Q2 LynnStyle 的 BPW 按 13,276,009,792 × 8 ÷ 文本 + MTP 参数数 27,320,697,856 = 3.89;Q2 NInfer 加视觉前为 13,272,798,720 字节、BPW 3.89。GGUF Q8_0 的 BPW 按 29,069,202,688 × 8 ÷ 文本 + MTP 参数数 27,320,697,856 = 8.51;Q8_0 NInfer 加视觉前为 29,065,983,488 字节、BPW 8.51。GGUF Q6_K 两个包的 BPW 按单个文件字节数 × 8 ÷ 文本 + MTP 参数数 27,320,697,856 计算:GGUF 为 23,177,516,384 字节、6.79,NInfer 加视觉前为 23,084,144,128 字节、6.76。参数数按 GGUF 头部统计(866 个张量:文本 26,895,998,464 + MTP 424,699,392);视觉不计入分母:llama.cpp 的外挂 mmproj 和现在打进每个 `.ninfer` 的视觉部分(295,720,448 字节)都不算。主仓库 BF16 / FP8 / NVFP4 各档按 27,781,427,952(含视觉塔)计算,分母不同,不宜直接横向比较 BPW。

## 最佳 TPS 推荐与并发推荐

测试环境:单张 RTX PRO 6000 Blackwell;1 分钟快测,生成上限 512,开思考(xhigh),采样 temperature 1.0、top_p 0.95、top_k 20;每档只发与并发数相同的请求数(C1 发 1 个、C2 发 2 个、C4 发 4 个、C8 发 8 个)。数字为总吞吐 tok/s(全部输出 token ÷ 墙钟时间)。这是快测:请求少、生成短,数字不能与其他口径的测速直接比较。NInfer 行用 `GGUF-NInfer/` 包测得,测速时服务参数为 `--max-context 32768 --kv-capacity 32768 --kv-dtype rk8v4 --max-concurrency 8`;llama.cpp 行用 `GGUF/` 包测得。

| 引擎 · 投机方式 | C1 | C2 | C4 | C8 |
|---|---:|---:|---:|---:|
| NInfer · Q8_0 MTP(草稿长度 4) | 109.5 | 未测 | 332.0 | **486.3** |
| NInfer · Q6_K MTP(草稿长度 3) | 131.9 | 161.9 | **235.5** | 388.1 |
| NInfer · 不开投机 | 56.0 | 93.9 | 162.1 | 298.1 |
| NInfer · Q3 LynnStyle MTP (4 draft,512 短测) | 167.4 | 179.8 | 285.1 | **512.3** |
| llama.cpp · Q3 LynnStyle MTP (4096 长测) | 78.5 | 161.6 | **191.8** | 未测 |
| NInfer · Q4 LynnStyle MTP (4 draft,512 短测) | 157.0 | 174.3 | 287.5 | **436.4** |
| llama.cpp · Q4 LynnStyle MTP (4096 长测) | 73.6 | 77.7 | **81.1** | 未测 |
| NInfer · Q2 LynnStyle MTP (4 draft) | 205.7 | 210.4 | 308.0 | **521.0** |
| llama.cpp · Q2 LynnStyle MTP | 104.9 | 167.6 | **174.8** | 未测 |
| llama.cpp · Q8_0 MTP | 85.3 | 133.6 | **190.8** | 未测 |
| llama.cpp · Q6_K MTP | 97.2 | 95.3 | 168.1 | 189.0 |
| llama.cpp · 不开投机 | 53.4 | 未测 | 123.0 | 未测 |

- **推荐(Q8)**:NInfer + C8 + MTP(486.3 tok/s)。Q6_K 仍推荐 NInfer + C4 + MTP(235.5 tok/s),与下文启动命令一致(`--max-concurrency 4`);只看总吞吐时 Q6_K 的 C8 更高(388.1 tok/s)。
- **MTP 已内置**:每个包都自带 MTP 头(Q2 / Q3 / Q4 LynnStyle 的 `.gguf` 为 Q4_0、`-Q4MTP.ninfer` 为 Q4_K,其 -Q8MTP 版为 Q8_0;Q6_K 的 GGUF 为 Q8_0,NInfer 的 attention/MLP 权重为 Q6_K),不需要外挂草稿模型。Q6_K 单请求时 NInfer 开 MTP 为 131.9 tok/s,约为 llama.cpp 不开投机(53.4 tok/s)的 2.5 倍;llama.cpp 开 MTP 时 C1 总吞吐 97.2 tok/s(单请求解码 119.0 tok/s)。

## 推荐启动脚本

### 量化方案

**GGUF Q6_K**(`GGUF/`、`GGUF-NInfer/`):主干 Q6_K,用 512 个分块(chunk)的 imatrix 校准,并做结构保护:线性注意力(SSM)的 `ssm_alpha` / `ssm_beta` 保持 BF16,词嵌入与输出头为 Q8_0,MTP 头(`blk.64` 的 attn q/k/v/output、ffn gate/up/down 与 `nextn.eh_proj`)全部为 Q8_0,其 norm 保持 F32。GGUF 共 866 个张量、65 个块(64 层主干 + 1 层 MTP)。`.ninfer` 由同一份 GGUF 转换,主干量化相同,其 MTP 的 attention/MLP 权重为 Q6_K(`gguf_q6_k`),仅 `mtp/input_projection` 为 Q8_0;GGUF 不含视觉权重(llama.cpp 用 `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`,加 `--mmproj`);`.ninfer` 包内已含视觉部分(加 `--vision`,见下文「NInfer · 视觉」)。

### 启动命令


`.ninfer` 用 NInfer-all(`iamwavecut/ninfer-all` 的 master 分支)加载:包里保留的是 GGUF 量化块,其他 NInfer 构建不能读。llama.cpp 需支持 `--spec-type draft-mtp` 的上游版本。NInfer 的 `--kv-capacity` 是所有请求共享的 KV 池;llama.cpp 的 `-c 409600 -np 4` 会把上下文平分给 4 个槽位,每个请求最多 102,400 token,够单请求写到 94K。对话接口为 `POST /v1/chat/completions`;NInfer 请求里的 `model` 要与 `--model-id` 一致。视觉:llama.cpp 用 `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`(`--mmproj`;629,247,008 字节,sha256 `cae9799dc9196449b0d83f716e64af89d5cf65147510462e5a629a2aa23adb32`)。每个 `.ninfer` 包内都含视觉部分;`ninfer-serve` 加 `--vision` 即可输入图片(见下文「NInfer · 视觉」)。

**16G 显存 / 单流推荐**：显存 16G、只需单路使用时，更推荐 `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer`。它是本仓最小的 NInfer 包（13,568,617,472 字节，约 12.6 GiB），内置 Q4_K MTP 头和视觉部分（加 `--vision` 即可看图，不需要 mmproj），官方 NInfer-all master 与社区分支 ninfer-fusion-kvmem 都能直接运行。16G 卡未实测，以上是按文件体积判断；上下文先从 32K 起，显存不够再调小。

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer \
  --model-id qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --max-context 32768 --kv-capacity 32768 --kv-dtype rk8v4 \
  --max-concurrency 1 --spec mtp --draft-tokens 4 --vision
```

**社区分支 ninfer-fusion-kvmem**:Q2～Q4 LynnStyle 的 NInfer 包(`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer`)内置 MTP 头已改为 Q4_K,在官方 NInfer-all master 和社区分支 ninfer-fusion-kvmem 上都能正常加载并开启 MTP(2026-10-11 实测)。`GGUF/` 下的 `.gguf` 内置 MTP 头仍为 Q4_0,llama.cpp 支持。Q8 MTP 版本继续保留作为备选(权重相同,只把 MTP 头改为 Q8_0):llama.cpp 用 `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf`、`GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf`、`GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf`;NInfer 用 `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer`(model id 分别为 `qwen3.8-27b-coder390-Q2LynnStyle-Q8Mtp`、`qwen3.8-27b-coder390-Q3LynnStyle-Q8Mtp`、`qwen3.8-27b-coder390-Q4LynnStyle-Q8Mtp`)。

**MTP 与 DFlash2**:本仓库所有 GGUF / NInfer 包都内置 MTP 头(Q2 / Q3 / Q4 LynnStyle 为内置 **Q4** MTP(`.gguf` 为 Q4_0,`-Q4MTP.ninfer` 为 Q4_K);其 `-Q8MTP` 版本为 Q8_0 MTP 头)。开启方式:NInfer 加 `--spec mtp --draft-tokens N`,llama.cpp 加 `--spec-type draft-mtp --spec-draft-n-max N`;省略这两个参数即不开投机。DFlash2 是外挂草稿模型,不在本仓库这些包里,本仓库不提供 GGUF / NInfer 用的 DFlash2 草稿;需要 DFlash2 时请用主仓 BF16 / FP8 / NVFP4 各档自带的 `DFlash2-FP8/`(SGLang `--speculative-algorithm DFLASH`)或 NVFP4-NInfer 仓库的 `.ninfer` 包(`--spec dflash2`)。MTP 与 DFlash2 互斥:同一个服务只能开其中一种,不要同时开。

#### NInfer

**NInfer · GGUF Q2 LynnStyle · MTP(草稿长度 4,推荐并发 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer \
  --model-id qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --kv-dtype rk8v4 \
  --max-concurrency 8 --spec mtp --draft-tokens 4
```

**NInfer · GGUF Q3 LynnStyle · MTP(草稿长度 4,推荐并发 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q3LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4
```

**NInfer · GGUF Q4 LynnStyle · MTP(草稿长度 4,推荐并发 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q4LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4
```

**NInfer · GGUF Q4 LynnStyle · Q8MTP · MTP(草稿长度 4,推荐并发 8)**:Q8_0 MTP 头备选(`-Q4MTP` 包在 NInfer-all 与 ninfer-fusion-kvmem 上也能用);Q2 / Q3 把文件名和 model id 里的 `Q4` 换成 `Q2` / `Q3`。

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q4LynnStyle-Q8Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4
```

**NInfer · GGUF Q6_K · MTP(草稿长度 3,推荐并发 4)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer \
  --model-id qwen3.8-27b-coder390-q6k-mtp \
  --max-context 102400 --kv-capacity 409600 --kv-dtype rk8v4 \
  --max-concurrency 4 --spec mtp --draft-tokens 3
```

**NInfer · GGUF Q8_0 · MTP(草稿长度 4,推荐并发 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer \
  --model-id qwen3.8-27b-coder390-q8-mtp \
  --max-context 102400 --kv-capacity 819200 --kv-dtype rk8v4 \
  --max-concurrency 8 --spec mtp --draft-tokens 4
```

不要用 `--max-context 131072 --kv-capacity 131072`(KV 池不够多请求排队时会 HTTP 503)。不要加 `--lm-head-q6` / `--embedding-q4`。需 NInfer-all 的 `ninfer-serve`;官方 ninfer-src 读不了 `gguf_blocks_v1`。

**NInfer · 视觉(图片输入)**

`GGUF-NInfer/` 里每个 `.ninfer` 都已打包视觉部分(295,720,448 字节,2026-10-09 加入)。视觉部分由 BF16 视觉权重按 NInfer 的视觉格式量化:patch embedding 为 Q6,attention q/k/v 与 MLP fc1 为 Q4,其余投影为 Q5,merger 为 Q8,norm 与 bias 保持 BF16。文本与 MTP 权重和之前逐字节相同。在上面任一 NInfer 命令后加 `--vision` 即可,不需要别的文件(单独的 `vision-bf16.safetensors` 用不到)。这些包内置 MTP 头,不含 DFlash2 草稿,所以每个包两条命令:不开投机、开 MTP。

```bash
# Q2LynnStyle · 不开投机
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --vision

# Q2LynnStyle · MTP(草稿长度 4)
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4 \
  --vision

# Q3LynnStyle · 不开投机
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q3LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --vision

# Q3LynnStyle · MTP(草稿长度 4)
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q3LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4 \
  --vision

# Q4LynnStyle · 不开投机
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q4LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --vision

# Q4LynnStyle · MTP(草稿长度 4)
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q4LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4 \
  --vision

# Q6_K · 不开投机
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-q6k-mtp \
  --max-context 102400 --kv-capacity 409600 --max-concurrency 4 \
  --kv-dtype rk8v4 \
  --vision

# Q6_K · MTP(草稿长度 3)
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-q6k-mtp \
  --max-context 102400 --kv-capacity 409600 --max-concurrency 4 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 3 \
  --vision

# Q8_0 · 不开投机
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-q8-mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --vision

# Q8_0 · MTP(草稿长度 4)
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-q8-mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4 \
  --vision
```

图片请求(按 OpenAI 格式放 `image_url`;`url` 填图片的 `http(s)://` 链接,也可以传本地图片的数据 URI;`model` 要与 `--model-id` 一致):

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.8-27b-coder390-Q4LynnStyle-Mtp",
    "messages": [{"role": "user", "content": [
      {"type": "image_url", "image_url": {"url": "https://example.com/demo.png"}},
      {"type": "text", "text": "Describe this image."}
    ]}],
    "max_tokens": 2048
  }'
```

图片按 OpenAI 格式放在 `POST /v1/chat/completions` 的 `image_url` 里。`--vision` 把视觉编码器放在 GPU 上;显存紧张时改用 `--vision-cpu`(在 CPU 上跑,单张图默认最多 256 个合并 token,可用 `--vision-max-merged` 调整)。不加 `--vision` 时和以前一样只跑文本。`GGUF-NInfer/vision-bf16.safetensors` 是视觉部分的 BF16 原始权重,NInfer 运行时不需要它。引擎实测(2026-10-09,单张 RTX PRO 6000):Q2 LynnStyle 包加 `--vision` 正确回答了看图问题;开 MTP、3 个草稿 token 时接受长度 3.00,decode 207 tok/s。Q3 / Q4 LynnStyle、Q6_K、Q8_0 包也已在 NInfer-all `master` 上开 MTP 加 `--vision` 实测,均回答正确(单次短测:Q4 151.9 tok/s、接受率 66.7%;Q6_K 131.1 tok/s、65.4%;Q8_0 121.5 tok/s、68.2%);Q8 MTP 版见上文「Q8 MTP 版本 · 检查」。

#### llama.cpp

**llama.cpp · GGUF Q2 LynnStyle · MTP(代表命令;换 `-m` 即可切到 Q3 / Q4 / Q6_K / Q8_0)**

```bash
llama-server -m ./GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf \
  -c 409600 -np 4 -ngl 99 --jinja \
  --host 127.0.0.1 --port 8080 \
  --alias qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --spec-type draft-mtp --spec-draft-n-max 4
```

换其他 GGUF 档只需改 `-m` 为 `...-Q3LynnStyle-MTP.gguf`、`...-Q4LynnStyle-MTP.gguf`、`...-Q6_K-MTP.gguf` 或 `...-Q8_0-MTP.gguf`(并相应改 `--alias`,例如 `qwen3.8-27b-coder390-q6k-mtp`、`qwen3.8-27b-coder390-q8-mtp`)。MTP 已融合进 GGUF(`blk.64`),不要再外挂 draft;日志应出现 `creating MTP draft context against the target model`。需要图像输入时加 `--mmproj ./GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`。

**llama.cpp · 视觉(图片输入)**

```bash
llama-server -m ./GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf \
  --mmproj ./GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf \
  -c 409600 -np 4 -ngl 99 --jinja \
  --host 127.0.0.1 --port 8080 \
  --alias qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --spec-type draft-mtp --spec-draft-n-max 4
```

GGUF 文件本身不含视觉权重,加 `--mmproj ./GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` 即可看图,八个 GGUF 都用这同一个 mmproj(按上文换 `-m` 和 `--alias`;已在 Q3 / Q4 LynnStyle、Q6_K、Q8_0 上实测看图)。去掉 `--spec-type` / `--spec-draft-n-max` 即不开投机。不加 `--mmproj` 时 llama.cpp 只跑文本。图片按 OpenAI 格式放在 `POST /v1/chat/completions` 的 `image_url` 里(请求与 NInfer 示例相同,`model` 填 `--alias`)。

**可选:外挂 Q8_0 MTP 草稿。** `GGUF/mtp-Qwen3.8-27B-Coder390-EfficientThink-Q8_0.gguf`(3,164,006,656 字节)是单独的 Q8_0 MTP 头,权重和 Q6_K、Q8_0 包里内置的 MTP 头相同。Q2、Q3、Q4 LynnStyle 自带的是更小的 Q4 MTP 头,想换成 Q8 头就加 `-md` 指向这个文件。Q6_K 和 Q8_0 已经内置 Q8 头,外挂没有额外收益。加了 `-md` 之后,日志应出现 `loading draft model`,而不是 `creating MTP draft context against the target model`。2026-10-09 在一台 RTX PRO 6000 上用 llama.cpp 实测：目标是 Q3 LynnStyle，`--spec-draft-n-max 4`，日志出现 `loading draft model`。贪心接受率 66.1%、110.2 tok/s；不加 `-md`、用内置 Q4 MTP 头是 66.0%、112.2 tok/s。temperature 1.0 时是 52.4%、94.4 tok/s，对照 51.9%、95.6 tok/s。12 条提示词输出一致，Q8 文件没有更快。

```bash
llama-server -m ./GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.gguf \
  -md ./GGUF/mtp-Qwen3.8-27B-Coder390-EfficientThink-Q8_0.gguf \
  -c 409600 -np 4 -ngl 99 --jinja \
  --host 127.0.0.1 --port 8080 \
  --alias qwen3.8-27b-coder390-Q3LynnStyle-Mtp \
  --spec-type draft-mtp --spec-draft-n-max 4
```

## 其他文件纵览

### `GGUF/`(含 Q3/Q4/Q2/Q8/Q6 包 + Q3/Q4/Q2 Q8MTP 包 + Q8 MTP 草稿 + mmproj + SHA256SUMS)

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.gguf` | 17,303,770,432 | `9985b3d41fc7dc0bb5d493f7523d4515504912a3a7fc830f66e0fd2f90f9fd95` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.gguf` | 19,620,406,592 | `56c7c605a59764d9f0bb645d4eb335f1574af2c9e74020386139597df0e872f5` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf` | 13,276,009,792 | `cad973b3b7cc0d86bd39968209268318a746673c12c9536e5c37408baa7b5e6e` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf` | 13,488,346,432 | `62fd6cf6079dfb02b3e3aab68e39b4cdc6a471a51a82b56c9a76068e961d8a4a` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf` | 17,516,107,072 | `2c74a65df9d229bfba2eb3a878a25b84d4035d1be4061c9a665af213d98cae58` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf` | 19,832,743,232 | `5e2a1784298f696cb38f063962da0ad4acd1fd020c6e7c6e520df54acf8f57eb` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf` | 29,069,202,688 | `b24e8c5fe3f2b282cce841400c740fcaca48afcdcf9e991f7bbe9a59a78cabfe` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf` | 23,177,516,384 | `302597c53d1b00f7230b53a8a050831390a4371e92a80c1ac644fa920af76ab1` |
| `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` | 629,247,008 | `cae9799dc9196449b0d83f716e64af89d5cf65147510462e5a629a2aa23adb32` |
| `GGUF/mtp-Qwen3.8-27B-Coder390-EfficientThink-Q8_0.gguf` | 3,164,006,656 | `50a030e852289eed86065e2e2de57d89241174e99faa2c1c2f06c29c270789ee` |
| `GGUF/SHA256SUMS` | 1,187 | `7677cef32b796c8c54d18592e8d198a14563a994496c8161b84ab7bdba30d183` |

### `GGUF-NInfer/`(含 Q3/Q4/Q2 -Q4MTP 包(Q4_K MTP 头) + Q8/Q6 + Q3/Q4/Q2 Q8MTP 包(Q8_0 MTP 头),均含视觉 + vision-bf16.safetensors(BF16 原始文件,运行时不需要) + SHA256SUMS)

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer` | 17,596,369,920 | `f1d4e45fb12db2a0b142c00badc14f1413869acbeb8b40bc0898c4f4610f322e` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer` | 19,913,006,080 | `e445a0a970ea10975858c6ee679741be0a119fc763c9d7fa23c3999094aa032b` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer` | 13,568,617,472 | `a6555ef4623fa0d0cc81a5674bff724c60bf69bdcd70dc6e5be97c4afbfab040` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.ninfer` | 13,780,954,112 | `993ff3e54f7bd697c2f88b62b9d00455fb95c095d7d99d4cd458868cf6b5c6d3` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.ninfer` | 17,808,706,560 | `815241ba4d8f62055720d8632617b24814da3bf881948867b8eb65dbccd4bdb3` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer` | 20,125,342,720 | `f88730f1fc8d65d720780da6b305e9c943c016f4660695923d7023eddd6b2fad` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer` | 29,361,802,240 | `8ace439259c8ade2b7dacee8aca92df62d7cc93d6c7d40ac026be797bb02a9c5` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer` | 23,379,962,880 | `60d7b3f4f79304e1ab1e22c161cdace29e7f8f9b8350755e4eab45e2d5e0d168` |
| `GGUF-NInfer/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `GGUF-NInfer/SHA256SUMS` | 1,082 | `7cb6f58402c7fc14b7740487407c285232a54989e3ad1ebf25892c597944af38` |

### `imatrix/`(GGUF imatrix 与校正集)

`imatrix/coder390-imatrix-calibration.txt` 是重算 GGUF 重要性矩阵(imatrix)用的校正文本:用本模型 RL 训练 rollout 的输入重新整理,1,368 条(171 道题 × 8),500,816 token。不含测评题(对照 MMLU、GPQA Diamond、LiveCodeBench 做 13-gram 重叠检查,命中 0 条)。功能上与发布 GGUF 时用的校正集等价,但不是同一个文件;原 imatrix 数据文件没有保留。`imatrix/coder390-imatrix.gguf` 是 2026-10-09 用这份校正集重新算出的 imatrix(本模型 BF16 GGUF,llama.cpp `71ad059`,`-c 512 --chunks 512`;496 个条目、512 个块,与发布 GGUF 的元数据一致),可直接传给 `llama-quantize --imatrix`。命令与一致性检查见 `imatrix/README.md`。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `imatrix/coder390-imatrix-calibration.txt` | 1,710,336 | `2113e4f3720c88621e05fc0424008d45bbb05d2ad338e082c6d52662c1f2ef94` |
| `imatrix/coder390-imatrix.gguf` | 27,300,160 | `be0924f24bd82c05b28da0c1d803ef29c1961f60bf9e978a16ffe746ee2adcf1` |
| `imatrix/SHA256SUMS` | 187 | `215787c717b8260885dd95af463c246a3e37a38aa05d1a1fb68c61261bd0dd37` |

### 校验

```bash
(cd GGUF && sha256sum -c SHA256SUMS)
(cd GGUF-NInfer && sha256sum -c SHA256SUMS)
(cd imatrix && sha256sum -c SHA256SUMS)
```

## 加载说明

- Q6_K:两个包主干量化相同(Q6_K + imatrix + 结构保护,见上文「量化方案」),都内置 MTP 头(GGUF `blk.64` 为 Q8_0;NInfer 的 MTP attention/MLP 权重为 Q6_K,输入投影为 Q8_0),不需要外挂草稿模型;推荐 NInfer + C4 + MTP。
- `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`:llama.cpp 直接加载,GGUF 架构为 `qwen35`,65 个块,最后一块(`blk.64`)为 MTP。
- `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer`:只能用 NInfer-all 加载;SGLang、vLLM、llama.cpp、transformers 都不能读。
- 视觉:llama.cpp 用 `--mmproj GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`(629,247,008 字节,sha256 `cae9799dc9196449b0d83f716e64af89d5cf65147510462e5a629a2aa23adb32`)。NInfer:每个 `.ninfer` 包内已含视觉部分,加 `--vision` 即可;`GGUF-NInfer/` 里的 `vision-bf16.safetensors`(921,497,224 字节,sha256 `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33`)是这部分的 BF16 原始权重,运行时不需要。
- 成绩在 llama.cpp 上用 GGUF 包测得;LCB 测评脚本与 NInfer 接口不兼容(收到的回复不是合法 JSON),属于测评脚本问题,不是模型质量问题,LCB 以 llama.cpp 为准。

## 已知局限

- GGUF Q6_K:GPQA 174 低于原版 Qwen3.8 27B(FP8)的 177;MMLU 思考长度按原文用 BF16 tokenizer 计数,LCB 没有保存思考原文,没有思考长度分位数;全量三联只在 GGUF(llama.cpp)上跑,NInfer 包未单独跑全量;速度为快测(每档请求数等于并发数,生成上限 512),不能与其他档直接比较;`GGUF/` 已提供 mmproj;看图已实测:llama.cpp + mmproj 在 Q3 / Q4 LynnStyle、Q6_K、Q8_0 上,NInfer `--vision` 在 Q2 / Q3 / Q4 LynnStyle、Q6_K、Q8_0 上。
- 成绩依赖上述口径(100K 上下文、94,208 生成上限、不计超时),不宜与其他口径直接比较;MMLU 有采样抖动。

## 许可证与致谢

本模型采用 Apache-2.0 许可证,遵循基座 Qwen3.8-27B 的许可。

感谢 Qwen 团队提供基座模型与官方 FP8 方案;感谢 Opus5.5、GPT6Astra、Grok4.7、DSV4Pro、K3 在出题、金标、教师轨迹、数据核对与 RLOO 价值评审中的工作;感谢 llama.cpp 与 NInfer 社区。
<!-- CARD_ZH_END -->
