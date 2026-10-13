---
license: mit
base_model: zai-org/GLM-5.3-Flash
base_model_relation: quantized
pipeline_tag: text-generation
quantized_by: peasantsmith
tags:
  - gguf
  - imatrix
  - mixture-of-experts
  - glm
  - project-maya
  - vision
---

# GLM-5.3-Flash · Maya-S, Maya-S24, Maya-M and Maya-L

**Maya-L: 99.2% of the full FP8 model's accuracy** on zero-shot tasks (ARC, HellaSwag, WinoGrande, PIQA), in 156 GB.
**Maya-S: 97.9%** in a 96 GB file. **Maya-S24: 97.7%, and up to 14% faster decode on 24 GB cards**, in 94.7 GB.
**Maya-M: 97.9%, and closer to the full model token by token**, in 116 GB.

GGUF quantizations of [zai-org/GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash) (321 B parameters, a
mixture of experts with about 18 B active per token), made for **Project Maya**. Project Maya keeps the most-used
experts on the GPU, the next in RAM and the rest on the SSD, so all four run well below the model's size (two GPUs with
30 GB of RAM in the measurements below). More memory is faster, and every machine is different: try it on yours.
All four are made from Z.ai's own FP8 release - the precision the model is served at - not from a re-quantized file.

- **Maya-S** (96.5 GB) is the compact one, made for PCs with a smaller memory pool across RAM and VRAM: its routed
  experts - most of the model - in about 2 bits (IQ2_XXS / IQ2_S), its attention and shared experts in 6-bit (Q6_K).
- **Maya-S24** (94.7 GB) is Maya-S for 24 GB cards (RTX 3090 / 4090): the same 2-bit routed experts, with only the
  small part every token runs through - the attention and shared experts - in 4-bit (Q4_K) instead of Maya-S's
  6-bit. That leaves about 1.5 GB more room for experts on the GPU.
- **Maya-M** (116 GB) is closer to the full model, for PCs with a bigger memory pool: built with the same
  FP8-statistics recipe and more bits where they count (2- to 3-bit experts), calibrated toward tool calls and
  front-end code.
- **Maya-L** (156.3 GB) is the closest, for PCs with the biggest memory pool: Maya-M's recipe one step up (3- to 4-bit
  experts: IQ3_S / IQ4_XS, Q5_K in the most sensitive layers).

> **Built partly on the IST Austria DAS Lab ([ISTA-DASLab](https://huggingface.co/ISTA-DASLab)) recipe.** All four use their
> GPTQ-style error-feedback rounding for the experts (each expert rounded against its own input statistics from the
> FP8 model), and are measured the way they measure their quants: task accuracy against the full-precision model.

## Files

| Folder | Files | Size |
| --- | --- | ---: |
| `Maya-S-v2-IQ2_XXS/` | `GLM-5.3-Flash-Maya-S-v2-IQ2_XXS-00001-of-00003.gguf`, `-00002-of-00003.gguf`, `-00003-of-00003.gguf` | 96.5 GB |
| `Maya-S24/` | `GLM-5.3-Flash-Maya-S24-IQ2_XXS_S-00001-of-00003.gguf`, `-00002-of-00003.gguf`, `-00003-of-00003.gguf` | 94.7 GB |
| `Maya-M/` | `GLM-5.3-Flash-Maya-M-IQ2_S-00001-of-00003.gguf`, `-00002-of-00003.gguf`, `-00003-of-00003.gguf` | 116.0 GB |
| `Maya-L/` | `GLM-5.3-Flash-Maya-L-IQ3_S-00001-of-00004.gguf`, `-00002-`, `-00003-`, `-00004-of-00004.gguf` | 156.3 GB |
| `vision/` | `mmproj-GLM-5.3-Flash-F16.gguf` (the vision tower and projector, F16, from the official weights), `GLM-5.3-Flash-vocab.gguf` (the tokenizer, for the encoder) | 1.14 GB |

The model's NextN (MTP) layer is included in all four, so engines that draft with it get speculative decoding.

## What is in them

| Tensors | Maya-S | Maya-S24 | Maya-M | Maya-L |
| --- | --- | --- | --- | --- |
| Routed experts, gate and up (42 layers) | IQ2_XXS, rounded with error feedback | as Maya-S | IQ2_S, rounded with error feedback | IQ3_S, rounded with error feedback |
| Routed experts, down | IQ3_XXS in the first and last four MoE layers, IQ2_S in the rest | as Maya-S | IQ3_S in the first and last four MoE layers, IQ3_XXS in the rest | Q5_K in the first and last four MoE layers, IQ4_XS in the rest |
| Attention projections (KDA, MLA/DSA) and shared experts | Q6_K | **Q4_K** | Q6_K | Q6_K |
| The three dense layers, embeddings, output, MLA k_b / v_b | Q6_K | Q6_K | Q6_K | Q6_K |
| Small KDA projections, the DSA indexer | Q8_0 | Q8_0 | Q8_0 | Q8_0 |
| Router, norms, stream-mixing weights | F32 | F32 | F32 | F32 |
| NextN draft layer experts | Q2_K (gate/up), Q3_K (down) | as Maya-S | Q3_K (gate/up), Q4_K (down) | Q4_K (gate/up), Q5_K (down) |

## How they were made

1. **Calibration text**: 128 sequences of 2,048 tokens in GLM's own chat template, reasoning blocks included - chat,
   multilingual chat, reasoning traces, web code (single-file HTML/CSS/JS pages, three.js scenes, canvas and WebGL
   animations), other code and tool calls; Maya-M's and Maya-L's weighted further toward tool calls and front-end code.
2. **Statistics from the FP8 model itself**, layer by layer: an importance matrix for every expert separately, not one
   per layer.
3. **Error-feedback rounding** of the experts' gate and up projections (GPTQ-style, at the quantizer's 256-weight
   blocks, each expert with its own input statistics): on held-out text it lowers the experts' output error by about a
   quarter against plain importance-weighted rounding at the same size.
4. llama.cpp's own quantizers (ggml), so the files are ordinary GGUFs.

## Against the original (FP8)

**Maya-L keeps 99.2% of the full model's zero-shot accuracy; Maya-S and Maya-M 97.9%, Maya-S24 97.7%.** Multiple-choice tasks at 400 questions each do not
separate them (a point or two either way is within the test's noise); token by token, below, Maya-M is clearly
closer to the FP8 model.

| Task (zero-shot) | FP8 | Maya-S | Maya-S24 | Maya-M | Maya-L |
| --- | ---: | ---: | ---: | ---: | ---: |
| ARC-Easy (acc) | 87.2 | 86.2 (98.9%) | 85.8 (98.3%) | 86.5 (99.1%) | 86.0 (98.6%) |
| ARC-Challenge (acc norm) | 71.0 | 68.2 (96.1%) | 69.0 (97.2%) | 69.0 (97.2%) | 69.8 (98.2%) |
| HellaSwag (acc norm) | 88.5 | 87.5 (98.9%) | 84.8 (95.8%) | 86.8 (98.0%) | 88.5 (100%) |
| WinoGrande (acc) | 78.5 | 75.5 (96.2%) | 77.0 (98.1%) | 76.2 (97.1%) | 77.8 (99.0%) |
| PIQA (acc norm) | 87.0 | 86.2 (99.1%) | 86.2 (99.1%) | 85.0 (97.7%) | 87.0 (100%) |
| **Average** | **82.5** | **80.8 (97.9%)** | **80.6 (97.7%)** | **80.7 (97.9%)** | **81.8 (99.2%)** |

400 questions per task, the same questions for every model, scored the way lm-evaluation-harness scores them (the answer with the highest log-likelihood; length-normalized where the choices differ in length) - the FP8 model run layer by layer in PyTorch, the quants through Project Maya's engine (`tools/maya_quant/zs_*.py`).

Token by token, on held-out text never used for calibration (7,672 positions), with the FP8 model's own predictions as the reference:

| | FP8 | Maya-S | Maya-S24 | Maya-M | Maya-L |
| --- | ---: | ---: | ---: | ---: | ---: |
| Same top token as FP8 | 100% | 83.3% | 83.1% | 86.2% | 90.0% |
| KL divergence from FP8 | 0 | 0.428 | 0.444¹ | 0.329 | 0.188² |
| Top-1 accuracy on the actual next token | 71.5% | 68.8% | 67.9% | 70.3% | 71.2% |

¹ Measured with a later engine, next to Maya-S at 0.421 in the same run. ² Measured with a later engine, next to Maya-M at 0.291 (same top token 86.8%) in the same run.

Closest on chat and reasoning text, furthest on tool-call formats and on text the FP8 model has memorized.

No loops in long generation (Maya-S): 14 answers of 6,000-14,000 tokens (three.js scenes, canvas animations,
explanations, a plan in Portuguese, a proof; temperature 1.0 and greedy) without a repeated passage. The context fill
test (a fact at the start of an 8k, 16k and 30k-token context, asked about at the end) finds it every time.

## Speed

Maya-S on two Tesla V100 32 GB (30 GB RAM) with Project Maya: decode (writing the answer) **up to 40 tokens/s**, with
the MTP block drafting, and it keeps that pace at long context (60K tokens); prefill (reading the prompt) **up to 560
tokens/s** (up to 670 with Project Maya v1.0.15).
On one Tesla V100 32 GB with 64 GB of RAM: decode **up to 19 tokens/s**, prefill **up to 370 tokens/s**.
Maya-S24 on the same card limited to 24 GB: decode 13.5 tokens/s against Maya-S's 11.8 (+14%); on the full 32 GB
19.1 against 17.2 (+11%); prefill the same.
`./maya.sh --bench` measures your machine the same way.

## Running it

**[Project Maya](https://github.com/mw00/project-maya)** sets everything up and runs it:

```sh
git clone https://github.com/mw00/project-maya.git && cd project-maya
./setup.sh          # Windows (experimental): START-MAYA.bat
```

- It checks the PC, downloads the model you pick and verifies every file's sha256, compiles the engine for your
  GPU(s), and starts it. Press Enter at each question for the recommended choice: Maya-S, or Maya-S24 when every card
  has 24 GB or less. `./setup.sh --setup --model Maya-S24` or `--model Maya-M` or `--model Maya-L` sets up the others.
- **GPUs:** NVIDIA, V100 / RTX 20 or newer, one GPU or up to 16 that share the model. AMD (experimental, Linux,
  ROCm 7): RX 7900 XT / XTX and Radeon AI PRO R9700 / RX 9070 (one or two), Strix Halo (one).
- **Memory:** the most-used experts stay in VRAM, the next in RAM and the rest are read from the SSD, so it runs with
  32 GB of RAM; more VRAM and RAM is faster. Put the model on an NVMe SSD.
- **Use it:** the dashboard at `http://127.0.0.1:8080` (chat, pictures through the vision files above, a live monitor),
  or the OpenAI- and Anthropic-compatible API at the same address (streaming and tool calls; Claude Code:
  `ANTHROPIC_BASE_URL=http://127.0.0.1:8080`).
- `./maya.sh --bench` measures your machine; `--bench` and `--report` in a GitHub issue add it to the users' speeds.

## License

The model is Z.ai's GLM-5.3-Flash under the MIT license; these quantizations are released under the same license.
