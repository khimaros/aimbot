---
license: mit
base_model: deepseek-ai/DeepSeek-V4.1-Flash-1017
base_model_relation: quantized
pipeline_tag: text-generation
library_name: gguf
tags:
  - gguf
  - llama.cpp
  - deepseek
  - deepseek-v4.1
  - mixture-of-experts
  - engram
  - imatrix
  - rtx-pro-6000
  - blackwell
  - cpu-offload
  - tool-use
  - reasoning
quantized_by: prometheusAIR
---

# DeepSeek-V4.1-Flash-1017 GGUF: imatrix quants for one big workstation

Three imatrix-guided quants of [DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017),
built and validated on one machine: an RTX PRO 6000 96 GB, a 16 GB second card, and 128 GB of RAM. The routed
experts are split across GPU and RAM, and the ~195 GiB engram tables are memory-mapped and read from disk on demand,
so they cost disk space, not RAM.

All three quants were measured against the release-precision experts, not against another quant, and all three
answer all 16 retrieval and multi-hop questions exactly at depths up to 255K tokens.

> **These files need a DeepSeek-V4.1 build of llama.cpp.** Upstream llama.cpp cannot load DeepSeek-V4.1 yet
> ([#28696](https://github.com/ggml-org/llama.cpp/pull/28696) is open). See [Runtime](#runtime).

## Which one do I want?

| | **IQ3_XXS** (recommended) | **IQ2_XS** | **IQ2_XXS** |
|---|---|---|---|
| Weights you must hold in VRAM + RAM | 193.9 GiB | 171.7 GiB | 152.0 GiB |
| Engram tables (mmapped from disk) | 194.6 GiB | 194.6 GiB (identical files) | 194.6 GiB (identical files) |
| Total download | 388.4 GiB | 366.3 GiB | 346.5 GiB |
| Mean KL divergence vs release experts | **0.141** | 0.183 | 0.229 |
| Median KL divergence | **0.023** | 0.033 | 0.046 |
| Same top-1 token | **88.5%** | 86.7% | 85.1% |
| Perplexity vs reference | +5.2% | +10.4% | +14.1% |
| Depth ladder (needle + multi-hop, to 255K) | **16/16** | **16/16** | **16/16** |
| Decode, reference box (see below) | 18.1-20.6 tok/s (16 at 255K) | 20.4-22.9 tok/s (17 at 255K) | 22.1-25.9 tok/s (19 at 255K) |
| Prefill, 32K-255K prompt | 475-527 tok/s | 529-592 tok/s | 636-727 tok/s |

- **IQ3_XXS:** pick this if your VRAM + RAM can hold ~194 GiB of weights plus context.
- **IQ2_XS:** pick this when you're ~20 GiB short. It costs 30% more KL divergence and ~1.8 points of top-1
  agreement. On the same box it decodes ~10% faster and prefills ~15% faster, because fewer expert bytes sit in RAM.
- **IQ2_XXS:** pick this when you're ~40 GiB short of IQ3_XXS, or when speed matters more than fidelity. Against
  IQ3_XXS it costs 62% more KL divergence and 3.4 points of top-1 agreement; on the same box it decodes ~25% faster
  and prefills ~40% faster.

Shards `-00008-`, `-00009-` and `-00010-` (the two engram tables among them, 204.1 GiB together) are byte-identical
in all three quants, and `-00006-` is also shared by IQ3_XXS and IQ2_XS (see `SHA256SUMS`). If you want more than
one quant, download those once and copy or link them under the other quant's name.

## Recipes

| tensor group | IQ3_XXS | IQ2_XS | IQ2_XXS |
|---|---|---|---|
| Routed experts gate/up (80 tensors) | `IQ3_XXS` on 28 layers, `IQ2_XS` on 12 | `IQ2_XS` | `IQ2_XXS` |
| Routed experts down (40) | `IQ3_XXS` | `IQ3_XXS` | `Q2_K` |
| Shared expert, attention, indexer/engram projections | `Q8_0` (copied from the source, not re-quantized) | same | same |
| Router, mHC, compressor, norms, some indexer/engram parts | `F32` / `BF16`, as in the source | same | same |
| `token_embd`, `output` | `BF16` | `BF16` | `BF16` |
| Engram tables (2 x 384M rows x 256) | `Q8_0`, see [Engram precision](#engram-precision) | same | same |

The routed experts are about 95% of the non-engram bytes, so their bit width decides quality.

**Which 12 layers get `IQ2_XS` in the IQ3_XXS quant:** 1, 12, 13, 20, 21, 27, 30, 31, 32, 33, 34, 35. We
didn't pick them from imatrix energy, which on this family mostly tracks depth. Instead, a forward-pass probe
measured, per layer, the size of the MoE output (absolute, and relative to the residual stream) on three kinds of text (general,
reasoning traces, tool dialogues). The 12 layers that contribute least across all three were demoted. The three
probes agree almost exactly. Layer 15 contributes about as much as the residual itself in every probe, so it
stays at `IQ3_XXS` everywhere.

`general.file_type` reports `Q8_0` because that was the quantizer's base type. The experts are per-tensor
overrides, so trust the table above, not the Hub's type badge.

## Engram precision

DeepSeek ships the engram tables in block-scaled FP8 (E4M3 values with one E8M0 scale per 32, i.e. MXFP8).
GGUF has no FP8 storage type, so every GGUF of this model stores the engram in some other type. These files use
`Q8_0`, taken from the source conversion. Sampling 16,384 rows against the release shows **0.55% relative RMS
error**, a worst-row cosine of 0.99998, and no element bit-identical.

## Runtime

Use [smalinin/llama.cpp, branch `my_build`](https://github.com/smalinin/llama.cpp/tree/my_build). No patch is
needed. The fork implements V4.1's two-level candidate prefilter, which is what makes context past 16,384 tokens
faithful. It also carries upstream's fix for an out-of-bounds read in the CUDA routed-expert matmul
([#29953](https://github.com/ggml-org/llama.cpp/pull/29953)); without that fix, CUDA builds can hit an Xid 31 fault.
We haven't tested these files on other V4.1 runtimes (ik_llama.cpp, antirez's ds4).

```bash
git clone -b my_build https://github.com/smalinin/llama.cpp llama.cpp-dsv41
cd llama.cpp-dsv41 && git checkout 425badfe8   # the commit we tested
cmake -B build -DGGML_CUDA=ON && cmake --build build --config Release -j
```

**Which build the numbers come from.** The quality, depth-ladder and speed results on this card were measured on
smalinin's older `my_build_deepseek41` branch at `cfd8adcf6`, plus a
[patch](https://huggingface.co/prometheusAIR/DeepSeek-V4.1-Flash-1017-GGUF/blob/30cab4ae80cbbe42e522b3e6c0b560071331a78a/patches/dsv41s-runtime.patch)
(still in this repo's history) that added the same MMQ fix and two changes these files don't use. We then
re-tested IQ3_XXS on `my_build` at `425badfe8`, on the same box with the same settings:

- **Function:** the shakedown (chat, thinking, tool calls, a tool round trip) and all 16 depth-ladder questions to
  255K pass. GPU0 peaks at 92,552 MiB, about 100 MiB below the older build.
- **Output:** KL divergence between the two builds is 0.011 (same top-1 token 96.4%, 48 x 512 tokens of
  wikitext). That is what any rounding change does to this quant: on the older build alone, scoring 4 sequences
  per batch instead of 1 also gives 0.011, and so does switching the engram between `Q8_0` and BF16. Identical
  runs repeat exactly (KL 0).
- **Speed:** within run-to-run variation. Short-prompt decode averaged 19.7 tok/s on both builds over two rounds
  in alternating order. Over the 16 ladder questions, run back to back on the same day, decode averaged 17.2 tok/s
  on `my_build` and 17.8 on the older build (-3%; per rung, from 0 to -13%), and prefill of the long prompts
  averaged 498 vs 477 tok/s.

The IQ2_XS and IQ2_XXS files weren't re-run on `my_build`.

## Reference box and settings

RTX PRO 6000 Blackwell 96 GB (GPU0) + RTX 5070 Ti 16 GB (GPU1), Ryzen 9 9950X3D, 128 GB DDR5. The engram shards
live on an NVMe RAID.

```bash
CUDA_VISIBLE_DEVICES=0,1 llama-server \
  --model DeepSeek-V4.1-Flash-1017-IQ3_XXS-00001-of-00010.gguf \
  --device CUDA0,CUDA1 --tensor-split 1,0 -ngl 999 \
  -ot 'blk\.(20|21)\.ffn_(gate|up|down)_exps\.weight=CUDA1,blk\.24\.ffn_down_exps\.weight=CPU' \
  -ncmoe 24 \
  --ctx-size 262144 -fa on -b 2048 -ub 2048 -np 1 --threads 12 \
  --jinja --temp 1.0 --top-p 1.0 --min-p 0.0
```

| | GPU0 | GPU1 | RAM (CPU expert tier) | disk (engram) |
|---|---|---|---|---|
| Weights placed | 78.7 GiB | 8.1 GiB | 105.8 GiB | 194.6 GiB |
| Used after load, 256K ctx | 92,474 MiB | 10,154 MiB | | |
| Peak during the 255K rung | 92,654 MiB (4.6 GiB free) | | | |

**IQ2_XS on the same box:** use `-ncmoe 23` and drop the `blk\.24\.ffn_down_exps` override
(`-ot 'blk\.(20|21)\.ffn_(gate|up|down)_exps\.weight=CUDA1'`). That places 77.3 GiB on GPU0 and 85.1 GiB in RAM;
GPU0 holds 90,730 MiB after load and peaks at 90,940 MiB in the 255K rung.

**IQ2_XXS on the same box:** use `-ncmoe 18` and send block 18's down-projection experts to RAM as well
(`-ot 'blk\.(20|21)\.ffn_(gate|up|down)_exps\.weight=CUDA1,blk\.18\.ffn_down_exps\.weight=CPU'`). That places
78.1 GiB on GPU0, 7.1 GiB on GPU1 and 65.5 GiB in RAM; GPU0 holds 91,002 MiB after load and peaks at 91,180 MiB in
the 255K rung.

### Settings that matter

- **`-np 1`.** We validated with one slot and haven't tested more. How sequences are batched changes the output
  slightly: on IQ3_XXS, scoring 4 sequences per batch instead of 1 moves it by KL divergence 0.011, the same as
  any rounding change, but on the release-precision master the same change gives ~0.1. To reproduce our KL
  numbers or imatrix, run one sequence per batch (`-c` = `-b` = `-ub`).
- **Keep mmap on.** No `--load-mode none`, no `--mlock`. The engram is read lazily from the file; loading it would
  need another ~195 GiB of RAM.
- **`--tensor-split 1,0`** keeps every layer on GPU0 and moves only expert tensors to the second card. Splitting
  layers across cards disables the fused mHC ops.
- **`-ncmoe N` keeps the experts of the first N layers in RAM.** Raise it if GPU0 runs out of memory, lower it if RAM does. The compute buffer
  grows with context, so test at your full `--ctx-size`.
- **Thinking** is on by default. Turn it off per request with
  `"chat_template_kwargs": {"enable_thinking": false}`. Don't use `{"thinking": false}`, which renders a
  non-thinking prompt while the parser still expects a thinking block.
- **Sampling:** DeepSeek recommends `temperature 1.0`, `top_p 1.0`.
- **The first long request after a load is slow.** It pages the RAM expert tier back in from disk. After that,
  speeds are as below.

### Chat template

The embedded template is a V4.1 template that reproduces all five of DeepSeek's official encoder test cases
byte for byte, with one fix: top-level tools also render when the conversation starts with a user message.
DeepSeek's reference encoder attaches tools to the system message, so in a conversation that starts with a user
message they're silently dropped. No `--chat-template-file` is needed; the release files were tested with the
embedded template.

## Validation

Everything in this section was measured on the older `my_build_deepseek41` build; [Runtime](#runtime) has the
re-test on `my_build`.

**KL divergence.** Reference = the source GGUF, whose routed experts are bit-identical to the release's MXFP4.
Its trunk and engram are `Q8_0`. Text: wikitext-2 test, 40 chunks of 4,096 tokens, scoring the second half of
each (81,920 tokens), one sequence per batch.

**Depth ladder.** Facts planted at 10/50/90% depth in a synthetic log, and four questions per rung: a verbatim
needle, a single retrieval, a three-fact multi-hop sum, and a comparison. Thinking on, effort low. The IQ3_XXS
rows were measured before the shard-1 metadata rewrite (same tensor bytes); the release files repeated the 32K rung, 4/4.
The IQ2_XS and IQ2_XXS rows are the release files. Every rung scored 4/4 on all three quants.

| prompt tokens | IQ3_XXS prefill / decode | IQ2_XS prefill / decode | IQ2_XXS prefill / decode |
|---:|---:|---:|---:|
| 32,137 | 475 / 19.2-20.1 tok/s | 592 / 21.7-22.9 tok/s | 727 / 24.2-25.1 tok/s |
| 64,141 | 527 / 19.2-20.6 tok/s | 591 / 20.7-22.9 tok/s | 720 / 23.9-25.9 tok/s |
| 125,244 | 513 / 18.1-19.5 tok/s | 570 / 20.4-21.5 tok/s | 688 / 22.1-23.8 tok/s |
| 255,340 | 479 / 15.6-16.1 tok/s | 529 / 16.3-17.3 tok/s | 636 / 18.8-19.4 tok/s |

**Functional checks:** arithmetic, thinking open/close, tool calls with thinking on and off, and a tool-result
round trip all pass on all three quants, using the release files and their embedded template. Short-prompt decode
is 18.4-18.9 tok/s (IQ3_XXS), 21.4-22.4 tok/s (IQ2_XS) and 24.1-24.8 tok/s (IQ2_XXS).

## Calibration

The imatrix (`imatrix/DeepSeek-V4.1-Flash-1017-imatrix.gguf`) covers 950,272 tokens, computed as 116 single
sequences of 8,192 tokens. All 46,080 routed-expert slots received activations. The corpus is 2.96M characters:

- general/scientific prose, plus an agentic, code and tool-use set
- source code: DeepSeek's reference inference and encoding code, and the llama.cpp runtime
- the documents behind pfeifferj's GSQ-RCO calibration: fineweb-edu, LLM compression calibration chats and
  OpenThoughts reasoning traces, with the chat and reasoning sets rendered in the V4.1 chat format
- Chinese Wikipedia (65 articles)
- DeepSeek's five official encoder test cases, and 48 dialogues rendered with the V4.1 template

## Files

| quant | files |
|---|---|
| IQ3_XXS | `DeepSeek-V4.1-Flash-1017-IQ3_XXS-000{01..10}-of-00010.gguf` |
| IQ2_XS | `DeepSeek-V4.1-Flash-1017-IQ2_XS-000{01..10}-of-00010.gguf` |
| IQ2_XXS | `DeepSeek-V4.1-Flash-1017-IQ2_XXS-000{01..10}-of-00010.gguf` |
| imatrix | `imatrix/DeepSeek-V4.1-Flash-1017-imatrix.gguf` |
| checksums | `SHA256SUMS` (`sha256sum -c SHA256SUMS --ignore-missing`) |

Shards 8 and 9 each hold one engram table (97.3 GiB apiece). Point llama.cpp at shard 1; it finds the rest.
Downloading shards 8 and 9 with `huggingface_hub` / `hf download` needs Xet (`hf_xet`, the default); with
`HF_HUB_DISABLE_XET=1` set, the Hub refuses files this large.

## Attribution

- Model: [DeepSeek-AI](https://huggingface.co/deepseek-ai), MIT License.
- Source conversion: [mrfakename/DeepSeek-V4.1-Flash-1017-GGUF](https://huggingface.co/mrfakename/DeepSeek-V4.1-Flash-1017-GGUF)
  (`Q8_0` trunk/engram, release MXFP4 experts unchanged).
- Runtime: smalinin's `my_build` (first validated on his `my_build_deepseek41` with Nick Mermiges' MMQ padding
  fix). Upstream V4.1 support: vcruz305's [#28696](https://github.com/ggml-org/llama.cpp/pull/28696).
- Calibration document list: pfeifferj's GSQ-RCO manifest.
