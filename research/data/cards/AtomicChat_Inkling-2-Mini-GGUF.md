---
license: apache-2.0
base_model: thinkingmachines/Inkling-2-Mini
pipeline_tag: image-text-to-text
tags:
- gguf
- llama.cpp
- inkling2
- moe
---

# Inkling-2-Mini GGUF

<div style="display: flex; gap: 8px; align-items: center; margin-top: 10px; margin-bottom: 10px;">
  <a href="https://atomic.chat/?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_inkling_2_mini&utm_content=btn_atomic"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_atomic.png" width="162" alt="Atomic Chat"></a>
  <a href="https://discord.gg/8wGSsvmg4V"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_discord.png" width="119" alt="Discord"></a>
  <a href="https://github.com/AtomicBot-ai/Atomic-Chat"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_github.png" width="115" alt="GitHub"></a>
  <a href="https://x.com/atomic_chat_hq"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_x.png" width="108" alt="X"></a>
</div>
<ul style="margin: 0 0 12px 0;">
  <li>Learn how to run Inkling 2 Mini locally - read <a href="https://atomic.chat/blog/guides/how-to-run-inkling-2-mini-locally?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_inkling_2_mini&utm_content=bullet_guide">our guide</a>.</li>
  <li>Built by the team behind <a href="https://atomic.chat/?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_inkling_2_mini&utm_content=bullet_app">Atomic Chat</a>, the app that runs open-weight models locally and offline.</li>
</ul>
<hr style="margin: 0 0 16px 0;">


GGUF files of [thinkingmachines/Inkling-2-Mini](https://huggingface.co/thinkingmachines/Inkling-2-Mini) by AtomicChat: a 26.4B mixture-of-experts model (3.4B active, 128 experts with 8 active) with a looped core, where the middle 12 of its 24 layers run three times. It takes text and image input. License: Apache-2.0, the same as the base model (LICENSE in this repo).

## Files

AD (Atomic Dynamic) files give each tensor its own type. The experts hold 94% of the weights and carry the compression; attention and the loop controllers stay Q8_0. Quality is measured against our BF16: top-1 is how often the file picks the same next token as the original, and mean KLD is the divergence of the whole next-token distribution (lower is better).

| file | GB on disk | top-1 | mean KLD | notes |
|---|---:|---:|---:|---|
| `BF16/` (2 parts) | 52.2 | — | — | the reference |
| `Inkling-2-Mini-Q8_0.gguf` | 27.74 | 97.7% | 0.0033 | |
| **`Inkling-2-Mini-AD-Q6_K.gguf`** | 23.79 | **97.6%** | **0.0037** | Q8_0 quality, 4 GB smaller |
| `Inkling-2-Mini-Q6_K.gguf` | 23.40 | 97.3% | 0.0047 | llama.cpp preset, no imatrix |
| `Inkling-2-Mini-Q5_K_M.gguf` | 19.81 | 96.3% | 0.0079 | llama.cpp preset, no imatrix; still in the PR #32695 layout, does not load on b12600 yet |
| **`Inkling-2-Mini-AD-Q5_K.gguf`** | 19.07 | **97.1%** | **0.0052** | |
| `Inkling-2-Mini-Q4_K_M.gguf` | 17.38 | 94.7% | 0.0165 | llama.cpp preset, no imatrix; still in the PR #32695 layout, does not load on b12600 yet |
| **`Inkling-2-Mini-AD-Q4_K.gguf`** | 16.53 | **96.3%** | **0.0080** | Q5_K_M quality, 3.3 GB smaller |
| **`Inkling-2-Mini-AD-IQ4_XS.gguf`** | 15.00 | **95.8%** | **0.0101** | |
| **`Inkling-2-Mini-AD-IQ3_S.gguf`** | 13.34 | **94.2%** | **0.0205** | |
| **`Inkling-2-Mini-AD-IQ3_XXS.gguf`** | 12.58 | **93.3%** | **0.0271** | |
| **`Inkling-2-Mini-AD-IQ2_S.gguf`** | 11.56 | **91.3%** | **0.047** | |
| **`Inkling-2-Mini-AD-IQ2_XXS.gguf`** | 10.43 | **88.5%** | **0.084** | |
| **`Inkling-2-Mini-AD-IQ2_M.gguf`** | 8.67 | **85.7%** | **0.130** | expert down Q2_0 except the 8 busiest layers |
| **`Inkling-2-Mini-AD-IQ2_XXS-Q2.gguf`** | 7.90 | **84.3%** | **0.158** | |
| **`Inkling-2-Mini-AD-IQ1_M.gguf`** | 7.26 | **81.1%** | **0.236** | 1-bit |
| **`Inkling-2-Mini-AD-IQ1_S.gguf`** | 6.88 | **79.5%** | **0.278** | 1-bit |
| `mmproj-Inkling-2-Mini-F16.gguf` / `-BF16.gguf` | 0.64 | | | vision projector (image input) |
| `mmproj-Inkling-2-Mini-Q8_0.gguf` | 0.35 | | | smaller vision projector, checked with AD-IQ1_S on b12603 |

Even Q8_0 matches the BF16's top token only 97.7% of the time on this model, so 97–98% is the ceiling here, not 99%+. Our guess is that rounding adds up over the 48 layer passes of the loop; we have not tested it.

- **Measured:** our neutral corpus in 30 languages, 87 chunks of 4096 tokens. The tool is llama.cpp `llama-perplexity --kl-divergence`, built from PR #32695. Every file was measured against the same BF16 logits, made once on an H100; the files themselves ran on H100 and A10 GPUs with that one build. The table, the importance matrix and the per-tensor recipes are in [AtomicChat/Inkling-2-Mini-GGUF-metrics](https://huggingface.co/datasets/AtomicChat/Inkling-2-Mini-GGUF-metrics).
- **How to choose:** the memory a file needs is its size plus the KV cache plus about 1 GB of buffers. The KV cache is small here: only 4 of the 24 layers use full attention, the rest a 1024-token window. Good 4-bit files reach 96–97% top-1. The 1- and 2-bit files are for machines where nothing larger fits.
- **The presets' names don't tell the whole story.** The expert down projection has rows of 1152, which k-quants cannot take, so llama.cpp swaps the type there: Q8_0 in all 24 layers of Q6_K; Q8_0 in half of the layers and Q5_1 in the rest for Q5_K_M; Q8_0 and Q5_0 for Q4_K_M. The AD files use block-32 types on that tensor by design. The 1- and 2-bit files put Q2_0 there, quantized with the importance matrix (`patches/q2_0-imatrix.patch`; llama.cpp's own Q2_0 quantizer ignores the matrix).
- **Importance matrix:** 4.76M tokens of our calibration corpus rendered through the model's chat template, in 6 shards. Two shards ran on the BF16. Four ran on the Q8_0, because no GPU with room for the 52 GB BF16 was free at release time.
- **Base:** the vendor ships the weights in NVFP4 and MXFP8; our BF16 is that checkpoint dequantized.


## Optional DSpark drafter

[Download `dspark-Inkling-2-Mini-Q8_0.gguf`](https://huggingface.co/AtomicChat/Inkling-2-Mini-GGUF/resolve/main/dspark-Inkling-2-Mini-Q8_0.gguf) (481 MiB). This is the original Inkling-2-Mini DSpark drafter exported from Thinking Machines' `mtp.safetensors`. Q8_0 applies to 27 attention and MLP projections. The remaining 31 tensors match our BF16 export byte for byte.

> **Running this drafter currently requires a llama.cpp build from [PR #32218](https://github.com/ggml-org/llama.cpp/pull/32218).** The commands below pin the tested commit, `e4b1cb5`. Use the `inkling2_loop` target `Inkling-2-Mini-AD-Q4_K.gguf` from this repository.

### Run with DSpark on CUDA

```bash
git init llama.cpp-inkling-dspark
git -C llama.cpp-inkling-dspark fetch --depth=1 https://github.com/ggml-org/llama.cpp.git \
  e4b1cb5318f1ac55d148be228c6347c6a94cc4c6
git -C llama.cpp-inkling-dspark checkout --detach FETCH_HEAD
cmake -S llama.cpp-inkling-dspark -B llama.cpp-inkling-dspark/build \
  -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release
cmake --build llama.cpp-inkling-dspark/build --target llama-server --parallel

hf download AtomicChat/Inkling-2-Mini-GGUF \
  Inkling-2-Mini-AD-Q4_K.gguf dspark-Inkling-2-Mini-Q8_0.gguf --local-dir inkling-gguf

llama.cpp-inkling-dspark/build/bin/llama-server \
  -m inkling-gguf/Inkling-2-Mini-AD-Q4_K.gguf \
  -md inkling-gguf/dspark-Inkling-2-Mini-Q8_0.gguf \
  --spec-type draft-dspark --spec-draft-n-max 3 \
  -ngl 99 -ngld 99 -fa on -c 4096 -np 1 --jinja
```

### AtomicChat and Unsloth on the same A100

We used one A100 SXM4 40 GB, one request at a time, a 4,096-token context, and the same three greedy text prompts (code, explanation, and JSON). Each run generated 192 tokens per prompt. Decode throughput is total generated tokens divided by total decode time. Peak VRAM is the highest device reading sampled every 200 ms. Acceptance is accepted draft tokens divided by proposed draft tokens.

| Target and runtime | Drafter | Decode tok/s | Peak VRAM | Draft tokens accepted |
|---|---|---:|---:|---:|
| AtomicChat `AD-Q4_K`, llama.cpp PR #32218 | Off | 46.4 | 16.42 GiB | — |
| AtomicChat `AD-Q4_K`, llama.cpp PR #32218 | AtomicChat Q8_0 | **62.7** | **17.79 GiB** | 44.9% (328/730) |
| Unsloth `UD-Q4_K_XL`, [Unsloth CUDA 12 Portable build b12588](https://github.com/unslothai/llama.cpp/releases/tag/b12588-mix-c0c3de8) | Off | 45.8 | 17.05 GiB | — |
| Unsloth `UD-Q4_K_XL`, same build | Unsloth Q8_0 | 53.2 | 18.44 GiB | 46.4% (331/714) |

DSpark increased decode throughput by 35.0% for AtomicChat and 16.1% for Unsloth. With DSpark enabled, the AtomicChat setup decoded 17.7% faster and used 0.65 GiB less peak VRAM in this run. The comparison uses each publisher's own target quant and runtime. In the AtomicChat control, our BF16 and Q8_0 drafters generated identical token IDs on all three prompts, and both diverged from the run without DSpark at the same positions.

## Run it

The GGUF files in this repository have been updated to use the merged Inkling 2 loop architecture from [llama.cpp PR #32694](https://github.com/ggml-org/llama.cpp/pull/32694).

**Requirements:** llama.cpp b12600 or newer.

The previous implementation from PR #32695 is no longer required.

### Build llama.cpp

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j
```

### Run the model

```bash
./build/bin/llama-server \
  -m Inkling-2-Mini-AD-Q4_K.gguf \
  --jinja \
  -c 32768 \
  -ngl 99
```

**Important:** Do not mix GGUF files from the old PR #32695 layout with the merged PR #32694 implementation.


- **Thinking** is set by the chat template's `reasoning_effort`: `none`, `minimal`, `low`, `medium`, `high`, `xhigh` (default 0.9). Pass it as `"chat_template_kwargs": {"reasoning_effort": "low"}` on `/v1/chat/completions`. The vendor notes that `none` does not switch reasoning off completely.
- **Sampling:** the vendor's generation config uses temperature 1.0.
- **Checked** in llama-server (BF16, AD-IQ1_M, AD-IQ1_S, with the F16 projector): plain chat, reasoning at `none` and `high`, a tool call, an image question, and a reply in Chinese.

## Related

- **Uncensored variant:** [AtomicChat/Inkling-2-Mini-Uncensored-GGUF](https://huggingface.co/AtomicChat/Inkling-2-Mini-Uncensored-GGUF): a LoRA adapter for these files, and AD-Q4_K, AD-IQ3_S and AD-IQ2_M with the edit baked in.
