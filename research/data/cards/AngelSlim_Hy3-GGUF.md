---
base_model:
- tencent/Hy3
pipeline_tag: text-generation
license: apache-2.0
---


<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/Tencent/AngelSlim/blob/main/docs/source/assets/logos/angelslim_logo_light.png?raw=true">
    <img alt="AngelSlim" src="https://github.com/Tencent/AngelSlim/blob/main/docs/source/assets/logos/angelslim_logo.png?raw=true" width=55%>
  </picture>
</p>

<h3 align="center">
Dedicated to building a more intuitive, comprehensive, and efficient LLMs compression toolkit.
</h3>

<p align="center">
          📖 <a href="https://angelslim.readthedocs.io/">Documentation</a>&nbsp&nbsp | &nbsp&nbsp🤗 <a href="https://huggingface.co/AngelSlim">Hugging Face</a>&nbsp&nbsp | &nbsp&nbsp🤖 <a href="https://modelscope.cn/models/AngelSlim/Hy3-GGUF">ModelScope</a>&nbsp&nbsp | &nbsp&nbsp💬 <a href="./docs/source/assets/angel_slim_wechat.png">WeChat</a>
<br>
</p>

<br>

# Hy3 llama.cpp Quantization

Low-bit quantized **Hy3 (hy_v3)** GGUFs for llama.cpp — ready to run out of the box, with MTP self-speculative decoding. This repo ships the quantized models, plus the mixed-precision recipes to build your own from a calibration set.

<p align="center">
  <img src="assets/benchmark.png" width="95%"/>
</p>

Two parts below: **Deploy** (build & run) and **Quantization**.

---

# Quick Start

## Build

Clone the latest llama.cpp (must include the `hy_v3` support merged in
[PR #25395](https://github.com/ggml-org/llama.cpp/pull/25395) — i.e. any commit after
`505b1ed`; the current `master` is fine) and build it following the official
[build guide](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md):

```bash
git clone https://github.com/ggml-org/llama.cpp llama.cpp-hyv3
# build per docs/build.md (CUDA / Metal / CPU as appropriate for your machine)
```

Binaries land in `llama.cpp-hyv3/build/bin/`.

> **Already downloaded an older GGUF?** Earlier GGUFs here were built against a patched
> llama.cpp and won't load correctly on today's upstream. To build and run those, follow
> the [previous README](https://huggingface.co/AngelSlim/Hy3-GGUF/blob/218c93f0fb5227553b67e556b01dfe70fb70cf30/README.md)
> (the `setup_hyv3_llama.sh` + patches flow) instead.

## Run

```bash
# plain serve (no speculative decoding)
./llama.cpp-hyv3/build/bin/llama-server -m /path/to/Hy3.gguf -ctk q8_0 -ctv q8_0 -fa on -c 65536

# serve + MTP self-speculative decoding (needs an MTP gguf, i.e. converted WITHOUT --no-mtp)
./llama.cpp-hyv3/build/bin/llama-server -m /path/to/Hy3-mtp.gguf --spec-type draft-mtp --spec-draft-n-max 3 --spec-draft-n-min 1 -ctk q8_0 -ctv q8_0 -ctkd q8_0 -ctvd q8_0 -fa on -c 65536
```

### Recommended setups

| GPUs | build | MTP | `-c` (context) | KV cache |
|---|---|---|---|---|
| 1× H20 (96 GB) | IQ1_M | no  | `-c 65536` | `-ctk q8_0 -ctv q8_0` |
| 2× H20 (192 GB) | IQ1_M | yes | / (default) | / (f16) |
| 2× H20 (192 GB) | Q4_K_M | yes | `-c 65536` | `-ctk q8_0 -ctv q8_0 -ctkd q8_0 -ctvd q8_0` |
| 4× H20 (384 GB) | Q4_K_M | yes | / (default) | / (f16) |

Weights: IQ1_M ~83 GiB, Q4_K_M ~166 GiB (MTP adds ~2 GiB plus a draft KV cache).
1 card fits only IQ1_M, and tightly — shrink context, quantize KV, no MTP. 2 cards
run IQ1_M+MTP with room to spare (drop `-c`/KV flags), but Q4_K_M+MTP is tight, so
keep `-c 65536` and q8_0 KV (main + draft). 4 cards run Q4_K_M+MTP comfortably.

---

# Quantize with Your Own Data

If you have a calibration set, you can compute your own importance matrix and
quantize the model yourself. All steps use stock llama.cpp tools; the mixed-precision
recipes are shipped in this folder.

### The mixed-precision recipes

The recipes in `recipes/` spend bits where they matter:

- **Attention** (`attn_q/k/v`) and the **token embedding / output head** stay high
  (q8_0 / q4_K / q6_K) — cheap in size, and where low bits hurt most.
- **Shared experts** (`ffn_*_shexp`, active on every token) stay at q5_K–q6_K.
- **Routed experts** (`ffn_*_exps`) carry the aggressive low bits and dominate the file
  size. In the IQ1_M recipe most layers are iq1_m, with `ffn_down` a bit higher
  (iq3_xxs) and sensitive layers upgraded (iq2_xxs) layer-by-layer.

| recipe | target | MTP head |
|---|---|---|
| `recipes/hyv3_q4km_recipe.txt`     | ~Q4_K_M mixed | no  |
| `recipes/hyv3_q4km_mtp_recipe.txt` | ~Q4_K_M mixed | yes |
| `recipes/hyv3_iq1m_recipe.txt`     | ~IQ1_M mixed (extreme) | no  |
| `recipes/hyv3_iq1m_mtp_recipe.txt` | ~IQ1_M mixed (extreme) | yes |

The `*_mtp` variants add the MTP block (`blk.<n>.nextn.*` and layer-`<n>` experts).
Use them only for a gguf that still has the MTP head; use the plain ones for a gguf
converted with `--no-mtp`. (The MTP block's experts stay at K-quant, not IQ*, because
very-low-bit IQ types need an imatrix and the imatrix only covers the trunk layers.)

### 1. Convert HF → BF16 GGUF

```bash
PYTHONPATH=./llama.cpp-hyv3/gguf-py python ./llama.cpp-hyv3/convert_hf_to_gguf.py /path/to/HYV3-hf --outfile Hy3-BF16.gguf --outtype bf16
#   add --no-mtp to drop the MTP head (then use a non-mtp recipe below)
```

### 2. Compute the importance matrix (imatrix)

The calibration file is plain text containing samples with the model's special
tokens already applied (one file, fed via `-f`). The imatrix is independent of the
target quant type — compute it once on BF16 and reuse it for any recipe.

```bash
./llama.cpp-hyv3/build/bin/llama-imatrix -m Hy3-BF16.gguf -f calib.txt -o imatrix.gguf --output-format gguf --parse-special
#   single GPU can't hold BF16 -> add --cpu-moe (keep experts on CPU) or -ngl 0
```

### 3. Quantize with a recipe

Pick the recipe matching your target and whether the gguf has an MTP head (table
above). `--token-embedding-type` differs: keep it at q8_0 for Q4_K_M (embedding is
cheap, no reason to crush it), drop it to q4_K for the extreme IQ1_M build. The
examples below are for MTP ggufs — use the `non-mtp` recipe for a `--no-mtp` gguf.

```bash
# ~Q4_K_M mixed
./llama.cpp-hyv3/build/bin/llama-quantize --imatrix imatrix.gguf --tensor-type-file recipes/hyv3_q4km_mtp_recipe.txt --token-embedding-type q8_0 --output-tensor-type q6_K Hy3-BF16-mtp.gguf Hy3-Q4_K_M-mtp.gguf Q4_K_M

# ~IQ1_M mixed (extreme)
./llama.cpp-hyv3/build/bin/llama-quantize --imatrix imatrix.gguf --tensor-type-file recipes/hyv3_iq1m_mtp_recipe.txt --token-embedding-type q4_K --output-tensor-type q6_K Hy3-BF16-mtp.gguf Hy3-IQ1_M-mtp.gguf IQ1_M
```