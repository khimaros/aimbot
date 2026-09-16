---
license: mit
base_model: inclusionAI/Ling-3.0-flash
base_model_relation: quantized
pipeline_tag: text-generation
tags:
  - gguf
  - llama.cpp
  - imatrix
  - moe
library_name: llama.cpp
---

# Ling 3.0 flash: GGUF

Quantizations of [`inclusionAI/Ling-3.0-flash`](https://huggingface.co/inclusionAI/Ling-3.0-flash):
124B total, 5.1B active, hybrid linear attention (35 KDA blocks interleaved 5:1 with 7 gated MLA
blocks) over a 512-expert MoE.

Bits are placed by hand rather than by the default rules, and the controls that prove it is worth
something are published next to the files. At the same size, our layout sits 31 to 41 % closer to
BF16 than what `llama-quantize` produces on its own

> **These files need a TurboQuant build.** `bailingmoe3` is in upstream llama.cpp, but we have some important bugfixes to it.
> Nothing has to be compiled, see [Run it](#run-it).

 
## Pick a file
 
| your memory | file | size | mean KL | |
| --- | --- | ---: | ---: | --- |
| 128 GB (Mac Studio, 2x 4090, ...) | `AD-Q5_K_M` | 89.4 GB | 0.0242 | the default pick |
| 96 GB | `AD-Q4_K_S` | 74.2 GB | 0.0318 | |
| 80 GB (H100, A100) | `AD-IQ4_XXS` | 69.3 GB | 0.0329 | |
| 64 GB | `AD-IQ3_M` | 62.2 GB | 0.0481 | |
| 48 GB | `AD-IQ2_M` | 49.1 GB | 0.0882 | quality starts to slip here |
| 32 GB | `AD-IQ1_S` | 32.4 GB | 0.2452 | last resort, expect real damage |
 
Weights and context share your memory, so leave headroom below the number in the first column.
Every rung of the ladder is in the [full table](#measurements).
 
Files **without** the `AD-` prefix are controls, published so the claim above can be checked. They
are not meant to be used: `*_STOCK` is what llama.cpp picks by itself, `*_FLAT` is our bit budget
with the differentiation switched off.
 
![image](https://cdn-uploads.huggingface.co/production/uploads/6a54dea4f19f5386700504da/6vQLcJ4kRKjBWFDKCm85V.png)

## Run it
 
Grab the archive for your machine from release
[`b10269-1.5.1`](https://github.com/AtomicBot-ai/atomic-llama-cpp-turboquant/releases/b10269-1.5.1)
or newer.
 
| machine | archive |
| --- | --- |
| Linux, NVIDIA | `llama-turboquant-linux-x64-cuda-13.3.tar.gz` (or `-cuda-12.4`) |
| DGX Spark, arm64 NVIDIA | `llama-turboquant-linux-arm64-cuda-13.3.tar.gz` |
| Linux, AMD | `llama-turboquant-linux-x64-rocm.tar.gz` |
| Linux, any GPU via Vulkan | `llama-turboquant-linux-x64-vulkan.tar.gz` |
| Linux, CPU only | `llama-turboquant-linux-x64-cpu.tar.gz` |
| macOS, Apple silicon | `llama-turboquant-macos-arm64.tar.gz` |
| Windows | `llama-turboquant-windows-x64-cuda-13.3.zip` and friends |
 
```bash
wget https://github.com/AtomicBot-ai/atomic-llama-cpp-turboquant/releases/download/b10269-1.5.0/llama-turboquant-linux-x64-cuda-13.3.tar.gz
tar xzf llama-turboquant-linux-x64-cuda-13.3.tar.gz && cd llama-turboquant-*
 
./llama-cli -m AD-Q5_K_M/Ling-3.0-flash-AD-Q5_K_M-00001-of-00002.gguf --jinja -ngl 99 -c 32768
```
 
The chat template ships inside the GGUF, thinking mode and tool calling included. Sampling
recommended by the authors: `temperature 0.6, top_p 0.95, top_k 20`.
 
Intel GPUs are the one gap: there is no SYCL archive yet, that path still needs a source build.
 
## What `AD` means
 
Atomic Dynamic: the bits are placed deliberately, along three axes.
 
- **by tensor role.** The router (`ffn_gate_inp`) and the expert bias stay F32, because an error
  there changes *which* expert runs instead of degrading its output. Attention, the KDA gates and
  the shared expert stay Q8_0. `output` stays F16, it feeds the logits directly.
- **by projection.** Inside the experts, `down_proj` gets more bits than `gate/up`, it is the more
  sensitive half of the SwiGLU.
- **by depth.** The edge MoE blocks (2, 3, 39, 40, 41) get more bits than the middle ones.
Routed experts are 97.1 % of the weights, so that is the only thing actually squeezed. Everything
else stays high precision and costs about 4 GB in total, which is cheap insurance.
 
### What it is worth, measured
 
| ours | size | mean KL | control | size | mean KL | |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| `AD-Q5_K_M` | 89.4 | 0.02420 | `Q5_K_M_STOCK` | 88.3 | 0.03509 | **31 % lower** |
| `AD-Q4_K_S` | 74.2 | 0.03178 | `Q4_K_M_STOCK` | 75.3 | 0.05121 | **38 % lower**, and smaller |
| `AD-IQ4_XXS` | 69.3 | 0.03293 | `IQ4_XS_STOCK` | 66.4 | 0.05605 | **41 % lower** |
| `AD-Q4_K_S` | 74.2 | 0.03178 | `Q4_K_FLAT` | 72.3 | 0.03321 | 4.3 % lower |
 
Those rows split the win. Most of it comes from refusing to quantize the 3 % of the weights that
are not experts. The per-projection and per-depth differentiation inside the experts adds the
remaining 4.3 % on top.


### NVFP4
 
Two builds, both 72.3 GB, [->safetensors for vLLM here<-](https://huggingface.co/AtomicChat/Ling-3.0-flash-NVFP4) and [->GGUF here<-](https://huggingface.co/AtomicChat/Ling-3.0-flash-NVFP4-GGUF).
 
| build | mean KL | top-1 | |
| --- | ---: | ---: | --- |
| `NVFP4` | 0.05602 | 94.72 % | the format as it comes |
| `AD-NVFP4` | 0.05363 | 94.86 % | our block scale |
 
Same format and same block layout in both. The AD build differs in one thing: the scale of each
block is chosen by sweeping the neighbouring UE4M3 codes, laying the weights on the E2M1 grid for
each candidate and scoring the error weighted by the importance matrix, with the same convention
the k-quants use.
 
Worth knowing before you download: at this size a k-quant rung is much closer to BF16
(`AD-Q4_K_S`, 74.2 GB, KL 0.0318). NVFP4 buys native FP4 tensor cores on Blackwell, not accuracy.

## Measurements
 

![image](https://cdn-uploads.huggingface.co/production/uploads/6a54dea4f19f5386700504da/_AMEbEps95GOOl0vkKpa5.png)


All numbers are measured against the BF16 baseline on held-out text that never entered the
calibration corpus, on identical hardware (4x RTX PRO 6000 Blackwell). Raw logs and json:
[`AtomicChat/Ling-3.0-flash-GGUF-metrics`](https://huggingface.co/datasets/AtomicChat/Ling-3.0-flash-GGUF-metrics).
 
- **mean KL** is how far the quantized model's next-token distribution sits from BF16, averaged
  over tokens. Lower is better, 0 means identical.
- **99 % KL** is the worst one percent of tokens. This is where a quant actually breaks.
- **top-1** is how often the quant's most likely token is the same as the BF16 one.

| quant | size, GB | bpw | mean KL | 99 % KL | top-1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `AD-Q8_0` | 133.1 | 8.56 | 0.01961 | 0.1385 | 98.05 % |
| `AD-Q6_K` | 107.5 | 6.91 | 0.02110 | 0.1614 | 97.92 % |
| `Q6_K_STOCK` | 102.2 | 6.57 | 0.02424 | 0.2045 | 97.59 % |
| `AD-Q5_K_L` | 95.3 | 6.13 | 0.02253 | 0.1815 | 97.62 % |
| `AD-Q5_K_M` | 89.4 | 5.75 | 0.02420 | 0.2011 | 97.45 % |
| `Q5_K_M_STOCK` | 88.3 | 5.68 | 0.03509 | 0.3327 | 96.76 % |
| `AD-Q5_K_S` | 87.4 | 5.62 | 0.02531 | 0.2088 | 97.35 % |
| `AD-Q4_K_L` | 84.0 | 5.40 | 0.02884 | 0.2572 | 97.01 % |
| `AD-Q4_K_M` | 79.3 | 5.10 | 0.03060 | 0.2715 | 96.82 % |
| `AD-IQ4_NL` | 79.3 | 5.10 | 0.03022 | 0.2846 | 96.81 % |
| `Q4_K_M_STOCK` | 75.3 | 4.84 | 0.05121 | 0.5737 | 95.44 % |
| `AD-IQ4_XS` | 74.8 | 4.81 | 0.03231 | 0.3076 | 96.66 % |
| `AD-Q4_K_S` | 74.2 | 4.77 | 0.03178 | 0.3101 | 96.60 % |
| `Q4_K_FLAT` | 72.3 | 4.65 | 0.03321 | 0.3301 | 96.47 % |
| `AD-NVFP4` | 72.3 | 4.65 | 0.05363 | 0.6389 | 94.86 % |
| `NVFP4` | 72.3 | 4.65 | 0.05602 | 0.6849 | 94.72 % |
| `AD-IQ4_XXS` | 69.3 | 4.46 | 0.03293 | 0.3325 | 96.44 % |
| `IQ4_XS_FLAT` | 68.6 | 4.41 | 0.03423 | 0.3390 | 96.42 % |
| `IQ4_XS_STOCK` | 66.4 | 4.27 | 0.05605 | 0.6462 | 94.94 % |
| `AD-IQ3_M` | 62.2 | 4.00 | 0.04809 | 0.5994 | 95.28 % |
| `AD-IQ3_S` | 57.8 | 3.72 | 0.05767 | 0.7663 | 94.63 % |
| `AD-IQ3_XXS` | 57.1 | 3.67 | 0.06034 | 0.7672 | 94.44 % |
| `AD-IQ2_M` | 49.1 | 3.16 | 0.08823 | 1.2551 | 92.50 % |
| `AD-IQ2_S` | 46.9 | 3.02 | 0.09351 | 1.3602 | 92.03 % |
| `AD-IQ2_XS` | 44.7 | 2.88 | 0.11132 | 1.6463 | 91.28 % |
| `AD-IQ2_XXS` | 39.2 | 2.52 | 0.14866 | 2.2138 | 90.08 % |
| `AD-IQ1_M` | 36.5 | 2.35 | 0.20415 | 3.0059 | 87.94 % |
| `AD-IQ1_S` | 32.4 | 2.08 | 0.24518 | 3.4699 | 86.58 % |
 
Two pairs sit at the same size on purpose. At 79 GB, `AD-Q4_K_M` is better in the tail and
`AD-IQ4_NL` in the mean. At 74 GB, `AD-Q4_K_S` is better in the mean and smaller, `AD-IQ4_XS`
better in the tail and in top-1. Pick by the metric you care about.
 
Sizes are GB, 10^9 bytes. llama.cpp prints GiB, so `AD-Q5_K_M` shows up there as 83.3 GiB.
 
Rung names follow the community convention, not the upstream preset list: `IQ4_XXS`, `Q5_K_L` and
`Q4_K_L` are our mixes and you will not find them in `llama-quantize`.
 
## How these were built
 
The base is a **bit-exact** BF16 conversion: 877 of 917 tensors are byte-identical to the
safetensors checkpoint, the remaining 40 are the MoE routers, stored as F32 instead of BF16, which
is a lossless widening (max absolute difference 0.0).
 
The new architecture was checked layer by layer against the HuggingFace reference before any quant
was produced. Over a fixed 32-token forward, the cosine similarity of the first block output is
0.99999 and the mean KL over the vocabulary is 4.8e-4, which is the noise floor between the
reference GPU kernels and the llama.cpp CPU path.
 
The importance matrix was collected on the **BF16** model, not on a quantized proxy, over 522
chunks of 4096 tokens from [`AtomicChat/calib-corpora`](https://huggingface.co/datasets/AtomicChat/calib-corpora).
 
Which tensor gets what:
 
| tensors | type | why |
| --- | --- | --- |
| `ffn_gate_inp`, `exp_probs_b`, all norms, `ssm_a`, `ssm_dt`, `ssm_conv1d_*` | F32 | an error in the router changes which expert runs, it does not degrade smoothly |
| `attn_*`, `ssm_f`, `ssm_g`, `ssm_beta` | Q8_0 | 2.4B parameters in total |
| `ffn_*_shexp` | Q8_0 | the shared expert sees every token |
| `output` | F16 | feeds the logits directly |
| `ffn_*_exps` | per rung | 120.8B parameters, the actual knob |
 
## Speed
 
4x RTX PRO 6000 Blackwell (96 GB each), full offload, `llama-bench`:
 
| quant | prompt, t/s | generation, t/s |
| --- | ---: | ---: |
| `AD-Q5_K_M` (83.3 GiB) | 3309 ± 38 | 106.6 ± 1.7 |
 
Consumer cards and Apple silicon will be added as those runs happen. Comparing across different
GPUs is not meaningful, so every figure says which machine it came from.
 
## On a Mac
 
GGUF runs natively on Apple silicon through Metal, MLX is not required:
 
```bash
./llama-cli -m AD-Q5_K_M/Ling-3.0-flash-AD-Q5_K_M-00001-of-00002.gguf --jinja -ngl 99 -c 32768
```
 
A 128 GB Mac Studio fits `AD-Q5_K_M` (89 GB) comfortably. `AD-Q6_K` (107 GB) needs the wired memory
limit raised and leaves little room for context.
 
## Known limitations
 
- **MTP / speculative decoding is not wired up.** The checkpoint carries one multi-token-prediction
  block, the converter drops it.
- **NVFP4 needs Blackwell to be fast.** It loads and runs elsewhere through the dequantization
  path, but the native FP4 tensor cores only exist on sm_100 and sm_120.
- **Intel GPUs need a source build.** No SYCL archive in the release yet.
 
