---
base_model: Nanbeige/Nanbeige4.3-33B
base_model_relation: quantized
quantized_by: AtomicChat
pipeline_tag: text-generation
library_name: gguf
license: apache-2.0
language:
- en
- zh
tags:
- atomic-dynamic
- gguf
- llama.cpp
- nanbeige
- imatrix
- quantized
- agent
- reasoning
- conversational
- atomic-chat
---

# Nanbeige4.3-33B · GGUF
<p style="margin-top: 0; margin-bottom: 0;">
  <em>GGUF quants of Nanbeige's Nanbeige4.3-33B, built from Nanbeige's original BF16 weights on release day.</em>
</p>
<div style="display: flex; gap: 8px; align-items: center; margin-top: 10px; margin-bottom: 10px;">
  <a href="https://atomic.chat/?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_nanbeige4_3_33b&utm_content=btn_atomic"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_atomic.png" width="162" alt="Atomic Chat"></a>
  <a href="https://discord.gg/8wGSsvmg4V"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_discord.png" width="119" alt="Discord"></a>
  <a href="https://github.com/AtomicBot-ai/Atomic-Chat"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_github.png" width="115" alt="GitHub"></a>
  <a href="https://x.com/atomic_chat_hq"><img src="https://huggingface.co/AtomicChat/Qwen3.8-27B-GGUF/resolve/main/btn_x.png" width="108" alt="X"></a>
</div>
<ul style="margin: 0 0 12px 0;">
  <li><a href="https://huggingface.co/Nanbeige/Nanbeige4.3-33B">Nanbeige4.3-33B</a> is Nanbeige's 33B dense agent and reasoning model (Llama architecture, 512K context, thinking on by default), Apache-2.0.</li>
  <li>You can now run Nanbeige4.3-33B in <a href="https://atomic.chat/?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_nanbeige4_3_33b&utm_content=bullet_app">Atomic Chat</a>, with thinking on by default.</li>
  <li><b>Atomic Dynamic</b> (AD) files with our own importance matrix, from 13.7 GB to 30.1 GB on disk, plus plain <code>Q8_0</code> and <code>Q5_K_M</code>; every one measured against the BF16 original on one stand.</li>
</ul>
<hr style="margin: 0 0 16px 0;">

> [!NOTE]
> **Built on release day, 25 October.** `Q8_0` and `Q5_K_M` are llama.cpp's own
> presets, made without an importance matrix; its `Q6_K` and `Q4_K_M` were up
> for the first hours and are removed now that `AD-` files beat them at the same
> size (their numbers stay below as the baseline). The `AD-` files
> use our own importance matrix, collected on the BF16 weights (`--parse-special`)
> over 8,000 chunks of 512 tokens of our calibration corpus. The corpus build was
> rendered for Qwen3.8-27B, whose chat format (ChatML) Nanbeige4.3 shares; it is
> `imatrix/imatrix.gguf` in the metrics repo.

## Pick a file

`KL divergence` is how far the quantized model's predictions drift from the
original BF16 weights. Lower is better, and zero means identical. `top-1` is how
often it picks the same next token the original would have picked. Every file
was measured on the same stand: our neutral multilingual text, 24 chunks of
4,096 tokens, llama.cpp `36e36e6`. Raw logs and the importance matrix are in
[the metrics repo](https://huggingface.co/datasets/AtomicChat/Nanbeige4.3-33B-GGUF-metrics).

| File | Size on disk | Built | KL divergence | top-1 |
|---|---:|---|---:|---:|
| [Nanbeige4.3-33B-Q8_0.gguf](https://huggingface.co/AtomicChat/Nanbeige4.3-33B-GGUF/blob/main/Nanbeige4.3-33B-Q8_0.gguf) | 35.2 GB | plain 8-bit | 0.0032 | 98.0% |
| [Nanbeige4.3-33B-AD-Q6_K.gguf](https://huggingface.co/AtomicChat/Nanbeige4.3-33B-GGUF/blob/main/Nanbeige4.3-33B-AD-Q6_K.gguf) | 30.1 GB | Atomic Dynamic, our imatrix | 0.0052 | 97.5% |
| [Nanbeige4.3-33B-AD-Q6_K-Q5_K.gguf](https://huggingface.co/AtomicChat/Nanbeige4.3-33B-GGUF/blob/main/Nanbeige4.3-33B-AD-Q6_K-Q5_K.gguf) | 27.9 GB | Atomic Dynamic, our imatrix | 0.0102 | 96.1% |
| [Nanbeige4.3-33B-AD-Q5_K_M.gguf](https://huggingface.co/AtomicChat/Nanbeige4.3-33B-GGUF/blob/main/Nanbeige4.3-33B-AD-Q5_K_M.gguf) | 24.7 GB | Atomic Dynamic, our imatrix | 0.0213 | 94.7% |
| [Nanbeige4.3-33B-Q5_K_M.gguf](https://huggingface.co/AtomicChat/Nanbeige4.3-33B-GGUF/blob/main/Nanbeige4.3-33B-Q5_K_M.gguf) | 23.5 GB | llama.cpp preset, no imatrix | 0.0304 | 93.4% |
| [Nanbeige4.3-33B-AD-Q5_K_M-Q4_K_M.gguf](https://huggingface.co/AtomicChat/Nanbeige4.3-33B-GGUF/blob/main/Nanbeige4.3-33B-AD-Q5_K_M-Q4_K_M.gguf) | 22.6 GB | Atomic Dynamic, our imatrix | 0.0332 | 93.1% |
| [Nanbeige4.3-33B-AD-Q4_K_M.gguf](https://huggingface.co/AtomicChat/Nanbeige4.3-33B-GGUF/blob/main/Nanbeige4.3-33B-AD-Q4_K_M.gguf) | 21.2 GB | Atomic Dynamic, our imatrix | 0.0380 | 92.6% |
| [Nanbeige4.3-33B-AD-IQ4_XS.gguf](https://huggingface.co/AtomicChat/Nanbeige4.3-33B-GGUF/blob/main/Nanbeige4.3-33B-AD-IQ4_XS.gguf) | 20.3 GB | Atomic Dynamic, our imatrix | 0.0462 | 92.0% |
| [Nanbeige4.3-33B-AD-IQ3_S.gguf](https://huggingface.co/AtomicChat/Nanbeige4.3-33B-GGUF/blob/main/Nanbeige4.3-33B-AD-IQ3_S.gguf) | 17.1 GB | Atomic Dynamic, our imatrix | 0.1019 | 87.5% |
| [Nanbeige4.3-33B-AD-IQ3_XXS.gguf](https://huggingface.co/AtomicChat/Nanbeige4.3-33B-GGUF/blob/main/Nanbeige4.3-33B-AD-IQ3_XXS.gguf) | 14.9 GB | Atomic Dynamic, our imatrix | 0.1593 | 84.6% |
| [Nanbeige4.3-33B-AD-IQ2_S.gguf](https://huggingface.co/AtomicChat/Nanbeige4.3-33B-GGUF/blob/main/Nanbeige4.3-33B-AD-IQ2_S.gguf) | 13.7 GB | Atomic Dynamic, our imatrix | 0.2448 | 80.5% |

Removed, measured on the same stand: llama.cpp's plain `Q6_K` (27.2 GB, KL
divergence 0.0165, top-1 95.5%) and `Q4_K_M` (20.1 GB, 0.0693, 89.9%).

> [!IMPORTANT]
> This model is unusually sensitive to quantization. llama.cpp's plain `Q6_K`
> picks the original's next token only 95.5% of the time (most models reach 98%
> at 6 bits) and plain `Q4_K_M` 89.9%. At about the same size on disk, the `AD-`
> files keep much more: `AD-IQ4_XS` (20.3 GB) has a third less KL divergence than
> `Q4_K_M` (20.1 GB), and `AD-Q6_K-Q5_K` (27.9 GB) 39% less than `Q6_K` (27.2 GB).
`AD-Q6_K` (30.1 GB) is within reach of `Q8_0` (97.5% against 98.0%). Below 4 bits
> the model loses a lot: `AD-IQ3_XXS` and `AD-IQ2_S` change the next token often
> (top-1 below 85%); use them only if nothing larger fits.

`AD-` marks an **Atomic Dynamic** layout: the FFN of the first and last layers
one step up, attention output and the head at `q6_k` or higher, the small key
and value projections at `q8_0`. The rest of the name is the type of the FFN up
projections. Compare files by size on disk, not by name.

## Run

llama.cpp:

```bash
llama-server -hf AtomicChat/Nanbeige4.3-33B-GGUF:AD-Q4_K_M --jinja -c 32768
```

Thinking is on by default. To turn it off:
`--chat-template-kwargs '{"enable_thinking": false}'`.

Nanbeige's recommended sampling: reasoning and chat `--temp 0.6 --top-p 0.95`;
agentic and tool use `--temp 1.0 --top-p 0.95`.

Or download a file and open it in [Atomic Chat](https://atomic.chat/?utm_source=huggingface&utm_medium=referral&utm_campaign=hf_nanbeige4_3_33b&utm_content=run).

## License and credits

The weights are Nanbeige's, released under Apache-2.0 (`LICENSE` in this repo).
Quantized by AtomicChat.
