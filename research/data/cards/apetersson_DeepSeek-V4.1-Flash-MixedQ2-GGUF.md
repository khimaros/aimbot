---
license: mit
base_model: deepseek-ai/DeepSeek-V4.1-Flash
base_model_relation: quantized
library_name: gguf
pipeline_tag: text-generation
tags: [gguf, deepseek, deepseek-v4.1, mixed-quant, iq2-xxs, q2-k]
---

# DeepSeek-V4.1-Flash mixed-Q2 GGUF (IQ2_XXS gate/up + Q2_K down)

Routed-expert requantisation of `deepseek-ai/DeepSeek-V4.1-Flash` revision
`2bc89ac599031fa673cab993f1df02fc4a98c673`, produced on a 32-vCPU Runpod CPU pod with the
pinned llama.cpp ggml reference quantisers (PR `ggml-org/llama.cpp#28696` head
`cd628010bc3fc0a787d156c969d52a0789451c96`). Tensor names follow that PR's `deepseek4` table.

This is a **weights artifact**. No runtime has yet been shown to execute it end to end; the
"Runtime status" and "Smoke-test findings" sections say exactly what has been measured on which
hardware, and what is still blocked.

## Recipe

| projection | ggml type | bits/weight | tensors |
|---|---|---:|---:|
| gate/up (`w1`, `w3`) | IQ2_XXS | 2.0625 | 80 |
| down (`w2`) | Q2_K | 2.625 | 40 |

- Expert payload **152.88 GB for 543,581,798,400 routed weights = 2.2500 bits/weight**, block bytes
  copied verbatim from the digest-verified safetensors artifact (no re-quantisation during packing).
- Everything else keeps native precision: FP8 dense weights are dequantised to BF16 with
  DeepSeek-V4.1's **32x32** E8M0 block scales (V4 uses 128x128 — using the wrong value silently
  rescales every weight), BF16/F32 tensors are copied byte-for-byte, E8M0 scale tensors are consumed.
- **Not imatrix-based.** No activation calibration was collected; IQ2_XXS used a constant unit
  importance vector (the unweighted reference path). This is a deliberate memory-bounded choice,
  not a calibrated one.
- **Not included:** the two Engram tables (202.75 GB, stay native in the source checkpoint —
  SGLang dequantises them on lookup and can hold them host-resident), the MTP/DSpark blocks
  (no defined V4.1 GGUF slot in the runtime tables yet; skipped, not guessed), and the
  vision/aligner tensors (they belong in a separate mmproj file).

## Files

| file | bytes |
|---|---:|
| `DSV41-mixedq2-00001-of-00005.gguf` | 39,170,298,296 |
| `DSV41-mixedq2-00002-of-00005.gguf` | 39,994,226,128 |
| `DSV41-mixedq2-00003-of-00005.gguf` | 39,001,134,232 |
| `DSV41-mixedq2-00004-of-00005.gguf` | 39,579,707,392 |
| `DSV41-mixedq2-00005-of-00005.gguf` | 12,172,412,456 |
| **total** | **169,917,778,504 B = 169.92 GB (1,038 tensors, arch `deepseek4`)** |

`SHA256SUMS` covers the five shards. The pack is deterministic: two independent runs produced
byte-identical shard digests.

## Smoke-test findings (what was actually measured)

| check | hardware | result |
|---|---|---|
| gguf-py structural read-back (all 5 shards, split-aware) | CPU | **pass** — types IQ2_XXS/Q2_K/BF16/F32 as designed, no duplicate tensor names |
| shard transport, SHA256 re-hashed from the Hub | CPU pod in the GPU's datacenter | **pass** — all five shards match `SHA256SUMS` (39.17/39.99/39.00/39.97/10.80 GB, ~150-200 s each) |
| fidelity vs the MXFP4 source decode, 8 experts per projection | CPU | IQ2_XXS cosine **0.9407 min**, Q2_K **0.9633 min** (rel-RMS 0.352 / 0.270) |
| ggml **CPU** kernel, real blocks through `ggml_mul_mat` | 32-vCPU pod | cosine **0.99998**, rel-RMS **0.0068** vs the dequantised reference |
| ggml **CUDA** kernel (SM120, RTX PRO 6000) | 1× RTX PRO 6000 | inconclusive — the CUDA devel image needed `python3`/`curl` bootstrapping and PEP 668 blocked pip; fixed in the worker, not re-run (B200/B300 are the useful arches) |
| SGLang DeepSeek-V4 name map, **unpatched** | CPU | **fails**: 48 tensors have no rule and the router pair collides (`ffn_gate_inp` + `exp_probs_b` -> `layers.N.ffn.gate`) |
| SGLang DeepSeek-V4 name map, **patched** (4 rules below) | CPU, against the real shard-1 tensors | **pass — 245/245 tensors mapped** |
| SGLang end-to-end start | 1× B300 (§288 GB), GGUF read from a same-datacenter volume | **died before loading weights**: `Unrecognized model ... should have a model_type key in its config.json` — SGLang builds a `ModelConfig` from `AutoConfig` first. Fixed by shipping `config.json` + tokenizer with the shards; the retry is queued |
| llama.cpp V4.1 runtime | — | cannot load any V4.1 file: PR #28696 is converter-only and V4.1 ships no `output_hc_*` tensors |
| vLLM GGUF path | — | official plugin carries Triton IQ2_XXS GEMM/fused MoE but has **no DeepSeek tensor map** yet |

Operational findings worth more than the numbers:

- **A Runpod network volume is datacenter-local and single-attach.** The artifact volume is in
  US-NC-2; B300 stock was in US-WA-2/EU-NL-1, so the GPU could not mount it. Pre-fetch the shards
  with a *CPU* pod sharing the GPU's datacenter (a second network volume in that DC), then attach
  it to the GPU. Downloads at ~200 MB/s cost about 15 minutes of CPU-pod time instead of 15
  minutes of GPU time, and avoid Hugging Face rate limits (anonymous `curl` fetches get HTTP 429
  while an authenticated client is pulling the same repo).
- **Ship `config.json` and the tokenizer next to the shards.** They are now in this repository.
- SGLang's GGUF error surfaces before any tensor is read, so a config problem looks like a model
  problem; check `AutoConfig` resolution first when a start dies instantly.

Two defects were found and fixed by that fail-closed mapper before publication: MTP norm/head
templates had landed on the main `output_norm` (duplicate tensor, rejected by any split-aware
reader) and llama.cpp's router naming (`ffn_gate_inp` + `exp_probs_b`) collides in SGLang's mapper
(which splits `.weight`/`.bias`). The published pack has neither problem.

## Hardware that fits

| configuration | verdict |
|---|---|
| **1× B200 180 GB** + host Engram | **fits** — non-Engram static set ≈153 GiB against ~167.6 GiB usable |
| **1× B300 288 GB** + host Engram | **fits** comfortably (this is what the smoke uses while B200 stock is empty) |
| 2× RTX PRO 6000 96 GB + host Engram | fits weights (≈79 GiB/card) but needs expert-parallel plumbing |
| **1× RTX PRO 6000 96 GB** | **does not fit the model** — only useful for the kernel harness below |
| 4× RTX PRO 6000 96 GB | fits; the native route (no quantisation) is what current community builds use |

## Run recipes

### 1. SGLang — works with a 4-rule mapper patch (this is the tested path)

Requires `lmsysorg/sglang:dev-dsv41` (SGLang PR #38798) and an NVIDIA B300 (288 GB) or B200
(180 GB). Point `--model-path` at a directory holding the five shards **plus** `config.json`,
`tokenizer.json` and `tokenizer_config.json` from the source revision. Put a patched copy of
`srt/model_loader/deepseek4_gguf.py` ahead of SGLang on `PYTHONPATH` and add these four rules to
its `_v4_checkpoint_name` inner-layer branch (they fix the llama.cpp router naming and supply the
V4.1 indexer tensors that the mapper does not know yet):

**Patch required (two naming gaps, not a weight problem).** Copy the mapper patch from this
repository and apply it to the SGLang tree:

```bash
# patches/ is attached to this repository next to this README
git apply patches/sglang-deepseek4-gguf-name-map.patch      # from the SGLang repo root
# or, against an installed package:
patches/apply.sh --sglang-root /sgl-workspace/sglang        # applies in place, then verifies
```

It fixes the router naming collision (`ffn_gate_inp` + `exp_probs_b` -> `layers.N.ffn.gate`)
and supplies the 48 tensor rules the mapper lacks (`ffn_gate_inp.bias_vl` x40,
`indexer.attn_k` x4, `indexer.k_norm` x4). Measured: **unpatched the mapper fails; patched it
maps 245/245 tensors of shard 1.** See `patches/README.md` for the full rationale and the
packer-side `--naming sglang` alternative.

```bash
export SGLANG_ENABLE_DSV41_ENGRAM_HOST_TABLE=1        # Engram lives on the host, dequantised on lookup
export PYTHONPATH=/path/to/patched-sglang:$PYTHONPATH
python3 -m sglang.launch_server \
  --model-path ./gguf-with-config/                    # shards + config.json + tokenizer files
  --quantization gguf --load-format gguf \
  --tp-size 1 --port 30000 \
  --disable-cuda-graph                                # V4.1 cells OOM in graph capture (sglang#38839, #38861)
  --max-total-tokens 8192 --context-length 4096 --mem-fraction-static 0.85
# DSpark off: it is the part that fails to start on this backend.
```

**Engram is the known gap in this file.** The two hash tables are not in the GGUF, so the loader
must obtain them from the source revision; expect a missing-tensor error at the Engram layer if it
cannot. That error is the signal to attach those tables, not to change the quantisation.

Q2_K (`w2`) uses the tensor-core MMQ kernel; IQ2_XXS (`w1`/`w3`) has no MMQ in SGLang and takes the
MoE vector kernel at every token count, so prefill is slower than a k-quant file would be.

### 2. ggml kernel harness — works today on any Blackwell card, including 96 GB

```bash
git clone --filter=blob:none https://github.com/ggml-org/llama.cpp /opt/llama.cpp
git -C /opt/llama.cpp fetch --depth 1 origin refs/pull/28696/head
git -C /opt/llama.cpp checkout FETCH_HEAD
cmake -S /opt/llama.cpp -B /opt/llama.cpp/build -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=ON \
      -DGGML_NATIVE=OFF -DCMAKE_CUDA_ARCHITECTURES=120a -DBUILD_SHARED_LIBS=ON \
      -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF -DLLAMA_BUILD_TOOLS=OFF -DLLAMA_BUILD_SERVER=OFF
cmake --build /opt/llama.cpp/build --target ggml -j$(nproc)          # 120a=RTX PRO 6000, 100a=B200, 103a=B300
hf download apetersson/DeepSeek-V4.1-Flash-MixedQ2-GGUF --include '*00001*' --local-dir ./gguf
# (any single shard is enough: the harness slices one expert tensor out of it)
python3 v41_quant_kernel_smoke.py --gguf ./gguf --kernel-bin ./kernel_smoke --tensors 6
```

This executes the real IQ2_XXS/Q2_K blocks through `ggml_mul_mat` and compares against the
gguf-py dequantisation of the same bytes (gates: cosine ≥ 0.999, relative RMS ≤ 1%). It is the
only end-to-end check of the weights that runs on a 96 GB card and needs no model runtime.

### 3. llama.cpp — validation only

The container parses (`GGUFReader`), but the `deepseek4` runtime cannot load a V4.1 file yet.
Use it to verify the artifact, not to run it.

### 4. vLLM — blocked on a DeepSeek entry in the GGUF plugin

vLLM main has the V4.1 model definitions (PR #56228, merged), and the official
`vllm-project/vllm-gguf-plugin` has Triton IQ2_XXS GEMM + fused MoE. What is missing is a
DeepSeek tensor-name adapter in `vllm_gguf_plugin/weights_adapter/transformers.py`. Once that
exists, this is the better-performing route for prefill.

## GPU and staging notes learned the hard way

- **Stage everything on CPU before renting a GPU.** Hugging Face returns HTTP 429 to anonymous or
  bursty fetches (an authenticated client pulling the same repo at the same time is enough to
  trigger it), and every retry burns GPU dollars. The working pattern: one CPU pod sharing the
  GPU's datacenter downloads the shards, the `config.json`/tokenizer and this repo's worker bundle
  into a network volume; the GPU pod then starts with zero network work.
- **Runpod network volumes are datacenter-local and single-attach.** The weights were produced in
  US-NC-2; B300/B200 stock came and went in EU-NL-1, US-WA-2 and EUR-IS-2, so the volume cannot
  simply be mounted by the GPU. A delivery volume in the GPU's DC is the fix (US-WA-2 does not
  support network volumes; EU-NL-1 does).
- **AMD:** `AMD Instinct MI300X OAM` (192 GB) exists in the catalog and would fit these weights,
  but SGLang's DeepSeek-V4.1 work targets MI350X and its GGUF quantisation kernels are CUDA-only,
  so the serve path is unproven there. The kernel harness could run via ggml's HIP backend
  (`-DGGML_HIP=ON`), which is untested for this artifact.
- **Availability, not money, was the binding constraint** on the smoke: B200 has been empty all
  afternoon; B300 appears and disappears within minutes; MI300X was unavailable when probed.

## Limits, stated plainly

- The quantisation is uncalibrated (unit importance); no imatrix, no capability scores yet.
- Engram and MTP/DSpark are absent from this file, so a runtime that requires them must attach
  them from the source checkpoint (Engram) or run without the draft (DSpark).
- No behavioural evaluation has been run, so nothing here claims refusal behaviour, KL,
  multimodal quality or long-context quality.
- The 2.25 bits/weight pay for themselves only because one 180–288 GB card can then hold the
  model; on multi-GPU native-class hardware the native checkpoint is the safer choice.
