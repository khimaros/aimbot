---
base_model: ricursiveAI/Ripple-65B-Preview
base_model_relation: quantized
quantized_by: AtomicChat
pipeline_tag: text-generation
library_name: gguf
license: apache-2.0
tags:
- gguf
- llama.cpp
- ripple
- ricursiveai
- quantized
- conversational
- agentic-coding
- atomic-chat
---

# How to Run Ripple-65B Preview Locally
<p style="margin-top: 0; margin-bottom: 0;">
  <em>The first GGUF of Ricursive's Ripple-65B Preview. We wrote its llama.cpp support, merged upstream in b12167. Built from ricursiveAI's original BF16 weights.</em>
</p>
<div style="display: flex; gap: 8px; align-items: center; margin-top: 10px; margin-bottom: 10px;">
  <a href="https://atomic.chat/?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_ripple_65b_preview&utm_content=btn_atomic"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_atomic.png" width="162" alt="Atomic Chat"></a>
  <a href="https://discord.gg/8wGSsvmg4V"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_discord.png" width="119" alt="Discord"></a>
  <a href="https://github.com/AtomicBot-ai/Atomic-Chat"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_github.png" width="115" alt="GitHub"></a>
  <a href="https://x.com/atomic_chat_hq"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_x.png" width="108" alt="X"></a>
</div>
<ul style="margin: 0 0 12px 0;">
  <li>Built by the team behind <a href="https://atomic.chat/?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_ripple_65b_preview&utm_content=bullet_app">Atomic Chat</a>, the app that runs open-weight models locally and offline.</li>
  <li>Runs on stock llama.cpp <a href="https://github.com/ggml-org/llama.cpp/releases/tag/b12167">b12167</a> or newer, no patch: Ripple support was merged in <a href="https://github.com/ggml-org/llama.cpp/pull/31692">PR #31692</a>. Apps that bundle an older llama.cpp, LM Studio and Ollama among them, load these files once they move to b12167 or newer.</li>
</ul>
<hr style="margin: 0 0 16px 0;">

[Ripple-65B Preview](https://huggingface.co/ricursiveAI/Ripple-65B-Preview) is a 65B dense model trained from scratch by Ricursive Intelligence on 12T tokens, post-trained for agentic coding, Apache-2.0. This repo has GGUF files of it for llama.cpp.

## Pick a file

AD (Atomic Dynamic) files use our per-tensor layouts, quantized with an importance matrix computed on the BF16 weights over our public 4.7M-token [calibration build](https://huggingface.co/datasets/AtomicChat/calib-corpora/tree/main/builds/ripple-65b), rendered with Ripple's own chat template. File names are `Ripple-65B-Preview-<name>.gguf`; for a split file, point llama.cpp at the first part.

| file | GB on disk | bpw | suggested hardware | mean KLD | 99th pct KLD | same top token |
|---|---:|---:|---|---:|---:|---:|
| `BF16` (3 parts) | 129.6 | 16.00 | the original weights, bit-exact | 0 | 0 | 100% |
| `Q8_0` (2 parts) | 68.8 | 8.50 | 128 GB Macs, DGX Spark | 0.0010 | 0.011 | 99.0% |
| `AD-Q6_K` (2 parts) | 57.7 | 7.12 | 64 GB+ with long context | 0.0016 | 0.016 | 98.7% |
| `AD-Q5_K_M` | 47.9 | 5.92 | 64 GB Macs | 0.0067 | 0.090 | 97.3% |
| `AD-Q4_K_M` | 40.4 | 4.99 | 48 GB (2x 24 GB GPUs, 48 GB Macs) | 0.0136 | 0.172 | 95.9% |
| `AD-IQ4_XS` | 38.7 | 4.78 | 48 GB, more room for context | 0.0149 | 0.177 | 95.6% |
| `AD-IQ3_S` | 32.4 | 4.00 | 36-48 GB | 0.0327 | 0.374 | 93.4% |
| `AD-IQ3_XXS` | 28.0 | 3.45 | 32 GB (RTX 5090) | 0.0584 | 0.628 | 91.2% |
| `AD-IQ2_S` | 25.3 | 3.13 | 32 GB, more room for context | 0.0959 | 1.012 | 88.5% |
| `AD-IQ2_XS` | 22.1 | 2.73 | 24-32 GB | 0.1778 | 1.777 | 84.2% |
| `AD-IQ2_XXS` | 20.0 | 2.47 | 24 GB (RTX 3090 / 4090) | 0.2605 | 2.465 | 80.8% |
| `AD-IQ1_M` | 18.5 | 2.28 | research, see below | 0.3743 | 3.219 | 76.8% |
| `Q4_K_M` (plain llama.cpp preset, no imatrix) | 38.8 | 4.79 | baseline | 0.0380 | 0.447 | 93.0% |

The suggested hardware leaves room for a moderate context; long contexts need more memory for the KV cache. "Same top token" is how often the file picks the same next token as the BF16 original; "mean KLD" is the KL divergence of its next-token distribution from BF16's. Both are measured with `llama-perplexity` on our 30-language neutral corpus (87 chunks of 4096 tokens), llama.cpp `9e2a04a` with the port, 8x A100 40 GB.

At the size of the plain llama.cpp Q4_K_M (38.8 GB), `AD-IQ4_XS` (38.7 GB) has 2.5x lower mean KLD (0.0149 against 0.0380) and matches the original's token choice 95.6% of the time against 93.0%. `AD-IQ3_S` reaches the plain Q4_K_M's quality at 6.4 GB less. The plain file stays in the repo for now as the baseline.

`AD-IQ1_M` is a research file: a 1-bit-class layout that matches the original's token choice 76.8% of the time, below `AD-IQ2_XXS` (80.8%) for only 1.5 GB less.

Speed, one run: the plain Q4_K_M with `llama-cli` on 1x GH200 96 GB processes the prompt at 309 tokens/s and generates 40.6 tokens/s.

## Run it

Use llama.cpp [b12167](https://github.com/ggml-org/llama.cpp/releases/tag/b12167) or newer: a [release build](https://github.com/ggml-org/llama.cpp/releases) for your platform, or from source:

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build -DGGML_CUDA=ON          # Mac: drop -DGGML_CUDA=ON (Metal is on by default)
cmake --build build -j --config Release --target llama-server llama-cli
```

Then serve a file (the chat template with tools and `<think>` reasoning is embedded in it, so pass `--jinja`):

```bash
./build/bin/llama-server -m Ripple-65B-Preview-AD-Q4_K_M.gguf --jinja -c 32768 -ngl 99
```

Ricursive publishes no default sampling settings for the Preview.

These files were made and measured with llama.cpp `9e2a04a` and our port (`ricursive-port.patch`, kept in this repo). The merged upstream support uses the same tensor names and keys, so the files load unchanged. Checked on b12167 built from source with no patch, 1x A100 40 GB: `AD-IQ2_XXS` loads in `llama-server --jinja`, answers a coding prompt and stops on its own, and makes a correct tool call.

## llama.cpp support

We wrote llama.cpp's support for Ripple, and it was merged upstream in [PR #31692](https://github.com/ggml-org/llama.cpp/pull/31692) (first release: b12167). It adds the `ricursive` architecture: 80 blocks with four RMSNorms each (pre and post attention, pre and post FFN), per-head Q/K RMSNorm, an elementwise sigmoid gate on the attention output (`g_proj`), a value residual (each block's V input mixes the scaled token embeddings back in with a learned weight), sliding-window attention (1024 tokens, RoPE) on four blocks of five and full attention without positional encoding on the fifth, SwiGLU with the gate and up activations clamped at 20, and the embeddings scaled by sqrt(5120). No new ggml op.

How we checked it against Ricursive's own `modeling_ricursive.py` (fp32, transformers 4.57.6), with llama.cpp in F32 on the same token ids:

| check | mean KLD | same top token |
|---|---:|---:|
| random 10-block checkpoint, sliding window 8, clamp 0.5 (every code path), ctx 64 | 0.000000 | 100.00% |
| the first 10 real blocks of Ripple-65B Preview + its head, ctx 512 | 0.000000 | 100.00% |

Also: `test-llama-archs -a ricursive` passes on CPU, and llama-server renders the chat template byte for byte like `apply_chat_template` (plain, system, multi-turn with reasoning, tools, parallel tool calls with results).

## Model facts

| | |
|---|---|
| parameters | 65B, dense |
| layers | 80 (64 sliding-window + 16 global) |
| hidden / FFN | 5120 / 40960 |
| attention | 80 query heads, 8 KV heads, head dim 128 |
| context | up to 1M tokens per Ricursive (config: 2,097,152) |
| vocabulary | 100,352 (OLMo/cl100k-style BPE) |
| license | Apache-2.0 (`LICENSE` in this repo, from the base model) |

Quantized by AtomicChat.
