---
language:
- zh
- en
base_model:
- tencent/Hy4
---
[中文](./README_zh.md) ｜ English

<p align="center">
  <img src="https://github.com/Tencent/AngelSlim/blob/main/docs/source/assets/logos/angelslim_logo.png?raw=true" alt="AngelSlim" width="70%">
</p>

### A more accessible, comprehensive, and efficient toolkit for large model compression.

✒️ [TechnicalReport](https://arxiv.org/abs/2602.21233)   |    📖 [Documentation](https://angelslim.readthedocs.io/)   |   🤗 [Hugging Face](https://huggingface.co/AngelSlim)   |   🤖 [ModelScope](https://modelscope.cn/organization/AngelSlim)  


💬 [WeChat](https://github.com/Tencent/AngelSlim/blob/main/docs/source/assets/angel_slim_wechat.png?raw=true) |   🫨 [Discord](https://discord.com/invite/dHVNeuNdFt)  



# Hy4 (A49B) GGUF

**Language:** English · [中文](README_zh.md)

GGUF builds of the Hy4 VL model (`HYV4VLForConditionalGeneration`, 256 routed experts, 78 layers), plus the vision encoder as a separate mmproj file.

| file | size | bpw | notes |
|---|---:|---:|---|
| `Hy4-Q4_K_M.gguf` | 437.93 GiB | 4.89 | standard 4-bit, safe default |
| `Hy4-IQ2.gguf` | 309.58 GiB | 3.45 | routed-expert `gate`/`up` in IQ2_XS, rest as Q4_K_M |
| `Hy4-STQ1_0.gguf` | 214.65 GiB | 2.39 | MIX-STQ1_0 mixed precision, needs the STQ1_0 patch |
| `mmproj-HY4-VL-BF16.gguf` | 2.49 GiB | - | vision encoder (ViT + projector), works with all three |

![Hy4 GGUF benchmark results](https://huggingface.co/AngelSlim/Hy4-GGUF/resolve/main/Hy4-GGUF-BENCH.png)

---

## 1. What these are

**`Hy4-Q4_K_M.gguf`**: a conventional Q4_K_M. Most tensors are Q4_K, `ffn_down_exps` / `ffn_down_shexp` get Q6_K on 37 layers through llama.cpp's own logic. Use this unless you are memory-constrained.

**`Hy4-IQ2.gguf`**: the Q4_K_M recipe with the routed-expert `gate`/`up` projections lowered to IQ2_XS (2.31 bpw).

**`Hy4-STQ1_0.gguf`**: mixed precision at ~2.39 bpw, about half the size of Q4_K_M. The routed-expert `gate`/`up` projections run at 1.3125 bpw (STQ1_0) on 28 / 30 layers and 2.0625 bpw (IQ2_XXS) on the others. See section 4.

**`mmproj-HY4-VL-BF16.gguf`**: the vision tower in BF16 (convolution weights and position table in F32). A 40-layer SigLIP-style encoder (width 1536, patch 16) with a learned 128x128 position grid, followed by the `rmsnorm_mlp_adapter` projector: RMSNorm, 2x2 strided conv, GELU, 1x1 conv to 6144, and one newline embedding appended to each row of image tokens.

The text GGUFs were converted from the VL checkpoint. They carry `rope.dimension_sections = [12, 10, 10, 0]` and store the rope rows in NeoX order, so the text model runs interleaved M-RoPE (IMROPE). Text-only prompts give the same rotation as plain RoPE.

## 2. Building

```bash
git clone https://github.com/Little0o0/llama.cpp && cd llama.cpp
git checkout f8d4cc414        # head of PR #32517 

git apply ../hy4-patch/0001-stq1_0-quant-and-cuda.patch   # skip if you do not use STQ1_0

cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j
```

The default `-DGGML_NATIVE=ON` builds for the GPU in the local machine. Use the usual llama.cpp options if you need something else, see [docs/build.md](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md).

The STQ1_0 patch adds the type to ggml (CPU reference + ARM NEON, CUDA dequantize / MMVQ / MUL_MAT_ID), gguf-py and `llama-quantize`. It has no MMQ kernel, so prompt processing on STQ1_0 tensors goes through dequantize + cuBLAS.

## 3. Running

```bash
# image + text
build/bin/llama-mtmd-cli -m Hy4-IQ2.gguf --mmproj mmproj-HY4-VL-BF16.gguf \
    -ngl 99 -c 8192 --temp 0 -n 512 --jinja --image photo.jpg -p "Describe this image."

# OpenAI-compatible server (text and images)
build/bin/llama-server -m Hy4-STQ1_0.gguf --mmproj mmproj-HY4-VL-BF16.gguf \
    -ngl 99 -c 32768 --jinja --host 0.0.0.0 --port 8080

# text only
build/bin/llama-cli -m Hy4-IQ2.gguf -ngl 99 -c 8192 --temp 0 -n 512 --jinja -st -f prompt.txt
```

- **`--jinja` is required for chat.** The HY4 chat template matches no llama.cpp built-in family. The model thinks before it answers, so leave enough `-n` / `max_tokens` for the reasoning part.
- **The mmproj needs a VL text GGUF.** `hy_v4_vl` refuses a text model without rope sections, because image tokens need M-RoPE positions.
- **Loading from network storage.** llama.cpp mmaps weights by default and random page faults over NFS can be very slow. Either copy the GGUF to local disk or read it sequentially with `-lm none` (`--no-mmap` in older builds).
- VRAM for full residency: ~438 GiB (Q4_K_M), ~310 GiB (IQ2) or ~215 GiB (STQ1_0), plus the KV cache and ~3 GiB for the mmproj. One 8x H20 node (8 x 96 GiB) holds any of them; with less, lower `-ngl`.
- Images are resized like the HF processor (bicubic, multiples of 32 px, 4096 to 4194304 pixels), so one image takes between 4 and 4096 tokens plus one newline token per row.

Python tools reading these files must use the `gguf-py` of the patched tree, with an **absolute** path: `sys.path.insert(0, '/path/to/llama.cpp/gguf-py')`.

## 4. STQ1_0 and the mixed-precision recipe

**The format.** STQ1_0 comes from llama.cpp PR #22836. Weights are ternary `{-d, 0, +d}` with **exactly one of every four lanes forced to zero** (3:4 sparsity). Each group of 4 weights is a 4-bit code plus a 1-bit table select into a 32-entry codebook, and one fp16 scale covers 256 weights: `2 + 32 + 8 = 42` bytes per 256 weights = **1.3125 bpw**.

**Type id.** In this tree `GGML_TYPE_STQ1_0 = 44` (43 is `F8_E4M3`) and `LLAMA_FTYPE_MOSTLY_STQ1_0 = 43`. This matches the tensors stored in `hy_a49b-STQ1_0.gguf`. The patch shipped with [AngelSlim/Hy4-preview-GGUF](https://huggingface.co/AngelSlim/Hy4-preview-GGUF) is based on an older tree and uses 43, so do not mix the two.

**Where the bits go.** The three routed-expert families are most of the parameters, so the recipe spends freely on everything else:

| family | STQ1_0 build | why |
|---|---|---|
| `ffn_gate_exps` / `ffn_up_exps` | STQ1_0 (28 / 30 layers), IQ2_XXS (others) | the bulk, layer choice is imatrix-derived |
| `ffn_down_exps` | IQ3_XXS, IQ4_XS on the last 3 layers | writes straight into the residual stream, so it stays higher |
| shared expert `gate` / `up` / `down` | Q6_K | small, always active |
| attention `output` / `gate` / `q_a` | Q5_K | llama.cpp only bumps these automatically when `n_expert == 8`, HY4 has 256 |
| MLA `q_b` / `k_b` / `v_b` / `kv_a_mqa` | Q8_0 | the split HY4 names miss llama.cpp's substring rules |
| DSA indexer | Q8_0 / F32 | small, gates which 2048 tokens each query sees |
| iHC `*_fn`, router, norms, sinks | F32 | mirrors the reference `_keep_in_fp32_modules` |
| `token_embd` / `output` | BF16 / F32 | `output` via `--leave-output-tensor` |

### Re-quantizing from bf16

**An imatrix is mandatory for STQ1_0**: the encoder uses it for the scale solve and the zero placement.

```bash
build/bin/llama-quantize --imatrix imatrix.gguf \
    --tensor-type-file STQ1_0.tensortypes --leave-output-tensor \
    HY4-VL-BF16-00001-of-00033.gguf out.gguf IQ1_M      # Q4_K_M build: use Q4_K_M as the base ftype
```

The mmproj is converted separately from the HF checkpoint:

```bash
python3 convert_hf_to_gguf.py /path/to/hf_checkpoint --mmproj --outtype bf16 --outfile mmproj-HY4-VL-BF16.gguf
```

---

## Files

```
hy4-patch/
  0001-stq1_0-quant-and-cuda.patch    25 files, +685/-4, applies on f8d4cc414 (PR #32517), STQ1_0 only
```