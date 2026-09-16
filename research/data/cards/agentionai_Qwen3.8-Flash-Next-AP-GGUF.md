---
base_model:
- Qwen/Qwen3.8-Flash-Next
base_model_relation: quantized
license: other
license_name: qwen-community-1.0
license_link: LICENSE
library_name: gguf
pipeline_tag: text-generation
tags:
- gguf
- qwen3.8-flash-next
- qwen4exp
- imatrix
- agentionai
---

# Qwen3.8-Flash-Next AP GGUF

[Agention Precision](https://agention.ai/models/qwen3.8-flash-next/) (AP) quants of
[Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next).
Mainline llama.cpp compatible — standard quant types only, no fork required.

<div align="left">
  <p>
    <em>Quantized for accuracy per gigabyte of VRAM, and measured — every tier below is
    scored against the same reference on a held-out corpus.
    <a href="https://agention.ai/models/qwen3.8-flash-next/">Method and full results</a>.</em>
  </p>
</div>


Each tier varies the quant type per tensor group rather than using one type throughout, to get the most accuracy per gigabyte of VRAM.

![Quality against size across the AP lineup](chart.png)


## Tiers

| tier | VRAM | n-gram table (host) | download size | eff. bpw | experts (gate/up) | KL div | top-1 agree |
|---|---:|---:|---:|--:|---|---|---|
| `AP-Q5_K_XL` | **76.75** | 35.76 | 112.51 | 5.46 | Q5_K 5.5 | 0.0839 ± 0.0008 | 86.63 ± 0.14 % |
| `AP-Q5_K_M` | **76.75** | 26.82 | 103.57 | 5.03 | Q5_K 5.5 | 0.0853 ± 0.0008 | 86.48 ± 0.14 % |
| `AP-Q4_K_XL` | **67.38** | 26.82 | 94.20 | 4.57 | Q4_K 4.5 | 0.0992 ± 0.0009 | 85.71 ± 0.14 % |
| `AP-Q4_K_M` | **61.22** | 26.82 | 88.04 | 4.27 | IQ4_XS 4.25 + IQ3_S 3.44 | 0.1243 ± 0.0011 | 84.22 ± 0.15 % |
| `AP-IQ4_XS` | **57.42** | 26.82 | 84.24 | 4.09 | IQ3_S 3.44 | 0.1584 ± 0.0014 | 82.89 ± 0.15 % |
| `AP-IQ3_XXS` | **53.90** | 26.82 | 80.72 | 3.92 | IQ3_XXS 3.06 | 0.1844 ± 0.0016 | 81.85 ± 0.16 % |
| `AP-IQ2_S` | **49.21** | 26.82 | 76.03 | 3.69  | IQ2_S 2.5 | 0.2657 ± 0.0022 | 79.14 ± 0.16 % |


Sizes in GiB. **VRAM** is what the GPU must hold; the 51.2B-parameter n-gram table
(`per_layer_token_embd`) is offloadable to system RAM with
`-ot "per_layer_token_embd=CPU"`, so plan around the VRAM column, not the download.

**Tier names follow the base ftype convention** (as unsloth's do) and do not describe the
experts — the `experts` column does.

## Which one should I use?

- **`AP-Q4_K_XL`** — the default. Closest to the source that still fits a 72 GiB budget.
- **`AP-Q4_K_M`** — 6 GiB less VRAM for 1.5 points of top-1. Take it if 67 GiB doesn't fit.
- **`AP-IQ2_S`** — the floor. Usable at 49 GiB, and 2.8 points ahead of the nearest
  2-bit alternative at comparable size, but the gap to Q4 is large. Take it only if you must.

`AP-Q5_K_M` and `AP-Q5_K_XL` need identical VRAM (76.75 GiB) and are 1.7σ apart in quality —
the XL's extra 9 GiB is entirely n-gram-table precision. Prefer `AP-Q5_K_M` unless you keep
the table on the GPU.

## Quality methodology

All figures are KL divergence and top-1 agreement against the same source, measured
on a **held-out corpus** the model has not memorised, `-c 2048`, via
`llama-perplexity --kl-divergence`. This means that numbers can't be directly compared with other measurements.

**Why not wikitext.** This architecture carries a 51.2B-parameter n-gram lookup table, and
wikitext is inside its memorised set. The same file scores **6.9–8.6 points higher top-1 on
wikitext than on held-out text**, and the inflation *grows* as the quant gets smaller — so
wikitext compresses exactly the differences you are choosing between. It is vendor-
independent; other publishers' quants of this model show it too. For reference, `AP-Q4_K_M`
scores 84.22 % held-out and 91.82 % on wikitext.

## Running

```bash
llama-cli -hf agentionai/Qwen3.8-Flash-Next-AP-GGUF:AP-Q4_K_XL \
  -ngl 999 -fa 1 -ot "per_layer_token_embd=CPU"
```

Qwen's recommended settings:

| parameter | thinking mode | instruct (non-thinking) |
|---|---|---|
| temperature | 1.0 | 0.7 |
| top_p | 0.95 | 0.80 |
| top_k | 20 | 20 |
| min_p | 0.0 | 0.0 |
| presence_penalty | 0.0 | 1.5 |
| repetition_penalty | 1.0 | 1.0 |

The `-ot` flag keeps the 51.2B-parameter n-gram table in system RAM. You have three
choices for where that table lives:

## Vision

The vision projector is `mmproj-F16.gguf` at the repository root. Download it alongside any
tier to enable image input:

```bash
llama-cli -hf agentionai/Qwen3.8-Flash-Next-AP-GGUF:AP-Q4_K_XL \
  --mmproj-hf agentionai/Qwen3.8-Flash-Next-AP-GGUF:mmproj-F16.gguf \
  -ngl 999 -fa 1 -ot "per_layer_token_embd=CPU"
```

## Support AgentionAI
These quants are released freely. If it saves you compute or makes Qwen more useful, you can sponsor continued tuning, quantization and benchmarking on [GitHub](https://github.com/sponsors/agentionai).