---
license: other
license_name: upstage-solar-license
license_link: LICENSE
base_model: upstage/Solar-Open2-250B
base_model_relation: quantized
pipeline_tag: text-generation
language:
  - en
  - ko
  - ja
tags:
  - gguf
  - llama.cpp
  - solar
  - moe
  - quantized
  - imatrix
---

# Solar-Open2-250B-GGUF

GGUF quantizations of [**upstage/Solar-Open2-250B**](https://huggingface.co/upstage/Solar-Open2-250B) — Upstage's 250B-A15B hybrid linear-attention MoE — for local inference with llama.cpp. Built and tested on a workstation with 128 GB DDR5 system RAM and an RTX 6000 Pro 96 GB Blackwell GPU.

> ## ⚠️ These files do NOT run on mainline llama.cpp (yet)
>
> Solar Open 2 uses a new architecture (`solar_open2`) that is **not in upstream llama.cpp**. Loading these GGUFs with a stock build fails with `unknown model architecture: 'solar-open2'`.
>
> You must build the small patch included here (`solar_open2-llama.cpp.patch`, 951 lines across 11 files). See **[Building llama.cpp](#building-llamacpp)** below. If/when the architecture is merged upstream, this requirement goes away.
>
> Status as of **2026-08-05**: still not upstream — there is an open feature request ([ggml-org/llama.cpp#26115](https://github.com/ggml-org/llama.cpp/issues/26115)) and no PR. Note that mainline *does* support **Solar-Open-100B** (`SolarOpenForCausalLM`), which is a different model on a different attention stack; that support does nothing for Solar Open 2.

**Built with Solar.** 

This is an independent, third-party quantization. It is **not** affiliated with or endorsed by Upstage. All model weights are © Upstage under the [Upstage Solar License](LICENSE).

---

## What is Solar Open 2?

A 250B-parameter Mixture-of-Experts that activates ~15B parameters per token. Its stack interleaves **one softmax-attention (GQA) layer with three linear-attention (KDA) layers** in every block of four (S-L-L-L × 12 = 48 layers), with **no positional encoding** (NoPE). The linear layers carry sequence context in a fixed-size recurrent state, so the KV cache stays constant in length and only the 12 softmax layers cache anything — making very long context cheap. Trained on English, Korean, and Japanese, aimed at agentic / office / coding use. See the [technical report](https://huggingface.co/upstage/Solar-Open2-250B/blob/main/Solar_Open_2_Tech_Report.pdf) for details.

The architecture's linear-attention core is **KDA (Kimi Delta Attention)** with a negative-eigenvalue extension (β = 2σ(·) ∈ (0,2)), the same delta-net family already supported in llama.cpp for Kimi-Linear; this port reuses that kernel and adds the GQA-with-sigmoid-gate softmax path, NoPE, and the S-L-L-L layout.

---

## Available quantizations

| File | Bits | Size | PPL (wikitext-2)¹ | vs Q6_K |
|---|---|---|---|---|
| `Q6_K/` | 6.57 | 191 GiB | **4.123** | — |
| `IQ4_XS/` ⭐ | 4.35 | 127 GiB | **4.159** | +0.9 % |
| `Q2_K/` | 3.05 | 89 GiB | **4.774** | +15.8 % |
| `IQ1_M/` ⚠️ | 1.93 | 56 GiB | **7.717** | **+87.2 %** |

¹ Perplexity over a fixed 40-chunk slice of `wiki.test.raw` at `n_ctx=512`. Lower is better; all four were measured identically so the deltas are directly comparable. `Q6_K` is the near-lossless baseline the deltas are computed against.

> **On comparing perplexity across repos:** these numbers are only meaningful against an identical slice. Our own `Q2_K` measures **4.774 over 40 chunks** but **5.486 over 80 chunks** — same file, same settings, different chunk count. If you are comparing our numbers to another quantizer's, check that the chunk count matches first.

**Which to pick:**
- **`IQ4_XS` — recommended.** Near-Q6_K quality (+0.88 % PPL is within measurement noise) at two-thirds the size. This is the quality/size sweet spot.
- **`Q2_K` — speed / single-card.** Fits entirely on one 96 GB GPU and runs ~2.5× faster, but +15.8 % PPL is a real, perceptible quality drop (the sub-4-bit cliff on this fine-grained 320-expert MoE). Good for drafts, high-throughput, or demos; not a replacement for IQ4_XS as a daily driver.
- **`Q6_K` — near-lossless reference.** For evaluation or as an imatrix source.
- **`IQ1_M` — smaller-VRAM only. Read the warning below before choosing this version.**

### ⚠️ About `IQ1_M`

**Perplexity is 87 % worse than `Q6_K`** That is a severe, honest number and we are putting it up front rather than in a footnote. It was built by request, for people who cannot fit the 89 GiB `Q2_K`.

**`IQ1_M` gains are mostly for memory footprint, not speed.** Measured on one RTX PRO 6000 (96 GB), both fully GPU-resident: `IQ1_M` decodes at **95.5 tok/s using 58 GiB VRAM**, `Q2_K` at **94.9 tok/s using ~89 GiB**. Identical speed. **If you can fit `Q2_K`, use `Q2_K`** — `IQ1_M` is intended for 64 GB-class hardware (64 GB Apple Silicon, 2×32 GB, 80 GB A100).

That said, it degrades more gracefully than the perplexity implies. At temperature 0 it answered factual chains, arithmetic (47 × 23 = 1081, self-verified), a correct Rayleigh-scattering explanation, a correct recursive `fib`, and fluent Korean translation — and it scored **15/15 exact on needle-in-a-haystack** at 2K/4K/8K/16K/28K × 10 %/50 %/90 % depth. Our reading is that the 320-expert MoE has enough routing redundancy, and keeping attention and embeddings at Q6_K preserves enough of the retrieval machinery, that the damage shows up as degraded fluency and reliability rather than outright breakage. Expect more repetition, weaker long-form coherence, and more frequent factual slips than any other rung here.

All four protect what matters most: **attention and embeddings are kept at Q6_K** (only ~3 % of parameters, so the cost is negligible), and `blk.0`'s experts — which the calibration set activates least — are boosted (Q5_K in IQ4_XS, Q4_K in Q2_K, IQ2_XXS in IQ1_M) to avoid quantizing rarely-seen weights against a weak importance signal. Quantization used the included **importance matrix** (`Solar-Open2-250B.imatrix`), computed over an English + Korean + Japanese + code calibration mix so language- and domain-specialized experts are represented.

> **Blackwell / sm_120 note.** The `iq1_s`, `iq2_s`, and `iq3_s` CUDA matmul kernels produce wrong results on compute capability 12.0 (verified with `test-backend-ops` on both an RTX PRO 6000 and a 5070 Ti). That is an upstream llama.cpp issue, not specific to this model — but it means **any** low-bit quant built around those types (e.g. `IQ2_M`, which uses `iq2_s`) is unusable on 50-series and RTX PRO Blackwell cards. The types used here — `iq1_m`, `iq2_xxs`, `iq4_xs`, `iq4_nl`, and all K-quants — all pass.

---

## Building llama.cpp

The patch is generated against upstream master `6ea215d17` (2026-08-04), where it is verified to apply cleanly and compile with zero errors. A nearby master should work with minor fuzz.

> **Refreshed 2026-08-05.** If you are holding an older copy of this patch, replace it. The previous revision (2026-07-26, generated against `88b47a755`) no longer applies to current master: upstream added `LLM_ARCH_QWEN3TTS` immediately adjacent to one of our hunks in `src/llama-arch.cpp`, and `common/chat.cpp` and `gguf-py/gguf/constants.py` have drifted by hundreds of lines. The port's own code is unchanged — this is a rebase, not a fix, so **no re-download of the GGUFs is needed**.

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
git checkout 6ea215d17
git apply /path/to/solar_open2-llama.cpp.patch     # adds the solar_open2 arch + tool parser

cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=120   # 120 = Blackwell; set to your GPU
cmake --build build --target llama-server -j
```

The patch touches: `gguf-py` + `src/llama-arch.*` (arch registration), `conversion/solar_open2.py` + `conversion/__init__.py` wiring (HF→GGUF conversion), `src/models/solar-open2.cpp` (the graph), `common/chat.cpp` (tool-call + reasoning parser), and `src/llama-vocab.cpp` (registers `<|im:end|>` as an end-of-generation token).

> **Note:** if you built from an earlier version of this patch and saw `<|im:end|>` at the end of replies, rebuild with the current patch — the fix is here, and your existing GGUF downloads work as-is (no re-download needed).

---

## Running

Download **all** shards of a quant into one directory, then point `--model` at the **first** shard (`…-00001-of-000NN.gguf`); llama.cpp loads the rest automatically.

```bash
./build/bin/llama-server \
  --model IQ4_XS/Solar-Open2-250B-IQ4_XS-00001-of-00004.gguf \
  --host 0.0.0.0 --port 8080 \
  --device CUDA0 -ngl 999 -ncmoe 15 \
  --no-mmap \
  --ctx-size 32768 -fa on -b 512 -ub 512 -np 1 --threads 12 \
  --jinja
```

**Flags that are load-bearing, not decoration:**

- **`--no-mmap` is required for CPU-offloaded setups.** With mmap, the CPU-resident experts are demand-faulted from disk in 4 KB pages and throughput collapses (~1.9 tok/s in our tests); `--no-mmap` loads them into RAM up front (~18 tok/s at IQ4_XS with offload). Not needed if the whole model is on the GPU.
- **`-ub 512` (or `4096`), never `2048`.** This port has a bug at `-ub 2048` specifically: a full 2048-token micro-batch followed by a small tail triggers a CUDA illegal-memory-access on this architecture's shape. `-ub 512` and `-ub 4096` are both fine. (Reported below under *Known issues*.)
- **`-ncmoe N` and `--device CUDA0`.** `-ncmoe` keeps the experts of the first N layers on CPU. Use a single GPU device with it — llama.cpp assigns later (expert-heavy) layers to additional devices, which will OOM a smaller second GPU. Drop `-ncmoe` entirely if the model fits on one GPU (e.g. Q2_K on a 96 GB card).

**Rough hardware sizing** (per quant, for `-ncmoe` tuning): weights split between VRAM and system RAM. IQ4_XS ≈ 127 GiB total (e.g. ~92 GiB VRAM + ~35 GiB RAM at `-ncmoe 15`); Q2_K ≈ 89 GiB fits on a single 96 GB card with no offload; IQ1_M ≈ 56 GiB fits a 64 GB card or 64 GB of unified memory with no offload. The KV cache is tiny — only 12 of 48 layers cache, ~48 KiB/token — so long context costs little VRAM (256K ≈ 12 GiB, 1M ≈ 48 GiB f16).

**Budgeting VRAM at very long context.** The KV cache is not the only term that grows. At `-ub 4096` and a 1M context the CUDA compute buffer alone is **~12.9 GiB** (it scales with `-ub`, and is only ~2 GiB at 128K). A working budget from our own tuning, per GPU: `non-expert weights + (2.55 GiB × resident expert layers) + KV + compute buffer + ~2.7 GiB overhead`. Size the compute buffer before you size the offload, or you will OOM after the weights have already loaded.

### Measured performance

On a single RTX PRO 6000 Blackwell (96 GB) + Ryzen 9950X3D, DDR5:

| Quant | Offload | Decode | Prefill | Needle retrieval |
|---|---|---|---|---|
| IQ4_XS | `-ncmoe 15` | 37.6 tok/s | 31.8 tok/s | exact to 16K (tested) |
| Q2_K | all-GPU | 94.9 tok/s | 63.5 tok/s | exact to 4K (tested) |
| IQ1_M | all-GPU (58 GiB) | 95.5 tok/s | — | 15/15 exact to 28K |

---

## Reasoning

Solar Open 2 is a reasoning model, and **reasoning is ON by default** — the template's first line is `set reasoning_effort = reasoning_effort if reasoning_effort is defined else "high"`, so omitting the setting gives you full-depth thinking. To control it, pass `reasoning_effort` in `chat_template_kwargs`:

```json
{
  "model": "solar",
  "messages": [ ... ],
  "chat_template_kwargs": { "reasoning_effort": "high" }
}
```

Values that turn reasoning **on**: `medium`, `high`, `xhigh`. Any other value (e.g. `"none"`) turns it **off** — but *omitting the key entirely* falls back to the template's own default of `"high"`, i.e. **on**.

> **Agent/client note.** Because the default is on, clients that can't set `chat_template_kwargs` get full-depth reasoning on *every* call — including cheap auxiliary ones like session-title generation. Measured here: a title request reasoned for **3,743 tokens (~105 s)** to produce a four-word title, versus **5 tokens** with `reasoning_effort: "none"`. If your client has short timeouts on such helper calls, either raise them or bound thinking server-side with `--reasoning-budget N` (note that this caps main-task reasoning too).

## Tool calling

Supported via the standard OpenAI `tools` / `tool_calls` API. The included parser handles Solar's custom marker format (`<|tool_call:start|>name … <|tool_arg:start|>key<|tool_arg:value|>value<|tool_arg:end|> … <|tool_call:end|>`), including multiple/parallel calls and typed arguments. Start the server with `--jinja` (shown above) and send `tools` as usual.

---

## Provenance & reproducibility

- **Base weights:** `upstage/Solar-Open2-250B` (BF16), converted to a BF16 GGUF, then quantized.
- **Importance matrix:** computed from the Q6_K over an English (`calibration_datav3`) + Korean/Japanese Wikipedia + source-code mix, so that language- and domain-specialized experts are exercised. Included as `Solar-Open2-250B.imatrix` (GGUF format) if you want to make your own quants.
- **Per-tensor recipe** (both builds): experts at the headline type; `blk.0` experts boosted one K-quant rung (weakest calibration coverage); all `attn_*` and token/output embeddings at Q6_K.
- Every build was validated for coherence, needle-in-haystack retrieval at depth, and perplexity before release. `IQ4_XS`'s numeric correctness was additionally checked against an independent NumPy reference forward pass of the architecture.

## Known issues

- **`-ub 2048` crashes** (CUDA illegal memory access) on this architecture's shape when a full 2048-token micro-batch is followed by a small tail. Use `-ub 512` or `-ub 4096`. Under investigation; the weights/conversion are not implicated (a runtime flag fully avoids it).
- This is a **community port**, not upstream-reviewed. The architecture, quant recipe, reasoning behavior, and tool parser are validated empirically, but edge cases may remain. Issues/feedback welcome.

## Attribution & license

Model weights are © Upstage, released under the **Upstage Solar License** (see [`LICENSE`](LICENSE)). Per that license, this derivative is named with the **"Solar"** prefix, displays **"Built with Solar,"** and ships a copy of the license. The quantization tooling and the llama.cpp patch are provided under llama.cpp's MIT license.

If you use this, please cite the [Solar Open 2 technical report](https://huggingface.co/upstage/Solar-Open2-250B/blob/main/Solar_Open_2_Tech_Report.pdf) and link back to the [original model](https://huggingface.co/upstage/Solar-Open2-250B).
