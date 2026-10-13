---
base_model: trohrbaugh/Qwen3.8-Flash-Next-heretic-2
base_model_relation: quantized
license: other
license_name: qwen-community-1.0
license_link: https://huggingface.co/Qwen/Qwen3.8-Flash-Next/blob/main/LICENSE
library_name: llama.cpp
pipeline_tag: image-text-to-text
tags:
- gguf
- qwen4exp
- heretic
- uncensored
- abliterated
- mtp
- speculative-decoding
- llama.cpp
---

# Qwen3.8-Flash-Next-heretic-2 — GGUF (static quants)

<p align="center">
    🧬 Source model: <a href="https://huggingface.co/trohrbaugh/Qwen3.8-Flash-Next-heretic-2" target="_blank">trohrbaugh/Qwen3.8-Flash-Next-heretic-2</a> · base: <a href="https://huggingface.co/Qwen/Qwen3.8-Flash-Next" target="_blank">Qwen/Qwen3.8-Flash-Next</a>
    <br>
    📦 imatrix (i1) quants: <a href="https://huggingface.co/spiritfather/Qwen3.8-Flash-Next-heretic-2-i1-GGUF" target="_blank">spiritfather/Qwen3.8-Flash-Next-heretic-2-i1-GGUF</a> · MTP head: <a href="https://huggingface.co/spiritfather/Qwen3.8-Flash-Next-heretic-2-GGUF/tree/main/mtp" target="_blank">mtp/</a> · vision: <a href="https://huggingface.co/spiritfather/Qwen3.8-Flash-Next-heretic-2-GGUF/tree/main/mmproj" target="_blank">mmproj/</a>
    <br>
    🛠️ Runs on <a href="https://github.com/ggml-org/llama.cpp" target="_blank">llama.cpp</a> (master); MTP needs <a href="https://github.com/ggml-org/llama.cpp/pull/27836" target="_blank">PR #27836</a> · decensored with <a href="https://github.com/p-e-w/heretic" target="_blank">Heretic</a>
    <br>
    📊 Scored on <a href="https://caliperbench.com/m/qwen3.8-flash-next-heretic-2/" target="_blank">CaliperBench</a>
    <br>
    💬 <a href="https://discord.gg/rhE9zdKyE4" target="_blank">Discord</a>
</p>

> [!Note]
> All credit for the model goes to **[trohrbaugh](https://huggingface.co/trohrbaugh)**, who produced [Qwen3.8-Flash-Next-heretic-2](https://huggingface.co/trohrbaugh/Qwen3.8-Flash-Next-heretic-2) with a custom fork of [Heretic](https://github.com/p-e-w/heretic) (v1.3.0+custom, per-layer direction) — author-reported **0/100 refusals (base 99/100), KL divergence 0.0818**, the lowest-KL heretic of Qwen3.8-Flash-Next at time of writing. The base model is [Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) (177B total / ~3B active MoE, arch `qwen4exp`) by the Qwen team. This repository only re-packages those weights as GGUF.

> [!Tip]
> Benchmarked on **[CaliperBench](https://caliperbench.com)** — a creative-writing benchmark scoring prose craft, roleplay and willingness rather than general intelligence. See this model's scores: [caliperbench.com/m/qwen3.8-flash-next-heretic-2/](https://caliperbench.com/m/qwen3.8-flash-next-heretic-2/).

> [!Important]
> These files ship the model's own **MTP/NextN speculative-decoding head** (`mtp/`, plus a pre-grafted pair per quant) — the first Flash-Next quants to do so. The trunk files load on any current llama.cpp; the head needs [PR #27836](https://github.com/ggml-org/llama.cpp/pull/27836). See [MTP](#mtp-speculative-decoding-the-models-own-draft-head).

## Provided quants

| Quant | Size | On GPU (trunk) | Mixture (default / up / gate / down) | PLE | MTP pair | PPL (wikitext-2, ctx 512) | vs Q8_0 | KLD vs Q8_0 |
|:--|--:|--:|:--|:--|:--:|:--|:--|:--|
| [Q4_K_M](https://huggingface.co/spiritfather/Qwen3.8-Flash-Next-heretic-2-GGUF/tree/main/Q4_K_M) | 130.8 GiB (5 files) | 80.1 GiB | Q8_0 / Q4_K / Q4_K / Q8_0 | Q8_0 | ✓ | 3.635241 ± 0.045789 | +0.552% | 0.036144 ± 0.000587 |
| [Q5_K_M](https://huggingface.co/spiritfather/Qwen3.8-Flash-Next-heretic-2-GGUF/tree/main/Q5_K_M) | 141.3 GiB (6 files) | 90.6 GiB | Q8_0 / Q5_K / Q5_K / Q8_0 | Q8_0 | ✓ | 3.642467 ± 0.045911 | +0.752% | 0.022276 ± 0.000373 |
| [Q6_K](https://huggingface.co/spiritfather/Qwen3.8-Flash-Next-heretic-2-GGUF/tree/main/Q6_K) | 157.1 GiB (6 files) | 106.5 GiB | Q8_0 / Q6_K / Q6_K / Q8_0 | Q8_0 | ✓ | 3.619753 ± 0.045509 | +0.124% | 0.014800 ± 0.000285 |
| [Q8_0](https://huggingface.co/spiritfather/Qwen3.8-Flash-Next-heretic-2-GGUF/tree/main/Q8_0) | 175.3 GiB (6 files) | 124.6 GiB | Q8_0 / Q8_0 / Q8_0 / Q8_0 | Q8_0 | ✓ | 3.616601 ± 0.045455 | +0.036% | 0.000000 ± 0.000000 |

PPL/KLD: `llama-perplexity` on wikitext-2-raw test, ctx 512, 120 chunks, reference logits from this repo's Q8_0 (the bf16 trunk is 250 GiB and does not fit a 256 GB Mac; Q8_0 is within noise of it). Lower KLD is better; AesSedai's stock-model table uses the same method against bf16 and is the closest comparison.

## Loading (any current llama.cpp)

The trunk files load on stock llama.cpp — `qwen4exp` merged upstream in [#27742](https://github.com/ggml-org/llama.cpp/pull/27742) (b10685+). Vision needs `--mmproj mmproj/mmproj-Qwen3.8-Flash-Next-heretic-2-Q8_0.gguf` (projector is byte-identical to base; heretic only edits the LM).

```
llama-server -m Q4_K_M/Qwen3.8-Flash-Next-heretic-2-Q4_K_M-00001-of-00005.gguf -ngl 99 -fa on -c 65536 -ctk q8_0 -ctv q8_0 --jinja
```

**Memory:** only the trunk lives on the GPU (the "On GPU" column). The 51B-row n-gram table `per_layer_token_embd` (50.7 GiB at Q8_0) is a lookup table; with `--tensor-read-lazy auto` (default on builds with [#27837](https://github.com/ggml-org/llama.cpp/pull/27837)) it stays on disk and only touched rows page in — measured ~47 GB less resident memory, zero throughput cost. Context is cheap: ~21 KiB/token with q8_0 KV (full native 262K ≈ 5.5 GiB).

**Thinking:** on by default (`reasoning_effort` xhigh|medium|low). Turn off per request with `chat_template_kwargs: {"enable_thinking": false}` or serve with `--reasoning off --chat-template-kwargs '{"enable_thinking": false}'`.

## MTP speculative decoding (the model's own draft head)

Qwen ships a 4B NextN/MTP head trained jointly with the model; most Flash-Next GGUFs drop it. Here it is kept:

- `mtp/mtp-Qwen3.8-Flash-Next-heretic-2-Q8_0.gguf` — the head alone (34 tensors, 3.85 GiB), exported with `convert_hf_to_gguf.py --mtp`.
- `<QUANT>/MTP/` — a **pre-grafted shard pair** (rewritten shard 1 + a head shard) so you can add MTP to a quant you already downloaded without re-downloading the trunk.

**Requires llama.cpp [PR #27836](https://github.com/ggml-org/llama.cpp/pull/27836)** (`qwen4exp : add NextN/MTP draft head`) — stock master does not load the head for this arch (it ignores `nextn_predict_layers` for `qwen4exp`). Files follow that PR's tensor layout (`blk.48.*`, `nextn.hc_head_*`, +1-shifted norms) as of commit `1d8de7c`; if the layout changes before merge these two small artifacts will be re-exported. The head must be **in the model file** — `-md mtp-….gguf` does not work on that PR (it treats the sidecar as a full model). A build without the PR simply ignores the head tensors.

Steps (example Q4_K_M):

```bash
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
git fetch origin pull/27836/head:pr27836 && git checkout pr27836
cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j --target llama-server

# next to the trunk shards, add the two MTP files, then clone/rename the middle shards to the -MTP- pattern (cp -c = APFS clone; use ln on Linux)
cd Q4_K_M/ && cp MTP/* .
N=$(ls Qwen3.8-Flash-Next-heretic-2-Q4_K_M-MTP-00001-of-*.gguf | sed -E 's/.*-of-0*([0-9]+)\.gguf/\1/')
for i in $(seq 2 $((N-1))); do cp -c Qwen3.8-Flash-Next-heretic-2-Q4_K_M-$(printf %05d $i)-of-$(printf %05d $((N-1))).gguf Qwen3.8-Flash-Next-heretic-2-Q4_K_M-MTP-$(printf %05d $i)-of-$(printf %05d $N).gguf; done

llama-server -m Qwen3.8-Flash-Next-heretic-2-Q4_K_M-MTP-00001-of-$(printf %05d $N).gguf -ngl 99 -fa on \
    --spec-type draft-mtp --spec-draft-n-max 5 --spec-draft-p-min 0.75      # 6-7 for Q4-class quants; see the sweep below
```

Check the log for `creating MTP draft context` and `draft acceptance = …` lines.

### MTP report

Settings sweep on the **stock** Qwen3.8-Flash-Next (UD-Q4_K_XL + Q8_0 head, Apple M3 Ultra 256 GB, Metal, ~975-token prompt, 300 generated tokens, temp 0, single slot):

| n-max | p-min | code t/s | prose t/s | acceptance code / prose |
|--:|--:|--:|--:|:--|
| — (plain) | — | 33.9 | 34.1 | — |
| 2 | 0 | 47.7 | 38.5 | 89% / 73% |
| 3 | 0 | 50.2 | 35.7 | 86% / 61% |
| 4 | 0 | 49.9 | 31.5 | 82% / 48% |
| 6 | 0.75 | 59.7 | 42.5 | 91% / 81% |
| **7** | **0.75** | **60.1 (+77%)** | **44.4 (+30%)** | 88% / 84% |
| 8 | 0.75 | 44.3 | 40.5 | 85% / 84% |
| 8 | 0.5 | 37.6 | 30.3 | 74% / 55% |

Sweep on **this repo's Q8_0** (same box, same prompts; plain decode 36.1 code / 36.0 prose):

| n-max | p-min 0.75 code / prose | p-min 0.9 code / prose |
|--:|:--|:--|
| 1 | 42.3 / 40.1 | 40.6 / 38.8 |
| 3 | 54.6 / 42.6 | 54.1 / 42.0 |
| 5 | **60.5 / 42.6** | 57.4 / **42.9** |
| 6 | **61.4** / 41.0 | 58.5 / 42.6 |
| 7 | 45.6 / 41.2 | 46.8 / 42.2 |
| 8 | 40.5 / 40.0 | 48.1 / 40.0 |

(p-min 1.0 never drafts: flat 33 t/s, i.e. plain minus overhead.)

Takeaways: keep `--spec-draft-p-min` set (0.75–0.9); without it, depth beyond 3 loses to plain decode on prose. On Metal the sweet spot is **n-max 5–6 for Q8_0** (+70% code, +18% prose) and 6–7 for Q4 quants; one step past that falls off a cliff (verify-batch threshold in the Metal MoE path — may differ per backend). Reported elsewhere on this PR: HIP +17% at n-max 2; CUDA works; **Vulkan is a net loss** (rejected drafts replay the recurrent state). Greedy output is close to but not bit-identical with plain decode on any backend.

On these heretic-2 files: measured on this repo's Q4_K_M (Apple M3 Ultra 256 GB, Metal, PR #27836 build, ~975-token prompt, 300 generated tokens, temp 0, single slot, `n-max 7 / p-min 0.75`): **code: 28.6 → 49.9 t/s (+75%), draft acceptance 86% (227/263)**; **prose: 26.7 → 35.4 t/s (+33%), draft acceptance 80% (151/188)**. The head carries over to the heretic intact — acceptance matches the stock model's. The trunk was also confirmed to load and generate on a stock upstream-master build (`90c26fc`, no PRs), where the head files are simply ignored.

## Quant recipe

`llama-quantize` from a bf16 trunk exported with `--no-nextn`. **Only the routed-expert tensors (`ffn_{gate,up,down}_exps`) carry the nominal quant; everything else is pinned to Q8_0** (`--tensor-type` on `attn_`, `ssm_`, `hc_`, `_shexp`, `ple_`, `per_layer_token_embd`, plus `--token-embedding-type q8_0 --output-tensor-type q8_0`). This is the same shape AesSedai and unsloth use for this arch, and it matters: a plain `llama-quantize Q4_K_M` (which drops the 2-KV-head attention, the rank-320 hyper-connections, `ssm_out`, shared experts and embeddings to Q4–Q6) measured **KLD 0.177 / PPL +9.1%** vs Q8_0 on this model; the pinned recipe costs ~0.5 GiB more. `ffn_down_exps` has 640 columns and cannot take 256-block K/IQ quants, so llama.cpp upgrades it automatically (Q8_0/Q5_0 by layer in Q4_K_M, Q8_0 in Q6_K/Q5_K_M, IQ4_NL in IQ quants). Indexer projections stay BF16, gates/norms F32. Head quantized separately to Q8_0; grafted with jlkivey's `graft-mtp-shard.py` (byte-exact, verified).

Built with llama.cpp `qwen4exp/lazy-tensor+mtp` = master `90c26fc` + PR #27836 + PR #27837, transformers 5.16.1.

## License

Qwen Community License 1.0, inherited from the base model (not Apache-2.0: Model-as-a-Service use needs a separate license from Qwen).
