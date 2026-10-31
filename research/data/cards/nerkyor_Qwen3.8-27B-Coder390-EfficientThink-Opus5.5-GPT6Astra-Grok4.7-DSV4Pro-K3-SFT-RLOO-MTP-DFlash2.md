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
- fp8
- bf16
- nvfp4
- modelopt
- quantization
- calibration
- static-quantization
- compressed-tensors
- gsq-rco
- gsq
- rco
- hessian
- imatrix
- block128
- mtp
- dflash2
- speculative-decoding
- multimodal
- sglang
- vllm
- gguf
- llama.cpp
---

![Coder390 FP8 vs. original FP8](assets/header-fp8-vs-base-en.png)

![NVFP4 · INT8 · NInfer](assets/coder390-nvfp4-int8-ninfer-en.png)

![GGUF](assets/coder390-gguf-en.png)

<!-- CARD_EN_START -->
# Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2

A model post-trained with several rounds of SFT and RLOO on top of [Qwen3.8-27B-EfficientThink-SFT-SimPO-DFlash2](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2), which is itself the official [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) post-trained with SFT and SimPO. It is built to fix the original model's habit of failing to stop: it already has an answer, yet keeps re-deriving until it hits the 94K cap with no final answer. This repository provides five safetensors tiers, **BF16**, **static FP8 Block128**, **NVFP4 W4A16**, **NVFP4 W4A4**, and **NVFP4 W4A4-W8A8** (mixed precision), all fully multimodal (text + image/video) with the official BF16 MTP bundled; all load in SGLang without patches, and the FP8 package is also smoke-tested on vLLM. It also has **NInfer W4A4 / W4A4-W8A8** (`NVFP4-NInfer/`), **INT4 W4A16** (`INT4/W4A16/`, text + image, vLLM), **INT8 W8A8** (`INT8/W8A8/`), **INT8 W8A16** (`INT8/W8A16/`, text + image), and **GGUF Q2 / Q3 / Q4 LynnStyle (plus Q8 MTP versions), Q6_K, and Q8_0** (`GGUF/`, `GGUF-NInfer/`, built-in MTP).

- **Far fewer 94K truncations**: under the same protocol, 4 → 1 on GPQA and 13 → 3 on LCB.
- **No regression on any suite**: GPQA **178/198**, MMLU **450/500**, LCB **90/100** (static FP8), vs. 177 / 444 / 83 for the original FP8.
- **Lossless quantization**: GPQA and LCB are identical across BF16, dynamic FP8, and static FP8.
- **Two speculative-decoding options (mutually exclusive)**: about 180 tok/s per request with DFlash2 and 91 tok/s with MTP, vs. about 46 tok/s without speculation.

**Related repositories**

- GGUF / GGUF-NInfer (llama.cpp, NInfer, built-in MTP): [Hugging Face](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-GGUF-NInfer) · [ModelScope](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-GGUF-NInfer)
- NVFP4-NInfer: [Hugging Face](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-NVFP4-NInfer) · [ModelScope](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-NVFP4-NInfer)

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
| MTP / DFlash2 | Bundled BF16 MTP head / companion DFlash2 speculative-decoding draft |

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

**Result**: under the same protocol, 94K truncations drop from 4 to 1 on GPQA and from 13 to 3 on LCB (FP8) compared with the original Qwen3.8 27B (FP8), and none of the three scores falls below it (all FP8 figures; see the NVFP4 scores below).

## Scores

**Protocol**: the same Coder390 merged weights; two RTX PRO 6000 GPUs, C8 per GPU, 100K context, 94,208-token generation cap, no client-side timeout, DFlash2 draft, SGLang; full GPQA 198, MMLU 500, and LCB 100. Empty answers count as wrong, truncated-but-correct answers count as correct, and every failed sample stays in the denominator.

| Suite | Original Qwen3.8 27B (FP8) | BF16 | Dynamic FP8 | Static FP8 |
|---|---:|---:|---:|---:|
| GPQA | 177/198 | 178/198 | 178/198 | **178/198** |
| MMLU | 444/500 | 446/500 | 445/500 | **450/500** |
| LCB | 83/100 | 90/100 | 90/100 | **90/100** |

GPQA and LCB are identical across all three precisions. MMLU varies between 445 and 450, which is sampling noise rather than a precision effect. Dynamic FP8 means online FP8 quantization of the BF16 weights at inference time; it is not shipped as a separate package.

### All tiers: scores, reasoning length, 94K truncation, and empty answers

Reasoning length is `usage.reasoning_tokens`; a 94K truncation means the output hit the generation cap. LCB empty answers are the number of problems for which no runnable code could be extracted. The original, BF16, dynamic FP8, and static FP8 rows use two RTX PRO 6000 GPUs with C8 per GPU; the three NVFP4 tiers use a single RTX PRO 6000 at C8; the rest of the protocol is the same.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | Original Qwen3.8 27B (FP8) | 177/198 | 5,299 / 12,607 / 50,577 | 4 | 3 |
| GPQA | BF16 | **178/198** | **3,196** / **8,200** / **28,417** | **2** | **2** |
| GPQA | Dynamic FP8 | **178/198** | **2,815** / **8,371** / **27,744** | **1** | **1** |
| GPQA | Static FP8 | **178/198** | **2,966** / **7,832** / **26,431** | **1** | **2** |
| GPQA | NVFP4 W4A16 | 170/198 | **2,965** / **9,667** / **28,433** | **2** | 3 |
| GPQA | NVFP4 W4A4 | 167/198 | **2,876** / **10,996** / **31,986** | **2** | 3 |
| GPQA | NVFP4 W4A4-W8A8 | 172/198 | **2,953** / **10,010** / **35,731** | **2** | 4 |
| MMLU | Original Qwen3.8 27B (FP8) | 444/500 | 205 / 373 / 1,622 | 1 | 0 |
| MMLU | BF16 | **446/500** | **154** / **252** / **779** | 1 | 0 |
| MMLU | Dynamic FP8 | **445/500** | **138** / **271** / **881** | 1 | 0 |
| MMLU | Static FP8 | **450/500** | **154** / **279** / **937** | 1 | 0 |
| MMLU | NVFP4 W4A16 | 439/500 | **159** / **277** / **1,061** | 1 | 0 |
| MMLU | NVFP4 W4A4 | 440/500 | **168** / **306** / **967** | 2 | 0 |
| MMLU | NVFP4 W4A4-W8A8 | 442/500 | **157** / **273** / **778** | **0** | 0 |
| LCB | Original Qwen3.8 27B (FP8) | 83/100 | 8,388 / 24,241 / 94,208 | 13 | 13 |
| LCB | BF16 | **90/100** | **5,073** / **16,033** / **38,911** | **2** | **2** |
| LCB | Dynamic FP8 | **90/100** | **4,791** / **15,866** / **41,168** | **4** | **4** |
| LCB | Static FP8 | **90/100** | **4,511** / **16,027** / **43,992** | **3** | **3** |
| LCB | NVFP4 W4A16 | **91/100** | **5,119** / **15,790** / **47,768** | **4** | **3** |
| LCB | NVFP4 W4A4 | **92/100** | **6,338** / **15,771** / **54,096** | **3** | **3** |
| LCB | NVFP4 W4A4-W8A8 | **88/100** | **4,731** / **15,122** / **41,344** | **2** | **1** |

Bold marks values better than the original Qwen3.8 27B (FP8): a higher score, or lower P50 / P70 / P90, 94K truncations, or empty answers; values equal to or worse than the original are not bolded.

LCB improves the most: all 13 of the original's 94K truncations ended with empty code (13 truncations, 13 empty answers), and the Coder390 tiers cut this to 2–4. The 3 for W4A4 are problems 0, 53, and 96 (problem ids in the score file), likewise truncated with no code; of the 4 for W4A16, problems 6, 7, and 54 have no code, and problem 53 has 20 characters of code but is wrong; of the 2 for W4A4-W8A8, problem 11 has no code, and problem 6 has 2,338 characters of code but is wrong. On GPQA the original had 4 truncations at the 94K cap and the tiers have 1–2; on MMLU the original had 1 and the tiers have 0–2, with no clear change.

<details open>
<summary>Details for six precisions (bucketed by reasoning length)</summary>

Buckets are "correct / questions in bucket", split by reasoning length, left-closed and right-open.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty | <2K | 2–12K | 12–24K | 24–48K | ≥48K |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| GPQA | BF16 | 178/198 | 3,196 / 8,200 / 28,417 | 2 | 2 | 80/85 | 66/68 | 17/20 | 12/18 | 3/7 |
| GPQA | Dynamic FP8 | 178/198 | 2,815 / 8,371 / 27,744 | 1 | 1 | 78/81 | 68/70 | 18/21 | 11/17 | 3/9 |
| GPQA | Static FP8 | 178/198 | 2,966 / 7,832 / 26,431 | 1 | 2 | 82/84 | 68/74 | 17/19 | 9/17 | 2/4 |
| GPQA | NVFP4 W4A16 | 170/198 | 2,965 / 9,667 / 28,433 | 2 | 3 | 77/80 | 64/70 | 17/21 | 8/17 | 4/10 |
| GPQA | NVFP4 W4A4 | 167/198 | 2,876 / 10,996 / 31,986 | 2 | 3 | 76/82 | 58/60 | 20/23 | 12/26 | 1/7 |
| GPQA | NVFP4 W4A4-W8A8 | 172/198 | 2,953 / 10,010 / 35,731 | 2 | 4 | 79/82 | 58/63 | 19/22 | 14/22 | 2/9 |
| MMLU | BF16 | 446/500 | 154 / 252 / 779 | 1 | 0 | 432/472 | 13/23 | 1/3 | 0/0 | 0/2 |
| MMLU | Dynamic FP8 | 445/500 | 138 / 271 / 881 | 1 | 0 | 436/477 | 8/21 | 0/1 | 0/0 | 1/1 |
| MMLU | Static FP8 | 450/500 | 154 / 279 / 937 | 1 | 0 | 435/469 | 13/27 | 2/3 | 0/0 | 0/1 |
| MMLU | NVFP4 W4A16 | 439/500 | 159 / 277 / 1,061 | 1 | 0 | 427/471 | 11/26 | 0/1 | 1/1 | 0/1 |
| MMLU | NVFP4 W4A4 | 440/500 | 168 / 306 / 967 | 2 | 0 | 426/469 | 13/28 | 0/1 | 0/0 | 1/2 |
| MMLU | NVFP4 W4A4-W8A8 | 442/500 | 157 / 273 / 778 | 0 | 0 | 432/477 | 8/20 | 1/2 | 1/1 | 0/0 |
| LCB | BF16 | 90/100 | 5,073 / 16,033 / 38,911 | 2 | 2 | 40/40 | 25/26 | 11/14 | 9/11 | 5/9 |
| LCB | Dynamic FP8 | 90/100 | 4,791 / 15,866 / 41,168 | 4 | 4 | 38/39 | 25/26 | 11/14 | 12/13 | 4/8 |
| LCB | Static FP8 | 90/100 | 4,511 / 16,027 / 43,992 | 3 | 3 | 39/39 | 24/26 | 13/13 | 12/14 | 2/8 |
| LCB | NVFP4 W4A16 | 91/100 | 5,119 / 15,790 / 47,768 | 4 | 3 | 38/38 | 26/27 | 13/13 | 10/12 | 4/10 |
| LCB | NVFP4 W4A4 | 92/100 | 6,338 / 15,771 / 54,096 | 3 | 3 | 33/33 | 30/31 | 9/11 | 13/14 | 7/11 |
| LCB | NVFP4 W4A4-W8A8 | 88/100 | 4,731 / 15,122 / 41,344 | 2 | 1 | 40/41 | 21/24 | 16/16 | 7/10 | 4/9 |

</details>

### NVFP4 tiers

**Protocol**: one RTX PRO 6000, C8, 100K context, 94,208-token generation cap, no client-side timeout, DFlash2 draft, SGLang; full GPQA 198, MMLU 500, and LCB 100.

| Suite | NVFP4 W4A16 | NVFP4 W4A4 | NVFP4 W4A4-W8A8 |
|---|---:|---:|---:|
| GPQA | 170/198 | 167/198 | 172/198 |
| MMLU | 439/500 | 440/500 | 442/500 |
| LCB | 91/100 | 92/100 | 88/100 |

Reasoning length, 94K truncations, and empty answers for the three NVFP4 tiers are in the "All tiers" table above. LCB correctness is judged by each problem's `pass` field. Raw records: `evaluation/SCORES_NVFP4_W4A16.json`, `evaluation/SCORES_NVFP4_W4A4.json`, and `evaluation/SCORES_NVFP4_MIXED.json` (the W4A4-W8A8 tier).

### NInfer tiers: scores, reasoning length, 94K truncations, and empty answers

**Protocol**: scores carried over from the official triad run on 2026-10-05 on the same NInfer text path; one RTX PRO 6000, official NInfer engine (`Neroued/ninfer`), C8, 100K context, 94,208 generation cap, client not timed, **no speculation**; full GPQA 198 / MMLU 500 / LCB 100; empty answers count as wrong, truncations that still answer correctly count as correct, and every failure stays in the denominator. The packages uploaded now add a Q8 MTP head, the DFlash2 draft, and the proposal head on top of that text path; the text path is unchanged and the full triad was not re-run. Only the NInfer engine can load `.ninfer`; SGLang / vLLM / llama.cpp / transformers cannot.

Reasoning length is `usage.reasoning_tokens` (i.e. `completion_tokens_details.reasoning_tokens`); a 94K truncation means the generation cap was hit. LCB empty answers are the number of problems for which no runnable code could be extracted. Bold means better than the original Qwen3.8 27B (FP8).

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | NInfer W4A4 | 177/198 | **2,934** / **7,646** / **25,804** | **2** | **2** |
| GPQA | NInfer W4A4-W8A8 | 177/198 | **3,176** / **8,844** / **24,804** | **2** | **2** |
| MMLU | NInfer W4A4 | **449/500** | **164** / **285** / **830** | **0** | 0 |
| MMLU | NInfer W4A4-W8A8 | 444/500 | **163** / **281** / **923** | **0** | 0 |
| LCB | NInfer W4A4 | **89/100** | **3,994** / **15,533** / **36,125** | **2** | **2** |
| LCB | NInfer W4A4-W8A8 | **92/100** | **4,046** / **15,829** / **40,479** | **2** | **3** |

For NInfer W4A4, the 2 LCB empty answers are problems 11 and 15, both truncated with no code; the 2 GPQA empty answers are problems 79 and 127, both truncated with an empty pred. MMLU has no truncations and no empty answers. For NInfer W4A4-W8A8, the 3 LCB empty answers are problems 17, 53, and 54 (problem 17 stopped normally with no code; 53 and 54 were truncated with no code); the 2 GPQA empty answers are problems 79 and 127, both truncated with an empty pred. MMLU has no truncations and no empty answers.

<details open>
<summary>Details for the two NInfer tiers (by reasoning-length bucket)</summary>

Buckets are "correct / problems in bucket", half-open on the left.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty | <2K | 2–12K | 12–24K | 24–48K | ≥48K |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| GPQA | NInfer W4A4 | 177/198 | 2,934 / 7,646 / 25,804 | 2 | 2 | 76/83 | 69/71 | 17/22 | 14/19 | 1/3 |
| GPQA | NInfer W4A4-W8A8 | 177/198 | 3,176 / 8,844 / 24,804 | 2 | 2 | 79/82 | 70/74 | 13/21 | 12/16 | 3/5 |
| MMLU | NInfer W4A4 | 449/500 | 164 / 285 / 830 | 0 | 0 | 438/480 | 11/19 | 0/1 | 0/0 | 0/0 |
| MMLU | NInfer W4A4-W8A8 | 444/500 | 163 / 281 / 923 | 0 | 0 | 435/478 | 8/21 | 1/1 | 0/0 | 0/0 |
| LCB | NInfer W4A4 | 89/100 | 3,994 / 15,533 / 36,125 | 2 | 2 | 40/41 | 21/23 | 12/14 | 13/16 | 3/6 |
| LCB | NInfer W4A4-W8A8 | 92/100 | 4,046 / 15,829 / 40,479 | 2 | 3 | 38/38 | 26/26 | 14/16 | 11/12 | 3/8 |

</details>

### INT4 W4A16: scores, 94K truncations, and empty answers

**Protocol**: one RTX PRO 6000, vLLM 0.28, C8, 100K context, 94,208 generation cap, client not timed, reasoning effort xhigh, **MTP speculation with 3 draft tokens** (built-in head), `--reasoning-parser qwen3`; full GPQA 198 / MMLU 500 / LCB 100; empty answers count as wrong, truncations that still answer correctly count as correct, and every failure stays in the denominator. The run was paused on 2026-10-09 and resumed with the same server settings; finished problems were kept.

A 94K truncation means the generation cap was hit. LCB empty answers are the number of problems for which no runnable code could be extracted. Bold means better than the original Qwen3.8 27B (FP8); its numbers are in the all-tier table above.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | INT4 W4A16 | 177/198 | **3,136** / **8,115** / **27,856** | **1** | **1** |
| MMLU | INT4 W4A16 | **446/500** | **176** / **322** / **1,098** | **0** | 0 |
| LCB | INT4 W4A16 | **87/100** | **4,494** / **19,046** / **36,053** | **2** | **2** |

Reasoning lengths come from `usage.reasoning_tokens` returned by vLLM. GPQA: 1 truncation (problem 79), 1 empty answer (problem 79). MMLU has no truncations and no empty answers. LCB: 2 truncations (problem atcoder:arc182_e:6, atcoder:arc195_d:54), 2 empty answers (problem atcoder:arc182_e:6, atcoder:arc195_d:54). By difficulty, LCB is hard 37/46, medium 27/31, and easy 23/23. Mean MTP accept length over the run (vLLM log, 3 draft tokens): 2.81.

### INT8 W8A8: scores, 94K truncations, and empty answers

**Protocol**: one RTX PRO 6000, vLLM 0.28, C8, 100K context, 94,208 generation cap, client not timed, **no speculation**, reasoning effort xhigh; full GPQA 198 / MMLU 500 / LCB 100; empty answers count as wrong, truncations that still answer correctly count as correct, and every failure stays in the denominator. INT8 W8A8 loads only in vLLM.

A 94K truncation means the generation cap was hit. LCB empty answers are the number of problems for which no runnable code could be extracted. Bold means better than the original Qwen3.8 27B (FP8); its numbers are in the all-tier table above.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | INT8 W8A8 | 175/198 | **3,862** / **9,055** / **25,299.5** | **1** | **1** |
| MMLU | INT8 W8A8 | **450/500** | **156** / **291** / **864.4** | **0** | 0 |
| LCB | INT8 W8A8 | **91/100** | — | **2** | **0** |

Note: the INT8 W8A8 eval ran vLLM without a reasoning parser, so `usage.reasoning_tokens` is 0 throughout and reasoning plus answer were returned as content. GPQA and MMLU reasoning lengths were recounted from the raw text: the text before `</think>` in the content, counted with the BF16 tokenizer (the same method as the GGUF tiers). The LCB result file kept only the code, not the reasoning text, so it cannot be counted; that cell reads "—".

GPQA's 1 truncation is problem 127, with an empty pred, so it also counts as the empty answer. LCB's 2 truncations are problems 7 and 53: problem 7 left code that raised a runtime error and was judged wrong; problem 53 was truncated, but its code was still judged correct; LCB has no empty answers. MMLU has no truncations and no empty answers. By difficulty, LCB is hard 38/46, medium 30/31, and easy 23/23.

### INT8 W8A16: scores, 94K truncations, and empty answers

**Protocol**: one RTX PRO 6000, vLLM 0.28, C8, 100K context, 94,208 generation cap, client not timed, reasoning effort xhigh, **MTP speculation with 3 draft tokens** (external draft `INT8/W8A16/MTP-BF16/`), `--reasoning-parser qwen3`; full GPQA 198 / MMLU 500 / LCB 100; empty answers count as wrong, truncations that still answer correctly count as correct, and every failure stays in the denominator. INT8 W8A16 loads only in vLLM (pack-quantized GPTQ W8A16). Vision and MTP smoke-tested on the same stack (MTP mean accept length 3.31; image OCR correct with and without thinking).

A 94K truncation means the generation cap was hit. LCB empty answers are the number of problems for which no runnable code could be extracted. Bold means better than the original Qwen3.8 27B (FP8); its numbers are in the all-tier table above.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | INT8 W8A16 | 170/198 | **3,203** / **7,999** / **27,188** | **1** | **1** |
| MMLU | INT8 W8A16 | **449/500** | **162** / **287** / **876** | **0** | 0 |
| LCB | INT8 W8A16 | **94/100** | **5,422** / **17,884** / **39,584** | **1** | **1** |

Reasoning lengths come from `usage.reasoning_tokens` returned by vLLM. GPQA: 1 truncation (problem 79), 1 empty answer (problem 79). MMLU has no truncations and no empty answers. LCB: 1 truncation (atcoder:arc195_d:54), 1 empty answer (atcoder:arc195_d:54). By difficulty, LCB is easy 23/23, medium 31/31, hard 40/46.

Same-protocol TPS / concurrency tables will be added after the speed harness finishes; smoke decode was ~119 tok/s wall with MTP+vision on a short prompt.

### GGUF Q2 / Q3 / Q4 LynnStyle: scores, reasoning length, 94K truncations, and empty answers

**Protocol**: one RTX PRO 6000, llama.cpp (`llama-server`), C4, about 100K context per slot, 94,208 generation cap, client not timed, thinking on; full GPQA 198 / MMLU 500 / LCB 100; empty answers count as wrong, truncations that still answer correctly count as correct, and every failure stays in the denominator. Scored before the built-in MTP head was attached (external Q8 MTP draft); same quantized weights. The matching `.ninfer` packages under `GGUF-NInfer/` are converted from the same GGUFs; the full triad was run only on the GGUF.

A 94K truncation means the generation cap was hit. LCB empty answers are the number of problems for which no runnable code could be extracted. Bold means better than the original Qwen3.8 27B (FP8); its numbers are in the all-tier table above.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | GGUF Q2 LynnStyle | 177/198 | **2,989.5** / **8,923.8** / **27,156.1** | **3** | **0** |
| MMLU | GGUF Q2 LynnStyle | 433/500 | **181** / **326.3** / **1,020.5** | 1 | 0 |
| LCB | GGUF Q2 LynnStyle | **90/100** | **5,656.5** / **17,835.8** / **40,067.3** | **1** | **1** |
| GPQA | GGUF Q3 LynnStyle-16G | 172/198 | **3,811** / **11,404** / **31,418** | **2** | **2** |
| MMLU | GGUF Q3 LynnStyle-16G | 427/500 | **190** / **361** / 1,665 | **0** | 0 |
| LCB | GGUF Q3 LynnStyle-16G | **90/100** | **6,520** / **21,586** / **43,184** | **3** | **3** |
| GPQA | GGUF Q3 LynnStyle | 173/198 | **3,125.5** / **7,265.2** / **24,343.1** | **1** | **1** |
| MMLU | GGUF Q3 LynnStyle | **449/500** | **148** / **279.3** / **923.4** | **0** | 0 |
| LCB | GGUF Q3 LynnStyle | **92/100** | **4,421** / **14,232.2** / **34,946** | **1** | **1** |
| GPQA | GGUF Q4 LynnStyle | 175/198 | **2,951.0** / **8,159.3** / **25,649.0** | **1** | **2** |
| MMLU | GGUF Q4 LynnStyle | **448/500** | **164** / **312.9** / **1,077.7** | **0** | 0 |
| LCB | GGUF Q4 LynnStyle | **89/100** | **3,669.5** / **14,810.5** / **38,182.1** | **2** | **2** |

Note: reasoning lengths are counted from the raw text with the BF16 tokenizer (GPQA/LCB: `reasoning` field; MMLU: text before the last line of `response`), not from the API `reasoning_tokens`.

### GGUF Q6_K: scores, reasoning length, 94K truncations, and empty answers

**Protocol**: one RTX PRO 6000, llama.cpp (`llama-server`) loading `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`, C4, 100K context, 94,208 generation cap, client not timed, reasoning effort xhigh; full GPQA 198 / MMLU 500 / LCB 100; empty answers count as wrong, truncations that still answer correctly count as correct, and every failure stays in the denominator. `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer` is converted from the same GGUF with the same backbone quantization; the full triad was run only on the GGUF.

Reasoning length is `usage.reasoning_tokens`; a 94K truncation means the generation cap was hit. LCB empty answers are the number of problems for which no runnable code could be extracted. Bold means better than the original Qwen3.8 27B (FP8); its numbers are in the all-tier table above.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | GGUF Q6_K | 174/198 | **3,683** / **9,814** / **27,966** | **2** | **2** |
| MMLU | GGUF Q6_K | **448/500** | **162** / **310.3** / **939.4** | **0** | 0 |
| LCB | GGUF Q6_K | **91/100** | — | **0** | **1** |

Note: for MMLU and LCB, llama.cpp did not return reasoning tokens separately (`usage` has no `reasoning_tokens`). MMLU reasoning length is the text before the last line of `response`, counted with the BF16 tokenizer (the same method as Q8_0); the LCB result file kept no reasoning text, so it cannot be counted and reads "—". GPQA reasoning tokens were counted separately by the eval script.

GPQA's 2 truncations are problems 79 and 127; both hit 94,208 with an empty pred, so they also count as the empty answers. MMLU has no truncations and no empty answers.

LCB has no 94K truncations; its 1 empty answer is problem 92, which stopped normally without producing code.

LCB is scored on llama.cpp: the LCB eval script gets replies from NInfer that are not valid JSON. This is a compatibility issue between the eval script and the API, not a model-quality issue; the same GGUF on llama.cpp passed every problem in the same spot-check batch.


### GGUF Q8_0: scores, reasoning length, 94K truncations, and empty answers

**Protocol**: single RTX PRO 6000, llama.cpp (`llama-server`) loading `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf`, C4, 100K context, generation cap 94,208, no client timeout, thinking xhigh; full GPQA 198 / MMLU 500 / LCB 100; empty answers count as wrong; truncated-but-correct counts as correct. `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer` is converted from the same GGUF; the full triad was run on GGUF only.

Reasoning length: GPQA from `usage.reasoning_tokens`; MMLU from text before the last newline of `response`, counted with the BF16 tokenizer; LCB from saved `reasoning` text. 94K truncation means hitting the generation cap. LCB empty means no runnable code was extracted. Bold beats original Qwen3.8 27B (FP8).

| Bench | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | GGUF Q8_0 | 171/198 | **3,102.5** / **7,971** / **28,891.6** | **2** | **0** |
| MMLU | GGUF Q8_0 | 443/500 | **164** / **291** / **741** | **0** | 0 |
| LCB | GGUF Q8_0 | **90/100** | **4,098.5** / **16,087.8** / **39,135.5** | **3** | **3** |

GPQA: 2 truncations, 0 empty. MMLU: 0 / 0. LCB: 3 truncations, 3 empty (length with no code).

LCB is scored on llama.cpp: the LCB harness gets non-JSON replies from NInfer — a harness issue, not model quality.


## Run this model in Lynn desktop Agent (V0.87.4)

[Lynn](https://github.com/MerkyorLynn/Lynn) is an open-source desktop AI Agent (GUI + standalone CLI): chat, search, file edits, coding, and realtime voice in one app, or as a headless worker for other tools and CI. **Free. Quick Start needs no configuration and no API key.**

Current defaults (V0.87.4):

| Role | Stack |
|---|---|
| Cloud chat / coding / tools | **Step 5 Preview** (native vision — send images directly) |
| Realtime voice | **StepAudio 2.5 Realtime** |
| On-device local | **This Coder390 EfficientThink 27B** Q2 / Q3 GGUF (built-in Q4 MTP; llama.cpp — **not NInfer**; this Lynn install ships **no vision** component) |

Hardware guidance: Apple Silicon uses unified memory; NVIDIA uses the largest single GPU VRAM (not summed GPUs, not host RAM). **Install is blocked below 14GiB.** Prefer **Q2 at 16GB**, **Q3 at 24GB+**. Leave headroom for KV cache and runtime buffers beyond the GGUF file size.

Tool arguments (places, dates, leagues, tickers, currency pairs, and so on) are filled by the model rather than guessed from the whole user sentence. Desktop features such as long-term memory and writing Diff ship with Lynn; see the release notes for the full changelog.

- [V0.87.4 release notes](https://github.com/MerkyorLynn/Lynn/releases/tag/v0.87.4)
- [China download page (recommended)](https://download.merkyorlynn.com/download.html)
- macOS Apple Silicon: [mirror](https://download.merkyorlynn.com/downloads/Lynn-0.87.4-macOS-arm64.dmg) · [GitHub](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.4/Lynn-0.87.4-macOS-arm64.dmg)
- macOS Intel: [mirror](https://download.merkyorlynn.com/downloads/Lynn-0.87.4-macOS-x64.dmg) · [GitHub](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.4/Lynn-0.87.4-macOS-x64.dmg)
- Windows: [mirror](https://download.merkyorlynn.com/downloads/Lynn-0.87.4-Windows-Setup.exe) · [GitHub](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.4/Lynn-0.87.4-Windows-Setup.exe)

In Lynn: **Settings → Models → Local Qwen3.8-27B → pick Q2 / Q3 → Install & start**. Local tiers load only the Q2 / Q3 LynnStyle-MTP files under this repo’s `GGUF/` directory. NInfer / NVFP4 and other formats stay outside Lynn’s one-click install — use their own engines.

## Quantization tiers

| Tier | Directory | Notes | Package size (bytes) | BPW | GPQA / MMLU / LCB |
|---|---|---|---:|---:|---|
| BF16 | `BF16/` | Fully multimodal, original config, official BF16 MTP bundled, DFlash2 draft included, no patches needed | 55,583,125,732 (≈51.8 GiB) | 16.00 | 178 / 446 / 90 |
| Static FP8 Block128 | `FP8/` | Fully multimodal, official BF16 MTP bundled, DFlash2 draft included | 33,669,220,491 (≈31.4 GiB) | 9.00 | 178 / 450 / 90 |
| NVFP4 W4A16 | `NVFP4/W4A16/` | Fully multimodal, language-model Linear layers with NVFP4 weights + BF16 activations, official BF16 MTP bundled, DFlash2 draft included, no patches needed in SGLang | 20,613,406,953 (≈19.2 GiB, excluding the draft) | 5.93 | 170 / 439 / 91 |
| NVFP4 W4A4 | `NVFP4/W4A4/` | Fully multimodal, language-model Linear layers with NVFP4 weights + NVFP4 activations, official BF16 MTP bundled, DFlash2 draft included, no patches needed in SGLang | 20,613,386,462 (≈19.2 GiB, excluding the draft) | 5.93 | 167 / 440 / 92 |
| NVFP4 W4A4-W8A8 | `NVFP4/W4A4-W8A8/` | Fully multimodal, language-model MLP layers in NVFP4 W4A4 and attention / linear-attention projections in FP8 W8A8, official BF16 MTP bundled, DFlash2 draft included, no patches needed in SGLang | 23,769,634,648 (≈22.1 GiB, excluding the draft) | 6.84 | 172 / 442 / 88 |
| NInfer W4A4 | `NVFP4-NInfer/W4A4/` | Official NInfer package (`.ninfer`), W4A4 text path with a Q8 MTP head, the DFlash2 draft, the proposal head, and the vision component built in (image input with `--vision`); loadable only by the official NInfer engine (`Neroued/ninfer`) | 23,773,675,264 (≈22.1 GiB) | 6.76 | 177 / 449 / 89 |
| NInfer W4A4-W8A8 | `NVFP4-NInfer/W4A4-W8A8/` | Official NInfer mixed-precision package (`.ninfer`), W4A4-W8A8 text path with a Q8 MTP head, the DFlash2 draft, the proposal head, and the vision component built in (image input with `--vision`); loadable only by the official NInfer engine (`Neroued/ninfer`) | 23,773,675,264 (≈22.1 GiB) | 6.76 | 177 / 444 / 92 |
| INT4 W4A16 | `INT4/W4A16/` | Text + image (`Qwen3_5ForConditionalGeneration`): GPTQ INT4 weights (symmetric, group size 128) with BF16 activations in compressed-tensors format; built-in BF16 MTP head (`model_mtp.safetensors`) for vLLM speculative decoding; BF16 vision tower (`model_visual.safetensors`); no DFlash2 draft; tested on vLLM | 19,437,985,972 (≈18.1 GiB) | 5.25 | 177 / 446 / 87 |
| INT8 W8A8 | `INT8/W8A8/` | Text + image (`Qwen3_5ForConditionalGeneration`; the BF16 vision tower is a separate file, `model_visual.safetensors`, added 2026-10-09): SmoothQuant per-channel INT8 weights + per-token dynamic INT8 activations in compressed-tensors format; does not include the DFlash2 draft; MTP comes as a separate BF16 draft folder (`INT8/W8A8/MTP-BF16/`) for vLLM speculative decoding; loadable only by vLLM | 30,422,466,299 (≈28.3 GiB) | 8.77 | 175 / 450 / 91 |
| INT8 W8A16 | `INT8/W8A16/` | Text + image (`Qwen3_5ForConditionalGeneration`): GPTQ symmetric per-channel INT8 weights + BF16 activations (compressed-tensors pack-quantized); BF16 vision tower `model_visual.safetensors`; MTP as separate BF16 draft folder `INT8/W8A16/MTP-BF16/`; no DFlash2 draft; loadable only by vLLM | 30,370,996,824 (≈28.3 GiB including vision; MTP draft extra) | 8.76 | 170 / 449 / 94 |
| GGUF Q3 LynnStyle | `GGUF/` | Mixed-precision LynnStyle GGUF (`Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.gguf`): lowest type Q3; **built-in Q4 MTP**; vision external | 17,303,770,432 (~16.1 GiB) | 5.07 | 173 / 449 / 92 |
| GGUF Q3 LynnStyle · NInfer | `GGUF-NInfer/` | NInfer from Q3 LynnStyle GGUF; built-in Q4_K MTP and vision; NInfer-all and ninfer-fusion-kvmem | 17,596,369,920 (~16.4 GiB) | 5.07 | 173 / 449 / 92 |
| GGUF Q3 LynnStyle · Q8MTP | `GGUF/` | The same Q3 LynnStyle GGUF with only the built-in MTP head re-encoded as Q8_0 (`Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf`); every other tensor is byte-identical to the original; an alternative with a Q8_0 MTP head (the original's Q4_0 MTP head is supported by llama.cpp); llama.cpp vision via the mmproj in `GGUF/` | 17,516,107,072 (~16.3 GiB) | 5.13 | 173 / 449 / 92 |
| GGUF Q3 LynnStyle · Q8MTP · NInfer | `GGUF-NInfer/` | NInfer package from the Q8MTP GGUF above (`Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.ninfer`), built-in Q8_0 MTP head and vision, model id `qwen3.8-27b-coder390-Q3LynnStyle-Q8Mtp`; body weights identical to the original Q3 LynnStyle package, scores carried over | 17,808,706,560 (~16.6 GiB) | 5.13 | 173 / 449 / 92 |
| GGUF Q4 LynnStyle | `GGUF/` | Mixed-precision LynnStyle GGUF (`Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.gguf`): lowest type Q4; **built-in Q4 MTP**; vision external | 19,620,406,592 (~18.3 GiB) | 5.75 | 175 / 448 / 89 |
| GGUF Q4 LynnStyle · NInfer | `GGUF-NInfer/` | NInfer from Q4 LynnStyle GGUF; built-in Q4_K MTP and vision; NInfer-all and ninfer-fusion-kvmem | 19,913,006,080 (~18.5 GiB) | 5.74 | 175 / 448 / 89 |
| GGUF Q4 LynnStyle · Q8MTP | `GGUF/` | The same Q4 LynnStyle GGUF with only the built-in MTP head re-encoded as Q8_0 (`Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf`); every other tensor is byte-identical to the original; an alternative with a Q8_0 MTP head (the original's Q4_0 MTP head is supported by llama.cpp); llama.cpp vision via the mmproj in `GGUF/` | 19,832,743,232 (~18.5 GiB) | 5.81 | 175 / 448 / 89 |
| GGUF Q4 LynnStyle · Q8MTP · NInfer | `GGUF-NInfer/` | NInfer package from the Q8MTP GGUF above (`Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer`), built-in Q8_0 MTP head and vision, model id `qwen3.8-27b-coder390-Q4LynnStyle-Q8Mtp`; body weights identical to the original Q4 LynnStyle package, scores carried over | 20,125,342,720 (~18.7 GiB) | 5.81 | 175 / 448 / 89 |
| GGUF Q3 LynnStyle-16G | `GGUF/` | Our lowest Q3 tier, for 16 GB VRAM (`Qwen3.8-27B-Coder390-Q3LynnStyle16G-MTP.gguf`): lowest type IQ3_XXS, no Q6 / Q8 in the body; importance-matrix correction + GSQ-RCO (same-byte refinements, size unchanged); **built-in Q4_K MTP**; llama.cpp vision via the mmproj in `GGUF/`; scored with llama.cpp + DFlash2 external draft | 13,276,009,920 (~12.4 GiB) | 3.89 | 172 / 427 / 90 |
| GGUF Q3 LynnStyle-16G · NInfer | `GGUF-NInfer/` | NInfer package from the same Q3 LynnStyle-16G weights: built-in **Q4_K MTP** + built-in **Q8 vision** (add `--vision`; no mmproj) | 13,765,136,896 (~12.8 GiB) | 3.89 | same scores (GGUF triad) |
| GGUF Q2 LynnStyle | `GGUF/` | Mixed-precision LynnStyle GGUF (`Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf`): lowest type Q2; **built-in Q4 MTP**; vision external | 13,276,009,792 (~12.4 GiB) | 3.89 | 177 / 433 / 90 |
| GGUF Q2 LynnStyle · NInfer | `GGUF-NInfer/` | NInfer from Q2 LynnStyle GGUF; built-in Q4_K MTP and vision; NInfer-all and ninfer-fusion-kvmem | 13,568,617,472 (~12.6 GiB) | 3.89 | 177 / 433 / 90 |
| GGUF Q2 LynnStyle · Q8MTP | `GGUF/` | The same Q2 LynnStyle GGUF with only the built-in MTP head re-encoded as Q8_0 (`Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf`); every other tensor is byte-identical to the original; an alternative with a Q8_0 MTP head (the original's Q4_0 MTP head is supported by llama.cpp); llama.cpp vision via the mmproj in `GGUF/` | 13,488,346,432 (~12.6 GiB) | 3.95 | 177 / 433 / 90 |
| GGUF Q2 LynnStyle · Q8MTP · NInfer | `GGUF-NInfer/` | NInfer package from the Q8MTP GGUF above (`Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.ninfer`), built-in Q8_0 MTP head and vision, model id `qwen3.8-27b-coder390-Q2LynnStyle-Q8Mtp`; body weights identical to the original Q2 LynnStyle package, scores carried over | 13,780,954,112 (~12.8 GiB) | 3.95 | 177 / 433 / 90 |
| GGUF Q8_0 | `GGUF/` | GGUF single file for llama.cpp (`Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf`): Q8_0 backbone, built-in MTP head, no external draft; llama.cpp vision via `--mmproj` with the mmproj in `GGUF/` | 29,069,202,688 (~27.1 GiB) | 8.51 | 171 / 443 / 90 |
| GGUF Q8_0 · NInfer | `GGUF-NInfer/` | NInfer package converted from the same Q8_0 GGUF (`.ninfer`), built-in MTP head and vision component; loadable only by NInfer-all (`iamwavecut/ninfer-all`); scores from the same GGUF on llama.cpp | 29,361,802,240 (~27.3 GiB) | 8.51 | 171 / 443 / 90 |
| GGUF Q6_K | `GGUF/` | Single GGUF file for llama.cpp (`Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`): Q6_K backbone with imatrix calibration and a built-in Q8 MTP head, so no external draft is needed; llama.cpp vision via `--mmproj` with the mmproj in `GGUF/` | 23,177,516,384 (≈21.6 GiB) | 6.79 | 174 / 448 / 91 |
| GGUF Q6_K · NInfer | `GGUF-NInfer/` | NInfer package (`.ninfer`) converted from the same GGUF, same backbone quantization, built-in MTP head (attention/MLP weights Q6_K, input projection Q8_0), vision component built in (image input with `--vision`); loadable only by NInfer-all (`iamwavecut/ninfer-all`); scores measured on the same GGUF with llama.cpp | 23,379,962,880 (≈21.8 GiB) | 6.76 | 174 / 448 / 91 |

**Community fork ninfer-fusion-kvmem:** the Q2 / Q3 / Q4 LynnStyle NInfer packages (`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer`, `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer`, `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer`) carry a built-in MTP head re-encoded as Q4_K and load and run MTP on both the official NInfer-all `master` and the community fork ninfer-fusion-kvmem (tested 2026-10-11). The `.gguf` files in `GGUF/` keep a Q4_0 MTP head, which llama.cpp supports. The Q8 MTP versions remain available as an alternative (same weights, only the MTP head re-encoded as Q8_0): `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf`, `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf` and `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf` for llama.cpp, and `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.ninfer`, `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.ninfer` and `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer` for NInfer (model ids `qwen3.8-27b-coder390-Q2LynnStyle-Q8Mtp`, `qwen3.8-27b-coder390-Q3LynnStyle-Q8Mtp`, `qwen3.8-27b-coder390-Q4LynnStyle-Q8Mtp`).

**Q8 MTP versions · check** (2026-10-09, one RTX PRO 6000): NInfer-all `master` with `--spec mtp --draft-tokens 3 --vision`, int8 KV, 8,192 context; llama.cpp with `--spec-type draft-mtp --spec-draft-n-max 4` and `--mmproj`; one image request each, short runs. The image question was answered correctly in every run (llama.cpp with thinking on and off).

| Package | NInfer decode tok/s | NInfer MTP acceptance (tokens/round) | llama.cpp decode tok/s | llama.cpp draft acceptance | Image |
|---|---:|---:|---:|---:|---|
| Q2 LynnStyle · Q8MTP | 211.7 | 64.2% (3.14) | 180.1 | 0.879 | correct |
| Q3 LynnStyle · Q8MTP | 134.9 | 51.7% (2.55) | 138.3 | 0.904 | correct |
| Q4 LynnStyle · Q8MTP | 154.8 | 71.0% (3.13) | 135.6 | 0.879 | correct |

BPW (bits per weight) is the effective average bit width of the whole package: the total bytes of the main-model weight files (`.safetensors`, including the vision tower, MTP, and scale tensors, excluding the DFlash2 draft) × 8 ÷ total parameter count. The parameter count is taken from the safetensors headers and is identical across the five tiers at 27,781,427,952 (an NVFP4 packed U8 tensor counts 2 elements per byte; scale tensors add no elements). The weight-file totals for BF16, static FP8, NVFP4 W4A16, NVFP4 W4A4, and NVFP4 W4A4-W8A8 are 55,563,008,568, 31,242,033,200, 20,593,097,872, 20,593,145,056, and 23,749,329,544 bytes respectively. Every tier is mixed precision (different layers use different bit widths), so the nominal bit width can mislead; BPW reflects quality density per unit of size.

BPW for the two NInfer tiers is the whole `.ninfer` file bytes × 8 ÷ total parameter count 27,781,427,952: both files were 23,477,856,260 bytes before the vision component was added, so BPW is 6.76 for each. Each `.ninfer` package includes the Q8 MTP head, the DFlash2 draft, and the proposal head; the vision component added on 2026-10-09 (295,720,448 bytes) is not counted in this BPW; the safetensors-based BPW above for NVFP4 / BF16 / FP8 excludes the DFlash2 draft, so the two formulas differ and BPW should not be compared directly across those families.

INT8 W8A8's BPW counts only its 8 INT8 text weight files (the BF16 vision file `model_visual.safetensors`, 921,497,224 bytes, is not counted): their total bytes, 29,480,791,128, × 8 ÷ the text parameter count 26,895,998,464, giving 8.77. The text parameter count comes from the safetensors headers of the 8 INT8 weight files (INT8 and BF16 tensors count their elements; scale tensors add no elements) and equals the BF16 package's count without the vision tower (460,730,096) and MTP (424,699,392); because the denominator differs from the 27,781,427,952 used above, BPW should not be compared directly with the other tiers.

BPW for the two GGUF Q8_0 packages is the single file's bytes × 8 ÷ the text + MTP parameter count 27,320,697,856: the GGUF is 29,069,202,688 bytes, giving 8.51, and the NInfer package was 29,065,983,488 bytes before the vision component was added, giving 8.51. BPW for the two GGUF Q6_K packages is the single file's bytes × 8 ÷ the text + MTP parameter count 27,320,697,856: the GGUF is 23,177,516,384 bytes, giving 6.79, and the NInfer package was 23,084,144,128 bytes before the vision component was added, giving 6.76. The parameter count comes from the GGUF header (866 tensors: text 26,895,998,464 + MTP 424,699,392); vision is not counted in the denominator (neither the llama.cpp mmproj nor the 295,720,448-byte vision part now inside each `.ninfer`). Because the denominator differs from both the 27,781,427,952 used above and the 26,895,998,464 used for INT8 W8A8, BPW should not be compared directly with the other tiers.

- Each tier carries its own copy of the DFlash2 draft (identical files, 2,407,384,680 bytes): `FP8/DFlash2-FP8/`, `BF16/DFlash2-FP8/`, `NVFP4/W4A16/DFlash2-FP8/`, `NVFP4/W4A4/DFlash2-FP8/`, and `NVFP4/W4A4-W8A8/DFlash2-FP8/`.
- For a BF16 DFlash2 draft (e.g. for V100 or engines that cannot load the FP8 draft), use the upstream [incoai/Qwen3.8-27B-DFlash2](https://huggingface.co/incoai/Qwen3.8-27B-DFlash2).
- DFlash2 draft format: FP8 E4M3 weights with 128×128 block scales (`weight_scale_inv`), the same format as the FP8 body; q/k/v projections, `fc`, the candidate selector, convolutions and norms stay BF16. It replaced the earlier per-tensor-scale draft on 2026-10-08 (engines that only read block scales, such as radiance, loaded the old draft without error but accepted almost no draft tokens). Checked on one RTX PRO 6000 on 2026-10-09 (SGLang 0.5.21, FP8 body, `--speculative-num-draft-tokens 8 --speculative-dflash-block-size 8`, one request at a time, 6 coding prompts, 1,024-token cap): greedy mean accept length is 5.05 at 171 tok/s per request (median), against 4.99 at 178 tok/s for the earlier draft with the same command. At temperature 1.0 the two run at 155 and 152 tok/s. In SGLang the new draft accepts as well as the old one. The other DFlash2 speed numbers in this card were measured with the earlier draft.
- Speed figures for BF16 and static FP8 were measured on the static FP8 package (BF16 was not benchmarked separately and shares the same figures); the three NVFP4 tiers were each benchmarked on their own package.
- NVFP4 scores were measured on a single GPU at C8; see "NVFP4 tiers" above for the protocol.
- NInfer tier scores are carried over from the 2026-10-05 triad on the same text path (single GPU, C8, official NInfer, no speculation); see the NInfer tiers section above. NInfer speeds were measured separately on the new packages; see "NInfer tiers" under Best-TPS and concurrency recommendations below.
- INT4 W4A16 scores are a full triad measured on a single GPU at C8 with vLLM 0.28 and MTP (3 draft tokens, built-in head); see the INT4 W4A16 section above for the protocol, and "INT4 W4A16" under Best-TPS and concurrency recommendations below for speeds.
- INT8 W8A8 scores are a full triad measured on a single GPU at C8 with vLLM and no speculation; see the INT8 W8A8 section above for the protocol. Its speeds come from a quick benchmark; see "INT8 W8A8" under Best-TPS and concurrency recommendations below.
- GGUF Q6_K scores are a full triad measured on a single GPU at C4 with llama.cpp; see the GGUF Q6_K section above for the protocol. Its speeds come from a quick benchmark; see "GGUF Q6_K" under Best-TPS and concurrency recommendations below.
- GGUF Q8_0 scores are a full triad measured on a single GPU at C4 with llama.cpp; see the GGUF Q8_0 section above for the protocol. For speeds see "GGUF Q8_0" below (NInfer C8 MTP 486.3; llama.cpp C4 MTP 190.8).
- The two NInfer tiers are under `NVFP4-NInfer/W4A4/` and `NVFP4-NInfer/W4A4-W8A8/`, INT8 W8A8 is under `INT8/W8A8/`, INT4 W4A16 is under `INT4/W4A16/`, and GGUF Q2 / Q3 / Q4 LynnStyle (plus their Q8 MTP versions), Q6_K, and Q8_0 are under `GGUF/` and `GGUF-NInfer/`.

## Best-TPS and concurrency recommendations

Environment: one RTX PRO 6000 Blackwell 96GB; SGLang, 32K context (32,768), 4,096-token generation cap, thinking enabled, model-default sampling.

| Goal | Pick | Aggregate tok/s | Per-request tok/s |
|---|---|---:|---:|
| Fastest single request | DFlash2 · C1 | 146.7 | **180.3** |
| Highest aggregate throughput | DFlash2 · C16 | **1,057.5** | 93.6 |
| Balanced daily use | DFlash2 · C8 | 646.3 | 113.9 |
| MTP only: fastest single request | MTP · C1 | 82.1 | **91.1** |
| MTP only: highest aggregate throughput | MTP · C16 | **612.7** | 60.1 |
| MTP only: balanced daily use | MTP · C8 | 380.3 | 71.1 |

- **Which speculation**: at every measured concurrency (C1–C16), DFlash2 beats MTP on both aggregate and per-request speed. Use DFlash2 whenever you can.
- **When to use MTP**: when you do not want to load the separate DFlash2 draft (DFlash2 has only been validated on SGLang; vLLM 0.28 + MTP: temporarily unavailable for FP8; use SGLang for now). If you run MTP only: use C1 for the fastest single request (91.1 tok/s), C4 for interactive use with a few users (293.3 aggregate, 84.0 per request), C8 for shared serving (380.3 aggregate, 71.1 per request), and C16 when only total throughput matters (612.7 aggregate, 60.1 per request).
- **Concurrency**: C1–C4 for interactive use, C8 for shared or batch serving, C16 when only total throughput matters. Concurrency above C16 was not tested.

<details>
<summary>Full measured table</summary>

C1 is the main run (4 requests); C4/C8/C16 are reruns with more requests (6×C per cell). "vs. no spec" is the ratio of aggregate throughput at the same concurrency.

| Speculation | Concurrency | Aggregate tok/s | Per-request decode tok/s (median) | TTFT s (median) | Accept length | Accept rate | vs. no spec |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP (bundled BF16) | C1 | 82.1 | 91.1 | 0.12 | 2.858 | 0.619 | 1.82× |
| MTP (bundled BF16) | C4 | 293.3 | 84.0 | 0.15 | 2.844 | 0.615 | 1.96× |
| MTP (bundled BF16) | C8 | 380.3 | 71.1 | 0.16 | 2.813 | 0.604 | 1.34× |
| MTP (bundled BF16) | C16 | 612.7 | 60.1 | 0.17 | 2.747 | 0.582 | 1.45× |
| DFlash2 | C1 | 146.7 | 180.3 | 0.12 | 4.289 | 0.470 | 3.25× |
| DFlash2 | C4 | 384.9 | 124.4 | 0.16 | 3.982 | 0.425 | 2.57× |
| DFlash2 | C8 | 646.3 | 113.9 | 0.15 | 4.131 | 0.447 | 2.28× |
| DFlash2 | C16 | 1,057.5 | 93.6 | 0.24 | 4.017 | 0.431 | 2.50× |
| No speculation | C1 | 45.1 | 45.6 | 0.11 | n/a | n/a | 1.00× |
| No speculation | C4 | 149.5 | 42.2 | 0.13 | n/a | n/a | 1.00× |
| No speculation | C8 | 283.0 | 41.7 | 0.12 | n/a | n/a | 1.00× |
| No speculation | C16 | 422.8 | 38.4 | 0.13 | n/a | n/a | 1.00× |

| Speculation | Fastest per request | Recommended (highest aggregate with per-request speed ≥ 60% of C1) | Highest aggregate |
|---|---|---|---|
| MTP | C1 (91.1 tok/s) | C16 (612.7 tok/s, 60.1 per request) | C16 |
| DFlash2 | C1 (180.3 tok/s) | C8 (646.3 tok/s, 113.9 per request) | C16 (1,057.5 tok/s) |
| No speculation | C1 (45.6 tok/s) | C16 (422.8 tok/s) | C16 |

</details>

### NVFP4 tiers

Same environment as above: one RTX PRO 6000 Blackwell 96GB; SGLang, 32K context (32,768), 4,096-token generation cap, thinking enabled, model-default sampling. Data from `evaluation/BENCH_NVFP4_W4A16.json`, `evaluation/BENCH_NVFP4_W4A4.json`, and `evaluation/BENCH_NVFP4_MIXED.json` (the W4A4-W8A8 tier).

| Goal | Pick | W4A16 aggregate tok/s | W4A16 per-request tok/s | W4A4 aggregate tok/s | W4A4 per-request tok/s | W4A4-W8A8 aggregate tok/s | W4A4-W8A8 per-request tok/s |
|---|---|---:|---:|---:|---:|---:|---:|
| Fastest single request | DFlash2 · C1 | 147.4 | **218.4** | 188.6 | **211.5** | 175.1 | **216.8** |
| Highest aggregate throughput | DFlash2 · C16 | **1,012.3** | 96.6 | **1,143.2** | 121.1 | **1,146.4** | 105.5 |
| Balanced daily use | DFlash2 · C8 | 472.4 | 131.7 | 689.8 | 132.4 | 627.9 | 132.4 |
| MTP only: fastest single request | MTP · C1 | 101.1 | **128.9** | 104.7 | **124.5** | 99.9 | **116.3** |
| MTP only: highest aggregate throughput | MTP · C16 | **817.3** | 70.6 | **912.4** | 73.0 | **580.2** | 69.4 |
| MTP only: balanced daily use | MTP · C8 | 450.7 | 91.3 | 355.5 | 86.6 | 417.2 | 83.2 |

- **Which speculation**: on W4A4 and W4A4-W8A8, DFlash2 beats MTP on both aggregate and per-request speed at every measured concurrency (C1–C16). On W4A16, MTP has the higher aggregate only at C4 (351.4 vs. 315.2); DFlash2 is faster at every other level and on per-request speed throughout.
- **MTP only**: on W4A16, use C1 for the fastest single request (128.9 tok/s), C4 for interactive use with a few users (351.4 aggregate, 108.0 per request), C8 for shared serving (450.7 aggregate, 91.3 per request), and C16 when only total throughput matters (817.3 aggregate, 70.6 per request). On W4A4 the same levels give C1 124.5 tok/s, C4 323.2 / 103.9, C8 355.5 / 86.6, and C16 912.4 / 73.0; on W4A4-W8A8, C1 116.3 tok/s, C4 213.0 / 99.8, C8 417.2 / 83.2, and C16 580.2 / 69.4 (aggregate / per request).
- **Accept length**: MTP 2.608–2.967 (W4A16), 2.597–2.923 (W4A4), and 2.647–2.865 (W4A4-W8A8); DFlash2 3.351–4.143 (W4A16), 3.723–4.327 (W4A4), and 3.828–4.364 (W4A4-W8A8).
- **Concurrency**: above C16 was not tested.

<details>
<summary>NVFP4 W4A16 full measured table</summary>

Requests per level: 4 at C1, 12 at C4, 24 at C8, 48 at C16. "vs. no spec" is the ratio of aggregate throughput at the same concurrency.

| Speculation | Concurrency | Aggregate tok/s | Per-request decode tok/s (median) | TTFT s (median) | Accept length | Accept rate | vs. no spec |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP (bundled BF16) | C1 | 101.1 | 128.9 | 0.11 | 2.608 | 0.537 | 1.44× |
| MTP (bundled BF16) | C4 | 351.4 | 108.0 | 0.13 | 2.796 | 0.599 | 2.34× |
| MTP (bundled BF16) | C8 | 450.7 | 91.3 | 0.13 | 2.743 | 0.581 | 1.50× |
| MTP (bundled BF16) | C16 | 817.3 | 70.6 | 0.15 | 2.967 | 0.656 | 1.58× |
| DFlash2 | C1 | 147.4 | 218.4 | 0.10 | 3.469 | 0.353 | 2.11× |
| DFlash2 | C4 | 315.2 | 164.9 | 0.13 | 3.351 | 0.337 | 2.10× |
| DFlash2 | C8 | 472.4 | 131.7 | 0.14 | 3.454 | 0.351 | 1.57× |
| DFlash2 | C16 | 1,012.3 | 96.6 | 0.23 | 4.143 | 0.449 | 1.96× |
| No speculation | C1 | 70.0 | 71.6 | 0.09 | n/a | n/a | 1.00× |
| No speculation | C4 | 150.3 | 62.1 | 0.10 | n/a | n/a | 1.00× |
| No speculation | C8 | 300.9 | 62.1 | 0.10 | n/a | n/a | 1.00× |
| No speculation | C16 | 515.8 | 54.7 | 0.10 | n/a | n/a | 1.00× |

| Speculation | Fastest per request | Recommended (highest aggregate with per-request speed ≥ 60% of C1) | Highest aggregate |
|---|---|---|---|
| MTP | C1 (128.9 tok/s) | C8 (450.7 tok/s, 91.3 per request) | C16 (817.3 tok/s) |
| DFlash2 | C1 (218.4 tok/s) | C8 (472.4 tok/s, 131.7 per request) | C16 (1,012.3 tok/s) |
| No speculation | C1 (71.6 tok/s) | C16 (515.8 tok/s) | C16 (515.8 tok/s) |

</details>

<details>
<summary>NVFP4 W4A4 full measured table</summary>

Requests per level: 4 at C1, 12 at C4, 24 at C8, 48 at C16. "vs. no spec" is the ratio of aggregate throughput at the same concurrency.

| Speculation | Concurrency | Aggregate tok/s | Per-request decode tok/s (median) | TTFT s (median) | Accept length | Accept rate | vs. no spec |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP (bundled BF16) | C1 | 104.7 | 124.5 | 0.15 | 2.685 | 0.562 | 1.48× |
| MTP (bundled BF16) | C4 | 323.2 | 103.9 | 0.18 | 2.597 | 0.531 | 2.04× |
| MTP (bundled BF16) | C8 | 355.5 | 86.6 | 0.17 | 2.683 | 0.561 | 1.12× |
| MTP (bundled BF16) | C16 | 912.4 | 73.0 | 0.18 | 2.923 | 0.641 | 1.86× |
| DFlash2 | C1 | 188.6 | 211.5 | 0.14 | 4.327 | 0.476 | 2.66× |
| DFlash2 | C4 | 456.1 | 182.1 | 0.16 | 4.011 | 0.430 | 2.88× |
| DFlash2 | C8 | 689.8 | 132.4 | 0.17 | 3.723 | 0.389 | 2.18× |
| DFlash2 | C16 | 1,143.2 | 121.1 | 0.28 | 3.985 | 0.427 | 2.33× |
| No speculation | C1 | 70.9 | 72.0 | 0.13 | n/a | n/a | 1.00× |
| No speculation | C4 | 158.3 | 62.8 | 0.15 | n/a | n/a | 1.00× |
| No speculation | C8 | 316.8 | 62.5 | 0.14 | n/a | n/a | 1.00× |
| No speculation | C16 | 490.5 | 55.2 | 0.14 | n/a | n/a | 1.00× |

| Speculation | Fastest per request | Recommended (highest aggregate with per-request speed ≥ 60% of C1) | Highest aggregate |
|---|---|---|---|
| MTP | C1 (124.5 tok/s) | C8 (355.5 tok/s, 86.6 per request) | C16 (912.4 tok/s) |
| DFlash2 | C1 (211.5 tok/s) | C8 (689.8 tok/s, 132.4 per request) | C16 (1,143.2 tok/s) |
| No speculation | C1 (72.0 tok/s) | C16 (490.5 tok/s) | C16 (490.5 tok/s) |

</details>

<details>
<summary>NVFP4 W4A4-W8A8 full measured table</summary>

Requests per level: 4 at C1, 12 at C4, 24 at C8, 48 at C16. "vs. no spec" is the ratio of aggregate throughput at the same concurrency.

| Speculation | Concurrency | Aggregate tok/s | Per-request decode tok/s (median) | TTFT s (median) | Accept length | Accept rate | vs. no spec |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP (bundled BF16) | C1 | 99.9 | 116.3 | 0.17 | 2.865 | 0.621 | 1.61× |
| MTP (bundled BF16) | C4 | 213.0 | 99.8 | 0.19 | 2.667 | 0.555 | 1.09× |
| MTP (bundled BF16) | C8 | 417.2 | 83.2 | 0.18 | 2.647 | 0.549 | 1.33× |
| MTP (bundled BF16) | C16 | 580.2 | 69.4 | 0.19 | 2.772 | 0.591 | 1.24× |
| DFlash2 | C1 | 175.1 | 216.8 | 0.16 | 4.201 | 0.458 | 2.82× |
| DFlash2 | C4 | 395.0 | 152.4 | 0.19 | 3.995 | 0.427 | 2.02× |
| DFlash2 | C8 | 627.9 | 132.4 | 0.19 | 3.828 | 0.404 | 2.00× |
| DFlash2 | C16 | 1,146.4 | 105.5 | 0.30 | 4.364 | 0.479 | 2.44× |
| No speculation | C1 | 62.2 | 63.0 | 0.15 | n/a | n/a | 1.00× |
| No speculation | C4 | 195.7 | 56.4 | 0.17 | n/a | n/a | 1.00× |
| No speculation | C8 | 314.0 | 53.4 | 0.16 | n/a | n/a | 1.00× |
| No speculation | C16 | 469.4 | 47.7 | 0.16 | n/a | n/a | 1.00× |

| Speculation | Fastest per request | Recommended (highest aggregate with per-request speed ≥ 60% of C1) | Highest aggregate |
|---|---|---|---|
| MTP | C1 (116.3 tok/s) | C8 (417.2 tok/s, 83.2 per request) | C16 (580.2 tok/s) |
| DFlash2 | C1 (216.8 tok/s) | C8 (627.9 tok/s, 132.4 per request) | C16 (1,146.4 tok/s) |
| No speculation | C1 (63.0 tok/s) | C16 (469.4 tok/s) | C16 (469.4 tok/s) |

</details>

### NInfer tiers

Setup: one RTX PRO 6000 Blackwell; official NInfer with the same context flags as the NInfer launch commands below (`--max-context 102400 --kv-capacity 819200 --max-concurrency 8 --kv-dtype fp8`); 4,096 generation cap, thinking on (template default xhigh), sampling temperature 1.0, top_p 0.95, top_k 20, same prompts as the NVFP4 benchmark above; 4 requests at C1, 12 at C4, 24 at C8. MTP uses 4 draft tokens and DFlash2 uses 8, both with `--lm-head-draft`. Numbers are aggregate decode tok/s. NInfer supports at most 8 concurrent requests, so C16 was not tested.

| Speculation | Tier | C1 | C4 | C8 |
|---|---|---:|---:|---:|
| No speculation | NInfer W4A4 | 68.1 | 195.8 | 306.8 |
| No speculation | NInfer W4A4-W8A8 | 68.1 | 236.1 | 369.5 |
| MTP (4 draft tokens) | NInfer W4A4 | 154.8 | 498.3 | 678.3 |
| MTP (4 draft tokens) | NInfer W4A4-W8A8 | 162.5 | 367.6 | 663.9 |
| DFlash2 (8 draft tokens) | NInfer W4A4 | 207.1 | 539.6 | 975.9 |
| DFlash2 (8 draft tokens) | NInfer W4A4-W8A8 | 199.1 | 650.1 | 804.9 |

- **Best setting**: for both tiers and all three modes, aggregate throughput peaks at C8. NInfer W4A4 tops out with DFlash2 · C8 (975.9 tok/s) and NInfer W4A4-W8A8 with DFlash2 · C8 (804.9 tok/s); with MTP only, C8 gives 678.3 and 663.9 tok/s respectively.
- **C8 versus NVFP4 W4A4 (SGLang)**: NInfer W4A4 reaches 306.8 vs 316.8 with no speculation, 678.3 vs 355.5 with MTP, and 975.9 vs 689.8 tok/s with DFlash2. The engines and context settings differ, so treat this as a rough comparison.

### INT4 W4A16

Setup: one NVIDIA RTX PRO 6000 Blackwell (96 GB); vLLM 0.28 with `--max-model-len 102400`, `--max-num-seqs 8`, and `--gpu-memory-utilization 0.85`; MTP row uses the built-in head with `--speculative-config '{"method":"mtp","num_speculative_tokens":3}'`. 1024 generation cap, thinking on, sampling temperature 1.0, top_p 0.95, top_k 20; each level sends 2 × concurrency requests over the same 8 prompts (same script as the INT8 `MTP-BF16/` table). Numbers are aggregate tok/s (all output tokens ÷ wall-clock time); the last column is the median per-request decode speed at C1.

| Speculation | C1 | C2 | C4 | C8 | C1 per request |
|---|---:|---:|---:|---:|---:|
| No speculation | 67.3 | 110.1 | 197.4 | 350.0 | 68.4 |
| MTP (3 draft tokens) | 121.2 | 193.2 | 347.5 | 500.1 | 135.2 |

- **Accept length** (mean tokens per step, including the verified token): 2.77–2.92 across C1–C8 in this table; 2.81 averaged over the full eval run.
- The INT4 scores above were measured with MTP (3 draft tokens).

### INT8 W8A8

Setup: one RTX PRO 6000 Blackwell; vLLM 0.28 with `--max-model-len 102400` and `--max-num-seqs 8`; 512 generation cap, thinking on (xhigh), sampling temperature 1.0, top_p 0.95, top_k 20; each level sends only as many requests as its concurrency (1 at C1, 2 at C2, 4 at C4, 8 at C8). This is a quick benchmark with few requests and short outputs, so the numbers are not directly comparable with the tiers above. Numbers are aggregate tok/s (all output tokens ÷ wall-clock time). Both rows were measured on a separate, unreleased comparison build with MTP (the same INT8 text weights plus one BF16 MTP layer); with no speculation the MTP layer is not used. This package does not include MTP; a separate MTP draft folder is now provided (see below).

| Speculation | C1 | C2 | C4 | C8 |
|---|---:|---:|---:|---:|
| No speculation | 30.8 | 45.5 | 101.2 | **177.3** |
| MTP (earlier comparison build, not the released draft) | 23.9 | 37.8 | 72.5 | 145.9 |

- **Recommendation (this table)**: no speculation at C8 (177.3 tok/s); aggregate throughput rises with concurrency, and nothing above C8 was tested.
- The MTP row above came from an earlier, unreleased comparison build and is kept for reference only; it does not describe the `MTP-BF16/` draft folder, which is measured separately below. This tier has no DFlash2 draft.

**With the `MTP-BF16/` draft folder**

Setup: one NVIDIA RTX PRO 6000 Blackwell (96 GB); vLLM 0.28 with `--max-model-len 102400`, `--max-num-seqs 8`, and `--gpu-memory-utilization 0.85`; MTP row uses `--speculative-config '{"method":"mtp","model":"./INT8/W8A8/MTP-BF16","num_speculative_tokens":3}'`. 1024 generation cap, thinking on, sampling temperature 1.0, top_p 0.95, top_k 20; each level sends 2 × concurrency requests over the same 8 prompts. Numbers are aggregate tok/s (all output tokens ÷ wall-clock time); the last column is the median per-request decode speed at C1. Different hardware and settings from the table above, so compare rows only within this table.

| Speculation | C1 | C2 | C4 | C8 | C1 per request |
|---|---:|---:|---:|---:|---:|
| No speculation | 31.1 | 59.9 | 81.9 | 127.0 | 31.6 |
| MTP (3 draft tokens) | 65.9 | 120.5 | 199.4 | 389.8 | 75.7 |

- **Accept length** (mean tokens per step, including the verified token): 2.74–2.90 across C1–C8.
- With this draft, 3 draft tokens is faster at every level on this machine: 65.9 tok/s at C1 against 31.1 with no speculation, and 389.8 tok/s at C8 against 127.0.
- The INT8 scores above were measured without speculation; the draft folder does not change any INT8 weight file.

### GGUF Q6_K

Setup: one RTX PRO 6000 Blackwell; 1-minute quick benchmark, 512 generation cap, thinking on (xhigh), sampling temperature 1.0, top_p 0.95, top_k 20; each level sends only as many requests as its concurrency (1 at C1, 2 at C2, 4 at C4, 8 at C8). Numbers are aggregate tok/s (all output tokens ÷ wall-clock time). This is a quick benchmark with few requests and short outputs, so the numbers are not directly comparable with the full SGLang / NInfer benchmarks above. NInfer rows were measured on the `GGUF-NInfer/` package with the server at `--max-context 32768 --kv-capacity 32768 --kv-dtype rk8v4 --max-concurrency 8`; llama.cpp rows were measured on the `GGUF/` package.

| Engine · speculation | C1 | C2 | C4 | C8 |
|---|---:|---:|---:|---:|
| NInfer · MTP (3 draft tokens) | 131.9 | 161.9 | **235.5** | 388.1 |
| NInfer · no speculation | 56.0 | 93.9 | 162.1 | 298.1 |
| llama.cpp · MTP | 97.2 | 95.3 | 168.1 | 189.0 |
| llama.cpp · no speculation | 53.4 | not measured | 123.0 | not measured |

- **Recommendation**: NInfer + C4 + MTP (235.5 tok/s), matching the recommended launch command below (`--max-concurrency 4`). For aggregate throughput alone, C8 is higher (388.1 tok/s); raise `--max-concurrency` to 8 for that.
- **MTP is built in**: both packages carry a built-in MTP head (GGUF: Q8_0; NInfer: Q6_K attention/MLP weights), so no external draft model is needed. For a single request, NInfer with MTP reaches 131.9 tok/s, about 2.5× llama.cpp without speculation (53.4 tok/s); llama.cpp with MTP reaches 97.2 tok/s aggregate at C1 (119.0 tok/s single-request decode).


### GGUF Q8_0

Hardware: single RTX PRO 6000 Blackwell. llama.cpp rows use the quick protocol (thinking on, fused MTP): C1=4 requests, C2=6, C4=12; aggregate decode tok/s. NInfer rows use the same-caliber bench (thinking on, template default xhigh, max_tokens 4096, temperature 1.0, top_p 0.95, top_k 20; C1=4, C4=12, C8=24; MTP draft-tokens 4).

| Engine · speculation | C1 | C2 | C4 | C8 |
|---|---:|---:|---:|---:|
| NInfer · MTP (draft 4) | 109.5 | not measured | 332.0 | **486.3** |
| llama.cpp · MTP | 85.3 | 133.6 | **190.8** | not measured |

- **Recommended**: NInfer + C8 + MTP (486.3 tok/s). Fastest llama.cpp point is C4 MTP (190.8 tok/s).
- **MTP built in**: both packages carry an MTP head; no external draft model.


## Recommended launch commands

### Quantization scheme

- **BF16** (`BF16/`): all weights in BF16 with the original multimodal config (mrope retained, `mtp_num_hidden_layers=1`) and no `quantization_config`.
- **Static FP8** (`FP8/`): official-style static FP8, E4M3 weights in 128×128 blocks with one scale per block (`weight_scale_inv`); activations use dynamic FP8. The config only adds a top-level FP8 `quantization_config`.
- **NVFP4 W4A16** (`NVFP4/W4A16/`): ModelOpt local-Hessian calibration. NVFP4 is E2M1 in 16-element blocks with one E4M3 scale per block plus a per-tensor FP32 second-level scale. MLP gate/up/down, full-attention q/k/v/o, and linear-attention `in_proj_qkv` / `in_proj_z` / `out_proj` (400 Linear layers) use NVFP4 weights with BF16 activations; linear-attention `in_proj_a` / `in_proj_b` and `lm_head` (97 layers) stay in BF16. The quantization metadata uses ModelOpt's `MIXED_PRECISION` format (each of the 400 layers tagged `W4A16_NVFP4`), which SGLang detects as `modelopt_mixed`. 1,999 tensors: 1,651 language, 333 vision, 15 MTP.
- **NVFP4 W4A4** (`NVFP4/W4A4/`): same calibration data and algorithm and the same 400 Linear layers, with both weights and activations in NVFP4 (activations are quantized at inference in 16-element blocks). Standard `NVFP4` export, detected by SGLang as `modelopt_fp4`. 2,399 tensors: 2,051 language, 333 vision, 15 MTP.
- **NVFP4 W4A4-W8A8** (`NVFP4/W4A4-W8A8/`): mixed precision with the same calibration data and algorithm. MLP gate/up/down (192 Linear layers) use NVFP4 W4A4 (both weights and activations in NVFP4; activations are quantized at inference in 16-element blocks); full-attention q/k/v/o and linear-attention `in_proj_qkv` / `in_proj_z` / `out_proj` (208 Linear layers) use FP8 W8A8 (E4M3 weights and activations with static per-tensor scales; activation scales come from calibration); linear-attention `in_proj_a` / `in_proj_b` and `lm_head` (97 layers) stay in BF16. The quantization metadata uses ModelOpt's `MIXED_PRECISION` format (each layer tagged `NVFP4` or `FP8`), which SGLang detects as `modelopt_mixed`. 2,191 tensors: 1,843 language, 333 vision, 15 MTP.
- **NVFP4 calibration data**: complete trajectories (prompt + reasoning + final answer) that were correct and non-empty, taken from this model's own RLOO training data: 512 samples, about 1.735M tokens, at most 4,096 tokens each. No official GPQA, MMLU, or LCB problems are used. See `evaluation/NVFP4_CALIBRATION_METHOD.md`. In all three tiers the vision tower (333 tensors) and MTP (15 tensors) are BF16.
- Architecture: `Qwen3_5ForConditionalGeneration`, 64 layers (linear attention and full attention alternating 3:1). The FP8 package has 1,599 tensors: 1,251 language, 333 vision, 15 MTP.

| Component (static FP8 package) | Precision |
|---|---|
| Linear attention `A_log`, `dt_bias`, `norm`, `conv1d`, `in_proj_a` / `in_proj_b` (×48) | BF16 |
| Linear attention `in_proj_qkv`, `in_proj_z`, `out_proj` (×48) | FP8 E4M3 Block128 |
| Full-attention q/k/v/o and all MLP gate/up/down (400 Linear layers including the row above) | FP8 E4M3 Block128 |
| `embed_tokens`, `lm_head` | BF16 |
| Vision tower (333 tensors) | BF16, taken unchanged from the RLOO merged weights |
| MTP (15 tensors) | BF16, taken unchanged from the official Qwen3.8-27B |

All SSM control branches stay in BF16; the exclusion list matches Qwen's official FP8 release, keeping 146 language-model modules in BF16. FP8 package smoke tests passed: patch-free load in SGLang, greedy output identical to the text-only evaluation build, SGLang image request, SGLang MTP, and vLLM image request. vLLM 0.28 + MTP: temporarily unavailable for FP8; use SGLang for now.

NVFP4 smoke tests: patch-free load in SGLang, greedy parity, and the image request passed. MTP and DFlash2 speed and accept length come from the separate benchmark runs (all C1–C16 levels completed; see above).

**GGUF Q8_0** (`GGUF/`, `GGUF-NInfer/`): Q8_0 backbone with built-in MTP head (`blk.64.nextn`), no external draft; 866 tensors; `.ninfer` converted from the same GGUF; the GGUF has no vision weights (llama.cpp uses `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` via `--mmproj`); the `.ninfer` carries the vision component inside the package (add `--vision`; see NInfer · vision below).

**GGUF Q6_K** (`GGUF/`, `GGUF-NInfer/`): Q6_K backbone calibrated with a 512-chunk imatrix, plus structure protection: the linear-attention (SSM) `ssm_alpha` / `ssm_beta` stay BF16, the token embedding and output head are Q8_0, and the MTP head (`blk.64` attn q/k/v/output, ffn gate/up/down, and `nextn.eh_proj`) is entirely Q8_0 with its norms kept in F32. The GGUF has 866 tensors in 65 blocks (64 backbone layers + 1 MTP layer). The `.ninfer` is converted from the same GGUF with the same backbone quantization; its MTP attention/MLP weights are Q6_K (`gguf_q6_k`) and only `mtp/input_projection` is Q8_0; the GGUF has no vision weights (llama.cpp uses `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` via `--mmproj`); the `.ninfer` carries the vision component inside the package (add `--vision`; see NInfer · vision below).

### Commands

Requires official SGLang ≥ 0.5.19; vLLM ≥ 0.28 (MTP only). vLLM MTP on NVFP4 with tensor parallel ≥ 2 has a known issue (vLLM #52480); use a single GPU there. vLLM 0.28 + MTP: temporarily unavailable for FP8; use SGLang for now. INT8 W8A8 and INT4 W4A16 load only in vLLM (tested on 0.28); their commands are below, after the NInfer commands.

**MTP and DFlash2 are mutually exclusive; enable only one per launch.** The examples use `./FP8`; for the BF16 tier, replace the `--model-path` path with `./BF16`, and for the NVFP4 tiers replace `--model-path` with `./NVFP4/W4A16`, `./NVFP4/W4A4`, or `./NVFP4/W4A4-W8A8`. The DFlash2 draft is the `DFlash2-FP8` folder inside each tier (e.g. `./FP8/DFlash2-FP8`, `./BF16/DFlash2-FP8`, `./NVFP4/W4A16/DFlash2-FP8`). SGLang detects the NVFP4 quantization format automatically, so no `--quantization` flag is needed; among these SGLang-format tiers, vLLM was validated only on the FP8 package (without MTP), and NVFP4 was tested only on SGLang; INT8 W8A8 and INT4 W4A16 are vLLM-only and were evaluated on vLLM 0.28. Concurrency and context settings match the benchmark runs; adjust as needed.

**SGLang · MTP (bundled BF16)**

```bash
python -m sglang.launch_server \
  --model-path ./FP8 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4
```

**vLLM · MTP**

vLLM 0.28 + MTP: temporarily unavailable for FP8; use SGLang for now (see the SGLang MTP command above).

**SGLang · DFlash2**

```bash
python -m sglang.launch_server \
  --model-path ./FP8 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path ./FP8/DFlash2-FP8 \
  --speculative-draft-model-quantization fp8 \
  --speculative-num-draft-tokens 8
```

**SGLang · NVFP4 W4A16 · DFlash2** (for W4A4, replace both `W4A16` with `W4A4`; for MTP on NVFP4, use the MTP command above and change only `--model-path`)

```bash
python -m sglang.launch_server \
  --model-path ./NVFP4/W4A16 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path ./NVFP4/W4A16/DFlash2-FP8 \
  --speculative-draft-model-quantization fp8 \
  --speculative-num-draft-tokens 8
```

**SGLang · NVFP4 W4A4-W8A8 · DFlash2** (for MTP, use the MTP command above and change only `--model-path`)

```bash
python -m sglang.launch_server \
  --model-path ./NVFP4/W4A4-W8A8 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path ./NVFP4/W4A4-W8A8/DFlash2-FP8 \
  --speculative-draft-model-quantization fp8 \
  --speculative-num-draft-tokens 8
```

The BF16 / FP8 / NVFP4 scores in this card were measured on SGLang with DFlash2 enabled (NInfer and INT8 W8A8 without speculation, INT4 W4A16 with MTP, GGUF on llama.cpp; see each section); speculative decoding does not change the target model's output distribution. Default sampling is in `generation_config.json` (temperature 1.0, top_p 0.95, top_k 20).

**Images on SGLang / vLLM**: `BF16/`, `FP8/`, `NVFP4/W4A16/`, `NVFP4/W4A4/` and `NVFP4/W4A4-W8A8/` are full multimodal checkpoints: `config.json` declares `Qwen3_5ForConditionalGeneration` with a `vision_config`, each folder has `preprocessor_config.json` and `video_preprocessor_config.json`, and the weight index maps all 333 vision-tower tensors (to `vision-bf16.safetensors` in that folder; for BF16, to `model-00002-of-00002.safetensors`). The SGLang and vLLM commands above accept images as they are, with no extra flag; send OpenAI-style `image_url` parts to `POST /v1/chat/completions` (request example under NInfer · vision below; set `model` to the served model name). `INT8/W8A8/` accepts images too since 2026-10-09 (`Qwen3_5ForConditionalGeneration`; BF16 vision tower in `model_visual.safetensors`, preprocessor configs included): use the INT8 vLLM commands below as they are. `INT4/W4A16/` accepts images too (BF16 vision tower in `model_visual.safetensors`): use the INT4 vLLM command below.

#### NVFP4 · NInfer (`.ninfer`, official NInfer)

W4A4 is shown; for W4A4-W8A8, change the path to `./NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8-MTP-DFlash2.ninfer` and `--model-id` to `qwen3.8-27b-coder390-w4a4-w8a8`.

The MTP-DFlash2 packages already contain the Q8 MTP head and the DFlash2 draft, so NInfer needs no external draft model (unlike the SGLang commands above, which take a DFlash2 draft path); pass either `--spec mtp` or `--spec dflash2`, or omit `--spec` to run without speculation.

**Images:** the two V3 MTP-DFlash2 `.ninfer` packages in `NVFP4-NInfer/` (W4A4 and W4A4-W8A8) contain the vision component since 2026-10-09 (295,720,448 bytes, quantized from the BF16 vision weights: patch embedding Q6, attention q/k/v and MLP fc1 Q4, other projections Q5, merger Q8, norms and biases BF16). Text, MTP and DFlash2 weights are byte-for-byte unchanged. Add `--vision` to any NInfer command below and send images as OpenAI-style `image_url` parts to `POST /v1/chat/completions`. Without `--vision` the packages run text-only, as before. The V2 packages (`-NInferV2-NOT-FOR-V3`) are unchanged and still have no vision. GPU test on 2026-10-09 (one RTX PRO 6000, NInfer-all 64492cb with `--vision`, image prompt): both MTP-DFlash2 packages answered correctly. W4A4-MTP-DFlash2: MTP (3 draft tokens) accept length 2.89, decode 153 tok/s; DFlash2 (7 draft tokens) accept length 3.53, decode 185 tok/s. W4A4-W8A8-MTP-DFlash2: MTP 3.19, 164 tok/s; DFlash2 3.74, 195 tok/s.

**NInfer · no speculation**

```bash
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8
```

**NInfer · MTP (4 draft tokens)**

```bash
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec mtp --draft-tokens 4 --lm-head-draft
```

**NInfer · DFlash2 (8 draft tokens)**

```bash
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec dflash2 --draft-tokens 8 --lm-head-draft
```

**NInfer · vision (image input), one command per package**

Each command is the matching NInfer command above plus `--vision`. Nothing else is needed: the vision component is inside every V3 `.ninfer`, so the `vision-bf16.safetensors` next to the packages is not used at run time.

```bash
# W4A4 · MTP-DFlash2 package · no speculation
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --vision

# W4A4 · MTP-DFlash2 package · MTP
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec mtp --draft-tokens 4 --lm-head-draft \
  --vision

# W4A4 · MTP-DFlash2 package · DFlash2
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec dflash2 --draft-tokens 8 --lm-head-draft \
  --vision

# W4A4-W8A8 · MTP-DFlash2 package · no speculation
ninfer-serve ./NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4-w8a8 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --vision

# W4A4-W8A8 · MTP-DFlash2 package · MTP
ninfer-serve ./NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4-w8a8 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec mtp --draft-tokens 4 --lm-head-draft \
  --vision

# W4A4-W8A8 · MTP-DFlash2 package · DFlash2
ninfer-serve ./NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4-w8a8 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec dflash2 --draft-tokens 8 --lm-head-draft \
  --vision
```

Image request: OpenAI-style `image_url` part in `POST /v1/chat/completions`; `url` takes an `http(s)://` image link; a data URI of a local image also works, and `model` must match `--model-id`.

```bash
curl http://127.0.0.1:19931/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.8-27b-coder390-w4a4",
    "messages": [{"role": "user", "content": [
      {"type": "image_url", "image_url": {"url": "https://example.com/demo.png"}},
      {"type": "text", "text": "Describe this image."}
    ]}],
    "max_tokens": 2048
  }'
```

Health check: `curl -sf http://127.0.0.1:19931/health`. The chat endpoint is `POST /v1/chat/completions`; the request `model` must match `--model-id`.

**vLLM · INT4 W4A16 · MTP (built-in head) · text and images**

```bash
VLLM_USE_FLASHINFER_SAMPLER=0 \
vllm serve ./INT4/W4A16 \
  --trust-remote-code --dtype bfloat16 \
  --max-model-len 102400 --served-model-name qwen3.8-27b-coder390-int4-w4a16 \
  --gpu-memory-utilization 0.85 --max-num-seqs 8 \
  --reasoning-parser qwen3 \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}'
```

Images go as OpenAI-style `image_url` parts with the same server; no extra flag is needed:

```bash
curl -s http://127.0.0.1:8000/v1/chat/completions -H 'Content-Type: application/json' -d '{
  "model": "qwen3.8-27b-coder390-int4-w4a16",
  "messages": [{"role": "user", "content": [
    {"type": "image_url", "image_url": {"url": "https://example.com/chart.png"}},
    {"type": "text", "text": "Describe this image."}
  ]}],
  "max_tokens": 2048
}'
```

Remove `--speculative-config` to run without speculation. Tested on vLLM 0.28 (`VLLM_USE_FLASHINFER_SAMPLER=0` matches the tested setup); SGLang and NInfer were not tested with this package. `--reasoning-parser qwen3` returns the reasoning separately.

**vLLM · INT8 W8A8 (no speculation)**

```bash
VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel \
VLLM_USE_FLASHINFER_SAMPLER=0 \
vllm serve ./INT8/W8A8 \
  --trust-remote-code --dtype bfloat16 \
  --max-model-len 102400 --served-model-name qwen3.8-27b-coder390-int8-w8a8 \
  --gpu-memory-utilization 0.85 --max-num-seqs 8 \
  --reasoning-parser qwen3
```

On RTX PRO 6000 Blackwell, vLLM's Cutlass INT8 kernel is unavailable and the server will not start unless it is disabled with `VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel`; vLLM then uses its Triton INT8 kernel (the startup log shows `TritonInt8ScaledMMLinearKernel`). `VLLM_USE_FLASHINFER_SAMPLER=0` matches the tested setup. Tested on vLLM 0.28; SGLang cannot load this package (`ModelOptFp8Config` raises an error). `--reasoning-parser qwen3` returns the reasoning separately in `reasoning_content` (it was off during scoring).

**vLLM · INT8 W8A8 · MTP (external draft `INT8/W8A8/MTP-BF16/`)**

```bash
VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel \
VLLM_USE_FLASHINFER_SAMPLER=0 \
vllm serve ./INT8/W8A8 \
  --trust-remote-code --dtype bfloat16 \
  --max-model-len 102400 --served-model-name qwen3.8-27b-coder390-int8-w8a8 \
  --gpu-memory-utilization 0.85 --max-num-seqs 8 \
  --reasoning-parser qwen3 \
  --speculative-config '{"method":"mtp","model":"./INT8/W8A8/MTP-BF16","num_speculative_tokens":3}'
```

On an RTX PRO 6000 Blackwell, set `VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel` and `VLLM_USE_FLASHINFER_SAMPLER=0`, as in the command above. Both rows of the new table used those two settings.

**vLLM · INT8 W8A16 (no speculation)**

```bash
VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel VLLM_USE_FLASHINFER_SAMPLER=0 \
vllm serve ./INT8/W8A16 \
  --served-model-name qwen3.8-27b-coder390-int8-w8a16 \
  --trust-remote-code --max-model-len 102400 --max-num-seqs 8 \
  --gpu-memory-utilization 0.90 --reasoning-parser qwen3
```

**vLLM · INT8 W8A16 · MTP (external draft `INT8/W8A16/MTP-BF16/`)**

```bash
VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel VLLM_USE_FLASHINFER_SAMPLER=0 \
vllm serve ./INT8/W8A16 \
  --served-model-name qwen3.8-27b-coder390-int8-w8a16 \
  --trust-remote-code --max-model-len 102400 --max-num-seqs 8 \
  --gpu-memory-utilization 0.90 --reasoning-parser qwen3 \
  --speculative-config '{"method":"mtp","model":"./INT8/W8A16/MTP-BF16","num_speculative_tokens":3}'
```

**GGUF / GGUF-NInfer**

Load the `.ninfer` with NInfer-all (the `master` branch of `iamwavecut/ninfer-all`): the package keeps the GGUF quantization blocks, which other NInfer builds cannot read. llama.cpp needs an upstream build that supports `--spec-type draft-mtp`. NInfer's `--kv-capacity` is one KV pool shared by all requests; llama.cpp's `-c 409600 -np 4` splits the context evenly across 4 slots, so each request gets at most 102,400 tokens, enough for a single request to reach 94K. The chat endpoint is `POST /v1/chat/completions`; for NInfer the request `model` must match `--model-id`. Vision: `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` for llama.cpp `--mmproj` (629,247,008 bytes, sha256 `cae9799dc9196449b0d83f716e64af89d5cf65147510462e5a629a2aa23adb32`). Each `.ninfer` package carries the vision component; add `--vision` to `ninfer-serve` to accept images (see NInfer · vision below).

**16 GB VRAM / single-stream pick:** for 16 GB cards and single-user use, `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer` is the friendlier choice. It is the smallest NInfer package in this repo (13,568,617,472 bytes, about 12.6 GiB), has a built-in Q4_K MTP head and built-in vision (add `--vision`; no mmproj needed), and runs on both the official NInfer-all `master` and the community fork ninfer-fusion-kvmem. No 16 GB card was tested; this recommendation is by size. Start at 32K context and lower it if memory runs short.

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer \
  --model-id qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --max-context 32768 --kv-capacity 32768 --kv-dtype rk8v4 \
  --max-concurrency 1 --spec mtp --draft-tokens 4 --vision
```

**Community fork ninfer-fusion-kvmem:** the Q2 / Q3 / Q4 LynnStyle NInfer packages (`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer`, `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer`, `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer`) carry a built-in MTP head re-encoded as Q4_K and load and run MTP on both the official NInfer-all `master` and the community fork ninfer-fusion-kvmem (tested 2026-10-11). The `.gguf` files in `GGUF/` keep a Q4_0 MTP head, which llama.cpp supports. The Q8 MTP versions remain available as an alternative (same weights, only the MTP head re-encoded as Q8_0): `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf`, `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf` and `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf` for llama.cpp, and `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.ninfer`, `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.ninfer` and `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer` for NInfer (model ids `qwen3.8-27b-coder390-Q2LynnStyle-Q8Mtp`, `qwen3.8-27b-coder390-Q3LynnStyle-Q8Mtp`, `qwen3.8-27b-coder390-Q4LynnStyle-Q8Mtp`).

**MTP and DFlash2**: every package under `GGUF/` and `GGUF-NInfer/` has a built-in MTP head (Q2 / Q3 / Q4 LynnStyle use built-in **Q4** MTP: Q4_0 in the `.gguf`, Q4_K in the `-Q4MTP.ninfer`; their `-Q8MTP` versions use a Q8_0 MTP head). To enable it, add `--spec mtp --draft-tokens N` for NInfer or `--spec-type draft-mtp --spec-draft-n-max N` for llama.cpp; leave these out to run without speculation. DFlash2 is an external draft model and is not in these GGUF / NInfer packages; this repository does not ship a DFlash2 draft for GGUF / GGUF-NInfer. For DFlash2, use the `DFlash2-FP8/` draft that ships with the BF16 / FP8 / NVFP4 tiers in this repository (SGLang `--speculative-algorithm DFLASH`) or the `.ninfer` packages under `NVFP4-NInfer/` (`--spec dflash2`). MTP and DFlash2 are mutually exclusive: a server runs one or the other, never both.

#### GGUF · NInfer

**NInfer · GGUF Q3 LynnStyle-16G · MTP + vision (draft 4, recommended concurrency 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-Q3LynnStyle16G-MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-q3lynnstyle16g-mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4 --vision
```

For 16 GB VRAM / single-stream, start with `--max-context 32768 --kv-capacity 32768 --max-concurrency 1` and raise if memory allows. Vision is built into this `.ninfer` (Q8 tower); add `--vision`. GGUF for this tier stays text-only (use `--mmproj` on llama.cpp).

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

#### GGUF · llama.cpp

**llama.cpp · GGUF Q2 LynnStyle · MTP (representative; swap the `-m` path for Q3 / Q4 / Q6_K / Q8_0)**

```bash
llama-server -m ./GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf \
  -c 409600 -np 4 -ngl 99 --jinja \
  --host 127.0.0.1 --port 8080 \
  --alias qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --spec-type draft-mtp --spec-draft-n-max 4
```

To use another GGUF tier, only change `-m` to `...-Q3LynnStyle-MTP.gguf`, `...-Q4LynnStyle-MTP.gguf`, `...-Q6_K-MTP.gguf`, or `...-Q8_0-MTP.gguf` (and the `--alias`, e.g. `qwen3.8-27b-coder390-q6k-mtp`, `qwen3.8-27b-coder390-q8-mtp`). MTP is fused inside the GGUF (`blk.64`); do not attach an external draft; the log should show `creating MTP draft context against the target model`. For image input add `--mmproj ./GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`.

**llama.cpp · GGUF Q3 LynnStyle-16G · MTP (16 GB VRAM)**

```bash
llama-server -m ./GGUF/Qwen3.8-27B-Coder390-Q3LynnStyle16G-MTP.gguf \
  -c 32768 -np 1 -ngl 99 --jinja \
  --temp 1.0 --top-p 0.95 --top-k 20 \
  --host 127.0.0.1 --port 8080 \
  --alias qwen3.8-27b-coder390-q3lynnstyle16g-mtp \
  --spec-type draft-mtp --spec-draft-n-max 4
```

Not yet tested on a 16 GB card; the command above uses one slot at 32K context, raise `-c` / `-np` if memory allows. MTP is fused inside the GGUF (Q4_K, `blk.64`); do not attach an external draft. For image input add `--mmproj ./GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`. The three-suite scores for this tier were measured with llama.cpp + DFlash2 external draft (C4, 100K context, 94,208 generation cap, no timeout, xhigh). Speeds on one RTX PRO 6000 Blackwell: llama.cpp fused MTP 4096-cap long C1/C2/C4 = 31.9/46.6/78.1 tok/s (accept 0.597); NInfer 512-cap short C1/C2/C4/C8 = 33.5/44.7/77.4/127.0 tok/s (accept 0.488). Protocols differ.

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

### `FP8/` (main package: 19 files, 31,262,188,871 bytes)

`FP8/SHA256SUMS` covers the first 18 files below.

| File | Bytes | SHA256 |
|---|---:|---|
| `FP8/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `FP8/config.json` | 17,784 | `9e58e8daf2914c2d11c07449dc7f03bbb822ba39dec37c4c5b3bd1f623492f90` |
| `FP8/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `FP8/model.safetensors.index.json` | 135,976 | `989573833195e17342983c7fd109e010155c423a355068b5aceb6631fcee83f2` |
| `FP8/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `FP8/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `FP8/text-01.safetensors` | 2,542,796,928 | `54d83c1d36631de231876217a8e0c2483eccee8746369a482b79442bdfc5d958` |
| `FP8/text-02.safetensors` | 3,998,718,144 | `5b1e34725cd88924495765149ff816903d702180c72561c2e22e8377e2044fa8` |
| `FP8/text-03.safetensors` | 3,969,173,888 | `5e2376d6cce25aecf2d8901959f9d6f98801a0b2e98331f4088481bf839c9cf3` |
| `FP8/text-04.safetensors` | 3,925,079,000 | `669b87fd69d2de004073ed633f8e2890c8c9c90e1101bd59c859f1431b5cb967` |
| `FP8/text-05.safetensors` | 3,994,338,456 | `3f150179f9e3f03e2ef2e1afc805e7d745c1ab88dd72776fadf7c33f1d73ae67` |
| `FP8/text-06.safetensors` | 3,920,901,280 | `4d658974b7efb906972bc66cb4fd6dc7f1b7ac1fa79a7db068442314e3bf75d4` |
| `FP8/text-07.safetensors` | 3,972,285,640 | `d155ad91985b57e2515cea321a474708dd162665d1f5870df1c85601a2ca9b2c` |
| `FP8/text-08.safetensors` | 3,147,842,216 | `e37d025cd9bcacdd00fa0969f5c827d2504019c020585dfe1aca3934152b7700` |
| `FP8/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `FP8/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `FP8/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `FP8/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `FP8/SHA256SUMS` | 1,570 | (checksum list itself) |

### `FP8/DFlash2-FP8/` (4 files, 2,407,384,680 bytes)

| File | Bytes | SHA256 |
|---|---:|---|
| `FP8/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `FP8/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `FP8/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `FP8/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `BF16/` (12 files, 55,583,125,732 bytes; the DFlash2 subdirectory is listed separately below)

`BF16/SHA256SUMS` covers the first 11 files below. `mtp-bf16.safetensors` is byte-identical to the file of the same name in the FP8 package.

| File | Bytes | SHA256 |
|---|---:|---|
| `BF16/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `BF16/config.json` | 3,799 | `b25e4020b4f791f2b20a3bf486f7ded5116fa0680cf7aa2ac50f80ee353663ce` |
| `BF16/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `BF16/model-00001-of-00002.safetensors` | 49,825,162,976 | `ed83b8a41d447f4592c490b6135917419aea00fc7dbf9d6f5eb9525631f86fe0` |
| `BF16/model-00002-of-00002.safetensors` | 4,888,445,168 | `5c56330027c0eb9a776e89f80ef1643e60b1c2ae3adbbaf4b5142ebf7cb57271` |
| `BF16/model.safetensors.index.json` | 112,034 | `e8e177ff98a940337d496a0820e51c9fb68b2ab98fb68647d26aef9368dedeab` |
| `BF16/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `BF16/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `BF16/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `BF16/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `BF16/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `BF16/SHA256SUMS` | 990 | (checksum list itself) |

### `BF16/DFlash2-FP8/` (4 files, 2,407,384,680 bytes)

Byte-identical to `FP8/DFlash2-FP8/`.

| File | Bytes | SHA256 |
|---|---:|---|
| `BF16/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `BF16/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `BF16/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `BF16/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `NVFP4/W4A16/` (main package: 17 files, 20,613,406,953 bytes; the DFlash2 subdirectory is listed separately below)

`NVFP4/W4A16/SHA256SUMS` covers the first 16 files below; its own SHA256 is `ecc28d31be0d97e23509af61625251af14980db5b67189a1d1ca75a3fc9652f3`. `mtp-bf16.safetensors` is byte-identical to the file of the same name in the FP8 package.

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4/W4A16/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `NVFP4/W4A16/config.json` | 69,785 | `e71fd7b2cbade1ebb8be0382c81f7bf69eb1e039e30734914378d2c41217ef62` |
| `NVFP4/W4A16/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `NVFP4/W4A16/hf_quant_config.json` | 65,978 | `2ff46ad6bc27eb740e29831e642522ee4c110fea1ae9520b89272566b0d12d62` |
| `NVFP4/W4A16/model.safetensors.index.json` | 171,578 | `13651163cd9c1c20af460e6595616075a1f0d7f5995a3efc46d3ac449bc4f51e` |
| `NVFP4/W4A16/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `NVFP4/W4A16/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `NVFP4/W4A16/text-01.safetensors` | 3,994,732,420 | `dfdd15ab6b889eee01357d38910552bb0968248df0e21a9564d7ae29482d3139` |
| `NVFP4/W4A16/text-02.safetensors` | 3,981,611,096 | `8e4a2a7b4c9325c27380a41de0fb51028065ff97090af9d4213cb5a50629d517` |
| `NVFP4/W4A16/text-03.safetensors` | 3,960,207,028 | `c92929b575321e080d0ea2ca7c1a26b49fa638a8d03bacfef2cd0b6f83237689` |
| `NVFP4/W4A16/text-04.safetensors` | 3,983,003,152 | `feb69e1a4c7a374f1a11cf3e4af5d70fdd870963519e71469eb067a86fb35634` |
| `NVFP4/W4A16/text-05.safetensors` | 2,902,646,528 | `28dda5f9a39b83736ae458c2e626b429bbd18e408be63ef598dbb47327c97e3e` |
| `NVFP4/W4A16/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `NVFP4/W4A16/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `NVFP4/W4A16/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `NVFP4/W4A16/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4/W4A16/SHA256SUMS` | 1,399 | `ecc28d31be0d97e23509af61625251af14980db5b67189a1d1ca75a3fc9652f3` |

### `NVFP4/W4A16/DFlash2-FP8/` (4 files, 2,407,384,680 bytes)

Byte-identical to `FP8/DFlash2-FP8/`.

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4/W4A16/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `NVFP4/W4A16/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `NVFP4/W4A16/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `NVFP4/W4A16/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `NVFP4/W4A4/` (main package: 17 files, 20,613,386,462 bytes; the DFlash2 subdirectory is listed separately below)

`NVFP4/W4A4/SHA256SUMS` covers the first 16 files below; its own SHA256 is `5aea8bb9c1f1979661bfa5c1216de7aafeb64cd708aa8cc71f3b185c224cfde0`. `mtp-bf16.safetensors` is byte-identical to the file of the same name in the FP8 package.

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4/W4A4/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `NVFP4/W4A4/config.json` | 18,130 | `4df9be90e61070a553447129e504fea7be8e60dc22ae9e9f7a85bdfc140c0054` |
| `NVFP4/W4A4/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `NVFP4/W4A4/hf_quant_config.json` | 13,956 | `d3603810fba7548903ba2f3382fdd30f5704d3b6e0688e2dccf34fe023c11d31` |
| `NVFP4/W4A4/model.safetensors.index.json` | 207,580 | `541d828aed73b4df9f9fc86be7111aa404983d55d9797ca1cfb3e71474bfd3b7` |
| `NVFP4/W4A4/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `NVFP4/W4A4/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `NVFP4/W4A4/text-01.safetensors` | 3,994,737,240 | `1ea4cf8a0036b5d87815b65a38d0d2c00b37c010056a03d0db1fc72eb6c829bc` |
| `NVFP4/W4A4/text-02.safetensors` | 3,981,625,016 | `c9a0d2c3c506ad17da4dd47bf571326eef201e40db6f259a9d42971778033359` |
| `NVFP4/W4A4/text-03.safetensors` | 3,960,220,600 | `3c8778873d2ef08c512b7e457d61a6ac9ea047975e4723cd3804d0d18e86c1db` |
| `NVFP4/W4A4/text-04.safetensors` | 3,983,016,880 | `40081557adf0713f1624cdb2d1c53ea5fd2a30e09f5f964799457b23e4e2304d` |
| `NVFP4/W4A4/text-05.safetensors` | 2,902,647,672 | `0266ba0fa0354a4c409bc180c9d9a67ed12c915fc9886970745c87f8babcaa24` |
| `NVFP4/W4A4/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `NVFP4/W4A4/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `NVFP4/W4A4/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `NVFP4/W4A4/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4/W4A4/SHA256SUMS` | 1,399 | `5aea8bb9c1f1979661bfa5c1216de7aafeb64cd708aa8cc71f3b185c224cfde0` |

### `NVFP4/W4A4/DFlash2-FP8/` (4 files, 2,407,384,680 bytes)

Byte-identical to `FP8/DFlash2-FP8/`.

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4/W4A4/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `NVFP4/W4A4/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `NVFP4/W4A4/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `NVFP4/W4A4/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `NVFP4/W4A4-W8A8/` (main package: 18 files, 23,769,634,648 bytes; the DFlash2 subdirectory is listed separately below)

`NVFP4/W4A4-W8A8/SHA256SUMS` covers the first 17 files below; its own SHA256 is `c177f4907a7dd037efe91b8d34927dd3a3624227f259238b82db0f12f8b0b8e2`. `mtp-bf16.safetensors` is byte-identical to the file of the same name in the FP8 package.

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4/W4A4-W8A8/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `NVFP4/W4A4-W8A8/config.json` | 71,802 | `d1cc2af6971ae0bb776f5f36eb1c923546742fda3a83e6d8355720a652e27b5d` |
| `NVFP4/W4A4-W8A8/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `NVFP4/W4A4-W8A8/hf_quant_config.json` | 43,976 | `2bd65f6f325ea8e8e40c37b6e7d386633ac6236db6fcde3d7e9de128d961a599` |
| `NVFP4/W4A4-W8A8/model.safetensors.index.json` | 187,500 | `1257454a255efb01ba8047fe41bf34460b551c210db7cc8c4713f1c01150c69d` |
| `NVFP4/W4A4-W8A8/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `NVFP4/W4A4-W8A8/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `NVFP4/W4A4-W8A8/text-01.safetensors` | 3,981,847,464 | `b5502eb2c54c5a53ee08712c48935023ed924e0f054acb3573e1288095d2e3ff` |
| `NVFP4/W4A4-W8A8/text-02.safetensors` | 3,956,368,808 | `f08e7fccb4d2467af8b2b2d3bc587e6e8404b5764e9fc8e640ad0ff4f445d293` |
| `NVFP4/W4A4-W8A8/text-03.safetensors` | 3,956,368,928 | `8299287bb0e570efda02bcbe67c4bd9c5378b44bbf84c17ff062fc5ce6ba53e0` |
| `NVFP4/W4A4-W8A8/text-04.safetensors` | 3,967,919,248 | `bea560dda7b885cca987b8352e2ae659acaee70c3255fde7fa487c1fd73badf2` |
| `NVFP4/W4A4-W8A8/text-05.safetensors` | 3,573,130,520 | `a969faa5f2a3963450ad64bb84664035676c426877499593aea91080643ba6fa` |
| `NVFP4/W4A4-W8A8/text-06.safetensors` | 2,542,796,928 | `54d83c1d36631de231876217a8e0c2483eccee8746369a482b79442bdfc5d958` |
| `NVFP4/W4A4-W8A8/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `NVFP4/W4A4-W8A8/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `NVFP4/W4A4-W8A8/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `NVFP4/W4A4-W8A8/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4/W4A4-W8A8/SHA256SUMS` | 1,485 | `c177f4907a7dd037efe91b8d34927dd3a3624227f259238b82db0f12f8b0b8e2` |

### `NVFP4/W4A4-W8A8/DFlash2-FP8/` (4 files, 2,407,384,680 bytes)

Byte-identical to `FP8/DFlash2-FP8/`.

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4/W4A4-W8A8/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `NVFP4/W4A4-W8A8/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `NVFP4/W4A4-W8A8/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `NVFP4/W4A4-W8A8/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `evaluation/`

Score, benchmark, smoke-test (static FP8 and BF16), and calibration records. `evaluation/SHA256SUMS` covers the first 22 files below (23 files in total, including the checksum list itself). `NVFP4_*.results.summary.json` are the raw summaries of the three suites for the three NVFP4 tiers (`NVFP4_MIXED_*` is the W4A4-W8A8 tier).

| File | Bytes | SHA256 |
|---|---:|---|
| `evaluation/SCORES_STATICFP8.json` | 3,935 | `eba280071a75fc8dd90e5866df783a68ccd08bdb4d4dde85c062f7d398ea0eb0` |
| `evaluation/BENCH_STATICFP8.json` | 6,511 | `c62c6c82f234a27fa93faf691d1d4ee01a2408a18bbe94efafe341e4ad10db20` |
| `evaluation/BENCH_STATICFP8.md` | 1,405 | `ea662952b73446d5b88422b2a3dbcc215829521cc001cb26ad492caa137fa2ac` |
| `evaluation/SMOKE_STATICFP8.json` | 2,119 | `1a2383ad0f8e26f02ec7d65db418fea2bd50e73458ee247cc9d2f9322ffbb833` |
| `evaluation/SCORES_BF16.json` | 4,279 | `76e921712bab0577853499d3f67440de6f3577f4818c40184f4b0580e5f7a77e` |
| `evaluation/SMOKE_BF16.json` | 889 | `01ea5e4518615af2a3c574fa49ae6f2a4819482bbaafce2695b62016b14a582f` |
| `evaluation/SCORES_NVFP4_W4A16.json` | 3,319 | `7294901f3493f593e0de6d7f95b860c44578780300aebcb52bca6f06ead1ddfd` |
| `evaluation/BENCH_NVFP4_W4A16.json` | 3,992 | `1877fe3e4126de72ad1165a1e0f5d1dd569f73f1dcd16a93249c389b3d47f2d3` |
| `evaluation/SCORES_NVFP4_W4A4.json` | 3,212 | `eee169bb6cde4d048d12d604a72c7570b0ebd0fee88a3c19d39ad4493a912f30` |
| `evaluation/BENCH_NVFP4_W4A4.json` | 3,922 | `2ebedf7e221f69765364a73deaca459a9636a4c190b2cbde06de8d119a15f4a7` |
| `evaluation/SCORES_NVFP4_MIXED.json` | 3,063 | `845027e6324b5300ed5ce306b3515b559f75b5c0e8ef1aac4d1b98d62d135454` |
| `evaluation/BENCH_NVFP4_MIXED.json` | 4,038 | `3d6f348425b6fd184d620c101a803139d7bcc0d620ff3237c28cc627e8f85ca7` |
| `evaluation/NVFP4_CALIBRATION_METHOD.md` | 3,712 | `e3678dbe9020a83998a5c66207b515376defebd78e6fadf4f63e55059785e03a` |
| `evaluation/NVFP4_W4A16_gpqa.results.summary.json` | 1,182 | `4835f8cf4b403047487b0a52db88574a2125ba103a30404b8b9e97e7112511bd` |
| `evaluation/NVFP4_W4A16_lcb.results.summary.json` | 2,642 | `56990657d101c2ce47b44d5fcdcb498a286bbf6093ae7790cde5809ba266d5a1` |
| `evaluation/NVFP4_W4A16_mmlu.results.summary.json` | 4,075 | `e9d507b5da71621032a13f487eb60159e0369c025ed12c4fa613e70b6f0f71e5` |
| `evaluation/NVFP4_W4A4_gpqa.results.summary.json` | 1,189 | `961b3f98b4a54d78d1983896a0b12b10a3d1e7facf456f594793dc7bbefb5e70` |
| `evaluation/NVFP4_W4A4_lcb.results.summary.json` | 2,640 | `bd371e898121ee5dd6fda47065254cc2137ba783b466b3830f0c58d631137688` |
| `evaluation/NVFP4_W4A4_mmlu.results.summary.json` | 4,076 | `b468cf81854562e0e20bf232ddd13b68ed58e10a4da840e6bd3c20564d20f74a` |
| `evaluation/NVFP4_MIXED_gpqa.results.summary.json` | 1,171 | `72c000ffc4ff15db8d542b6d9d924c5795ad491d946dee0f6c3f11b0e62151f1` |
| `evaluation/NVFP4_MIXED_lcb.results.summary.json` | 2,641 | `7e3d3146dd98954ef80358ce88f5505798f77427c1a5ddf73c65dd728cf3afc2` |
| `evaluation/NVFP4_MIXED_mmlu.results.summary.json` | 4,077 | `3088c6254dad8af25ace3b44f4cfa688b192eca98f693afa1c595df121cb9afb` |
| `evaluation/SHA256SUMS` | 2,071 | (checksum list itself) |

### Verification

```bash
(cd FP8 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd BF16 && sha256sum -c SHA256SUMS)
(cd NVFP4/W4A16 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd NVFP4/W4A4 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd NVFP4/W4A4-W8A8 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd NVFP4-NInfer/W4A4 && sha256sum -c SHA256SUMS)
(cd NVFP4-NInfer/W4A4-W8A8 && sha256sum -c SHA256SUMS)
(cd INT4/W4A16 && sha256sum -c SHA256SUMS)
(cd INT8/W8A8 && sha256sum -c SHA256SUMS && cd MTP-BF16 && sha256sum -c SHA256SUMS)
(cd INT8/W8A16 && sha256sum -c SHA256SUMS && cd MTP-BF16 && sha256sum -c SHA256SUMS)
(cd GGUF && sha256sum -c SHA256SUMS)
(cd GGUF-NInfer && sha256sum -c SHA256SUMS)
(cd evaluation && sha256sum -c SHA256SUMS)
```

## NInfer loading notes

- Only the NInfer engine can load `.ninfer`; SGLang, vLLM, llama.cpp, and transformers cannot.
- Use `ninfer-serve` from official NInfer ([`Neroued/ninfer`](https://github.com/Neroued/ninfer), `master` branch); no patches are needed. (Only the GGUF-derived `.ninfer` packages need NInfer-all.) Tested on one RTX PRO 6000 Blackwell (compute capability 12.0); NInfer supports at most 8 concurrent requests.
- `NVFP4-NInfer/W4A4/` and `NVFP4-NInfer/W4A4-W8A8/` each hold one `.ninfer` file with MTP and DFlash2: the text path is the same one scored on 2026-10-05, and the package also carries a Q8 MTP head, the DFlash2 draft, the proposal head, and (since 2026-10-09) the vision component, so `--vision` enables image input; the `vision-bf16.safetensors` in the same folder is the BF16 source of that part and is not needed at run time. The MTP projections are Q8 because several of their matrix shapes have no BF16 kernel in NInfer, and a BF16 MTP makes the server exit while building the compute graph.
- MTP and DFlash2 are mutually exclusive per launch (`--spec mtp` or `--spec dflash2`); `--lm-head-draft` must be used together with `--spec`. MTP accepts 1–5 draft tokens and DFlash2 1–15; the NInfer commands under Commands above use 4 and 8, as in the benchmark. The DFlash2 draft is built into the package, so no separate `DFlash2-FP8/` directory is needed.
- These context flags are verified to start: `--max-context 102400 --kv-capacity 819200 --max-concurrency 8 --kv-dtype fp8`. `--kv-capacity` must fall between `max-context` and `max-context × max-concurrency`; 819,200 is exactly 8 × 102,400.
- The HF packages under the NVFP4 directories still run in SGLang (MTP or DFlash2); they are not interchangeable with the NInfer packages.

### NInfer V2 packages (Tesla V100 only)

The four packages whose filenames contain `NInferV2-NOT-FOR-V3` are for Tesla V100 only (ninfer-v100 branch); on any other GPU, use the packages without this suffix.

- The 4 packages whose filenames contain `NInferV2-NOT-FOR-V3` use the NInfer **V2** container and are only for the Tesla V100 `ninfer-v100` branch. Official NInfer (`ninfer-serve`) reads V3 only and rejects these files; on other GPUs, use the V3 packages above (without `NInferV2` in the name). Do not rename the V2 packages to V3 filenames or use them to replace the V3 packages.
- The two text-only packages (`Qwen3.8-27B-Coder390-W4A4-NInferV2-NOT-FOR-V3.ninfer`, `Qwen3.8-27B-Coder390-W4A4-W8A8-NInferV2-NOT-FOR-V3.ninfer`) have no MTP or DFlash2, so do not pass `--spec`; the two MTP-DFlash2 packages (`…-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer`) accept `--spec mtp` or `--spec dflash2`; they already contain the MTP head and the DFlash2 draft, so no external draft model is needed. None of the four V2 packages includes the vision component, so they cannot take images (no `--vision`); for image input use the V3 packages.
- V100 has no NVFP4 KV or K8V4 KV, so do not use the V3 flags `--kv-dtype rk8v4` or `--kv-capacity 819200`; when serving on V100, add `--prefill-chunk 2048`.
- The V2 packages have not been separately evaluated; they have only passed SHA256 verification. In `SHA256SUMS`, the two V2 lines come after a `#` comment line, separate from the V3 lines.

```bash
# V100 ninfer-v100 branch · text-only package (no --spec)
ninfer ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-NInferV2-NOT-FOR-V3.ninfer \
  --prompt "Explain prefill and decode in three sentences." \
  --max-context 8192 \
  --max-new 256

# V100 ninfer-v100 branch · MTP-DFlash2 package (MTP on)
ninfer ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer \
  --prompt "Explain prefill and decode in three sentences." \
  --max-context 8192 \
  --max-new 256 \
  --spec mtp --draft-tokens 3
```

### `NVFP4-NInfer/W4A4/` (5 files, 68,925,700,831 bytes)

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer` | 23,773,675,264 | `3c2d39f364a8932c82b41d4c424c940285573b0309481a67c2fde048368bf808` |
| `NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-NInferV2-NOT-FOR-V3.ninfer` | 20,752,831,236 | `eac9e3d47fe6731c021d7154fd2f801a8263ac6d00e6d16834e54947ee58bcf8` |
| `NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer` | 23,477,696,516 | `e93f3b83f7589fdb776ce25a0cdef98ed1892e101ef564fdb844a5aacff13d22` |
| `NVFP4-NInfer/W4A4/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4-NInfer/W4A4/SHA256SUMS` | 591 | `1b84a36b7b7c150376bdb00c61c629565040b92b0b8a84784dcdcb8c35dc6b3e` |

### `NVFP4-NInfer/W4A4-W8A8/` (5 files, 68,925,700,846 bytes)

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8-MTP-DFlash2.ninfer` | 23,773,675,264 | `cccfbf0ba3ec4e86837e8e6481ec32ee3e10636633e421429f19ea3ea97926e2` |
| `NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-W4A4-W8A8-NInferV2-NOT-FOR-V3.ninfer` | 20,752,831,236 | `01a4440f77dcdac66906e1bb061e1c38c6b236b805ff7bcb644aedf90f06a038` |
| `NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-W4A4-W8A8-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer` | 23,477,696,516 | `099b2d00fa3982d601218d6587dc25222cc21ef708de7dab8b2e2c0bee60da74` |
| `NVFP4-NInfer/W4A4-W8A8/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4-NInfer/W4A4-W8A8/SHA256SUMS` | 606 | `78a23ee97290b0d82b7d2a8fb163a2dab4479592568d36bd093ab82ad8747549` |

## INT4 W4A16 notes

- Text and image: the architecture is `Qwen3_5ForConditionalGeneration` (64 text layers, linear and full attention alternating 3:1). The BF16 vision tower is a separate file (`model_visual.safetensors`, 333 tensors, 921,497,224 bytes, the same file as in `INT8/W8A8/`), with `preprocessor_config.json` / `video_preprocessor_config.json`. The built-in MTP head is BF16 (`model_mtp.safetensors`, 15 tensors). No DFlash2 draft.
- Quantization: GPTQ W4A16 with llm-compressor, INT4 weights, symmetric, group size 128, static activation order, dampening 0.01; activations stay BF16. `lm_head`, the token embedding, the MTP head and the vision tower are not quantized. Calibration: 512 sequences × 4,096 tokens rebuilt from this model's RL training rollouts. Quantization metadata uses the compressed-tensors (`pack-quantized`) format; `recipe.yaml` is the llm-compressor recipe.
- BPW 5.25: `model.safetensors` (17,646,891,544 bytes, text weights only) × 8 ÷ the text parameter count 26,895,998,464; the MTP and vision files are not counted.
- Image + MTP check (2026-10-09, one RTX PRO 6000, vLLM 0.28, 3 draft tokens): the image prompt was answered correctly with thinking on and off.
- Loading: validated only on vLLM 0.28. `VLLM_LOAD.json` records the load settings.

### `INT4/W4A16/` (14 files, 19,437,985,972 bytes)

| File | Bytes | SHA256 |
|---|---:|---|
| `INT4/W4A16/VLLM_LOAD.json` | 510 | `7542f50d98101cd5d9406aaa70be1d52f76cbd235f8c48cee374655a053006a6` |
| `INT4/W4A16/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `INT4/W4A16/config.json` | 5,138 | `31e02ecfdf892d0db6bde3c1b97d8ce5a564e142a344fee4a9d3412e68524fbd` |
| `INT4/W4A16/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `INT4/W4A16/model.safetensors` | 17,646,891,544 | `e74d9161d57af066d7a8855526742561a187f81d67819ca10709a58c82b7eca7` |
| `INT4/W4A16/model.safetensors.index.json` | 189,311 | `5820a85fbea69c56cc34f33903c1a7c94af92736c779c2e9c934e538bac7dbd9` |
| `INT4/W4A16/model_mtp.safetensors` | 849,400,392 | `1d8268aa85ace093a561e3e7b63b9d390dac1cd55a90cd55b5ec509c3c9da9fe` |
| `INT4/W4A16/model_visual.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `INT4/W4A16/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `INT4/W4A16/recipe.yaml` | 359 | `3211d4cd0d4e5a3aca00b86b7db7ccf4890f07565c5474ba50eda1a1e3f68526` |
| `INT4/W4A16/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `INT4/W4A16/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `INT4/W4A16/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `INT4/W4A16/SHA256SUMS` | 1,153 | `744e89c9524117579510637c5b194f893cc9cd013b7fcd5029d2fe073a4b3dd2` |

## INT8 W8A8 notes

- Text and image (since 2026-10-09): the architecture is `Qwen3_5ForConditionalGeneration` (64 text layers, linear and full attention alternating 3:1). The BF16 vision tower from the BF16 tier is a separate file (`model_visual.safetensors`, 333 tensors, 921,497,224 bytes), with `preprocessor_config.json` / `video_preprocessor_config.json`; it is excluded from quantization. The 8 INT8 weight files are unchanged. The package has no embedded MTP head (use `MTP-BF16/`) and no DFlash2 draft. Checked on one RTX PRO 6000 on 2026-10-09 (vLLM 0.28, Cutlass INT8 kernel disabled, `MTP-BF16/` with 3 draft tokens): the image prompt was answered correctly, text output was normal, accept length 3.21, single-request decode 86 tok/s.
- Quantization: SmoothQuant + INT8 W8A8. Weights are quantized to INT8 per output channel, and activations are quantized to INT8 per token at runtime; the SmoothQuant pre-scale is folded into the weights, so no inference-engine patch is needed. Quantization metadata uses the compressed-tensors (`int-quantized`) format.
- Layer layout: MLP gate/up/down, full-attention q/k/v/o, and linear-attention `in_proj_qkv` / `in_proj_z` / `out_proj` make up 400 INT8 Linear layers; linear-attention `in_proj_a` / `in_proj_b` and `lm_head`, 97 in total, stay BF16; linear-attention control branches such as `A_log`, `dt_bias`, `norm`, and `conv1d` also stay BF16.
- Calibration and error: 512 calibration samples; held-out NLL rises from 0.50535 (BF16) to 0.52812, a perplexity ratio of 1.023 (measured before the pre-scale was folded into the weights).
- Loading: validated only on vLLM 0.28; not for SGLang or NInfer. `VLLM_LOAD.json` records the load requirements. On RTX PRO 6000 Blackwell the Cutlass INT8 kernel must be disabled; see Commands above.
- MTP draft: `INT8/W8A8/MTP-BF16/` holds the BF16 MTP tensors only. Checked on one RTX PRO 6000 on 2026-10-09 (vLLM 0.28, Cutlass INT8 kernel disabled, `num_speculative_tokens=3`): mean accept length 2.74–2.90.

### `INT8/W8A8/` (19 files, 30,422,466,299 bytes)

| File | Bytes | SHA256 |
|---|---:|---|
| `INT8/W8A8/VLLM_LOAD.json` | 329 | `b1101c2ef1d53e76f132686a15079068fc76ad2ae139514817e088c6223adf7b` |
| `INT8/W8A8/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `INT8/W8A8/config.json` | 25,592 | `478564df2dc7566492e2794b68c976491a8d6e98a604e2e307da4535ea3029eb` |
| `INT8/W8A8/generation_config.json` | 214 | `a4cef85934ea1fdcb207944dbc6eee70dbbf16806874428556ae33023336c0a4` |
| `INT8/W8A8/model-00001-of-00008.safetensors` | 3,978,325,744 | `f8f7ecb52576f50108d2a9335074e5621dd5a0c2b5ee92b830929c8acc34900a` |
| `INT8/W8A8/model-00002-of-00008.safetensors` | 3,990,728,496 | `73c182d4362ca9351329eb9c812aa44f627631d1d1866868a326010dc8387a45` |
| `INT8/W8A8/model-00003-of-00008.safetensors` | 3,927,632,952 | `59510687bfca9272147d8153b0d3cc55a2672a03c7326d7099d78a313cc4f102` |
| `INT8/W8A8/model-00004-of-00008.safetensors` | 3,995,896,560 | `fd9c32e4a11dec2dbf42dfb4e5da653bbbc01cd075ff60e593869022138e2efd` |
| `INT8/W8A8/model-00005-of-00008.safetensors` | 3,922,465,008 | `7478173acc5b54c80329756cf2bb81b5b804a0fa107217fbba5d0cb3353c3f77` |
| `INT8/W8A8/model-00006-of-00008.safetensors` | 3,984,366,360 | `cd53edb6084ec639667f2bdb997f7822db1eb758a15a06818fddcac603642127` |
| `INT8/W8A8/model-00007-of-00008.safetensors` | 3,138,579,112 | `997de745c52a87d54f684a461dd831f59d80e6b0c4c43e7ad75bd148cc87fdd5` |
| `INT8/W8A8/model-00008-of-00008.safetensors` | 2,542,796,896 | `6866cf8adcccc4cc6a00e74bc025f1a774fb52103b70f2674d0288272951a733` |
| `INT8/W8A8/model.safetensors.index.json` | 150,000 | `1eb8ea02681331fd897e247681411f1fad4e7cf421e6e133cdec7459e22f1ca7` |
| `INT8/W8A8/model_visual.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `INT8/W8A8/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `INT8/W8A8/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `INT8/W8A8/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `INT8/W8A8/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `INT8/W8A8/SHA256SUMS` | 1,705 | `f88bd3ed9476945cdb814e91fea5f18d2dc2b58c64cb187b5d23bfa364d28ebc` |

### `INT8/W8A8/MTP-BF16/` (3 files, 849,403,270 bytes)

`INT8/W8A8/MTP-BF16/SHA256SUMS` covers the first 2 files below; its own SHA256 is `313b058349deba83f05adb44b79f2f76ae668337834086f8dbcfacba131bf403`.

| File | Bytes | SHA256 |
|---|---:|---|
| `INT8/W8A8/MTP-BF16/config.json` | 2,681 | `7204cab1eb08579205ea9d8bbb556c396210d68693797df4333660b7bed6a41f` |
| `INT8/W8A8/MTP-BF16/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `INT8/W8A8/MTP-BF16/SHA256SUMS` | 165 | `313b058349deba83f05adb44b79f2f76ae668337834086f8dbcfacba131bf403` |

### `INT8/W8A16/` (main package + MTP-BF16 draft)

`INT8/W8A16/SHA256SUMS` covers the root files below; MTP hashes are in `INT8/W8A16/MTP-BF16/SHA256SUMS`.

| Path | Bytes | SHA256 |
|---|---:|---|
| `INT8/W8A16/VLLM_LOAD.json` | 619 | `45ad2233d5117157ae36998ccad835fecf26c6f312ac2d76b4ce18dc5dfd333c` |
| `INT8/W8A16/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `INT8/W8A16/config.json` | 5,141 | `4a4b2681cf80f9d73d83731f9bb2f94c031ffe7ad8260a5117ca351160a01b8e` |
| `INT8/W8A16/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `INT8/W8A16/model-00001-of-00002.safetensors` | 19,970,729,024 | `56df395c6e33c29e937f976ba6f1eab27301993d8a045343d1b678aedbd1f1b3` |
| `INT8/W8A16/model-00002-of-00002.safetensors` | 9,478,770,576 | `004c9641a2f2bc9d6906afeb5e73491d3679bedcb0e0e5f8747466f8066e5381` |
| `INT8/W8A16/model.safetensors.index.json` | 215,980 | `a1891443d49799ef92c47e4a00e2300b30e594eea7bd1bd608bd6023f4c40eea` |
| `INT8/W8A16/model_visual.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `INT8/W8A16/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `INT8/W8A16/recipe.yaml` | 969 | `34751e1269751f9e7d3b60e570bc8dacccbdeaab464ea36d06fee0ff8ba0637c` |
| `INT8/W8A16/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `INT8/W8A16/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `INT8/W8A16/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `INT8/W8A16/MTP-BF16/config.json` | 2,681 | `7204cab1eb08579205ea9d8bbb556c396210d68693797df4333660b7bed6a41f` |
| `INT8/W8A16/MTP-BF16/mtp-bf16.safetensors` | 849,400,392 | `1d8268aa85ace093a561e3e7b63b9d390dac1cd55a90cd55b5ec509c3c9da9fe` |
| `INT8/W8A16/SHA256SUMS` | 1,179 | `cfac30661e10381caf020d719661342f879f44c057f93cefcca3e14a6f12e09c` |
| `INT8/W8A16/MTP-BF16/SHA256SUMS` | 165 | `913083df00735f5895bbc7411d0884f3ddad8d35f6a742186bfa9df14c88c790` |

## GGUF Q2 LynnStyle notes

- Mixed-precision LynnStyle; lowest type reaches Q2; built-in **Q4 MTP** (not Q8). Scored before the built-in MTP head was attached (external Q8 MTP draft); same quantized weights: GPQA 177/198, MMLU 433/500, LCB 90/100. Reasoning P50/P70/P90: GPQA 2,989.5 / 8,923.8 / 27,156.1; MMLU 181 / 326.3 / 1,020.5; LCB 5,656.5 / 17,835.8 / 40,067.3.
- Size: GGUF 13,276,009,792 bytes (BPW 3.89), NInfer 13,568,617,472 bytes with vision (text + MTP BPW 3.89); denominator 27,320,697,856.
- Speeds: llama.cpp built-in Q4 MTP long bench C4 174.8 tok/s (4096 gen cap); NInfer short bench C8 521.0 tok/s (512 gen cap). Protocols differ.
- Launch GGUF and NInfer separately (MTP built-in); see Commands above. MTP and DFlash2 are mutually exclusive, and this repository ships no DFlash2 draft for GGUF.

## GGUF Q3 LynnStyle notes

- Mixed-precision LynnStyle; built-in **Q4 MTP** (not Q8). Scored before the built-in MTP head was attached (external Q8 MTP draft); same quantized weights: GPQA **173/198**, MMLU **449/500**, LCB **92/100**. Reasoning P50/P70/P90: GPQA 3,125.5 / 7,265.2 / 24,343.1; MMLU 148 / 279.3 / 923.4; LCB 4,421 / 14,232.2 / 34,946.
- Size: GGUF 17,303,770,432 bytes (BPW **5.07**), NInfer 17,596,369,920 bytes with vision (text + MTP BPW **5.07**); denominator 27,320,697,856.
- Speeds: llama.cpp fused MTP long bench C4 **191.8** tok/s (4096 gen cap); NInfer short bench C8 **512.3** tok/s (512 gen cap). Protocols differ.
- Launch GGUF and NInfer separately (MTP built-in). MTP and DFlash2 are mutually exclusive; this repository ships no DFlash2 draft for GGUF. See the GGUF-NInfer repository card for full launch commands.

## GGUF Q4 LynnStyle notes

- Mixed-precision LynnStyle; built-in **Q4 MTP** (not Q8). Scored before the built-in MTP head was attached (external Q8 MTP draft); same quantized weights: GPQA **175/198**, MMLU **448/500**, LCB **89/100**. Reasoning P50/P70/P90: GPQA 2,951.0 / 8,159.3 / 25,649.0; MMLU 164 / 312.9 / 1,077.7; LCB 3,669.5 / 14,810.5 / 38,182.1.
- Size: GGUF 19,620,406,592 bytes (BPW **5.75**), NInfer 19,913,006,080 bytes with vision (text + MTP BPW **5.74**); denominator 27,320,697,856.
- Speeds: llama.cpp fused MTP long bench C4 **81.1** tok/s (4096 gen cap); NInfer short bench C8 **436.4** tok/s (512 gen cap). Protocols differ.
- Launch GGUF and NInfer separately (MTP built-in). MTP and DFlash2 are mutually exclusive; this repository ships no DFlash2 draft for GGUF. See the GGUF-NInfer repository card for full launch commands.

## GGUF Q8_0 notes

- Both packages share the Q8_0 backbone with a built-in MTP head; recommended NInfer + C8 + MTP (486.3 tok/s).
- `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf`: load with llama.cpp.
- `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer`: NInfer-all only; use `--max-context 102400 --kv-capacity 819200 --max-concurrency 8`.
- Scores from llama.cpp on the GGUF; reasoning tokens are split for all three benches.

## GGUF Q6_K notes

- Both packages share the same backbone quantization (Q6_K + imatrix + structure protection; see Quantization scheme above) and carry a built-in MTP head (GGUF `blk.64` is Q8_0; NInfer MTP attention/MLP weights are Q6_K, input projection Q8_0), so no external draft model is needed; NInfer + C4 + MTP is recommended.
- `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`: loads directly in llama.cpp; the GGUF architecture is `qwen35` with 65 blocks, the last of which (`blk.64`) is MTP.
- `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer`: loadable only by NInfer-all; SGLang, vLLM, llama.cpp, and transformers cannot read it.
- Vision: llama.cpp uses `--mmproj GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` (629,247,008 bytes); each `.ninfer` package carries the vision component (add `--vision` under NInfer); `GGUF-NInfer/vision-bf16.safetensors` (921,497,224 bytes) is the BF16 source of that part and is not needed at run time.
- Scores were measured with the GGUF package on llama.cpp; the LCB eval script is not compatible with the NInfer API (its replies are not valid JSON), which is an eval-script issue rather than a model-quality issue, so LCB is scored on llama.cpp.

### `GGUF/` (11 files: Q3+Q4+Q2+Q8+Q6 + Q3/Q4/Q2 Q8MTP + Q8 MTP draft + mmproj + SHA256SUMS)

| File | Bytes | SHA256 |
|---|---:|---|
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.gguf` | 17,303,770,432 | `9985b3d41fc7dc0bb5d493f7523d4515504912a3a7fc830f66e0fd2f90f9fd95` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.gguf` | 19,620,406,592 | `56c7c605a59764d9f0bb645d4eb335f1574af2c9e74020386139597df0e872f5` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf` | 13,276,009,792 | `cad973b3b7cc0d86bd39968209268318a746673c12c9536e5c37408baa7b5e6e` |
| `GGUF/Qwen3.8-27B-Coder390-Q3LynnStyle16G-MTP.gguf` | 13,276,009,920 | `3872d17684a1b71d38fd36eb5ace047ac61bab11799926455de933fe0b3e60e1` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-Q3LynnStyle16G-MTP.ninfer` | 13,765,136,896 | `d9459f94883dde338cbd6ac07059bc92b4842fdba904a30a8cc00969f7dfb423` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf` | 13,488,346,432 | `62fd6cf6079dfb02b3e3aab68e39b4cdc6a471a51a82b56c9a76068e961d8a4a` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf` | 17,516,107,072 | `2c74a65df9d229bfba2eb3a878a25b84d4035d1be4061c9a665af213d98cae58` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf` | 19,832,743,232 | `5e2a1784298f696cb38f063962da0ad4acd1fd020c6e7c6e520df54acf8f57eb` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf` | 29,069,202,688 | `b24e8c5fe3f2b282cce841400c740fcaca48afcdcf9e991f7bbe9a59a78cabfe` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf` | 23,177,516,384 | `302597c53d1b00f7230b53a8a050831390a4371e92a80c1ac644fa920af76ab1` |
| `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` | 629,247,008 | `cae9799dc9196449b0d83f716e64af89d5cf65147510462e5a629a2aa23adb32` |
| `GGUF/mtp-Qwen3.8-27B-Coder390-EfficientThink-Q8_0.gguf` | 3,164,006,656 | `50a030e852289eed86065e2e2de57d89241174e99faa2c1c2f06c29c270789ee` |
| `GGUF/SHA256SUMS` | 1,187 | `7677cef32b796c8c54d18592e8d198a14563a994496c8161b84ab7bdba30d183` |

### `GGUF-NInfer/` (10 files: Q3+Q4+Q2 -Q4MTP (Q4_K MTP head) + Q8+Q6 + Q3/Q4/Q2 Q8MTP (Q8_0 MTP head) packages, all with vision + vision-bf16 (BF16 source, not needed at runtime) + SHA256SUMS)

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
| `GGUF-NInfer/SHA256SUMS` | 1,088 | `786409f76d95820fd18251d55d35ca8c36526412c0d8581645fdd24a73955d4a` |

### imatrix (published in the GGUF-NInfer repo)

The `imatrix/` folder of the GGUF-NInfer repo ([Hugging Face](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-GGUF-NInfer/tree/main/imatrix), [ModelScope](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-GGUF-NInfer/files)) holds the calibration text for the GGUF importance matrix, `coder390-imatrix-calibration.txt` (1,368 records = 171 problems × 8, rebuilt from the inputs of this model's RL training rollouts, 500,816 tokens, no benchmark questions), and `coder390-imatrix.gguf`, an imatrix recomputed from it on 2026-10-09 (BF16 GGUF of this model, `-c 512 --chunks 512`, 496 entries and 512 chunks, SHA256 `be0924f24bd82c05b28da0c1d803ef29c1961f60bf9e978a16ffe746ee2adcf1`). The set is functionally equivalent to, but not byte-identical with, the one used for the published GGUFs; the original imatrix data file was not kept.

## Known limitations

- On GPQA, the empty answers at all three precisions come from the same two molecular-biology questions; this is a long-standing issue with those questions, not a quantization effect.
- The long tail is not eliminated: accuracy is clearly lower for reasoning ≥48K (e.g., static FP8 LCB ≥48K is 2/8), and 3 LCB problems still hit the 94K cap.
- MMLU shows 445–450 sampling variation across precisions. Scores depend on the protocol above (100K context, 94,208-token cap, no timeout) and should not be compared directly with numbers from other protocols.
- Performance of the SGLang-format tiers was measured on a single RTX PRO 6000 Blackwell with SGLang: BF16 / static FP8 figures come from the static FP8 package, and each NVFP4 tier was measured on its own package. For these tiers vLLM was covered only by load and image smoke tests on the FP8 package (vLLM 0.28 + MTP: temporarily unavailable for FP8; use SGLang for now), and NVFP4 was not tested on vLLM; DFlash2 was validated only on SGLang. INT8 W8A8 and INT4 W4A16 were evaluated and benchmarked on vLLM 0.28, the NInfer packages on NInfer, and GGUF on llama.cpp and NInfer-all.
- NVFP4 GPQA (170, 167, and 172) is below the 178 of BF16 / FP8, MMLU (439, 440, and 442) is slightly below 445–450, and LCB (91, 92, and 88) is around 90; the calibration data comes from this model's own RLOO training data and contains no official evaluation problems. NVFP4 smoke tests were run only on SGLang (patch-free load, greedy parity, image request); MTP and DFlash2 are covered by the full benchmark runs.
- BF16 scores come from full-suite runs on the same weight shards; GPU smoke test of the BF16 package (2026-10-09, one RTX PRO 6000, SGLang 0.5.21 with the built-in MTP head, 3 steps / 4 draft tokens): the image prompt was answered correctly with thinking on and off; average accept length 3.43, about 81 tok/s for a single request.
- INT8 W8A8 runs only in vLLM (its scores were measured on text; image input was added on 2026-10-09); GPQA 175 is slightly below the 177 of the original Qwen3.8 27B (FP8); speeds come from a quick benchmark (requests per level equal to the concurrency, 512 generation cap) and are not directly comparable with the other tiers; GPQA / MMLU reasoning lengths were recounted from the raw text with the BF16 tokenizer; LCB kept no reasoning text, so it has no reasoning-length percentiles.
- GGUF Q8_0: GPQA 171 below original Qwen3.8 27B (FP8) 177; LCB truncations 3, empty 3; full triad on GGUF (llama.cpp) only; NInfer speed is same-caliber, llama.cpp is the quick protocol.
- GGUF Q6_K: GPQA 174 is below the 177 of the original Qwen3.8 27B (FP8); MMLU reasoning length is counted from the raw text with the BF16 tokenizer, and LCB kept no reasoning text, so it has no reasoning-length percentiles; the full triad was run only on the GGUF (llama.cpp), not separately on the NInfer package; speeds come from a quick benchmark (requests per level equal to the concurrency, 512 generation cap) and are not directly comparable with the other tiers; vision uses `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` (llama.cpp `--mmproj`); the NInfer package carries the vision component (`--vision`); image input was tested with llama.cpp + mmproj on Q3 / Q4 LynnStyle, Q6_K, and Q8_0, and with NInfer `--vision` on Q2 / Q3 / Q4 LynnStyle, Q6_K, and Q8_0.

## License and acknowledgements

Licensed under Apache-2.0, following the license of the base model Qwen3.8-27B.

Thanks to the Qwen team for the base model and the official FP8 scheme; to Opus5.5, GPT6Astra, Grok4.7, DSV4Pro, and K3 for problem writing, gold labels, teacher trajectories, data review, and the RLOO value review; and to the SGLang, vLLM, and DFlash communities.
<!-- CARD_EN_END -->

<!-- LANG_SEPARATOR -->

---

<!-- CARD_ZH_START -->
# Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2

![Coder390 FP8 对比原版 FP8](assets/header-fp8-vs-base-zh.png)

![NVFP4 · INT8 · NInfer](assets/coder390-nvfp4-int8-ninfer-zh.png)

![GGUF](assets/coder390-gguf-zh.png)

在 [Qwen3.8-27B-EfficientThink-SFT-SimPO-DFlash2](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2)(官方 [Qwen3.8-27B](https://modelscope.cn/models/Qwen/Qwen3.8-27B) 经 SFT + SimPO 后训练得到的模型)基础上继续做多轮 SFT 与 RLOO 后训练,专治原版「已有答案却停不下来、写满 94K 也不给最终答案」的问题。本仓库提供 **BF16**、**静态 FP8 Block128**、**NVFP4 W4A16**、**NVFP4 W4A4**、**NVFP4 W4A4-W8A8**(混合精度)五个 safetensors 档,均为完整多模态(文本 + 图像/视频)、内置官方 BF16 MTP,SGLang 免补丁加载(FP8 包另经 vLLM 冒烟验证);另有 **NInfer W4A4 / W4A4-W8A8**(`NVFP4-NInfer/`)、**INT4 W4A16**(`INT4/W4A16/`,文本 + 图像,vLLM)、**INT8 W8A8**(`INT8/W8A8/`,文本 + 图像)、**INT8 W8A16**(`INT8/W8A16/`,文本 + 图像)以及 **GGUF Q2 / Q3 / Q4 LynnStyle(另有 Q8 MTP 版)、Q6_K、Q8_0**(`GGUF/`、`GGUF-NInfer/`,内置 MTP)。

- **94K 截断大幅减少**:同口径下 GPQA 从 4 降到 1,LCB 从 13 降到 3。
- **三项全面不低于原版**:GPQA **178/198**、MMLU **450/500**、LCB **90/100**(静态 FP8),原版 FP8 为 177 / 444 / 83。
- **量化无损**:BF16、动态 FP8、静态 FP8 三种精度 GPQA、LCB 一题不差。
- **两种投机解码(互斥)**:DFlash2 单请求约 180 tok/s,MTP 约 91 tok/s,不开投机约 46 tok/s。

**相关仓库**

- GGUF / GGUF-NInfer（llama.cpp、NInfer，内置 MTP）：[Hugging Face](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-GGUF-NInfer) · [ModelScope](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-GGUF-NInfer)
- NVFP4-NInfer：[Hugging Face](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-NVFP4-NInfer) · [ModelScope](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-NVFP4-NInfer)

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
| MTP / DFlash2 | 内置 BF16 MTP 头 / 配套 DFlash2 投机解码草稿 |

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

**结果**:同口径下,GPQA 的 94K 截断从原版 Qwen3.8 27B(FP8)的 4 降到 1,LCB 从 13 降到 3,三项分数均不低于原版(均为 FP8 档;NVFP4 三档见下文成绩)。

## 成绩

**口径**:同一份 Coder390 合并权重;两张 RTX PRO 6000,每卡 C8,上下文 100K,生成上限 94,208,客户端不计超时,DFlash2 草稿,SGLang;GPQA 198、MMLU 500、LCB 100 全量;空答记错,截断但答对记对,失败样本全部留在分母里。

| 套题 | 原版 Qwen3.8 27B(FP8) | BF16 | 动态 FP8 | 静态 FP8 |
|---|---:|---:|---:|---:|
| GPQA | 177/198 | 178/198 | 178/198 | **178/198** |
| MMLU | 444/500 | 446/500 | 445/500 | **450/500** |
| LCB | 83/100 | 90/100 | 90/100 | **90/100** |

GPQA、LCB 三种精度一题不差;MMLU 在 445–450 之间,属于采样抖动,不是精度造成的。动态 FP8 是推理时对 BF16 权重在线量化,不另出包。

### 全档位:分数、思考长度、94K 截断与空答

思考长度取 `usage.reasoning_tokens`;94K 截断指写满生成上限。LCB 空答指没有提取到可运行代码的题数。原版 FP8、BF16、动态 FP8、静态 FP8 为两张 RTX PRO 6000、每卡 C8;NVFP4 三档为单张 RTX PRO 6000、C8,其余口径相同。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | 原版 Qwen3.8 27B(FP8) | 177/198 | 5,299 / 12,607 / 50,577 | 4 | 3 |
| GPQA | BF16 | **178/198** | **3,196** / **8,200** / **28,417** | **2** | **2** |
| GPQA | 动态 FP8 | **178/198** | **2,815** / **8,371** / **27,744** | **1** | **1** |
| GPQA | 静态 FP8 | **178/198** | **2,966** / **7,832** / **26,431** | **1** | **2** |
| GPQA | NVFP4 W4A16 | 170/198 | **2,965** / **9,667** / **28,433** | **2** | 3 |
| GPQA | NVFP4 W4A4 | 167/198 | **2,876** / **10,996** / **31,986** | **2** | 3 |
| GPQA | NVFP4 W4A4-W8A8 | 172/198 | **2,953** / **10,010** / **35,731** | **2** | 4 |
| MMLU | 原版 Qwen3.8 27B(FP8) | 444/500 | 205 / 373 / 1,622 | 1 | 0 |
| MMLU | BF16 | **446/500** | **154** / **252** / **779** | 1 | 0 |
| MMLU | 动态 FP8 | **445/500** | **138** / **271** / **881** | 1 | 0 |
| MMLU | 静态 FP8 | **450/500** | **154** / **279** / **937** | 1 | 0 |
| MMLU | NVFP4 W4A16 | 439/500 | **159** / **277** / **1,061** | 1 | 0 |
| MMLU | NVFP4 W4A4 | 440/500 | **168** / **306** / **967** | 2 | 0 |
| MMLU | NVFP4 W4A4-W8A8 | 442/500 | **157** / **273** / **778** | **0** | 0 |
| LCB | 原版 Qwen3.8 27B(FP8) | 83/100 | 8,388 / 24,241 / 94,208 | 13 | 13 |
| LCB | BF16 | **90/100** | **5,073** / **16,033** / **38,911** | **2** | **2** |
| LCB | 动态 FP8 | **90/100** | **4,791** / **15,866** / **41,168** | **4** | **4** |
| LCB | 静态 FP8 | **90/100** | **4,511** / **16,027** / **43,992** | **3** | **3** |
| LCB | NVFP4 W4A16 | **91/100** | **5,119** / **15,790** / **47,768** | **4** | **3** |
| LCB | NVFP4 W4A4 | **92/100** | **6,338** / **15,771** / **54,096** | **3** | **3** |
| LCB | NVFP4 W4A4-W8A8 | **88/100** | **4,731** / **15,122** / **41,344** | **2** | **1** |

加粗表示优于原版 Qwen3.8 27B(FP8):分数更高,或 P50 / P70 / P90、94K 截断、空答更低;等于或不如原版的不加粗。

LCB 改善最明显:原版 13 条 94K 截断全是空代码(截断 13、空答 13),Coder390 各档降到 2–4 条。W4A4 的 3 条是第 0、53、96 题(成绩文件中的题目编号),同样是截断后没有代码;W4A16 的 4 条中,第 6、7、54 题没有代码,第 53 题有 20 个字符的代码但答错;W4A4-W8A8 的 2 条中,第 11 题没有代码,第 6 题有 2,338 个字符的代码但答错。GPQA 的 94K 截断原版 4 条,各档 1–2 条;MMLU 原版 1 条,各档 0–2 条,没有明显变化。

<details open>
<summary>六种精度明细(按思考长度分桶)</summary>

分桶为「答对/该桶题数」,按思考长度左闭右开。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 | <2K | 2–12K | 12–24K | 24–48K | ≥48K |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| GPQA | BF16 | 178/198 | 3,196 / 8,200 / 28,417 | 2 | 2 | 80/85 | 66/68 | 17/20 | 12/18 | 3/7 |
| GPQA | 动态 FP8 | 178/198 | 2,815 / 8,371 / 27,744 | 1 | 1 | 78/81 | 68/70 | 18/21 | 11/17 | 3/9 |
| GPQA | 静态 FP8 | 178/198 | 2,966 / 7,832 / 26,431 | 1 | 2 | 82/84 | 68/74 | 17/19 | 9/17 | 2/4 |
| GPQA | NVFP4 W4A16 | 170/198 | 2,965 / 9,667 / 28,433 | 2 | 3 | 77/80 | 64/70 | 17/21 | 8/17 | 4/10 |
| GPQA | NVFP4 W4A4 | 167/198 | 2,876 / 10,996 / 31,986 | 2 | 3 | 76/82 | 58/60 | 20/23 | 12/26 | 1/7 |
| GPQA | NVFP4 W4A4-W8A8 | 172/198 | 2,953 / 10,010 / 35,731 | 2 | 4 | 79/82 | 58/63 | 19/22 | 14/22 | 2/9 |
| MMLU | BF16 | 446/500 | 154 / 252 / 779 | 1 | 0 | 432/472 | 13/23 | 1/3 | 0/0 | 0/2 |
| MMLU | 动态 FP8 | 445/500 | 138 / 271 / 881 | 1 | 0 | 436/477 | 8/21 | 0/1 | 0/0 | 1/1 |
| MMLU | 静态 FP8 | 450/500 | 154 / 279 / 937 | 1 | 0 | 435/469 | 13/27 | 2/3 | 0/0 | 0/1 |
| MMLU | NVFP4 W4A16 | 439/500 | 159 / 277 / 1,061 | 1 | 0 | 427/471 | 11/26 | 0/1 | 1/1 | 0/1 |
| MMLU | NVFP4 W4A4 | 440/500 | 168 / 306 / 967 | 2 | 0 | 426/469 | 13/28 | 0/1 | 0/0 | 1/2 |
| MMLU | NVFP4 W4A4-W8A8 | 442/500 | 157 / 273 / 778 | 0 | 0 | 432/477 | 8/20 | 1/2 | 1/1 | 0/0 |
| LCB | BF16 | 90/100 | 5,073 / 16,033 / 38,911 | 2 | 2 | 40/40 | 25/26 | 11/14 | 9/11 | 5/9 |
| LCB | 动态 FP8 | 90/100 | 4,791 / 15,866 / 41,168 | 4 | 4 | 38/39 | 25/26 | 11/14 | 12/13 | 4/8 |
| LCB | 静态 FP8 | 90/100 | 4,511 / 16,027 / 43,992 | 3 | 3 | 39/39 | 24/26 | 13/13 | 12/14 | 2/8 |
| LCB | NVFP4 W4A16 | 91/100 | 5,119 / 15,790 / 47,768 | 4 | 3 | 38/38 | 26/27 | 13/13 | 10/12 | 4/10 |
| LCB | NVFP4 W4A4 | 92/100 | 6,338 / 15,771 / 54,096 | 3 | 3 | 33/33 | 30/31 | 9/11 | 13/14 | 7/11 |
| LCB | NVFP4 W4A4-W8A8 | 88/100 | 4,731 / 15,122 / 41,344 | 2 | 1 | 40/41 | 21/24 | 16/16 | 7/10 | 4/9 |

</details>

### NVFP4 三档

**口径**:单张 RTX PRO 6000,C8,上下文 100K,生成上限 94,208,客户端不计超时,DFlash2 草稿,SGLang;GPQA 198、MMLU 500、LCB 100 全量。

| 套题 | NVFP4 W4A16 | NVFP4 W4A4 | NVFP4 W4A4-W8A8 |
|---|---:|---:|---:|
| GPQA | 170/198 | 167/198 | 172/198 |
| MMLU | 439/500 | 440/500 | 442/500 |
| LCB | 91/100 | 92/100 | 88/100 |

NVFP4 三档的思考长度、94K 截断与空答见上方「全档位」总表。LCB 按每题的 `pass` 字段判对错。原始记录见 `evaluation/SCORES_NVFP4_W4A16.json`、`evaluation/SCORES_NVFP4_W4A4.json`、`evaluation/SCORES_NVFP4_MIXED.json`(W4A4-W8A8 档)。

### NInfer 两档:分数、思考长度、94K 截断与空答

**口径**:分数沿用 2026-10-05 在同一条 NInfer 文本路径上测得的官方三联;单张 RTX PRO 6000,官方 NInfer 引擎(`Neroued/ninfer`),C8,上下文 100K,生成上限 94,208,客户端不计超时,**不开投机**;GPQA 198、MMLU 500、LCB 100 全量;空答记错,截断但答对记对,失败样本全部留在分母里。本次上传的新包只在这条文本路径上加入 Q8 MTP、DFlash2 草稿与 proposal head,文本路径不变,全量三联没有重跑。只有 NInfer 引擎能加载 `.ninfer`;SGLang / vLLM / llama.cpp / transformers 均不能加载。

思考长度取 `usage.reasoning_tokens`(即 `completion_tokens_details.reasoning_tokens`);94K 截断指写满生成上限。LCB 空答指没有提取到可运行代码的题数。加粗表示优于原版 Qwen3.8 27B(FP8)。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | NInfer W4A4 | 177/198 | **2,934** / **7,646** / **25,804** | **2** | **2** |
| GPQA | NInfer W4A4-W8A8 | 177/198 | **3,176** / **8,844** / **24,804** | **2** | **2** |
| MMLU | NInfer W4A4 | **449/500** | **164** / **285** / **830** | **0** | 0 |
| MMLU | NInfer W4A4-W8A8 | 444/500 | **163** / **281** / **923** | **0** | 0 |
| LCB | NInfer W4A4 | **89/100** | **3,994** / **15,533** / **36,125** | **2** | **2** |
| LCB | NInfer W4A4-W8A8 | **92/100** | **4,046** / **15,829** / **40,479** | **2** | **3** |

NInfer W4A4 的 LCB 空答 2 条是第 11、15 题,均为截断后没有代码;GPQA 空答 2 条是第 79、127 题,均为截断且 pred 为空。MMLU 无截断、无空答。NInfer W4A4-W8A8 的 LCB 空答 3 条是第 17、53、54 题(第 17 题正常停但没有代码,第 53、54 题截断且没有代码);GPQA 空答 2 条是第 79、127 题,均为截断且 pred 为空。MMLU 无截断、无空答。

<details open>
<summary>NInfer 两档明细(按思考长度分桶)</summary>

分桶为「答对/该桶题数」,按思考长度左闭右开。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 | <2K | 2–12K | 12–24K | 24–48K | ≥48K |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| GPQA | NInfer W4A4 | 177/198 | 2,934 / 7,646 / 25,804 | 2 | 2 | 76/83 | 69/71 | 17/22 | 14/19 | 1/3 |
| GPQA | NInfer W4A4-W8A8 | 177/198 | 3,176 / 8,844 / 24,804 | 2 | 2 | 79/82 | 70/74 | 13/21 | 12/16 | 3/5 |
| MMLU | NInfer W4A4 | 449/500 | 164 / 285 / 830 | 0 | 0 | 438/480 | 11/19 | 0/1 | 0/0 | 0/0 |
| MMLU | NInfer W4A4-W8A8 | 444/500 | 163 / 281 / 923 | 0 | 0 | 435/478 | 8/21 | 1/1 | 0/0 | 0/0 |
| LCB | NInfer W4A4 | 89/100 | 3,994 / 15,533 / 36,125 | 2 | 2 | 40/41 | 21/23 | 12/14 | 13/16 | 3/6 |
| LCB | NInfer W4A4-W8A8 | 92/100 | 4,046 / 15,829 / 40,479 | 2 | 3 | 38/38 | 26/26 | 14/16 | 11/12 | 3/8 |

</details>

### INT4 W4A16:分数、94K 截断与空答

**口径**:单张 RTX PRO 6000,vLLM 0.28,C8,上下文 100K,生成上限 94,208,客户端不计超时,思考强度 xhigh,**开 MTP 投机(内置头,3 个草稿 token)**,`--reasoning-parser qwen3`;GPQA 198 / MMLU 500 / LCB 100 全量;空答算错,截断但答对算对,所有失败都留在分母里。测评在 2026-10-09 暂停过,之后用同样的服务参数继续,已完成的题保留。

94K 截断指触到生成上限。LCB 空答指提取不到可运行代码的题数。加粗表示优于原版 Qwen3.8 27B(FP8),其数据见上面的全档表。

| 测评 | 精度 | 分数 | 思考长度 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | INT4 W4A16 | 177/198 | **3,136** / **8,115** / **27,856** | **1** | **1** |
| MMLU | INT4 W4A16 | **446/500** | **176** / **322** / **1,098** | **0** | 0 |
| LCB | INT4 W4A16 | **87/100** | **4,494** / **19,046** / **36,053** | **2** | **2** |

思考长度取自 vLLM 返回的 `usage.reasoning_tokens`。GPQA:截断 1 题(第 79 题),空答 1 题(第 79 题)。MMLU 没有截断,也没有空答。LCB:截断 2 题(第 atcoder:arc182_e:6, atcoder:arc195_d:54 题),空答 2 题(第 atcoder:arc182_e:6, atcoder:arc195_d:54 题)。LCB 按难度:难 37/46,中 27/31,易 23/23。整轮测评的 MTP 平均接受长度(vLLM 日志,3 个草稿 token):2.81。

### INT8 W8A8:分数、94K 截断与空答

**口径**:单张 RTX PRO 6000,vLLM 0.28,C8,上下文 100K,生成上限 94,208,客户端不计超时,**不开投机**,思考档位 xhigh;GPQA 198、MMLU 500、LCB 100 全量;空答记错,截断但答对记对,失败样本全部留在分母里。INT8 W8A8 只能用 vLLM 加载。

94K 截断指写满生成上限。LCB 空答指没有提取到可运行代码的题数。加粗表示优于原版 Qwen3.8 27B(FP8),其数字见上方「全档位」总表。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | INT8 W8A8 | 175/198 | **3,862** / **9,055** / **25,299.5** | **1** | **1** |
| MMLU | INT8 W8A8 | **450/500** | **156** / **291** / **864.4** | **0** | 0 |
| LCB | INT8 W8A8 | **91/100** | — | **2** | **0** |

注:INT8 W8A8 测评时 vLLM 未开推理解析器,`usage.reasoning_tokens` 均为 0,思考与答案都记在正文里。GPQA 与 MMLU 的思考长度按原文重新计数:取正文中 `</think>` 之前的文本,用 BF16 tokenizer 计数(与 GGUF 档相同的方法)。LCB 的结果文件只保存了代码,没有保存思考原文,无法计数,记「—」。

GPQA 的 1 条截断是第 127 题,pred 为空,同时记为空答。LCB 的 2 条截断是第 7、53 题:第 7 题截断后留下的代码运行出错,判错;第 53 题虽然截断,代码仍判对;LCB 没有空答。MMLU 无截断、无空答。LCB 按难度为 hard 38/46、medium 30/31、easy 23/23。

### INT8 W8A16:分数、94K 截断与空答

**口径**:单张 RTX PRO 6000,vLLM 0.28,C8,上下文 100K,生成上限 94,208,客户端不计超时,思考强度 xhigh,**开 MTP 投机(3 个草稿 token,外挂草稿 `INT8/W8A16/MTP-BF16/`)**,`--reasoning-parser qwen3`;GPQA 198 / MMLU 500 / LCB 100 全量;空答算错,截断但答对算对,所有失败都留在分母里。INT8 W8A16 只能用 vLLM 加载(pack-quantized GPTQ W8A16)。视觉与 MTP 在同一套环境上做过冒烟测试(MTP 平均接受长度 3.31;开、关思考时图片 OCR 都正确)。

94K 截断指触到生成上限。LCB 空答指提取不到可运行代码的题数。加粗表示优于原版 Qwen3.8 27B(FP8),其数据见上面的全档表。

| 测评 | 精度 | 分数 | 思考长度 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | INT8 W8A16 | 170/198 | **3,203** / **7,999** / **27,188** | **1** | **1** |
| MMLU | INT8 W8A16 | **449/500** | **162** / **287** / **876** | **0** | 0 |
| LCB | INT8 W8A16 | **94/100** | **5,422** / **17,884** / **39,584** | **1** | **1** |

思考长度取自 vLLM 返回的 `usage.reasoning_tokens`。GPQA:截断 1 题(第 79 题),空答 1 题(第 79 题)。MMLU 没有截断,也没有空答。LCB:截断 1 题(atcoder:arc195_d:54),空答 1 题(atcoder:arc195_d:54)。LCB 按难度:易 23/23,中 31/31,难 40/46。

同口径的 TPS / 并发表等速度测试跑完后补上;冒烟测试中短提示词开 MTP + 视觉的 decode 约 119 tok/s(墙钟)。

### GGUF Q2 / Q3 / Q4 LynnStyle:分数、思考长度、94K 截断与空答

**口径**:单张 RTX PRO 6000,llama.cpp(`llama-server`),C4,每槽上下文约 100K,生成上限 94,208,客户端不计超时,思考打开;GPQA 198、MMLU 500、LCB 100 全量;空答记错,截断但答对记对,失败样本全部留在分母里。成绩在内置 MTP 前测得(外挂 Q8 MTP 草稿),量化权重相同;`GGUF-NInfer/` 下对应的 `.ninfer` 由同一份 GGUF 转换,全量三联只在 GGUF 上跑。

94K 截断指写满生成上限。LCB 空答指没有提取到可运行代码的题数。加粗表示优于原版 Qwen3.8 27B(FP8),其数字见上方「全档位」总表。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | GGUF Q2 LynnStyle | 177/198 | **2,989.5** / **8,923.8** / **27,156.1** | **3** | **0** |
| MMLU | GGUF Q2 LynnStyle | 433/500 | **181** / **326.3** / **1,020.5** | 1 | 0 |
| LCB | GGUF Q2 LynnStyle | **90/100** | **5,656.5** / **17,835.8** / **40,067.3** | **1** | **1** |
| GPQA | GGUF Q3 LynnStyle-16G | 172/198 | **3,811** / **11,404** / **31,418** | **2** | **2** |
| MMLU | GGUF Q3 LynnStyle-16G | 427/500 | **190** / **361** / 1,665 | **0** | 0 |
| LCB | GGUF Q3 LynnStyle-16G | **90/100** | **6,520** / **21,586** / **43,184** | **3** | **3** |
| GPQA | GGUF Q3 LynnStyle | 173/198 | **3,125.5** / **7,265.2** / **24,343.1** | **1** | **1** |
| MMLU | GGUF Q3 LynnStyle | **449/500** | **148** / **279.3** / **923.4** | **0** | 0 |
| LCB | GGUF Q3 LynnStyle | **92/100** | **4,421** / **14,232.2** / **34,946** | **1** | **1** |
| GPQA | GGUF Q4 LynnStyle | 175/198 | **2,951.0** / **8,159.3** / **25,649.0** | **1** | **2** |
| MMLU | GGUF Q4 LynnStyle | **448/500** | **164** / **312.9** / **1,077.7** | **0** | 0 |
| LCB | GGUF Q4 LynnStyle | **89/100** | **3,669.5** / **14,810.5** / **38,182.1** | **2** | **2** |

注:思考长度从原文用 BF16 tokenizer 计数(GPQA/LCB 用 `reasoning` 字段,MMLU 由 `response` 末行前文本拆分;不以接口 `reasoning_tokens` 为准)。

### GGUF Q6_K:分数、思考长度、94K 截断与空答

**口径**:单张 RTX PRO 6000,llama.cpp(`llama-server`)加载 `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`,C4,上下文 100K,生成上限 94,208,客户端不计超时,思考档位 xhigh;GPQA 198、MMLU 500、LCB 100 全量;空答记错,截断但答对记对,失败样本全部留在分母里。`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer` 由同一份 GGUF 转换而来,主干量化相同,全量三联只在 GGUF 上跑。

思考长度取 `usage.reasoning_tokens`;94K 截断指写满生成上限。LCB 空答指没有提取到可运行代码的题数。加粗表示优于原版 Qwen3.8 27B(FP8),其数字见上方「全档位」总表。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | GGUF Q6_K | 174/198 | **3,683** / **9,814** / **27,966** | **2** | **2** |
| MMLU | GGUF Q6_K | **448/500** | **162** / **310.3** / **939.4** | **0** | 0 |
| LCB | GGUF Q6_K | **91/100** | — | **0** | **1** |

注:MMLU 与 LCB 测评时 llama.cpp 没有单独返回思考 token(`usage` 里没有 `reasoning_tokens`)。MMLU 的思考长度由 `response` 末行前文本拆分,用 BF16 tokenizer 计数(与 Q8_0 相同的方法);LCB 的结果文件没有保存思考原文,无法计数,记「—」;GPQA 的思考 token 由测评脚本单独统计。

GPQA 的 2 条截断是第 79、127 题,均写满 94,208 且 pred 为空,同时记为空答。MMLU 无截断、无空答。

LCB 无 94K 截断;空答 1 条是第 92 题,正常停止但没有给出代码。

LCB 以 llama.cpp 的结果为准:LCB 测评脚本请求 NInfer 时收到的回复不是合法 JSON,这是测评脚本与接口的兼容问题,不是模型质量问题;同一份 GGUF 用 llama.cpp 跑同一批抽测题全部通过。


### GGUF Q8_0:分数、思考长度、94K 截断与空答

**口径**:单张 RTX PRO 6000,llama.cpp(`llama-server`)加载 `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf`,C4,上下文 100K,生成上限 94,208,客户端不计超时,思考档位 xhigh;GPQA 198、MMLU 500、LCB 100 全量;空答记错,截断但答对记对,失败样本全部留在分母里。`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer` 由同一份 GGUF 转换而来,主干量化相同,全量三联只在 GGUF 上跑。

思考长度:GPQA 取 `usage.reasoning_tokens`;MMLU 由 `response` 末行前文本拆分并用 BF16 tokenizer 计数;LCB 由落盘的 `reasoning` 原文计数。94K 截断指写满生成上限。LCB 空答指没有提取到可运行代码的题数。加粗表示优于原版 Qwen3.8 27B(FP8)。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | GGUF Q8_0 | 171/198 | **3,102.5** / **7,971** / **28,891.6** | **2** | **0** |
| MMLU | GGUF Q8_0 | 443/500 | **164** / **291** / **741** | **0** | 0 |
| LCB | GGUF Q8_0 | **90/100** | **4,098.5** / **16,087.8** / **39,135.5** | **3** | **3** |

GPQA 截断 2、空答 0。MMLU 无截断、无空答。LCB 截断 3、空答 3(写满长度且无代码)。

LCB 以 llama.cpp 的结果为准:LCB 测评脚本请求 NInfer 时收到的回复不是合法 JSON,这是测评脚本与接口的兼容问题,不是模型质量问题。


## 用 Lynn 桌面 Agent 跑本模型（V0.87.4）

[Lynn](https://github.com/MerkyorLynn/Lynn) 是开源桌面 AI Agent（GUI + 独立 CLI）：对话、搜资料、改文件、写代码、实时语音都能在同一套界面里完成，也可以当其他工具或 CI 的无头 worker。**全部免费，Quick Start 无需配置、无需 API Key。**

当前默认能力（V0.87.4）：

| 用途 | 方案 |
|---|---|
| 云端对话 / 编码 / 工具 | **Step 5 Preview**（原生识图，直接发图即可） |
| 实时语音 | **StepAudio 2.5 Realtime** |
| 端侧本地 | **本仓 Coder390 EfficientThink 27B** 的 Q2 / Q3 GGUF（内置 Q4 MTP；走 llama.cpp，**不是 NInfer**；本次 Lynn 安装不含视觉组件） |

端侧硬件建议：Apple Silicon 看统一内存，NVIDIA 看单卡显存（不叠多卡、不用系统内存顶替）。**低于 14GiB 禁止安装**；**16GB 推荐 Q2**，**24GB 及以上推荐 Q3**。模型文件之外还需预留上下文缓存和运行缓冲。

工具参数由模型自己填写（地点、日期、联赛、行情代码、货币对等），不再从整句问题硬猜实体。长期记忆与写作 Diff 等桌面能力随 Lynn 提供；完整说明与更新见发布页。

- [V0.87.4 发布说明](https://github.com/MerkyorLynn/Lynn/releases/tag/v0.87.4)
- [国内下载页（推荐）](https://download.merkyorlynn.com/download.html)
- macOS Apple Silicon：[国内](https://download.merkyorlynn.com/downloads/Lynn-0.87.4-macOS-arm64.dmg) · [GitHub](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.4/Lynn-0.87.4-macOS-arm64.dmg)
- macOS Intel：[国内](https://download.merkyorlynn.com/downloads/Lynn-0.87.4-macOS-x64.dmg) · [GitHub](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.4/Lynn-0.87.4-macOS-x64.dmg)
- Windows：[国内](https://download.merkyorlynn.com/downloads/Lynn-0.87.4-Windows-Setup.exe) · [GitHub](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.4/Lynn-0.87.4-Windows-Setup.exe)

在 Lynn 里：**设置 → 模型 → 本地 Qwen3.8-27B → 选 Q2 / Q3 → 安装并启动**。本地档位只加载本仓库 `GGUF/` 下的 Q2 / Q3 LynnStyle-MTP 文件；NInfer / NVFP4 等其他格式请用对应引擎自行部署，不走 Lynn 一键安装。

## 量化档

| 档位 | 目录 | 说明 | 包大小(字节) | BPW | GPQA / MMLU / LCB |
|---|---|---|---:|---:|---|
| BF16 | `BF16/` | 完整多模态,原版 config,内置官方 BF16 MTP,含 DFlash2 草稿,免补丁 | 55,583,125,732(约 51.8 GiB) | 16.00 | 178 / 446 / 90 |
| 静态 FP8 Block128 | `FP8/` | 完整多模态,内置官方 BF16 MTP,含 DFlash2 草稿 | 33,669,220,491(约 31.4 GiB) | 9.00 | 178 / 450 / 90 |
| NVFP4 W4A16 | `NVFP4/W4A16/` | 完整多模态,语言模型 Linear 为 NVFP4 权重 + BF16 激活,内置官方 BF16 MTP,含 DFlash2 草稿,SGLang 免补丁 | 20,613,406,953(约 19.2 GiB,不含草稿) | 5.93 | 170 / 439 / 91 |
| NVFP4 W4A4 | `NVFP4/W4A4/` | 完整多模态,语言模型 Linear 为 NVFP4 权重 + NVFP4 激活,内置官方 BF16 MTP,含 DFlash2 草稿,SGLang 免补丁 | 20,613,386,462(约 19.2 GiB,不含草稿) | 5.93 | 167 / 440 / 92 |
| NVFP4 W4A4-W8A8 | `NVFP4/W4A4-W8A8/` | 完整多模态,语言模型 MLP 为 NVFP4 W4A4、注意力与线性注意力投影为 FP8 W8A8,内置官方 BF16 MTP,含 DFlash2 草稿,SGLang 免补丁 | 23,769,634,648(约 22.1 GiB,不含草稿) | 6.84 | 172 / 442 / 88 |
| NInfer W4A4 | `NVFP4-NInfer/W4A4/` | 官方 NInfer 包(`.ninfer`),W4A4 文本路径,包内含 Q8 MTP、DFlash2 草稿、proposal head 与视觉部分(加 `--vision` 可输入图片);仅官方 NInfer 引擎(`Neroued/ninfer`)可加载 | 23,773,675,264(约 22.1 GiB) | 6.76 | 177 / 449 / 89 |
| NInfer W4A4-W8A8 | `NVFP4-NInfer/W4A4-W8A8/` | 官方 NInfer 混合精度包(`.ninfer`),W4A4-W8A8 文本路径,包内含 Q8 MTP、DFlash2 草稿、proposal head 与视觉部分(加 `--vision` 可输入图片);仅官方 NInfer 引擎(`Neroued/ninfer`)可加载 | 23,773,675,264(约 22.1 GiB) | 6.76 | 177 / 444 / 92 |
| INT4 W4A16 | `INT4/W4A16/` | 文本 + 图像(`Qwen3_5ForConditionalGeneration`):GPTQ INT4 权重(对称,分组大小 128),激活保持 BF16,compressed-tensors 格式;内置 BF16 MTP 头(`model_mtp.safetensors`),供 vLLM 投机解码;BF16 视觉塔(`model_visual.safetensors`);不含 DFlash2 草稿;在 vLLM 上实测 | 19,437,985,972(约 18.1 GiB) | 5.25 | 177 / 446 / 87 |
| INT8 W8A8 | `INT8/W8A8/` | 文本 + 图像(`Qwen3_5ForConditionalGeneration`;BF16 视觉塔单独存为 `model_visual.safetensors`,2026-10-09 加入),SmoothQuant 按通道 INT8 权重 + 按 token 动态 INT8 激活,compressed-tensors 格式;不含 DFlash2 草稿;MTP 以单独的 BF16 草稿目录(`INT8/W8A8/MTP-BF16/`)提供,供 vLLM 投机解码使用;仅 vLLM 可加载 | 30,422,466,299(约 28.3 GiB) | 8.77 | 175 / 450 / 91 |
| INT8 W8A16 | `INT8/W8A16/` | 文本 + 图像(`Qwen3_5ForConditionalGeneration`):GPTQ 对称按通道 INT8 权重 + BF16 激活(compressed-tensors pack-quantized);BF16 视觉塔 `model_visual.safetensors`;MTP 以单独的 BF16 草稿目录 `INT8/W8A16/MTP-BF16/` 提供;不含 DFlash2 草稿;仅 vLLM 可加载 | 30,370,996,824(约 28.3 GiB,含视觉;MTP 草稿另计) | 8.76 | 170 / 449 / 94 |
| GGUF Q3 LynnStyle | `GGUF/` | 混合精度 LynnStyle GGUF(`Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.gguf`):最低 Q3;内置 **Q4 MTP**;视觉外挂 | 17,303,770,432(约 16.1 GiB) | 5.07 | 173 / 449 / 92 |
| GGUF Q3 LynnStyle · NInfer | `GGUF-NInfer/` | 由 Q3 LynnStyle GGUF 转换;内置 Q4_K MTP 与视觉;NInfer-all 与 ninfer-fusion-kvmem 均可 | 17,596,369,920(约 16.4 GiB) | 5.07 | 173 / 449 / 92 |
| GGUF Q3 LynnStyle · Q8MTP | `GGUF/` | 同一个 Q3 LynnStyle GGUF,只把内置 MTP 头改为 Q8_0(`Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf`),其他张量与原包逐字节相同;Q8_0 MTP 头备选版(原包的 Q4_0 MTP 头 llama.cpp 支持);llama.cpp 看图同样用 `GGUF/` 里的 mmproj | 17,516,107,072(约 16.3 GiB) | 5.13 | 173 / 449 / 92 |
| GGUF Q3 LynnStyle · Q8MTP · NInfer | `GGUF-NInfer/` | 由上面的 Q8MTP GGUF 转成的 NInfer 包(`Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.ninfer`),内置 Q8_0 MTP 头和视觉组件,model id `qwen3.8-27b-coder390-Q3LynnStyle-Q8Mtp`;主体权重与原 Q3 LynnStyle 包相同,分数沿用原包 | 17,808,706,560(约 16.6 GiB) | 5.13 | 173 / 449 / 92 |
| GGUF Q4 LynnStyle | `GGUF/` | 混合精度 LynnStyle GGUF(`Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.gguf`):最低 Q4;内置 **Q4 MTP**;视觉外挂 | 19,620,406,592(约 18.3 GiB) | 5.75 | 175 / 448 / 89 |
| GGUF Q4 LynnStyle · NInfer | `GGUF-NInfer/` | 由 Q4 LynnStyle GGUF 转换;内置 Q4_K MTP 与视觉;NInfer-all 与 ninfer-fusion-kvmem 均可 | 19,913,006,080(约 18.5 GiB) | 5.74 | 175 / 448 / 89 |
| GGUF Q4 LynnStyle · Q8MTP | `GGUF/` | 同一个 Q4 LynnStyle GGUF,只把内置 MTP 头改为 Q8_0(`Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf`),其他张量与原包逐字节相同;Q8_0 MTP 头备选版(原包的 Q4_0 MTP 头 llama.cpp 支持);llama.cpp 看图同样用 `GGUF/` 里的 mmproj | 19,832,743,232(约 18.5 GiB) | 5.81 | 175 / 448 / 89 |
| GGUF Q4 LynnStyle · Q8MTP · NInfer | `GGUF-NInfer/` | 由上面的 Q8MTP GGUF 转成的 NInfer 包(`Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer`),内置 Q8_0 MTP 头和视觉组件,model id `qwen3.8-27b-coder390-Q4LynnStyle-Q8Mtp`;主体权重与原 Q4 LynnStyle 包相同,分数沿用原包 | 20,125,342,720(约 18.7 GiB) | 5.81 | 175 / 448 / 89 |
| GGUF Q3 LynnStyle-16G | `GGUF/` | 我们最低的 Q3 档,面向 16G 显存(`Qwen3.8-27B-Coder390-Q3LynnStyle16G-MTP.gguf`):最低精度 IQ3_XXS,主体无 Q6 / Q8;重要性矩阵校正 + GSQ-RCO(同字节精修,体积不变);内置 **Q4_K MTP**;看图用 `GGUF/` 内的 mmproj;成绩用 llama.cpp + 外挂 DFlash2 测得 | 13,276,009,920(约 12.4 GiB) | 3.89 | 172 / 427 / 90 |
| GGUF Q3 LynnStyle-16G · NInfer | `GGUF-NInfer/` | 同权重 NInfer 包:内置 **Q4_K MTP** + 内置 **Q8 视觉**(加 `--vision`,无需 mmproj) | 13,765,136,896(约 12.8 GiB) | 3.89 | 同成绩(GGUF 三科) |
| GGUF Q2 LynnStyle | `GGUF/` | 混合精度 LynnStyle GGUF(`Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf`):最低 Q2;内置 **Q4 MTP**;视觉外挂 | 13,276,009,792(约 12.4 GiB) | 3.89 | 177 / 433 / 90 |
| GGUF Q2 LynnStyle · NInfer | `GGUF-NInfer/` | 由 Q2 LynnStyle GGUF 转换;内置 Q4_K MTP 与视觉;NInfer-all 与 ninfer-fusion-kvmem 均可 | 13,568,617,472(约 12.6 GiB) | 3.89 | 177 / 433 / 90 |
| GGUF Q2 LynnStyle · Q8MTP | `GGUF/` | 同一个 Q2 LynnStyle GGUF,只把内置 MTP 头改为 Q8_0(`Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf`),其他张量与原包逐字节相同;Q8_0 MTP 头备选版(原包的 Q4_0 MTP 头 llama.cpp 支持);llama.cpp 看图同样用 `GGUF/` 里的 mmproj | 13,488,346,432(约 12.6 GiB) | 3.95 | 177 / 433 / 90 |
| GGUF Q2 LynnStyle · Q8MTP · NInfer | `GGUF-NInfer/` | 由上面的 Q8MTP GGUF 转成的 NInfer 包(`Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.ninfer`),内置 Q8_0 MTP 头和视觉组件,model id `qwen3.8-27b-coder390-Q2LynnStyle-Q8Mtp`;主体权重与原 Q2 LynnStyle 包相同,分数沿用原包 | 13,780,954,112(约 12.8 GiB) | 3.95 | 177 / 433 / 90 |
| GGUF Q8_0 | `GGUF/` | llama.cpp 用 GGUF 单文件(`Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf`):主干 Q8_0,内置 MTP 头,不需要外挂草稿;视觉用 `GGUF/` 内的 mmproj(llama.cpp `--mmproj`) | 29,069,202,688(约 27.1 GiB) | 8.51 | 171 / 443 / 90 |
| GGUF Q8_0 · NInfer | `GGUF-NInfer/` | 由同一份 Q8_0 GGUF 转换的 NInfer 包(`.ninfer`),内置 MTP 头与视觉部分;仅 NInfer-all(`iamwavecut/ninfer-all`)可加载;成绩为同一份 GGUF 在 llama.cpp 上测得 | 29,361,802,240(约 27.3 GiB) | 8.51 | 171 / 443 / 90 |
| GGUF Q6_K | `GGUF/` | llama.cpp 用 GGUF 单文件(`Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`):主干 Q6_K + imatrix 校准,内置 Q8 MTP 头,不需要外挂草稿;视觉用 `GGUF/` 内的 mmproj(llama.cpp `--mmproj`) | 23,177,516,384(约 21.6 GiB) | 6.79 | 174 / 448 / 91 |
| GGUF Q6_K · NInfer | `GGUF-NInfer/` | 由同一份 GGUF 转换的 NInfer 包(`.ninfer`),主干量化相同,内置 MTP 头(attention/MLP 权重 Q6_K,输入投影 Q8_0),包内含视觉部分(加 `--vision` 可输入图片);仅 NInfer-all(`iamwavecut/ninfer-all`)可加载;成绩为同一份 GGUF 在 llama.cpp 上测得 | 23,379,962,880(约 21.8 GiB) | 6.76 | 174 / 448 / 91 |

**社区分支 ninfer-fusion-kvmem**:Q2～Q4 LynnStyle 的 NInfer 包(`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer`)内置 MTP 头已改为 Q4_K,在官方 NInfer-all master 和社区分支 ninfer-fusion-kvmem 上都能正常加载并开启 MTP(2026-10-11 实测)。`GGUF/` 下的 `.gguf` 内置 MTP 头仍为 Q4_0,llama.cpp 支持。Q8 MTP 版本继续保留作为备选(权重相同,只把 MTP 头改为 Q8_0):llama.cpp 用 `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf`、`GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf`、`GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf`;NInfer 用 `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer`(model id 分别为 `qwen3.8-27b-coder390-Q2LynnStyle-Q8Mtp`、`qwen3.8-27b-coder390-Q3LynnStyle-Q8Mtp`、`qwen3.8-27b-coder390-Q4LynnStyle-Q8Mtp`)。

**Q8 MTP 版本 · 检查**(2026-10-09,单张 RTX PRO 6000):NInfer-all `master`,`--spec mtp --draft-tokens 3 --vision`,int8 KV,上下文 8,192;llama.cpp 用 `--spec-type draft-mtp --spec-draft-n-max 4` 加 `--mmproj`;各发一个看图请求,短跑。所有运行看图都答对(llama.cpp 开关思考均答对)。

| 包 | NInfer decode tok/s | NInfer MTP 接受率(每轮 token 数) | llama.cpp decode tok/s | llama.cpp 草稿接受率 | 看图 |
|---|---:|---:|---:|---:|---|
| Q2 LynnStyle · Q8MTP | 211.7 | 64.2%(3.14) | 180.1 | 0.879 | 正确 |
| Q3 LynnStyle · Q8MTP | 134.9 | 51.7%(2.55) | 138.3 | 0.904 | 正确 |
| Q4 LynnStyle · Q8MTP | 154.8 | 71.0%(3.13) | 135.6 | 0.879 | 正确 |

BPW(bits per weight)是整包的有效平均位宽:整包主模型权重文件(`.safetensors`,含视觉塔、MTP 与 scale 张量,不含 DFlash2 草稿)总字节数 × 8 ÷ 总参数数。总参数数按 safetensors 头部统计,五档一致,均为 27,781,427,952 个(NVFP4 的 U8 打包张量一个字节算 2 个元素,scale 张量不计元素)。BF16、静态 FP8、NVFP4 W4A16、NVFP4 W4A4、NVFP4 W4A4-W8A8 的权重文件总字节数依次为 55,563,008,568、31,242,033,200、20,593,097,872、20,593,145,056、23,749,329,544。各档都是混合精度(不同层不同位宽),标称位宽会误导,BPW 反映单位体积下的质量密度。

NInfer 两档的 BPW 按整包 `.ninfer` 文件字节数 × 8 ÷ 总参数数 27,781,427,952 计算:两档文件加视觉前均为 23,477,856,260 字节,BPW 均为 6.76。`.ninfer` 包内含 Q8 MTP、DFlash2 草稿与 proposal head;2026-10-09 加入的视觉部分(295,720,448 字节)不计入这里的 BPW;上方 NVFP4 / BF16 / FP8 的 safetensors 计法不计 DFlash2 草稿,两种计法不同,不宜直接横向比较 BPW。

INT8 W8A8 的 BPW 只算 8 个 INT8 文本权重文件(BF16 视觉文件 `model_visual.safetensors` 921,497,224 字节不计入),按其总字节数 29,480,791,128 × 8 ÷ 文本参数数 26,895,998,464 计算,为 8.77。文本参数数按 8 个 INT8 权重文件的 safetensors 头部统计(INT8 与 BF16 张量计元素,scale 张量不计元素),与 BF16 包去掉视觉塔(460,730,096)和 MTP(424,699,392)后的参数数一致;分母与上方各档的 27,781,427,952 不同,不宜直接横向比较 BPW。

GGUF Q8_0 两个包的 BPW 按单个文件字节数 × 8 ÷ 文本 + MTP 参数数 27,320,697,856 计算:GGUF 29,069,202,688 字节、8.51,NInfer 加视觉前 29,065,983,488 字节、8.51。GGUF Q6_K 两个包的 BPW 按单个文件字节数 × 8 ÷ 文本 + MTP 参数数 27,320,697,856 计算:GGUF 为 23,177,516,384 字节、6.79,NInfer 加视觉前为 23,084,144,128 字节、6.76。参数数按 GGUF 头部统计(866 个张量:文本 26,895,998,464 + MTP 424,699,392);视觉不计入分母:llama.cpp 的外挂 mmproj 和现在打进每个 `.ninfer` 的视觉部分(295,720,448 字节)都不算。分母与上方各档的 27,781,427,952 及 INT8 W8A8 的 26,895,998,464 都不同,不宜直接横向比较 BPW。

- 每档各自带一份 DFlash2 草稿(文件完全相同,2,407,384,680 字节):`FP8/DFlash2-FP8/`、`BF16/DFlash2-FP8/`、`NVFP4/W4A16/DFlash2-FP8/`、`NVFP4/W4A4/DFlash2-FP8/`、`NVFP4/W4A4-W8A8/DFlash2-FP8/`。
- BF16 版 DFlash2 草稿(如 V100 或无法加载 FP8 草稿的引擎)请用上游 [incoai/Qwen3.8-27B-DFlash2](https://huggingface.co/incoai/Qwen3.8-27B-DFlash2)。
- DFlash2 草稿格式:FP8 E4M3 权重,128×128 分块 scale(`weight_scale_inv`),与 FP8 主体相同;q/k/v 投影、`fc`、候选选择器、卷积和 norm 保持 BF16。2026-10-08 起替换了原来按张量 scale 的草稿(只认分块 scale 的引擎,如 radiance,加载旧草稿不报错,但几乎不接受草稿 token)。2026-10-09 在一台 RTX PRO 6000 上用 SGLang 0.5.21 实测新草稿:FP8 主体,`--speculative-num-draft-tokens 8 --speculative-dflash-block-size 8`,单请求,6 条编程提示词,生成上限 1,024。贪心平均接受长度 5.05、单请求 171 tok/s(中位数);同一命令下旧草稿是 4.99、178 tok/s。temperature 1.0 时两者分别是 155 和 152 tok/s。在 SGLang 中新草稿的接受效果与旧草稿相当。本卡其他 DFlash2 测速数字是用旧草稿测的。
- BF16 与静态 FP8 的速度数据在静态 FP8 包上测得,BF16 未单独测速,沿用同一组数据;NVFP4 三档各自单独测速。
- NVFP4 三档的分数为单卡 C8 测得,口径见上文「NVFP4 三档」。
- NInfer 两档成绩沿用 2026-10-05 在同一文本路径上以单卡 C8、官方 NInfer、不开投机测得的三联,口径见上文「NInfer 两档」;NInfer 两档的速度为新包单独实测,见下文「最佳 TPS 推荐与并发推荐」中的「NInfer 两档」。
- INT4 W4A16 成绩为单卡 C8、vLLM 0.28、开 MTP(草稿长度 3,内置头)测得的全量三联,口径见上文「INT4 W4A16」;速度见下文「最佳 TPS 推荐与并发推荐」中的「INT4 W4A16」。
- INT8 W8A8 成绩为单卡 C8、vLLM、不开投机测得的全量三联,口径见上文「INT8 W8A8」;速度为快测,见下文「最佳 TPS 推荐与并发推荐」中的「INT8 W8A8」。
- GGUF Q6_K 成绩为单卡 C4、llama.cpp 测得的全量三联,口径见上文「GGUF Q6_K」;速度为快测,见下文「最佳 TPS 推荐与并发推荐」中的「GGUF Q6_K」。
- GGUF Q8_0 成绩为单卡 C4、llama.cpp 测得的全量三联,口径见上文「GGUF Q8_0」;速度见下文「GGUF Q8_0」(NInfer C8 MTP 486.3;llama.cpp C4 MTP 190.8)。
- NInfer 两档已上传到 `NVFP4-NInfer/W4A4/` 与 `NVFP4-NInfer/W4A4-W8A8/`,INT8 W8A8 已上传到 `INT8/W8A8/`,INT4 W4A16 已上传到 `INT4/W4A16/`,GGUF Q2 / Q3 / Q4 LynnStyle(含 Q8 MTP 版)、Q6_K 与 Q8_0 已上传到 `GGUF/` 与 `GGUF-NInfer/`。

## 最佳 TPS 推荐与并发推荐

测试环境:单张 RTX PRO 6000 Blackwell 96GB;SGLang,上下文 32K(32,768),生成上限 4,096,开思考,采样用模型默认值。

| 场景 | 推荐 | 总吞吐 tok/s | 单请求 tok/s |
|---|---|---:|---:|
| 单请求最快 | DFlash2 · C1 | 146.7 | **180.3** |
| 总吞吐最高 | DFlash2 · C16 | **1,057.5** | 93.6 |
| 日常均衡 | DFlash2 · C8 | 646.3 | 113.9 |
| 只用 MTP:单请求最快 | MTP · C1 | 82.1 | **91.1** |
| 只用 MTP:总吞吐最高 | MTP · C16 | **612.7** | 60.1 |
| 只用 MTP:日常均衡 | MTP · C8 | 380.3 | 71.1 |

- **选哪种投机**:实测 C1–C16 每一档,DFlash2 的总吞吐和单请求速度都高于 MTP,能用就用 DFlash2。
- **MTP 的位置**:不想另载 DFlash2 草稿时用 MTP(DFlash2 只在 SGLang 上验证过;FP8 包在 vLLM 0.28 上开 MTP 暂不可用,推荐 SGLang);只用 MTP 时:追求单请求速度用 C1(91.1 tok/s),交互与少量并发可用 C4(总吞吐 293.3,单请求 84.0),多人共用用 C8(总吞吐 380.3,单请求 71.1),只看总量用 C16(总吞吐 612.7,单请求 60.1)。
- **并发**:交互为主用 C1–C4;多人共用或批量跑用 C8;只看总量用 C16。C16 以上未测。

<details>
<summary>完整实测表</summary>

C1 为主测(4 个请求),C4/C8/C16 为加大请求数(每档 6×C)的复测。「相对不开投机」为同并发下总吞吐之比。

| 投机方式 | 并发 | 总吞吐 tok/s | 单请求解码 tok/s(中位) | 首 token 延迟 s(中位) | 接受长度 | 接受率 | 相对不开投机 |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP(包内 BF16) | C1 | 82.1 | 91.1 | 0.12 | 2.858 | 0.619 | 1.82× |
| MTP(包内 BF16) | C4 | 293.3 | 84.0 | 0.15 | 2.844 | 0.615 | 1.96× |
| MTP(包内 BF16) | C8 | 380.3 | 71.1 | 0.16 | 2.813 | 0.604 | 1.34× |
| MTP(包内 BF16) | C16 | 612.7 | 60.1 | 0.17 | 2.747 | 0.582 | 1.45× |
| DFlash2 | C1 | 146.7 | 180.3 | 0.12 | 4.289 | 0.470 | 3.25× |
| DFlash2 | C4 | 384.9 | 124.4 | 0.16 | 3.982 | 0.425 | 2.57× |
| DFlash2 | C8 | 646.3 | 113.9 | 0.15 | 4.131 | 0.447 | 2.28× |
| DFlash2 | C16 | 1,057.5 | 93.6 | 0.24 | 4.017 | 0.431 | 2.50× |
| 不开投机 | C1 | 45.1 | 45.6 | 0.11 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C4 | 149.5 | 42.2 | 0.13 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C8 | 283.0 | 41.7 | 0.12 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C16 | 422.8 | 38.4 | 0.13 | 不适用 | 不适用 | 1.00× |

| 投机方式 | 单请求最快 | 推荐并发(单请求速度不低于 C1 的 60% 时总吞吐最高) | 总吞吐最高 |
|---|---|---|---|
| MTP | C1(91.1 tok/s) | C16(612.7 tok/s,单请求 60.1) | C16 |
| DFlash2 | C1(180.3 tok/s) | C8(646.3 tok/s,单请求 113.9) | C16(1,057.5 tok/s) |
| 不开投机 | C1(45.6 tok/s) | C16(422.8 tok/s) | C16 |

</details>

### NVFP4 三档

测试环境同上:单张 RTX PRO 6000 Blackwell 96GB;SGLang,上下文 32K(32,768),生成上限 4,096,开思考,采样用模型默认值。数据取自 `evaluation/BENCH_NVFP4_W4A16.json`、`evaluation/BENCH_NVFP4_W4A4.json`、`evaluation/BENCH_NVFP4_MIXED.json`(W4A4-W8A8 档)。

| 场景 | 推荐 | W4A16 总吞吐 tok/s | W4A16 单请求 tok/s | W4A4 总吞吐 tok/s | W4A4 单请求 tok/s | W4A4-W8A8 总吞吐 tok/s | W4A4-W8A8 单请求 tok/s |
|---|---|---:|---:|---:|---:|---:|---:|
| 单请求最快 | DFlash2 · C1 | 147.4 | **218.4** | 188.6 | **211.5** | 175.1 | **216.8** |
| 总吞吐最高 | DFlash2 · C16 | **1,012.3** | 96.6 | **1,143.2** | 121.1 | **1,146.4** | 105.5 |
| 日常均衡 | DFlash2 · C8 | 472.4 | 131.7 | 689.8 | 132.4 | 627.9 | 132.4 |
| 只用 MTP:单请求最快 | MTP · C1 | 101.1 | **128.9** | 104.7 | **124.5** | 99.9 | **116.3** |
| 只用 MTP:总吞吐最高 | MTP · C16 | **817.3** | 70.6 | **912.4** | 73.0 | **580.2** | 69.4 |
| 只用 MTP:日常均衡 | MTP · C8 | 450.7 | 91.3 | 355.5 | 86.6 | 417.2 | 83.2 |

- **选哪种投机**:W4A4 与 W4A4-W8A8 在 C1–C16 每一档,DFlash2 的总吞吐和单请求速度都高于 MTP;W4A16 只有 C4 的总吞吐是 MTP 更高(351.4 对 315.2),其余各档与全部单请求速度都是 DFlash2 更高。
- **只用 MTP 时**:W4A16 追求单请求速度用 C1(128.9 tok/s),交互与少量并发可用 C4(总吞吐 351.4,单请求 108.0),多人共用用 C8(总吞吐 450.7,单请求 91.3),只看总量用 C16(总吞吐 817.3,单请求 70.6);W4A4 依次为 C1(124.5 tok/s)、C4(总吞吐 323.2,单请求 103.9)、C8(总吞吐 355.5,单请求 86.6)、C16(总吞吐 912.4,单请求 73.0);W4A4-W8A8 依次为 C1(116.3 tok/s)、C4(总吞吐 213.0,单请求 99.8)、C8(总吞吐 417.2,单请求 83.2)、C16(总吞吐 580.2,单请求 69.4)。
- **接受长度**:MTP 为 2.608–2.967(W4A16)、2.597–2.923(W4A4)与 2.647–2.865(W4A4-W8A8);DFlash2 为 3.351–4.143(W4A16)、3.723–4.327(W4A4)与 3.828–4.364(W4A4-W8A8)。
- **并发**:C16 以上未测。

<details>
<summary>NVFP4 W4A16 完整实测表</summary>

每档请求数:C1 4 个、C4 12 个、C8 24 个、C16 48 个。「相对不开投机」为同并发下总吞吐之比。

| 投机方式 | 并发 | 总吞吐 tok/s | 单请求解码 tok/s(中位) | 首 token 延迟 s(中位) | 接受长度 | 接受率 | 相对不开投机 |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP(包内 BF16) | C1 | 101.1 | 128.9 | 0.11 | 2.608 | 0.537 | 1.44× |
| MTP(包内 BF16) | C4 | 351.4 | 108.0 | 0.13 | 2.796 | 0.599 | 2.34× |
| MTP(包内 BF16) | C8 | 450.7 | 91.3 | 0.13 | 2.743 | 0.581 | 1.50× |
| MTP(包内 BF16) | C16 | 817.3 | 70.6 | 0.15 | 2.967 | 0.656 | 1.58× |
| DFlash2 | C1 | 147.4 | 218.4 | 0.10 | 3.469 | 0.353 | 2.11× |
| DFlash2 | C4 | 315.2 | 164.9 | 0.13 | 3.351 | 0.337 | 2.10× |
| DFlash2 | C8 | 472.4 | 131.7 | 0.14 | 3.454 | 0.351 | 1.57× |
| DFlash2 | C16 | 1,012.3 | 96.6 | 0.23 | 4.143 | 0.449 | 1.96× |
| 不开投机 | C1 | 70.0 | 71.6 | 0.09 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C4 | 150.3 | 62.1 | 0.10 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C8 | 300.9 | 62.1 | 0.10 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C16 | 515.8 | 54.7 | 0.10 | 不适用 | 不适用 | 1.00× |

| 投机方式 | 单请求最快 | 推荐并发(单请求速度不低于 C1 的 60% 时总吞吐最高) | 总吞吐最高 |
|---|---|---|---|
| MTP | C1(128.9 tok/s) | C8(450.7 tok/s,单请求 91.3) | C16(817.3 tok/s) |
| DFlash2 | C1(218.4 tok/s) | C8(472.4 tok/s,单请求 131.7) | C16(1,012.3 tok/s) |
| 不开投机 | C1(71.6 tok/s) | C16(515.8 tok/s) | C16(515.8 tok/s) |

</details>

<details>
<summary>NVFP4 W4A4 完整实测表</summary>

每档请求数:C1 4 个、C4 12 个、C8 24 个、C16 48 个。「相对不开投机」为同并发下总吞吐之比。

| 投机方式 | 并发 | 总吞吐 tok/s | 单请求解码 tok/s(中位) | 首 token 延迟 s(中位) | 接受长度 | 接受率 | 相对不开投机 |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP(包内 BF16) | C1 | 104.7 | 124.5 | 0.15 | 2.685 | 0.562 | 1.48× |
| MTP(包内 BF16) | C4 | 323.2 | 103.9 | 0.18 | 2.597 | 0.531 | 2.04× |
| MTP(包内 BF16) | C8 | 355.5 | 86.6 | 0.17 | 2.683 | 0.561 | 1.12× |
| MTP(包内 BF16) | C16 | 912.4 | 73.0 | 0.18 | 2.923 | 0.641 | 1.86× |
| DFlash2 | C1 | 188.6 | 211.5 | 0.14 | 4.327 | 0.476 | 2.66× |
| DFlash2 | C4 | 456.1 | 182.1 | 0.16 | 4.011 | 0.430 | 2.88× |
| DFlash2 | C8 | 689.8 | 132.4 | 0.17 | 3.723 | 0.389 | 2.18× |
| DFlash2 | C16 | 1,143.2 | 121.1 | 0.28 | 3.985 | 0.427 | 2.33× |
| 不开投机 | C1 | 70.9 | 72.0 | 0.13 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C4 | 158.3 | 62.8 | 0.15 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C8 | 316.8 | 62.5 | 0.14 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C16 | 490.5 | 55.2 | 0.14 | 不适用 | 不适用 | 1.00× |

| 投机方式 | 单请求最快 | 推荐并发(单请求速度不低于 C1 的 60% 时总吞吐最高) | 总吞吐最高 |
|---|---|---|---|
| MTP | C1(124.5 tok/s) | C8(355.5 tok/s,单请求 86.6) | C16(912.4 tok/s) |
| DFlash2 | C1(211.5 tok/s) | C8(689.8 tok/s,单请求 132.4) | C16(1,143.2 tok/s) |
| 不开投机 | C1(72.0 tok/s) | C16(490.5 tok/s) | C16(490.5 tok/s) |

</details>

<details>
<summary>NVFP4 W4A4-W8A8 完整实测表</summary>

每档请求数:C1 4 个、C4 12 个、C8 24 个、C16 48 个。「相对不开投机」为同并发下总吞吐之比。

| 投机方式 | 并发 | 总吞吐 tok/s | 单请求解码 tok/s(中位) | 首 token 延迟 s(中位) | 接受长度 | 接受率 | 相对不开投机 |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP(包内 BF16) | C1 | 99.9 | 116.3 | 0.17 | 2.865 | 0.621 | 1.61× |
| MTP(包内 BF16) | C4 | 213.0 | 99.8 | 0.19 | 2.667 | 0.555 | 1.09× |
| MTP(包内 BF16) | C8 | 417.2 | 83.2 | 0.18 | 2.647 | 0.549 | 1.33× |
| MTP(包内 BF16) | C16 | 580.2 | 69.4 | 0.19 | 2.772 | 0.591 | 1.24× |
| DFlash2 | C1 | 175.1 | 216.8 | 0.16 | 4.201 | 0.458 | 2.82× |
| DFlash2 | C4 | 395.0 | 152.4 | 0.19 | 3.995 | 0.427 | 2.02× |
| DFlash2 | C8 | 627.9 | 132.4 | 0.19 | 3.828 | 0.404 | 2.00× |
| DFlash2 | C16 | 1,146.4 | 105.5 | 0.30 | 4.364 | 0.479 | 2.44× |
| 不开投机 | C1 | 62.2 | 63.0 | 0.15 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C4 | 195.7 | 56.4 | 0.17 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C8 | 314.0 | 53.4 | 0.16 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C16 | 469.4 | 47.7 | 0.16 | 不适用 | 不适用 | 1.00× |

| 投机方式 | 单请求最快 | 推荐并发(单请求速度不低于 C1 的 60% 时总吞吐最高) | 总吞吐最高 |
|---|---|---|---|
| MTP | C1(116.3 tok/s) | C8(417.2 tok/s,单请求 83.2) | C16(580.2 tok/s) |
| DFlash2 | C1(216.8 tok/s) | C8(627.9 tok/s,单请求 132.4) | C16(1,146.4 tok/s) |
| 不开投机 | C1(63.0 tok/s) | C16(469.4 tok/s) | C16(469.4 tok/s) |

</details>

### NInfer 两档

测试环境:单张 RTX PRO 6000 Blackwell;官方 NInfer,上下文参数与下文 NInfer 启动命令相同(`--max-context 102400 --kv-capacity 819200 --max-concurrency 8 --kv-dtype fp8`);生成上限 4,096,开思考(模板默认 xhigh),采样 temperature 1.0、top_p 0.95、top_k 20,提示词与上方 NVFP4 测速相同;C1 发 4 个请求、C4 发 12 个、C8 发 24 个。MTP 草稿长度 4、DFlash2 草稿长度 8,均开 `--lm-head-draft`。数字为合计解码 tok/s。NInfer 并发上限为 8,C16 未测。

| 投机方式 | 档位 | C1 | C4 | C8 |
|---|---|---:|---:|---:|
| 不开投机 | NInfer W4A4 | 68.1 | 195.8 | 306.8 |
| 不开投机 | NInfer W4A4-W8A8 | 68.1 | 236.1 | 369.5 |
| MTP(草稿长度 4) | NInfer W4A4 | 154.8 | 498.3 | 678.3 |
| MTP(草稿长度 4) | NInfer W4A4-W8A8 | 162.5 | 367.6 | 663.9 |
| DFlash2(草稿长度 8) | NInfer W4A4 | 207.1 | 539.6 | 975.9 |
| DFlash2(草稿长度 8) | NInfer W4A4-W8A8 | 199.1 | 650.1 | 804.9 |

- **最佳组合**:两档、三种模式的总吞吐都在 C8 最高。NInfer W4A4 最高为 DFlash2 · C8(975.9 tok/s),NInfer W4A4-W8A8 最高为 DFlash2 · C8(804.9 tok/s);只用 MTP 时 C8 分别为 678.3 与 663.9 tok/s。
- **与 NVFP4 W4A4(SGLang)的 C8 对比**:NInfer W4A4 不开投机 306.8 对 316.8,MTP 678.3 对 355.5,DFlash2 975.9 对 689.8 tok/s。两者引擎与上下文设置不同,仅作参考。

### INT4 W4A16

环境:单张 NVIDIA RTX PRO 6000 Blackwell(96 GB);vLLM 0.28,`--max-model-len 102400`、`--max-num-seqs 8`、`--gpu-memory-utilization 0.85`;MTP 一行用内置头,`--speculative-config '{"method":"mtp","num_speculative_tokens":3}'`。生成上限 1024,开思考,采样温度 1.0、top_p 0.95、top_k 20;每档并发发送 2 × 并发数个请求,共用 8 条提示(与 INT8 `MTP-BF16/` 表同一脚本)。数值为总吞吐 tok/s(全部输出 token ÷ 墙钟时间);最后一列是 C1 单请求 decode 速度中位数。

| 投机 | C1 | C2 | C4 | C8 | C1 单请求 |
|---|---:|---:|---:|---:|---:|
| 不开投机 | 67.3 | 110.1 | 197.4 | 350.0 | 68.4 |
| MTP(3 个草稿 token) | 121.2 | 193.2 | 347.5 | 500.1 | 135.2 |

- **接受长度**(每步平均产出 token 数,含校验 token):本表 C1–C8 为 2.77–2.92;整轮测评平均 2.81。
- 上面的 INT4 分数是开 MTP(3 个草稿 token)测得的。

### INT8 W8A8

测试环境:单张 RTX PRO 6000 Blackwell;vLLM 0.28,`--max-model-len 102400`、`--max-num-seqs 8`;生成上限 512,开思考(xhigh),采样 temperature 1.0、top_p 0.95、top_k 20;每档只发与并发数相同的请求数(C1 发 1 个、C2 发 2 个、C4 发 4 个、C8 发 8 个)。这是快测:请求少、生成短,数字不能与上面各档直接比较。数字为总吞吐 tok/s(全部输出 token ÷ 墙钟时间)。两行都在另做的内置 MTP 对照版上测得(同一份 INT8 文本权重另加一层 BF16 MTP,未发布);不开投机时 MTP 层不参与计算。本包不含 MTP;现另提供单独的 MTP 草稿目录(见下文)。

| 投机方式 | C1 | C2 | C4 | C8 |
|---|---:|---:|---:|---:|
| 不开投机 | 30.8 | 45.5 | 101.2 | **177.3** |
| MTP(早先对照版,非本次发布的草稿) | 23.9 | 37.8 | 72.5 | 145.9 |

- **推荐(本表)**:不开投机,C8(177.3 tok/s);并发越高总吞吐越高,C8 以上未测。
- 上表 MTP 一行来自早先未发布的对照版,仅作参考,不代表 `MTP-BF16/` 草稿目录;该目录的结果见下文。本档没有 DFlash2 草稿。

**使用 `MTP-BF16/` 草稿目录**

测试环境:一台 NVIDIA RTX PRO 6000 Blackwell(96 GB);vLLM 0.28,`--max-model-len 102400`、`--max-num-seqs 8`、`--gpu-memory-utilization 0.85`;MTP 一行用 `--speculative-config '{"method":"mtp","model":"./INT8/W8A8/MTP-BF16","num_speculative_tokens":3}'`。生成上限 1024,开思考,采样 temperature 1.0、top_p 0.95、top_k 20;每档发 2 × 并发数个请求,轮流使用同一组 8 条提示词。数字为总吞吐 tok/s(全部输出 token ÷ 墙钟时间),最后一列为 C1 单请求解码速度中位数。硬件和设置都与上表不同,只在本表内比较。

| 投机方式 | C1 | C2 | C4 | C8 | C1 单请求 |
|---|---:|---:|---:|---:|---:|
| 不开投机 | 31.1 | 59.9 | 81.9 | 127.0 | 31.6 |
| MTP(3 个草稿 token) | 65.9 | 120.5 | 199.4 | 389.8 | 75.7 |

- **接受长度**(每步平均产出 token 数,含验证 token):C1–C8 为 2.74–2.90。
- 用这份草稿、3 个草稿 token,这台机器上每一档都更快:C1 为 65.9 tok/s,不开投机是 31.1;C8 为 389.8 tok/s,不开投机是 127.0。
- 上面的 INT8 分数是不开投机测的;草稿目录不改动任何 INT8 权重文件。

### GGUF Q6_K

测试环境:单张 RTX PRO 6000 Blackwell;1 分钟快测,生成上限 512,开思考(xhigh),采样 temperature 1.0、top_p 0.95、top_k 20;每档只发与并发数相同的请求数(C1 发 1 个、C2 发 2 个、C4 发 4 个、C8 发 8 个)。数字为总吞吐 tok/s(全部输出 token ÷ 墙钟时间)。这是快测:请求少、生成短,数字不能与上面 SGLang / NInfer 各档的完整测速直接比较。NInfer 行用 `GGUF-NInfer/` 包测得,测速时服务参数为 `--max-context 32768 --kv-capacity 32768 --kv-dtype rk8v4 --max-concurrency 8`;llama.cpp 行用 `GGUF/` 包测得。

| 引擎 · 投机方式 | C1 | C2 | C4 | C8 |
|---|---:|---:|---:|---:|
| NInfer · MTP(草稿长度 3) | 131.9 | 161.9 | **235.5** | 388.1 |
| NInfer · 不开投机 | 56.0 | 93.9 | 162.1 | 298.1 |
| llama.cpp · MTP | 97.2 | 95.3 | 168.1 | 189.0 |
| llama.cpp · 不开投机 | 53.4 | 未测 | 123.0 | 未测 |

- **推荐**:NInfer + C4 + MTP(235.5 tok/s),与下文推荐启动命令(`--max-concurrency 4`)一致。只看总吞吐时 C8 更高(388.1 tok/s),需把 `--max-concurrency` 调到 8。
- **MTP 已内置**:两个包都自带 MTP 头(GGUF 为 Q8_0;NInfer 的 attention/MLP 权重为 Q6_K),不需要外挂草稿模型。单请求时 NInfer 开 MTP 为 131.9 tok/s,约为 llama.cpp 不开投机(53.4 tok/s)的 2.5 倍;llama.cpp 开 MTP 时 C1 总吞吐 97.2 tok/s(单请求解码 119.0 tok/s)。


### GGUF Q8_0

测试环境:单张 RTX PRO 6000 Blackwell。llama.cpp 行为快测口径(思考打开、融合 MTP):C1 发 4 个请求、C2 发 6 个、C4 发 12 个;数字为合计 decode tok/s。NInfer 行同口径测速(思考打开,模板默认 xhigh,生成上限 4096,temperature 1.0,top_p 0.95,top_k 20;C1 发 4、C4 发 12、C8 发 24;MTP draft-tokens 4)。

| 引擎 · 投机方式 | C1 | C2 | C4 | C8 |
|---|---:|---:|---:|---:|
| NInfer · MTP(草稿长度 4) | 109.5 | 未测 | 332.0 | **486.3** |
| llama.cpp · MTP | 85.3 | 133.6 | **190.8** | 未测 |

- **推荐**:NInfer + C8 + MTP(486.3 tok/s)。llama.cpp 最快为 C4 MTP(190.8 tok/s)。
- **MTP 已内置**:两个包都自带 MTP 头,不需要外挂草稿模型。


## 推荐启动脚本

### 量化方案

- **BF16**(`BF16/`):全部权重 BF16,原版多模态 config(保留 mrope,`mtp_num_hidden_layers=1`),无 `quantization_config`。
- **静态 FP8**(`FP8/`):官方式静态 FP8,权重 E4M3,128×128 分块,每块一个 scale(`weight_scale_inv`),激活为动态 FP8;config 只在顶层加了 FP8 `quantization_config`。
- **NVFP4 W4A16**(`NVFP4/W4A16/`):ModelOpt local-Hessian 校准;NVFP4 为 E2M1,16 个元素一块,每块一个 E4M3 尺度,另加张量级 FP32 二级尺度。MLP gate/up/down、全注意力 q/k/v/o、线性注意力 `in_proj_qkv` / `in_proj_z` / `out_proj` 共 400 个 Linear 为 NVFP4 权重、BF16 激活;线性注意力 `in_proj_a` / `in_proj_b` 与 `lm_head` 共 97 个保持 BF16。量化元数据为 ModelOpt `MIXED_PRECISION` 格式(400 层逐层标 `W4A16_NVFP4`),SGLang 自动识别为 `modelopt_mixed`。张量共 1,999 个:语言模型 1,651、视觉 333、MTP 15。
- **NVFP4 W4A4**(`NVFP4/W4A4/`):同一份校准数据和算法,同样 400 个 Linear,权重与激活都为 NVFP4(激活在推理时按 16 个元素一块量化);标准 `NVFP4` 导出,SGLang 自动识别为 `modelopt_fp4`。张量共 2,399 个:语言模型 2,051、视觉 333、MTP 15。
- **NVFP4 W4A4-W8A8**(`NVFP4/W4A4-W8A8/`):混合精度,同一份校准数据和算法。MLP gate/up/down 共 192 个 Linear 为 NVFP4 W4A4(权重与激活都为 NVFP4,激活在推理时按 16 个元素一块量化);全注意力 q/k/v/o 与线性注意力 `in_proj_qkv` / `in_proj_z` / `out_proj` 共 208 个 Linear 为 FP8 W8A8(E4M3 权重与激活,每张量静态 scale,激活 scale 由校准统计得到);线性注意力 `in_proj_a` / `in_proj_b` 与 `lm_head` 共 97 个保持 BF16。量化元数据为 ModelOpt `MIXED_PRECISION` 格式(逐层标 `NVFP4` 或 `FP8`),SGLang 自动识别为 `modelopt_mixed`。张量共 2,191 个:语言模型 1,843、视觉 333、MTP 15。
- **NVFP4 校准数据**:取自本模型自己的 RLOO 训练数据中答对且答案非空的完整轨迹(提示 + 思考 + 最终答案),512 条、约 173.5 万 token,单条最多 4,096 token;官方 GPQA、MMLU、LCB 的题目都不进校准。详见 `evaluation/NVFP4_CALIBRATION_METHOD.md`。三档的视觉塔(333 个张量)与 MTP(15 个张量)均为 BF16。
- 结构:`Qwen3_5ForConditionalGeneration`,64 层(线性注意力与全注意力 3:1 交替);FP8 包张量共 1,599 个:语言模型 1,251、视觉 333、MTP 15。

| 组件(静态 FP8 包) | 精度 |
|---|---|
| 线性注意力 `A_log`、`dt_bias`、`norm`、`conv1d`、`in_proj_a` / `in_proj_b`(×48) | BF16 |
| 线性注意力 `in_proj_qkv`、`in_proj_z`、`out_proj`(×48) | FP8 E4M3 Block128 |
| 全注意力 q/k/v/o、全部 MLP gate/up/down(与上一行合计 400 个 Linear) | FP8 E4M3 Block128 |
| `embed_tokens`、`lm_head` | BF16 |
| 视觉塔(333 个张量) | BF16,原样取自 RLOO 合并权重 |
| MTP(15 个张量) | BF16,原样取自官方 Qwen3.8-27B |

SSM 控制分支全部保留 BF16;排除清单与 Qwen 官方 FP8 一致,语言模型部分共 146 个模块保留 BF16。FP8 包冒烟通过:SGLang 免补丁加载、贪心输出与测评用纯文本版逐字一致、SGLang 图像请求、SGLang MTP、vLLM 图像请求。FP8 包在 vLLM 0.28 上开 MTP 暂不可用,推荐 SGLang。

NVFP4 三档冒烟:SGLang 免补丁加载、贪心对拍、图像请求通过。MTP 与 DFlash2 的速度和接受长度以单独的性能测评为准(C1–C16 均已跑完,见上文)。

**GGUF Q8_0**(`GGUF/`、`GGUF-NInfer/`):主干 Q8_0,内置 MTP 头(`blk.64.nextn`),不需要外挂草稿;866 个张量;`.ninfer` 由同一份 GGUF 转换;GGUF 不含视觉权重(llama.cpp 用 `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`,加 `--mmproj`);`.ninfer` 包内已含视觉部分(加 `--vision`,见下文「NInfer · 视觉」)。

**GGUF Q6_K**(`GGUF/`、`GGUF-NInfer/`):主干 Q6_K,用 512 个分块(chunk)的 imatrix 校准,并做结构保护:线性注意力(SSM)的 `ssm_alpha` / `ssm_beta` 保持 BF16,词嵌入与输出头为 Q8_0,MTP 头(`blk.64` 的 attn q/k/v/output、ffn gate/up/down 与 `nextn.eh_proj`)全部为 Q8_0,其 norm 保持 F32。GGUF 共 866 个张量、65 个块(64 层主干 + 1 层 MTP)。`.ninfer` 由同一份 GGUF 转换,主干量化相同,其 MTP 的 attention/MLP 权重为 Q6_K(`gguf_q6_k`),仅 `mtp/input_projection` 为 Q8_0;GGUF 不含视觉权重(llama.cpp 用 `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`,加 `--mmproj`);`.ninfer` 包内已含视觉部分(加 `--vision`,见下文「NInfer · 视觉」)。

### 启动命令

需官方 SGLang ≥ 0.5.19;vLLM ≥ 0.28(仅 MTP)。vLLM 在张量并行 ≥ 2 时对 NVFP4 开 MTP 有已知问题(vLLM #52480),NVFP4 用 vLLM 开 MTP 时请用单卡。FP8 包在 vLLM 0.28 上开 MTP 暂不可用,推荐 SGLang。INT8 W8A8 与 INT4 W4A16 只能用 vLLM 加载(在 0.28 上实测),命令见下文 NInfer 命令之后。

**MTP 和 DFlash2 互斥,一次启动只能开其中一种。** 下面以 `./FP8` 为例,用 BF16 档时把 `--model-path` 的路径换成 `./BF16`,用 NVFP4 档时把 `--model-path` 换成 `./NVFP4/W4A16`、`./NVFP4/W4A4` 或 `./NVFP4/W4A4-W8A8`;DFlash2 草稿用各档目录下的 `DFlash2-FP8`(如 `./FP8/DFlash2-FP8`、`./BF16/DFlash2-FP8`、`./NVFP4/W4A16/DFlash2-FP8`)。NVFP4 三档的量化格式由 SGLang 自动识别,不需要加 `--quantization`;这些 SGLang 格式的档中 vLLM 只在 FP8 包上验证过(不开 MTP),NVFP4 只在 SGLang 上测过;INT8 W8A8 与 INT4 W4A16 只能用 vLLM,在 vLLM 0.28 上测评。并发与上下文参数与性能测试一致,可按需调整。

**SGLang · MTP(包内 BF16)**

```bash
python -m sglang.launch_server \
  --model-path ./FP8 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4
```

**vLLM · MTP**

FP8 包在 vLLM 0.28 上开 MTP 暂不可用,推荐 SGLang(见上面的 SGLang MTP 命令)。

**SGLang · DFlash2**

```bash
python -m sglang.launch_server \
  --model-path ./FP8 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path ./FP8/DFlash2-FP8 \
  --speculative-draft-model-quantization fp8 \
  --speculative-num-draft-tokens 8
```

**SGLang · NVFP4 W4A16 · DFlash2**(W4A4 把两处 `W4A16` 换成 `W4A4`;NVFP4 开 MTP 时用上面的 MTP 命令,只换 `--model-path`)

```bash
python -m sglang.launch_server \
  --model-path ./NVFP4/W4A16 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path ./NVFP4/W4A16/DFlash2-FP8 \
  --speculative-draft-model-quantization fp8 \
  --speculative-num-draft-tokens 8
```

**SGLang · NVFP4 W4A4-W8A8 · DFlash2**(开 MTP 时用上面的 MTP 命令,只换 `--model-path`)

```bash
python -m sglang.launch_server \
  --model-path ./NVFP4/W4A4-W8A8 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path ./NVFP4/W4A4-W8A8/DFlash2-FP8 \
  --speculative-draft-model-quantization fp8 \
  --speculative-num-draft-tokens 8
```

本卡 BF16 / FP8 / NVFP4 的三项测评分数是在 SGLang 上开 DFlash2 测出的(NInfer 与 INT8 W8A8 不开投机,INT4 W4A16 开 MTP,GGUF 在 llama.cpp 上测,详见各节);投机解码不改变目标模型的输出分布。采样默认值见 `generation_config.json`(temperature 1.0、top_p 0.95、top_k 20)。

**SGLang / vLLM 看图**:`BF16/`、`FP8/`、`NVFP4/W4A16/`、`NVFP4/W4A4/`、`NVFP4/W4A4-W8A8/` 都是完整多模态权重:`config.json` 为 `Qwen3_5ForConditionalGeneration` 且带 `vision_config`,目录里有 `preprocessor_config.json` 与 `video_preprocessor_config.json`,权重索引覆盖全部 333 个视觉塔张量(指向同目录的 `vision-bf16.safetensors`;BF16 指向 `model-00002-of-00002.safetensors`)。上面的 SGLang、vLLM 命令原样即可接收图片,不需要额外参数;图片按 OpenAI 格式放在 `POST /v1/chat/completions` 的 `image_url` 里(请求示例见下文「NInfer · 视觉」,`model` 换成服务的模型名)。`INT8/W8A8/` 自 2026-10-09 起也能看图(`Qwen3_5ForConditionalGeneration`;BF16 视觉塔在 `model_visual.safetensors`,附 preprocessor 配置):直接用下面的 INT8 vLLM 命令即可。`INT4/W4A16/` 同样能看图(BF16 视觉塔在 `model_visual.safetensors`),用下面的 INT4 vLLM 命令即可。

#### NVFP4 · NInfer(`.ninfer`,官方 NInfer)

以 W4A4 档为例;用 W4A4-W8A8 档时把路径换成 `./NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8-MTP-DFlash2.ninfer`,`--model-id` 换成 `qwen3.8-27b-coder390-w4a4-w8a8`。

MTP-DFlash2 包内已包含 Q8 MTP 和 DFlash2 草稿，NInfer 不需要外挂草稿模型（这一点与上面 SGLang 需要传 DFlash2 草稿路径不同）；启动时用 `--spec mtp` 或 `--spec dflash2` 二选一，不加 `--spec` 即不开投机。

**图片输入**：`NVFP4-NInfer/` 下的两个 V3 MTP-DFlash2 `.ninfer` 包(W4A4 与 W4A4-W8A8)自 2026-10-09 起包含视觉部分(295,720,448 字节,由 BF16 视觉权重量化:patch embedding 为 Q6,attention q/k/v 与 MLP fc1 为 Q4,其余投影为 Q5,merger 为 Q8,norm 与 bias 保持 BF16)。文本、MTP 与 DFlash2 权重逐字节不变。在下面任一 NInfer 命令后加 `--vision`,图片按 OpenAI 格式放在 `POST /v1/chat/completions` 的 `image_url` 里。不加 `--vision` 时和以前一样只跑文本。V2 包(`-NInferV2-NOT-FOR-V3`)未改动,仍不含视觉。2026-10-09 GPU 实测(单张 RTX PRO 6000,NInfer-all 64492cb 加 `--vision`,看图问题):两个 MTP-DFlash2 包都回答正确。W4A4-MTP-DFlash2:MTP(3 个草稿 token)接受长度 2.89,decode 153 tok/s;DFlash2(7 个草稿 token)接受长度 3.53,decode 185 tok/s。W4A4-W8A8-MTP-DFlash2:MTP 3.19,164 tok/s;DFlash2 3.74,195 tok/s。

**NInfer · 不开投机**

```bash
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8
```

**NInfer · MTP(草稿长度 4)**

```bash
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec mtp --draft-tokens 4 --lm-head-draft
```

**NInfer · DFlash2(草稿长度 8)**

```bash
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec dflash2 --draft-tokens 8 --lm-head-draft
```

**NInfer · 视觉(图片输入),每个包一条命令**

每条命令就是上面对应的 NInfer 命令加 `--vision`,不需要别的文件:视觉部分已在每个 V3 `.ninfer` 包内,同目录的 `vision-bf16.safetensors` 运行时用不到。

```bash
# W4A4 · MTP-DFlash2 包 · 不开投机
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --vision

# W4A4 · MTP-DFlash2 包 · MTP
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec mtp --draft-tokens 4 --lm-head-draft \
  --vision

# W4A4 · MTP-DFlash2 包 · DFlash2
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec dflash2 --draft-tokens 8 --lm-head-draft \
  --vision

# W4A4-W8A8 · MTP-DFlash2 包 · 不开投机
ninfer-serve ./NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4-w8a8 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --vision

# W4A4-W8A8 · MTP-DFlash2 包 · MTP
ninfer-serve ./NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4-w8a8 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec mtp --draft-tokens 4 --lm-head-draft \
  --vision

# W4A4-W8A8 · MTP-DFlash2 包 · DFlash2
ninfer-serve ./NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4-w8a8 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec dflash2 --draft-tokens 8 --lm-head-draft \
  --vision
```

图片请求:按 OpenAI 格式在 `POST /v1/chat/completions` 里放 `image_url`;`url` 填图片的 `http(s)://` 链接,也可以传本地图片的数据 URI;`model` 要与 `--model-id` 一致。

```bash
curl http://127.0.0.1:19931/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.8-27b-coder390-w4a4",
    "messages": [{"role": "user", "content": [
      {"type": "image_url", "image_url": {"url": "https://example.com/demo.png"}},
      {"type": "text", "text": "Describe this image."}
    ]}],
    "max_tokens": 2048
  }'
```

健康检查:`curl -sf http://127.0.0.1:19931/health`。对话接口为 `POST /v1/chat/completions`,请求里的 `model` 要与 `--model-id` 一致。

**vLLM · INT4 W4A16 · MTP(内置头)· 文本与图像**

```bash
VLLM_USE_FLASHINFER_SAMPLER=0 \
vllm serve ./INT4/W4A16 \
  --trust-remote-code --dtype bfloat16 \
  --max-model-len 102400 --served-model-name qwen3.8-27b-coder390-int4-w4a16 \
  --gpu-memory-utilization 0.85 --max-num-seqs 8 \
  --reasoning-parser qwen3 \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}'
```

图片按 OpenAI 格式放在 `image_url` 里,用同一个服务即可,不需要额外参数:

```bash
curl -s http://127.0.0.1:8000/v1/chat/completions -H 'Content-Type: application/json' -d '{
  "model": "qwen3.8-27b-coder390-int4-w4a16",
  "messages": [{"role": "user", "content": [
    {"type": "image_url", "image_url": {"url": "https://example.com/chart.png"}},
    {"type": "text", "text": "描述这张图片。"}
  ]}],
  "max_tokens": 2048
}'
```

去掉 `--speculative-config` 即不开投机。在 vLLM 0.28 上实测(`VLLM_USE_FLASHINFER_SAMPLER=0` 与实测设置一致);SGLang 与 NInfer 未用此包测试。`--reasoning-parser qwen3` 会把思考单独返回。

**vLLM · INT8 W8A8(不开投机)**

```bash
VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel \
VLLM_USE_FLASHINFER_SAMPLER=0 \
vllm serve ./INT8/W8A8 \
  --trust-remote-code --dtype bfloat16 \
  --max-model-len 102400 --served-model-name qwen3.8-27b-coder390-int8-w8a8 \
  --gpu-memory-utilization 0.85 --max-num-seqs 8 \
  --reasoning-parser qwen3
```

RTX PRO 6000 Blackwell 上 vLLM 的 Cutlass INT8 内核不可用,不关掉就起不来,须用 `VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel` 关掉;关掉后改走 Triton INT8 内核(启动日志里能看到 `TritonInt8ScaledMMLinearKernel`)。`VLLM_USE_FLASHINFER_SAMPLER=0` 与测试时一致。在 vLLM 0.28 上实测;SGLang 不能加载本包(`ModelOptFp8Config` 报错)。`--reasoning-parser qwen3` 会把思考内容单独放进 `reasoning_content`(测分时未开)。

**vLLM · INT8 W8A8 · MTP(外挂草稿 `INT8/W8A8/MTP-BF16/`)**

```bash
VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel \
VLLM_USE_FLASHINFER_SAMPLER=0 \
vllm serve ./INT8/W8A8 \
  --trust-remote-code --dtype bfloat16 \
  --max-model-len 102400 --served-model-name qwen3.8-27b-coder390-int8-w8a8 \
  --gpu-memory-utilization 0.85 --max-num-seqs 8 \
  --reasoning-parser qwen3 \
  --speculative-config '{"method":"mtp","model":"./INT8/W8A8/MTP-BF16","num_speculative_tokens":3}'
```

在 RTX PRO 6000 Blackwell 上按上面的命令设置 `VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel` 和 `VLLM_USE_FLASHINFER_SAMPLER=0`。新表的两行都用了这两项设置。

**vLLM · INT8 W8A16(不开投机)**

```bash
VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel VLLM_USE_FLASHINFER_SAMPLER=0 \
vllm serve ./INT8/W8A16 \
  --served-model-name qwen3.8-27b-coder390-int8-w8a16 \
  --trust-remote-code --max-model-len 102400 --max-num-seqs 8 \
  --gpu-memory-utilization 0.90 --reasoning-parser qwen3
```

**vLLM · INT8 W8A16 · MTP(外挂草稿 `INT8/W8A16/MTP-BF16/`)**

```bash
VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel VLLM_USE_FLASHINFER_SAMPLER=0 \
vllm serve ./INT8/W8A16 \
  --served-model-name qwen3.8-27b-coder390-int8-w8a16 \
  --trust-remote-code --max-model-len 102400 --max-num-seqs 8 \
  --gpu-memory-utilization 0.90 --reasoning-parser qwen3 \
  --speculative-config '{"method":"mtp","model":"./INT8/W8A16/MTP-BF16","num_speculative_tokens":3}'
```

**GGUF / GGUF-NInfer**

`.ninfer` 用 NInfer-all(`iamwavecut/ninfer-all` 的 master 分支)加载:包里保留的是 GGUF 量化块,其他 NInfer 构建不能读。llama.cpp 需支持 `--spec-type draft-mtp` 的上游版本。NInfer 的 `--kv-capacity` 是所有请求共享的 KV 池;llama.cpp 的 `-c 409600 -np 4` 会把上下文平分给 4 个槽位,每个请求最多 102,400 token,够单请求写到 94K。对话接口为 `POST /v1/chat/completions`;NInfer 请求里的 `model` 要与 `--model-id` 一致。视觉:llama.cpp 用 `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`(`--mmproj`;629,247,008 字节,sha256 `cae9799dc9196449b0d83f716e64af89d5cf65147510462e5a629a2aa23adb32`)。每个 `.ninfer` 包内都含视觉部分;`ninfer-serve` 加 `--vision` 即可输入图片(见下文「NInfer · 视觉」)。

**16G 显存 / 单流推荐**：显存 16G、只需单路使用时，更推荐 `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer`。它是本仓最小的 NInfer 包（13,568,617,472 字节，约 12.6 GiB），内置 Q4_K MTP 头和视觉部分（加 `--vision` 即可看图，不需要 mmproj），官方 NInfer-all master 与社区分支 ninfer-fusion-kvmem 都能直接运行。16G 卡未实测，以上是按文件体积判断；上下文先从 32K 起，显存不够再调小。

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer \
  --model-id qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --max-context 32768 --kv-capacity 32768 --kv-dtype rk8v4 \
  --max-concurrency 1 --spec mtp --draft-tokens 4 --vision
```

**社区分支 ninfer-fusion-kvmem**:Q2～Q4 LynnStyle 的 NInfer 包(`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q4MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q4MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q4MTP.ninfer`)内置 MTP 头已改为 Q4_K,在官方 NInfer-all master 和社区分支 ninfer-fusion-kvmem 上都能正常加载并开启 MTP(2026-10-11 实测)。`GGUF/` 下的 `.gguf` 内置 MTP 头仍为 Q4_0,llama.cpp 支持。Q8 MTP 版本继续保留作为备选(权重相同,只把 MTP 头改为 Q8_0):llama.cpp 用 `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf`、`GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf`、`GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf`;NInfer 用 `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.ninfer`、`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.ninfer`(model id 分别为 `qwen3.8-27b-coder390-Q2LynnStyle-Q8Mtp`、`qwen3.8-27b-coder390-Q3LynnStyle-Q8Mtp`、`qwen3.8-27b-coder390-Q4LynnStyle-Q8Mtp`)。

**MTP 与 DFlash2**:`GGUF/` 与 `GGUF-NInfer/` 下所有包都内置 MTP 头(Q2 / Q3 / Q4 LynnStyle 为内置 **Q4** MTP(`.gguf` 为 Q4_0,`-Q4MTP.ninfer` 为 Q4_K);其 `-Q8MTP` 版本为 Q8_0 MTP 头)。开启方式:NInfer 加 `--spec mtp --draft-tokens N`,llama.cpp 加 `--spec-type draft-mtp --spec-draft-n-max N`;省略这两个参数即不开投机。DFlash2 是外挂草稿模型,不在这些 GGUF / NInfer 包里,本仓库不提供 GGUF / GGUF-NInfer 用的 DFlash2 草稿;需要 DFlash2 时请用本仓库 BF16 / FP8 / NVFP4 各档自带的 `DFlash2-FP8/`(SGLang `--speculative-algorithm DFLASH`)或 `NVFP4-NInfer/` 的 `.ninfer` 包(`--spec dflash2`)。MTP 与 DFlash2 互斥:同一个服务只能开其中一种,不要同时开。

#### GGUF · NInfer

**NInfer · GGUF Q3 LynnStyle-16G · MTP + 视觉(草稿长度 4,推荐并发 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-Q3LynnStyle16G-MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-q3lynnstyle16g-mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4 --vision
```

16G 显存 / 单路可先用 `--max-context 32768 --kv-capacity 32768 --max-concurrency 1`,显存够再调大。本 `.ninfer` 已内置 Q8 视觉塔,加 `--vision` 即可。同档 GGUF 仍只含文本(llama.cpp 看图用 `--mmproj`)。

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

#### GGUF · llama.cpp

**llama.cpp · GGUF Q2 LynnStyle · MTP(代表命令;换 `-m` 即可切到 Q3 / Q4 / Q6_K / Q8_0)**

```bash
llama-server -m ./GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf \
  -c 409600 -np 4 -ngl 99 --jinja \
  --host 127.0.0.1 --port 8080 \
  --alias qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --spec-type draft-mtp --spec-draft-n-max 4
```

换其他 GGUF 档只需改 `-m` 为 `...-Q3LynnStyle-MTP.gguf`、`...-Q4LynnStyle-MTP.gguf`、`...-Q6_K-MTP.gguf` 或 `...-Q8_0-MTP.gguf`(并相应改 `--alias`,例如 `qwen3.8-27b-coder390-q6k-mtp`、`qwen3.8-27b-coder390-q8-mtp`)。MTP 已融合进 GGUF(`blk.64`),不要再外挂 draft;日志应出现 `creating MTP draft context against the target model`。需要图像输入时加 `--mmproj ./GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`。

**llama.cpp · GGUF Q3 LynnStyle-16G · MTP(16G 显存)**

```bash
llama-server -m ./GGUF/Qwen3.8-27B-Coder390-Q3LynnStyle16G-MTP.gguf \
  -c 32768 -np 1 -ngl 99 --jinja \
  --temp 1.0 --top-p 0.95 --top-k 20 \
  --host 127.0.0.1 --port 8080 \
  --alias qwen3.8-27b-coder390-q3lynnstyle16g-mtp \
  --spec-type draft-mtp --spec-draft-n-max 4
```

本档未在 16G 卡上实测,上面按单路 32K 上下文给出,显存够再调大 `-c` / `-np`。MTP 已融合进 GGUF(Q4_K,`blk.64`),不要再外挂 draft。看图时加 `--mmproj ./GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`。本档的三科成绩是用 llama.cpp + 外挂 DFlash2 草稿测得(C4,100K 上下文,生成上限 94,208,不计超时,xhigh)。速度在一张 RTX PRO 6000 Blackwell 上测得:llama.cpp 融合 MTP 4096 长测 C1/C2/C4 = 31.9/46.6/78.1 tok/s(接受率 0.597);NInfer 512 短测 C1/C2/C4/C8 = 33.5/44.7/77.4/127.0 tok/s(接受率 0.488)。长短测协议不同。

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

### `FP8/`(主包 19 个文件,31,262,188,871 字节)

`FP8/SHA256SUMS` 覆盖下表前 18 个文件。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `FP8/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `FP8/config.json` | 17,784 | `9e58e8daf2914c2d11c07449dc7f03bbb822ba39dec37c4c5b3bd1f623492f90` |
| `FP8/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `FP8/model.safetensors.index.json` | 135,976 | `989573833195e17342983c7fd109e010155c423a355068b5aceb6631fcee83f2` |
| `FP8/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `FP8/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `FP8/text-01.safetensors` | 2,542,796,928 | `54d83c1d36631de231876217a8e0c2483eccee8746369a482b79442bdfc5d958` |
| `FP8/text-02.safetensors` | 3,998,718,144 | `5b1e34725cd88924495765149ff816903d702180c72561c2e22e8377e2044fa8` |
| `FP8/text-03.safetensors` | 3,969,173,888 | `5e2376d6cce25aecf2d8901959f9d6f98801a0b2e98331f4088481bf839c9cf3` |
| `FP8/text-04.safetensors` | 3,925,079,000 | `669b87fd69d2de004073ed633f8e2890c8c9c90e1101bd59c859f1431b5cb967` |
| `FP8/text-05.safetensors` | 3,994,338,456 | `3f150179f9e3f03e2ef2e1afc805e7d745c1ab88dd72776fadf7c33f1d73ae67` |
| `FP8/text-06.safetensors` | 3,920,901,280 | `4d658974b7efb906972bc66cb4fd6dc7f1b7ac1fa79a7db068442314e3bf75d4` |
| `FP8/text-07.safetensors` | 3,972,285,640 | `d155ad91985b57e2515cea321a474708dd162665d1f5870df1c85601a2ca9b2c` |
| `FP8/text-08.safetensors` | 3,147,842,216 | `e37d025cd9bcacdd00fa0969f5c827d2504019c020585dfe1aca3934152b7700` |
| `FP8/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `FP8/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `FP8/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `FP8/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `FP8/SHA256SUMS` | 1,570 | (校验清单本身) |

### `FP8/DFlash2-FP8/`(4 个文件,2,407,384,680 字节)

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `FP8/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `FP8/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `FP8/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `FP8/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `BF16/`(12 个文件,55,583,125,732 字节;DFlash2 子目录另列在下面)

`BF16/SHA256SUMS` 覆盖下表前 11 个文件。`mtp-bf16.safetensors` 与 FP8 包中的同名文件逐字节相同。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `BF16/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `BF16/config.json` | 3,799 | `b25e4020b4f791f2b20a3bf486f7ded5116fa0680cf7aa2ac50f80ee353663ce` |
| `BF16/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `BF16/model-00001-of-00002.safetensors` | 49,825,162,976 | `ed83b8a41d447f4592c490b6135917419aea00fc7dbf9d6f5eb9525631f86fe0` |
| `BF16/model-00002-of-00002.safetensors` | 4,888,445,168 | `5c56330027c0eb9a776e89f80ef1643e60b1c2ae3adbbaf4b5142ebf7cb57271` |
| `BF16/model.safetensors.index.json` | 112,034 | `e8e177ff98a940337d496a0820e51c9fb68b2ab98fb68647d26aef9368dedeab` |
| `BF16/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `BF16/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `BF16/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `BF16/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `BF16/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `BF16/SHA256SUMS` | 990 | (校验清单本身) |

### `BF16/DFlash2-FP8/`(4 个文件,2,407,384,680 字节)

与 `FP8/DFlash2-FP8/` 逐字节相同。

| 文件 | 字节数 | SHA256 |
|---|---:|---|
| `BF16/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `BF16/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `BF16/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `BF16/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `NVFP4/W4A16/`(主包 17 个文件,20,613,406,953 字节;DFlash2 子目录另列在下面)

`NVFP4/W4A16/SHA256SUMS` 覆盖下表前 16 个文件,其自身 SHA256 为 `ecc28d31be0d97e23509af61625251af14980db5b67189a1d1ca75a3fc9652f3`。`mtp-bf16.safetensors` 与 FP8 包中的同名文件逐字节相同。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `NVFP4/W4A16/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `NVFP4/W4A16/config.json` | 69,785 | `e71fd7b2cbade1ebb8be0382c81f7bf69eb1e039e30734914378d2c41217ef62` |
| `NVFP4/W4A16/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `NVFP4/W4A16/hf_quant_config.json` | 65,978 | `2ff46ad6bc27eb740e29831e642522ee4c110fea1ae9520b89272566b0d12d62` |
| `NVFP4/W4A16/model.safetensors.index.json` | 171,578 | `13651163cd9c1c20af460e6595616075a1f0d7f5995a3efc46d3ac449bc4f51e` |
| `NVFP4/W4A16/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `NVFP4/W4A16/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `NVFP4/W4A16/text-01.safetensors` | 3,994,732,420 | `dfdd15ab6b889eee01357d38910552bb0968248df0e21a9564d7ae29482d3139` |
| `NVFP4/W4A16/text-02.safetensors` | 3,981,611,096 | `8e4a2a7b4c9325c27380a41de0fb51028065ff97090af9d4213cb5a50629d517` |
| `NVFP4/W4A16/text-03.safetensors` | 3,960,207,028 | `c92929b575321e080d0ea2ca7c1a26b49fa638a8d03bacfef2cd0b6f83237689` |
| `NVFP4/W4A16/text-04.safetensors` | 3,983,003,152 | `feb69e1a4c7a374f1a11cf3e4af5d70fdd870963519e71469eb067a86fb35634` |
| `NVFP4/W4A16/text-05.safetensors` | 2,902,646,528 | `28dda5f9a39b83736ae458c2e626b429bbd18e408be63ef598dbb47327c97e3e` |
| `NVFP4/W4A16/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `NVFP4/W4A16/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `NVFP4/W4A16/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `NVFP4/W4A16/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4/W4A16/SHA256SUMS` | 1,399 | `ecc28d31be0d97e23509af61625251af14980db5b67189a1d1ca75a3fc9652f3` |

### `NVFP4/W4A16/DFlash2-FP8/`(4 个文件,2,407,384,680 字节)

与 `FP8/DFlash2-FP8/` 逐字节相同。

| 文件 | 字节数 | SHA256 |
|---|---:|---|
| `NVFP4/W4A16/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `NVFP4/W4A16/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `NVFP4/W4A16/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `NVFP4/W4A16/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `NVFP4/W4A4/`(主包 17 个文件,20,613,386,462 字节;DFlash2 子目录另列在下面)

`NVFP4/W4A4/SHA256SUMS` 覆盖下表前 16 个文件,其自身 SHA256 为 `5aea8bb9c1f1979661bfa5c1216de7aafeb64cd708aa8cc71f3b185c224cfde0`。`mtp-bf16.safetensors` 与 FP8 包中的同名文件逐字节相同。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `NVFP4/W4A4/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `NVFP4/W4A4/config.json` | 18,130 | `4df9be90e61070a553447129e504fea7be8e60dc22ae9e9f7a85bdfc140c0054` |
| `NVFP4/W4A4/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `NVFP4/W4A4/hf_quant_config.json` | 13,956 | `d3603810fba7548903ba2f3382fdd30f5704d3b6e0688e2dccf34fe023c11d31` |
| `NVFP4/W4A4/model.safetensors.index.json` | 207,580 | `541d828aed73b4df9f9fc86be7111aa404983d55d9797ca1cfb3e71474bfd3b7` |
| `NVFP4/W4A4/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `NVFP4/W4A4/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `NVFP4/W4A4/text-01.safetensors` | 3,994,737,240 | `1ea4cf8a0036b5d87815b65a38d0d2c00b37c010056a03d0db1fc72eb6c829bc` |
| `NVFP4/W4A4/text-02.safetensors` | 3,981,625,016 | `c9a0d2c3c506ad17da4dd47bf571326eef201e40db6f259a9d42971778033359` |
| `NVFP4/W4A4/text-03.safetensors` | 3,960,220,600 | `3c8778873d2ef08c512b7e457d61a6ac9ea047975e4723cd3804d0d18e86c1db` |
| `NVFP4/W4A4/text-04.safetensors` | 3,983,016,880 | `40081557adf0713f1624cdb2d1c53ea5fd2a30e09f5f964799457b23e4e2304d` |
| `NVFP4/W4A4/text-05.safetensors` | 2,902,647,672 | `0266ba0fa0354a4c409bc180c9d9a67ed12c915fc9886970745c87f8babcaa24` |
| `NVFP4/W4A4/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `NVFP4/W4A4/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `NVFP4/W4A4/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `NVFP4/W4A4/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4/W4A4/SHA256SUMS` | 1,399 | `5aea8bb9c1f1979661bfa5c1216de7aafeb64cd708aa8cc71f3b185c224cfde0` |

### `NVFP4/W4A4/DFlash2-FP8/`(4 个文件,2,407,384,680 字节)

与 `FP8/DFlash2-FP8/` 逐字节相同。

| 文件 | 字节数 | SHA256 |
|---|---:|---|
| `NVFP4/W4A4/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `NVFP4/W4A4/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `NVFP4/W4A4/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `NVFP4/W4A4/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `NVFP4/W4A4-W8A8/`(主包 18 个文件,23,769,634,648 字节;DFlash2 子目录另列在下面)

`NVFP4/W4A4-W8A8/SHA256SUMS` 覆盖下表前 17 个文件,其自身 SHA256 为 `c177f4907a7dd037efe91b8d34927dd3a3624227f259238b82db0f12f8b0b8e2`。`mtp-bf16.safetensors` 与 FP8 包中的同名文件逐字节相同。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `NVFP4/W4A4-W8A8/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `NVFP4/W4A4-W8A8/config.json` | 71,802 | `d1cc2af6971ae0bb776f5f36eb1c923546742fda3a83e6d8355720a652e27b5d` |
| `NVFP4/W4A4-W8A8/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `NVFP4/W4A4-W8A8/hf_quant_config.json` | 43,976 | `2bd65f6f325ea8e8e40c37b6e7d386633ac6236db6fcde3d7e9de128d961a599` |
| `NVFP4/W4A4-W8A8/model.safetensors.index.json` | 187,500 | `1257454a255efb01ba8047fe41bf34460b551c210db7cc8c4713f1c01150c69d` |
| `NVFP4/W4A4-W8A8/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `NVFP4/W4A4-W8A8/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `NVFP4/W4A4-W8A8/text-01.safetensors` | 3,981,847,464 | `b5502eb2c54c5a53ee08712c48935023ed924e0f054acb3573e1288095d2e3ff` |
| `NVFP4/W4A4-W8A8/text-02.safetensors` | 3,956,368,808 | `f08e7fccb4d2467af8b2b2d3bc587e6e8404b5764e9fc8e640ad0ff4f445d293` |
| `NVFP4/W4A4-W8A8/text-03.safetensors` | 3,956,368,928 | `8299287bb0e570efda02bcbe67c4bd9c5378b44bbf84c17ff062fc5ce6ba53e0` |
| `NVFP4/W4A4-W8A8/text-04.safetensors` | 3,967,919,248 | `bea560dda7b885cca987b8352e2ae659acaee70c3255fde7fa487c1fd73badf2` |
| `NVFP4/W4A4-W8A8/text-05.safetensors` | 3,573,130,520 | `a969faa5f2a3963450ad64bb84664035676c426877499593aea91080643ba6fa` |
| `NVFP4/W4A4-W8A8/text-06.safetensors` | 2,542,796,928 | `54d83c1d36631de231876217a8e0c2483eccee8746369a482b79442bdfc5d958` |
| `NVFP4/W4A4-W8A8/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `NVFP4/W4A4-W8A8/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `NVFP4/W4A4-W8A8/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `NVFP4/W4A4-W8A8/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4/W4A4-W8A8/SHA256SUMS` | 1,485 | `c177f4907a7dd037efe91b8d34927dd3a3624227f259238b82db0f12f8b0b8e2` |

### `NVFP4/W4A4-W8A8/DFlash2-FP8/`(4 个文件,2,407,384,680 字节)

与 `FP8/DFlash2-FP8/` 逐字节相同。

| 文件 | 字节数 | SHA256 |
|---|---:|---|
| `NVFP4/W4A4-W8A8/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `NVFP4/W4A4-W8A8/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `NVFP4/W4A4-W8A8/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `NVFP4/W4A4-W8A8/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `evaluation/`

成绩、性能、冒烟(静态 FP8 与 BF16)与校准记录。`evaluation/SHA256SUMS` 覆盖下表前 22 个文件(表中共 23 行,最后一行为校验清单本身)。`NVFP4_*.results.summary.json` 为 NVFP4 三档三项测评的原始汇总(`NVFP4_MIXED_*` 为 W4A4-W8A8 档)。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `evaluation/SCORES_STATICFP8.json` | 3,935 | `eba280071a75fc8dd90e5866df783a68ccd08bdb4d4dde85c062f7d398ea0eb0` |
| `evaluation/BENCH_STATICFP8.json` | 6,511 | `c62c6c82f234a27fa93faf691d1d4ee01a2408a18bbe94efafe341e4ad10db20` |
| `evaluation/BENCH_STATICFP8.md` | 1,405 | `ea662952b73446d5b88422b2a3dbcc215829521cc001cb26ad492caa137fa2ac` |
| `evaluation/SMOKE_STATICFP8.json` | 2,119 | `1a2383ad0f8e26f02ec7d65db418fea2bd50e73458ee247cc9d2f9322ffbb833` |
| `evaluation/SCORES_BF16.json` | 4,279 | `76e921712bab0577853499d3f67440de6f3577f4818c40184f4b0580e5f7a77e` |
| `evaluation/SMOKE_BF16.json` | 889 | `01ea5e4518615af2a3c574fa49ae6f2a4819482bbaafce2695b62016b14a582f` |
| `evaluation/SCORES_NVFP4_W4A16.json` | 3,319 | `7294901f3493f593e0de6d7f95b860c44578780300aebcb52bca6f06ead1ddfd` |
| `evaluation/BENCH_NVFP4_W4A16.json` | 3,992 | `1877fe3e4126de72ad1165a1e0f5d1dd569f73f1dcd16a93249c389b3d47f2d3` |
| `evaluation/SCORES_NVFP4_W4A4.json` | 3,212 | `eee169bb6cde4d048d12d604a72c7570b0ebd0fee88a3c19d39ad4493a912f30` |
| `evaluation/BENCH_NVFP4_W4A4.json` | 3,922 | `2ebedf7e221f69765364a73deaca459a9636a4c190b2cbde06de8d119a15f4a7` |
| `evaluation/SCORES_NVFP4_MIXED.json` | 3,063 | `845027e6324b5300ed5ce306b3515b559f75b5c0e8ef1aac4d1b98d62d135454` |
| `evaluation/BENCH_NVFP4_MIXED.json` | 4,038 | `3d6f348425b6fd184d620c101a803139d7bcc0d620ff3237c28cc627e8f85ca7` |
| `evaluation/NVFP4_CALIBRATION_METHOD.md` | 3,712 | `e3678dbe9020a83998a5c66207b515376defebd78e6fadf4f63e55059785e03a` |
| `evaluation/NVFP4_W4A16_gpqa.results.summary.json` | 1,182 | `4835f8cf4b403047487b0a52db88574a2125ba103a30404b8b9e97e7112511bd` |
| `evaluation/NVFP4_W4A16_lcb.results.summary.json` | 2,642 | `56990657d101c2ce47b44d5fcdcb498a286bbf6093ae7790cde5809ba266d5a1` |
| `evaluation/NVFP4_W4A16_mmlu.results.summary.json` | 4,075 | `e9d507b5da71621032a13f487eb60159e0369c025ed12c4fa613e70b6f0f71e5` |
| `evaluation/NVFP4_W4A4_gpqa.results.summary.json` | 1,189 | `961b3f98b4a54d78d1983896a0b12b10a3d1e7facf456f594793dc7bbefb5e70` |
| `evaluation/NVFP4_W4A4_lcb.results.summary.json` | 2,640 | `bd371e898121ee5dd6fda47065254cc2137ba783b466b3830f0c58d631137688` |
| `evaluation/NVFP4_W4A4_mmlu.results.summary.json` | 4,076 | `b468cf81854562e0e20bf232ddd13b68ed58e10a4da840e6bd3c20564d20f74a` |
| `evaluation/NVFP4_MIXED_gpqa.results.summary.json` | 1,171 | `72c000ffc4ff15db8d542b6d9d924c5795ad491d946dee0f6c3f11b0e62151f1` |
| `evaluation/NVFP4_MIXED_lcb.results.summary.json` | 2,641 | `7e3d3146dd98954ef80358ce88f5505798f77427c1a5ddf73c65dd728cf3afc2` |
| `evaluation/NVFP4_MIXED_mmlu.results.summary.json` | 4,077 | `3088c6254dad8af25ace3b44f4cfa688b192eca98f693afa1c595df121cb9afb` |
| `evaluation/SHA256SUMS` | 2,071 | (校验清单本身) |

### 校验

```bash
(cd FP8 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd BF16 && sha256sum -c SHA256SUMS)
(cd NVFP4/W4A16 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd NVFP4/W4A4 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd NVFP4/W4A4-W8A8 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd NVFP4-NInfer/W4A4 && sha256sum -c SHA256SUMS)
(cd NVFP4-NInfer/W4A4-W8A8 && sha256sum -c SHA256SUMS)
(cd INT4/W4A16 && sha256sum -c SHA256SUMS)
(cd INT8/W8A8 && sha256sum -c SHA256SUMS && cd MTP-BF16 && sha256sum -c SHA256SUMS)
(cd INT8/W8A16 && sha256sum -c SHA256SUMS && cd MTP-BF16 && sha256sum -c SHA256SUMS)
(cd GGUF && sha256sum -c SHA256SUMS)
(cd GGUF-NInfer && sha256sum -c SHA256SUMS)
(cd evaluation && sha256sum -c SHA256SUMS)
```

## NInfer 加载说明

- 只有 NInfer 引擎能加载 `.ninfer`;SGLang、vLLM、llama.cpp、transformers 都不能读。
- 使用官方 NInfer([`Neroued/ninfer`](https://github.com/Neroued/ninfer) 的 master 分支)的 `ninfer-serve`,无需打补丁(只有由 GGUF 转换的 `.ninfer` 需用 NInfer-all)。实测硬件为单张 RTX PRO 6000 Blackwell(算力 12.0);NInfer 并发上限为 8。
- `NVFP4-NInfer/W4A4/` 与 `NVFP4-NInfer/W4A4-W8A8/` 各有一个带 MTP 与 DFlash2 的 `.ninfer` 文件:文本路径与 2026-10-05 测分时相同,包内另含 Q8 MTP、DFlash2 草稿、proposal head,以及 2026-10-09 加入的视觉部分,加 `--vision` 可输入图片;同一文件夹的 `vision-bf16.safetensors` 是这部分的 BF16 原始权重,运行时不需要。MTP 投影为 Q8:其中几个矩阵形状在 NInfer 里没有 BF16 内核,用 BF16 会在建计算图时退出。
- MTP 与 DFlash2 一次启动只能选一种(`--spec mtp` 或 `--spec dflash2`);`--lm-head-draft` 须与 `--spec` 一起用。MTP 草稿长度可取 1–5,DFlash2 可取 1–15;上文「启动命令」中的 NInfer 命令用测速时的 4 与 8。DFlash2 草稿已打在包里,不需要另载 `DFlash2-FP8/` 目录。
- 下面的上下文参数已验证能启动:`--max-context 102400 --kv-capacity 819200 --max-concurrency 8 --kv-dtype fp8`。`--kv-capacity` 须落在 `max-context` 到 `max-context × max-concurrency` 之间,819,200 正好是 8 × 102,400。
- NVFP4 目录下的 HF 包仍用 SGLang(可开 MTP 或 DFlash2);与 NInfer 包互不通用。

### NInfer V2 包(仅 Tesla V100)

文件名带 `NInferV2-NOT-FOR-V3` 的四个包只给 Tesla V100 用（ninfer-v100 分支）；其他显卡请用不带这个后缀的包。

- 文件名含 `NInferV2-NOT-FOR-V3` 的 4 个包是 NInfer **V2** 容器,只给 Tesla V100 的 `ninfer-v100` 分支用。官方 NInfer(`ninfer-serve`)只读 V3,会拒绝这些文件;其他显卡请用上面不带 `NInferV2` 的 V3 包。不要把 V2 包改名成 V3 文件名,也不要用它们替换 V3 包。
- 两个纯文本包(`Qwen3.8-27B-Coder390-W4A4-NInferV2-NOT-FOR-V3.ninfer`、`Qwen3.8-27B-Coder390-W4A4-W8A8-NInferV2-NOT-FOR-V3.ninfer`)不含 MTP 与 DFlash2,不要加 `--spec`;两个 MTP-DFlash2 包(`…-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer`)可加 `--spec mtp` 或 `--spec dflash2`,包内已包含 MTP 和 DFlash2 草稿,不需要外挂草稿模型。四个 V2 包都不含视觉部分,不能输入图片(不支持 `--vision`);需要看图请用 V3 包。
- V100 上没有 NVFP4 KV 与 K8V4 KV,不要用 V3 的 `--kv-dtype rk8v4` 或 `--kv-capacity 819200`;在 V100 上起服务时加 `--prefill-chunk 2048`。
- V2 包未单独测评,只做了 SHA256 校验。`SHA256SUMS` 里 V2 的两行放在 `#` 注释行之后,与 V3 分开。

```bash
# V100 ninfer-v100 分支 · 纯文本包(不加 --spec)
ninfer ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-NInferV2-NOT-FOR-V3.ninfer \
  --prompt "用三句话说明 prefill 和 decode。" \
  --max-context 8192 \
  --max-new 256

# V100 ninfer-v100 分支 · MTP-DFlash2 包(开 MTP)
ninfer ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer \
  --prompt "用三句话说明 prefill 和 decode。" \
  --max-context 8192 \
  --max-new 256 \
  --spec mtp --draft-tokens 3
```

### `NVFP4-NInfer/W4A4/`(5 个文件,68,925,700,831 字节)

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer` | 23,773,675,264 | `3c2d39f364a8932c82b41d4c424c940285573b0309481a67c2fde048368bf808` |
| `NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-NInferV2-NOT-FOR-V3.ninfer` | 20,752,831,236 | `eac9e3d47fe6731c021d7154fd2f801a8263ac6d00e6d16834e54947ee58bcf8` |
| `NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer` | 23,477,696,516 | `e93f3b83f7589fdb776ce25a0cdef98ed1892e101ef564fdb844a5aacff13d22` |
| `NVFP4-NInfer/W4A4/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4-NInfer/W4A4/SHA256SUMS` | 591 | `1b84a36b7b7c150376bdb00c61c629565040b92b0b8a84784dcdcb8c35dc6b3e` |

### `NVFP4-NInfer/W4A4-W8A8/`(5 个文件,68,925,700,846 字节)

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8-MTP-DFlash2.ninfer` | 23,773,675,264 | `cccfbf0ba3ec4e86837e8e6481ec32ee3e10636633e421429f19ea3ea97926e2` |
| `NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-W4A4-W8A8-NInferV2-NOT-FOR-V3.ninfer` | 20,752,831,236 | `01a4440f77dcdac66906e1bb061e1c38c6b236b805ff7bcb644aedf90f06a038` |
| `NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-W4A4-W8A8-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer` | 23,477,696,516 | `099b2d00fa3982d601218d6587dc25222cc21ef708de7dab8b2e2c0bee60da74` |
| `NVFP4-NInfer/W4A4-W8A8/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4-NInfer/W4A4-W8A8/SHA256SUMS` | 606 | `78a23ee97290b0d82b7d2a8fb163a2dab4479592568d36bd093ab82ad8747549` |

## INT4 W4A16 说明

- 文本与图像:架构为 `Qwen3_5ForConditionalGeneration`(64 层文本,线性注意力与全注意力 3:1 交替)。BF16 视觉塔单独存为 `model_visual.safetensors`(333 个张量,921,497,224 字节,与 `INT8/W8A8/` 中的是同一个文件),附 `preprocessor_config.json` / `video_preprocessor_config.json`。内置 MTP 头为 BF16(`model_mtp.safetensors`,15 个张量)。不含 DFlash2 草稿。
- 量化:用 llm-compressor 做 GPTQ W4A16,INT4 权重,对称,分组大小 128,静态激活顺序,dampening 0.01;激活保持 BF16。`lm_head`、词嵌入、MTP 头与视觉塔不量化。校准数据:用本模型 RL 训练 rollout 重新整理的 512 条 × 4,096 token。量化元数据为 compressed-tensors(`pack-quantized`)格式;`recipe.yaml` 是 llm-compressor 配方。
- BPW 5.25:`model.safetensors`(17,646,891,544 字节,只含文本权重)× 8 ÷ 文本参数数 26,895,998,464;MTP 与视觉文件不计入。
- 看图 + MTP 检查(2026-10-09,单张 RTX PRO 6000,vLLM 0.28,3 个草稿 token):开关思考两种情况下看图问题都回答正确。
- 加载:只在 vLLM 0.28 上验证过。`VLLM_LOAD.json` 记录了加载设置。

### `INT4/W4A16/`(14 个文件,19,437,985,972 字节)

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `INT4/W4A16/VLLM_LOAD.json` | 510 | `7542f50d98101cd5d9406aaa70be1d52f76cbd235f8c48cee374655a053006a6` |
| `INT4/W4A16/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `INT4/W4A16/config.json` | 5,138 | `31e02ecfdf892d0db6bde3c1b97d8ce5a564e142a344fee4a9d3412e68524fbd` |
| `INT4/W4A16/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `INT4/W4A16/model.safetensors` | 17,646,891,544 | `e74d9161d57af066d7a8855526742561a187f81d67819ca10709a58c82b7eca7` |
| `INT4/W4A16/model.safetensors.index.json` | 189,311 | `5820a85fbea69c56cc34f33903c1a7c94af92736c779c2e9c934e538bac7dbd9` |
| `INT4/W4A16/model_mtp.safetensors` | 849,400,392 | `1d8268aa85ace093a561e3e7b63b9d390dac1cd55a90cd55b5ec509c3c9da9fe` |
| `INT4/W4A16/model_visual.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `INT4/W4A16/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `INT4/W4A16/recipe.yaml` | 359 | `3211d4cd0d4e5a3aca00b86b7db7ccf4890f07565c5474ba50eda1a1e3f68526` |
| `INT4/W4A16/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `INT4/W4A16/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `INT4/W4A16/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `INT4/W4A16/SHA256SUMS` | 1,153 | `744e89c9524117579510637c5b194f893cc9cd013b7fcd5029d2fe073a4b3dd2` |

## INT8 W8A8 说明

- 文本 + 图像(2026-10-09 起):架构为 `Qwen3_5ForConditionalGeneration`(文本 64 层,线性注意力与全注意力 3:1 交替)。视觉塔取自 BF16 档,以 BF16 单独存为 `model_visual.safetensors`(333 个张量,921,497,224 字节),并附 `preprocessor_config.json` / `video_preprocessor_config.json`;视觉塔不量化。8 个 INT8 权重文件未改动。包内不含 MTP 头(用 `MTP-BF16/`),也不含 DFlash2 草稿。2026-10-09 在一台 RTX PRO 6000 上实测(vLLM 0.28,关掉 Cutlass INT8 内核,`MTP-BF16/`、3 个草稿 token):看图问题回答正确,文本输出正常,接受长度 3.21,单请求 decode 86 tok/s。
- 量化:SmoothQuant + INT8 W8A8。权重按输出通道量化为 INT8,激活在推理时按 token 动态量化为 INT8;SmoothQuant 的预缩放已折进权重,推理框架不需要补丁。量化元数据为 compressed-tensors(`int-quantized`)格式。
- 层分布:MLP gate/up/down、全注意力 q/k/v/o、线性注意力 `in_proj_qkv` / `in_proj_z` / `out_proj` 共 400 个 Linear 为 INT8;线性注意力 `in_proj_a` / `in_proj_b` 与 `lm_head` 共 97 个保持 BF16;线性注意力的 `A_log`、`dt_bias`、`norm`、`conv1d` 等控制分支也保持 BF16。
- 校准与误差:512 条校准样本;留出集 NLL 由 BF16 的 0.50535 升到 0.52812,困惑度之比 1.023(在把预缩放折进权重之前测得)。
- 加载:只在 vLLM 0.28 上验证,不适用于 SGLang 与 NInfer;`VLLM_LOAD.json` 记录了本包的加载条件。RTX PRO 6000 Blackwell 上须关掉 Cutlass INT8 内核,见上文「启动命令」。
- MTP 草稿:`INT8/W8A8/MTP-BF16/` 只有 BF16 的 MTP 张量。2026-10-09 在一台 RTX PRO 6000 上用 vLLM 0.28 实测(关掉 Cutlass INT8 内核,`num_speculative_tokens=3`):平均接受长度 2.74–2.90。

### `INT8/W8A8/`(19 个文件,30,422,466,299 字节)

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `INT8/W8A8/VLLM_LOAD.json` | 329 | `b1101c2ef1d53e76f132686a15079068fc76ad2ae139514817e088c6223adf7b` |
| `INT8/W8A8/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `INT8/W8A8/config.json` | 25,592 | `478564df2dc7566492e2794b68c976491a8d6e98a604e2e307da4535ea3029eb` |
| `INT8/W8A8/generation_config.json` | 214 | `a4cef85934ea1fdcb207944dbc6eee70dbbf16806874428556ae33023336c0a4` |
| `INT8/W8A8/model-00001-of-00008.safetensors` | 3,978,325,744 | `f8f7ecb52576f50108d2a9335074e5621dd5a0c2b5ee92b830929c8acc34900a` |
| `INT8/W8A8/model-00002-of-00008.safetensors` | 3,990,728,496 | `73c182d4362ca9351329eb9c812aa44f627631d1d1866868a326010dc8387a45` |
| `INT8/W8A8/model-00003-of-00008.safetensors` | 3,927,632,952 | `59510687bfca9272147d8153b0d3cc55a2672a03c7326d7099d78a313cc4f102` |
| `INT8/W8A8/model-00004-of-00008.safetensors` | 3,995,896,560 | `fd9c32e4a11dec2dbf42dfb4e5da653bbbc01cd075ff60e593869022138e2efd` |
| `INT8/W8A8/model-00005-of-00008.safetensors` | 3,922,465,008 | `7478173acc5b54c80329756cf2bb81b5b804a0fa107217fbba5d0cb3353c3f77` |
| `INT8/W8A8/model-00006-of-00008.safetensors` | 3,984,366,360 | `cd53edb6084ec639667f2bdb997f7822db1eb758a15a06818fddcac603642127` |
| `INT8/W8A8/model-00007-of-00008.safetensors` | 3,138,579,112 | `997de745c52a87d54f684a461dd831f59d80e6b0c4c43e7ad75bd148cc87fdd5` |
| `INT8/W8A8/model-00008-of-00008.safetensors` | 2,542,796,896 | `6866cf8adcccc4cc6a00e74bc025f1a774fb52103b70f2674d0288272951a733` |
| `INT8/W8A8/model.safetensors.index.json` | 150,000 | `1eb8ea02681331fd897e247681411f1fad4e7cf421e6e133cdec7459e22f1ca7` |
| `INT8/W8A8/model_visual.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `INT8/W8A8/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `INT8/W8A8/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `INT8/W8A8/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `INT8/W8A8/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `INT8/W8A8/SHA256SUMS` | 1,705 | `f88bd3ed9476945cdb814e91fea5f18d2dc2b58c64cb187b5d23bfa364d28ebc` |

### `INT8/W8A8/MTP-BF16/`(3 个文件,849,403,270 字节)

`INT8/W8A8/MTP-BF16/SHA256SUMS` 覆盖下表前 2 个文件,其自身 SHA256 为 `313b058349deba83f05adb44b79f2f76ae668337834086f8dbcfacba131bf403`。

| 文件 | 字节数 | SHA256 |
|---|---:|---|
| `INT8/W8A8/MTP-BF16/config.json` | 2,681 | `7204cab1eb08579205ea9d8bbb556c396210d68693797df4333660b7bed6a41f` |
| `INT8/W8A8/MTP-BF16/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `INT8/W8A8/MTP-BF16/SHA256SUMS` | 165 | `313b058349deba83f05adb44b79f2f76ae668337834086f8dbcfacba131bf403` |

### `INT8/W8A16/`(主包 + MTP-BF16 草稿)

`INT8/W8A16/SHA256SUMS` 覆盖下表根目录文件;MTP 文件的哈希见 `INT8/W8A16/MTP-BF16/SHA256SUMS`。

| 路径 | 字节 | SHA256 |
|---|---:|---|
| `INT8/W8A16/VLLM_LOAD.json` | 619 | `45ad2233d5117157ae36998ccad835fecf26c6f312ac2d76b4ce18dc5dfd333c` |
| `INT8/W8A16/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `INT8/W8A16/config.json` | 5,141 | `4a4b2681cf80f9d73d83731f9bb2f94c031ffe7ad8260a5117ca351160a01b8e` |
| `INT8/W8A16/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `INT8/W8A16/model-00001-of-00002.safetensors` | 19,970,729,024 | `56df395c6e33c29e937f976ba6f1eab27301993d8a045343d1b678aedbd1f1b3` |
| `INT8/W8A16/model-00002-of-00002.safetensors` | 9,478,770,576 | `004c9641a2f2bc9d6906afeb5e73491d3679bedcb0e0e5f8747466f8066e5381` |
| `INT8/W8A16/model.safetensors.index.json` | 215,980 | `a1891443d49799ef92c47e4a00e2300b30e594eea7bd1bd608bd6023f4c40eea` |
| `INT8/W8A16/model_visual.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `INT8/W8A16/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `INT8/W8A16/recipe.yaml` | 969 | `34751e1269751f9e7d3b60e570bc8dacccbdeaab464ea36d06fee0ff8ba0637c` |
| `INT8/W8A16/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `INT8/W8A16/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `INT8/W8A16/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `INT8/W8A16/MTP-BF16/config.json` | 2,681 | `7204cab1eb08579205ea9d8bbb556c396210d68693797df4333660b7bed6a41f` |
| `INT8/W8A16/MTP-BF16/mtp-bf16.safetensors` | 849,400,392 | `1d8268aa85ace093a561e3e7b63b9d390dac1cd55a90cd55b5ec509c3c9da9fe` |
| `INT8/W8A16/SHA256SUMS` | 1,179 | `cfac30661e10381caf020d719661342f879f44c057f93cefcca3e14a6f12e09c` |
| `INT8/W8A16/MTP-BF16/SHA256SUMS` | 165 | `913083df00735f5895bbc7411d0884f3ddad8d35f6a742186bfa9df14c88c790` |

## GGUF Q2 LynnStyle 说明

- 混合精度 LynnStyle,最低精度到 Q2;内置 **Q4 MTP**(不是 Q8)。成绩在内置 MTP 前测得(外挂 Q8 MTP 草稿),量化权重相同:GPQA 177/198、MMLU 433/500、LCB 90/100。思考 P50/P70/P90:GPQA 2,989.5 / 8,923.8 / 27,156.1;MMLU 181 / 326.3 / 1,020.5;LCB 5,656.5 / 17,835.8 / 40,067.3。
- 体积:GGUF 13,276,009,792 字节(BPW 3.89),NInfer 13,568,617,472 字节,含视觉(文本 + MTP BPW 3.89);分母 27,320,697,856。
- 速度:llama.cpp 内置 Q4 MTP 长测 C4 174.8 tok/s(生成上限 4096);NInfer 短测 C8 521.0 tok/s(生成上限 512)。口径不同。
- GGUF 与 NInfer 分开启动(MTP 内置),命令见上文「启动命令」。MTP 与 DFlash2 互斥,本仓库不提供 GGUF 用的 DFlash2 草稿。

## GGUF Q3 LynnStyle 说明

- 混合精度 LynnStyle;内置 **Q4 MTP**(不是 Q8)。成绩在内置 MTP 前测得(外挂 Q8 MTP 草稿),量化权重相同:GPQA **173/198**、MMLU **449/500**、LCB **92/100**。思考 P50/P70/P90:GPQA 3,125.5 / 7,265.2 / 24,343.1;MMLU 148 / 279.3 / 923.4;LCB 4,421 / 14,232.2 / 34,946。
- 体积:GGUF 17,303,770,432 字节(BPW **5.07**),NInfer 17,596,369,920 字节,含视觉(文本 + MTP BPW **5.07**);分母 27,320,697,856。
- 速度:llama.cpp 融合 MTP 长测 C4 **191.8** tok/s(生成上限 4096);NInfer 短测 C8 **512.3** tok/s(生成上限 512)。口径不同。
- GGUF 与 NInfer 启动命令分开写(MTP 已内置)。MTP 与 DFlash2 互斥,本仓库不提供 GGUF 用的 DFlash2 草稿。完整启动命令见 GGUF-NInfer 仓库卡片。

## GGUF Q4 LynnStyle 说明

- 混合精度 LynnStyle;内置 **Q4 MTP**(不是 Q8)。成绩在内置 MTP 前测得(外挂 Q8 MTP 草稿),量化权重相同:GPQA **175/198**、MMLU **448/500**、LCB **89/100**。思考 P50/P70/P90:GPQA 2,951.0 / 8,159.3 / 25,649.0;MMLU 164 / 312.9 / 1,077.7;LCB 3,669.5 / 14,810.5 / 38,182.1。
- 体积:GGUF 19,620,406,592 字节(BPW **5.75**),NInfer 19,913,006,080 字节,含视觉(文本 + MTP BPW **5.74**);分母 27,320,697,856。
- 速度:llama.cpp 融合 MTP 长测 C4 **81.1** tok/s(生成上限 4096);NInfer 短测 C8 **436.4** tok/s(生成上限 512)。口径不同。
- GGUF 与 NInfer 分开启动(MTP 内置)。MTP 与 DFlash2 互斥,本仓库不提供 GGUF 用的 DFlash2 草稿。完整启动命令见 GGUF-NInfer 仓库卡片。

## GGUF Q8_0 说明

- 两个包主干量化相同(Q8_0),都内置 MTP 头,不需要外挂草稿模型;推荐 NInfer + C8 + MTP(486.3 tok/s)。
- `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf`:llama.cpp 直接加载。
- `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer`:只能用 NInfer-all 加载;启动请用 `--max-context 102400 --kv-capacity 819200 --max-concurrency 8`。
- 成绩在 llama.cpp 上用 GGUF 包测得;思考 token 三项均已拆分。

## GGUF Q6_K 说明

- 两个包主干量化相同(Q6_K + imatrix + 结构保护,见上文「量化方案」),都内置 MTP 头(GGUF `blk.64` 为 Q8_0;NInfer 的 MTP attention/MLP 权重为 Q6_K,输入投影为 Q8_0),不需要外挂草稿模型;推荐 NInfer + C4 + MTP。
- `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`:llama.cpp 直接加载,GGUF 架构为 `qwen35`,65 个块,最后一块(`blk.64`)为 MTP。
- `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer`:只能用 NInfer-all 加载;SGLang、vLLM、llama.cpp、transformers 都不能读。
- 视觉:llama.cpp 用 `--mmproj GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`(629,247,008 字节),每个 `.ninfer` 包内已含视觉部分(NInfer 下加 `--vision`);`GGUF-NInfer/` 里的 `vision-bf16.safetensors`(921,497,224 字节)是这部分的 BF16 原始权重,运行时不需要。
- 成绩在 llama.cpp 上用 GGUF 包测得;LCB 测评脚本与 NInfer 接口不兼容(收到的回复不是合法 JSON),属于测评脚本问题,不是模型质量问题,LCB 以 llama.cpp 为准。

### `GGUF/`(11 个文件:Q3+Q4+Q2+Q8+Q6 + Q3/Q4/Q2 Q8MTP + Q8 MTP 草稿 + mmproj + SHA256SUMS)

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.gguf` | 17,303,770,432 | `9985b3d41fc7dc0bb5d493f7523d4515504912a3a7fc830f66e0fd2f90f9fd95` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.gguf` | 19,620,406,592 | `56c7c605a59764d9f0bb645d4eb335f1574af2c9e74020386139597df0e872f5` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf` | 13,276,009,792 | `cad973b3b7cc0d86bd39968209268318a746673c12c9536e5c37408baa7b5e6e` |
| `GGUF/Qwen3.8-27B-Coder390-Q3LynnStyle16G-MTP.gguf` | 13,276,009,920 | `3872d17684a1b71d38fd36eb5ace047ac61bab11799926455de933fe0b3e60e1` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-Q3LynnStyle16G-MTP.ninfer` | 13,765,136,896 | `d9459f94883dde338cbd6ac07059bc92b4842fdba904a30a8cc00969f7dfb423` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-Q8MTP.gguf` | 13,488,346,432 | `62fd6cf6079dfb02b3e3aab68e39b4cdc6a471a51a82b56c9a76068e961d8a4a` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-Q8MTP.gguf` | 17,516,107,072 | `2c74a65df9d229bfba2eb3a878a25b84d4035d1be4061c9a665af213d98cae58` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-Q8MTP.gguf` | 19,832,743,232 | `5e2a1784298f696cb38f063962da0ad4acd1fd020c6e7c6e520df54acf8f57eb` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf` | 29,069,202,688 | `b24e8c5fe3f2b282cce841400c740fcaca48afcdcf9e991f7bbe9a59a78cabfe` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf` | 23,177,516,384 | `302597c53d1b00f7230b53a8a050831390a4371e92a80c1ac644fa920af76ab1` |
| `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` | 629,247,008 | `cae9799dc9196449b0d83f716e64af89d5cf65147510462e5a629a2aa23adb32` |
| `GGUF/mtp-Qwen3.8-27B-Coder390-EfficientThink-Q8_0.gguf` | 3,164,006,656 | `50a030e852289eed86065e2e2de57d89241174e99faa2c1c2f06c29c270789ee` |
| `GGUF/SHA256SUMS` | 1,187 | `7677cef32b796c8c54d18592e8d198a14563a994496c8161b84ab7bdba30d183` |

### `GGUF-NInfer/`(10 个文件:Q3+Q4+Q2 -Q4MTP(Q4_K MTP 头) + Q8+Q6 + Q3/Q4/Q2 Q8MTP(Q8_0 MTP 头)包,均含视觉 + vision-bf16(BF16 原始文件,运行时不需要) + SHA256SUMS)

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
| `GGUF-NInfer/SHA256SUMS` | 1,088 | `786409f76d95820fd18251d55d35ca8c36526412c0d8581645fdd24a73955d4a` |

### imatrix(发布在 GGUF-NInfer 仓库)

GGUF-NInfer 仓库的 `imatrix/` 目录([Hugging Face](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-GGUF-NInfer/tree/main/imatrix)、[ModelScope](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-GGUF-NInfer/files))里有 GGUF 重要性矩阵的校正文本 `coder390-imatrix-calibration.txt`(1,368 条 = 171 道题 × 8,用本模型 RL 训练 rollout 的输入重新整理,500,816 token,不含测评题),以及 2026-10-09 用它重新算出的 `coder390-imatrix.gguf`(本模型 BF16 GGUF,`-c 512 --chunks 512`,496 个条目、512 个块,SHA256 `be0924f24bd82c05b28da0c1d803ef29c1961f60bf9e978a16ffe746ee2adcf1`)。校正集功能上与发布 GGUF 时用的等价,但不是同一个文件;原 imatrix 数据文件没有保留。

## 已知局限

- GPQA 的空答在三种精度下都出在同两道分子生物题上,是题目上的老问题,与量化无关。
- 长尾仍未消除:思考 ≥48K 的题正确率明显偏低(如静态 FP8 的 LCB ≥48K 为 2/8),LCB 仍有 3 道写满 94K。
- MMLU 在三种精度间有 445–450 的采样抖动;成绩依赖上述口径(100K 上下文、94,208 生成上限、不计超时),不宜与其他口径直接比较。
- SGLang 格式各档的性能在单张 RTX PRO 6000 Blackwell + SGLang 上测得:BF16 / 静态 FP8 用的是静态 FP8 包,NVFP4 三档各用自己的包;这些档中 vLLM 只做了 FP8 包的加载与图像冒烟(FP8 包在 vLLM 0.28 上开 MTP 暂不可用,推荐 SGLang),NVFP4 未在 vLLM 上测试;DFlash2 只在 SGLang 上验证。INT8 W8A8 与 INT4 W4A16 在 vLLM 0.28 上测评与测速,NInfer 包在 NInfer 上测,GGUF 在 llama.cpp 与 NInfer-all 上测。
- NVFP4 三档的 GPQA(170、167、172)低于 BF16 / FP8 的 178,MMLU(439、440、442)略低于 445–450,LCB(91、92、88)在 90 上下;校准数据来自本模型自己的 RLOO 训练数据,不含官方测评题。NVFP4 只在 SGLang 上做过免补丁加载、贪心对拍和图像请求冒烟,MTP 与 DFlash2 以完整的性能测评为准。
- BF16 包的成绩来自同一份分片的全量测评,包本身的 GPU 冒烟(2026-10-09,单张 RTX PRO 6000,SGLang 0.5.21 + 内置 MTP 头,3 步 / 4 个草稿 token):开关思考两种情况下看图问题都回答正确,平均接受长度 3.43,单请求约 81 tok/s。
- INT8 W8A8 只能用 vLLM(分数在文本上测得;2026-10-09 加入了图像输入);GPQA 175 略低于原版 Qwen3.8 27B(FP8)的 177;速度为快测(每档请求数等于并发数,生成上限 512),不能与其他档直接比较;GPQA / MMLU 思考长度按原文用 BF16 tokenizer 重新计数,LCB 没有保存思考原文,没有思考长度分位数。
- GGUF Q8_0:GPQA 171 低于原版 Qwen3.8 27B(FP8)的 177;LCB 截断 3、空答 3;全量三联只在 GGUF(llama.cpp)上跑;NInfer 速度为同口径测速,llama.cpp 为快测协议。
- GGUF Q6_K:GPQA 174 低于原版 Qwen3.8 27B(FP8)的 177;MMLU 思考长度按原文用 BF16 tokenizer 计数,LCB 没有保存思考原文,没有思考长度分位数;全量三联只在 GGUF(llama.cpp)上跑,NInfer 包未单独跑全量;速度为快测(每档请求数等于并发数,生成上限 512),不能与其他档直接比较;视觉用 `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`(llama.cpp `--mmproj`),NInfer 包已含视觉部分(`--vision`);看图已实测:llama.cpp + mmproj 在 Q3 / Q4 LynnStyle、Q6_K、Q8_0 上,NInfer `--vision` 在 Q2 / Q3 / Q4 LynnStyle、Q6_K、Q8_0 上。

## 许可证与致谢

本模型采用 Apache-2.0 许可证,遵循基座 Qwen3.8-27B 的许可。

感谢 Qwen 团队提供基座模型与官方 FP8 方案;感谢 Opus5.5、GPT6Astra、Grok4.7、DSV4Pro、K3 在出题、金标、教师轨迹、数据核对与 RLOO 价值评审中的工作;感谢 SGLang、vLLM 与 DFlash 社区。
<!-- CARD_ZH_END -->
