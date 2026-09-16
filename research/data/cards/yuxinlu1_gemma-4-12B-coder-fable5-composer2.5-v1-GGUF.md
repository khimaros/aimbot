---
license: apache-2.0
base_model: google/gemma-4-12B-it
library_name: gguf
pipeline_tag: text-generation
tags: [gemma4, coding, code, reasoning, thinking, gguf, llama.cpp, local-llm]
---

# 💻 Gemma4-12B-Coder (GGUF) — Composer 2.5 × Fable 5 ✨
### 🐣 Tiny footprint, big brain — a local **coding** model for *everyone*

> **No matter your GPU. No matter your RAM.** If you've got **~4.5 GB** of VRAM *or* unified memory free,
> you can run your own private, offline coding assistant right now. 🚀
> This is the **v1 / code edition** — distilled from **real chain-of-thought** so it *thinks through* a problem
> before writing the solution. 🧠💻 All local, all yours, no API, no cloud.

### 🎯 What it is
A focused fine-tune of Gemma 4 12B on **verifiable Python coding** data — every training example's reasoning leads to
code that **actually passed its tests**. The result reasons in the open (edge cases, complexity, approach) and then
emits a clean, runnable solution. 💚

---

## 📌 Announcements

**🚀🔥 IT'S HERE — v2 is OUT NOW!** v2 has shipped — the **GGUF quants are live and ready to run** →
**[grab v2 here](https://huggingface.co/yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF)**. 🎉
The **full `safetensors` master** (build / fine-tune on top) goes up **tomorrow**. v2 is **agentic + coding** focused —
the piece v1 was missing.

**Here's the result that got me most excited.** When I saw v2's **tau2-bench `telecom`** result — an agentic tool-use
benchmark where the model has to *diagnose → fix → verify*, exactly like real terminal/debugging work — I literally got
**launched out of my chair** (…okay, *kidding* 😄). The jump in **actually solving the problem** is wild:

| tau2-bench **telecom** · local, same harness, **Q8_0** | score |
|---|---|
| official `gemma-4-12B-it` (base) | **~15%** |
| 🟢 **v2 (this release)** | **~55%** |

The base model tends to **give up early** (hands the problem off to a human); **v2 keeps going** and works it the way a
much bigger model would. Full benchmark details are in the **[v2 card](https://huggingface.co/yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF)** now. 🔧

**✅ safetensors master (this v1 model) is UP.** Full-precision weights are live →
**[yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1](https://huggingface.co/yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1)**
— roll your own GGUF / MLX / AWQ quants or fine-tune straight from the master. 🎉

---

## 📣 Context length fixed: now **256K** (was 131K) — thanks, community! 💚

A community member spotted that this model was reporting only a **131K** context window. That turned out to be
the well-known upstream **Gemma 4 metadata bug** — Google's initial `config.json` shipped with
`max_position_embeddings: 131072` instead of the real **262144 (256K)**, and that value got baked into a lot of
downstream finetunes and quants (including this one) before it was fixed upstream.

The weights were always fine — it was purely a metadata field. **All GGUF quants have been re-patched to the
full 256K context** (`gemma4.context_length = 262144`). Just re-download if you grabbed an earlier copy. 🙏

---

## 📚 Training data (the interesting part 🍳)

This is a **distillation** of two complementary chain-of-thought sources, both over verifiable Python coding tasks
(algorithmic / function-level problems that come with deterministic tests):

- **🥇 Main set — Composer 2.5 *real* CoT.** Genuine, model-authored reasoning traces. The teacher solved each problem,
  its code was **run against the task's tests, and only the passing solutions were kept**. So the reasoning you're
  learning from leads to code that *actually works*.
- **🥈 Aux set — Fable 5 (released today! 🎉).** A clever twist: we took the problems where **Composer 2.5 got it wrong**
  and handed them to **Fable 5** to *redo* — re-deriving a fresh, self-consistent chain-of-thought and a correct
  solution, again **gated on passing the tests**. This recovers the hard cases the main teacher missed. These traces
  are **synthetic** (rationalized CoT), and are tagged separately so the two sources stay distinguishable.

The recipe: real CoT for the bulk of solid coverage, plus synthetic "second-attempt" CoT to patch the failures —
both verified by execution before anything entered training. ✅

---

## 📦 Pick your size (GGUF quants)

| Quant | Size | Vibe |
|------|------|------|
| 🟢 **Q2_K** | **4.5 GB** | tiniest — runs almost anywhere |
| 🟡 **Q3_K_M** | **5.7 GB** | great for 8 GB VRAM — much better than Q2 |
| 🔵 **Q4_K_M** | **6.87 GB** | the sweet spot 👌 (recommended) |
| 🟣 **Q6_K** | **9.11 GB** | near-lossless |
| ⚪ **Q8_0** | **11.8 GB** | basically full quality |

---

## 🧮 "Will it fit?" — context length cheat-sheet

Rough estimates 🤓 (assumes `q8_0` KV cache + ~1.5 GB overhead; **use `q4_0` KV cache for ≈2× more context!**).
Max context is **256K**. "—" = won't fit, pick a smaller quant. ✂️

| Your VRAM / unified mem | 🟢 Q2_K (4.5G) | 🟡 Q3_K_M (5.7G) | 🔵 Q4_K_M (6.87G) | 🟣 Q6_K (9.11G) | ⚪ Q8_0 (11.8G) |
|---|---|---|---|---|---|
| **8 GB**  | ~16K ctx | ~10K | tight (~2–4K) | — | — |
| **12 GB** | ~48K | ~38K | ~30K | ~12K | — |
| **16 GB** | ~80K | ~72K | ~64K | ~44K | ~22K |
| **24 GB** | ~200K | ~160K | ~128K | ~110K | ~88K |
| **32 GB** | 256K (max) 🎉 | 256K | 256K | ~230K | ~190K |

> 💡 Apple Silicon / integrated GPUs with **unified memory** count too — same numbers, just slower than a dGPU.
> 💡 Low on room? Drop a quant or switch KV cache to `q4_0` and your context roughly doubles.

---

## 🚀 How to run it (super easy)

### Option A — llama.cpp (recommended) 🦙
1. Grab a quant above (e.g. `…-Q4_K_M.gguf`) and `llama-server` from [llama.cpp](https://github.com/ggml-org/llama.cpp).
   > ⚠️ Needs a **recent llama.cpp** (this is the `gemma4_unified` architecture — older builds won't load it).
2. Run a server (Windows `.bat` shown — tweak `--port`, `--ctx-size` to taste):

```bat
@echo off
cd /d C:\llama.cpp
llama-server.exe ^
  -m C:\models\gemma4-coding-Q4_K_M.gguf ^
  --ctx-size 16384 ^
  --n-gpu-layers 99 ^
  --no-mmap ^
  -fa on ^
  --cache-type-k q8_0 --cache-type-v q8_0 ^
  --temp 1.0 --top-p 0.95 --top-k 64 ^
  --host 0.0.0.0 --port 18080
pause
```
3. Open `http://localhost:18080` and chat. 🎉  (Tip: bump `--ctx-size` per the table; use `q4_0` KV for more.)

### Option B — one-click apps 🖱️
Works in **LM Studio**, **Jan**, **Ollama**, etc. — just import the GGUF, pick your quant, go. 🐾

### 🧠 Thinking mode
This model thinks in Gemma's native thought channel before answering — exactly how it was trained. Keep
**`enable_thinking=true`** (the default chat template handles it). Recommended sampling: `temp 1.0, top_p 0.95, top_k 64`.
For coding you can also go greedy (`temp 0`) for more deterministic solutions.

---

## ⚠️ Good to know
- **Reduced refusals:** the training data is task-focused with no safety hedging, so this refuses less than the base
  model. It is **not** safety-aligned — add your own guardrails for production. Use responsibly. 🙏
- Specialized for **Python / algorithmic** coding. Reasoning quality is strongest in that domain; general-knowledge
  facts/numbers should still be double-checked.
- English-centric.

---

## 📚 Base & License
- **License: Apache 2.0.** Gemma 4 is released by Google under
  **[Apache 2.0](https://ai.google.dev/gemma/apache_2)** (unlike the older Gemma 1/2/3 terms), so this fine-tune is
  **Apache 2.0** too — free to use, modify, and redistribute. 🎉
- **Base model:** [`google/gemma-4-12B-it`](https://huggingface.co/google/gemma-4-12B-it).
- Personal/hobby project — shared as-is, no warranty. Have fun, and happy hacking! 🐾✨
