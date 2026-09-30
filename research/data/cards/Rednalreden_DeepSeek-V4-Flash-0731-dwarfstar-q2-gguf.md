---
license: mit
base_model: deepseek-ai/DeepSeek-V4-Flash-0731
base_model_relation: quantized
pipeline_tag: text-generation
library_name: gguf
tags:
  - gguf
  - deepseek
  - deepseek-v4
  - moe
  - imatrix
  - 2-bit
  - dwarfstar
---

# DeepSeek-V4-Flash-0731 — 2-bit imatrix GGUF for DwarfStar

A 2-bit, importance-matrix-guided GGUF quantization of
[deepseek-ai/DeepSeek-V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731),
built with the [DwarfStar](https://github.com/antirez/ds4) (`ds4`) toolchain.

Intended for 96 GB and 128 GB machines that cannot hold a 4-bit build.

| | |
|---|---|
| File | `DeepSeek-V4-Flash-0731-IQ2XXS-w2Q2K-AProjQ8-SExpQ8-OutQ8-imatrix.gguf` |
| Size | 86,720,111,520 bytes (80.8 GiB) |
| Resident model | 80.76 GiB |
| Context overhead | ~0.86 GiB at `--ctx 32768` |
| Architecture | 43 layers, 256 routed experts (top-6), 1 shared expert |

## Quantization recipe

| Tensor group | Type |
|---|---|
| Routed experts, gate (`w1`) / up (`w3`) | `IQ2_XXS` |
| Routed experts, down (`w2`) | `Q2_K` |
| Attention projections | `Q8_0` |
| Shared experts | `Q8_0` |
| Output | `Q8_0` |
| HC / compressor / indexer | `F16` |

This matches the established DwarfStar Flash `q2-imatrix` recipe, applied to the
0731 checkpoint. The 0731 weights ship as fp4 routed experts (`I8` packed E2M1
with `F8_E8M0` block-32 scales) and fp8 dense tensors; `deepseek4-quantize`
dequantizes both to f32 before requantizing.

## Importance matrix

Activation statistics were collected with the `ds4` runtime itself, hooking the
layer-major Metal prefill graph, so the counts come from the real DS4 inference
graph rather than a proxy implementation.

- Dataset: `gguf-tools/imatrix/dataset/rendered_prompts.txt` (DS4-rendered chat
  prompts: source review, long context, agent/tool-call DSML, prose tasks, and
  benchmark prompts, in both thinking and non-thinking forms)
- Budget: 2,720 prompts / 1,496,249 tokens / 386,032,242 routed-expert observations
- Output: 129 entries (43 layers × 3 routed tensors), one packed vector per expert

For gate/up the collector records squared FFN-normalized input activation; for
down, the squared route-weighted SwiGLU row.

## Measured effect of the imatrix

Scored against 100 official DeepSeek V4 Flash continuations by target-token
negative log likelihood, comparing this build to an otherwise identical build of
the same checkpoint quantized **without** an imatrix:

| Build | avg NLL |
|---|---:|
| 0731 Q2, no imatrix | 0.579809 |
| 0731 Q2, imatrix (this file) | 0.571552 |
| **Relative change** | **-1.42%** |

Per-case wins: 54 imatrix / 46 no-imatrix.

Both builds are the same checkpoint, so this isolates the imatrix contribution.
Note that the reference continuations were collected from an earlier Flash
checkpoint, which raises the absolute NLL for both builds equally; only the
relative difference is meaningful here.

## Usage

```sh
git clone https://github.com/antirez/ds4
cd ds4 && make
./ds4 -m DeepSeek-V4-Flash-0731-IQ2XXS-w2Q2K-AProjQ8-SExpQ8-OutQ8-imatrix.gguf \
      -p "Write a C function that reverses a string in place."
```

Or serve it:

```sh
./ds4-server -m DeepSeek-V4-Flash-0731-IQ2XXS-w2Q2K-AProjQ8-SExpQ8-OutQ8-imatrix.gguf --ctx 100000
```

Observed on an Apple M5 Max (128 GB, Metal): prefill 86.9 t/s, generation
29.6 t/s at short context. Throughput falls as context grows.

## Caveats

- 2-bit routed experts are a real quality tradeoff. If you have the RAM for a
  4-bit or mixed q2/q4 build, prefer it.
- Only the routed expert tensors are 2-bit; attention, shared experts, and the
  output head stay at `Q8_0`, and the HC/compressor/indexer path stays at `F16`.
- This file requires DwarfStar. It is not a llama.cpp-compatible GGUF: the DS4
  architecture, compressed attention, and packed routed-expert layout are
  specific to the `ds4` runtime.

## License

MIT, inherited from the base model.
