---
license: apache-2.0
base_model: google/gemma-4-12B-it
library_name: transformers
pipeline_tag: text-generation
tags: [gemma4, coding, code, reasoning, thinking, safetensors, transformers]
---

# 💻 Gemma4-12B-Coder — **safetensors master (full precision)** ✨
### Composer 2.5 × Fable 5 · v1 / code edition

> **This is the full-precision `safetensors` master** for my Gemma 4 12B coding fine-tune — the same model many of
> you have been running as GGUF, now in its original weights. 🧠💻 A focused fine-tune of Gemma 4 12B on
> **verifiable Python coding** data: it reasons in the open (edge cases, complexity, approach) and then writes a
> clean, runnable solution.

---

## 🎯 What this repo is for

This repo holds the **un-quantized master weights** (`model.safetensors`, bf16). Use it to:

- 🔧 **Roll your own quants** — make custom GGUF / **MLX** / AWQ / GPTQ builds from full precision.
- 🧪 **Fine-tune further** — it's a clean base for your own LoRA / continued training.
- 🤗 **Run it in `transformers`** (needs a recent build with `gemma4_unified` support).

> 🏃 **Just want to run it?** You don't need this repo — grab a ready-made quant from the
> **[GGUF repo →](https://huggingface.co/yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF)** (runs in ~4.5 GB of
> VRAM / unified memory in LM Studio, Ollama, llama.cpp, Jan…). This master is for *builders*. 💚

---

## 📌 Announcements

**🚀 v2 is almost here!** Initial training of **v2 is done** and it's in **benchmarking + final QA**. So many of you
flagged the **agentic** behavior — so this round I **significantly grew the dataset (especially agentic data)**.
**v2 is focused on agentic + coding.** Targeting a release **this Friday or Saturday (US Pacific).** 🎉

**📣 Context length is 256K.** This master ships with the corrected `max_position_embeddings = 262144` (256K) — the
well-known upstream Gemma 4 metadata bug (`config.json` once said `131072`) is **already fixed here**, so anything you
quantize/convert from these weights inherits the full 256K. 💚 Thanks to the community member who spotted it!

---

## 🤗 Run it in transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

repo = "yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1"
tok = AutoTokenizer.from_pretrained(repo)
model = AutoModelForCausalLM.from_pretrained(repo, torch_dtype=torch.bfloat16, device_map="auto")

msgs = [{"role": "user", "content": "Write a Python function to check if a string is a valid IPv4 address."}]
inputs = tok.apply_chat_template(msgs, add_generation_prompt=True, return_tensors="pt").to(model.device)
out = model.generate(inputs, max_new_tokens=1024)
print(tok.decode(out[0][inputs.shape[-1]:], skip_special_tokens=True))
```

> 🧠 **Thinking mode:** it thinks in Gemma's native thought channel before answering (keep `enable_thinking=true`,
> the default chat template handles it). Recommended sampling: `temp 1.0, top_p 0.95, top_k 64`; for coding you can
> also go greedy (`temp 0`) for more deterministic solutions. Needs a **recent `transformers`** that knows the
> `gemma4_unified` architecture.

---

## 📦 Ready-made GGUF quants

All from the **[GGUF repo](https://huggingface.co/yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF)**:

| Quant | Size | Vibe |
|------|------|------|
| 🟢 [**Q2_K**](https://huggingface.co/yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF/blob/main/gemma4-coding-Q2_K.gguf) | **4.5 GB** | tiniest — runs almost anywhere |
| 🟡 [**Q3_K_M**](https://huggingface.co/yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF/blob/main/gemma4-coding-Q3_K_M.gguf) | **5.7 GB** | great for 8 GB VRAM |
| 🔵 [**Q4_K_M**](https://huggingface.co/yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF/blob/main/gemma4-coding-Q4_K_M.gguf) | **6.87 GB** | the sweet spot 👌 (recommended) |
| 🟣 [**Q6_K**](https://huggingface.co/yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF/blob/main/gemma4-coding-Q6_K.gguf) | **9.11 GB** | near-lossless |
| ⚪ [**Q8_0**](https://huggingface.co/yuxinlu1/gemma-4-12B-coder-fable5-composer2.5-v1-GGUF/blob/main/gemma4-coding-Q8_0.gguf) | **11.8 GB** | basically full quality |

> ⚠️ GGUF needs a **recent llama.cpp** — this is the `gemma4_unified` architecture, older builds won't load it.

---

## ⚡ Optional: free speed with MTP (lossless)

There's a tiny **Gemma 4 MTP draft model** in my main reasoning repo →
**[`MTP/` folder](https://huggingface.co/yuxinlu1/gemma-4-12B-it-Claude-4.6-4.8-Opus-GGUF/tree/main/MTP)**. It's the
**stock Gemma 4 drafter**, so it pairs with **any** Gemma 4 12B quant — including these coder quants — for
**lossless speculative decoding** (byte-for-byte identical output, just faster). Because it's trained on base Gemma 4,
the hit-rate on this fine-tune is a bit lower than on vanilla Gemma 4, but it's free and has no downside. Add three
flags (`--model-draft`, `--spec-type draft-mtp`, `--n-gpu-layers-draft`); see the
[main repo](https://huggingface.co/yuxinlu1/gemma-4-12B-it-Claude-4.6-4.8-Opus-GGUF) for the full command. 🏎️

---

## 📚 Training data (the interesting part 🍳)

A **distillation** of two complementary chain-of-thought sources over verifiable Python coding tasks
(algorithmic / function-level problems with deterministic tests):

- **🥇 Main — Composer 2.5 *real* CoT.** Genuine model-authored reasoning traces; each solution was **run against the
  task's tests and only passing ones were kept**. The reasoning you learn from leads to code that *actually works*.
- **🥈 Aux — Fable 5 redo.** The problems where Composer 2.5 got it **wrong**, handed to Fable 5 to *re-derive* a fresh,
  self-consistent CoT and a correct solution — again **gated on passing the tests**. Recovers the hard cases the main
  teacher missed. These are synthetic (rationalized) CoT and are tagged separately.

Real CoT for solid coverage + synthetic "second-attempt" CoT to patch the failures — **all verified by execution**
before training. ✅

---

## ⚠️ Good to know
- **Reduced refusals:** task-focused training with no safety hedging, so it refuses less than the base model. It is
  **not** safety-aligned — add your own guardrails for production. Use responsibly. 🙏
- Specialized for **Python / algorithmic** coding; general-knowledge facts/numbers should still be double-checked.
- English-centric.

---

## 📚 Base & License
- **License: Apache 2.0.** Gemma 4 is released by Google under
  **[Apache 2.0](https://ai.google.dev/gemma/apache_2)** (unlike the older Gemma 1/2/3 terms), so this fine-tune is
  **Apache 2.0** too — free to use, modify, and redistribute. 🎉
- **Base model:** [`google/gemma-4-12B-it`](https://huggingface.co/google/gemma-4-12B-it).
- Personal/hobby project — shared as-is, no warranty. Have fun, and happy hacking! 🐾✨
