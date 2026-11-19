---
base_model: tencent/Hy4-flash
base_model_relation: quantized
quantized_by: AtomicChat
pipeline_tag: image-text-to-text
library_name: gguf
license: other
license_name: tencent-hy-license
license_link: LICENSE
tags:
- gguf
- llama.cpp
- hunyuan
- hy4-flash
- moe
- quantized
- conversational
- vision
- atomic-chat
---

# Hy4-flash for 64 GB machines
<p style="margin-top: 0; margin-bottom: 0;">
  <em>Tencent's 220B Hy4-flash with 49 GB of weights in memory: the experts at ~2.3 bits, everything else at Q8_0, the Engram n-gram table in a file of its own that stays on the SSD.</em>
</p>
<div style="display: flex; gap: 8px; align-items: center; margin-top: 10px; margin-bottom: 10px;">
  <a href="https://atomic.chat/?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_hy4_flash&utm_content=btn_atomic"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_atomic.png" width="162" alt="Atomic Chat"></a>
  <a href="https://discord.gg/8wGSsvmg4V"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_discord.png" width="119" alt="Discord"></a>
  <a href="https://github.com/AtomicBot-ai/Atomic-Chat"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_github.png" width="115" alt="GitHub"></a>
  <a href="https://x.com/atomic_chat_hq"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_x.png" width="108" alt="X"></a>
</div>
<ul style="margin: 0 0 12px 0;">
  <li>Built by the team behind <a href="https://atomic.chat/?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_hy4_flash&utm_content=bullet_app">Atomic Chat</a>, the app that runs open-weight models locally and offline.</li>
  <li>Needs llama.cpp with Hy4-flash support: the open PR <a href="https://github.com/ggml-org/llama.cpp/pull/32517">ggml-org/llama.cpp#32517</a>, tested at <code>0a054d0b</code>. Stock llama.cpp, LM Studio and Ollama do not load these files yet.</li>
</ul>
<hr style="margin: 0 0 16px 0;">

[Hy4-flash](https://huggingface.co/tencent/Hy4-flash) is Tencent's Mixture-of-Experts model with 220B parameters: 155.5B in the network itself (512 routed experts, 16 active per token, 11.3B active parameters in all) and 63.5B in Engram, a table of learned bigram and trigram embeddings looked up by hash. It reads text and images and has a 1M-token context.

The Engram table is read row by row, a few kilobytes per token, so it can stay on disk. What has to fit in memory is the rest. Tencent's own GGUF builds ([AngelSlim/Hy4-flash-GGUF](https://huggingface.co/AngelSlim/Hy4-flash-GGUF)) keep 72–105 GB of it in memory and are the better choice on 96 GB and 128 GB machines. This repo has one file built for 64 GB: 49.1 GB of weights, the table in a second file.

## Files

| file | what is in it | GB on disk |
|---|---|---:|
| `Hy4-flash-AD-IQ2_S-IQ2_XXS-00001-of-00002.gguf` | everything but the Engram table: routed experts with down projections at IQ2_S and gate/up at IQ2_XXS, everything else at Q8_0 (2.52 bits per weight) | 49.05 |
| `Hy4-flash-AD-IQ2_S-IQ2_XXS-00002-of-00002.gguf` | the Engram table, Q4_0 (660M rows of 96) | 35.64 |
| `mmproj-Hy4-flash-F16.gguf` | the vision projector, for image input | 0.97 |

Point llama.cpp at the first part; it loads the second by itself. With the vision projector and a 32K context, `llama-server` held 51.4 GB of GPU memory on our CUDA box. We have not measured it on a Mac.

## Quality

Measured against our BF16 conversion of the original weights with `llama-perplexity` on our 30-language neutral corpus (104 chunks of 4096 tokens), llama.cpp PR #32517 at `0a054d0b`, 8x A100 80 GB. "Same top token" is how often the file picks the same next token as BF16; "mean KLD" is the KL divergence of its next-token distribution from BF16's.

| file | in memory | GB on disk | mean KLD | 99th pct KLD | same top token |
|---|---:|---:|---:|---:|---:|
| Q8_0 (ours, not published) | 165.5 | 232.8 | 0.136 | 2.92 | 91.8% |
| Tencent `Q4_K_M` | 105.0 | 168.4 | 0.198 | 4.18 | 89.3% |
| Tencent `IQ2-AH` | 71.6 | 135.0 | 0.651 | 8.73 | 77.9% |
| **`AD-IQ2_S-IQ2_XXS` (this repo)** | **49.1** | **84.7** | **0.725** | **9.08** | **76.4%** |

"In memory" is everything but the Engram table. Tencent's files also carry a multi-token-prediction block from their internal export, which the public checkpoint does not have.

This model loses more to quantization than most. Even Q8_0 picks a different top token than BF16 on 8.2% of tokens, where most models stay above 98% agreement. The losses are concentrated: Tencent's `Q4_K_M` has a median KLD of 0.008, so most tokens come out nearly exact and a minority diverge a lot. Our reading is that small rounding differences change which 16 of the 512 experts the router picks. Read the table as a ranking.

On that scale, this file needs 22.5 GB less memory than Tencent's smallest file and gives up 1.4 points of top-token agreement. Tencent reports its `IQ2-AH` between 2 and 6.5 points below BF16 on its own agent and coding benchmarks; we have not run task benchmarks on this file.

Treat it as an experimental build: it brings the model to 64 GB machines, with the losses above.

## What we checked by hand

`llama-server --jinja` with this file and the vision projector, temperature 0 unless noted:

- **English:** short factual answers and arithmetic were correct.
- **Reasoning on (the default):** a reasoning puzzle, answered correctly.
- **Chinese:** a two-sentence answer in Chinese.
- **Code:** a correct Python function.
- **Images:** a test image described correctly: shapes, colours, their positions, and the text on it.
- **Tool calls:** with reasoning on, the model called the provided tool. With `reasoning_effort` set to `no_think` it answered in prose instead of calling the tool. Our Q8_0 called it in both modes. For agents, keep reasoning on.

Speed on 4x A100 80 GB (layers split across the cards, the Engram table on the host): about 23 to 26 tokens/s of generation. This is not a Mac number; Tencent reports 48 to 50 tokens/s for its `Q4_K_M` and `Q3_K` on an M5 Max 128 GB.

## How to run

Build llama.cpp from the PR:

```bash
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
git fetch origin pull/32517/head:hy4-flash && git checkout 0a054d0b
cmake -B build && cmake --build build --config Release -j
```

Serve it, with the Engram table kept on the host side:

```bash
./build/bin/llama-server -m Hy4-flash-AD-IQ2_S-IQ2_XXS-00001-of-00002.gguf --mmproj mmproj-Hy4-flash-F16.gguf \
  -ngl 99 -ot 'per_layer_token_embd\.weight=CPU' -c 32768 --jinja --temp 0.9 --top-p 1.0
```

Reasoning is on by default; for direct answers add `--chat-template-kwargs '{"reasoning_effort":"no_think"}'`. Temperature 0.9 and top-p 1.0 are Tencent's recommended sampling.

On a 64 GB Mac, let the GPU use more of the memory before starting: `sudo sysctl iogpu.wired_limit_mb=57344` (resets on reboot).

The PR is not merged yet. If its format changes before the merge, we will update these files.

## How it was made

- **Conversion.** From the BF16 safetensors of `tencent/Hy4-flash` (revision `d88c9dfd`) with the PR's converter. The public checkpoint names a few things differently from what that converter expects: the architecture names, the sparse-attention layer type, the Engram token map shipped as a tensor, and no `engram_enable` flag. Without changes the converter refuses the checkpoint, or drops the Engram layers if only the names are fixed. `conversion/prep.py` and `conversion/hy4-flash-public-ckpt.patch` in this repo make the mapping.
- **Check against Tencent's GGUF.** The Engram token map and hash parameters are identical, and all 1,171 tensors that Tencent's `IQ2-AH` keeps unquantized match ours byte for byte.
- **Importance matrix.** Computed on the BF16 weights over 1,114 chunks of 512 tokens (about 570k tokens). That is an even eighth of our 4.56M-token [calibration build](https://huggingface.co/datasets/AtomicChat/calib-corpora/tree/main/builds/hy4-flash-moe), rendered with Hy4-flash's chat template; the long-context part was not used. Every routed expert received data: at least 69 tokens, median about 11,000.
- **Layout.**
  - Routed experts: gate/up at IQ2_XXS, down at IQ2_S.
  - At Q8_0: attention, the shared expert, the latent projections around the experts, the sparse-attention indexer, the Engram projections, the embeddings and the output head.
  - At F32: the hyper-connection matrices.
  - The Engram table at Q4_0.
- **Table precision barely matters here.** With the same weights and the table at Q4_0, F8_E4M3 or Q8_0, mean KLD is 0.7255, 0.7203 and 0.7204.
- **Other 64 GB layouts we measured:**
  - down at IQ2_XS (47.5 GB in memory): 0.754 mean KLD, 75.7% same top token;
  - gate/up at IQ1_M with down at IQ3_XXS (48.3 GB): 0.919 and 72.9%.
- **Not included.** The DFly2 speculative drafter, which llama.cpp does not support.

All logs, the importance matrix and the hand checks are in [AtomicChat/Hy4-flash-GGUF-metrics](https://huggingface.co/datasets/AtomicChat/Hy4-flash-GGUF-metrics).

## License and credits

Hy4-flash is made by Tencent and released under the Tencent Hy License ([LICENSE](LICENSE) in this repo). It is Apache 2.0 with additional commercial terms: a separate license from Tencent is required for model-as-a-service businesses above US$50M annual revenue or for products above 100M monthly active users. These GGUF files are derived from it and carry the same license. Quantized by AtomicChat.
